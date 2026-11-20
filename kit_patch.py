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
    if 'window.__KIT = {' not in s: s=once(s,'<script id="kit-script">','<script>window.__KIT = { svgId: "sv", nofit: true, keepNoQuiz: true, hintTouch: "Turn the wheel with one finger. Tap a phrase to see it in the other language. Pinch with two fingers to zoom.", hint: "Turn the wheel. Click a phrase to see it in the other language." };</script>\n<script id="kit-script">')
    if 'window.__kitCount = function' not in s: s=once(s,"window.__swLayout(); window.__swFit(); renders.forEach(function (r) { r(); }); show(0);","window.__kitCount = function () { return [states.filter(function (x) { return x.learned; }).length, states.length]; };   /* phone kit: Learned n/total */\nwindow.__swLayout(); window.__swFit(); renders.forEach(function (r) { r(); }); show(0);")
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
def run(path):
    s=open(path).read()
    s=re.sub(r'<style id="kit-style">.*?</style>\n','',s,flags=re.S); s=re.sub(r'<script id="kit-script">.*?</script>\n','',s,flags=re.S)
    s=once(s,'</head>','<style id="kit-style">\n'+css+'</style>\n</head>')
    s=once(s,'</body>','<script id="kit-script">\n'+js+'</script>\n</body>')
    s=re.sub(r'<!-- Last updated:[^>]*-->\n?','',s)
    s=once(s,'<!DOCTYPE html>','<!DOCTYPE html>\n'+stamp) if s.startswith('<!DOCTYPE html>') else s
    if 'max-width: 0px' not in s and 'sw/' not in path:   # SW keeps its Quiz off on phones (an inline Quiz inside the wheel; Alan's earlier decision) until he decides otherwise
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
    if 'rice/' in path: s=rice(s)
    else: s=wrapit(s,path)
    open(path,'w').write(s); print('patched',path)
for p in sys.argv[1:]: run(p)