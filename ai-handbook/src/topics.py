import importlib.util, pathlib
R = pathlib.Path(__file__).parent
def _m(n):
    s = importlib.util.spec_from_file_location(n, R / f'{n}.py'); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
_h = _m('topics_head')
CSS = _h.CSS + '\n.b4 .n{color:var(--warn)}\n'
HEADER = _h.HEADER.replace('</div>\n  <div class="labels">', '  <a href="#labs"><small style="color:var(--muted)">Updated often</small><b>Landscape</b><span>Labs, chips, open source, what is new</span></a>\n  </div>\n  <div class="labels">', 1)
PARTS = [
 dict(nav='Part 1 · Foundations', prefix='F', cls='b1', level=('p1','Part 1 of 4','AI Foundations','How models learn, how LLMs work, and how to judge them.'), topics=_m('p1').TOPICS),
 dict(nav='Part 2 · Modern systems', prefix='M', cls='b2', level=('p2','Part 2 of 4','Modern AI Systems','RAG, agents, other AI fields, and running AI in production.'), topics=_m('p2').TOPICS),
 dict(nav='Part 3 · Hardware, robotics', prefix='H', cls='b3', level=('p3','Part 3 of 4','Hardware and Robotics','The chips, data centres and robots AI runs on.'), topics=_m('p3').TOPICS),
 dict(nav='Part 4 · Future', prefix='X', cls='b4', level=('p4','Part 4 of 4','Future Intelligence','AGI, safety, governance, economics, research and careers.'), topics=_m('p4').TOPICS),
 dict(nav='Landscape · Oct 2026', prefix='L', cls='b4', level=('landscape','Updated 14 Oct 2026','Industry Landscape','Who builds what, what is new, and how to judge a claim.'), topics=_m('landscape').TOPICS),
]
FOOTER = '''<footer>
  <p>Every topic lists its own sources under "Further learning". Fast-moving facts (models, chips, robots, regulation) are dated and tagged production, research, demo, claim or reported. Last updated 14 Oct 2026. Diagrams drawn with rough.js in the Excalidraw style.</p>
</footer>
'''
