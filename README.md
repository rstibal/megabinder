# MegaBinder

**▶ Open the app: [rstibal.github.io/megabinder](https://rstibal.github.io/megabinder/)**

A digital binder for your physical Pokémon TCG collection. Lay your cards out page by page the way they sit in your real binder, mark what you still need, see what it's worth, and keep it in sync across your devices. No account, no server, no install required. It runs in the browser and can be added to your home screen as an app.

Card data, art and prices come from [TCGdex](https://tcgdex.dev).

---

## Features

### Building binders
- **Multiple binders**, each with its own pocket grid (2×2 up to 6×6).
- **Add by set.** Load a whole set and filter by rarity (Common through Hyper Rare) and card number (e.g. `1-198, 215`). Optionally add reverse holos as their own slots next to the normal copy.
- **Search by card.** Every printing is its own result, so a Common shows both its normal and reverse holo.
- **Automatic finish.** Normal, Holo, Full Art, Gold, Rainbow or Rev. Holo is worked out from the rarity and TCGdex's variant data. There's nothing to pick by hand.
- **Rearrange** cards between slots (unlock the layout first), add pages, and remove empty extra pages.

### Planning and shopping
- **Need vs. owned.** Grey out cards you still have to get (or mark a whole set as needed and tick cards off as they arrive). The header shows owned and to-get counts.
- **Prices.** The card popup shows the TCGplayer market and low price for that exact printing, with a Buy link. Cardmarket's trend price (converted to USD, marked ≈) fills in when TCGplayer has none.
- **Binder value.** Totals for collected, still-to-get and the whole binder, plus the five most valuable cards.
- **Shopping list.** Every needed card with its price and Buy link, sortable, with duplicates merged. Copy it as plain text.
- **Find and filter.** Search by name, number, set, rarity or finish (press `/`), and show All, Owned or Need.

### Languages
- **English, Japanese and Traditional Chinese** cards. Japanese and Chinese cards show their English name and set name next to the original.
- Gaps in TCGdex's Japanese data are filled from a bundled TCGplayer catalogue snapshot, and some newer Japanese sets borrow the matching English card's art (marked with a ribbon) until real scans appear.

### Everyday use
- **Turn pages** with the arrows, the ← → keys, or by swiping on a phone. A short slide shows each turn.
- **Fit to screen** sizes the cards so a whole page fits the window. Handy on foldables and tablets.
- **Quick menu.** Right-click a card (or press and hold on a phone) to mark it owned or needed, open its details, or remove it, with Undo.
- **Share** a read-only copy of a binder as a link.
- **Install as an app.** Chrome and Edge show an Install button; on iPhone or iPad use Share → Add to Home Screen. Once installed it opens full-screen and loads offline, with your binders and any card art you've already viewed. Searching, prices and sync need a connection.

### Cloud sync (optional)
The ☁ button keeps your binders in sync through a **private GitHub gist in your own account**. You need a GitHub classic token with only the `gist` scope, which is stored in that browser only. Changes upload a few seconds after you make them and download when you come back to the tab. If both sides changed, you choose which to keep, and every save stays in the gist's revision history.

Without sync, everything is stored in your browser's `localStorage` on that device.

---

## Running it yourself

It's a single `index.html` with no build step and no dependencies. Serve the folder with any static server:

```bash
git clone https://github.com/rstibal/megabinder.git
cd megabinder
python -m http.server 8765
```

Then open http://localhost:8765/index.html. (Opening the file directly works for most things, but the service worker and the bundled language data need a server.)

The live site is published by GitHub Pages from `main`.

### Files

| File | Purpose |
|------|---------|
| `index.html` | The whole app: markup, styles and script |
| `sw.js` | Service worker (network-first, so updates arrive on a normal reload) |
| `manifest.webmanifest`, `icon-*.png`, `apple-touch-icon.png` | Installable app metadata and icons |
| `jp-gap.json`, `jp-en.json`, `zh-en.json` | Japanese gap data and English names for Japanese and Chinese cards |
| `tools/build_jp_gap.py` | Rebuilds `jp-gap.json` and `jp-en.json` from [TCGCSV](https://tcgcsv.com) |
| `tools/build_zh_en.py` | Rebuilds `zh-en.json` (run after `build_jp_gap.py`) |
| `tools/build_icons.py` | Draws the Poké Ball app icons |

### Stored in the browser

| Key | Contents |
|-----|----------|
| `pkBinder4` | All binders and cards |
| `pkSync1` | Cloud sync settings for this browser |
| `pkFit1`, `pkFx1` | Per-device display preferences |
| `pkSets6`, `pkSetsL1`, `pkBulkCache6` | Cached set lists and set contents |

---

## Credits

- Card data, images and prices: [TCGdex](https://tcgdex.dev) (free, open source, no API key)
- Japanese catalogue data: [TCGCSV](https://tcgcsv.com), a mirror of TCGplayer's catalogue
- A few promo images: [pokemontcg.io](https://pokemontcg.io)

Pokémon and all related names and card images are trademarks of Nintendo, Creatures Inc. and GAME FREAK inc. MegaBinder is an unofficial fan project and is not affiliated with or endorsed by them.

## License

MIT
