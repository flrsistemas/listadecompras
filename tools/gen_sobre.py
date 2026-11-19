import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import APP
ROOT = os.path.join(APP, 'sobre')
BASE = "/listadecompras/sobre/"

ICONS_HTML = '<link rel="icon" href="/listadecompras/icons/icon.svg" type="image/svg+xml">\n<link rel="icon" href="/listadecompras/icons/favicon-32.png" sizes="32x32" type="image/png">\n<link rel="apple-touch-icon" href="/listadecompras/icons/apple-touch-icon.png">\n<meta name="theme-color" content="#16a34a">\n'

CSS = """
  :root {
    color-scheme: dark;
    --bg: #14201A;
    --surface: #1B2B22;
    --text: #E9F2EC;
    --muted: #A9BDB0;
    --border: #2D4336;
    --accent: #4ADE80;
    --accent-bg: #1D3A2A;
    --brand: #16A34A;
    --brand-text: #FFFFFF;
  }
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0 16px 72px; background: var(--bg); color: var(--text);
    font: 16px/1.65 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
  main { max-width: 760px; margin: 0 auto; }
  header.site { padding: 24px 0 0; }
  .back { color: var(--muted); font-size: .95rem; text-decoration: none; }
  .back:hover, .back:focus-visible { color: var(--text); text-decoration: underline; }
  article.app { margin-top: 40px; padding-top: 28px; border-top: 1px solid var(--border); }
  .app h2 { font-size: 1.6rem; line-height: 1.2; margin: 0 0 6px; }
  .app .lead { font-size: 1.1rem; color: var(--muted); margin: 0 0 20px; }
  .app h3.section { font-size: 1.05rem; margin: 30px 0 12px; }
  .actions { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; margin: 0 0 6px; }
  .button { display: inline-block; background: var(--brand); color: var(--brand-text); padding: 13px 22px;
    border-radius: 12px; font-weight: 600; text-decoration: none; }
  .button:hover, .button:focus-visible { filter: brightness(1.12); }
  .link { color: var(--muted); font-size: .95rem; }
  .note { color: var(--muted); font-size: .9rem; margin: 10px 0 0; }
  .grid { display: grid; grid-template-columns: 1fr; gap: 14px; }
  @media (min-width: 640px) { .grid { grid-template-columns: 1fr 1fr; } }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 18px 20px; }
  .card h4 { margin: 0 0 6px; font-size: 1.02rem; }
  .card p { margin: 0; color: var(--muted); font-size: .95rem; }
  ol.steps { list-style: none; counter-reset: passo; padding: 0; margin: 0; display: grid; gap: 12px; }
  ol.steps li { counter-increment: passo; position: relative; background: var(--surface); border: 1px solid var(--border);
    border-radius: 14px; padding: 16px 18px 16px 64px; }
  ol.steps li::before { content: counter(passo); position: absolute; left: 18px; top: 16px; width: 32px; height: 32px;
    border-radius: 50%; background: var(--brand); color: var(--brand-text); display: grid; place-items: center; font-weight: 700; }
  ol.steps h4 { margin: 0 0 4px; font-size: 1.02rem; }
  ol.steps p { margin: 0; color: var(--muted); font-size: .95rem; }
  .shots { display: flex; gap: 14px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 4px 2px 14px; margin: 0 -2px; }
  .shots figure { margin: 0; flex: 0 0 auto; scroll-snap-align: start; }
  .shots img { display: block; width: 200px; height: auto; border-radius: 18px; border: 1px solid var(--border); }
  .shots figcaption { color: var(--muted); font-size: .85rem; margin-top: 8px; max-width: 200px; }
  .summary { background: var(--accent-bg); border-left: 4px solid var(--accent); border-radius: 0 10px 10px 0; padding: 16px 18px; }
  .summary p { margin: 0; }
  a { color: inherit; text-decoration-color: var(--accent); text-underline-offset: 3px; }
  a.button { text-decoration: none; }
  footer { margin-top: 56px; padding-top: 20px; border-top: 1px solid var(--border); color: var(--muted); font-size: .88rem; }
  .topbar { display: flex; justify-content: space-between; align-items: center; gap: 16px; }
  .langs { display: flex; gap: 4px; margin-left: auto; font-size: .85rem; }
  .langs a { color: var(--muted); text-decoration: none; padding: 4px 10px; border: 1px solid var(--border); border-radius: 999px; }
  .langs a:hover, .langs a:focus-visible { color: var(--text); }
  .langs a[aria-current="page"] { color: var(--text); border-color: var(--muted); font-weight: 600; }
"""

