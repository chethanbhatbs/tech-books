CSS = r'''
:root {
  --paper: #F4F5F7; --sheet: #FFFFFF; --ink: #1A2230; --muted: #5B6676; --line: rgba(26, 34, 48, 0.14);
  --acc: #C2381C; --acc2: #F05033; --wash: #FCEDE8; --wash2: #FFF6E5;
  --ok: #1F7A44; --ok-wash: #E7F4EC; --bad: #B42318; --bad-wash: #FCEBEA; --trap: #8A5A00; --trap-wash: #FFF4DC;
  --code-bg: #F1F3F6; --term-bg: #F7F8FA;
  --f-body: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  --f-mono: "IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
  --f-hand: "Kalam", "Comic Sans MS", cursive;
  color-scheme: light;
}
:root[data-theme="dark"] {
  --paper: #12161C; --sheet: #1A1F27; --ink: #E5E9EF; --muted: #9AA5B4; --line: rgba(229, 233, 239, 0.14);
  --acc: #FF8466; --acc2: #F05033; --wash: rgba(240, 80, 51, 0.16); --wash2: rgba(232, 168, 56, 0.14);
  --ok: #5CC489; --ok-wash: rgba(92, 196, 137, 0.13); --bad: #FF7A6E; --bad-wash: rgba(255, 122, 110, 0.13);
  --trap: #E8B84A; --trap-wash: rgba(232, 184, 74, 0.13); --code-bg: #232A34; --term-bg: #151A21;
  color-scheme: dark;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
body { margin: 0; background: var(--paper); color: var(--ink); font-family: var(--f-body); font-size: 16px; line-height: 1.6; }
a { color: var(--acc); }
.shell { display: grid; grid-template-columns: 272px minmax(0, 1fr); max-width: 1260px; margin: 0 auto; }
.railoff .shell { grid-template-columns: minmax(0, 1fr); }
.railoff .rail { display: none; }
.railopen { display: none; position: fixed; top: 12px; left: 12px; z-index: 20; height: 36px; padding: 0 14px; border: 1px solid var(--line); border-radius: 6px; background: var(--sheet); color: var(--ink); font: 500 14px var(--f-body); cursor: pointer; }
.railoff .railopen { display: block; }
.rail { position: sticky; top: 0; height: 100vh; overflow-y: auto; padding: 24px 16px 32px; border-right: 1px solid var(--line); }
.rail-top { display: flex; align-items: center; justify-content: space-between; margin: 0 4px 12px; }
.brand { color: var(--ink); text-decoration: none; display: flex; align-items: center; gap: 10px; font-weight: 600; font-size: 18px; }
.brand svg { width: 28px; height: 28px; flex: none; }
.iconbtn { width: 36px; height: 36px; border: 1px solid var(--line); border-radius: 6px; background: var(--sheet); color: var(--muted); font-size: 16px; cursor: pointer; }
.themebtn { width: calc(100% - 8px); margin: 0 4px 12px; height: 36px; border: 1px solid var(--line); border-radius: 6px; background: var(--sheet); color: var(--ink); font: 500 14px var(--f-body); cursor: pointer; }
.iconbtn:hover, .themebtn:hover, .railopen:hover { background: var(--code-bg); }
.mod { margin-top: 8px; }
.modbtn { display: flex; align-items: center; gap: 6px; width: 100%; height: 36px; padding: 0 8px; border: 0; background: none; color: var(--muted); font: 600 12px var(--f-body); letter-spacing: 0.06em; text-transform: uppercase; cursor: pointer; text-align: left; border-radius: 6px; }
.modbtn:hover { background: var(--code-bg); }
.modbtn.static { cursor: default; }
.modbtn.static:hover { background: none; }
.chev { display: inline-block; width: 14px; transition: transform .15s; }
.modbtn[aria-expanded="false"] .chev { transform: rotate(-90deg); }
.modbtn[aria-expanded="false"] + ol { display: none; }
.rail ol { list-style: none; margin: 0; padding: 0; display: grid; gap: 2px; }
.rail a { display: grid; grid-template-columns: 26px minmax(0, 1fr) 16px; align-items: center; min-height: 34px; padding: 4px 8px; border-radius: 6px; color: var(--ink); text-decoration: none; font-size: 14px; line-height: 1.3; }
.rail a .n { color: var(--muted); font-family: var(--f-mono); font-size: 12px; }
.rail a .ok { color: var(--ok); font-size: 13px; }
.rail a.done .ok::after { content: "✓"; }
.rail a:hover { background: var(--code-bg); }
.rail a.active { background: var(--wash); color: var(--acc); font-weight: 600; }
.rail a.qa { color: var(--muted); }
.rail li.sub { font-size: 12px; color: var(--muted); padding: 6px 8px 0 42px; }
.soonlist h4 { font-size: 12px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin: 20px 8px 6px; }
.rail li.soon { display: grid; grid-template-columns: 26px minmax(0, 1fr); padding: 4px 8px; font-size: 14px; color: var(--muted); }
.rail li.soon .n { font-family: var(--f-mono); font-size: 12px; }
main { min-width: 0; padding: 40px 24px 120px 40px; }
.col { max-width: 840px; margin: 0 auto; }
.page { position: relative; background: var(--sheet) url("__WM__") no-repeat right 32px bottom 96px / 260px 260px; border: 1px solid var(--line); border-radius: 8px; padding: 48px 56px 24px; margin-bottom: 32px; }
.paged .page:not(.current) { display: none; }
.folio { position: absolute; top: 18px; right: 24px; font: 12px var(--f-mono); color: var(--muted); }
.runhead { font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); padding-bottom: 12px; margin-bottom: 8px; border-bottom: 1px solid var(--line); }
.pager { display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); align-items: start; gap: 16px; margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--line); font-size: 14px; }
.pager a { color: var(--acc); text-decoration: none; display: grid; gap: 2px; }
.pager a:hover { text-decoration: underline; }
.pager a span { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }
.pager .nextp { text-align: right; }
.pager .pno { font-family: var(--f-mono); font-size: 12px; color: var(--muted); }
.hero { position: relative; padding-right: 120px; }
.hero-logo { position: absolute; right: 0; top: 0; width: 96px; }
.hero h1 { font-size: 40px; line-height: 1.15; font-weight: 600; margin: 0 0 12px; letter-spacing: -0.01em; }
.hero .lede { margin: 0 0 16px; color: var(--muted); font-size: 18px; }
.how { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 24px; }
.how div { background: var(--paper); border: 1px solid var(--line); border-radius: 6px; padding: 12px 16px; font-size: 14px; }
.how b { display: block; font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--acc); margin-bottom: 4px; }
.meta { font-size: 14px; color: var(--muted); margin-top: 16px; }
.btn { display: inline-flex; align-items: center; height: 36px; padding: 0 16px; border: 0; border-radius: 6px; background: var(--acc); color: #fff; font: 600 14px var(--f-body); text-decoration: none; cursor: pointer; }
.btn:hover { filter: brightness(0.92); }
.btn.small { height: 32px; padding: 0 12px; font-size: 14px; margin-top: 8px; }
.btn.ghost { background: none; color: var(--acc); border: 1px solid var(--line); }
h3.sec { margin: 40px 0 12px; font-size: 20px; }
.credit { font-size: 12px; color: var(--muted); margin-top: 32px; }
.roadmap { margin: 0; background: var(--paper); border: 1px solid var(--line); border-radius: 8px; padding: 12px; }
.roadmap svg { display: block; width: 100%; height: auto; }
.roadmap figcaption { font-size: 14px; color: var(--muted); padding: 8px 4px 0; }
.road { stroke: var(--line); stroke-width: 22; stroke-linecap: round; stroke-linejoin: round; }
.road-mid { stroke: var(--muted); stroke-width: 2; stroke-dasharray: 10 10; opacity: 0.5; }
.stop-c { fill: var(--sheet); stroke: var(--ink); stroke-width: 2; }
.stop:hover .stop-c { fill: var(--wash); }
.stop.done .stop-c { fill: var(--ok-wash); stroke: var(--ok); }
.stop.here .stop-c { stroke: var(--acc); stroke-width: 4; }
.stop-n { font: 600 16px var(--f-mono); fill: var(--ink); }
.stop-l { font: 16px var(--f-hand); fill: var(--muted); }
.topic-head { margin-bottom: 24px; }
.chapno { font-size: 40px; line-height: 1.15; font-weight: 600; color: var(--acc); padding-bottom: 12px; margin-bottom: 16px; border-bottom: 2px solid var(--acc2); }
h2 { font-size: 28px; line-height: 1.25; font-weight: 600; margin: 4px 0 8px; }
.goal { color: var(--muted); font-size: 18px; margin: 0; }
.toc, .modlist { margin: 24px 0 0; padding: 0; list-style: none; border-top: 1px solid var(--line); }
.toc li, .modlist li { border-bottom: 1px solid var(--line); }
.toc a, .modlist a { display: grid; grid-template-columns: 72px minmax(0, 1fr); align-items: baseline; padding: 8px 0; color: var(--acc); text-decoration: none; }
.toc a:hover, .modlist a:hover { text-decoration: underline; }
.modlist p { margin: 0 0 10px 72px; color: var(--muted); font-size: 14px; }
.rn { font-family: var(--f-mono); color: var(--muted); font-size: 14px; }
h3 { font-size: 22px; line-height: 1.3; font-weight: 600; margin: 0 0 8px; }
.prose p { margin: 0 0 12px; }
.prose p:last-child { margin-bottom: 0; }
code { font-family: var(--f-mono); font-size: 14px; background: var(--code-bg); padding: 1px 5px; border-radius: 4px; }
.concept, .rule { margin: 40px 0 0; scroll-margin-top: 12px; }
.concept h3:empty { display: none; }
.rule h3 { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 12px; }
.rnum { font-family: var(--f-mono); font-size: 14px; font-weight: 500; color: var(--acc); background: var(--wash); padding: 2px 8px; border-radius: 4px; }
.got { margin-left: auto; font: 500 14px var(--f-body); color: var(--muted); display: inline-flex; align-items: center; gap: 6px; cursor: pointer; }
.got input { width: 16px; height: 16px; accent-color: var(--ok); }
.given { font-size: 14px; color: var(--muted); margin: 8px 0 0; }
.case { background: var(--sheet); border: 1px solid var(--line); border-radius: 6px; margin: 12px 0; overflow: hidden; }
.case-h { font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; padding: 6px 14px; }
.case.good .case-h { background: var(--ok-wash); color: var(--ok); }
.case.bad .case-h { background: var(--bad-wash); color: var(--bad); }
.case.trap .case-h { background: var(--trap-wash); color: var(--trap); }
.case.trap .why { padding: 0 14px 12px; }
.case .term { border: 0; border-radius: 0; margin: 0; }
details.setup { margin: 0 14px 6px; }
details.setup summary { color: var(--muted); font-weight: 500; }
details.setup pre.tout { padding: 4px 0 4px 16px; color: var(--muted); }
.term { background: var(--term-bg); border: 1px solid var(--line); border-radius: 6px; padding: 8px 0; margin: 8px 0 12px; }
.tl { display: flex; align-items: center; gap: 12px; padding: 2px 14px; }
.cmdline { flex: 1; min-width: 0; font: 14px/1.6 var(--f-mono); overflow-x: auto; white-space: pre; }
.cmdline b { font-weight: 600; }
.ps { color: var(--acc); user-select: none; }
.cp { flex: none; height: 26px; padding: 0 8px; border: 1px solid var(--line); border-radius: 4px; background: var(--sheet); color: var(--muted); font: 500 12px var(--f-body); cursor: pointer; }
.cp:hover { color: var(--ink); }
.cp.done { color: var(--ok); }
pre { margin: 0; }
pre.tout { padding: 2px 14px 8px 30px; font: 14px/1.6 var(--f-mono); color: var(--ink); white-space: pre; overflow-x: auto; }
pre.tout.mini { padding: 0; white-space: pre-wrap; font-size: 12px; }
.errline { color: var(--bad); font-weight: 600; }
.hintline { color: var(--muted); }
.addline { color: var(--ok); }
.delline { color: var(--bad); }
.exlabel { margin: 0; font-size: 14px; color: var(--muted); }
.why { margin: 8px 0 0; }
.src { font-size: 14px; color: var(--muted); margin: 8px 0 0; }
.tablewrap { overflow-x: auto; margin: 16px 0; background: var(--sheet); border: 1px solid var(--line); border-radius: 6px; }
table { border-collapse: collapse; width: 100%; font-size: 14px; }
th { text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); font-weight: 600; background: var(--code-bg); }
th, td { padding: 8px 14px; border-bottom: 1px solid var(--line); vertical-align: top; }
tr:last-child td { border-bottom: 0; }
td code { white-space: nowrap; }
.cheat table { table-layout: fixed; min-width: 640px; }
.cheat th:nth-child(1) { width: 40%; } .cheat th:nth-child(2) { width: 24%; } .cheat th:nth-child(3) { width: 36%; }
.cheat td code { white-space: normal; word-break: break-word; }
figure.sketch { margin: 24px 0; background: var(--sheet); border: 1px solid var(--line); border-radius: 6px; }
.sketch-scroll { overflow-x: auto; padding: 12px; }
figure.sketch svg { display: block; width: 100%; height: auto; }
figure.sketch figcaption { font-size: 14px; color: var(--muted); padding: 8px 14px 12px; border-top: 1px dashed var(--line); }
.legend { margin: 0; padding: 8px 14px 4px 40px; font-size: 14px; border-top: 1px dashed var(--line); }
.legend li { margin-bottom: 4px; }
svg .stroke { stroke: var(--ink); stroke-width: 1.8; stroke-linejoin: round; stroke-linecap: round; }
svg .stroke.thin { stroke-width: 0.9; opacity: 0.55; }
svg .arrow { stroke-width: 1.7; }
svg .hand { font-family: var(--f-hand); fill: var(--ink); }
svg .note { fill: var(--muted); }
svg .mono { font-family: var(--f-mono); fill: var(--ink); }
svg .badge { fill: var(--acc); }
svg .badge-t { fill: #fff; font: 600 15px var(--f-body); }
.takeaways { margin-top: 40px; background: var(--wash2); border: 1px solid var(--line); border-radius: 8px; padding: 20px 24px; }
.takeaways ol { margin: 0; padding-left: 22px; }
.takeaways li { margin-bottom: 6px; }
.lab { margin-top: 40px; border: 1px solid var(--line); border-radius: 8px; padding: 24px; background: var(--sheet); }
.lab-h { display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; }
.lab-tag { font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #fff; background: var(--acc); padding: 2px 8px; border-radius: 4px; }
.lsteps { list-style: none; margin: 16px 0 0; padding: 0; counter-reset: ls; }
.lstep { counter-increment: ls; position: relative; border-top: 1px solid var(--line); padding: 10px 0 10px 40px; }
.lstep::before { content: counter(ls); position: absolute; left: 0; top: 12px; width: 26px; height: 26px; border-radius: 50%; background: var(--code-bg); color: var(--muted); font: 600 12px/26px var(--f-mono); text-align: center; }
.lstep.ticked::before { content: "✓"; background: var(--ok-wash); color: var(--ok); }
.lstep .tl { padding: 0; }
.lstep pre.tout { padding: 8px 14px; background: var(--term-bg); border-radius: 6px; margin: 4px 0 0; }
.tick { float: right; margin-left: 12px; font-size: 14px; color: var(--muted); display: inline-flex; gap: 6px; align-items: center; cursor: pointer; }
.tick input { width: 16px; height: 16px; accent-color: var(--ok); }
.silent { font-size: 14px; color: var(--muted); margin: 4px 0 0; font-style: italic; }
.hint { color: var(--muted); font-size: 14px; margin: 12px 0 0; }
details { margin-top: 6px; }
summary { cursor: pointer; font-size: 14px; font-weight: 600; color: var(--acc); width: fit-content; padding: 2px 0; }
summary:focus-visible, a:focus-visible, button:focus-visible, input:focus-visible { outline: 2px solid var(--acc); outline-offset: 2px; border-radius: 4px; }
textarea.mine { display: block; width: 100%; margin-top: 8px; font: 14px/1.5 var(--f-mono); color: var(--ink); background: var(--paper); border: 1px solid var(--line); border-radius: 6px; padding: 8px 12px; resize: vertical; }
textarea.mine:focus { outline: 2px solid var(--acc); outline-offset: 1px; background: var(--sheet); }
.verdict { font-size: 14px; margin: 6px 0 0; white-space: pre-wrap; }
.verdict.yes { color: var(--ok); }
.verdict.no { color: var(--bad); }
.exercises { margin-top: 40px; border: 1px solid var(--line); border-radius: 8px; padding: 24px; }
.exlist { list-style: none; margin: 0; padding: 0; display: grid; gap: 24px; }
.ex { min-width: 0; border-top: 1px solid var(--line); padding-top: 16px; }
.ex:first-child { border-top: 0; padding-top: 0; }
.ex-h { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.ex-n { font: 600 14px var(--f-mono); }
.ex-kind { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); font-weight: 600; }
.ex p { margin: 0 0 8px; }
.brk { margin-top: 40px; border: 1px dashed var(--line); border-radius: 8px; padding: 16px 20px; background: var(--paper); }
.brk-h { font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--acc); margin-bottom: 4px; }
.brk p { margin: 0; }
.quiz { margin-top: 24px; }
.qcard { border: 1px solid var(--line); border-radius: 8px; padding: 24px; }
.qtop { display: flex; justify-content: space-between; font-size: 14px; color: var(--muted); margin-bottom: 12px; }
.qq { font-size: 18px; margin: 0 0 16px; }
.qopts { display: grid; gap: 8px; }
.qopt { text-align: left; min-height: 44px; padding: 8px 14px; border: 1px solid var(--line); border-radius: 6px; background: var(--sheet); color: var(--ink); font: 15px var(--f-body); cursor: pointer; }
.qopt:hover:not(:disabled) { background: var(--code-bg); }
.qopt.right { background: var(--ok-wash); border-color: var(--ok); color: var(--ok); font-weight: 600; }
.qopt.wrong { background: var(--bad-wash); border-color: var(--bad); color: var(--bad); }
.qopt:disabled { cursor: default; }
.qexp { margin: 16px 0 0; font-size: 15px; }
.qexp small { color: var(--muted); }
.qbar { display: flex; gap: 8px; margin-top: 16px; flex-wrap: wrap; }
.qscore { font-size: 28px; font-weight: 600; margin: 0 0 8px; }
.qbest { font-size: 14px; color: var(--muted); }
.revgrid { display: grid; gap: 12px; }
.rev { min-width: 0; border: 1px solid var(--line); border-radius: 6px; padding: 12px 16px; }
.rev-h { display: flex; gap: 10px; align-items: baseline; }
.rev-n { font: 12px var(--f-mono); color: var(--muted); }
.rev p { margin: 4px 0 0; }
.rev .term { margin-bottom: 0; }
@media print {
  .rail, .pager, .railopen, .cp, .got, .tick { display: none !important; }
  .shell { display: block; }
  .page { display: block !important; border: 0; break-before: page; }
}
@media (max-width: 900px) {
  .shell { grid-template-columns: minmax(0, 1fr); }
  .rail { position: static; height: auto; border-right: 0; border-bottom: 1px solid var(--line); padding: 16px; }
  .rail .soonlist { display: none; }
  #railhide { display: none; }
  .railoff .rail { display: block; }
  .railopen { display: none !important; }
  main { padding: 16px 16px 80px; }
  .page { padding: 28px 16px 16px; background-size: 160px 160px; }
  .hero { padding-right: 0; }
  .hero-logo { display: none; }
  .hero h1, .chapno { font-size: 30px; }
  .how { grid-template-columns: minmax(0, 1fr); }
  .pager { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
  .pager .pno { display: none; }
  .lab, .exercises { padding: 16px; }
  .got { margin-left: 0; }
}
'''

