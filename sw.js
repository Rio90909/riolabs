// Direct Chat service worker — app-shell cache (Stage 17 fix, cache v2).
// v1 was cache-first for the shell, which trapped phones on the first
// downloaded copy forever (updates never arrived). v2 is NETWORK-FIRST
// for the shell: a fresh copy wins whenever the network answers, and the
// cache is only the offline fallback. API traffic is NEVER intercepted:
// non-GET requests and every cross-origin request (Firebase, Supabase,
// Google, YouTube, CDNs) pass straight through to the network.
const DC_CACHE = 'dc-v2';
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

  const isPage = url.pathname.endsWith('/') || url.pathname.endsWith('index.html');
  const isManifest = url.pathname.endsWith('manifest.webmanifest');

  if (isPage || isManifest) {
    // Network-first: fresh copy wins and becomes the new offline fallback.
    event.respondWith(
      fetch(req).then(res => {
        if (res && res.ok) {
          const copy = res.clone();
          const key = isManifest ? './manifest.webmanifest' : './index.html';
          caches.open(DC_CACHE).then(cache => cache.put(key, copy)).catch(() => {});
        }
        return res;
      }).catch(() => caches.match(isManifest ? './manifest.webmanifest' : './index.html'))
    );
    return;
  }

  // Other same-origin files (icons): cache-first is fine, they don't change.
  event.respondWith(
    caches.match(req, { ignoreSearch: true }).then(hit => hit || fetch(req))
  );
});
