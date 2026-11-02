"""Git From Zero: runner + page components.

Every command shown in the book is run here, in a throwaway home folder with a fixed
author and a fixed clock, so commit IDs are the same on every build. A step that the
text says works must exit 0; a step that the text says breaks must exit non-zero AND
print the error text the book quotes. Anything else stops the build.
"""
import html
import os
import pathlib
import re
import shutil
import subprocess
import tempfile

esc = html.escape
ROOT = pathlib.Path(tempfile.mkdtemp(prefix="gitbook-")).resolve()
SHOW_HOME = "/Users/you"
GIT_BIN = shutil.which("git")
GIT_DIR = os.path.dirname(GIT_BIN)
GIT_VER = subprocess.run([GIT_BIN, "--version"], capture_output=True, text=True).stdout.strip()
_N = [0]


class Sandbox:
    """A fresh fake home folder. Commands run one after another; `cd` carries over."""

    def __init__(self, config=True, start="git-practice"):
        _N[0] += 1
        self.home = ROOT / f"s{_N[0]}" / "home"
        self.home.mkdir(parents=True)
        self.tick = 0
        self.env = {
            "HOME": str(self.home), "PATH": GIT_DIR + ":/usr/bin:/bin:/usr/sbin:/sbin",
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_PAGER": "cat", "PAGER": "cat", "TERM": "dumb",
            "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8", "TZ": "Asia/Kolkata", "GIT_EDITOR": "true",
        }
        self.cwd = self.home
        if config:
            self.run('git config --global user.name "Asha Rao"')
            self.run("git config --global user.email asha@example.com")
            self.run("git config --global init.defaultBranch main")
        if start:
            (self.home / start).mkdir()
            self.cwd = self.home / start

    def run(self, cmd):
        self.tick += 1
        t = f"2026-10-26T10:{self.tick // 60:02d}:{self.tick % 60:02d}+05:30"
        env = dict(self.env, GIT_AUTHOR_DATE=t, GIT_COMMITTER_DATE=t)
        script = f'cd "{self.cwd}" || exit 99\n{cmd}\n__rc=$?\nprintf "\\n__PWD__%s" "$PWD" >&2\nexit $__rc\n'
        p = subprocess.run(["bash", "-c", script], capture_output=True, text=True, env=env)
        err = p.stderr
        m = re.search(r"\n?__PWD__(.*)$", err)
        if m:
            self.cwd = pathlib.Path(m.group(1))
            err = err[:m.start()]
        out = (p.stdout + err)
        out = out.replace(str(self.home), SHOW_HOME).replace(str(self.home).replace("/private", ""), SHOW_HOME)
        return p.returncode, out.rstrip("\n")


def run_steps(steps, box=None, config=True, start="git-practice"):
    """steps: "cmd" (must work) | ("!", cmd, expect) (must fail with expect) |
    ("h", cmd) (hidden setup) | ("?", cmd) (shown, any exit). Returns list of (cmd, out, rc, kind)."""
    box = box or Sandbox(config=config, start=start)
    res = []
    for s in steps:
        kind, cmd, expect = ("ok", s, None) if isinstance(s, str) else (s[0], s[1], s[2] if len(s) > 2 else None)
        rc, out = box.run(cmd)
        if kind in ("ok", "h") and rc != 0:
            raise SystemExit(f"STEP SHOULD WORK but exit {rc}: {cmd}\n{out}")
        if kind == "!":
            if rc == 0:
                raise SystemExit(f"STEP SHOULD BREAK but worked: {cmd}\n{out}")
            if expect and expect not in out:
                raise SystemExit(f"STEP broke with a different error: {cmd}\nexpected: {expect}\ngot: {out}")
        if kind == "ok" and expect and expect not in out:
            raise SystemExit(f"STEP output missing {expect!r}: {cmd}\n{out}")
        res.append((cmd, out, rc, kind))
    return res, box