JS = r'''
(function () {
  var S = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var root = document.documentElement;
  var pages = Array.prototype.slice.call(document.querySelectorAll('.page'));
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.rail ol a[href^="#"]'));
  root.classList.add('paged');

  function show() {
    var id = decodeURIComponent(location.hash.slice(1));
    var el = id ? document.getElementById(id) : null;
    var pg = el ? el.closest('.page') : null;
    if (!pg) { pg = pages[0]; el = null; }
    pages.forEach(function (p) { p.classList.toggle('current', p === pg); });
    var ch = pg.getAttribute('data-ch');
    navLinks.forEach(function (a) {
      var h = a.getAttribute('href').slice(1);
      var on = h === pg.id || (pg.classList.contains('ch') && a.getAttribute('data-nav-ch') === ch);
      a.classList.toggle('active', on);
    });
    var go = function () { if (el && el !== pg) el.scrollIntoView({ behavior: 'instant' }); else window.scrollTo({ top: 0, behavior: 'instant' }); };
    go(); requestAnimationFrame(go);
    if (pg.id !== 'cover') S.set('gfz-last', pg.id);
    var q = pg.querySelector('.quiz');
    if (q && !q.dataset.ready) startQuiz(q);
    paintRoad();
  }
  window.addEventListener('hashchange', show);

  document.addEventListener('keydown', function (e) {
    if (e.target.closest('textarea, input, select, button') || e.metaKey || e.ctrlKey || e.altKey) return;
    var cur = document.querySelector('.page.current');
    var a = e.key === 'ArrowRight' ? cur.querySelector('.pager .nextp') : e.key === 'ArrowLeft' ? cur.querySelector('.pager .prev') : null;
    if (a) { e.preventDefault(); location.hash = a.getAttribute('href'); }
  });

  // theme
  var tb = document.getElementById('theme');
  function syncTheme() {
    var dark = root.getAttribute('data-theme') === 'dark';
    tb.textContent = dark ? 'Light mode' : 'Dark mode';
    tb.setAttribute('aria-pressed', dark ? 'true' : 'false');
  }
  tb.addEventListener('click', function () {
    var t = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', t); S.set('gfz-theme', t); syncTheme();
  });
  syncTheme();

  // rail
  function setRail(off) { root.classList.toggle('railoff', off); S.set('gfz-railoff', off ? '1' : '0'); }
  document.getElementById('railhide').addEventListener('click', function () { setRail(true); });
  document.getElementById('railopen').addEventListener('click', function () { setRail(false); });
  document.querySelectorAll('.modbtn:not(.static)').forEach(function (b, i) {
    var k = 'gfz-mod-' + i;
    if (S.get(k) === '0') b.setAttribute('aria-expanded', 'false');
    b.addEventListener('click', function () {
      var open = b.getAttribute('aria-expanded') !== 'true';
      b.setAttribute('aria-expanded', open ? 'true' : 'false'); S.set(k, open ? '1' : '0');
    });
  });

  // copy
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.cp');
    if (!b) return;
    var txt = b.getAttribute('data-cmd');
    var done = function () { b.textContent = 'Copied'; b.classList.add('done'); setTimeout(function () { b.textContent = 'Copy'; b.classList.remove('done'); }, 1200); };
    if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, done); else done();
  });

  // progress: rules and lab steps
  function bindTicks(sel, attr, onChange) {
    document.querySelectorAll(sel).forEach(function (cb) {
      var k = 'gfz-' + cb.getAttribute(attr);
      cb.checked = S.get(k) === '1';
      if (onChange) onChange(cb);
      cb.addEventListener('change', function () { S.set(k, cb.checked ? '1' : '0'); if (onChange) onChange(cb); paintProgress(); });
    });
  }
  bindTicks('input[data-rule]', 'data-rule');
  bindTicks('input[data-step]', 'data-step', function (cb) { cb.closest('.lstep').classList.toggle('ticked', cb.checked); });

  function chapterDone(ch) {
    var boxes = document.querySelectorAll('.page[data-ch="' + ch + '"] input[data-rule]');
    if (!boxes.length) { var b = +S.get('gfz-best-' + ch) || 0; return b >= 80; }
    for (var i = 0; i < boxes.length; i++) if (!boxes[i].checked) return false;
    return true;
  }
  function paintProgress() {
    document.querySelectorAll('[data-nav-ch]').forEach(function (a) { a.classList.toggle('done', chapterDone(a.getAttribute('data-nav-ch'))); });
    document.querySelectorAll('.rail a.qa').forEach(function (a) {
      var k = a.getAttribute('href').slice(1).replace(/^q-/, '').replace(/^m-/, 'm');
      a.classList.toggle('done', (+S.get('gfz-best-' + k) || 0) >= 80);
    });
    paintRoad();
  }
  function paintRoad() {
    var last = S.get('gfz-last');
    var lastPg = last && document.getElementById(last);
    var lastCh = lastPg && lastPg.getAttribute('data-ch');
    document.querySelectorAll('.stop[data-ch]').forEach(function (s) {
      var c = s.getAttribute('data-ch');
      s.classList.toggle('done', chapterDone(c));
      s.classList.toggle('here', c === lastCh);
    });
    document.querySelectorAll('.stop[data-mod]').forEach(function (s) {
      s.classList.toggle('done', (+S.get('gfz-best-m' + s.getAttribute('data-mod')) || 0) >= 80);
    });
  }

  // checker: ignore commit IDs, dates, names and paths
  function norm(s) {
    return s.replace(/\r/g, '').split('\n').map(function (l) {
      l = l.replace(/^\$ .*$/, '').replace(/\b[0-9a-f]{7,40}\b/g, '#').replace(/\/Users\/[^\/\s]+/g, '/Users/you').replace(/\/home\/[^\/\s]+/g, '/Users/you');
      if (/^\s*git version/.test(l)) l = 'git version';
      return l.replace(/\s+/g, ' ').trim();
    }).filter(function (l) { return l && !/^(Date:|Author:)/.test(l); });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-check]');
    if (!b) return;
    var box = b.parentElement;
    var ta = box.querySelector('textarea.mine');
    var v = box.querySelector('.verdict');
    var want = norm(b.getAttribute('data-check')), got = norm(ta.value);
    if (!ta.value.trim()) { v.className = 'verdict no'; v.textContent = 'Paste or type something first.'; return; }
    for (var i = 0; i < Math.max(want.length, got.length); i++) {
      if (want[i] !== got[i]) {
        v.className = 'verdict no';
        v.textContent = '✗ Line ' + (i + 1) + ' differs.\nBook: ' + (want[i] || '(nothing more)') + '\nYou:  ' + (got[i] || '(nothing more)');
        return;
      }
    }
    v.className = 'verdict yes'; v.textContent = '✓ Matches the book (IDs, dates and names ignored).';
  });
  document.querySelectorAll('textarea.mine').forEach(function (t, i) {
    var p = t.closest('[id]');
    var k = 'gfz-ta-' + (p ? p.id : '') + '-' + i;
    var v = S.get(k); if (v) t.value = v;
    t.addEventListener('input', function () { S.set(k, t.value); });
  });

  // quizzes
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function startQuiz(box, only) {
    box.dataset.ready = '1';
    var key = box.getAttribute('data-quiz');
    var all = window.QUIZ[key] || [];
    var qs = only || (key.charAt(0) === 'm' ? shuffle(all) : all.slice());
    var i = 0, score = 0, missed = [];
    function render() {
      if (i >= qs.length) return finish();
      var q = qs[i];
      var h = '<div class="qcard"><div class="qtop"><span>Question ' + (i + 1) + ' of ' + qs.length + '</span><span>Score ' + score + '</span></div>'
        + '<p class="qq">' + q.q + '</p><div class="qopts">'
        + q.o.map(function (o, k) { return '<button class="qopt" type="button" data-k="' + k + '">' + o + '</button>'; }).join('')
        + '</div><div class="qafter"></div></div>';
      box.innerHTML = h;
      box.querySelectorAll('.qopt').forEach(function (b) {
        b.addEventListener('click', function () {
          var k = +b.getAttribute('data-k');
          box.querySelectorAll('.qopt').forEach(function (x) { x.disabled = true; });
          box.querySelectorAll('.qopt')[q.a].classList.add('right');
          if (k === q.a) score++; else { b.classList.add('wrong'); missed.push(q); }
          box.querySelector('.qafter').innerHTML = '<p class="qexp" role="status">' + (k === q.a ? '✓ Right. ' : '✗ Not quite. ') + q.e + ' <small>(' + q.f + ')</small></p>'
            + '<div class="qbar"><button class="btn" type="button">' + (i + 1 < qs.length ? 'Next question' : 'See score') + '</button></div>';
          var nb = box.querySelector('.qbar .btn');
          nb.addEventListener('click', function () { i++; render(); });
          nb.focus();
        });
      });
    }
    function finish() {
      var pct = Math.round(100 * score / qs.length);
      if (!only) { var best = +S.get('gfz-best-' + key) || 0; if (pct > best) S.set('gfz-best-' + key, String(pct)); }
      var best2 = S.get('gfz-best-' + key) || pct;
      box.innerHTML = '<div class="qcard"><p class="qscore">' + score + ' / ' + qs.length + ' (' + pct + '%)</p>'
        + '<p class="qbest">' + (pct >= 80 ? 'Passed.' : 'Pass mark is 80%.') + ' Best: ' + best2 + '%</p><div class="qbar">'
        + (missed.length ? '<button class="btn" type="button" data-a="missed">Retry the ' + missed.length + ' you missed</button>' : '')
        + '<button class="btn ghost" type="button" data-a="again">Start again</button></div></div>';
      var m = box.querySelector('[data-a="missed"]');
      if (m) m.addEventListener('click', function () { startQuiz(box, missed); });
      box.querySelector('[data-a="again"]').addEventListener('click', function () { startQuiz(box); });
      paintProgress();
    }
    render();
  }

  function syncContinue() {
    var last = S.get('gfz-last'), c = document.getElementById('continue');
    if (last && document.getElementById(last)) { c.href = '#' + last; c.parentElement.hidden = false; }
  }
  window.addEventListener('hashchange', syncContinue);
  syncContinue();
  paintProgress();
  show();
})();
'''
