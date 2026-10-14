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
.labels{margin:24px 0 0}
.labels-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;margin-bottom:4px}
.labels-head b{font-family:var(--display);font-size:17px}
.labels-head span{color:var(--muted);font-size:16px}
.labels .tbl{margin:8px 0 0}
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
  <div class="labels">
    <div class="labels-head"><b>How sure is each fact?</b><span>AI changes every month, so fast-moving facts carry one of these labels.</span></div>
    <div class="tbl"><table>
      <tr><th>Label</th><th>What it means</th><th>How far to trust it</th></tr>
      <tr><td><span class="chip ok">production</span></td><td>Released and generally available. You can use it today.</td><td>Reliable. Still note the version and date.</td></tr>
      <tr><td><span class="chip res">research</span></td><td>Published in a paper or lab report.</td><td>True in the test setup; not yet a product.</td></tr>
      <tr><td><span class="chip warn">demo</span></td><td>Shown in a video or keynote, not released.</td><td>Not usable yet. It may change or never ship.</td></tr>
      <tr><td><span class="chip claim">claim</span></td><td>The company's own statement, not checked by anyone else.</td><td>Treat as marketing until someone re-tests it.</td></tr>
      <tr><td><span class="chip claim">reported</span></td><td>Found only in the press or other third-party sources.</td><td>Unconfirmed. Check the official source first.</td></tr>
    </table></div>
  </div>
</header>
'''
