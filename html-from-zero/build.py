"""Builds html-course.html.

Every HTML example on the page is opened in a real browser (Chromium, through
Playwright) and the picture shown is a screenshot of what that browser drew.
Every example is also run through the W3C Nu HTML Checker (tools/vnu). If an
example that should be clean gets an error, or an example that should break
does not get the message the text says, the build stops.

Run:  python3 build.py
"""
import base64
import datetime
import html
import io
import json
import re
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image
from playwright.sync_api import sync_playwright

from bookkit import CSS, DEFS, JS, figure, sarrow, sbox, stext

HERE = pathlib.Path(__file__).parent
OUT = HERE / "html-course.html"
VNU = HERE / "tools/vnu-runtime-image/bin/vnu"
SUNSET = (HERE / "tools/sunset.png").read_bytes()
TODAY = datetime.date.today().strftime("%d %b %Y")
esc = html.escape
WORK = pathlib.Path(tempfile.mkdtemp(prefix="htmlbook-"))

WRAP_TOP = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Lesson</title>\n</head>\n<body>\n'
WRAP_END = '</body>\n</html>\n'
WRAP_LINES = WRAP_TOP.count("\n")

# ---------------------------------------------------------------- jobs
# Each example becomes a job. Placeholders go into the page now; the browser
# and the checker run once over every job at the end, then fill them in.

JOBS = []


def job(code, *, expect=None, warn=False, files=None, page="index.html", raw=None,
        check=True, dom=False, probe=None, clean=True):
    """expect: list of text that must appear in the checker's messages.
    clean: with no expect, the checker must report no errors and no warnings."""
    code = code.strip("\n")
    if raw is None:
        low = code.lower()
        raw = low.startswith("<!doctype") or low.startswith("<html") or "<head" in low
    j = dict(id=len(JOBS), code=code, expect=expect or [], warn=warn, files=files or {},
             page=page, raw=raw, check=check, dom=dom, probe=probe, clean=clean)
    JOBS.append(j)
    return j


def code_html(code):
    return f'<pre class="code"><code class="language-markup">{esc(code)}</code></pre>'


def slot(j, label):
    return f'@@JOB{j["id"]}:{label}@@'


def show(j, label="What the browser shows"):
    return code_html(j["code"]) + slot(j, label)


def works(code, **kw):
    return show(job(code, **kw))


def breaks(code, expect, **kw):
    return show(job(code, expect=expect if isinstance(expect, list) else [expect], **kw))


# ---------------------------------------------------------------- blocks

RULE_INDEX = {}


def rule(num, title, body, ok=None, bad=None, why=None, ok_kw=None, bad_kw=None):
    rid = "r" + num.replace(".", "-")
    title = esc(title, quote=False)
    RULE_INDEX.setdefault(num.split(".")[0], []).append((rid, num, title))
    h = [f'<section class="rule" id="{rid}"><h3><span class="rnum">Rule {num}</span>{title}</h3>',
         f'<div class="prose">{body}</div>']
    for c in ([] if ok is None else ok if isinstance(ok, list) else [ok]):
        h.append(f'<div class="case good"><div class="case-h"><span class="mark">&#10003;</span> Works</div>'
                 f'{works(c, **(ok_kw or {}))}</div>')
    for c, e in ([] if bad is None else bad if isinstance(bad, list) else [bad]):
        h.append(f'<div class="case bad"><div class="case-h"><span class="mark">&#10007;</span> Breaks</div>'
                 f'{breaks(c, e, **(bad_kw or {}))}</div>')
    if why:
        h.append(f'<p class="why"><b>Why:</b> {why}</p>')
    h.append("</section>")
    return "\n".join(h)


def trap(title, code, why, **kw):
    """The checker finds nothing wrong, but the page does something you did not mean."""
    return (f'<div class="case trap"><div class="case-h"><span class="mark">!</span> Trap: {esc(title, quote=False)}</div>'
            f'{works(code, **kw)}<p class="why"><b>Why:</b> {why}</p></div>')


def concept(title, body, cid=None):
    a = f' id="{cid}"' if cid else ""
    return f'<section class="concept"{a}><h3>{title}</h3><div class="prose">{body}</div></section>'


