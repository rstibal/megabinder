# MegaBinder

A single-file browser app for tracking your physical Pokémon TCG collection. Searches real card data and art via the [TCGdex](https://tcgdex.dev) API, stores your collection locally in the browser.

---

## Features

- **Real card art** — searches pokemontcg.io as you type, results display actual card thumbnails
- **Multiple binders** — create, rename, and switch between separate binders (e.g. one per set, one per type)
- **Configurable grid** — choose from 2×2 up to 6×6 pocket layouts, adjustable per binder
- **Add by Set** — load an entire set and add cards in bulk. Filter by **rarity** (Common, Uncommon, Rare, Double Rare, Illustration Rare, Ultra Rare, Special Illustration Rare, Hyper Rare, plus Other for older sets) and by **card number** (e.g. `1-198, 215`); only matching cards are shown and selected, and you can still click individual cards to deselect them. A separate **Rev. Holo** chip row (Common / Uncommon / Rare, off by default) adds reverse holos as their own slots right after the normal copy. Bulk-added cards get their finish automatically: Ultra Rare and Illustration / Special Illustration Rare → Full Art, Hyper Rare → Gold (Secret Rare → Rainbow in older sets), otherwise Normal or Holo from TCGdex's per-card variant data, and Rev. Holo for reverse copies
- **Search by card** — each printing is its own result (a Common shows a normal and a Rev. Holo tile), and the finish is set automatically; there's no finish picker. TCG Pocket sets are excluded
- **Binder planner** — every card in an Add by Set batch goes into the binder; click a card to grey it out as *still to get* (or hit **All Needed** to start a set from scratch). Greyed slots show a NEED badge and don't count as owned; open one and choose **Mark as Owned** when you get it. The header shows owned vs. to-get counts
- **Parallel tracking** — track Normal, Reverse Holo, Holo, Full Art, Rainbow, and Gold finishes per slot, each with a distinct visual effect
- **Cloud sync** — optional. The ☁ button connects to a private GitHub gist in your own account (classic token with only the `gist` scope, stored in that browser only) so binders stay in sync across devices. Changes push a few seconds after you make them and pull when you return to the tab; if both sides changed you choose which to keep, and every save stays in the gist's revision history
- **Persistent storage** — everything saves to `localStorage`; no account or server required
- **Set autocomplete** — full set list fetched once and cached; type to filter
- **Page navigation** — ◀ ▶ buttons or ← → arrow keys to flip through binder pages

---

## Usage

### Local file (recommended for full functionality)

```bash
# Clone the repo
git clone https://github.com/rstibal/megabinder.git

# Open directly in Chrome — no build step needed
open index.html          # macOS
start index.html         # Windows
xdg-open index.html      # Linux
```

The app needs an internet connection to call the PokéTCG.io API for card search and set data. Everything else runs offline.

### GitHub Pages

Live at https://rstibal.github.io/megabinder/ (served from `main`). The app works as a hosted static page — card search, images, and localStorage all function normally from a served URL.

---

## API

Card data and images come from [TCGdex](https://tcgdex.dev) — free, open source, no API key, CORS-enabled. (The app previously used PokéTCG.io, which is deprecated and shutting down on 2027-03-01.)

Endpoints used (English): `/sets`, `/sets/{id}`, `/cards?name=…`, `/cards?set.id=eq:{id}&rarity=eq:{rarity}`, `/cards/{id}`. Card images are `{image}/low.webp` and `{image}/high.webp`. Transient 5xx/429 responses are retried with backoff.

Search results don't include rarity, so it's fetched when you pick a card. For bulk add, each of the 8 rarities and the normal/reverse/holo variant flags are fetched in parallel per set (the set endpoint lists neither).

### What gets cached in localStorage

| Key | Contents | TTL |
|-----|----------|-----|
| `pkBinder4` | All binder and card data | Permanent |
| `pkSets5` | Full set list for autocomplete | 7 days |
| `pkBulkCache6` | Per-set card listings (bulk add) | 24 hours |

---

## Tech

Vanilla HTML, CSS, and JavaScript — no frameworks, no build step, no dependencies. Single file.

---

## Development

Open `index.html` in a browser. All logic is in the `<script>` block at the bottom of the file; all styles are in the `<style>` block in `<head>`.

[Claude Code](https://claude.ai/code) works well for iterating on this — point it at the repo and describe what you want to change.

---

## License

MIT
