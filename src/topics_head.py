CSS = r'''
nav.rail a{grid-template-columns:38px minmax(0,1fr)}
.topic .what{font-size:19px;line-height:1.55;margin:0 0 8px}
.facts{margin:20px 0;border:1px solid var(--line);border-radius:8px;background:var(--surface)}
.fr{display:grid;grid-template-columns:180px minmax(0,1fr);gap:16px;padding:12px 16px;border-bottom:1px solid var(--line)}
.fr:last-child{border-bottom:0}
.fl{font-family:var(--display);font-weight:600;font-size:13px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);padding-top:3px}
.fc ul.plain,.qa ul.plain{margin:0;padding-left:18px}
.fc li,.qa li{font-size:16px;line-height:1.5;margin:2px 0}
@media (max-width:700px){.fr{grid-template-columns:minmax(0,1fr);gap:4px}}
.qa{background:var(--accent-soft);border-radius:8px;padding:12px 16px 14px;margin:20px 0}
.qa h3{margin:0 0 6px;font-size:13px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--accent)}
.chip{font-family:var(--mono);font-size:13px;padding:0 6px;border-radius:4px;margin-right:6px;white-space:nowrap;border:1px solid currentColor}
.chip.ok{color:var(--ok)} .chip.warn{color:var(--warn)} .chip.res{color:var(--lv3)} .chip.claim{color:var(--muted)}
ul.links li{margin-bottom:2px}
.legend{display:flex;flex-wrap:wrap;gap:8px 20px;font-size:16px;margin:8px 0 0}
'''

HEADER = r'''<header class="top">
  <div class="theme" role="group" aria-label="Colour theme"><button type="button" data-t="light" id="th-light">Light</button><button type="button" data-t="dark" id="th-dark">Dark</button><button type="button" data-t="auto" id="th-auto">Auto</button></div>
  <div class="eyebrow">Handbook for QA engineers · Last updated 14 Oct 2026</div>
  <h1>How AI Works</h1>
  <p class="lede">A reference to AI and emerging technology: what each thing is, how it works, where it stands today, what it cannot do yet, and how to test it. Every topic follows the same template, and every fast-moving fact carries a date and a source.</p>
  <div class="levels">
    <a href="#p1"><small style="color:var(--lv1)">Part 1</small><b>AI Foundations</b><span>Learning, LLMs, transformers, evals</span></a>
    <a href="#p2"><small style="color:var(--lv2)">Part 2</small><b>Modern AI Systems</b><span>RAG, agents, vision, speech, MLOps</span></a>
    <a href="#p3"><small style="color:var(--lv3)">Part 3</small><b>Hardware and Robotics</b><span>Chips, data centres, robots, physical AI</span></a>
    <a href="#p4"><small style="color:var(--warn)">Part 4</small><b>Future Intelligence</b><span>AGI, safety, governance, economics, careers</span></a>
  </div>
  <div class="legend"><span><span class="chip ok">production</span>shipping and generally available</span><span><span class="chip res">research</span>a paper or lab result</span><span><span class="chip warn">demo</span>shown, not shipped</span><span><span class="chip claim">claim</span>vendor or press claim, not independently checked</span></div>
</header>
'''
