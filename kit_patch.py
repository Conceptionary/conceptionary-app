import sys,re,datetime,subprocess
css=open('/home/claude/kit/kit.css').read(); js=open('/home/claude/kit/kit.js').read()
stamp='<!-- Last updated: %s -->'%(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=13))).strftime('%Y-%m-%d @ %-I:%M %p').replace('AM','a.m.').replace('PM','p.m.')+' (Mangawhai, NZ)')
def once(s,a,b):
    assert s.count(a)==1,(a[:50],s.count(a)); return s.replace(a,b)

LAY = r"""function lay(i, txt) {   /* WRAP: a phrase wider than WRAPMAX (about a third of the circle) breaks at its spaces onto 2 or 3 lines */
        var s = sizeOf(i); cv.font = '700 ' + s + 'px ' + FONT;
        var t = plain(txt).replace(/\s+/g, ' ').trim(), full = cv.measureText(t).width, words = t.split(' '), longest = 0;
        words.forEach(function (x) { longest = Math.max(longest, cv.measureText(x).width); });
        var cap = Math.max(WRAPMAX, longest);
        if (words.length < 2 || full <= cap) return { w: full + 3, h: s * 1.35, n: 1 };
        function wrap(cp) { var lines = [], cu = ''; words.forEach(function (x) { var tr = cu ? cu + ' ' + x : x; if (cu && cv.measureText(tr).width > cp) { lines.push(cu); cu = x; } else cu = tr; }); lines.push(cu); return lines; }
        var lines = wrap(cap); while (lines.length > 3 && cap < full) { cap += 1; lines = wrap(cap); }
        while (cap > longest && wrap(cap - 1).length === lines.length) cap -= 1;   /* the narrowest box that keeps the same number of lines */
        lines = wrap(cap); var wm = 0; lines.forEach(function (l) { wm = Math.max(wm, cv.measureText(l).width); });
        return { w: wm * 1.05 + 3, h: s * (1.2 * lines.length + 0.15), n: lines.length };
    }
    var WRAPMAX = 22;
    function wOf(i, txt) { return lay(i, txt).w; }
    function hOf(i, txt) { return txt == null ? sizeOf(i) * 1.35 : lay(i, txt).h; }"""

LAYR = LAY.replace("function lay(i, txt)","function lay(i, k, txt)").replace("var s = sizeOf(i);","var s = sizeOf(i, k);").replace("function wOf(i, txt) { return lay(i, txt).w; }","function wOf(i, k, txt) { return lay(i, k, txt).w; }").replace("function hOf(i, txt) { return txt == null ? sizeOf(i) * 1.35 : lay(i, txt).h; }","function hOf(i, k, txt) { return txt == null ? sizeOf(i, k) * 1.35 : lay(i, k, txt).h; }")
def sw(s):
    """Steering Wheel: the svg is #sv; the wheel lays out all its phrases itself (__swFit), so the kit must not re-fit it."""
    if 'window.__KIT = {' not in s: s=once(s,'<script id="kit-script">','<script>window.__KIT = { svgId: "sv", nofit: true, hintTouch: "Turn the wheel with one finger. Tap a phrase to see it in the other language. Pinch with two fingers to zoom.", hint: "Turn the wheel. Click a phrase to see it in the other language." };</script>\n<script id="kit-script">')
    if 'window.__kitCount = function' not in s: s=once(s,"window.__swLayout(); window.__swFit(); renders.forEach(function (r) { r(); }); show(0);","window.__kitCount = function () { return [states.filter(function (x) { return x.learned; }).length, states.length]; };   /* phone kit: Learned n/total */\nwindow.__swLayout(); window.__swFit(); renders.forEach(function (r) { r(); }); show(0);")
    if 'const swDock = ' not in s:
        s=once(s,"const noQuiz = function () { return de.classList.contains('no-quiz'); };","""const noQuiz = function () { return de.classList.contains('no-quiz'); };
/* PHONE QUIZ DOCK (phone kit): on a phone the answer box lives in a box under the wheel (portrait) or under the buttons at the lower left (landscape), above the on-screen keyboard */
const swDock = document.createElement('div'); swDock.id = 'swQuizDock'; document.body.appendChild(swDock);
window.__swDockKeep = function () {
    var vv = window.visualViewport; function keep() {
        if (!swDock.classList.contains('on')) { swDock.style.translate = ''; return; }
        swDock.style.translate = '0px 0px'; var r = swDock.getBoundingClientRect(), bottom = vv ? vv.offsetTop + vv.height : window.innerHeight, dy = Math.max(0, r.bottom - bottom + 10);
        swDock.style.translate = dy ? '0px ' + (-dy) + 'px' : '0px 0px';
    }
    [30, 200, 450, 800].forEach(function (ms) { setTimeout(keep, ms); });
};
if (window.visualViewport) { window.visualViewport.addEventListener('resize', function () { window.__swDockKeep(); }); window.visualViewport.addEventListener('scroll', function () { window.__swDockKeep(); }); }""")
        s=once(s,"fo.classList.toggle('sw-off', !quiz);","""var useDock = quiz && de.classList.contains('kit-phone');
        if (useDock) { if (window.__swOwn && window.__swOwn[0] !== xd) window.__swOwn[1].appendChild(window.__swOwn[0]); window.__swOwn = [xd, fo]; swDock.appendChild(xd); swDock.classList.add('on'); window.__swDockKeep(); }
        else if (xd.parentNode !== fo) { fo.appendChild(xd); if (window.__swOwn && window.__swOwn[0] === xd) { swDock.classList.remove('on'); window.__swOwn = null; window.__swDockKeep(); } }
        fo.classList.toggle('sw-off', !quiz || useDock);""")
        s=once(s,"(quiz ? (LOGV ? 62 : 50) : 28)","(quiz && !useDock ? (LOGV ? 62 : 50) : 28)")
    return s
