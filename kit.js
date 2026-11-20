/* ==== CONCEPTIONARY PHONE KIT (c) 2026 Alan William Preston ==== */
(function () {
  if (window.__kit) return; window.__kit = true;
  var de = document.documentElement, CFG = window.__KIT || {};
  function lab(k, d) { var v = window.LANG && LANG[k]; return (v && !/^[A-Z_]+$/.test(v)) ? v : d; }

  /* 1. TOUCH: let the phone's pinch zoom work (touch-action decides what a finger may do) --------------------------------------- */
  var lastT = 0;
  function endDrags() { ['touchend', 'mouseup'].forEach(function (t) { try { document.dispatchEvent(new Event(t, { bubbles: true })); } catch (e) {} }); }
  document.addEventListener('touchstart', function (e) { lastT = Date.now(); e.preventDefault = function () {}; if (e.touches && e.touches.length > 1) endDrags(); }, { capture: true, passive: true });
  document.addEventListener('touchmove', function (e) { lastT = Date.now(); if (e.touches && e.touches.length > 1) e.preventDefault = function () {}; }, { capture: true, passive: true });
  document.addEventListener('touchend', function () { lastT = Date.now(); }, { capture: true, passive: true });
  document.addEventListener('touchcancel', function () { lastT = Date.now(); endDrags(); }, { capture: true, passive: true });
  ['mousedown', 'mousemove', 'mouseup'].forEach(function (t) { document.addEventListener(t, function (e) { if (e.isTrusted && Date.now() - lastT < 700) e.stopImmediatePropagation(); }, true); });   /* the mouse events a phone makes after a touch */

  /* 2. A BIGGER CIRCLE ON A PORTRAIT PHONE: the view box is fitted to the circle, and the words are slid inside the screen ------- */
  var svg = document.getElementById(CFG.svgId || 'svgCanvas'), phone = window.matchMedia('(max-width: 700px) and (orientation: portrait)'), busy = false, last = '';
  function faceR() {
    if (CFG.faceR) return CFG.faceR;
    var r = 0; svg.querySelectorAll('circle').forEach(function (c) {
      if (c.closest('foreignObject') || c.id === 'draggableFrame' || c.id === 'dragDot') return;
      var cx = +c.getAttribute('cx') || 0, cy = +c.getAttribute('cy') || 0, rr = +c.getAttribute('r') || 0;
      if (Math.abs(cx - 50) < 3 && Math.abs(cy - 50) < 3) r = Math.max(r, rr);
    });
    return r || 36;
  }
  function tbe() { try { return textBoxElements; } catch (e) { return []; } }
  function boxes() { return tbe().filter(function (fo) { return fo && fo.style.display !== 'none' && fo.getAttribute('width'); }); }
  function fit() {
    if (!svg || busy || !phone.matches || CFG.nofit) return;
    var cw = svg.clientWidth, ch = svg.clientHeight; if (!cw || !ch) return;
    busy = true;
    try {
      var R = faceR(), pad = 0.8, wrapped = boxes().some(function (fo) { return fo.dataset.wrap === '1'; }), shares = CFG.share ? [CFG.share] : ((wrapped || CFG.adapt) ? [0.84, 0.78, 0.72, 0.66, 0.60, 0.55] : [0.84]), g = null;
      /* everything drawn on the dial that is not a word (labels, moon icons, ticks) must stay on screen: measure how far it reaches from the centre */
      var halfW = R;
      try {
        var m = svg.getScreenCTM(); if (m) { var inv = m.inverse();
          Array.prototype.forEach.call(svg.children, function (el) {
            if (/^(foreignObject|defs|style|title|desc)$/i.test(el.tagName)) return;
            if (el.querySelector && el.querySelector('foreignObject')) return;     /* the words are placed separately */
            var r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
            var p1 = new DOMPoint(r.left, r.top).matrixTransform(inv), p2 = new DOMPoint(r.right, r.bottom).matrixTransform(inv);
            if (p2.x - p1.x > 130) return;                  /* a background shape, not a mark on the dial */
            halfW = Math.max(halfW, Math.abs(p1.x - 50), Math.abs(p2.x - 50));
          });
        }
      } catch (err) {}
      function build(share) {
        var vw = Math.max(2 * R / share, 2 * halfW + 3), vh = vw * ch / cw, vx = 50 - vw / 2, vy = 50 - vh / 2;
        var bs = boxes().map(function (fo) { return { fo: fo, x: +fo.getAttribute('x'), y: +fo.getAttribute('y'), w: +fo.getAttribute('width'), h: +fo.getAttribute('height') }; });
        bs.forEach(function (b) { b.x = Math.min(Math.max(b.x, vx + pad), vx + vw - pad - b.w); b.y = Math.min(Math.max(b.y, vy + pad), vy + vh - pad - b.h); });
        var hit = 0; bs.forEach(function (b) { var nx = Math.min(Math.max(50, b.x), b.x + b.w), ny = Math.min(Math.max(50, b.y), b.y + b.h); var depth = R - Math.hypot(nx - 50, ny - 50); if (depth > (CFG.slack || 9)) hit++; window.__kitDepth = Math.max(window.__kitDepth || 0, 0); });
        return { vx: vx, vy: vy, vw: vw, vh: vh, bs: bs, hit: hit };
      }
      for (var si = 0; si < shares.length; si++) { g = build(shares[si]); if (!g.hit) break; }   /* a smaller circle only when the words would sit on it */
      var vx = g.vx, vy = g.vy, vw = g.vw, vh = g.vh, bs = g.bs;
      var vb = vx + ' ' + vy + ' ' + vw + ' ' + vh; svg.setAttribute('viewBox', vb); last = vb;
      for (var it = 0; it < 120; it++) {
        var moved = false;
        for (var i = 0; i < bs.length; i++) for (var j = i + 1; j < bs.length; j++) {
          var a = bs[i], b = bs[j], ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x) + 0.6, oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y) + 0.6;
          if (ox > 0 && oy > 0) {
            var d = ((a.y + a.h / 2) <= (b.y + b.h / 2)) ? -1 : 1, s = oy / 2;
            a.y += d * s; b.y -= d * s; moved = true;
            [a, b].forEach(function (q) { q.y = Math.min(Math.max(q.y, vy + pad), vy + vh - pad - q.h); });
          }
        }
        if (!moved) break;
      }
      bs.forEach(function (b) { b.fo.setAttribute('x', b.x); b.fo.setAttribute('y', b.y); });
    } finally { busy = false; }
  }
  if (svg) {
    var pend = 0; function soon() { cancelAnimationFrame(pend); pend = requestAnimationFrame(fit); }
    new MutationObserver(function () { if (!busy) soon(); }).observe(svg, { attributes: true, attributeFilter: ['viewBox'], subtree: false });
    new MutationObserver(function () { if (!busy) soon(); }).observe(svg, { attributes: true, attributeFilter: ['x', 'y', 'width', 'height', 'style'], subtree: true });
    window.addEventListener('resize', soon); window.addEventListener('orientationchange', soon);
    if (phone.addEventListener) phone.addEventListener('change', function () { if (!phone.matches && window.cmpPlaceAll) window.cmpPlaceAll(); soon(); });
    window.addEventListener('load', function () { setTimeout(soon, 50); setTimeout(soon, 400); });
    soon();
  }

  /* 3. PROGRESS, FIRST-USE HINT, CELEBRATION --------------------------------------------------------------------------------------- */
  var page = document.querySelector('.a4-page'), prog = document.createElement('div'), partyEl = document.createElement('div'), hintEl = document.createElement('div');
  prog.id = 'kitProgress'; partyEl.id = 'kitParty'; hintEl.id = 'kitHint';
  if (page) page.appendChild(prog); document.body.appendChild(partyEl); document.body.appendChild(hintEl);
  function total() { try { if (window.__kitCount) return window.__kitCount()[1]; return CFG.total ? CFG.total() : tbe().length; } catch (e) { return 0; } }
  function learnedN() { if (window.__kitCount) { try { return window.__kitCount()[0]; } catch (e) { return 0; } } return tbe().filter(function (fo) { return fo && fo.classList.contains('learned'); }).length; }   /* counted on the words of the mode now showing */
  var prev = 0, tot = 0;
  function paint(first) {
    tot = total(); var n = learnedN(); if (!tot) { prog.style.display = 'none'; return; } prog.style.display = '';
    prog.textContent = lab('progress_label', 'Learned') + ' ' + Math.min(n, tot) + '/' + tot; prog.classList.toggle('done', n >= tot);
    if (!first && n >= tot && prev < tot) {
      partyEl.innerHTML = '🎉<br>' + lab('all_done', 'All learned!'); partyEl.classList.remove('on'); void partyEl.offsetWidth; partyEl.classList.add('on');
      setTimeout(function () { partyEl.classList.remove('on'); }, 3600);
    }
    prev = n;
  }
  var lastTot = -1, ptimer = 0;
  function repaint() { clearTimeout(ptimer); ptimer = setTimeout(function () { var t = total(); var silent = (t !== lastTot); lastTot = t; paint(silent); }, 30); }
  if (svg) new MutationObserver(repaint).observe(svg, { attributes: true, attributeFilter: ['class'], childList: true, subtree: true });
  var tdp = document.getElementById('transDisplay'); if (tdp) new MutationObserver(repaint).observe(tdp, { childList: true, characterData: true, subtree: true });   /* two-mode templates (Rice): transition words show here */
  paint(true); window.addEventListener('load', function () { setTimeout(function () { lastTot = total(); paint(true); }, 300); setTimeout(function () { lastTot = total(); paint(true); }, 1200); });
  var seen = false; try { seen = localStorage.getItem('conceptionary-hint-v1') === '1'; } catch (e) {}
  if (!seen) {
    var touch = window.matchMedia('(pointer: coarse)').matches;
    hintEl.textContent = lab('first_hint', touch ? (CFG.hintTouch || 'Drag the sun. Tap a word to see it in the other language. Pinch with two fingers to zoom.' ): (CFG.hint || 'Drag the sun. Click a word to see it in the other language.'));
    setTimeout(function () { hintEl.classList.add('on'); }, 1200);
    var gone = false, hide = function () { if (gone) return; gone = true; hintEl.classList.remove('on'); try { localStorage.setItem('conceptionary-hint-v1', '1'); } catch (e) {} };
    setTimeout(hide, 11000);
    ['pointerdown', 'keydown'].forEach(function (t) { document.addEventListener(t, function () { setTimeout(hide, 1500); }, { once: true, capture: true }); });
  }

  /* 4. ANSWERS: alternatives (LANG.alt_answers = { "Autumn": ["Fall"] }) and "almost" feedback ------------------------------------- */
  function norm(t) { return String(t == null ? '' : t).toLowerCase().replace(/<[^>]*>/g, '').replace(/[\s\-!?.,;:'"’‘“”()]/g, ''); }
  window.__kitAlt = function (input, correct) {
    var alts = (window.LANG && LANG.alt_answers && LANG.alt_answers[String(correct).replace(/<[^>]*>/g, '')]) || [];
    var n = norm(input); return alts.some(function (a) { return norm(a) === n; });
  };
  window.__kitNear = function (input, correct) {
    var a = norm(input), b = norm(correct); if (!a || !b || a === b) return '';
    var n = Math.min(a.length, b.length), i = 0; while (i < n && a[i] === b[i]) i++;
    if (Math.abs(a.length - b.length) <= 1 && (function () { var d = 0, k; if (a.length === b.length) { for (k = 0; k < a.length; k++) if (a[k] !== b[k]) d++; return d <= 1; } var s = a.length < b.length ? a : b, l = a.length < b.length ? b : a; for (k = 0; k < l.length; k++) { if (l.slice(0, k) + l.slice(k + 1) === s) return true; } return false; })())
      return lab('quiz_close', 'Almost! Check letter') + ' ' + (i + 1);
    return '';
  };
  if (typeof AnswerUtils !== 'undefined' && AnswerUtils.checkAnswer) {
    var oc = AnswerUtils.checkAnswer;
    AnswerUtils.checkAnswer = function (input, correct) { var ok = oc.call(AnswerUtils, input, correct) || window.__kitAlt(input, correct); window.__kitLast = { input: input, correct: correct, ok: ok }; return ok; };
  }
  var fb = document.getElementById('quizFeedback');
  if (fb) new MutationObserver(function () {
    var L = window.__kitLast; if (!L || L.ok || fb.dataset.kit === '1' || fb.style.color !== 'red') return;
    var near = window.__kitNear(L.input, L.correct); if (!near) return;
    fb.dataset.kit = '1'; fb.textContent = fb.textContent.replace(/\s*[—-]\s*.*$/, '') + ' — ' + near; setTimeout(function () { fb.dataset.kit = ''; }, 50);
  }).observe(fb, { childList: true, characterData: true, subtree: true });

  /* 5. THE QUIZ BOX: phone flag, drag anywhere (also by the answer box), stay above the on-screen keyboard ------------------------- */
  var QMQ = window.matchMedia('(pointer: coarse) and (max-width: 700px), (pointer: coarse) and (max-height: 520px) and (orientation: landscape)');
  function syncPhone() { de.classList.toggle('kit-phone', QMQ.matches); if (!CFG.keepNoQuiz) de.classList.remove('no-quiz'); }
  syncPhone(); if (QMQ.addEventListener) QMQ.addEventListener('change', syncPhone);
  var qc = document.querySelector('.quiz-container'), vv = window.visualViewport;
  if (qc) {
    /* on a phone the box opens at the TOP of the circle area, where the on-screen keyboard can never cover it */
    function placeTop() {
      if (!de.classList.contains('kit-phone') || qc.classList.contains('kit-moved')) return;
      var t = 4;   /* the very top: it covers the buttons for a moment, never the circle or the word you tapped */
      de.style.setProperty('--kit-qtop', Math.max(4, Math.round(t)) + 'px');
    }
    var wasOpen = false;
    new MutationObserver(function () { var open = qc.style.display === 'block'; if (open === wasOpen) return; wasOpen = open; de.classList.toggle('kit-quiz-open', open); if (open) { placeTop(); keepSoon(); } }).observe(qc, { attributes: true, attributeFilter: ['style'] });
    var st = null, swallow = false;
    qc.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      e.stopImmediatePropagation();                                  /* this drag replaces the older one that skipped the answer box */
      var r = qc.getBoundingClientRect(); st = { id: e.pointerId, dx: e.clientX - r.left, dy: e.clientY - r.top, x0: e.clientX, y0: e.clientY, drag: false, w: r.width };
    }, true);
    document.addEventListener('pointermove', function (e) {
      if (!st || e.pointerId !== st.id) return;
      if (!st.drag) {
        if (Math.hypot(e.clientX - st.x0, e.clientY - st.y0) < 7) return;
        st.drag = true; qc.classList.add('kit-moved'); qc.dataset.moved = '1'; qc.style.translate = '0px 0px';
        var w = de.classList.contains('kit-phone') ? Math.min(st.w, 380, window.innerWidth * 0.94) : st.w; st.dx = Math.min(st.dx, w - 20);
        if (de.classList.contains('kit-phone')) qc.style.setProperty('width', w + 'px', 'important');
        if (document.activeElement && document.activeElement.blur && qc.contains(document.activeElement)) document.activeElement.blur();
      }
      var w2 = qc.offsetWidth, h2 = qc.offsetHeight;
      qc.style.setProperty('left', Math.min(Math.max(e.clientX - st.dx, 0), Math.max(0, window.innerWidth - w2)) + 'px', 'important');
      qc.style.setProperty('top', Math.min(Math.max(e.clientY - st.dy, 0), Math.max(0, window.innerHeight - h2)) + 'px', 'important');
      e.preventDefault();
    }, { passive: false });
    function up(e) { if (!st || e.pointerId !== st.id) return; if (st.drag) { swallow = true; setTimeout(function () { swallow = false; }, 80); keep(); } st = null; }
    document.addEventListener('pointerup', up); document.addEventListener('pointercancel', up);
    qc.addEventListener('click', function (e) { if (swallow) { e.stopPropagation(); e.preventDefault(); swallow = false; } }, true);
    window.addEventListener('resize', function () { if (qc.style.display !== 'block') placeTop(); if (qc.classList.contains('kit-moved')) { qc.style.setProperty('left', Math.min(parseFloat(qc.style.left) || 0, Math.max(0, window.innerWidth - qc.offsetWidth)) + 'px', 'important'); qc.style.setProperty('top', Math.min(parseFloat(qc.style.top) || 0, Math.max(0, window.innerHeight - qc.offsetHeight)) + 'px', 'important'); } keep(); });
    /* keep the box above the on-screen keyboard, whether the browser shrinks the page or only the visible part of it */
    var kt = [];
    function keep() {
      function put(v) { if (qc.style.translate !== v) qc.style.translate = v; }
      if (!vv || qc.style.display !== 'block') { put('0px 0px'); return; }
      put('0px 0px');
      var r = qc.getBoundingClientRect(), bottom = vv.offsetTop + vv.height, dy = Math.max(0, r.bottom - bottom + 12);
      if (dy > 0) { dy = Math.min(dy, Math.max(0, r.top - vv.offsetTop - 4)); put('0px ' + (-dy) + 'px'); }
    }
    function keepSoon() { kt.forEach(clearTimeout); kt = [30, 200, 450, 800].map(function (ms) { return setTimeout(keep, ms); }); }
    if (vv) { vv.addEventListener('resize', keepSoon); vv.addEventListener('scroll', keepSoon); }
    qc.addEventListener('focusin', keepSoon); qc.addEventListener('focusout', function () { setTimeout(keep, 250); });
  }

  /* 6. FULL SCREEN ZOOM: Chrome switches its own pinch zoom off in full screen, so two fingers zoom and pan the circle here --------- */
  (function () {
    if (!svg) return;
    var zs = 1, tx = 0, ty = 0, g = null;
    function fsOn() { return !!(document.fullscreenElement || document.webkitFullscreenElement || window.__kitForceFs); }
    function apply() { svg.style.transformOrigin = '0 0'; svg.style.transform = (zs === 1 && !tx && !ty) ? '' : 'translate(' + tx + 'px,' + ty + 'px) scale(' + zs + ')'; window.__kitZoom = { s: zs, x: tx, y: ty }; }
    function sync() { de.classList.toggle('kit-fs', fsOn()); if (!fsOn()) { zs = 1; tx = ty = 0; apply(); } }
    ['fullscreenchange', 'webkitfullscreenchange'].forEach(function (t) { document.addEventListener(t, sync); });
    window.__kitSyncFs = sync; sync();
    function mid(t) { return { x: (t[0].clientX + t[1].clientX) / 2, y: (t[0].clientY + t[1].clientY) / 2, d: Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY) || 1 }; }
    document.addEventListener('touchstart', function (e) {
      if (!fsOn() || e.touches.length !== 2) return;
      var m = mid(e.touches), r = svg.getBoundingClientRect(); g = { d: m.d, s: zs, tx: tx, ty: ty, bx: r.left - tx, by: r.top - ty, mx: m.x, my: m.y };
    }, { capture: true, passive: true });
    document.addEventListener('touchmove', function (e) {
      if (!g || e.touches.length !== 2) return;
      var m = mid(e.touches), s = Math.min(4, Math.max(1, g.s * m.d / g.d));
      var cx = ((g.mx - g.bx) - g.tx) / g.s, cy = ((g.my - g.by) - g.ty) / g.s;      /* the point of the circle that sat under the fingers */
      var W = svg.clientWidth, H = svg.clientHeight, nx = (m.x - g.bx) - cx * s, ny = (m.y - g.by) - cy * s;
      zs = s; tx = Math.min(0, Math.max(W * (1 - s), nx)); ty = Math.min(0, Math.max(H * (1 - s), ny));
      if (s < 1.03) { zs = 1; tx = ty = 0; }
      apply(); if (e.cancelable) e.preventDefault();
    }, { capture: true, passive: false });
    document.addEventListener('touchend', function (e) { if (!e.touches || e.touches.length < 2) g = null; }, { capture: true, passive: true });
    document.addEventListener('touchcancel', function () { g = null; }, { capture: true, passive: true });
  })();

  /* 7. RESET BUTTON for Days of the Week (the Seasons files already have one): back to the opening view, all learned words cleared -- */
  (function () {
    var ctl = document.getElementById('cmpCtl');
    if (!ctl || document.getElementById('reset-btn') || (typeof daysOfWeekData === 'undefined' && !window.__kitReset)) return;
    var b = document.createElement('button'); b.id = 'reset-btn'; b.type = 'button'; b.className = 'tb kit-icon';
    var t = lab('reset_label', 'Reset'); b.title = t; b.setAttribute('aria-label', t);
    b.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4V1L7.5 5.5 12 10V7a6 6 0 1 1-6 6H4a8 8 0 1 0 8-9z"/></svg>';
    var fs = document.getElementById('fsBtn'); ctl.insertBefore(b, fs && fs.parentNode === ctl ? fs : null);
    b.addEventListener('click', function () {
      try {
        if (window.__cmpReset) window.__cmpReset();
        var q = document.getElementById('quizContainer'); if (q) q.style.display = 'none';
        currentQuizIndex = -1; document.getElementById('quizInput').value = ''; document.getElementById('quizFeedback').textContent = '';
        if (window.__kitReset) { window.__kitReset(); return; }   /* templates with their own reset steps (Compass) */
        learnedItems.fill(false); addedLearnedItems.fill(false);
        var li = document.getElementById('learned-items'); if (li) li.innerHTML = '';
        if (window.createTextBoxes) window.createTextBoxes();
        positionFrameOnDay(getCurrentDayIndex());
      } catch (err) { if (window.console) console.error('Reset failed', err); }
    });
  })();

  /* 8. TOOLS MENU LINKS: the User Manual and the Index of Exercises (change the two addresses here, in this one place) ------------- */
  var USER_MANUAL_URL = 'https://sites.google.com/view/conceptionary/home/user-manual';
  var EXERCISES_URL = 'https://sites.google.com/view/conceptionary/home/index-of-exercises';
  (function () {
    var menu = document.getElementById('toolsMenu'); if (!menu || document.getElementById('manualBtn')) return;
    function add(id, label, title, url) {
      var b = document.createElement('button'); b.id = id; b.type = 'button'; b.textContent = label; b.title = title;
      b.addEventListener('click', function (e) { e.stopPropagation(); menu.classList.remove('active'); window.open(url, '_blank', 'noopener'); });
      menu.appendChild(b);
    }
    add('manualBtn', lab('manual_label', 'User Manual'), lab('manual_title', 'How to use these templates (opens the Conceptionary website)'), USER_MANUAL_URL);
    add('exercisesBtn', lab('exercises_label', 'Exercises & Tests'), lab('exercises_title', 'Practise this vocabulary (opens the Index of Exercises)'), EXERCISES_URL);
  })();
})();