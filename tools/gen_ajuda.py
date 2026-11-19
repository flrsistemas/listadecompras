import os, re, sys, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import help_content as H

ICONS_HTML = '<link rel="icon" href="/listadecompras/icons/icon.svg" type="image/svg+xml">\n<link rel="icon" href="/listadecompras/icons/favicon-32.png" sizes="32x32" type="image/png">\n<link rel="apple-touch-icon" href="/listadecompras/icons/apple-touch-icon.png">\n<meta name="theme-color" content="#16a34a">\n'

from config import APP
BASE = "/listadecompras/ajuda/"
P = {'pt': BASE, 'en': BASE + 'en/', 'es': BASE + 'es/'}
PRIV = {'pt': '/listadecompras/privacy.html', 'en': '/listadecompras/privacy-en.html', 'es': '/listadecompras/privacy-es.html'}
SOBRE = {'pt': '/listadecompras/sobre/', 'en': '/listadecompras/sobre/en/', 'es': '/listadecompras/sobre/es/'}
CONTACT = {'pt': '/contato/', 'en': '/en/contact/', 'es': '/es/contacto/'}
OG = {'pt': 'pt_BR', 'en': 'en_US', 'es': 'es_ES'}

# CSS base = o mesmo das paginas de apresentacao
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_sobre.py'), encoding='utf-8').read()
BASE_CSS = re.search(r'CSS = """(.*?)"""', src, re.S).group(1)
EXTRA = """
  h1.page { font-size: 1.7rem; line-height: 1.25; margin: 34px 0 6px; }
  p.intro { color: var(--muted); margin: 0 0 22px; }
  .box { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 18px 20px; margin: 0 0 14px; }
  .box h3 { margin: 0 0 6px; font-size: 1.02rem; }
  .box p { margin: 0; color: var(--muted); font-size: .95rem; }
"""

DESC = {
 'pt': 'Perguntas frequentes sobre o app Lista de Compras.',
 'en': 'Frequently asked questions about the Lista de Compras app.',
 'es': 'Preguntas frecuentes sobre la app Lista de Compras.',
}
BACK = {'pt': '← Lista de Compras', 'en': '← Lista de Compras', 'es': '← Lista de Compras'}
INTRO = {
 'pt': 'Respostas rápidas sobre o <strong>Lista de Compras</strong>.',
 'en': 'Quick answers about <strong>Lista de Compras</strong>.',
 'es': 'Respuestas rápidas sobre <strong>Lista de Compras</strong>.',
}
FOOT = {'pt': 'Contato', 'en': 'Contact', 'es': 'Contacto'}


def page(lang):
    h = copy.deepcopy(H.DATA[lang])
    h['intro'] = INTRO[lang]
    old = H.DATA
    H.DATA = dict(old); H.DATA[lang] = h
    body = H.build_help(lang, {'pc': '', 'priv': PRIV[lang], 'contact': CONTACT[lang]})
    H.DATA = old
    langs = ''.join(
        '<a href="%s" lang="%s" hreflang="%s"%s onclick="try{localStorage.setItem(\'lang\',\'%s\')}catch(e){}">%s</a>'
        % (P[c], c, c, ' aria-current="page"' if c == lang else '', c, c.upper()) for c in ('pt', 'en', 'es'))
    alts = ''.join('<link rel="alternate" hreflang="%s" href="https://flrsistemas.com.br%s">\n' % (c, P[c]) for c in ('pt', 'en', 'es'))
    title = '%s — Lista de Compras' % h['title']
    script = ''
    if lang == 'pt':
        script = ("<script>\n  (function () {\n    try {\n"
                  "      var salvo = localStorage.getItem('lang');\n"
                  "      var l = salvo || String((navigator.languages && navigator.languages[0]) || navigator.language || 'pt').slice(0, 2).toLowerCase();\n"
                  "      if (l !== 'pt') location.replace('%s' + (l === 'es' ? 'es' : 'en') + '/');\n"
                  "    } catch (e) {}\n  })();\n</script>\n" % BASE)
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>{title}</title>
<meta name="description" content="{DESC[lang]}">
<link rel="canonical" href="https://flrsistemas.com.br{P[lang]}">
{alts}<link rel="alternate" hreflang="x-default" href="https://flrsistemas.com.br{P['pt']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="FLR Sistemas">
<meta property="og:locale" content="{OG[lang]}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{DESC[lang]}">
<meta property="og:url" content="https://flrsistemas.com.br{P[lang]}">
{ICONS_HTML}<style>{BASE_CSS}{EXTRA}</style>
{script}</head>
<body>
<main>

  <header class="site topbar">
    <a class="back" href="{SOBRE[lang]}">{BACK[lang]}</a>
    <nav class="langs" aria-label="Language">{langs}</nav>
  </header>

  <article class="app" id="ajuda" style="margin-top:12px;padding-top:0;border-top:0">
{body}
  </article>

  <footer>
    <p>
      FLR Sistemas<br>
      {FOOT[lang]}: <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a><br>
      <a href="{PRIV[lang]}">{ {'pt': 'Política de privacidade', 'en': 'Privacy Policy', 'es': 'Política de privacidad'}[lang] }</a>
    </p>
  </footer>

</main>
</body>
</html>
'''


for lang, sub in (('pt', ''), ('en', 'en'), ('es', 'es')):
    d = os.path.join(APP, 'ajuda', sub) if sub else os.path.join(APP, 'ajuda')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(page(lang))
print('ok')