def cmp_(s):
    """Compass: the click cycle already opens the Quiz unless <html class=no-quiz>; fix the learned word's place and add a Reset."""
    pat=re.compile(r'tb\.setAttribute\("x", x - 30\);\s*tb\.setAttribute\("y", y - 12\);')
    if pat.search(s): s=pat.sub('if (window.cmpPlaceOne) window.cmpPlaceOne(currentQuizIndex); else { tb.setAttribute("x", x - 30); tb.setAttribute("y", y - 12); }   /* kit: keep the measured place */',s,count=1)
    if 'window.__KIT = {' not in s: s=once(s,'<script id="kit-script">','<script>window.__KIT = { adapt: true, slack: 3, hintTouch: "Drag the compass needle. Tap a word to see it in the other language. Pinch with two fingers to zoom.", hint: "Drag the compass needle. Click a word to see it in the other language." };</script>\n<script id="kit-script">')
    # LOG: the TLR answer must go through AnswerUtils (macrons, plain vowels, ou/ei) like the other LOG templates; ROM keeps its plain comparison
    if 'AnswerUtils.checkAnswer(userAnswer, correct) :' not in s and 'collapse_double_vowels' in s:
        s=once(s,"if (userAnswer.toLowerCase() === correct.toLowerCase() ||","if ((typeof AnswerUtils !== 'undefined' ? AnswerUtils.checkAnswer(userAnswer, correct) : userAnswer.toLowerCase() === correct.toLowerCase()) ||")
    if 'collapse_double_vowels: false,' in s and 'optional pairs treated as one' not in s:
        s=once(s,"""        LANG.diacritic_map.forEach(([accented, plain]) => {
            t = t.split(accented).join(plain);
        });
""","""        LANG.diacritic_map.forEach(([accented, plain]) => {
            t = t.split(accented).join(plain);
        });
        (LANG.digraph_map || []).forEach(([a, b]) => { t = t.split(a).join(b); });   /* a long vowel written two ways (ou / ei) */
""")
        s=once(s,"collapse_double_vowels: false,","collapse_double_vowels: false,\n    digraph_map: [],   /* optional pairs treated as one when checking, e.g. [[\"ou\",\"o\"],[\"ei\",\"e\"]] */")
    if 'window.__kitReset = function' not in s:
        s=once(s,"document.addEventListener('DOMContentLoaded', initializeApp);","document.addEventListener('DOMContentLoaded', initializeApp);\n    window.__kitReset = function () {   /* phone kit: the Reset button */\n        learnedItems.fill(false); var li = document.getElementById('learned-items'); if (li) li.innerHTML = '';\n        if (window.createTextBoxes) window.createTextBoxes(); positionArrowOnDirection(0);\n    };")
    return s
