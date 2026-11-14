/* Conceptionary offline helper (service worker). (c) 2026 Alan William Preston
   WHAT IT DOES: the first time the site is opened online, it saves every template listed in conceptionary-templates.js (plus the launcher pages)
   on the device. After that the whole site opens with no connection. When online, each file is quietly refreshed in the background, so a changed
   template appears the NEXT time the page is opened.
   TO FORCE A FULL REFRESH on every device after a big update: change VERSION below (any new text) and push. */
var VERSION = 'v1';
var CACHE = 'conceptionary-' + VERSION;
var CORE = ['./', 'templates.html', 'view.html', 'index.html', 'conceptionary-templates.js', 'manifest.webmanifest', 'icons/icon-192.png', 'icons/icon-512.png', 'registry/conceptionary-registry.json'];

self.window = self;                               /* conceptionary-templates.js writes to window.* */
importScripts('conceptionary-templates.js');

function templateFiles() {
  var N = self.CONCEPTIONARY_NAV, out = [];
  if (!N) return out;
  N.flat.forEach(function (t) { ['rom', 'log'].forEach(function (k) { if (t[k]) out.push(N.folder(t[k]) + t[k] + '.html'); }); });
  return out;
}

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) {
    var all = CORE.concat(templateFiles());
    /* one at a time and forgiving: a template that is not in the repo (yet) is simply skipped */
    return Promise.all(all.map(function (u) { return fetch(u, { cache: 'reload' }).then(function (r) { if (r.ok) return c.put(u, r); }).catch(function () {}); }));
  }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k.indexOf('conceptionary-') === 0 && k !== CACHE; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener('fetch', function (e) {
  var req = e.request, url = new URL(req.url);
  if (url.origin !== location.origin) return;                               /* only our own site */
  if (req.method === 'HEAD') {                                              /* the launcher's "is this file there?" checks work offline too */
    e.respondWith(caches.match(req, { ignoreMethod: true, ignoreSearch: true }).then(function (r) { return r ? new Response(null, { status: 200 }) : fetch(req); }));
    return;
  }
  if (req.method !== 'GET') return;
  e.respondWith(caches.open(CACHE).then(function (c) {
    return c.match(req, { ignoreSearch: true }).then(function (hit) {       /* view.html?t=... is the same page whatever follows the ? */
      var net = fetch(req).then(function (r) {
        if (r && r.ok && r.type === 'basic') { c.put(url.pathname.slice(url.pathname.lastIndexOf('/') + 1) === '' ? req : new Request(url.origin + url.pathname), r.clone()); }
        return r;
      }).catch(function () { return hit; });
      return hit || net;                                                    /* saved copy first (fast, works offline); the network refreshes it behind the scenes */
    });
  }));
});