T = {
 'pt': dict(
  lang='pt', og='pt_BR', path=BASE, back='← FLR Sistemas', home='/',
  title='Lista de Compras — FLR Sistemas',
  desc='Listas de compras compartilhadas em tempo real, com preço dos itens e total da lista. Funciona no navegador e instala no celular.',
  lead='Faça as compras em conjunto: listas compartilhadas que se atualizam em tempo real.',
  open='Abrir o app', how='Como funciona',
  note='App web (PWA) para quem divide as compras da casa. Funciona no navegador e instala no celular, sem loja de aplicativos. Em português, inglês e espanhol. Dá para usar sem criar conta (as listas ficam só no aparelho).',
  h_what='O que ele faz',
  what='Crie uma lista, convide quem compra com você pelo e-mail e pronto: cada item marcado, adicionado ou removido aparece na hora para todos. Informe o preço unitário de cada item e acompanhe quanto a compra vai custar.',
  cards=[
   ('Compartilhe por e-mail','Convide familiares ou amigos pelo e-mail da conta deles. Só quem foi convidado vê a lista.'),
   ('Tempo real','Marcou o leite como comprado? Todo mundo vê na mesma hora, sem recarregar a página.'),
   ('Carrinho e total','Informe o preço unitário: o app multiplica pela quantidade e mostra, no topo da lista, o valor que já está no carrinho e o total. O total de cada lista aparece nos cartões da tela inicial.'),
   ('Por categoria','Os itens se organizam em Hortifruti, Açougue, Padaria e outras, e o app sugere a categoria pelo nome.'),
   ('Use sem sinal','No mercado sem sinal, você vê a última versão da lista e continua usando: marca, adiciona, edita e remove itens, cria, renomeia e exclui listas, e tudo é enviado quando o sinal volta.'),
   ('Instala como app','Adicione à tela inicial do celular e abra como qualquer outro aplicativo.'),
  ],
  h_how='Como funciona', how_id='how',
  steps=[
   ('Crie sua conta','Cadastre-se com nome, e-mail e uma senha de pelo menos 8 caracteres, com letras e números. Confirme o e-mail que você receber e entre.'),
   ('Crie uma lista','Dê um nome, como "Mercado do mês", e toque em Criar.'),
   ('Adicione os itens','Digite o nome, e se quiser a quantidade e o preço. A categoria é sugerida sozinha, e você pode trocar.'),
   ('Compartilhe','Toque no ícone de pessoas, informe o e-mail de quem vai participar e toque em Compartilhar. A pessoa precisa já ter uma conta.'),
  ],
  h_install='Instalar no celular',
  install='<strong>Android (Chrome):</strong> abra o app, toque no menu ⋮ e em "Instalar app" ou "Adicionar à tela inicial".<br><strong>iPhone (Safari):</strong> toque em Compartilhar e em "Adicionar à Tela de Início".',
  summary='Cada lista só é visível para quem foi convidado. O dono pode remover participantes ou excluir a lista, e cada participante pode sair da lista quando quiser.',
  contact='Contato',
 ),
 'en': dict(
  lang='en', og='en_US', path=BASE+'en/', back='← FLR Sistemas', home='/en/',
  title='Lista de Compras — FLR Sistemas',
  desc='Shopping lists shared in real time, with item prices and a list total. Works in the browser and installs on your phone.',
  lead='Shop together: shared lists that update in real time.',
  open='Open the app', how='How it works',
  note='Web app (PWA) for anyone sharing the household shopping. Works in the browser and installs on your phone, no app store needed. The app comes in English, Portuguese and Spanish. You can use it without an account (the lists stay only on your device).',
  h_what='What it does',
  what="Create a list, invite the people you shop with by e-mail, and that is it: every item checked, added or removed shows up instantly for everyone. Add each item's unit price and keep track of what the shopping will cost.",
  cards=[
   ('Share by e-mail','Invite family or friends using the e-mail of their account. Only invited people can see the list.'),
   ('Real time','Checked the milk off? Everyone sees it right away, without reloading the page.'),
   ('Cart and total',"Enter the unit price: the app multiplies it by the quantity and shows, at the top of the list, what is already in the cart and the total. Each list's total appears on the cards of the home screen."),
   ('By category','Items are grouped into Produce, Butcher, Bakery and more, and the app suggests the category from the name.'),
   ('Use it with no signal','At the supermarket with no signal, you still see the last version of the list and keep using it: check, add, edit and remove items, create, rename and delete lists, and everything is sent when the signal returns.'),
   ('Installs like an app',"Add it to your phone's home screen and open it like any other app."),
  ],
  h_how='How it works', how_id='how',
  steps=[
   ('Create your account','Sign up with your name, e-mail and a password of at least 8 characters, with letters and numbers. Confirm the e-mail you receive and sign in.'),
   ('Create a list','Give it a name, like "Monthly groceries", and tap "Create".'),
   ('Add the items','Type the name, and the quantity and price if you like. The category is suggested automatically, and you can change it.'),
   ('Share','Tap the people icon, enter the e-mail of who will join and tap "Share". That person needs to have an account already.'),
  ],
  h_install='Install on your phone',
  install='<strong>Android (Chrome):</strong> open the app, tap the ⋮ menu and "Install app" or "Add to home screen".<br><strong>iPhone (Safari):</strong> tap Share and "Add to Home Screen".',
  summary='Each list is visible only to the people invited. The owner can remove members or delete the list, and each member can leave the list at any time.',
  contact='Contact',
 ),
 'es': dict(
  lang='es', og='es_ES', path=BASE+'es/', back='← FLR Sistemas', home='/es/',
  title='Lista de Compras — FLR Sistemas',
  desc='Listas de compras compartidas en tiempo real, con precio de los artículos y total de la lista. Funciona en el navegador y se instala en el celular.',
  lead='Hagan las compras juntos: listas compartidas que se actualizan en tiempo real.',
  open='Abrir la app', how='Cómo funciona',
  note='App web (PWA) para quien comparte las compras del hogar. Funciona en el navegador y se instala en el celular, sin tienda de aplicaciones. La app viene en inglés, portugués y español. Puedes usarla sin cuenta (las listas quedan solo en tu dispositivo).',
  h_what='Qué hace',
  what='Crea una lista, invita por correo a quienes compran contigo y listo: cada artículo marcado, agregado o eliminado aparece al instante para todos. Anota el precio unitario de cada artículo y mira cuánto va a costar la compra.',
  cards=[
   ('Comparte por correo','Invita a familiares o amigos con el correo de su cuenta. Solo quien fue invitado ve la lista.'),
   ('Tiempo real','¿Marcaste la leche como comprada? Todos lo ven al instante, sin recargar la página.'),
   ('Carrito y total','Indica el precio unitario: la app lo multiplica por la cantidad y muestra, arriba de la lista, lo que ya está en el carrito y el total. El total de cada lista aparece en las tarjetas de la pantalla inicial.'),
   ('Por categoría','Los artículos se agrupan en Frutas y verduras, Carnicería, Panadería y más, y la app sugiere la categoría por el nombre.'),
   ('Úsala sin señal','En el supermercado sin señal, ves la última versión de la lista y sigues usándola: marcas, agregas, editas y quitas artículos, creas, renombras y eliminas listas, y todo se envía cuando vuelve la señal.'),
   ('Se instala como app','Agrégala a la pantalla de inicio del celular y ábrela como cualquier otra aplicación.'),
  ],
  h_how='Cómo funciona', how_id='how',
  steps=[
   ('Crea tu cuenta','Regístrate con nombre, correo y una contraseña de al menos 8 caracteres, con letras y números. Confirma el correo que recibas e inicia sesión.'),
   ('Crea una lista','Ponle un nombre, como "Compra del mes", y toca "Crear".'),
   ('Agrega los artículos','Escribe el nombre y, si quieres, la cantidad y el precio. La categoría se sugiere sola y puedes cambiarla.'),
   ('Comparte','Toca el ícono de personas, escribe el correo de quien va a participar y toca "Compartir". Esa persona ya debe tener una cuenta.'),
  ],
  h_install='Instalar en el celular',
  install='<strong>Android (Chrome):</strong> abre la app, toca el menú ⋮ y "Instalar app" o "Añadir a la pantalla de inicio".<br><strong>iPhone (Safari):</strong> toca Compartir y "Añadir a pantalla de inicio".',
  summary='Cada lista solo es visible para quienes fueron invitados. El dueño puede quitar participantes o eliminar la lista, y cada participante puede salir de la lista cuando quiera.',
  contact='Contacto',
 ),
}