def rice(s):
    """Rice: two modes (States/Transitions); wOf(i,k,txt) / hOf(i,k); the counter reads learnedS / learnedT."""
    if 'window.__KIT = {' not in s: s=once(s,'<script id="kit-script">','<script>window.__KIT = { faceR: 50, adapt: true };   /* Rice: the words sit OUTSIDE the water ring, so the circle shrinks until they fit */</script>\n<script id="kit-script">')
    if 'window.__kitCount = function' not in s: s=once(s,"window.updateVisibleTextBoxes = refresh;","window.updateVisibleTextBoxes = refresh;\n    window.__kitCount = function () { return transMode ? [learnedT.filter(Boolean).length, T.length] : [learnedS.filter(Boolean).length, S.length]; };   /* phone kit: Learned n/total for the mode now showing */")
    if 'kit: Quiz placed by CSS' not in s: s=once(s,"function placeQuiz() {\n        if (qc.dataset.moved === '1') return;","function placeQuiz() {   /* kit: Quiz placed by CSS */\n        return;\n        if (qc.dataset.moved === '1') return;")
    if 'function lay(' not in s:
        s=once(s,"function wOf(i, k, txt) { cv.font = '700 ' + sizeOf(i, k) + 'px ' + FONT; return cv.measureText(plain(txt)).width + 3; }\n    function hOf(i, k) { return sizeOf(i, k) * 1.35; }",LAYR)
        s=once(s,"w = wOf(i, k, word(i, k)), h = hOf(i, k), a =","w = wOf(i, k, word(i, k)), h = hOf(i, k, word(i, k)), a =")
        s=once(s,"var k = curK(i), w = wOf(i, k, fo.querySelector('div').innerHTML), h = hOf(i, k);","var k = curK(i), w = wOf(i, k, fo.querySelector('div').innerHTML), h = hOf(i, k, fo.querySelector('div').innerHTML);")
        s=once(s,"fo.setAttribute('width', r.w); fo.setAttribute('height', r.h); fo.style.overflow = 'visible'; }","fo.setAttribute('width', r.w); fo.setAttribute('height', r.h); fo.style.overflow = 'visible'; var dv = fo.querySelector('div'); if (dv) { var multi = r.h > sizeOf(i, curK(i)) * 1.6; dv.style.whiteSpace = multi ? 'normal' : 'nowrap'; dv.style.lineHeight = multi ? '1.2' : ''; fo.dataset.wrap = multi ? '1' : ''; } }")
    return s
def wrapit(s,path):
    if 'function lay(' in s:
        return s.replace("dv.style.lineHeight = multi ? '1.2' : ''; }","dv.style.lineHeight = multi ? '1.2' : ''; fo.dataset.wrap = multi ? '1' : ''; }") if 'fo.dataset.wrap = multi' not in s else s
    m=re.search(r"( *)function wOf\(i, txt\) \{ cv\.font = '700 ' \+ sizeOf\(i\) \+ 'px ' \+ FONT; return cv\.measureText\(plain\(txt\)\)\.width \+ 3; \}\n *function hOf\(i\) \{ return sizeOf\(i\) \* 1\.35; \}",s)
    if not m: print('  WRAP skipped (no wOf/hOf)',path); return s
    s=s[:m.start()]+m.group(1)+LAY+s[m.end():]
    s,n1=re.subn(r"\bw = wOf\(i, ([^;]*?)\), h = hOf\(i\)",r"tx_ = \1, w = wOf(i, tx_), h = hOf(i, tx_)",s)
    s=re.sub(r"var tx_ = ([^;]*?), w = wOf",r"var tx_ = \1, w = wOf",s)
    # the first form was 'var w = wOf(' -> 'var tx_ = ..., w = ...' ; fix a leading 'var tx_'
    n2=0
    def dv(mm):
        nonlocal n2; n2+=1
        return mm.group(0)+" var dv = fo.querySelector('div'); if (dv) { var multi = r.h > sizeOf(i) * 1.6; dv.style.whiteSpace = multi ? 'normal' : 'nowrap'; dv.style.lineHeight = multi ? '1.2' : ''; fo.dataset.wrap = multi ? '1' : ''; }"
    s=re.sub(r"fo\.setAttribute\('width', r\.w\); fo\.setAttribute\('height', r\.h\);",dv,s,count=1)
    print('  wrap sites',n1,n2)
    return s