def color_line(ln):
    e = esc(ln)
    if re.match(r"^(fatal|error):", ln) or ln.startswith("CONFLICT"):
        return f'<span class="errline">{e}</span>'
    if ln.startswith("hint:") or ln.startswith("warning:"):
        return f'<span class="hintline">{e}</span>'
    if ln.startswith("+") and not ln.startswith("+++"):
        return f'<span class="addline">{e}</span>'
    if ln.startswith("-") and not ln.startswith("---"):
        return f'<span class="delline">{e}</span>'
    return e


def term(res, label=None, copy=True):
    rows = []
    setup = [r for r in res if r[3] == "h"]
    res = [r for r in res if r[3] != "h"]
    if setup:
        cmds = "\n".join("$ " + esc(c) for c, *_ in setup)
        rows.append(f'<details class="setup"><summary>Setup: {len(setup)} commands, run first</summary><pre class="tout">{cmds}</pre></details>')
    for cmd, out, rc, kind in res:
        c = esc(cmd)
        btn = f'<button class="cp" type="button" data-cmd="{c}" aria-label="Copy command">Copy</button>' if copy else ""
        rows.append(f'<div class="tl"><span class="cmdline"><span class="ps">$</span> <b>{c}</b></span>{btn}</div>')
        if out:
            rows.append('<pre class="tout">' + "\n".join(color_line(l) for l in out.split("\n")) + "</pre>")
    lab = f'<p class="exlabel">{label}</p>' if label else ""
    return f'{lab}<div class="term">{"".join(rows)}</div>'


def plain_out(res):
    return "\n".join(o for _, o, _, _ in res if o)


# ---------- blocks ----------
RULES = {}      # chapter -> [(rid, n, title)]
CUR = {"ch": None}
COUNTS = {"rules": 0, "steps": 0, "ex": 0}


def concept(title, body):
    return f'<div class="concept"><h3>{title}</h3><div class="prose">{body}</div></div>'


def table(headers, rows, cls=""):
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tablewrap {cls}"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def demo(steps, label=None, **kw):
    res, _ = run_steps(steps, **kw)
    COUNTS["steps"] += len(res)
    return term(res, label)


def rule(title, body, ok=None, bad=None, why=None, given=None, ok_kw=None, bad_kw=None, trap=None, trap_kw=None):
    ch = CUR["ch"]
    lst = RULES.setdefault(ch, [])
    n = len(lst) + 1
    rid = f"r{ch}-{n}"
    lst.append((rid, n, re.sub("<[^>]+>", "", title)))
    COUNTS["rules"] += 1
    parts = [f'<div class="rule" id="{rid}"><h3><span class="rnum">Rule {n}</span><span>{title}</span>'
             f'<label class="got"><input type="checkbox" data-rule="{rid}"> Got it</label></h3>'
             f'<div class="prose">{body}</div>']
    if given:
        parts.append(f'<p class="given"><b>Start:</b> {given}</p>')
    if ok:
        res, _ = run_steps(ok, **(ok_kw or {}))
        COUNTS["steps"] += len(res)
        parts.append(f'<div class="case good"><div class="case-h"><span class="mark">✓</span> Works</div>{term(res)}</div>')
    if bad:
        res, _ = run_steps(bad, **(bad_kw or {}))
        COUNTS["steps"] += len(res)
        parts.append(f'<div class="case bad"><div class="case-h"><span class="mark">✗</span> Breaks</div>{term(res)}</div>')
    if trap:
        tsteps, ttext = trap
        res, _ = run_steps(tsteps, **(trap_kw or {}))
        COUNTS["steps"] += len(res)
        parts.append(f'<div class="case trap"><div class="case-h"><span class="mark">!</span> Trap: no error, wrong result</div>{term(res)}<p class="why">{ttext}</p></div>')
    if why:
        parts.append(f'<p class="why"><b>Why:</b> {why}</p>')
    parts.append("</div>")
    return "".join(parts)


