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
def wrapit(s,path):
    if 'function lay(' in s:
        return s.replace("dv.style.lineHeight = multi ? '1.2' : ''; }","dv.style.lineHeight = multi ? '1.2' : ''; fo.dataset.wrap = multi ? '1' : ''; }") if 'fo.dataset.wrap = multi' not in s else s
    old_w="function wOf(i, txt) { cv.font = '700 ' + sizeOf(i) + 'px ' + FONT; return cv.measureText(plain(txt)).width + 3; }"
    old_h="function hOf(i) { return sizeOf(i) * 1.35; }"
    s=once(s,old_w+"\n        "+old_h if 'dow/' in path else old_w+"\n    "+old_h, LAY)
    if 'dow/' in path:
        s=once(s,"var w = wOf(i, dayWord(i, kOf(i))), h = hOf(i), ux","var tx_ = dayWord(i, kOf(i)), w = wOf(i, tx_), h = hOf(i, tx_), ux")
        s=once(s,"var w = wOf(i, fo.querySelector('div').innerHTML), h = hOf(i), ux","var tx_ = fo.querySelector('div').innerHTML, w = wOf(i, tx_), h = hOf(i, tx_), ux")
        s=once(s,"fo.setAttribute('width', r.w); fo.setAttribute('height', r.h); fo.style.overflow = 'visible';","fo.setAttribute('width', r.w); fo.setAttribute('height', r.h); fo.style.overflow = 'visible';\n            var dv = fo.querySelector('div'); if (dv) { var multi = r.h > sizeOf(i) * 1.6; dv.style.whiteSpace = multi ? 'normal' : 'nowrap'; dv.style.lineHeight = multi ? '1.2' : ''; fo.dataset.wrap = multi ? '1' : ''; }")
    else:
        s=once(s,"var w = wOf(i, word(i, kFn(i))), h = hOf(i), a =","var tx_ = word(i, kFn(i)), w = wOf(i, tx_), h = hOf(i, tx_), a =")
        s=once(s,"var w = wOf(i, fo.querySelector('div').innerHTML), h = hOf(i);","var tx_ = fo.querySelector('div').innerHTML, w = wOf(i, tx_), h = hOf(i, tx_);")
        s=once(s,"fo.setAttribute('width', r.w); fo.setAttribute('height', r.h);","fo.setAttribute('width', r.w); fo.setAttribute('height', r.h); var dv = fo.querySelector('div'); if (dv) { var multi = r.h > sizeOf(i) * 1.6; dv.style.whiteSpace = multi ? 'normal' : 'nowrap'; dv.style.lineHeight = multi ? '1.2' : ''; fo.dataset.wrap = multi ? '1' : ''; }")
    return s

def run(path):
    s=open(path).read()
    s=re.sub(r'<style id="kit-style">.*?</style>\n','',s,flags=re.S); s=re.sub(r'<script id="kit-script">.*?</script>\n','',s,flags=re.S)
    s=once(s,'</head>','<style id="kit-style">\n'+css+'</style>\n</head>')
    s=once(s,'</body>','<script id="kit-script">\n'+js+'</script>\n</body>')
    s=re.sub(r'<!-- Last updated:[^>]*-->\n?','',s)
    s=once(s,'<!DOCTYPE html>','<!DOCTYPE html>\n'+stamp) if s.startswith('<!DOCTYPE html>') else s
    if 'sea/' in path:
        if 'max-width: 0px' not in s: s=once(s,"var mq = window.matchMedia('(pointer: coarse) and (max-width: 700px), (pointer: coarse) and (max-height: 520px) and (orientation: landscape)');","var mq = window.matchMedia('(max-width: 0px) and (min-width: 1px)');   /* the Quiz now shows on phones too, as a bottom sheet (phone kit) */")
    if 'dow/' in path:
        s=s.replace('<html lang="en" class="no-quiz"','<html lang="en"')
        s=s.replace("if (files && files[text]) { playUrl(files[text], done); return; }","if (files && files[text] && (!code || code === tlCode())) { playUrl(files[text], done); return; }")
        s=s.replace("if (files && files[text] && (!code || code === tlCode()) && (!code || code === tlCode()))","if (files && files[text] && (!code || code === tlCode()))")
    if 'dow/' in path:
        if '__kitLast' not in s:
            m=re.search(r"( +)const normalizedUserAnswer = normalizeText\(userAnswer\);\n",s); assert m
            s=s[:m.end()]+m.group(1)+"window.__kitLast = { input: userAnswer, correct: correctAnswerTL, ok: false };\n"+s[m.end():]
        if '__kitAlt(userAnswer' not in s:
            s,n=re.subn(r"(normalizedUserAnswer === normalizedCorrectTLR?)\) \{",r"\1 || window.__kitAlt(userAnswer, correctAnswerTL)) {",s,count=1); assert n==1
    s=wrapit(s,path)
    open(path,'w').write(s); print('patched',path)
for p in sys.argv[1:]: run(p)