def day(s):
    """Parts of the Day: HTML clock (svg + html frame + html word boxes inside #circle-container); its own phone layout; its own Quiz (ids renamed to the kit's)."""
    for a,b in (("'quiz-input'","'quizInput'"),('id="quiz-input"','id="quizInput"'),("'quiz-submit'","'quizCheck'"),('id="quiz-submit"','id="quizCheck"'),("'quiz-feedback'","'quizFeedback'"),('id="quiz-feedback"','id="quizFeedback"'),('class="quiz-feedback"','class="quizFeedback"'),('.quiz-feedback {','.quizFeedback {'),('id="quiz-container"','id="quizContainer"'),("getElementById('quiz-container')","getElementById('quizContainer')")):
        s=s.replace(a,b)
    s=re.sub(r"quizContainer\.classList\.add\('visible'\);(?! quizContainer\.style)","quizContainer.classList.add('visible'); quizContainer.style.display = 'block';",s)
    s=re.sub(r"quizContainer\.classList\.remove\('visible'\);(?! quizContainer\.style)","quizContainer.classList.remove('visible'); quizContainer.style.display = 'none';",s)
    s=s.replace("fb.style.color = '#f44336';","fb.style.color = 'red';")
    if 'id="dayZoom"' not in s:
        s=once(s,'<svg id="clock-svg"','<div id="dayClip" style="position:absolute;inset:0;overflow:hidden"><div id="dayZoom" style="position:absolute;inset:0"><svg id="clock-svg"')   # the ring and its frame zoom together inside this box; the words stay outside it
        s=once(s,'<div id="draggable-frame" class="draggable-frame"></div>','<div id="draggable-frame" class="draggable-frame"></div></div></div>')
    if 'window.__KIT = {' not in s: s=once(s,'<script id="kit-script">','<script>window.__KIT = { svgId: "dayZoom", progHost: ".container", nofit: true, hintTouch: "Drag the blue frame round the clock. Tap a word to see it in the other language. Pinch with two fingers to zoom.", hint: "Drag the blue frame round the clock. Click a word to see it in the other language." };   /* Day: the ring scales itself (isCompact), so the kit does not re-fit it; Full Screen zoom moves the whole circle */</script>\n<script id="kit-script">')
    if "closest('.text-box.sa, .text-box.active:not(.learned)')" not in s:   # pull-out inspection also on the word shown in the ordinary view (not only in Show All)
        s=once(s,"const box = e.target.closest ? e.target.closest('.text-box.sa') : null;","const box = e.target.closest ? e.target.closest('.text-box.sa, .text-box.active:not(.learned)') : null;")
    if 'kit: the ring may be zoomed' not in s:
        s=once(s,"    const rect   = circleContainer.getBoundingClientRect();\n    const dx     =","    const rect   = svg.getBoundingClientRect();   /* kit: the ring may be zoomed in Full Screen, so the angle is measured from the ring's own centre */\n    const dx     =")
    if 'window.__kitReset = function' not in s:
        s=once(s,"// --- Event listeners ------------------------------------------------","""window.__kitCount = function () { return [learned.size, vocabularyData.length]; };
window.__kitReset = function () {   /* phone kit: the Reset button - every learned word cleared, the frame back at sunrise */
    learned.clear(); currentItem = null; showAllState = 0;
    quizContainer.classList.remove('visible'); quizContainer.style.display = 'none';
    textBoxContainer.innerHTML = ''; createTextBoxes();
    document.querySelectorAll('.sector').forEach(x => x.classList.remove('active'));
    applyShowAll(); updateProgress(); positionDraggableFrame(6);
};

// --- Event listeners ------------------------------------------------""")
    # answers: alternatives (LANG.alt_answers) and "almost" feedback; LOG also goes through AnswerUtils (macrons, ou/ei)
    if 'window.__kitLast = { input: answer' not in s:
        if 'const AnswerUtils = {' in s:
            s=once(s,"        if (answer.toLowerCase() === correct) {","        window.__kitLast = { input: answer, correct: item.tlr, ok: false };\n        if ((typeof AnswerUtils !== 'undefined' ? AnswerUtils.checkAnswer(answer, item.tlr) : answer.toLowerCase() === correct) || window.__kitAlt(answer, item.tlr)) {")
        else:
            s=once(s,"        if (answer.toLowerCase() === correct) {","        window.__kitLast = { input: answer, correct: item.tl, ok: false };\n        if (answer.toLowerCase() === correct || window.__kitAlt(answer, item.tl)) {")
    if 'const AnswerUtils = {' in s and '(LANG.digraph_map ||' not in s:
        s=once(s,"        if (LANG.collapse_double_vowels) {","        (LANG.digraph_map || []).forEach(([a, b]) => { t = t.split(a).join(b); });   /* a long vowel written two ways (ou / ei) */\n        if (LANG.collapse_double_vowels) {")
    if 'const AnswerUtils = {' in s and 'id="quizDiacriticNote"' not in s:
        s=once(s,'    <div id="quizFeedback" class="quizFeedback"></div>','    <div id="quizDiacriticNote" style="font-size:12px;color:#555;margin-top:8px;"></div>\n    <div id="quizFeedback" class="quizFeedback"></div>')
        s=once(s,"    document.getElementById('quizInput').focus();\n","    document.getElementById('quizInput').focus();\n    document.getElementById('quizDiacriticNote').textContent = LANG.diacritic_instructions || '';\n")
    return s