def table(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def example(code, label=None, **kw):
    pre = f'<p class="exlabel">{label}</p>' if label else ""
    return f'<div class="case plain">{pre}{works(code, **kw)}</div>'


def source(*links):
    return '<p class="src">Source: ' + " · ".join(f'<a href="{u}">{t}</a>' for t, u in links) + "</p>"


EX_COUNT = [0]


def exercises(items, tid):
    h = ['<section class="exercises"><h3>Exercises</h3>',
         '<p class="hint">Write your answer in the box first. Then open the answer. '
         'Guessing before you look is what makes it stick.</p><ol class="exlist">']
    for i, it in enumerate(items, 1):
        EX_COUNT[0] += 1
        n = EX_COUNT[0]
        kind = it["kind"]
        q = f'<p>{it["q"]}</p>' if it.get("q") else ""
        code = code_html(it["code"].strip("\n")) if it.get("code") else ""
        if kind == "Predict":
            j = job(it["code"], expect=it.get("expect"), warn=it.get("warn", False),
                    files=it.get("files"), dom=it.get("dom", False), probe=it.get("probe"),
                    clean=it.get("clean", True))
            ans = slot(j, "What the browser really shows")
        elif kind == "Write":
            j = job(it["sol"], files=it.get("files"))
            ans = '<div class="outlabel">One answer</div>' + show(j)
        else:
            ans = ""
        explain = f'<p class="why">{it["a"]}</p>' if it.get("a") else ""
        h.append(f'<li class="ex"><div class="ex-h"><span class="ex-n">{tid}.{i}</span>'
                 f'<span class="ex-kind">{kind}</span></div>{q}{code}'
                 f'<label class="sr" for="ans-{n}">Your answer</label>'
                 f'<textarea id="ans-{n}" class="mine" rows="2" placeholder="Your answer"></textarea>'
                 f'<details><summary>Show answer</summary>{ans}{explain}</details></li>')
    h.append("</ol></section>")
    return "\n".join(h)


# ---------------------------------------------------------------- sketches

def d_request():
    s = sbox(20, 70, 120, 70, ["You"], "hy")
    s += sarrow(142, 105, 212, 105, "type address")
    s += sbox(215, 60, 160, 90, ["Browser", "Chrome, Safari"], "hb", 18)
    s += sarrow(377, 90, 517, 90, "1. asks for the page", 447, 74, 15)
    s += sbox(520, 60, 160, 90, ["Server", "a computer that", "stores the files"], "hn", 16)
    s += sarrow(517, 125, 377, 125, "2. sends page.html", 447, 150, 15)
    s += sarrow(295, 152, 295, 202, "3. draws it", 350, 182, 15)
    s += sbox(205, 205, 180, 60, ["The page you see"], "hg", 17)
    s += stext(700, 95, "On your own computer,", 16)
    s += stext(700, 117, "there is no server:", 16)
    s += stext(700, 139, "the browser opens", 16)
    s += stext(700, 161, "the file directly.", 16)
    return figure(900, 285, s, "Opening a web page: the browser asks a server for an HTML file, then draws it.")


def d_timeline():
    s = '<path d="M40,130 L870,130" class="stroke" fill="none" filter="url(#rough)"/>'
    pts = [(80, "Mar 1989", ["first proposal", "for the Web"]),
           (215, "Dec 1990", ["html, http, URL", "+ first browser"]),
           (350, "Aug 1991", ["announced on", "newsgroups"]),
           (485, "Apr 1993", ["CERN makes the", "code free to use"]),
           (620, "1994", ["W3C founded", "at MIT"]),
           (760, "2019", ["W3C + WHATWG:", "one HTML standard"])]
    for x, yr, lines in pts:
        s += f'<g filter="url(#rough)"><circle cx="{x}" cy="130" r="9" fill="url(#hy)" class="stroke"/></g>'
        s += stext(x, 100, yr, 19, "hand", "middle")
        for i, ln in enumerate(lines):
            s += stext(x, 168 + i * 22, ln, 16, "hand note", "middle")
    return figure(900, 230, s, "HTML's history, from CERN (home.cern) and the HTML standard (html.spec.whatwg.org).", 640)


def d_anatomy():
    s = stext(450, 70, '<a href="about.html">About me</a>', 24, "mono", "middle")
    s += '<g filter="url(#rough)">'
    s += '<path d="M222,85 L222,95 L455,95 L455,85" class="stroke" fill="none"/>'
    s += '<path d="M552,85 L552,95 L604,95 L604,85" class="stroke" fill="none"/>'
    s += '<path d="M465,85 L465,95 L545,95 L545,85" class="stroke" fill="none"/>'
    s += '<path d="M222,40 L222,30 L678,30 L678,40" class="stroke" fill="none"/></g>'
    s += stext(338, 125, "opening tag", 17, "hand", "middle")
    s += stext(505, 150, "content", 17, "hand", "middle")
    s += stext(640, 125, "closing tag", 17, "hand", "middle")
    s += stext(450, 22, "the whole thing is one element", 16, "hand note", "middle")
    s += sarrow(300, 175, 280, 105, "", )
    s += stext(320, 200, "href=\"about.html\" is an attribute:", 16, "hand note", "middle")
    s += stext(320, 222, "extra information, inside the opening tag", 16, "hand note", "middle")
    s += sarrow(640, 165, 600, 100)
    s += stext(700, 195, "same name, with / first", 16, "hand note", "middle")
    return figure(900, 240, s, "The parts of an element: opening tag, content, closing tag. Attributes live in the opening tag.", 640)


def d_tree():
    s = sbox(360, 20, 180, 56, ["<html>"], "hy", 18, True)
    s += sarrow(410, 78, 230, 128)
    s += sarrow(490, 78, 670, 128)
    s += sbox(140, 130, 180, 56, ["<head>"], "hb", 18, True)
    s += sbox(580, 130, 180, 56, ["<body>"], "hg", 18, True)
    s += stext(230, 215, "information ABOUT the page", 16, "hand note", "middle")
    s += stext(230, 237, "title, charset (not shown)", 16, "hand note", "middle")
    s += stext(670, 215, "everything you SEE", 16, "hand note", "middle")
    s += stext(670, 237, "headings, text, links, images", 16, "hand note", "middle")
    s += sarrow(230, 188, 160, 262)
    s += sarrow(230, 188, 300, 262)
    s += sbox(80, 265, 150, 50, ["<meta>"], "hn", 16, True)
    s += sbox(250, 265, 150, 50, ["<title>"], "hn", 16, True)
    s += sarrow(670, 188, 600, 262)
    s += sarrow(670, 188, 740, 262)
    s += sbox(520, 265, 150, 50, ["<h1>"], "hn", 16, True)
    s += sbox(690, 265, 150, 50, ["<p>"], "hn", 16, True)
    return figure(900, 335, s, "Every page is a tree: html holds head and body. Only the body is drawn on screen.", 640)


def d_folders():
    s = sbox(30, 30, 230, 56, ["my-site/"], "hy", 18, True)
    s += '<path d="M60,88 L60,280" class="stroke" fill="none" filter="url(#rough)"/>'
    rows = [(120, "index.html", "hn"), (190, "pages/", "hb"), (260, "images/", "hb")]
    for y, name, fill in rows:
        s += f'<path d="M60,{y} L100,{y}" class="stroke" fill="none" filter="url(#rough)"/>'
        s += sbox(100, y - 25, 190, 50, [name], fill, 17, True)
    s += f'<path d="M300,190 L340,190" class="stroke" fill="none" filter="url(#rough)"/>'
    s += sbox(340, 165, 190, 50, ["about.html"], "hn", 17, True)
    s += f'<path d="M300,260 L340,260" class="stroke" fill="none" filter="url(#rough)"/>'
    s += sbox(340, 235, 190, 50, ["sunset.png"], "hn", 17, True)
    s += stext(570, 110, "From index.html:", 17, "hand")
    s += stext(570, 135, 'href="pages/about.html"', 15, "mono")
    s += stext(570, 180, "From pages/about.html:", 17, "hand")
    s += stext(570, 205, 'href="../index.html"', 15, "mono")
    s += stext(570, 230, ".. means go up one folder", 16, "hand note")
    s += stext(570, 270, 'src="../images/sunset.png"', 15, "mono")
    return figure(900, 305, s, "A path is the route from the file you are in to the file you want.", 700)


# ---------------------------------------------------------------- content

TOPICS = []
MOJI = "Price: ₹499. Café open.".encode("utf-8").decode("cp1252", errors="replace")


def topic(num, slug, title, goal, body):
    TOPICS.append((num, slug, title, goal, body))


SRC_MDN = ("MDN: HTML", "https://developer.mozilla.org/en-US/docs/Web/HTML")
SRC_CERN = ("CERN: A short history of the Web", "https://home.cern/science/computing/the-birth-of-the-web/short-history-web/")
SRC_CERN35 = ("CERN: World Wide Web at 35", "https://home.cern/world-wide-web-35/")
SRC_SPEC = ("HTML Living Standard: introduction", "https://html.spec.whatwg.org/multipage/introduction.html")
SRC_SPEC_TEXT = ("HTML Living Standard: text-level semantics", "https://html.spec.whatwg.org/multipage/text-level-semantics.html")

topic("0", "web", "What is a web page?",
      "Before any code: what a web page is, and the three languages every page is made of.", "".join([
    concept("A web page is a text file", '''
<p><b>A web page is a text file that a browser turns into what you see.</b></p>
<p>The file is plain text with labels in it, saved with a name that ends in <code>.html</code>. The browser (Chrome, Safari, Firefox, Edge) reads the labels and draws headings, paragraphs, links and pictures.</p>'''),
    d_request(),
    concept("Four words you will hear", ""),
    table(["Word", "Plain meaning", "Example"], [
        ["Browser", "the app that shows web pages", "Chrome, Safari, Firefox, Edge"],
        ["Server", "a computer somewhere that stores web pages and sends them when asked", "the computer behind a website"],
        ["URL", "the address of a page", "<code>https://example.com/about.html</code>"],
        ["Website", "a group of pages that link to each other", "a shop's home, products and contact pages"],
    ]),
    concept("Three languages, three jobs", '''
<p>Almost every page uses three languages together. This book is about the first one.</p>'''),
    table(["Language", "Its job", "Like in a house"], [
        ["<b>HTML</b>", "what is on the page, and what each part is: a heading, a paragraph, a link", "the walls and rooms"],
        ["<b>CSS</b>", "how it looks: colours, sizes, where things sit", "the paint and furniture"],
        ["<b>JavaScript</b>", "what it does: reacts when you click or type", "the switches and wiring"],
    ]),
    '<p class="src">The three jobs are from MDN: HTML "defines the meaning and structure of web content", CSS describes "appearance/presentation", JavaScript "functionality/behavior". The house is only a way to remember it.</p>',
    source(SRC_MDN),
    concept("You do not need a server to learn", '''
<p>A <code>.html</code> file on your own computer opens straight in the browser. No server, no internet, nothing to install.</p>
<p>When you do this, the address bar starts with <code>file://</code> instead of <code>https://</code>. The browser below opened this example from a file and was asked what kind of address it had:</p>'''),
    example('<h1>My first page</h1>\n<p>Opened from a file on my computer.</p>', probe="location.protocol"),
    exercises([
        {"kind": "Think", "q": "Which language decides that some text is a heading: HTML, CSS or JavaScript?",
         "a": "HTML. It says what each part of the page is. CSS would decide the heading's colour or size."},
        {"kind": "Think", "q": "Which language would make a button change the page when you click it?",
         "a": "JavaScript. It handles what the page does."},
        {"kind": "Think", "q": "You double-click <code>trip.html</code> on your laptop. Does it need the internet to open?",
         "a": "No. The browser reads the file straight from your computer. The address starts with <code>file://</code>."},
        {"kind": "Think", "q": "In one line each: what is a browser, and what is a server?",
         "a": "A browser is the app that shows web pages. A server is a computer that stores pages and sends them when a browser asks."},
    ], "0"),
]))

topic("1", "what", "What is HTML?",
      "What the letters mean, who made it, when, why, and who looks after it today.", "".join([
    concept("The short answer", '''
<p><b>HTML is the set of labels you put around content to say what each part is.</b></p>
<p>MDN, the main reference for web developers, puts it like this: HTML "is the most basic building block of the Web. It defines the meaning and structure of web content."</p>'''),
    source(SRC_MDN),
    concept("What the letters mean", ""),
    table(["Letter", "Word", "Plain meaning"], [
        ["H T", "HyperText", "text with links that take you to other pages (MDN: \"text containing links that connect web pages to one another\")"],
        ["M", "Markup", "labels you put around content, like <code>&lt;h1&gt;</code> around a heading"],
        ["L", "Language", "a fixed set of those labels, with rules for using them"],
    ]),
    concept("What markup looks like", '''
<p>Below, <code>&lt;h1&gt;</code> and <code>&lt;/h1&gt;</code> are labels around the words <i>My trip to Goa</i>. They tell the browser "this is the main heading". The browser then shows it big and bold. You never see the labels themselves.</p>'''),
    example('<h1>My trip to Goa</h1>\n<p>We went in December.</p>'),
    rule("1.1", "HTML describes, it does not calculate",
         "<p>HTML has no maths, no decisions and no memory. It only labels content. That is why people call it a <b>markup language</b>, not a programming language.</p>",
         ok='<p>2 + 3</p>',
         why="The browser shows exactly the characters you typed. Working out <code>2 + 3</code> is a job for a programming language like JavaScript or Python."),
    concept("Who made it, and why", '''
<p>HTML was made by <b>Tim Berners-Lee</b> at <b>CERN</b>, a physics research lab in Europe, as part of the World Wide Web. CERN says the web "was originally conceived and developed to meet the demand for automated information-sharing between scientists".</p>
<ul>
<li>March 1989: he wrote the first proposal for the World Wide Web.</li>
<li>By Christmas 1990: he had built "html, http and URL" and the first web server, browser and editor (called WorldWideWeb).</li>
<li><code>info.cern.ch</code> was the world's first website, running on a NeXT computer at CERN.</li>
<li>August 1991: he announced the software on internet newsgroups.</li>
<li>30 April 1993: CERN made the source code free to use (royalty-free).</li>
<li>1994: he moved to MIT and founded the W3C (World Wide Web Consortium).</li>
</ul>'''),
    d_timeline(),
    source(SRC_CERN, SRC_CERN35, ("CERN: The birth of the Web", "https://home.cern/science/computing/the-birth-of-the-web/")),
    concept("Who looks after HTML today", '''
<p>HTML is written down as a <b>standard</b>: one long document that says what every label means, so all browsers draw pages the same way.</p>
<ul>
<li>Apple, Mozilla and Opera started a group called the <b>WHATWG</b> to keep developing HTML.</li>
<li>In 2019 the WHATWG and the W3C "signed an agreement to collaborate on a single version of HTML going forward".</li>
<li>That version is called the <b>HTML Living Standard</b>. It keeps being updated instead of getting new version numbers. Older tutorials call it <b>HTML5</b>; today it is just HTML.</li>
</ul>
<p>The standard opens with: "HTML is the World Wide Web's core markup language."</p>'''),
    source(SRC_SPEC),
    concept("Why learn HTML first", '''
<ul>
<li>Every web page is built on it. CSS and JavaScript work on top of the HTML.</li>
<li>All you need is a text editor and a browser, which you already have.</li>
<li>You see the result the moment you refresh the page.</li>
</ul>'''),
    exercises([
        {"kind": "Think", "q": "What do the letters H, T, M and L stand for?",
         "a": "HyperText Markup Language. HyperText: text with links. Markup: labels around content. Language: a fixed set of those labels."},
        {"kind": "Predict", "code": "<p>10 * 2</p>", "q": "What does the browser show?",
         "a": "<code>10 * 2</code>, exactly as typed. HTML does not do maths."},
        {"kind": "Think", "q": "Who made HTML, and where?",
         "a": "Tim Berners-Lee, at CERN."},
        {"kind": "Think", "q": "A 2012 tutorial says \"learn HTML5\". Is that a different language from what this book teaches?",
         "a": "No. HTML5 was the name of the standard back then. Today the same language is just called HTML, kept up to date as the HTML Living Standard."},
    ], "1"),
]))

topic("2", "first", "Your first page, and how mistakes behave",
      "Make a page, open it, and learn the one thing that makes HTML different from Python: the browser never shows an error.", "".join([
    concept("Make your first page", '''
<ol>
<li>Make a folder called <code>html-practice</code>.</li>
<li>Open a code editor. <b>VS Code</b> is free and is what most people use.</li>
<li>Make a new file and save it in that folder as <code>hello.html</code>.</li>
<li>Type the two lines below and save.</li>
<li>Double-click <code>hello.html</code>. It opens in your browser.</li>
<li>Change a word, save, then refresh the browser (<code>Cmd + R</code> on Mac, <code>Ctrl + R</code> on Windows) to see the change.</li>
</ol>'''),
    example('<h1>Hello</h1>\n<p>This is my first web page.</p>', "hello.html"),
    '<p class="note">Most examples in this book show only the lines you type inside the page. The full page skeleton around them comes in Chapter 4. The checker and the browser always got the full page.</p>',
    rule("2.1", "The file name must end in .html",
         "<p>The ending of the name tells the browser what kind of file it is. Only <code>.html</code> (or <code>.htm</code>) makes it read the labels.</p>",
         ok='<h1>Hello</h1>\n<p>This is my first web page.</p>'),
    '<div class="case bad"><div class="case-h"><span class="mark">&#10007;</span> Breaks: the same text saved as hello.txt</div>'
    + show(job('<h1>Hello</h1>\n<p>This is my first web page.</p>', page="hello.txt", check=False, raw=True)) + '</div>',
    '<p class="why"><b>Why:</b> A <code>.txt</code> file is treated as plain text, so the browser shows every character, labels included. No error is shown either way.</p>',
    rule("2.2", "The browser fixes mistakes without telling you",
         "<p>Python stops and prints an error. A browser does the opposite: it guesses what you meant, repairs the page, and shows something. So a page can look almost right and still be wrong.</p>"
         "<p>Below, the <code>&lt;b&gt;</code> (bold) label is never closed. The browser does not complain. It quietly carries the bold on into the next paragraph.</p>",
         ok='<p><b>Hello</b></p>\n<p>World</p>',
         bad=('<p><b>Hello</p>\n<p>World</p>', ["Unclosed element “b”"]),
         bad_kw={"dom": True},
         why="The browser had to decide where the bold ends. It chose to keep it going, and wrapped the second paragraph in a new <code>&lt;b&gt;</code> that you never wrote. You can see that in <i>what the browser built</i>, which is not what you wrote."),
    concept("How to find mistakes: the W3C checker", '''
<p>Because the browser stays silent, you check your page with a <b>checker</b> (also called a validator). It reads your HTML and lists every mistake, like Python's error message does.</p>
<ol>
<li>Open <code>validator.w3.org/nu</code>.</li>
<li>Choose <b>file upload</b> and pick your <code>.html</code> file, or choose <b>text input</b> and paste your code.</li>
<li>Click <b>Check</b>. A clean page says there are no errors or warnings.</li>
</ol>
<p>Every <i>Checker says</i> box in this book came from that same checker (the Nu HTML Checker), run on the example.</p>'''),
    concept("How to read a checker message", ''),
    table(["Part", "Example", "What it tells you"], [
        ["Type", "<b>Error</b> or <b>Warning</b>", "An error breaks the rules. A warning is advice you should usually follow."],
        ["Message", "Unclosed element “b”.", "what is wrong, naming the label"],
        ["Place", "line 1", "the line in your file (this book counts lines in the example you see)"],
    ]),
    concept("See what the browser built", '''
<p>Right-click anywhere on your page and choose <b>Inspect</b>. The panel that opens shows the page as the browser built it, after its repairs. Compare that with your file to spot where it guessed.</p>
<p><b>View Page Source</b> (also in the right-click menu) shows your file exactly as you wrote it.</p>'''),
    rule("2.3", "Spaces at the start of a line are only for you",
         "<p>In Python, spaces at the start of a line change the meaning. In HTML they do not. People indent HTML only so it is easier to read.</p>",
         ok=['<p>Line up\nthe code\nany way you like.</p>', '<p>Line up\n        the code\n    any way you like.</p>'],
         why="Both pictures are the same. The browser ignores where the lines start. Chapter 5 shows what it does with spaces and new lines in the middle of text."),
    exercises([
        {"kind": "Think", "q": "You save your page as <code>notes.html.txt</code> by mistake. What will the browser show?",
         "a": "Your labels as plain text, because the name ends in <code>.txt</code>. The last ending is the one that counts."},
        {"kind": "Predict", "code": "<p><i>Hi</p>\n<p>there</p>", "q": "Is <i>there</i> shown in italics?",
         "expect": ["Unclosed element “i”"], "dom": True,
         "a": "Yes. Like the bold example, the unclosed <code>&lt;i&gt;</code> carries on into the next paragraph."},
        {"kind": "Think", "q": "Your page looks fine in the browser. Does that prove the HTML is correct?",
         "a": "No. The browser repairs mistakes silently. Run it through the W3C checker to know."},
        {"kind": "Think", "q": "Which shows the page after the browser's repairs: View Page Source or Inspect?",
         "a": "Inspect. View Page Source shows your file as written."},
    ], "2"),
]))

topic("3", "tags", "Tags, elements and attributes",
      "The grammar of HTML: how labels open and close, how they sit inside each other, and how to add extra information to them.", "".join([
    concept("Three words, one picture", '''
<ul>
<li>A <b>tag</b> is a label name in angle brackets: <code>&lt;p&gt;</code>.</li>
<li>An <b>element</b> is the opening tag, the content and the closing tag together: <code>&lt;p&gt;Hi&lt;/p&gt;</code>.</li>
<li>An <b>attribute</b> is extra information written inside the opening tag: <code>href="about.html"</code>.</li>
</ul>'''),
    d_anatomy(),
    rule("3.1", "A closing tag has a / before the name",
         "<p>The closing tag repeats the name, with <code>/</code> first. It marks where the element ends.</p>",
         ok='<p>This is <b>important</b> news.</p>',
         bad=('<p>This is <b>important<b> news.</p>', ["Unclosed element “b”"]),
         bad_kw={"dom": True},
         why="Without the <code>/</code>, the second <code>&lt;b&gt;</code> opens another bold instead of closing the first. Bold never ends, so <i>news.</i> is bold too."),
    rule("3.2", "Tag names must be real HTML tags",
         "<p>HTML has a fixed list of tags. A name you invent is not an error the browser shows, but it means nothing to it.</p>",
         ok='<p>This is a paragraph.</p>',
         bad=('<paragraph>This is a paragraph.</paragraph>', ["Element “paragraph” not allowed"]),
         why="It looks almost the same, which is the trap. The browser does not know <code>&lt;paragraph&gt;</code>, so it gives it none of a paragraph's meaning, and the checker calls it \"a completely-unknown element\". The real name is <code>&lt;p&gt;</code>."),
    rule("3.3", "Tag names are not case-sensitive, but write them in lowercase",
         "<p><code>&lt;P&gt;</code> and <code>&lt;p&gt;</code> are the same tag. Lowercase is the normal habit, and every example in this book uses it.</p>",
         ok=['<p>lowercase tags</p>', '<P>UPPERCASE TAGS</P>'],
         why="Both are correct and draw the same paragraph. Lowercase is the habit to build, because that is what you will read everywhere."),
    rule("3.4", "Close tags in the reverse order you opened them",
         "<p>Elements sit inside each other like boxes inside boxes. The last one opened must be the first one closed.</p>",
         ok='<p><b><i>Bold and italic</i></b> then normal.</p>',
         bad=('<p><b><i>Bold and italic</b></i> then normal.</p>', ["End tag “b” violates nesting rules"]),
         why="<code>&lt;i&gt;</code> was opened last, so it must close first: <code>&lt;/i&gt;&lt;/b&gt;</code>. Crossing them is like closing the outer box while the inner one is still open."),
    rule("3.5", "Some elements have no closing tag",
         "<p>A few elements hold no content, so they have nothing to close. They are called <b>void elements</b>. The ones you will use most are <code>&lt;br&gt;</code> (line break), <code>&lt;img&gt;</code> (image), <code>&lt;hr&gt;</code> (line across) and <code>&lt;meta&gt;</code>.</p>",
         ok='<p>Line one<br>Line two</p>',
         bad=('<p>Line one</br>Line two</p>', ["End tag “br”"]),
         why="<code>&lt;/br&gt;</code> does not exist. The browser happens to treat it as a <code>&lt;br&gt;</code>, so the page looks fine, but the checker still calls it an error."),
    trap("writing <br/> with a slash",
         '<p>Line one<br/>Line two</p>',
         "You will see <code>&lt;br/&gt;</code> and <code>&lt;img ... /&gt;</code> in older code. The checker accepts it and the browser ignores the slash. Plain <code>&lt;br&gt;</code> is the same thing, shorter."),
    rule("3.6", "Attributes go in the opening tag, as name=\"value\"",
         "<p>An attribute adds information to an element. It always goes inside the <b>opening</b> tag, after the tag name and a space.</p>",
         ok='<a href="index.html">Home</a>',
         bad=('<a>Home</a href="index.html">', ["End tag had attributes"]),
         why="Attributes are never allowed on a closing tag. The browser drops it, so this link goes nowhere."),
    rule("3.7", "Put attribute values in quotes",
         "<p>A value with a space in it needs quotes, or the browser stops reading the value at the space. Quote every value and you never have to think about it.</p>",
         ok='<img src="sunset.png" alt="My sunset">',
         bad=('<img src="sunset.png" alt=My sunset>', ["Attribute “sunset” not allowed"]),
         ok_kw={"files": {"sunset.png": SUNSET}, "probe": "document.querySelector('img').alt"},
         bad_kw={"files": {"sunset.png": SUNSET}, "probe": "document.querySelector('img').alt"},
         why="Without quotes, the value ends at the space. <code>alt</code> became just <code>My</code>, and <code>sunset</code> turned into a second attribute that means nothing."),
    rule("3.8", "Do not repeat an attribute on one element",
         "<p>Each attribute can appear once per element.</p>",
         ok='<a href="about.html">About</a>',
         bad=('<a href="about.html" href="contact.html">About</a>', ["Duplicate attribute “href”"]),
         bad_kw={"probe": "document.querySelector('a').getAttribute('href')"},
         why="The browser keeps the first one and throws the second away, so this link goes to <code>about.html</code>."),
    rule("3.9", "Every opening quote needs a closing quote",
         "<p>A missing closing quote makes the browser keep reading everything after it as part of the value.</p>",
         ok='<p><a href="about.html">About</a></p>\n<p>Some more text.</p>',
         bad=('<p><a href="about.html>About</a></p>\n<p>Some more text.</p>', ["End of file reached when inside an attribute value"]),
         bad_kw={"dom": True},
         why="The browser kept reading the <code>href</code> value, looking for the closing quote. There was none, so it read to the end of the file and threw the whole tag away. The link and everything after it vanished."),
    exercises([
        {"kind": "Predict", "code": "<p>I <b>love</b> HTML.</p>", "q": "Which word is bold?",
         "a": "Only <i>love</i>. The bold starts at <code>&lt;b&gt;</code> and stops at <code>&lt;/b&gt;</code>."},
        {"kind": "Predict", "code": "<p><i>One <b>two</i> three</b></p>", "q": "Will the checker accept this?",
         "expect": ["violates nesting rules"],
         "a": "No. <code>&lt;b&gt;</code> was opened last, so it must close first."},
        {"kind": "Write", "q": "Write a paragraph that says <i>Call me</i>, with a line break, then <i>on Sunday</i>.",
         "sol": "<p>Call me<br>on Sunday</p>"},
        {"kind": "Predict", "code": '<a href="home.html" title=Go home>Home</a>', "q": "What is the value of the title attribute?",
         "expect": ["Attribute “home” not allowed"], "probe": "document.querySelector('a').title",
         "a": "Just <code>Go</code>. Without quotes the value stops at the space."},
        {"kind": "Think", "q": "Name the three parts of <code>&lt;h1&gt;Menu&lt;/h1&gt;</code>.",
         "a": "Opening tag <code>&lt;h1&gt;</code>, content <i>Menu</i>, closing tag <code>&lt;/h1&gt;</code>. All three together are one element."},
    ], "3"),
]))

FULL = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>My first page</title>
</head>
<body>
  <h1>Hello</h1>
  <p>This page is complete.</p>
</body>
</html>'''

topic("4", "skeleton", "The page skeleton",
      "The lines every HTML file starts with, what each one does, and what goes wrong without it.", "".join([
    concept("The full page", '''
<p>Every HTML file has the same frame around its content. Type it once, then copy it for every new page.</p>'''),
    example(FULL, "page.html"),
    table(["Line", "What it does"], [
        ["<code>&lt;!DOCTYPE html&gt;</code>", "tells the browser this is a modern HTML page"],
        ["<code>&lt;html lang=\"en\"&gt;</code>", "holds the whole page; <code>lang</code> says the language of the text"],
        ["<code>&lt;head&gt;</code>", "information <b>about</b> the page, not shown on it"],
        ["<code>&lt;meta charset=\"utf-8\"&gt;</code>", "says how the letters are stored, so ₹, é and emoji show correctly"],
        ["<code>&lt;title&gt;</code>", "the name in the browser tab"],
        ["<code>&lt;body&gt;</code>", "everything you see on the page"],
    ]),
    d_tree(),
    rule("4.1", "Start every page with <!DOCTYPE html>",
         "<p>The first line switches the browser into its normal mode. MDN: \"The only purpose of <code>&lt;!doctype html&gt;</code> is to activate no-quirks mode.\" Without it the browser uses <b>quirks mode</b>, where \"layout emulates behavior in Navigator 4 and Internet Explorer 5\", browsers from the 1990s.</p>",
         ok=FULL,
         bad=(FULL.replace("<!DOCTYPE html>\n", ""), ["Start tag seen without seeing a doctype first"]),
         ok_kw={"probe": "document.compatMode"}, bad_kw={"probe": "document.compatMode"},
         why="The browser reports which mode it chose. <code>CSS1Compat</code> is the normal mode. <code>BackCompat</code> is quirks mode. The page may look the same now, but the CSS you add later is laid out the old way."),
    source(("MDN: Quirks mode and standards mode", "https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Quirks_mode_and_standards_mode")),
    rule("4.2", "Every page needs a <title>",
         "<p>The title is the name in the browser tab, in bookmarks and in search results. The checker treats it as required.</p>",
         ok=FULL,
         bad=(FULL.replace("  <title>My first page</title>\n", ""), ["missing a required instance of child element “title”"]),
         ok_kw={"probe": "document.title"}, bad_kw={"probe": "document.title"},
         why="The browser was asked for the page's title. Without the element the answer is empty: the page has no name of its own."),
    rule("4.3", "Visible content goes in <body>, not <head>",
         "<p>The head is only for information about the page. Anything you want people to see goes in the body.</p>",
         ok=FULL,
         bad=(FULL.replace("  <title>My first page</title>\n", "  <title>My first page</title>\n  <h1>Welcome</h1>\n"), ["Stray end tag “head”"]),
         bad_kw={"dom": True},
         why="When the browser met <code>&lt;h1&gt;</code> inside the head, it closed the head early and started the body right there. <i>Welcome</i> still shows, but your own <code>&lt;/head&gt;</code> and <code>&lt;body&gt;</code> now come too late, and the checker calls them stray."),
    rule("4.4", "Declare the character set: <meta charset=\"utf-8\">",
         "<p>Your file is stored as numbers. <code>utf-8</code> tells the browser which numbers mean which letters, so it never has to guess. Put it first inside the head.</p>",
         ok=FULL.replace("This page is complete.", "Price: ₹499. Café open."),
         ok_kw={"probe": "document.characterSet"}),
    trap("leaving it out can still look fine",
         FULL.replace("  <meta charset=\"utf-8\">\n", "").replace("This page is complete.", "Price: ₹499. Café open."),
         "In this test Chromium guessed UTF-8 correctly and the checker said nothing. That is luck, not a rule: the browser had to guess. "
         "If something guesses an older encoding instead (windows-1252), the same text comes out as <code>" + esc(MOJI) + "</code>. "
         "That junk was produced by decoding this exact text the wrong way. The one line removes the guess.",
         probe="document.characterSet"),
    rule("4.5", "Say the page's language with lang",
         "<p><code>lang=\"en\"</code> on the <code>&lt;html&gt;</code> tag says which language the text is in. MDN: it is there \"primarily to allow assistive technologies such as screen readers to invoke the correct pronunciation.\" Use <code>hi</code> for Hindi, <code>kn</code> for Kannada.</p>",
         ok=FULL,
         bad=(FULL.replace('<html lang="en">', "<html>"), ["Consider adding a “lang” attribute"]),
         bad_kw={"warn": True},
         why="This one is a <b>warning</b>, not an error. The page works, but without <code>lang</code> the language is unknown, so a screen reader cannot pick the right pronunciation."),
    source(("MDN: the lang attribute", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/lang")),
    exercises([
        {"kind": "Think", "q": "Which part of the page is drawn on screen: head or body?",
         "a": "Only the body. The head holds information about the page."},
        {"kind": "Predict", "code": '<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n  <title>Recipes</title>\n</head>\n<body>\n  <p>Chai</p>\n</body>\n</html>',
         "q": "What does the browser tab say?", "probe": "document.title",
         "a": "<i>Recipes</i>. The title shows in the tab, not on the page."},
        {"kind": "Write", "q": "Write a complete page in Hindi (<code>lang=\"hi\"</code>), titled <i>नमस्ते</i>, with a heading that says <i>नमस्ते</i>.",
         "sol": '<!DOCTYPE html>\n<html lang="hi">\n<head>\n  <meta charset="utf-8">\n  <title>नमस्ते</title>\n</head>\n<body>\n  <h1>नमस्ते</h1>\n</body>\n</html>'},
        {"kind": "Think", "q": "You forgot <code>&lt;!DOCTYPE html&gt;</code>. The page looks fine. Why fix it anyway?",
         "a": "Without it the browser runs in quirks mode, which lays the page out like 1990s browsers did, and the checker reports it as an error."},
    ], "4"),
]))

topic("5", "text", "Headings and text",
      "Headings, paragraphs, line breaks, bold and italic, and what the browser does with your spaces.", "".join([
    rule("5.1", "There are six heading levels, h1 to h6",
         "<p><code>&lt;h1&gt;</code> is the main heading of the page. <code>&lt;h2&gt;</code> is a section heading under it, <code>&lt;h3&gt;</code> a part of that section, and so on down to <code>&lt;h6&gt;</code>.</p>",
         ok='<h1>Heading 1</h1>\n<h2>Heading 2</h2>\n<h3>Heading 3</h3>\n<h4>Heading 4</h4>\n<h5>Heading 5</h5>\n<h6>Heading 6</h6>',
         bad=('<h7>Heading 7</h7>', ["Element “h7” not allowed"]),
         why="There is no <code>&lt;h7&gt;</code>. The browser shows its text as plain words, with no heading style at all."),
    rule("5.2", "Pick the heading level by meaning, not by size",
         "<p>The number is the level in an outline, like chapter, section, sub-section. Screen readers let people jump between headings by level. If you only want smaller text, that is a job for CSS.</p>",
         ok='<h1>Goa trip</h1>\n<h2>Day 1</h2>\n<h3>Morning</h3>\n<h2>Day 2</h2>',
         bad=('<h2>Day 1</h2>\n<h3>Morning</h3>', ["none of them has a computed heading level of 1"]),
         bad_kw={"warn": True},
         why="The checker warns when a page has headings but no <code>&lt;h1&gt;</code>. Every page should start its outline with one main heading."),
    rule("5.3", "Text goes in paragraphs: <p>",
         "<p>Each <code>&lt;p&gt;</code> is one paragraph. The browser puts a gap above and below it.</p>",
         ok='<p>First paragraph.</p>\n<p>Second paragraph.</p>'),
    trap("pressing Enter does not make a new line",
         '<p>Roses are red.\nViolets are blue.\n\n\nHTML     ignores     extra spaces.</p>',
         "The browser turns any run of spaces, tabs and new lines into <b>one space</b>. Your blank lines and extra spaces disappear. To start a new line use <code>&lt;br&gt;</code>; to start a new paragraph use a new <code>&lt;p&gt;</code>."),
    rule("5.4", "<br> breaks a line inside a paragraph",
         "<p>Use it where the line break is part of the content, like an address or a poem.</p>",
         ok='<p>Roses are red.<br>\nViolets are blue.</p>'),
    rule("5.5", "<pre> keeps your spaces and new lines exactly",
         "<p>Inside <code>&lt;pre&gt;</code> (preformatted), the browser keeps every space and line break, and uses a fixed-width font.</p>",
         ok='<pre>Name    Age\nRavi    25\nMeena   31</pre>'),
    rule("5.6", "A heading cannot go inside a paragraph",
         "<p>A paragraph can hold text and small things like links and bold. It cannot hold a heading, another paragraph or other big blocks.</p>",
         ok='<h1>Menu</h1>\n<p>Today we have chai.</p>',
         bad=('<p><h2>Menu</h2> Today we have chai.</p>', ["No “p” element in scope but a “p” end tag seen"]),
         bad_kw={"dom": True},
         why="When the browser met <code>&lt;h2&gt;</code> it closed the paragraph first. Look at what it built: an empty paragraph, the heading, then loose text and an extra empty paragraph from your <code>&lt;/p&gt;</code>."),
    rule("5.7", "<strong> means important, <em> means stressed",
         "<p><code>&lt;strong&gt;</code> and <code>&lt;b&gt;</code> both look bold; <code>&lt;em&gt;</code> and <code>&lt;i&gt;</code> both look italic. The difference is meaning. The standard says <code>strong</code> \"represents strong importance, seriousness, or urgency\" and <code>em</code> \"represents stress emphasis\". Screen readers can use that meaning.</p>",
         ok='<p><strong>Warning:</strong> the floor is wet.</p>\n<p>I said <em>tomorrow</em>, not today.</p>'),
    source(SRC_SPEC_TEXT),
    rule("5.8", "Comments are notes the browser does not show",
         "<p>Write <code>&lt;!--</code> to start a comment and <code>--&gt;</code> to end it. Everything between is hidden from the page.</p>",
         ok='<!-- TODO: add a photo here -->\n<p>Welcome to my page.</p>',
         bad=('<!-- TODO: add a photo here\n<p>Welcome to my page.</p>', ["End of file inside comment"]),
         why="Without <code>--&gt;</code> the comment never ends, so it hides the rest of the page. The browser shows a blank page and no error."),
    exercises([
        {"kind": "Predict", "code": "<p>One\nTwo\nThree</p>", "q": "How many lines does the browser show?",
         "a": "One: <i>One Two Three</i>. New lines in the file become single spaces."},
        {"kind": "Write", "q": "Write this address so each part is on its own line, inside one paragraph: <i>12 MG Road</i> / <i>Bengaluru</i> / <i>560001</i>.",
         "sol": "<p>12 MG Road<br>\nBengaluru<br>\n560001</p>"},
        {"kind": "Predict", "code": "<p>Top</p>\n<!-- <p>Middle</p> -->\n<p>Bottom</p>", "q": "Which words show?",
         "a": "<i>Top</i> and <i>Bottom</i>. The middle paragraph is inside a comment."},
        {"kind": "Think", "q": "You want a smaller heading under your h1 because h2 \"looks too big\". Should you use h4 instead?",
         "a": "No. Use the level that matches the outline (h2 for a section). Change the size with CSS later."},
        {"kind": "Predict", "code": "<h3>Notes</h3>\n<h8>Small notes</h8>", "q": "Will the checker accept this?",
         "expect": ["Element “h8” not allowed"],
         "a": "No. Headings stop at h6. <code>&lt;h8&gt;</code> is not a tag, so its text shows as plain words."},
    ], "5"),
]))

topic("6", "links", "Links and paths",
      "Make text clickable, link to other sites and to your own files, and get the path right.", "".join([
    rule("6.1", "A link is <a> with an href",
         "<p><code>&lt;a&gt;</code> (anchor) makes a link. <code>href</code> is where it goes. The text between the tags is what people click.</p>",
         ok='<p>Read <a href="https://example.com">the example site</a>.</p>',
         why="The browser underlines link text and colours it blue by default."),
    trap("<a> without href is not a link",
         '<p>Read <a>the example site</a>.</p>',
         "Without <code>href</code> there is nowhere to go, so the browser draws plain text. The checker allows it, because <code>&lt;a&gt;</code> without <code>href</code> is valid; it is just not a link."),
    rule("6.2", "A link to another website needs the full address",
         "<p>Start with <code>https://</code>. Without it the browser thinks you mean a file in your own folder.</p>",
         ok='<a href="https://www.google.com">Google</a>',
         ok_kw={"probe": "document.querySelector('a').href"}),
    trap("leaving out https://",
         '<a href="www.google.com">Google</a>',
         "The checker is happy, but the browser read <code>www.google.com</code> as a <b>file name</b> in your folder. Clicking it opens a file that does not exist.",
         probe="document.querySelector('a').href"),
    concept("Paths: links to your own files", '''
<p>A <b>path</b> is the route from the file you are in to the file you want.</p>'''),
    d_folders(),
    table(["You write", "It means"], [
        ["<code>about.html</code>", "a file in the same folder"],
        ["<code>pages/about.html</code>", "go into the <code>pages</code> folder, then the file"],
        ["<code>../index.html</code>", "go up one folder, then the file"],
    ]),
    rule("6.3", "Paths use forward slashes /",
         "<p>Web paths always use <code>/</code>, even on Windows where folders on your computer use <code>\\</code>.</p>",
         ok='<a href="pages/about.html">About</a>',
         bad=('<a href="pages\\about.html">About</a>', ["used as path segment delimiter"]),
         ok_kw={"probe": "document.querySelector('a').href"}, bad_kw={"probe": "document.querySelector('a').href"},
         why="The checker rejects a backslash as a folder separator. Chromium quietly turned it into <code>/</code> here (look at what the browser was asked), but you should not rely on a browser fixing it."),
    rule("6.4", "No spaces in file names",
         "<p>Use <code>-</code> or <code>_</code> instead of spaces when you name files: <code>my-trip.html</code>, not <code>my trip.html</code>.</p>",
         ok='<a href="my-trip.html">My trip</a>',
         bad=('<a href="my trip.html">My trip</a>', ["Illegal character in path segment"]),
         bad_kw={"probe": "document.querySelector('a').href"},
         why="Spaces are not allowed in a web address. The browser turns the space into <code>%20</code>, which is easy to get wrong. Name files without spaces and the problem never comes up."),
    rule("6.5", "Link to a part of the same page with #id",
         "<p>Give an element an <code>id</code>, then link to it with <code>#</code> and that id. Clicking scrolls to it. Each id may be used only once per page.</p>",
         ok='<h1>Our shop</h1>\n<a href="#contact">Jump to contact</a>\n<h2 id="contact">Contact</h2>',
         bad=('<h2 id="contact">Contact</h2>\n<p id="contact">Call us.</p>', ["Duplicate ID “contact”"]),
         why="With two elements sharing one id, the browser jumps to the first and the second can never be reached."),
    exercises([
        {"kind": "Write", "q": "Make a link that says <i>Wikipedia</i> and goes to <code>https://www.wikipedia.org</code>.",
         "sol": '<a href="https://www.wikipedia.org">Wikipedia</a>'},
        {"kind": "Think", "q": "You are in <code>pages/about.html</code>. What path links back to <code>index.html</code> one folder up?",
         "a": "<code>../index.html</code>. <code>..</code> means go up one folder."},
        {"kind": "Predict", "code": '<a href="contact.html">', "q": "Will anyone be able to click this link?",
         "expect": ["Unclosed element “a”"],
         "a": "No. There is no link text and no closing tag, so there is nothing to click."},
        {"kind": "Think", "q": "Why is <code>Trip Photos.html</code> a bad file name for a web page?",
         "a": "It has a space. Spaces are not allowed in web addresses. Use <code>trip-photos.html</code>."},
    ], "6"),
]))

topic("7", "images", "Images",
      "Put pictures on the page, describe them for people who cannot see them, and size them.", "".join([
    rule("7.1", "An image is <img> with src and alt",
         "<p><code>src</code> (source) is the path to the picture file. <code>alt</code> is a short description of it. <code>&lt;img&gt;</code> is a void element, so it has no closing tag.</p>",
         ok='<img src="sunset.png" alt="Orange sunset over green hills">',
         ok_kw={"files": {"sunset.png": SUNSET}}),
    rule("7.2", "Always write alt",
         "<p>Screen readers read <code>alt</code> aloud to people who cannot see the picture, and the browser shows it when the picture fails to load. The checker requires it.</p>",
         ok='<img src="sunset.png" alt="Orange sunset over green hills">',
         bad=('<img src="sunset.png">', ["An “img” element must have an “alt” attribute"]),
         ok_kw={"files": {"sunset.png": SUNSET}}, bad_kw={"files": {"sunset.png": SUNSET}},
         why="The picture still shows, so the mistake is invisible to you. It is not invisible to someone using a screen reader."),
    trap("a wrong file name shows a broken image",
         '<img src="sunst.png" alt="Orange sunset over green hills">',
         "The checker cannot know which files you have, so it finds nothing wrong. The browser could not find <code>sunst.png</code>, so it showed a broken-image icon and the alt text. Asked for the image's real width, it says 0: nothing loaded. Check the spelling and the folder.",
         files={"sunset.png": SUNSET}, probe="document.querySelector('img').naturalWidth"),
    rule("7.3", "width and height are plain numbers, no px",
         "<p>You can give an image a size in pixels with <code>width</code> and <code>height</code>. Write just the number.</p>",
         ok='<img src="sunset.png" alt="Sunset" width="120" height="75">',
         bad=('<img src="sunset.png" alt="Sunset" width="120px" height="75px">', ["Bad value “120px” for attribute “width”"]),
         ok_kw={"files": {"sunset.png": SUNSET}}, bad_kw={"files": {"sunset.png": SUNSET}},
         why="The attribute only accepts a number. The browser happened to cope here, but the checker reports both values as errors."),
    rule("7.4", "Images in a folder need the folder in the path",
         "<p>Keep pictures in an <code>images</code> folder and include the folder name in <code>src</code>.</p>",
         ok='<img src="images/sunset.png" alt="Sunset">',
         ok_kw={"files": {"images/sunset.png": SUNSET}}),
    trap("forgetting the folder",
         '<img src="sunset.png" alt="Sunset">',
         "The picture is in <code>images/</code>, but the path says the file is right next to the page. The browser cannot find it and shows the alt text.",
         files={"images/sunset.png": SUNSET}),
    exercises([
        {"kind": "Write", "q": "Show <code>sunset.png</code> (in the same folder) with a good description.",
         "sol": '<img src="sunset.png" alt="Orange sunset over green hills">', "files": {"sunset.png": SUNSET}},
        {"kind": "Predict", "code": '<img src="sunset.png" alt="Sunset"></img>', "q": "Will the checker accept this?",
         "expect": ["Stray end tag “img”"], "files": {"sunset.png": SUNSET},
         "a": "No. <code>&lt;img&gt;</code> is a void element, so <code>&lt;/img&gt;</code> is not allowed."},
        {"kind": "Think", "q": "The picture loads fine without alt. Why add it?",
         "a": "Screen readers read alt aloud, and the browser shows it when the picture fails to load."},
        {"kind": "Predict", "code": '<img src="sunset.png" alt="Sunset" width="60">', "q": "How wide is the picture, and what happens to its height?",
         "files": {"sunset.png": SUNSET}, "probe": "(i => i.width + ' x ' + i.height)(document.querySelector('img'))",
         "a": "60 pixels wide. With only width set, the browser scales the height to keep the shape."},
    ], "7"),
]))

COMING = [("8", "Lists"), ("9", "Tables"), ("10", "Forms"), ("11", "Page layout tags"),
          ("12", "Special characters"), ("13", "Mini project")]


# ---------------------------------------------------------------- run the jobs

def doc_text(j):
    return j["code"] + "\n" if j["raw"] else WRAP_TOP + j["code"] + WRAP_END


def write_jobs():
    for j in JOBS:
        d = WORK / f"j{j['id']}"
        d.mkdir(parents=True)
        for name, body in j["files"].items():
            p = d / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(body if isinstance(body, bytes) else body.encode())
        (d / j["page"]).write_text(doc_text(j), encoding="utf-8")
        j["path"] = d / j["page"]


def check_all():
    paths = [str(j["path"]) for j in JOBS if j["check"]]
    p = subprocess.run([str(VNU), "--format", "json", *paths], capture_output=True, text=True)
    data = json.loads(p.stderr or p.stdout)
    by = {}
    for m in data["messages"]:
        url = m.get("url", "")
        by.setdefault(url.replace("file:", ""), []).append(m)
    for j in JOBS:
        msgs = by.get(str(j["path"]), []) + by.get(str(j["path"].resolve()), [])
        out = []
        for m in msgs:
            kind = "Error" if m["type"] == "error" else "Warning" if m.get("subType") == "warning" else None
            if not kind:
                continue
            line = m.get("lastLine")
            if line and not j["raw"]:
                line -= WRAP_LINES
            out.append((kind, m["message"], line))
        j["msgs"] = out
        text = " | ".join(f"{k}: {t}" for k, t, _ in out)
        if j["expect"]:
            for e in j["expect"]:
                hit = [k for k, t, _ in out if e in t]
                if not hit:
                    sys.exit(f"JOB {j['id']} EXPECTED '{e}'\n{j['code']}\n--- checker said: {text or '(nothing)'}")
                if not j["warn"] and "Error" not in hit:
                    sys.exit(f"JOB {j['id']} expected an ERROR for '{e}', got {hit}")
        elif j["check"] and j["clean"] and out:
            sys.exit(f"JOB {j['id']} SHOULD BE CLEAN\n{j['code']}\n--- checker said: {text}")


def png_uri(raw):
    im = Image.open(io.BytesIO(raw)).convert("RGB").quantize(colors=64, method=Image.Quantize.MEDIANCUT)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def render_all():
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={"width": 480, "height": 400}, device_scale_factor=2)
        pg = ctx.new_page()
        for j in JOBS:
            pg.goto(j["path"].as_uri())
            pg.wait_for_load_state("load")
            h = pg.evaluate("Math.ceil(Math.max(document.body ? document.body.getBoundingClientRect().bottom + 8 : 40, 40))")
            j["height"] = min(h, 360)
            pg.set_viewport_size({"width": 480, "height": j["height"]})
            j["shot"] = png_uri(pg.screenshot(clip={"x": 0, "y": 0, "width": 480, "height": j["height"]}))
            pg.set_viewport_size({"width": 480, "height": 400})
            if j["dom"]:
                j["built"] = pg.evaluate("document.body ? document.body.innerHTML.trim() : document.documentElement.outerHTML") \
                    if not j["raw"] else pg.evaluate("document.documentElement.outerHTML")
                # the whitespace after </body> in the file is moved into the body by the parser; hide it
                j["built"] = re.sub(r"\s+((?:</[a-z0-9]+>)+)$", r"\1", re.sub(r"\n\s*\n+", "\n", j["built"]))
            if j["probe"]:
                v = pg.evaluate(j["probe"])
                j["probed"] = str(v).replace(j["path"].parent.as_uri(), "file:///your-folder")
        b.close()


def fill(page):
    for j in JOBS:
        for label in ("What the browser shows", "What the browser really shows"):
            token = f'@@JOB{j["id"]}:{label}@@'
            if token not in page:
                continue
            parts = [f'<div class="outlabel">{label}</div>',
                     f'<div class="shot"><img src="{j["shot"]}" width="480" height="{j["height"]}" alt="Screenshot of the rendered example"></div>']
            if j.get("probed") is not None:
                parts.append(f'<div class="outlabel">Asked the browser</div><pre class="out"><span class="tb">{esc(j["probe"])}</span>\n'
                             f'<span class="o">{esc(j["probed"])}</span></pre>')
            if j.get("built") is not None:
                parts.append(f'<div class="outlabel">What the browser built</div>{code_html(j["built"])}')
            if j["check"]:
                if j["msgs"]:
                    rows = "\n".join(f'<span class="{"errline" if k == "Error" else "warnline"}">{k}: {esc(t)}</span>'
                                     f'{f" <span class=tb>(line {ln})</span>" if ln else ""}' for k, t, ln in j["msgs"])
                else:
                    rows = '<span class="okline">No errors or warnings.</span>'
                parts.append(f'<div class="outlabel">Checker says</div><pre class="out wrap">{rows}</pre>')
            page = page.replace(token, "".join(parts))
    assert "@@JOB" not in page
    return page


# ---------------------------------------------------------------- page

HTML_LOGO = '''<svg viewBox="74 100 364 412" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<polygon fill="#E44D26" points="107.644,470.877 74.633,100.62 437.367,100.62 404.321,470.819 255.778,512"/>
<polygon fill="#F16529" points="256,480.523 376.03,447.246 404.27,130.894 256,130.894"/>
<polygon fill="#EBEBEB" points="256,268.217 195.91,268.217 191.76,221.716 256,221.716 256,176.305 255.843,176.305 142.132,176.305 143.219,188.488 154.38,313.627 256,313.627"/>
<polygon fill="#EBEBEB" points="256,386.153 255.801,386.206 205.227,372.55 201.994,336.333 177.419,336.333 156.409,336.333 162.771,407.634 255.791,433.457 256,433.399"/>
<polygon fill="#FFFFFF" points="255.843,268.217 255.843,313.627 311.761,313.627 306.49,372.521 255.843,386.191 255.843,433.435 348.937,407.634 349.62,399.962 360.291,280.411 361.399,268.217 349.162,268.217"/>
<polygon fill="#FFFFFF" points="255.843,176.305 255.843,204.509 255.843,221.605 255.843,221.716 365.385,221.716 365.385,221.716 365.531,221.716 366.442,211.509 368.511,188.488 369.597,176.305"/>
</svg>'''

EXTRA_CSS = r'''
.shot { padding: 8px 14px 12px; }
.shot img { display: block; max-width: 100%; height: auto; border: 1px solid var(--line); border-radius: 4px; background: #fff; }
pre.out.wrap { white-space: pre-wrap; }
pre.out .warnline { color: var(--trap); font-weight: 600; }
pre.out .okline { color: var(--ok); font-weight: 600; }
.src { font-size: 14px; color: var(--muted); margin: 8px 0 0; }
.src a { color: var(--py-blue); }
.note { font-size: 14px; color: var(--muted); margin: 12px 0 0; }
.prose ol { margin: 0 0 12px; padding-left: 22px; }
'''


def build():
    rail = ['<nav class="rail" aria-label="Chapters"><a class="brand" href="#cover">' + HTML_LOGO + 'HTML From Zero</a>',
            '<h4>Chapters</h4><ol>']
    short = {"2": "First page, mistakes", "3": "Tags and attributes"}
    for num, slug, title, goal, body in TOPICS:
        rail.append(f'<li><a href="#t-{slug}"><span class="n">{num}</span><span>{short.get(num, title)}</span></a></li>')
    rail.append('</ol><div class="soonlist"><h4>Next part</h4><ol>')
    for num, title in COMING:
        rail.append(f'<li class="soon"><span class="n">{num}</span><span>{title}</span></li>')
    rail.append('</ol></div></nav>')

    total = len(TOPICS) + 1

    def label(i):
        if i == 0:
            return "Cover"
        n, _, t, _, _ = TOPICS[i - 1]
        return f"Chapter {n}: {t}"

    def ident(i):
        return "cover" if i == 0 else "t-" + TOPICS[i - 1][1]

    def pager(i):
        prev = f'<a class="prev" href="#{ident(i - 1)}"><span>Previous</span>{label(i - 1)}</a>' if i > 0 else '<span></span>'
        nxt = (f'<a class="nextp" href="#{ident(i + 1)}"><span>Next</span>{label(i + 1)}</a>' if i + 1 < total
               else '<a class="nextp" href="#cover"><span>Back to</span>Cover</a>')
        return f'<nav class="pager" aria-label="Pages">{prev}<span class="pno">Page {i + 1} of {total}</span>{nxt}</nav>'

    nxt = '<section class="next"><h3>Next part: chapters 8 to 13</h3><p>Lists, tables, forms, page layout tags, special characters, and a mini project. Same format.</p></section>'
    sections = []
    for i, (num, slug, title, goal, body) in enumerate(TOPICS, start=1):
        rules = RULE_INDEX.get(num, [])
        toc = ('<ol class="toc">' + "".join(f'<li><a href="#{rid}"><span class="rn">{rn}</span><span>{t}</span></a></li>'
                                            for rid, rn, t in rules) + "</ol>") if rules else ""
        extra = nxt if i == len(TOPICS) else ""
        sections.append(f'<section class="topic page" id="t-{slug}"><div class="topic-head">'
                        f'<div class="chapno">Chapter {num}</div><h2>{title}</h2><p class="goal">{goal}</p>{toc}</div>'
                        f'{body}{extra}{pager(i)}</section>')

    n_rules = sum(len(v) for v in RULE_INDEX.values())
    hero = f'''<section class="page cover" id="cover"><header class="hero">
<h1>HTML From Zero</h1>
<p>A book that starts at "what is a web page". Every rule shows HTML that works, HTML that breaks, a picture of what the browser really drew, and what the official checker says.</p>
<div class="how">
<div><b>1. Read the rule</b>Each rule has a working example and a breaking one.</div>
<div><b>2. Type it yourself</b>Copy each example into an <code>.html</code> file, open it, then break it on purpose.</div>
<div><b>3. Predict, then check</b>Write your answer before you open it. Being wrong first is how it sticks.</div>
</div>
<p class="meta">Chapters 0 to 7 · {n_rules} rules · {EX_COUNT[0]} exercises · every picture is a screenshot from Chromium, and every <i>Checker says</i> box is from the W3C Nu HTML Checker {VNU_VER}, both run on {TODAY}.</p>
</header>{pager(0)}</section>'''

    page = f'''<title>HTML From Zero</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=Kalam:wght@400&display=swap">
<style>{CSS}{EXTRA_CSS}</style>
{DEFS}
<div class="wm" aria-hidden="true">{HTML_LOGO}</div>
<div class="shell">
{"".join(rail)}
<main><div class="col">{hero}{"".join(sections)}</div></main>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script>{JS}</script>
'''
    return page, n_rules


VNU_VER = subprocess.run([str(VNU), "--version"], capture_output=True, text=True).stdout.strip().split(" ")[0]

if __name__ == "__main__":
    page, n_rules = build()
    write_jobs()
    check_all()
    render_all()
    page = fill(page)
    (HERE / 'report.json').write_text(json.dumps([{k: j.get(k) for k in ('id', 'code', 'msgs', 'probed', 'built', 'height')} for j in JOBS], ensure_ascii=False, indent=1))
    OUT.write_text(page)
    shutil.rmtree(WORK, ignore_errors=True)
    print(f"wrote {OUT}  rules={n_rules} exercises={EX_COUNT[0]} examples={len(JOBS)} bytes={len(page)}")
