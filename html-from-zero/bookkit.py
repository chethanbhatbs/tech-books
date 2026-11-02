"""Shared page kit for the book-style courses: sketch helpers, CSS, JS.
Copied from the Python course build.py on 2026-10-16."""
import html
esc = html.escape


def sbox(x, y, w, h, lines, fill="hb", size=19, mono=False):
    cls = "mono" if mono else "hand"
    t = []
    n = len(lines)
    for i, ln in enumerate(lines):
        ty = y + h / 2 + (i - (n - 1) / 2) * (size * 1.25) + size * 0.35
        t.append(f'<text x="{x + w / 2}" y="{ty:.1f}" class="{cls}" font-size="{size}" text-anchor="middle">{esc(ln)}</text>')
    return (f'<g filter="url(#rough)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="url(#{fill})" class="stroke"/>'
            f'<rect x="{x + 1.5}" y="{y - 1}" width="{w - 2}" height="{h + 1}" rx="9" fill="none" class="stroke thin"/></g>'
            + "".join(t))


def sarrow(x1, y1, x2, y2, label=None, lx=None, ly=None, size=16, curve=0):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - curve
    s = (f'<path d="M{x1},{y1} Q{mx},{my} {x2},{y2}" class="stroke arrow" fill="none" '
         f'marker-end="url(#ah)" filter="url(#rough)"/>')
    if label:
        lx = mx if lx is None else lx
        ly = (my - 8) if ly is None else ly
        s += f'<text x="{lx}" y="{ly}" class="hand note" font-size="{size}" text-anchor="middle">{esc(label)}</text>'
    return s


def stext(x, y, txt, size=17, cls="hand note", anchor="start"):
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" text-anchor="{anchor}">{esc(txt)}</text>'


def figure(w, h, inner, caption, minw=560):
    return (f'<figure class="sketch"><div class="sketch-scroll"><svg viewBox="0 0 {w} {h}" '
            f'style="min-width:{minw}px" role="img" aria-label="{esc(caption)}">{inner}</svg></div>'
            f'<figcaption>{caption}</figcaption></figure>')


DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="rough" filterUnits="userSpaceOnUse" x="-50" y="-50" width="1100" height="800"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="2.6"/></filter>
<pattern id="hb" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(-40)"><line x1="0" y1="0" x2="0" y2="9" stroke="#B23A16" stroke-width="1.3" opacity=".30"/></pattern>
<pattern id="hy" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(-40)"><line x1="0" y1="0" x2="0" y2="9" stroke="#E8833A" stroke-width="1.6" opacity=".45"/></pattern>
<pattern id="hg" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(-40)"><line x1="0" y1="0" x2="0" y2="9" stroke="#2B7A4B" stroke-width="1.3" opacity=".32"/></pattern>
<pattern id="hr" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(-40)"><line x1="0" y1="0" x2="0" y2="9" stroke="#B42318" stroke-width="1.3" opacity=".30"/></pattern>
<pattern id="hn" width="9" height="9" patternUnits="userSpaceOnUse"><rect width="9" height="9" fill="#FFFFFF"/></pattern>
<marker id="ah" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse"><path d="M1,1 L10,6 L1,11" fill="none" stroke="#18222E" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs></svg>'''