def clk(s):
    """Clock: a live analogue clock with greeting / time / part-of-day panels. No Quiz, no frame: the kit adds the Full Screen zoom (of #clock), touch targets and the first-use hint."""
    if 'window.__KIT = {' not in s: s=once(s,'<script id="kit-script">','<script>window.__KIT = { svgId: "clock", nofit: true, hintTouch: "Set a time with the Hour and Min buttons. Touch a box to see what it asks. Pinch with two fingers to zoom.", hint: "Set a time with the Hour and Min buttons. Move over a box to see what it asks." };   /* Clock: nothing to fit or learn; Full Screen zoom moves the clock face */</script>\n<script id="kit-script">')
    return s
def cal(s):
    """Calendar (365-day ring): ids already match the kit; the ring is svg #svgCanvas; Show All words are measured to fit the phone view; Learned counter counts the special days."""
    if 'window.__KIT = {' not in s:
        cfg = r"""<script>window.__KIT = { noHint: true, nofit: true, progClass: 'kit-cal' };   /* Calendar: its own instruction panel replaces the first-use hint; the view box is fitted by the code below */
(function () {
  var svg = document.getElementById('svgCanvas'), phone = window.matchMedia('(max-width: 700px) and (orientation: portrait)'), busy = false, pend = 0;
  window.__kitCount = function () { return [SPECIAL.filter(function (x) { return learned[x.i]; }).length, SPECIAL.length]; };   /* phone kit: Learned n/total */
  function wrapWords() {   /* portrait phone: a Show All phrase of two or more words breaks onto 2 lines, so the ring can stay big (kept as ONE text string in __full; the audio looks it up by textContent) */
    var g = document.getElementById('showAllLayer'); if (!g) return;
    Array.prototype.forEach.call(g.children, function (t) {
      var plain = !t.firstChild || t.firstChild.nodeType === 3;
      if (plain) t.__full = t.textContent;
      var full = t.__full || t.textContent, want = phone.matches && full.indexOf(' ') > 0 && full.length > 12;
      if (!plain && !want) { t.textContent = full; return; }
      if (!(plain && want)) return;
      var w = full.split(' '), best = 1, bd = 1e9, i, n;
      for (i = 1; i < w.length; i++) { n = w.slice(0, i).join(' ').length; if (Math.abs(n - (full.length - n - 1)) < bd) { bd = Math.abs(n - (full.length - n - 1)); best = i; } }
      var l1 = w.slice(0, best).join(' '), l2 = w.slice(best).join(' '), x = t.getAttribute('x'), y = +t.getAttribute('y'), up = t.getAttribute('text-anchor') === 'middle' ? (y < 50 ? -1.1 : 0) : -0.55;
      t.textContent = ''; [l1 + ' ', l2].forEach(function (ln, k) { var ts = document.createElementNS('http://www.w3.org/2000/svg', 'tspan'); ts.setAttribute('x', x); ts.setAttribute('dy', (k ? 1.1 : up) + 'em'); ts.textContent = ln; t.appendChild(ts); });
      t.__full = full;
    });
  }
  function fit() {   /* portrait phone: the ring is made as big as the words around it allow */
    if (busy || !svg) return; busy = true;
    try {
      wrapWords();
      var cw = svg.clientWidth, ch = svg.clientHeight; if (!cw || !ch) return;
      var m0 = phone.matches ? 8.5 : 0, m1 = 100 - m0, x0 = m0, x1 = m1, y0 = m0, y1 = m1, g = document.getElementById('showAllLayer');   /* phone: the ring only; otherwise the whole 100 x 100 drawing, as before */
      if (g) Array.prototype.forEach.call(g.children, function (t) { try { var b = t.getBBox(); x0 = Math.min(x0, b.x); x1 = Math.max(x1, b.x + b.width); y0 = Math.min(y0, b.y); y1 = Math.max(y1, b.y + b.height); } catch (e) {} });
      if (phone.matches || g) { x0 -= 1.5; x1 += 1.5; y0 -= 1.5; y1 += 1.5; }   /* the view box is centred on the ring AND its words, so a long word on one side does not shrink the ring on the other */
      var vw = Math.max(x1 - x0, (y1 - y0) * cw / ch), vh = vw * ch / cw, vb = ((x0 + x1) / 2 - vw / 2) + ' ' + ((y0 + y1) / 2 - vh / 2) + ' ' + vw + ' ' + vh;
      if (svg.getAttribute('viewBox') !== vb) svg.setAttribute('viewBox', vb);
    } finally { busy = false; }
  }
  function soon() { cancelAnimationFrame(pend); pend = requestAnimationFrame(fit); }
  if (svg) {
    new MutationObserver(function () { if (!busy) soon(); }).observe(svg, { childList: true, subtree: true, attributes: true, attributeFilter: ['x', 'y', 'style', 'transform', 'font-size', 'class'] });
    window.addEventListener('resize', soon); window.addEventListener('orientationchange', soon); window.addEventListener('load', function () { setTimeout(soon, 50); setTimeout(soon, 400); });
    if (phone.addEventListener) phone.addEventListener('change', soon); soon();
  }
  (function () {   /* Tools menu: Exercises & Tests (the User Manual button is already there) */
    var m = document.getElementById('userManualBtn'); if (!m || document.getElementById('exercisesBtn')) return;
    var x = document.createElement('button'); x.id = 'exercisesBtn'; x.type = 'button'; x.textContent = 'Exercises & Tests'; x.title = 'Practise this vocabulary (opens the Index of Exercises)';
    m.parentNode.insertBefore(x, m.nextSibling);
    x.addEventListener('click', function (e) { e.stopPropagation(); var dd = document.querySelector('.tools-dropdown'); if (dd) dd.classList.remove('active'); window.open('https://sites.google.com/view/conceptionary/home/index-of-exercises', '_blank', 'noopener'); });
  })();
})();
</script>
<script id="kit-script">"""
        s=once(s,'<script id="kit-script">',cfg)
    if 'window.__kitLast = { input: answer, correct: sp.' not in s:
        m=re.search(r"const exact +=\s*answer\.toLowerCase\(\) === sp\.(tlr|tl)\.toLowerCase\(\);",s)
        assert m,'CAL: no exact line'
        k=m.group(1)
        s=once(s,"    if (exact || normalized) {","    window.__kitLast = { input: answer, correct: sp."+k+", ok: false };\n    if (exact || normalized || window.__kitAlt(answer, sp."+k+")) {")
    if 'digraph_map' not in s:
        s=once(s,"    return str.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();","    let t = str.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();\n    (LANG.digraph_map || []).forEach(([a, b]) => { t = t.split(a).join(b); });   /* a long vowel written two ways (ou / ei) */\n    return t;")
        s=once(s,"    diacritic_chars: [],","    diacritic_chars: [],\n    digraph_map: [],   /* optional pairs treated as one when checking, e.g. [[\"ou\",\"o\"],[\"ei\",\"e\"]] */")
    return s
