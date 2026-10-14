"""Build the AI handbook from topic data (topics_*.py) into src.html, then inline the font."""
import base64, html, importlib.util, re, sys, pathlib

ROOT = pathlib.Path(__file__).parent
QA_SRC = pathlib.Path('/Users/chethanbhatbs/Documents/qa-handbook/src.html').read_text()
FONT = '/private/tmp/claude-501/-Users-chethanbhatbs/9f83bfda-1bb3-49d1-931b-cca4bb85e971/scratchpad/virgil.woff2'

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f'{name}.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

TAGS = {'production': 'ok', 'research': 'res', 'demo': 'warn', 'claim': 'claim', 'reported': 'claim'}

def tagify(s):
    """[production] etc. become small labelled chips."""
    return re.sub(r'\[(production|research|demo|claim|reported)\]',
                  lambda m: f'<span class="chip {TAGS[m.group(1)]}">{m.group(1)}</span>', s)

def ul(items):
    return '<ul class="plain">' + ''.join(f'<li>{tagify(i)}</li>' for i in items) + '</ul>'

def card(t, code, cls):
    h = [f'<section id="{t["id"]}" class="{cls} topic">',
         f'  <h2><span class="n">{code}</span>{t["title"]}</h2>',
         f'  <p class="what">{t["what"]}</p>']
    if t.get('diagram'):
        d = t['diagram']
        h.append(f'  <figure class="dg"><div class="scroll"><svg id="{d[0]}" style="--minw:{d[1]}px" role="img" aria-label="{html.escape(d[2])}"></svg></div><figcaption>{d[3]}</figcaption></figure>')
    h.append(f'  <h3>How it works</h3>\n  {t["how"]}')
    if t.get('extra'):
        h.append(t['extra'])
    terms = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td></tr>' for a, b in t['terms'])
    h.append(f'  <h3>Key terms</h3><div class="tbl"><table>{terms}</table></div>')
    rows = [('Where it is used', t['uses']), ('Current state', t['state']), ('Limitations', t['limits']), ("What's next", t['next'])]
    h.append('  <div class="facts">' + ''.join(f'<div class="fr"><div class="fl">{a}</div><div class="fc">{ul(b)}</div></div>' for a, b in rows) + '</div>')
    if t.get('qa'):
        h.append(f'  <div class="qa"><h3>QA perspective</h3>{ul(t["qa"])}</div>')
    links = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{l}</a></li>' for l, u in t['learn'])
    h.append(f'  <div class="facts"><div class="fr"><div class="fl">Further learning</div><div class="fc"><ul class="plain links">{links}</ul></div></div></div>')
    h.append('</section>\n')
    return '\n'.join(h)

def build():
    parts = load('topics').PARTS
    extra_css = load('topics').CSS
    diag = (ROOT / 'diagrams_v2.js').read_text()
    head = QA_SRC[:QA_SRC.index('<header class="top">')].replace('<title>QA Handbook</title>', '<title>How AI Works</title>')
    head = head.replace('svg text.tx{font-size:15px}', 'svg text.tx{font-size:15px}\nsvg .grn{color:var(--ok)}', 1)
    head = head.replace('</style>', extra_css + '\n</style>', 1)
    scripts = QA_SRC[QA_SRC.index('<script src="https://cdnjs'):QA_SRC.index('function build(){')]
    scripts = scripts.replace("    } else if (it.t === 'num'){",
        "    } else if (it.t === 'curve'){\n      grp(it.cls || 'ink').appendChild(rc.curve(it.p, o({strokeWidth: it.w || 1.6, roughness:0.8})));\n    } else if (it.t === 'num'){", 1)
    tail = QA_SRC[QA_SRC.index('function go(){'):]
    hdr = load('topics').HEADER
    nav, main = '', ''
    for p in parts:
        nav += f'  <h4>{p["nav"]}</h4>\n  <ol>\n'
        if p.get('level'):
            lid, sm, title, desc = p['level']
            main += f'<div class="level" id="{lid}"><small>{sm}</small><b>{title}</b><span>{desc}</span></div>\n\n'
        for i, t in enumerate(p['topics'], 1):
            code = f'{p["prefix"]}{i}'
            nav += f'    <li><a href="#{t["id"]}"><span>{code}</span>{t.get("short", t["title"])}</a></li>\n'
            main += t['raw'].replace('@@CODE@@', code) if t.get('raw') else card(t, code, p['cls'])
        nav += '  </ol>\n'
    body = hdr + '\n<div class="wrap">\n<nav class="rail" aria-label="Chapters">\n' + nav + '</nav>\n\n<main>\n\n' + main + '</main>\n</div>\n\n' + load('topics').FOOTER
    out = head + body + '\n' + scripts + 'function build(){\n' + diag + '\n}\n' + tail
    def lang(pre):
        p = pre.lstrip()
        if p.startswith(('CREATE', 'SELECT')): return 'sql'
        if p.startswith('{'): return 'json'
        if p.startswith(('import ', 'def ', 'probs', 'gates', 'from ')): return 'python'
        return 'none'
    out = re.sub(r'<pre>(.*?)</pre>', lambda m: f'<pre class="language-{lang(m.group(1))}"><code class="language-{lang(m.group(1))}">{m.group(1)}</code></pre>', out, flags=re.S)
    (ROOT / 'src.html').write_text(out)
    f = base64.b64encode(open(FONT, 'rb').read()).decode()
    (ROOT / 'ai-handbook.html').write_text(out.replace('__VIRGIL__', f))
    print('topics', sum(len(p['topics']) for p in parts), 'ch-caps', len(re.findall(r'max-width:\d+ch', out)),
          'dashes', out.count('—') + out.count('–'), 'bare-pre', out.count('<pre>'))

if __name__ == '__main__':
    build()
