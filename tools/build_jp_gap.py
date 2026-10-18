#!/usr/bin/env python3
"""Build jp-gap.json: Japanese card data for sets TCGdex is missing.

TCGdex (api.tcgdex.net) has some Japanese sets with no cards at all, and many more with cards but no pictures.
TCGCSV (tcgcsv.com, a free daily mirror of TCGplayer's catalog, category 85 "Pokemon Japan") has both, with
real Japanese card scans, so this script copies the part the app needs into a small static file. TCGCSV does not
allow requests from a web page, so the app can't call it live: re-run this script now and then to refresh.

    python tools/build_jp_gap.py

Also writes jp-en.json: English set names and English card names for every Japanese set that has a TCGplayer
group, so the app can show them next to the Japanese ones:
  { "v": 1, "built": "YYYY-MM-DD", "sets": { "<TCGdex set id>": { "n": "<English set name>", "c": { "003": "Ludicolo", ... } } } }

Output (jp-gap.json, next to index.html):
  { "v": 1, "built": "YYYY-MM-DD",
    "sets": { "<TCGdex set id>": { "name": "<TCGdex name>", "empty": 1 | 0,
              "c": [ [productId, "003", name, rarity, marketPrice], ... ] } } }
For sets TCGdex already has cards for, only the card numbers and product ids are kept (name/rarity/price blank).
The app ignores a set here as soon as TCGdex has real data for it.
"""
import json, re, sys, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date

TCGDEX = 'https://api.tcgdex.net/v2/ja'
CSV = 'https://tcgcsv.com/tcgplayer/85'

# TCGdex set id -> TCGCSV group name prefix, where the codes differ
MANUAL = {
    'XY5a': 'XY5-Bg: Gaia Volcano', 'XY5b': 'XY5-Bt: Tidal Storm',
    'XY8a': 'XY8-Bb: Blue Shock', 'XY8b': 'XY8-Br: Red Flash',
    'XY11a': 'XY11-Bb: Fever-Burst Fighter', 'XY11b': 'XY11-Br: Cruel Traitor',
    'L1a': 'L1: HeartGold Collection', 'L1b': 'L1: SoulSilver Collection',
}


def get(url):
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'megabinder-build'})
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception:
            pass
    return None


def group_code(g):
    m = re.match(r'^([A-Za-z0-9.+\-]+):', g['name'])
    return (g.get('abbreviation') or (m.group(1) if m else '')).lower()


def main():
    sets = get(f'{TCGDEX}/sets')
    with ThreadPoolExecutor(12) as ex:
        details = list(ex.map(lambda s: get(f"{TCGDEX}/sets/{urllib.parse.quote(s['id'])}"), sets))
    groups = get(f'{CSV}/groups')['results']
    by_code = {}
    for g in groups:
        by_code.setdefault(group_code(g), g)
    by_name = {g['name'].lower(): g for g in groups}

    matched = []   # (tcgdex set, detail, group) for every set with a TCGplayer group
    unmatched = []
    for s, d in zip(sets, details):
        if not d:
            continue
        g = by_name.get(MANUAL.get(s['id'], '').lower()) or by_code.get(s['id'].lower())
        if g:
            matched.append((s, d, g))
        else:
            cards = d.get('cards') or []
            unmatched.append((s['id'], 'empty' if not cards else 'no art' if not any(c.get('image') for c in cards) else 'ok'))

    def needs_gap(d):
        cards = d.get('cards') or []
        return not cards or any(not c.get('image') for c in cards)

    def fetch(item):
        s, d, g = item
        gid = g['groupId']
        prods = (get(f'{CSV}/{gid}/products') or {}).get('results', [])
        prices = {}
        if not (d.get('cards') or []):   # prices are only kept for sets TCGdex has no cards for
            for p in (get(f'{CSV}/{gid}/prices') or {}).get('results', []):
                if p.get('marketPrice') is not None:
                    prices[p['productId']] = max(prices.get(p['productId'], 0), p['marketPrice'])
        return prods, prices

    with ThreadPoolExecutor(8) as ex:
        fetched = list(ex.map(fetch, matched))

    out, en_out, total, n_names = {}, {}, 0, 0
    for (s, d, g), (prods, prices) in zip(matched, fetched):
        cards = d.get('cards') or []
        empty = not cards
        width = max((len(c['localId']) for c in cards), default=3)
        want = {c['localId'] for c in cards if not c.get('image')}
        rows, seen, names = [], set(), {}
        for p in prods:
            ext = {e['name']: e['value'] for e in p.get('extendedData', [])}
            num = (ext.get('Number') or '').split('/')[0].strip()
            if not num:
                continue   # sealed product, not a card
            if num.isdigit():
                num = num.zfill(width)
            name = re.sub(r'\s*-\s*\d+/[\w-]+\s*$', '', p['name']).strip()
            base = re.sub(r'\s*\([^)]*\)\s*$', '', name).strip() or name   # drop "(Master Ball Pattern)" style suffixes
            if base and (num not in names or len(base) < len(names[num])):
                names[num] = base
            if needs_gap(d) and num not in seen and (empty or num in want):
                seen.add(num)
                rows.append([p['productId'], num] + ([name, ext.get('Rarity', ''), prices.get(p['productId'])] if empty else []))
        if rows:
            rows.sort(key=lambda r: (not r[1].isdigit(), r[1]))
            out[s['id']] = {'name': d.get('name', ''), 'empty': 1 if empty else 0, 'c': rows}
            total += len(rows)
        if names:
            en_set = g['name'].split(':', 1)[1].strip() if re.match(r'^[^:]{1,14}:', g['name']) else g['name']
            en_out[s['id']] = {'n': en_set, 'c': dict(sorted(names.items()))}
            n_names += len(names)

    built = date.today().isoformat()
    with open('jp-gap.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'v': 1, 'built': built, 'sets': out}, f, ensure_ascii=False, separators=(',', ':'))
    with open('jp-en.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'v': 1, 'built': built, 'sets': en_out}, f, ensure_ascii=False, separators=(',', ':'))
    n_empty = sum(1 for v in out.values() if v['empty'])
    print(f"jp-gap.json: {len(out)} sets ({n_empty} empty on TCGdex, {len(out) - n_empty} missing pictures), {total} cards")
    print(f"jp-en.json: English names for {len(en_out)} sets, {n_names} cards")
    print('no TCGCSV match:', ', '.join(f'{i} ({why})' for i, why in unmatched))


if __name__ == '__main__':
    sys.exit(main())
