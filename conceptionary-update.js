/* Conceptionary "Update" button (c) 2026 Alan William Preston
   A web site cannot push files to a phone, so the phone pulls them: this fetches the template list, the launcher pages and every template again,
   ignoring the copies saved on the device, stores them for offline use, and reloads the page. Used by templates.html and view.html.
   window.conceptionaryUpdate({ onStatus: function (text) {...}, done: function (ok) {...} }) */
(function () {
  var running = false;
  function now() { try { return new Date().toLocaleString([], { day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit' }); } catch (e) { return new Date().toString(); } }
  window.conceptionaryLastUpdate = function () { try { return localStorage.getItem('conceptionary-last-update') || ''; } catch (e) { return ''; } };
  window.conceptionaryUpdate = function (o) {
    o = o || {}; var say = o.onStatus || function () {};
    if (running) return; running = true;
    function finish(ok, text, reload) { running = false; say(text); if (o.done) o.done(ok); if (reload) setTimeout(function () { location.reload(); }, 1600); }
    if (!/^https?:$/.test(location.protocol)) { finish(false, 'Update works on the live web address, not on a local file.'); return; }
    if (navigator.onLine === false) { finish(false, 'No connection: using the copy saved on this device.'); return; }
    say('Checking for the latest template list…');
    fetch('conceptionary-templates.js?v=' + Date.now(), { cache: 'reload' }).then(function (r) { if (!r.ok) throw new Error('list ' + r.status); return r.text(); }).then(function (src) {
      var fake = {}; try { (new Function('window', src))(fake); } catch (e) { throw new Error('list unreadable'); }
      var N = fake.CONCEPTIONARY_NAV; if (!N) throw new Error('list out of date');
      var tfiles = [], seen = {};
      N.flat.forEach(function (t) { ['rom', 'log'].forEach(function (k) { if (t[k]) { var u = N.folder(t[k]) + t[k] + '.html'; if (!seen[u]) { seen[u] = 1; tfiles.push(u); } } }); });
      var core = ['./', 'templates.html', 'view.html', 'index.html', 'conceptionary-templates.js', 'conceptionary-update.js', 'manifest.webmanifest', 'icons/icon-192.png', 'icons/icon-512.png', 'registry/conceptionary-registry.json'];
      var all = core.concat(tfiles), total = all.length, i = 0, okCount = 0, tOk = 0, listDate = fake.CONCEPTIONARY_LIST_DATE || '';
      var tset = {}; tfiles.forEach(function (u) { tset[u] = 1; });
      var cachesP = window.caches ? caches.keys().then(function (ks) { ks = ks.filter(function (k) { return k.indexOf('conceptionary-') === 0; }).sort(); return ks.length ? caches.open(ks[ks.length - 1]) : null; }) : Promise.resolve(null);
      return cachesP.then(function (cache) {
        function worker() {
          if (i >= all.length) return Promise.resolve();
          var u = all[i++];
          return fetch(u + (u.indexOf('?') < 0 && u !== './' ? '?v=' + Date.now() : ''), { cache: 'reload' }).then(function (r) {
            if (r.ok) { okCount++; if (tset[u]) tOk++; if (cache) return cache.put(new URL(u, location.href).href, r.clone()).catch(function () {}); }
          }).catch(function () {}).then(function () { say('Updating ' + Math.min(i, total) + ' of ' + total + '…'); return worker(); });
        }
        var ws = []; for (var w = 0; w < 6; w++) ws.push(worker());
        return Promise.all(ws).then(function () {
          if (navigator.serviceWorker && navigator.serviceWorker.getRegistration) { navigator.serviceWorker.getRegistration().then(function (g) { if (g && g.update) g.update(); }).catch(function () {}); }
          try { localStorage.setItem('conceptionary-last-update', now()); } catch (e) {}
          var msg = 'Updated: ' + tOk + ' templates' + (listDate ? ' (list dated ' + listDate + ')' : '') + ' saved on this device.';
          if (tOk < tfiles.length) msg += ' (' + (tfiles.length - tOk) + ' in the list were not found on the site.)';
          finish(true, msg, true);
        });
      });
    }).catch(function (e) { finish(false, 'Could not update (' + (e && e.message || 'network') + '). The saved copy is still in use.'); });
  };
})();