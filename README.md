# Pokémon Card Binder

A single-file browser app for tracking your physical Pokémon TCG collection. Searches real card data and art via the [PokéTCG.io](https://pokemontcg.io) API, stores your collection locally in the browser.

---

## Features

- **Real card art** — searches pokemontcg.io as you type, results display actual card thumbnails
- **Multiple binders** — create, rename, and switch between separate binders (e.g. one per set, one per type)
- **Configurable grid** — choose from 2×2 up to 6×6 pocket layouts, adjustable per binder
- **Add by Set** — load an entire set at once, select the cards you own, and add them in bulk
- **Parallel tracking** — track Normal, Reverse Holo, Holo, Full Art, Rainbow, and Gold finishes per slot, each with a distinct visual effect
- **Persistent storage** — everything saves to `localStorage`; no account or server required
- **Set autocomplete** — full set list fetched once and cached; type to filter
- **Page navigation** — ◀ ▶ buttons or ← → arrow keys to flip through binder pages

---

## Usage

### Local file (recommended for full functionality)

```bash
# Clone the repo
git clone https://github.com/rstibal/pokemon-binder.git

# Open directly in Chrome — no build step needed
open index.html          # macOS
start index.html         # Windows
xdg-open index.html      # Linux
```

The app needs an internet connection to call the PokéTCG.io API for card search and set data. Everything else runs offline.

### GitHub Pages

Live at https://rstibal.github.io/pokemon-binder/ (served from `main`). The app works as a hosted static page — card search, images, and localStorage all function normally from a served URL.

---

## API

Card data and images currently come from the [PokéTCG.io v2 API](https://docs.pokemontcg.io), with no API key. **That API is deprecated**: new key registration is closed, existing keys stop working on 2027-03-01, and the service is already unreliable (intermittent HTTP 500s). The app retries 5xx/429 responses with backoff, but that only helps so much.

**Planned migration: [TCGdex](https://tcgdex.dev)** — free, open source, no key, CORS enabled (`Access-Control-Allow-Origin: *`), so it works from a static page. Evaluated 2026-10-03:

| | PokéTCG.io (current) | TCGdex |
|---|---|---|
| Key required | No (reduced limits) | No |
| Status | Deprecated, ends 2027-03-01 | Active |
| Set list | `/v2/sets` | `/v2/en/sets` (220 sets, ~0.4–2s) |
| Cards in a set | `/cards?q=set.id:X` (paged, 5–8s) | `/v2/en/sets/{id}` (one call, ~0.4s) |
| Search | `/cards?q=name:"X"` | `/v2/en/cards?name=X` (~0.5s) |
| Images | `images.small` / `images.large` | `{image}/low.webp` / `{image}/high.webp` |
| Rarity / set name | in search results | only on `/cards/{id}`; list endpoints return id, name, number, image |
| Extras | — | Per-card variants (normal/reverse/holo), TCGplayer + Cardmarket prices |

Migration is small: the app only reads `images`, `number`, `rarity`, `set` and `id`, so an adapter in the three API functions can map TCGdex responses to the existing card shape. Search results lack rarity, so it would be fetched when a card is selected. Set IDs differ (`sv1` vs `sv01`), so existing saved binders keep working (cards store their own image URLs) but "Add by Set" uses the new IDs.

### What gets cached in localStorage

| Key | Contents | TTL |
|-----|----------|-----|
| `pkBinder4` | All binder and card data | Permanent |
| `pkSets4` | Full set list for autocomplete | 7 days |
| `pkBulkCache4` | Per-set card listings (bulk add) | 24 hours |

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