CSS = r'''
:root {
  /* Layout: a docs rail on the left, one reading column, sketches break out to full column width. Light only. */
  --paper: #F5F7FA;
  --sheet: #FFFFFF;
  --ink: #18222E;
  --muted: #5A6573;
  --line: rgba(24, 34, 46, 0.14);
  --py-blue: #B23A16;
  --py-yellow: #F16529;
  --blue-wash: #FBEDE7;
  --yellow-wash: #FDF1EA;
  --ok: #23703F;
  --ok-wash: #E8F4EC;
  --bad: #B42318;
  --bad-wash: #FCEBEA;
  --trap: #8A5A00;
  --trap-wash: #FFF4DC;
  --code-bg: #F2F4F7;
  --f-body: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  --f-mono: "IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
  --f-hand: "Kalam", "Comic Sans MS", cursive;
  color-scheme: light;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
body { background: var(--paper); color: var(--ink); font-family: var(--f-body); font-size: 16px; line-height: 1.6; }
.wm { position: fixed; right: 4vw; bottom: 6vh; width: 380px; height: 380px; opacity: 0.06; pointer-events: none; z-index: 2; }
.shell { position: relative; z-index: 1; display: grid; grid-template-columns: 264px minmax(0, 1fr); max-width: 1240px; margin: 0 auto; }
.rail { position: sticky; top: env(safe-area-inset-top, 0px); height: 100vh; overflow-y: auto; padding: 32px 16px 32px max(16px, env(safe-area-inset-left, 0px)); border-right: 1px solid var(--line); }
.brand { color: var(--ink); text-decoration: none; display: flex; align-items: center; gap: 10px; font-weight: 600; font-size: 18px; margin: 0 8px 24px; }
.brand svg { width: 30px; height: 30px; flex: none; }
.rail h4 { font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); margin: 20px 8px 6px; }
.rail ol { list-style: none; margin: 0; padding: 0; display: grid; gap: 2px; }
.rail a { display: grid; grid-template-columns: 26px minmax(0, 1fr); align-items: center; height: 34px; padding: 0 8px; border-radius: 6px; color: var(--ink); text-decoration: none; font-size: 14px; white-space: nowrap; }
.rail a span:last-child { overflow: hidden; text-overflow: ellipsis; }
.rail a .n { color: var(--muted); font-variant-numeric: tabular-nums; font-family: var(--f-mono); font-size: 12px; }
.rail a:hover { background: var(--code-bg); }
.rail a.active { background: var(--blue-wash); color: var(--py-blue); font-weight: 600; }
.rail li.soon { display: grid; grid-template-columns: 26px minmax(0, 1fr); align-items: center; height: 30px; padding: 0 8px; font-size: 14px; color: var(--muted); white-space: nowrap; overflow: hidden; }
.rail li.soon .n { font-family: var(--f-mono); font-size: 12px; }
main { min-width: 0; padding-block: 48px 120px; padding-left: max(16px, 48px); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.col { max-width: 800px; }
.hero { position: relative; }
.hero h1 { font-size: 36px; line-height: 1.2; font-weight: 600; margin: 0 0 12px; text-wrap: balance; letter-spacing: -0.01em; }
.hero p { margin: 0 0 12px; color: var(--muted); font-size: 18px; }
.hero .how { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 24px; }
.hero .how div { background: var(--sheet); border: 1px solid var(--line); border-radius: 6px; padding: 12px 16px; font-size: 14px; color: var(--ink); }
.hero .how b { display: block; font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin-bottom: 4px; }
.hero .meta { font-size: 14px; color: var(--muted); margin-top: 16px; }
.hero-art { position: absolute; right: 0; top: -12px; width: 150px; opacity: 0.9; }
/* Book pages: one sheet per chapter. With JS only the current sheet shows; print puts each on a new page. */
.page { position: relative; background: var(--sheet); border: 1px solid var(--line); border-radius: 8px; padding: 48px 56px 24px; margin-bottom: 32px; scroll-margin-top: 16px; }
.paged .page:not(.current) { display: none; }
.pager { display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); align-items: start; gap: 16px; margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--line); font-size: 14px; }
.pager a { color: var(--py-blue); text-decoration: none; display: grid; gap: 2px; }
.pager a:hover { text-decoration: underline; }
.pager a span { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }
.pager .nextp { text-align: right; }
.pager .pno { font-family: var(--f-mono); font-size: 12px; color: var(--muted); }
.topic { scroll-margin-top: 16px; }
.topic-head { position: relative; margin-bottom: 24px; }
.chapno { font-size: 36px; line-height: 1.2; font-weight: 600; color: var(--py-blue); padding-bottom: 12px; margin-bottom: 16px; border-bottom: 2px solid var(--py-yellow); }
.topic h2 { font-size: 28px; line-height: 1.25; font-weight: 600; margin: 4px 0 8px; text-wrap: balance; }
.topic .goal { color: var(--muted); font-size: 18px; margin: 0; }
.toc { margin: 24px 0 0; padding: 0; list-style: none; font-size: 16px; border-top: 1px solid var(--line); }
.toc li { border-bottom: 1px solid var(--line); }
.toc a { display: grid; grid-template-columns: 48px minmax(0, 1fr); align-items: baseline; padding: 8px 0; color: var(--py-blue); text-decoration: none; }
.toc a:hover { text-decoration: underline; }
.toc .rn { font-family: var(--f-mono); color: var(--muted); font-size: 14px; }
h3 { font-size: 22px; line-height: 1.3; font-weight: 600; margin: 0 0 8px; text-wrap: balance; }
.prose p, .concept p { margin: 0 0 12px; }
.prose ul { margin: 0 0 12px; padding-left: 22px; }
.prose li { margin-bottom: 4px; }
code { font-family: var(--f-mono); font-size: 14px; background: var(--code-bg); padding: 1px 5px; border-radius: 4px; }
.concept, .rule { margin: 32px 0 0; scroll-margin-top: 12px; }
.rule h3 { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 12px; }
.rnum { font-family: var(--f-mono); font-size: 14px; font-weight: 500; color: var(--py-blue); background: var(--blue-wash); padding: 2px 8px; border-radius: 4px; }
.case { background: var(--sheet); border: 1px solid var(--line); border-radius: 6px; margin: 12px 0; overflow: hidden; }
.case-h { font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; padding: 6px 14px; }
.case.good .case-h { background: var(--ok-wash); color: var(--ok); }
.case.bad .case-h { background: var(--bad-wash); color: var(--bad); }
.case.trap .case-h { background: var(--trap-wash); color: var(--trap); }
.case .mark { font-size: 14px; margin-right: 2px; }
.case.trap .why { padding: 0 14px 12px; }
.exlabel { margin: 0; padding: 8px 14px 0; font-size: 14px; color: var(--muted); }
pre { margin: 0; overflow-x: auto; }
pre.code { padding: 12px 14px; font-family: var(--f-mono); font-size: 14px; line-height: 1.6; background: var(--sheet); }
pre.code code { background: none; padding: 0; font-size: 14px; }
.concept pre.code, .rule .prose pre.code { border: 1px solid var(--line); border-radius: 6px; margin: 0 0 12px; }
pre.shell { background: var(--code-bg); }
.outlabel { font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); padding: 8px 14px 0; border-top: 1px dashed var(--line); }
pre.out { padding: 4px 14px 12px; font-family: var(--f-mono); font-size: 14px; line-height: 1.6; color: var(--ink); white-space: pre; }
pre.out .tb { color: var(--muted); }
pre.out .errline { color: var(--bad); font-weight: 600; }
pre.out .muted { color: var(--muted); font-style: italic; }
.why { margin: 8px 0 0; }
.tablewrap { overflow-x: auto; margin: 16px 0; background: var(--sheet); border: 1px solid var(--line); border-radius: 6px; }
table { border-collapse: collapse; width: 100%; font-size: 14px; }
th { text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); font-weight: 600; background: var(--code-bg); }
th, td { padding: 8px 14px; border-bottom: 1px solid var(--line); vertical-align: top; }
tr:last-child td { border-bottom: 0; }
td code { white-space: nowrap; }
figure.sketch { margin: 24px 0; background: var(--sheet); border: 1px solid var(--line); border-radius: 6px; }
.sketch-scroll { overflow-x: auto; padding: 12px; }
figure.sketch svg { display: block; width: 100%; height: auto; }
figure.sketch figcaption { font-size: 14px; color: var(--muted); padding: 8px 14px 12px; border-top: 1px dashed var(--line); }
svg .stroke { stroke: var(--ink); stroke-width: 1.8; stroke-linejoin: round; stroke-linecap: round; }
svg .stroke.thin { stroke-width: 0.9; opacity: 0.55; }
svg .arrow { stroke-width: 1.7; }
svg .hand { font-family: var(--f-hand); fill: var(--ink); }
svg .note { fill: var(--muted); }
svg .mono { font-family: var(--f-mono); fill: var(--ink); }
svg .mono.note { fill: var(--muted); }
svg .err { fill: var(--bad); font-weight: 600; }
.exercises { margin-top: 48px; background: var(--sheet); border: 1px solid var(--line); border-radius: 8px; padding: 24px; }
.exercises .hint { color: var(--muted); font-size: 14px; margin: 0 0 16px; }
.exlist { list-style: none; margin: 0; padding: 0; display: grid; gap: 24px; }
.ex { min-width: 0; border-top: 1px solid var(--line); padding-top: 16px; }
.ex:first-child { border-top: 0; padding-top: 0; }
.ex-h { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.ex-n { font-family: var(--f-mono); font-size: 14px; font-weight: 600; color: var(--ink); font-variant-numeric: tabular-nums; }
.ex-kind { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); font-weight: 600; }
.ex p { margin: 0 0 8px; }
.ex pre.code { border: 1px solid var(--line); border-radius: 6px; margin-bottom: 8px; background: var(--code-bg); }
textarea.mine { width: 100%; font: 14px/1.5 var(--f-mono); color: var(--ink); background: var(--paper); border: 1px solid var(--line); border-radius: 6px; padding: 8px 12px; resize: vertical; }
textarea.mine:focus { outline: 2px solid var(--py-blue); outline-offset: 1px; background: var(--sheet); }
details { margin-top: 8px; }
summary { cursor: pointer; font-size: 14px; font-weight: 600; color: var(--py-blue); width: fit-content; padding: 4px 0; }
summary:focus-visible { outline: 2px solid var(--py-blue); outline-offset: 2px; border-radius: 4px; }
details[open] { background: var(--paper); border: 1px solid var(--line); border-radius: 6px; padding: 4px 0 12px; }
details[open] summary { padding: 4px 14px; }
details .why { padding: 0 14px; }
details pre.code { background: var(--sheet); margin: 8px 14px; border: 1px solid var(--line); border-radius: 6px; }
details .outlabel { border-top: 0; }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
.next { margin-top: 56px; padding: 24px; border: 1px dashed var(--line); border-radius: 8px; color: var(--muted); }
.next h3 { color: var(--ink); }
@media print {
  .rail, .pager, .wm { display: none; }
  .shell { display: block; }
  .page { display: block !important; border: 0; padding: 0; break-before: page; }
}
a:focus-visible { outline: 2px solid var(--py-blue); outline-offset: 2px; }
/* Prism, light */
.token.comment { color: #6A737D; font-style: italic; }
.token.string { color: #0A7A3E; }
.token.number, .token.boolean { color: #B35900; }
.token.keyword { color: #7A3EB0; }
.token.builtin, .token.function { color: #1D5FA0; }
.token.operator, .token.punctuation { color: #5A6573; }
.token.class-name { color: #1D5FA0; }
@media (max-width: 900px) {
  .shell { grid-template-columns: minmax(0, 1fr); }
  .rail { position: static; height: auto; border-right: 0; border-bottom: 1px solid var(--line); padding: 20px max(16px, env(safe-area-inset-right, 0px)) 16px max(16px, env(safe-area-inset-left, 0px)); }
  .rail ol { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .rail .soonlist { display: none; }
  main { padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-top: 24px; }
  .hero .how { grid-template-columns: minmax(0, 1fr); }
  .page { padding: 24px 16px 16px; border-radius: 6px; }
  .wm { width: 220px; height: 220px; }
  .hero h1 { font-size: 28px; }
  .chapno { font-size: 28px; }
  .pager { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
  .pager .pno { display: none; }
  .exercises { padding: 16px; }
}
'''

