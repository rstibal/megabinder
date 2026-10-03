# Pokémon Card Binder

A single-file browser app for tracking your physical Pokémon TCG collection. Searches real card data and art via the [PokéTCG.io](https://pokemontcg.io) API, stores your collection locally in the browser.

![Pokémon Binder Screenshot](screenshot.png)

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
git clone https://github.com/YOUR_USERNAME/pokemon-binder.git

# Open directly in Chrome — no build step needed
open index.html          # macOS
start index.html         # Windows
xdg-open index.html      # Linux
```

The app needs an internet connection to call the PokéTCG.io API for card search and set data. Everything else runs offline.

### GitHub Pages

Push to a `gh-pages` branch or enable Pages on `main` in your repo settings. The app works as a hosted static page — card search, images, and localStorage all function normally from a served URL.

---

## API

Card data and images come from the free [PokéTCG.io v2 API](https://docs.pokemontcg.io). No API key is required for the free tier (1,000 requests/day). If you exceed that, [register for a free key](https://dev.pokemontcg.io) and add it to requests:

```js
// In index.html, find the fetch calls and add the header:
headers: { 'X-Api-Key': 'your-key-here' }
```

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