def lab(title, intro, steps, config=True):
    """Hands-on: the reader types each step in a real terminal. Expected output is real."""
    box = Sandbox(config=config, start=None)
    items = []
    for i, s in enumerate(steps, 1):
        if isinstance(s, tuple) and s[0] == "say":
            items.append(f'<li class="lstep say"><div class="lnote">{s[1]}</div></li>')
            continue
        res, _ = run_steps([s], box=box)
        cmd, out, rc, kind = res[0]
        COUNTS["steps"] += 1
        sid = f"lab-{CUR['ch']}-{i}"
        exp = ('<details><summary>What you should see</summary><pre class="tout">'
               + "\n".join(color_line(l) for l in out.split("\n")) + '</pre></details>') if out else '<p class="silent">Prints nothing. That is normal.</p>'
        check = (f'<details class="chk"><summary>Paste your output to check it</summary>'
                 f'<textarea class="mine" rows="3" spellcheck="false" aria-label="Your output"></textarea>'
                 f'<button class="btn small" type="button" data-check="{esc(out)}">Check</button><p class="verdict" role="status"></p></details>') if out and "Asha" not in out and "asha@" not in out else ""
        items.append(f'<li class="lstep" id="{sid}"><label class="tick"><input type="checkbox" data-step="{sid}"><span>Done</span></label>'
                     f'<div class="tl"><span class="cmdline"><span class="ps">$</span> <b>{esc(cmd)}</b></span>'
                     f'<button class="cp" type="button" data-cmd="{esc(cmd)}" aria-label="Copy command">Copy</button></div>{exp}{check}</li>')
    return (f'<section class="lab"><div class="lab-h"><span class="lab-tag">Hands-on lab</span><h3>{title}</h3></div>'
            f'<div class="prose">{intro}</div><ol class="lsteps">{"".join(items)}</ol>'
            f'<p class="hint">IDs like <code>a1b2c3d</code>, dates and your name will differ from the book. The checker ignores them.</p></section>')


def exercises(items):
    """items: ("predict", text, steps) | ("do", text, answer_html) | ("think", text, answer_html)"""
    lis = []
    for it in items:
        COUNTS["ex"] += 1
        n = COUNTS["ex"]
        kind, text = it[0], it[1]
        if kind == "predict":
            res, _ = run_steps(it[2], **(it[3] if len(it) > 3 else {}))
            *given, last = res
            pre = term(given, copy=False) if given else ""
            out = last[1]
            ans = term([last], copy=False)
            lis.append(f'<li class="ex"><div class="ex-h"><span class="ex-n">{n}</span><span class="ex-kind">Predict</span></div><p>{text}</p>{pre}'
                       f'<div class="term"><div class="tl"><span class="cmdline"><span class="ps">$</span> <b>{esc(last[0])}</b></span></div></div>'
                       f'<textarea class="mine" rows="3" spellcheck="false" aria-label="Your prediction" placeholder="Type what Git prints"></textarea>'
                       f'<button class="btn small" type="button" data-check="{esc(out)}">Check</button><p class="verdict" role="status"></p>'
                       f'<details><summary>Show answer</summary>{ans}</details></li>')
        else:
            label = "Do it" if kind == "do" else "Think"
            lis.append(f'<li class="ex"><div class="ex-h"><span class="ex-n">{n}</span><span class="ex-kind">{label}</span></div><p>{text}</p>'
                       f'<details><summary>Show answer</summary><div class="why">{it[2]}</div></details></li>')
    return (f'<section class="exercises"><h3>Exercises</h3><p class="hint">Predict first, then check. Being wrong first is how it sticks.</p>'
            f'<ol class="exlist">{"".join(lis)}</ol></section>')


def takeaways(points):
    return '<section class="takeaways"><h3>Key takeaways</h3><ol>' + "".join(f"<li>{p}</li>" for p in points) + "</ol></section>"


def source(*links):
    return '<p class="src">Source: ' + " · ".join(f'<a href="{u}" rel="noopener" target="_blank">{t}</a>' for t, u in links) + "</p>"


def cleanup():
    shutil.rmtree(ROOT, ignore_errors=True)