SH = {
 'pt': ('Como ele é', 'Telas do app com dados de exemplo.', ['Suas listas, com o total de cada uma', 'Itens por categoria, com preço', 'Compartilhando com quem vai comprar junto'],
        ['Tela com as listas de compras e o total de cada uma.', 'Tela de uma lista com itens por categoria, preços e o total da lista.', 'Janela para compartilhar a lista por e-mail e ver os participantes.']),
 'en': ('What it looks like', 'App screens with sample data.', ["Your lists, with each one's total", 'Items by category, with prices', 'Sharing with whoever shops with you'],
        ["Screen with the shopping lists and each list's total.", 'A list screen with items by category, prices and the list total.', 'Dialog for sharing the list by e-mail and seeing its members.']),
 'es': ('Cómo se ve', 'Pantallas de la app con datos de ejemplo.', ['Tus listas, con el total de cada una', 'Artículos por categoría, con precio', 'Compartiendo con quien compra contigo'],
        ['Pantalla con las listas de compras y el total de cada una.', 'Pantalla de una lista con artículos por categoría, precios y el total de la lista.', 'Ventana para compartir la lista por correo y ver los participantes.']),
}
IMGS = ['lista-listas', 'lista-itens', 'lista-compartilhar']


def shots_html(code):
    h, note, caps, alts = SH[code]
    fig = ('      <figure>\n        <img src="/listadecompras/sobre/img/%s-%s.png" width="1000" height="2260" loading="lazy"\n'
           '             alt="%s">\n        <figcaption>%s</figcaption>\n      </figure>')
    figs = '\n'.join(fig % (i, code, a, c) for i, c, a in zip(IMGS, caps, alts))
    return ('    <h3 class="section">%s</h3>\n    <p class="note" style="margin:0 0 10px">%s</p>\n'
            '    <div class="shots">\n%s\n    </div>\n') % (h, note, figs)


