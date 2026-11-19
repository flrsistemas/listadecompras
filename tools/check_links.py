import os, re, shutil, sys

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import APP, SITE, PC_DOCS, OUT, TOOLS
PREV = os.path.join(OUT, 'tree')

# monta a arvore como ficara no ar: / (empresa), /listadecompras/ (app), /precocerto/ (docs)
if os.path.exists(PREV):
    shutil.rmtree(PREV)
shutil.copytree(SITE, PREV, ignore=shutil.ignore_patterns('.git'))
shutil.copytree(APP, os.path.join(PREV, 'listadecompras'), ignore=shutil.ignore_patterns('.git', '.claude', '.agents', 'node_modules', 'tools'))
shutil.copytree(PC_DOCS, os.path.join(PREV, 'precocerto'))

HREF = re.compile(r'(?:href|src)="([^"#?]*)(?:[#?][^"]*)?"')
bad = {}
pages = 0
for dp, dn, fn in os.walk(PREV):
    for f in fn:
        if not f.endswith('.html'):
            continue
        pages += 1
        p = os.path.join(dp, f)
        txt = open(p, encoding='utf-8').read()
        for m in HREF.finditer(txt):
            u = m.group(1)
            if not u.startswith('/') or u.startswith('//'):
                continue
            rel = u.lstrip('/')
            t = os.path.join(PREV, rel.replace('/', os.sep))
            ok = os.path.isfile(t) or (os.path.isdir(t) and os.path.isfile(os.path.join(t, 'index.html'))) or rel == ''
            if rel == '':
                ok = os.path.isfile(os.path.join(PREV, 'index.html'))
            if not ok:
                bad.setdefault(u, []).append(os.path.relpath(p, PREV))
print('paginas verificadas:', pages)
for u, ps in sorted(bad.items()):
    print('QUEBRADO', u, '<-', ps[:3])
print('sem links quebrados' if not bad else '%d link(s) quebrado(s)' % len(bad))

# arquivos de teste (nao vao para o ar): app com Supabase simulado
shutil.copytree(os.path.join(TOOLS, 'testfiles'), os.path.join(PREV, 'test'))