# ---------- sketches (Excalidraw style) ----------
def sbox(x, y, w, h, lines, fill="hn", size=19, mono=False, num=None):
    cls = "mono" if mono else "hand"
    t = []
    n = len(lines)
    for i, ln in enumerate(lines):
        ty = y + h / 2 + (i - (n - 1) / 2) * (size * 1.25) + size * 0.35
        t.append(f'<text x="{x + w / 2}" y="{ty:.1f}" class="{cls}" font-size="{size}" text-anchor="middle">{esc(ln)}</text>')
    badge = ""
    if num is not None:
        badge = (f'<circle cx="{x + 2}" cy="{y + 2}" r="13" class="badge"/>'
                 f'<text x="{x + 2}" y="{y + 7}" class="badge-t" font-size="15" text-anchor="middle">{num}</text>')
    return (f'<g filter="url(#rough)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="url(#{fill})" class="stroke"/>'
            f'<rect x="{x + 1.5}" y="{y - 1}" width="{w - 2}" height="{h + 1}" rx="9" fill="none" class="stroke thin"/></g>'
            + "".join(t) + badge)


def scircle(cx, cy, r, label, fill="hn", size=16):
    return (f'<g filter="url(#rough)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{fill})" class="stroke"/></g>'
            f'<text x="{cx}" y="{cy + size * 0.35}" class="mono" font-size="{size}" text-anchor="middle">{esc(label)}</text>')


def sarrow(x1, y1, x2, y2, label=None, lx=None, ly=None, size=16, curve=0, dash=False):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - curve
    d = ' stroke-dasharray="6 5"' if dash else ""
    s = (f'<path d="M{x1},{y1} Q{mx},{my} {x2},{y2}" class="stroke arrow" fill="none"{d} '
         f'marker-end="url(#ah)" filter="url(#rough)"/>')
    if label:
        lx = mx if lx is None else lx
        ly = (my - 8) if ly is None else ly
        s += f'<text x="{lx}" y="{ly}" class="hand note" font-size="{size}" text-anchor="middle">{esc(label)}</text>'
    return s


def sline(x1, y1, x2, y2):
    return f'<path d="M{x1},{y1} L{x2},{y2}" class="stroke" fill="none" filter="url(#rough)"/>'


def stext(x, y, txt, size=17, cls="hand note", anchor="start"):
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" text-anchor="{anchor}">{esc(txt)}</text>'


def figure(w, h, inner, caption, legend=None, minw=560):
    leg = ""
    if legend:
        leg = '<ol class="legend">' + "".join(f"<li>{x}</li>" for x in legend) + "</ol>"
    return (f'<figure class="sketch"><div class="sketch-scroll"><svg viewBox="0 0 {w} {h}" '
            f'style="min-width:{minw}px" role="img" aria-label="{esc(re.sub("<[^>]+>", "", caption))}">{inner}</svg></div>'
            f'{leg}<figcaption>{caption}</figcaption></figure>')


DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="rough" filterUnits="userSpaceOnUse" x="-50" y="-50" width="1200" height="900"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="2.6"/></filter>
<pattern id="hb" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(-40)"><rect width="9" height="9" style="fill:var(--sheet)"/><line x1="0" y1="0" x2="0" y2="9" stroke="#E0502F" stroke-width="1.3" opacity=".35"/></pattern>
<pattern id="hy" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(-40)"><rect width="9" height="9" style="fill:var(--sheet)"/><line x1="0" y1="0" x2="0" y2="9" stroke="#D99A1E" stroke-width="1.6" opacity=".5"/></pattern>
<pattern id="hg" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(-40)"><rect width="9" height="9" style="fill:var(--sheet)"/><line x1="0" y1="0" x2="0" y2="9" stroke="#2B9A5B" stroke-width="1.3" opacity=".4"/></pattern>
<pattern id="hp" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(-40)"><rect width="9" height="9" style="fill:var(--sheet)"/><line x1="0" y1="0" x2="0" y2="9" stroke="#4A6FD8" stroke-width="1.3" opacity=".4"/></pattern>
<pattern id="hn" width="9" height="9" patternUnits="userSpaceOnUse"><rect width="9" height="9" style="fill:var(--sheet)"/></pattern>
<marker id="ah" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse"><path d="M1,1 L10,6 L1,11" fill="none" style="stroke:var(--ink)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs></svg>'''