JS = r'''
(function () {
  var pages = Array.prototype.slice.call(document.querySelectorAll('.page'));
  var links = Array.prototype.slice.call(document.querySelectorAll('.rail a[href^="#t-"]'));
  document.documentElement.classList.add('paged');
  function show() {
    var id = decodeURIComponent(location.hash.slice(1));
    var el = id ? document.getElementById(id) : null;
    var pg = el ? el.closest('.page') : null;
    if (!pg) { pg = pages[0]; el = null; }
    pages.forEach(function (p) { p.classList.toggle('current', p === pg); });
    links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + pg.id); });
    if (el && el !== pg) el.scrollIntoView({ behavior: 'instant' }); else window.scrollTo({ top: 0, behavior: 'instant' });
  }
  window.addEventListener('hashchange', show);
  show();
  document.addEventListener('keydown', function (e) {
    if (e.target.closest('textarea, input, select') || e.metaKey || e.ctrlKey || e.altKey) return;
    var cur = document.querySelector('.page.current');
    if (!cur) return;
    var a = e.key === 'ArrowRight' ? cur.querySelector('.pager .nextp') : e.key === 'ArrowLeft' ? cur.querySelector('.pager .prev') : null;
    if (a) { e.preventDefault(); location.hash = a.getAttribute('href'); }
  });
  document.querySelectorAll('textarea.mine').forEach(function (t) {
    var k = 'pyc-' + t.id;
    try { var v = localStorage.getItem(k); if (v) t.value = v; } catch (e) {}
    t.addEventListener('input', function () { try { localStorage.setItem(k, t.value); } catch (e) {} });
  });
})();
'''

