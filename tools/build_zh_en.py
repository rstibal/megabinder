#!/usr/bin/env python3
"""Build zh-en.json: English names for Traditional Chinese cards and sets.

TCGdex (api.tcgdex.net/v2/zh-tw) only has Chinese names. English names come from three places, in this order:
  1. Many Chinese sets share their code with a Japanese set (SV2D in both) and number their cards the same way, so
     the English name of that Japanese card (jp-en.json, built by tools/build_jp_gap.py: run that first) names the
     Chinese card. The same Chinese name always maps to the same English name, so the result is a plain
     "Chinese name -> English name" dictionary (the majority wins where a stray card disagrees).
  2. Pokemon not seen above: the Pokedex species list from PokeAPI (Traditional Chinese -> English), plus the rules
     suffix kept in Latin letters (V, VMAX, ex, GX...) and a few known prefixes (Radiant, Galarian...).
  3. Basic Energy cards.
Chinese sets that share a code with a Japanese set get that set's English name. The other sets are Chinese originals
(starter decks, collection sheets...) with no single Japanese equivalent, so they get none (matching them by card
overlap was tried: perfect on known sets, meaningless on these). Cards and sets without a match are left out.

    python tools/build_zh_en.py     # needs jp-en.json next to index.html

Output (zh-en.json): { "v": 1, "built": "YYYY-MM-DD", "names": { "<Chinese name>": "<English>" }, "sets": { "<set id>": "<English>" } }
"""
import collections, csv, io, json, re, sys, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date

TCGDEX = 'https://api.tcgdex.net/v2/zh-tw'
SPECIES = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species_names.csv'
PREFIX = {'光輝': 'Radiant ', '阿羅拉': 'Alolan ', '伽勒爾': 'Galarian ', '洗翠': 'Hisuian ', '帕底亞': 'Paldean ', '超級': 'Mega ', '原始': 'Primal '}
ENERGY = {'草': 'Grass', '火': 'Fire', '水': 'Water', '雷': 'Lightning', '超': 'Psychic', '鬥': 'Fighting', '惡': 'Darkness', '鋼': 'Metal', '妖': 'Fairy', '龍': 'Dragon'}


def get(url, raw=False):
    for _ in range(3):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'megabinder-build'}), timeout=60).read()
            return data if raw else json.loads(data)
        except Exception:
            pass
    return None


def derive(name, species):
    """English name from the Pokedex list: [Radiant ]Species[ suffix]; None when it isn't a plain Pokemon name."""
    m = re.match(r'^(.*?)\s*([A-Za-z][A-Za-z0-9\- ]*)?$', name.strip())
    base, suffix = m.group(1), (m.group(2) or '').strip()
    pre = ''
    for k, v in PREFIX.items():
        if base.startswith(k) and base[len(k):] in species:
            pre, base = v, base[len(k):]
            break
    if base not in species:
        return None
    return f"{pre}{species[base]}{' ' + suffix if suffix else ''}"


def main():
    with open('jp-en.json', encoding='utf-8') as f:
        jp = json.load(f)['sets']
    jp_ids = {k.lower(): k for k in jp}

    sets = get(f'{TCGDEX}/sets')
    with ThreadPoolExecutor(12) as ex:
        details = [d for d in ex.map(lambda s: get(f"{TCGDEX}/sets/{urllib.parse.quote(s['id'])}"), sets) if d]

    rows = [(d['id'], c['localId'], c['name']) for d in details for c in d.get('cards', []) if c.get('name')]
    votes = collections.defaultdict(collections.Counter)
    for sid, num, name in rows:
        k = jp_ids.get(sid.lower())
        e = k and jp[k]['c'].get(num)
        if e:
            votes[name][e] += 1
    names = {n: v.most_common(1)[0][0] for n, v in votes.items()}
    n_dict = len(names)

    species = {}
    csv_text = get(SPECIES, raw=True).decode('utf-8')
    by_id = collections.defaultdict(dict)
    for r in csv.DictReader(io.StringIO(csv_text)):
        by_id[int(r['pokemon_species_id'])][r['local_language_id']] = r['name']
    for langs in by_id.values():
        for lid in ('4', '12'):   # Traditional, Simplified Chinese
            if lid in langs and '9' in langs:
                species[langs[lid]] = langs['9']

    n_species = n_energy = 0
    for _, _, name in rows:
        if name in names:
            continue
        m = re.match(r'^基本[【\[]?(.)[】\]]?能量$', name)
        if m and m.group(1) in ENERGY:
            names[name] = f'Basic {ENERGY[m.group(1)]} Energy'
            n_energy += 1
            continue
        t = re.match(r'^<火箭隊的>(.+)$', name)   # "<Team Rocket's> Nidoran"
        e = derive(t.group(1), species) if t else derive(name, species)
        if e:
            names[name] = ("Team Rocket's " if t else '') + e
            n_species += 1

    # English set names: only for Chinese sets that share a code with a Japanese set
    by_set = collections.defaultdict(list)
    for sid, num, name in rows:
        by_set[sid].append(name)
    set_out = {sid: jp[jp_ids[sid.lower()]]['n'] for sid in by_set if sid.lower() in jp_ids}

    named = sum(1 for _, _, n in rows if n in names)
    with open('zh-en.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'v': 1, 'built': date.today().isoformat(), 'names': dict(sorted(names.items())), 'sets': set_out},
                  f, ensure_ascii=False, separators=(',', ':'))
    print(f"zh-en.json: {len(names)} names ({n_dict} from Japanese twins, {n_species} from the Pokedex list, {n_energy} energy); "
          f"{named} of {len(rows)} Chinese cards named; English names for {len(set_out)} of {len(by_set)} sets")
    left = collections.Counter(n for _, _, n in rows if n not in names)
    print('not named (most common):', ', '.join(f'{n} x{c}' for n, c in left.most_common(15)))


if __name__ == '__main__':
    sys.exit(main())
