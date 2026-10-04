/* MegaBinder service worker.
   - The app itself (index.html and friends) is network-first, so a normal reload always gets the newest version;
     the cached copy is only used when you're offline.
   - Card art from assets.tcgdex.net is cached as you browse, so your binders still show their pictures offline.
   - Everything else (TCGdex API, GitHub sync, prices) is never touched: it goes straight to the network. */
const CACHE_APP = 'megabinder-app-v1';
const CACHE_IMG = 'megabinder-img-v1';
const IMG_HOST = 'assets.tcgdex.net';
const IMG_LIMIT = 1500;   // keep the picture cache bounded
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_APP).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (![CACHE_APP, CACHE_IMG].includes(k)) await caches.delete(k);
    await self.clients.claim();
  })());
});

async function trim(cache) {
  const keys = await cache.keys();
  for (let i = 0; i < keys.length - IMG_LIMIT; i++) await cache.delete(keys[i]);   // oldest first
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  if (url.hostname === IMG_HOST) {   // card art: cache first
    e.respondWith((async () => {
      const cache = await caches.open(CACHE_IMG);
      const hit = await cache.match(req.url);
      if (hit) return hit;
      try {
        const res = await fetch(req.url, { mode: 'cors' });
        if (res.ok) { cache.put(req.url, res.clone()); trim(cache); }
        return res;
      } catch {
        return fetch(req);   // let the browser report the failure normally
      }
    })());
    return;
  }

  if (url.origin === self.location.origin) {   // the app: network first, cache when offline
    e.respondWith((async () => {
      const cache = await caches.open(CACHE_APP);
      try {
        const res = await fetch(new Request(req.url, { cache: 'no-cache' }));   // always revalidate, so updates show up on reload
        if (res.ok) cache.put(url.origin + url.pathname, res.clone());   // keyed without ?query so entries don't pile up
        return res;
      } catch {
        return (await cache.match(url.origin + url.pathname)) || (req.mode === 'navigate' ? await cache.match('index.html') : Response.error());
      }
    })());
  }
});
