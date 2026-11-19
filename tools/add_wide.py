import os, re

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import APP, SITE, PC_DOCS as PC, WORK as S

CSS = '''<style id="wide">
  /* Todas as abas usam a mesma largura em telas grandes (sem "pulo" ao trocar de aba) */
  html { scrollbar-gutter: stable; }
  @media (min-width: 1000px) {
    main.wide { max-width: 1100px; }
    main.wide .apps { gap: 24px; }
    main.wide article.app { padding: 26px 28px; }
    main.wide .thumb { height: 260px; }
    main.wide article.app > p, main.wide article.app > .summary { max-width: 72ch; }
    main.wide .grid { grid-template-columns: repeat(3, 1fr); }
    main.wide ol.steps { grid-template-columns: 1fr 1fr; }
    main.wide .shots { flex-wrap: wrap; overflow: visible; scroll-snap-type: none; gap: 20px; }
    main.wide .shots img { width: 220px; }
    main.wide .shots figcaption { max-width: 220px; }
    main.wide .shots.docs img { width: 300px; }
    main.wide .shots.docs figcaption { max-width: 300px; }
    /* abas de texto (Novidades, Ajuda, Contato, Privacidade): mesma largura, conteudo em colunas */
    main.wide .boxes { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin: 0 0 22px; }
    main.wide .boxes .box { margin: 0; }
    main.wide .news-list { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; align-items: start; }
    main.wide .news-list .news-item { margin: 0; }
    main.wide .faq-cols { display: grid; grid-template-columns: 1fr 1fr; gap: 0 36px; align-items: start; }
    main.wide .faq-cols section.faq-group:first-child, main.wide .faq-cols section.faq-group:nth-child(2) { margin-top: 30px; }
  }
</style>
'''

targets = [
    os.path.join(APP, 'sobre', 'index.html'), os.path.join(APP, 'sobre', 'en', 'index.html'), os.path.join(APP, 'sobre', 'es', 'index.html'),
    os.path.join(APP, 'ajuda', 'index.html'), os.path.join(APP, 'ajuda', 'en', 'index.html'), os.path.join(APP, 'ajuda', 'es', 'index.html'),
    os.path.join(PC, 'index.html'), os.path.join(PC, 'en', 'index.html'), os.path.join(PC, 'es', 'index.html'),
]
# todas as paginas do site da empresa (home e abas), menos os redirecionamentos
for dp, dn, fn in os.walk(SITE):
    dn[:] = [d for d in dn if d != '.git' and d != 'img']
    for f in fn:
        if f == 'index.html':
            p = os.path.join(dp, f)
            if 'http-equiv="refresh"' not in open(p, encoding='utf-8').read():
                targets.append(p)
for p in targets:
    t = open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in t else '\n'
    t = t.replace('\r\n', '\n')
    t = re.sub(r'<style id="wide">.*?</style>\n', '', t, flags=re.S)
    assert '</head>' in t and '<main' in t, p
    t = re.sub(r'<main(?: class="wide")?>', '<main class="wide">', t, count=1)
    t = t.replace('</head>', CSS + '</head>', 1)
    open(p, 'w', encoding='utf-8', newline='').write(t.replace('\n', nl))
    print('ok', os.path.relpath(p, S if (SITE in p or PC in p) else APP))
