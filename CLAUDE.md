# MegaBinder

A single-file web app (`index.html`, vanilla HTML/CSS/JS, no build step) for tracking a physical Pokémon TCG collection as digital binders.

- Repo: `rstibal/megabinder`. Live site: https://rstibal.github.io/megabinder/ (GitHub Pages, deploys on push to `main`; the browser may cache the old page, so test with a `?v=N` query).
- Card data and images: TCGdex REST API (`https://api.tcgdex.net/v2/en`). TCG Pocket sets are excluded. List results lack rarity and variants, which come from rarity-filtered queries or `/cards/{id}`.
- Storage: browser `localStorage` (`SK` for binders). Optional cloud sync copies the whole state to a private GitHub gist using a classic token with only the `gist` scope.

## Rules for working here

- Keep it one file with no dependencies unless asked.
- Bump `APP_VERSION` in `index.html` (format `YYYY.MM.DD.N`) with every change you push. It shows in the ☁ dialog so the user can tell whether a device is running a stale cached page.
- **Do not rename `GIST_FILE` / `GIST_DESC`** (`pokemon-binder...`): sync finds the existing gist by those names, so changing them would orphan users' cloud data. Do not rename `localStorage` keys without a migration.
- The app is an installable PWA: `manifest.webmanifest`, `sw.js` and the `icon-*.png` files sit beside `index.html`. Keep the service worker network-first for the app (a cache-first worker would bring back the stale-page problem) and add any new top-level asset to its `SHELL` list. If you test with a local server, unregister the service worker and clear the caches afterwards.
- Card art: when TCGdex omits `image` for a set, check whether the picture exists under the base set's folder before reaching for another host (see `IMG_TCGDEX`; Trainer/Galarian Gallery sets such as `swsh12tg` live in `swsh12/`). `IMG_FALLBACK` (pokemontcg.io) is only for the few promo sets TCGdex has nowhere.
- Never ask for, enter or print a user's GitHub token.
- Languages: English, Japanese (`ja`) and Traditional Chinese (`zh-tw`) come from TCGdex's per-language endpoints. Non-English cards carry `lang` (omitted for English) and are looked up by name or by set code + number (set codes repeat across languages, so price/detail cache keys are `lang/id`). The pokemontcg.io and base-set art fallbacks are English-only. Korean and Simplified Chinese have almost no TCGdex data, so they are not offered.
- Finish (Normal / Holo / Full Art / Gold / Rainbow / Rev. Holo) is automatic from rarity and TCGdex variants. There is no manual finish picker, so don't add one.
- Keep visual effects subtle and non-animated; the user finds motion distracting (reverse holos are a static stripe pattern plus a light frame).
- Drag-and-drop for slots is deferred. Don't build it unless asked.
- The file uses CRLF line endings on Windows; preserve them when scripting edits.

## Checking changes

Serve locally (`python -m http.server 8765`) and open `http://localhost:8765/index.html`. Seed a binder in the console by setting `st` and calling `renderAll()`. Check desktop (sidebar layout, 900px and up) and phone width (compact top header). Commit and push to `main` to publish.
