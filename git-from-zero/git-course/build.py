"""Build Git From Zero (Part 1: modules 0 to 3) into git-course.html.

python3 build.py   runs every command in a sandbox and writes the page.
"""
import base64
import datetime
import json
import pathlib
import re
import urllib.parse

import engine
from engine import esc, run_steps, term, DEFS, RULES, COUNTS, GIT_VER
import chapters
from chapters import PAGE, build_chapters
from bank import MODULES, COMING, QUIZ, CHEAT, REVISION, FACTS, JOKES

HERE = pathlib.Path(__file__).parent
OUT = HERE / "git-course.html"
TODAY = datetime.date.today().strftime("%d %b %Y")
LOGO_SVG = (HERE / "assets/git-icon.svg").read_text().strip()
LOGO = re.sub(r'width="[^"]+" height="[^"]+" ', "", LOGO_SVG)
LOGO_URI = "data:image/svg+xml," + urllib.parse.quote(LOGO_SVG)
WM_URI = "data:image/svg+xml," + urllib.parse.quote(LOGO_SVG.replace('fill="#f03c2e"', 'fill="#f03c2e" fill-opacity="0.05"'))


def brain_break(i):
    if i % 3 == 2:
        j = JOKES[(i // 3) % len(JOKES)]
        return f'<aside class="brk"><div class="brk-h">Brain break · Smile</div><p>{j}</p></aside>'
    f, (t, u) = FACTS[(i - i // 3) % len(FACTS)]
    return f'<aside class="brk"><div class="brk-h">Brain break · Fact</div><p>{f}</p><p class="src">Source: <a href="{u}" target="_blank" rel="noopener">{t}</a></p></aside>'


def cheat_sheet():
    rows = []
    for cmd, what, steps in CHEAT:
        ex = ""
        if steps:
            res, _ = run_steps(steps)
            *_, last = res
            ex = f'<pre class="tout mini">{esc(last[1])}</pre>' if last[1] else '<span class="silent">prints nothing</span>'
        rows.append(f"<tr><td><code>{esc(cmd)}</code></td><td>{what}</td><td>{ex}</td></tr>")
    return ('<div class="tablewrap cheat"><table><thead><tr><th>Command</th><th>Does</th><th>Real output</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def revision_sheet():
    out = []
    for i, (topic, d, steps) in enumerate(REVISION, 1):
        ex = ""
        if steps:
            res, _ = run_steps(steps)
            ex = term(res[-1:], copy=False)
        out.append(f'<div class="rev"><div class="rev-h"><span class="rev-n">{i}</span><b>{topic}</b></div><p>{d}</p>{ex}</div>')
    return '<div class="revgrid">' + "".join(out) + "</div>"


def d_roadmap(chs):
    """A winding road; one stop per chapter, a flag per module test."""
    pts = []
    stops = []
    for k, (mnum, mname, chl) in enumerate(MODULES):
        for c in chl:
            stops.append(("ch", c))
        stops.append(("mod", mnum))
    n = len(stops)
    W, rowh, per = 900, 150, 5
    for i in range(n):
        row, col = divmod(i, per)
        x = 80 + col * 185 if row % 2 == 0 else 80 + (per - 1 - col) * 185
        y = 70 + row * rowh
        pts.append((x, y))
    d = f"M{pts[0][0]},{pts[0][1]}"
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if y1 == y2:
            d += f" L{x2},{y2}"
        else:
            bx = x1 + (70 if x1 > 450 else -70)
            d += f" C{bx},{y1} {bx},{y2} {x2},{y2}"
    s = [f'<path d="{d}" class="road" fill="none"/>', f'<path d="{d}" class="road-mid" fill="none"/>']
    titles = {"0": "What is Git?", "1": "Set up", "2": "First repo", "3": "Everyday loop", "4": "See changes",
              "5": "Undo", "6": ".gitignore", "7": "Branches", "8": "Merging", "9": "Conflicts"}
    slugs = {num: slug for num, slug, title, goal, html in chs}
    for (kind, v), (x, y) in zip(stops, pts):
        if kind == "ch":
            s.append(f'<a href="#t-{slugs[v]}" class="stop" data-ch="{v}"><circle cx="{x}" cy="{y}" r="24" class="stop-c"/>'
                     f'<text x="{x}" y="{y + 6}" class="stop-n" text-anchor="middle">{v}</text>'
                     f'<text x="{x}" y="{y + 50}" class="stop-l" text-anchor="middle">{esc(titles[v][:22])}</text></a>')
        else:
            s.append(f'<a href="#m-{v}" class="stop flag" data-mod="{v}"><rect x="{x - 22}" y="{y - 22}" width="44" height="44" rx="6" class="stop-c"/>'
                     f'<text x="{x}" y="{y + 6}" class="stop-n" text-anchor="middle">M{v}</text>'
                     f'<text x="{x}" y="{y + 50}" class="stop-l" text-anchor="middle">Module {v} test</text></a>')
    h = 70 + ((n - 1) // per) * rowh + 80
    return (f'<figure class="roadmap"><svg viewBox="0 0 {W} {h}" role="img" aria-label="Roadmap of Part 1: chapters 0 to 9 and four module tests">'
            f'{"".join(s)}</svg><figcaption>Click a stop to open it. A stop turns green when you tick every rule in it; a flag turns green when you pass its test (80%+).</figcaption></figure>')


def build():
    chs = build_chapters()
    by_num = {c[0]: c for c in chs}
    quiz_data = {}
    for k, qs in QUIZ.items():
        quiz_data[k] = [{"q": q, "o": o, "a": a, "e": e, "f": f} for q, o, a, e, f in qs]

    pages = []   # (id, label, html, kind)
    bb = [0]

    def chapter_pages(num, slug, title, goal, body):
        sheets = body.split(PAGE)
        rules = RULES.get(num, [])
        toc = ('<ol class="toc">' + "".join(f'<li><a href="#{rid}"><span class="rn">Rule {n}</span><span>{t}</span></a></li>' for rid, n, t in rules) + "</ol>") if rules else ""
        for i, sh in enumerate(sheets):
            pid = f"t-{slug}" if i == 0 else f"t-{slug}-{i + 1}"
            head = (f'<div class="topic-head"><div class="chapno">Chapter {num}</div><h2>{title}</h2><p class="goal">{goal}</p>{toc}</div>' if i == 0
                    else f'<div class="runhead">Chapter {num} · {title}</div>')
            tail = ""
            if i == len(sheets) - 1:
                tail = brain_break(bb[0])
                bb[0] += 1
            pages.append((pid, f"Chapter {num}: {title}" + ("" if i == 0 else f" ({i + 1})"), f'{head}{sh}{tail}', "ch", num))

    for mnum, mname, chl in MODULES:
        intro = (f'<div class="topic-head"><div class="chapno">Module {mnum}</div><h2>{mname}</h2></div>'
                 '<ol class="modlist">' + "".join(f'<li><a href="#t-{by_num[c][1]}"><span class="rn">Ch {c}</span><span>{by_num[c][2]}</span></a>'
                                                   f'<p>{by_num[c][3]}</p></li>' for c in chl) + "</ol>")
        pages.append((f"mod-{mnum}", f"Module {mnum}: {mname}", intro, "mod", None))
        for c in chl:
            chapter_pages(*by_num[c])
            pages.append((f"q-{c}", f"Chapter {c} quiz", f'<div class="runhead">Chapter {c} · Quiz</div><h2>Chapter {c} quiz</h2>'
                          f'<p class="goal">{len(QUIZ[c])} questions, one at a time. Your best score is saved in this browser.</p>'
                          f'<div class="quiz" data-quiz="{c}"></div>', "quiz", c))
        mq = []
        for c in chl:
            mq += quiz_data[c]
        quiz_data["m" + mnum] = mq
        pages.append((f"m-{mnum}", f"Module {mnum} test", f'<div class="runhead">Module {mnum} · Test</div><h2>Module {mnum} test: {mname}</h2>'
                      f'<p class="goal">All {len(mq)} questions from chapters {", ".join(chl)}, shuffled. Pass mark 80%.</p>'
                      f'<div class="quiz" data-quiz="m{mnum}"></div>', "test", mnum))
    pages.append(("cheat", "Part 1 cheat sheet", '<div class="topic-head"><div class="chapno">Cheat sheet</div><h2>Part 1: the commands</h2>'
                  '<p class="goal">Every command from chapters 0 to 9. Outputs are real.</p></div>' + cheat_sheet(), "extra", None))
    pages.append(("rev", "Part 1 revision sheet", '<div class="topic-head"><div class="chapno">Revision</div><h2>Part 1: every topic in one line</h2>'
                  '<p class="goal">A definition and, where it helps, one real example.</p></div>' + revision_sheet(), "extra", None))

    # ---- cover
    n_rules = sum(len(v) for v in RULES.values())
    n_quiz = sum(len(v) for v in QUIZ.values())
    outcomes = [("Set up Git with your name and email", "1"), ("Turn any folder into a repo and save snapshots", "2–3"),
                ("Read exactly what changed, line by line", "4"), ("Undo any mistake, and pick the right undo", "5"),
                ("Keep secrets out of Git", "6"), ("Work on branches and merge them", "7–8"), ("Fix merge conflicts calmly", "9")]
    cover = f'''<header class="hero">
<div class="hero-logo">{LOGO}</div>
<h1>Git From Zero</h1>
<p class="lede">A hands-on book. Every rule shows a command that works, one that breaks with Git's exact message, and why. Then you type it yourself in a lab and check your output against the book.</p>
<div class="how">
<div><b>1 · Read the rule</b>Works, breaks, why. Every output was produced by really running Git.</div>
<div><b>2 · Do the lab</b>Type each step in your terminal. Paste your output, press Check.</div>
<div><b>3 · Take the quiz</b>One question at a time. Module tests at the end of each module.</div>
</div>
<p class="meta">Part 1 · modules 0 to 3 · chapters 0 to 9 · {n_rules} rules · {COUNTS["ex"]} exercises · {n_quiz} quiz questions · {COUNTS["steps"]} commands, all run with {GIT_VER} on {TODAY}.</p>
<p class="cont" hidden><a class="btn" id="continue" href="#cover">Continue where you stopped</a></p>
</header>
<h3 class="sec">Your road through Part 1</h3>
{d_roadmap(chs)}
<h3 class="sec">By the end of Part 1 you can</h3>
{engine.table(["You can", "Chapter"], [[a, b] for a, b in outcomes])}
<h3 class="sec">Coming in Part 2</h3>
{engine.table(["Module", "Topics"], [[f"Module {n}", t] for n, t in COMING])}
<p class="credit">Git logo by <a href="https://git-scm.com/community/logos" target="_blank" rel="noopener">Jason Long</a>, <a href="https://creativecommons.org/licenses/by/3.0/" target="_blank" rel="noopener">CC BY 3.0</a>. Examples use a made-up person, Asha Rao.</p>'''
    pages.insert(0, ("cover", "Cover", cover, "cover", None))

    total = len(pages)

    def pager(i):
        prev = f'<a class="prev" href="#{pages[i - 1][0]}"><span>Previous</span>{pages[i - 1][1]}</a>' if i > 0 else "<span></span>"
        nxt = (f'<a class="nextp" href="#{pages[i + 1][0]}"><span>Next</span>{pages[i + 1][1]}</a>' if i + 1 < total
               else '<a class="nextp" href="#cover"><span>Back to</span>Cover</a>')
        return f'<nav class="pager" aria-label="Pages">{prev}<span class="pno">Page {i + 1} of {total}</span>{nxt}</nav>'

    secs = []
    for i, (pid, label, body, kind, ref) in enumerate(pages):
        data = f' data-ch="{ref}"' if kind in ("ch", "quiz") else (f' data-mod="{ref}"' if kind == "test" else "")
        secs.append(f'<section class="page {kind}" id="{pid}"{data}>{body}<div class="folio">{i + 1}</div>{pager(i)}</section>')

    # ---- rail
    rail = [f'<nav class="rail" aria-label="Book contents"><div class="rail-top"><a class="brand" href="#cover">{LOGO}<span>Git From Zero</span></a>'
            '<button class="iconbtn" id="railhide" type="button" aria-label="Hide menu" title="Hide menu">⟨</button></div>'
            '<button class="themebtn" id="theme" type="button" aria-pressed="false">Dark mode</button>']
    for mnum, mname, chl in MODULES:
        items = "".join(f'<li><a href="#t-{by_num[c][1]}" data-nav-ch="{c}"><span class="n">{c}</span><span>{by_num[c][2]}</span><span class="ok" aria-hidden="true"></span></a></li>' for c in chl)
        quizzes = "".join(f'<li><a href="#q-{c}" class="qa"><span class="n">Q</span><span>Chapter {c} quiz</span><span class="ok"></span></a></li>' for c in chl)
        rail.append(f'<div class="mod"><button class="modbtn" type="button" aria-expanded="true"><span class="chev" aria-hidden="true">▾</span>'
                    f'<span>Module {mnum} · {mname}</span></button><ol>{items}<li class="sub">Quizzes</li>{quizzes}'
                    f'<li><a href="#m-{mnum}" class="qa" data-nav-mod="{mnum}"><span class="n">★</span><span>Module {mnum} test</span><span class="ok"></span></a></li></ol></div>')
    rail.append('<div class="mod"><div class="modbtn static"><span>Part 1 extras</span></div><ol>'
                '<li><a href="#cheat"><span class="n">≡</span><span>Cheat sheet</span></a></li>'
                '<li><a href="#rev"><span class="n">↺</span><span>Revision sheet</span></a></li></ol></div>')
    rail.append('<div class="soonlist"><h4>Part 2, coming next</h4><ol>' + "".join(f'<li class="soon"><span class="n">{n}</span><span>{t.split(":")[0]}</span></li>' for n, t in COMING) + "</ol></div></nav>")

    from styles import CSS, JS
    html = f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Git From Zero</title>
<meta name="description" content="A hands-on Git and GitHub book: every rule shows a command that works, one that breaks with Git's real message, and why.">
<link rel="icon" href="{LOGO_URI}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&amp;family=IBM+Plex+Sans:wght@400;500;600&amp;family=Kalam:wght@400&amp;display=swap">
<script>try{{var t=localStorage.getItem("gfz-theme");if(t)document.documentElement.setAttribute("data-theme",t);if(localStorage.getItem("gfz-railoff")==="1")document.documentElement.classList.add("railoff")}}catch(e){{}}</script>
<style>{CSS.replace("__WM__", WM_URI)}</style>
</head>
<body>
{DEFS}
<button class="railopen" id="railopen" type="button" aria-label="Show menu">☰ Menu</button>
<div class="shell">
{"".join(rail)}
<main><div class="col">{"".join(secs)}</div></main>
</div>
<script>window.QUIZ = {json.dumps(quiz_data)};</script>
<script>{JS}</script>
</body>
</html>
'''
    return html, n_rules, total


if __name__ == "__main__":
    html, n_rules, total = build()
    OUT.write_text(html)
    engine.cleanup()
    print(f"wrote {OUT.name}: pages={total} rules={n_rules} exercises={COUNTS['ex']} commands={COUNTS['steps']} bytes={len(html)}")