def run(path):
    s=open(path).read()
    s=re.sub(r'<style id="kit-style">.*?</style>\n','',s,flags=re.S); s=re.sub(r'<script id="kit-script">.*?</script>\n','',s,flags=re.S)
    s=once(s,'</head>','<style id="kit-style">\n'+css+'</style>\n</head>')
    s=once(s,'</body>','<script id="kit-script">\n'+js+'</script>\n</body>')
    s=re.sub(r'<!-- Last updated:[^>]*-->\n?','',s)
    s=once(s,'<!DOCTYPE html>','<!DOCTYPE html>\n'+stamp) if s.startswith('<!DOCTYPE html>') else s
    if 'max-width: 0px' not in s:
        s,nmq=re.subn(r"var mq = window\.matchMedia\('\(pointer: coarse\) and \(max-width: 700px\), \(pointer: coarse\) and \(max-height: 520px\) and \(orientation: landscape\)'\);","var mq = window.matchMedia('(max-width: 0px) and (min-width: 1px)');   /* the Quiz now shows on phones too (phone kit) */",s)
        if not nmq: print('  NOTE: no mq line found in',path)
    s=s.replace('<html lang="en" class="no-quiz"','<html lang="en"')
    if 'dow/' in path:
        s=s.replace("if (files && files[text]) { playUrl(files[text], done); return; }","if (files && files[text] && (!code || code === tlCode())) { playUrl(files[text], done); return; }")
    if 'function checkQuizAnswer' in s:
        if '__kitLast' not in s:
            m=re.search(r"( +)const normalizedUserAnswer = normalizeText\(userAnswer\);\n",s)
            if m: s=s[:m.end()]+m.group(1)+"window.__kitLast = { input: userAnswer, correct: correctAnswerTL, ok: false };\n"+s[m.end():]
            else: print('  NOTE: no normalizedUserAnswer line in',path)
        if '__kitAlt(userAnswer' not in s:
            s,n=re.subn(r"(normalizedUserAnswer === normalizedCorrectTLR?)\) \{",r"\1 || window.__kitAlt(userAnswer, correctAnswerTL)) {",s,count=1)
            if n!=1:
                s,n2=re.subn(r"( +)if \((\w+)\.toLowerCase\(\) === (\w+)\.toLowerCase\(\)\) \{",lambda m:m.group(1)+"window.__kitLast = { input: "+m.group(2)+", correct: "+m.group(3)+", ok: false };\n"+m.group(1)+"if ("+m.group(2)+".toLowerCase() === "+m.group(3)+".toLowerCase() || window.__kitAlt("+m.group(2)+", "+m.group(3)+")) {",s,count=1)
                if n2!=1 and 'AnswerUtils.checkAnswer(' not in s: print('  NOTE: answer condition not patched in',path)
    if 'sw/' in path: s=sw(s)
    if 'cmp/' in path: s=cmp_(s)
    if 'day/' in path: s=day(s)
    if 'cal/' in path: s=cal(s)
    if 'clk/' in path: s=clk(s)
    if 'rice/' in path: s=rice(s)
    else: s=wrapit(s,path)
    open(path,'w').write(s); print('patched',path)
for p in sys.argv[1:]: run(p)