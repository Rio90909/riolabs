// Direct Chat service worker — app-shell cache only (Stage 15).
// API traffic is NEVER intercepted: non-GET requests and every cross-origin
// request (Firebase, Supabase, Google, YouTube, CDNs) pass straight through
// to the network, so realtime chat can never be served stale from cache.
const DC_CACHE = 'dc-v1';
const DC_SHELL = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png'];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(DC_CACHE)
      // Each asset is added independently: a missing icon (404) must not
      // fail the whole install.
      .then(cache => Promise.all(DC_SHELL.map(url => cache.add(url).catch(() => {}))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== DC_CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return; // writes always hit the network
  let url;
  try { url = new URL(req.url); } catch (e) { return; }
  if (url.origin !== self.location.origin) return; // APIs/CDNs: network only

  // Same-origin GETs (the app shell): cache-first, network as the fallback,
  // and a fresh copy of the shell is stored whenever the network answers.
  event.respondWith(
    caches.match(req, { ignoreSearch: true }).then(hit => {
      if (hit) return hit;
      return fetch(req).then(res => {
        if (res && res.ok && (url.pathname.endsWith('/') || url.pathname.endsWith('index.html'))) {
          const copy = res.clone();
          caches.open(DC_CACHE).then(cache => cache.put('./index.html', copy)).catch(() => {});
        }
        return res;
      }).catch(() => caches.match('./index.html'));
    })
  );
});