AJ = {'pt': '/listadecompras/ajuda/', 'en': '/listadecompras/ajuda/en/', 'es': '/listadecompras/ajuda/es/'}
HW = {'pt': 'Ajuda', 'en': 'Help', 'es': 'Ayuda'}


def page(code):
    t = T[code]
    langs = ''.join(
        '<a href="%s" lang="%s" hreflang="%s"%s onclick="try{localStorage.setItem(\'lang\',\'%s\')}catch(e){}">%s</a>'
        % (T[c]['path'], c, c, ' aria-current="page"' if c == code else '', c, c.upper())
        for c in ('pt', 'en', 'es'))
    cards = '\n'.join('      <div class="card">\n        <h4>%s</h4>\n        <p>%s</p>\n      </div>' % c for c in t['cards'])
    steps = '\n'.join('      <li>\n        <h4>%s</h4>\n        <p>%s</p>\n      </li>' % s for s in t['steps'])
    script = ''
    if code == 'pt':
        script = ("<script>\n"
                  "  /* Escolha automatica de idioma, so na primeira visita e so na pagina padrao (pt). */\n"
                  "  (function () {\n    try {\n"
                  "      var salvo = localStorage.getItem('lang');\n"
                  "      var l = salvo || String((navigator.languages && navigator.languages[0]) || navigator.language || 'pt').slice(0, 2).toLowerCase();\n"
                  "      if (l !== 'pt') location.replace('%s' + (l === 'es' ? 'es' : 'en') + '/');\n"
                  "    } catch (e) {}\n  })();\n</script>\n" % BASE)
    hl = ''.join('<link rel="alternate" hreflang="%s" href="https://flrsistemas.com.br%s">\n' % (c, T[c]['path']) for c in ('pt', 'en', 'es'))
    return f'''<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="https://flrsistemas.com.br{t['path']}">
{hl}<link rel="alternate" hreflang="x-default" href="https://flrsistemas.com.br{BASE}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="FLR Sistemas">
<meta property="og:locale" content="{t['og']}">
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{t['desc']}">
<meta property="og:url" content="https://flrsistemas.com.br{t['path']}">
{ICONS_HTML}<style>{CSS}</style>
{script}</head>
<body>
<main>

  <header class="site topbar">
    <a class="back" href="{t['home']}">{t['back']}</a>
    <nav class="langs" aria-label="Language">{langs}</nav>
  </header>

  <article class="app" id="listadecompras">
    <h2>Lista de Compras</h2>
    <p class="lead">{t['lead']}</p>

    <div class="actions">
      <a class="button" href="/listadecompras/">{t['open']}</a>
      <a class="link" href="#{t['how_id']}">{t['how']}</a>
      <a class="link" href="{AJ[code]}">{HW[code]}</a>
    </div>
    <p class="note">{t['note']}</p>

    <h3 class="section">{t['h_what']}</h3>
    <p>{t['what']}</p>

    <div class="grid" style="margin-top:18px">
{cards}
    </div>

{shots_html(code)}
    <h3 class="section" id="{t['how_id']}">{t['h_how']}</h3>
    <ol class="steps">
{steps}
    </ol>

    <h3 class="section">{t['h_install']}</h3>
    <p>{t['install']}</p>

    <div class="summary" style="margin-top:28px">
      <p>{t['summary']}</p>
    </div>
  </article>

  <footer>
    <p>
      FLR Sistemas<br>
      {t['contact']}: <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a>
    </p>
  </footer>

</main>
</body>
</html>
'''


for code, sub in (('pt', ''), ('en', 'en'), ('es', 'es')):
    d = os.path.join(ROOT, sub) if sub else ROOT
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(page(code))
print('ok')
