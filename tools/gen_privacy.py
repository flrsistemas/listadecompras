import os, re

ICONS_HTML = '<link rel="icon" href="/listadecompras/icons/icon.svg" type="image/svg+xml">\n<link rel="icon" href="/listadecompras/icons/favicon-32.png" sizes="32x32" type="image/png">\n<link rel="apple-touch-icon" href="/listadecompras/icons/apple-touch-icon.png">\n<meta name="theme-color" content="#16a34a">\n'

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import APP, SITE
EMAIL = 'contato@flrsistemas.com.br'
FILES = {'pt': 'privacy.html', 'en': 'privacy-en.html', 'es': 'privacy-es.html'}
URL = {k: '/listadecompras/' + v for k, v in FILES.items()}

CSS = """
  :root {
    --bg: #F4FAF6;
    --surface: #FFFFFF;
    --text: #1F2D25;
    --muted: #55695D;
    --border: #D5E4DA;
    --accent: #16A34A;
    --accent-bg: #E8F6EE;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #14201A;
      --surface: #1B2B22;
      --text: #E9F2EC;
      --muted: #A9BDB0;
      --border: #2D4336;
      --accent: #4ADE80;
      --accent-bg: #1D3A2A;
    }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 32px 16px 72px;
    background: var(--bg);
    color: var(--text);
    font: 16px/1.65 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  }
  main { max-width: 680px; margin: 0 auto; }
  h1 { font-size: 1.75rem; line-height: 1.25; margin: 0 0 4px; }
  h2 {
    font-size: 1.15rem;
    margin: 40px 0 12px;
    padding-top: 20px;
    border-top: 1px solid var(--border);
  }
  h2:first-of-type { border-top: 0; padding-top: 0; }
  .sub { color: var(--muted); font-size: .92rem; margin: 0 0 28px; }
  .langs { color: var(--muted); font-size: .88rem; margin: 0 0 18px; }
  .summary {
    background: var(--accent-bg);
    border-left: 4px solid var(--accent);
    border-radius: 0 10px 10px 0;
    padding: 16px 18px;
    margin: 0 0 8px;
  }
  .summary p { margin: 0; }
  .summary strong { font-size: 1.05rem; }
  ul { padding-left: 22px; }
  li { margin: 6px 0; }
  table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: .95rem; }
  th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--border); vertical-align: top; }
  th { color: var(--muted); font-weight: 600; font-size: .85rem; text-transform: uppercase; letter-spacing: .03em; }
  a { color: inherit; text-decoration-color: var(--accent); text-underline-offset: 3px; }
  footer { margin-top: 48px; padding-top: 20px; border-top: 1px solid var(--border); color: var(--muted); font-size: .88rem; }
"""

L = {}

L['pt'] = dict(
 lang='pt', title='Política de privacidade — Lista de Compras',
 desc='Política de privacidade do app Lista de Compras, da FLR Sistemas.',
 h1='Política de privacidade',
 sub='App <strong>Lista de Compras</strong> &middot; FLR Sistemas &middot; Em vigor desde 18 de novembro de 2026',
 summary_t='O Lista de Compras guarda só o necessário para funcionar.',
 summary_p='Seu nome, seu e-mail e as listas que você cria. Não há anúncios, nem rastreamento, nem venda de dados. Só as pessoas que você convida veem as suas listas.',
 sections=[
  ('Quem somos', """<p>O Lista de Compras é desenvolvido e mantido pela <strong>FLR Sistemas</strong>. Para qualquer dúvida sobre esta política, escreva para <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a>.</p>"""),
  ('Os dados que coletamos', """<p>Para o app funcionar, precisamos de uma conta e do conteúdo que você cria nela:</p>
  <table>
    <tr><th>Dado</th><th>Para que serve</th></tr>
    <tr><td>Nome</td><td>Aparece para você e para os participantes das suas listas.</td></tr>
    <tr><td>E-mail</td><td>Entrar no app, confirmar o cadastro e receber convites para listas.</td></tr>
    <tr><td>Senha</td><td>Autenticação. É guardada de forma criptografada, e nós não conseguimos ler.</td></tr>
    <tr><td>Listas, itens, quantidades, preços e categorias</td><td>O conteúdo que você escreve, mostrado a você e aos participantes de cada lista.</td></tr>
    <tr><td>Participantes de cada lista</td><td>Controlar quem pode ver e editar cada lista.</td></tr>
  </table>"""),
  ('O que o app não faz', """<ul>
    <li>Não mostra anúncios e não usa identificador de publicidade.</li>
    <li>Não usa ferramentas de análise de uso, estatísticas nem rastreamento.</li>
    <li>Não acessa seus contatos, fotos, câmera, microfone, localização ou arquivos.</li>
    <li>Não coleta dados de pagamento.</li>
    <li>Não vende, aluga nem compartilha seus dados para fins de publicidade.</li>
  </ul>"""),
  ('Quem vê as suas listas', """<p>Quem você convida pelo e-mail passa a ver os itens, os preços e o nome e o e-mail dos outros participantes dessa lista. Quem não participa da lista não vê nada: o banco de dados tem regras de acesso que garantem isso. O dono pode remover participantes ou excluir a lista, e cada participante pode sair dela quando quiser.</p>"""),
  ('Serviços de terceiros', """<p>O app usa três serviços para funcionar:</p>
  <table>
    <tr><th>Serviço</th><th>Função</th><th>O que recebe</th></tr>
    <tr><td>Supabase</td><td>Guarda a conta e as listas, cuida do login e envia o e-mail de confirmação.</td><td>Os dados da tabela acima. Os servidores podem ficar fora do Brasil.</td></tr>
    <tr><td>GitHub Pages</td><td>Hospeda o site e o app.</td><td>O endereço IP de quem acessa, como em qualquer site.</td></tr>
    <tr><td>jsDelivr</td><td>Entrega uma biblioteca de código usada pelo app.</td><td>O endereço IP de quem acessa.</td></tr>
  </table>
  <p>Cada um segue a sua própria política de privacidade.</p>"""),
  ('Dados guardados no seu aparelho', """<p>O app guarda no navegador do seu aparelho a sua sessão de login, o idioma que você escolheu e uma cópia das suas listas, itens e totais, para você consultar mesmo sem internet, e as alterações nos itens que ainda não foram enviadas por falta de sinal (marcações, itens e listas novos, edições e remoções). Ao sair da conta ou limpar os dados do navegador, essa cópia deixa de existir no aparelho. No modo sem conta, as suas listas ficam apenas neste aparelho, sem nenhum envio para os nossos servidores, e são perdidas se você limpar esses dados.</p>"""),
  ('Por quanto tempo guardamos', """<p>Mantemos os dados enquanto a sua conta existir. Quando uma lista é excluída, os itens dela são apagados para todos os participantes. Você pode pedir a exclusão da conta e dos dados a qualquer momento.</p>"""),
  ('Segurança', """<p>A conexão é protegida por HTTPS, as senhas são guardadas de forma criptografada e cada pessoa só consegue ler as listas de que participa. Nenhum sistema é 100% seguro, mas cuidamos para reduzir o risco.</p>"""),
  ('Crianças', """<p>O Lista de Compras não é direcionado a crianças.</p>"""),
  ('Seus direitos', """<p>A Lei Geral de Proteção de Dados (LGPD, Lei 13.709/2018) garante a você o direito de confirmar que tratamos seus dados, acessá-los, corrigi-los, pedir a exclusão e a portabilidade. Dentro do app você vê e edita as suas listas a qualquer momento. Para os demais pedidos, ou para excluir a sua conta, escreva para <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a>, do e-mail cadastrado. Respondemos para o mesmo e-mail.</p>"""),
  ('Mudanças nesta política', """<p>Se o app passar a tratar dados de um jeito novo, esta página será atualizada antes da mudança valer, e a data no topo vai mudar.</p>"""),
 ],
 footer='Lista de Compras &middot; FLR Sistemas<br>\n    Contato: <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a><br>\n    Última atualização: 18 de novembro de 2026',
 back='← Voltar ao app', backurl='/listadecompras/',
)

L['en'] = dict(
 lang='en', title='Privacy Policy — Lista de Compras',
 desc='Privacy policy for the Lista de Compras app, by FLR Sistemas.',
 h1='Privacy Policy',
 sub='<strong>Lista de Compras</strong> app &middot; FLR Sistemas &middot; Effective November 18, 2026',
 summary_t='Lista de Compras keeps only what it needs to work.',
 summary_p='Your name, your e-mail and the lists you create. There are no ads, no tracking and no selling of data. Only the people you invite can see your lists.',
 sections=[
  ('Who we are', """<p>Lista de Compras is developed and maintained by <strong>FLR Sistemas</strong>. For any question about this policy, write to <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a>.</p>"""),
  ('The data we collect', """<p>For the app to work, we need an account and the content you create in it:</p>
  <table>
    <tr><th>Data</th><th>What it is for</th></tr>
    <tr><td>Name</td><td>Shown to you and to the people in your lists.</td></tr>
    <tr><td>E-mail</td><td>Signing in, confirming sign-up and receiving list invitations.</td></tr>
    <tr><td>Password</td><td>Authentication. It is stored encrypted, and we cannot read it.</td></tr>
    <tr><td>Lists, items, quantities, prices and categories</td><td>The content you write, shown to you and to the members of each list.</td></tr>
    <tr><td>Members of each list</td><td>Controlling who can see and edit each list.</td></tr>
  </table>"""),
  ('What the app does not do', """<ul>
    <li>It shows no advertising and uses no advertising identifier.</li>
    <li>It uses no analytics, usage statistics or tracking.</li>
    <li>It does not access your contacts, photos, camera, microphone, location or files.</li>
    <li>It does not collect payment data.</li>
    <li>It does not sell, rent or share your data for advertising.</li>
  </ul>"""),
  ('Who sees your lists', """<p>People you invite by e-mail can see the items, the prices and the name and e-mail of the other members of that list. People who are not in the list see nothing: access rules in the database ensure this. The owner can remove members or delete the list, and each member can leave at any time.</p>"""),
  ('Third-party services', """<p>The app uses three services to work:</p>
  <table>
    <tr><th>Service</th><th>Role</th><th>What it receives</th></tr>
    <tr><td>Supabase</td><td>Stores the account and lists, handles sign-in and sends the confirmation e-mail.</td><td>The data in the table above. Its servers may be located outside Brazil.</td></tr>
    <tr><td>GitHub Pages</td><td>Hosts the site and the app.</td><td>Visitors' IP address, as with any website.</td></tr>
    <tr><td>jsDelivr</td><td>Delivers a code library used by the app.</td><td>Visitors' IP address.</td></tr>
  </table>
  <p>Each follows its own privacy policy.</p>"""),
  ('Data kept on your device', """<p>The app keeps in your device's browser your sign-in session, the language you chose and a copy of your lists, items and totals, so you can view them without internet, and the item changes not yet sent because of no signal (check marks, new items and lists, edits and removals). When you sign out or clear the browser data, that copy is removed from the device. In the no-account mode, your lists stay only on this device, with nothing sent to our servers, and they are lost if you clear that data.</p>"""),
  ('How long we keep it', """<p>We keep the data while your account exists. When a list is deleted, its items are deleted for every member. You can ask for your account and data to be deleted at any time.</p>"""),
  ('Security', """<p>The connection is protected by HTTPS, passwords are stored encrypted, and each person can read only the lists they take part in. No system is 100% secure, but we take care to reduce the risk.</p>"""),
  ('Children', """<p>Lista de Compras is not directed at children.</p>"""),
  ('Your rights', """<p>Brazil's General Data Protection Law (LGPD, Law 13.709/2018), and similar laws elsewhere, give you the right to confirm that we process your data, access it, correct it, ask for its deletion and portability. Inside the app you can see and edit your lists at any time. For other requests, or to delete your account, write to <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a> from the registered e-mail. We reply to the same address.</p>"""),
  ('Changes to this policy', """<p>If the app ever begins handling data in a new way, this page will be updated before the change goes live, and the date at the top will change.</p>"""),
 ],
 footer='Lista de Compras &middot; FLR Sistemas<br>\n    Contact: <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a><br>\n    Last updated: November 18, 2026',
 back='← Back to the app', backurl='/listadecompras/',
)

L['es'] = dict(
 lang='es', title='Política de privacidad — Lista de Compras',
 desc='Política de privacidad de la app Lista de Compras, de FLR Sistemas.',
 h1='Política de privacidad',
 sub='App <strong>Lista de Compras</strong> &middot; FLR Sistemas &middot; En vigor desde el 18 de noviembre de 2026',
 summary_t='Lista de Compras guarda solo lo necesario para funcionar.',
 summary_p='Tu nombre, tu correo y las listas que creas. No hay anuncios, ni rastreo, ni venta de datos. Solo las personas que invitas ven tus listas.',
 sections=[
  ('Quiénes somos', """<p>Lista de Compras es desarrollada y mantenida por <strong>FLR Sistemas</strong>. Para cualquier duda sobre esta política, escribe a <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a>.</p>"""),
  ('Los datos que recopilamos', """<p>Para que la app funcione, necesitamos una cuenta y el contenido que creas en ella:</p>
  <table>
    <tr><th>Dato</th><th>Para qué sirve</th></tr>
    <tr><td>Nombre</td><td>Se muestra a ti y a los participantes de tus listas.</td></tr>
    <tr><td>Correo</td><td>Iniciar sesión, confirmar el registro y recibir invitaciones a listas.</td></tr>
    <tr><td>Contraseña</td><td>Autenticación. Se guarda cifrada y nosotros no podemos leerla.</td></tr>
    <tr><td>Listas, artículos, cantidades, precios y categorías</td><td>El contenido que escribes, mostrado a ti y a los participantes de cada lista.</td></tr>
    <tr><td>Participantes de cada lista</td><td>Controlar quién puede ver y editar cada lista.</td></tr>
  </table>"""),
  ('Lo que la app no hace', """<ul>
    <li>No muestra anuncios y no usa identificador de publicidad.</li>
    <li>No usa herramientas de análisis de uso, estadísticas ni rastreo.</li>
    <li>No accede a tus contactos, fotos, cámara, micrófono, ubicación ni archivos.</li>
    <li>No recopila datos de pago.</li>
    <li>No vende, alquila ni comparte tus datos con fines publicitarios.</li>
  </ul>"""),
  ('Quién ve tus listas', """<p>Quien invitas por correo pasa a ver los artículos, los precios y el nombre y el correo de los demás participantes de esa lista. Quien no participa en la lista no ve nada: las reglas de acceso de la base de datos lo garantizan. El dueño puede quitar participantes o eliminar la lista, y cada participante puede salir de ella cuando quiera.</p>"""),
  ('Servicios de terceros', """<p>La app usa tres servicios para funcionar:</p>
  <table>
    <tr><th>Servicio</th><th>Función</th><th>Qué recibe</th></tr>
    <tr><td>Supabase</td><td>Guarda la cuenta y las listas, gestiona el inicio de sesión y envía el correo de confirmación.</td><td>Los datos de la tabla anterior. Sus servidores pueden estar fuera de Brasil.</td></tr>
    <tr><td>GitHub Pages</td><td>Aloja el sitio y la app.</td><td>La dirección IP de quien accede, como en cualquier sitio web.</td></tr>
    <tr><td>jsDelivr</td><td>Entrega una biblioteca de código que usa la app.</td><td>La dirección IP de quien accede.</td></tr>
  </table>
  <p>Cada uno sigue su propia política de privacidad.</p>"""),
  ('Datos guardados en tu dispositivo', """<p>La app guarda en el navegador de tu dispositivo tu sesión de inicio, el idioma que elegiste y una copia de tus listas, artículos y totales, para que puedas consultarlos sin internet, y los cambios en los artículos aún no enviados por falta de señal (marcas, artículos y listas nuevos, ediciones y eliminaciones). Al cerrar sesión o borrar los datos del navegador, esa copia deja de existir en el dispositivo. En el modo sin cuenta, tus listas quedan solo en este dispositivo, sin ningún envío a nuestros servidores, y se pierden si borras esos datos.</p>"""),
  ('Por cuánto tiempo los guardamos', """<p>Mantenemos los datos mientras tu cuenta exista. Cuando se elimina una lista, sus artículos se borran para todos los participantes. Puedes pedir la eliminación de la cuenta y de los datos en cualquier momento.</p>"""),
  ('Seguridad', """<p>La conexión está protegida por HTTPS, las contraseñas se guardan cifradas y cada persona solo puede leer las listas en las que participa. Ningún sistema es 100% seguro, pero cuidamos de reducir el riesgo.</p>"""),
  ('Niños', """<p>Lista de Compras no está dirigida a niños.</p>"""),
  ('Tus derechos', """<p>La Ley General de Protección de Datos de Brasil (LGPD, Ley 13.709/2018) te garantiza el derecho de confirmar que tratamos tus datos, acceder a ellos, corregirlos, pedir su eliminación y su portabilidad. Dentro de la app ves y editas tus listas en cualquier momento. Para otras solicitudes, o para eliminar tu cuenta, escribe a <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a> desde el correo registrado. Respondemos al mismo correo.</p>"""),
  ('Cambios en esta política', """<p>Si la app pasa a tratar datos de una forma nueva, esta página se actualizará antes de que el cambio entre en vigor, y la fecha de arriba cambiará.</p>"""),
 ],
 footer='Lista de Compras &middot; FLR Sistemas<br>\n    Contacto: <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a><br>\n    Última actualización: 18 de noviembre de 2026',
 back='← Volver a la app', backurl='/listadecompras/',
)


def page(code):
    t = L[code]
    langs = ' &middot; '.join(
        ('<strong>%s</strong>' % c.upper()) if c == code else '<a href="%s" hreflang="%s">%s</a>' % (URL[c], c, c.upper())
        for c in ('pt', 'en', 'es'))
    secs = '\n'.join('  <h2>%s</h2>\n  %s\n' % (h, b) for h, b in t['sections'])
    alts = ''.join('<link rel="alternate" hreflang="%s" href="https://flrsistemas.com.br%s">\n' % (c, URL[c]) for c in ('pt', 'en', 'es'))
    return f'''<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="https://flrsistemas.com.br{URL[code]}">
{ICONS_HTML}{alts}<style>{CSS}</style>
</head>
<body>
<main>
  <p class="langs"><a href="{t['backurl']}">{t['back']}</a> &middot; {langs}</p>
  <h1>{t['h1']}</h1>
  <p class="sub">{t['sub']}</p>

  <div class="summary">
    <p><strong>{t['summary_t']}</strong></p>
    <p style="margin-top:8px">{t['summary_p']}</p>
  </div>

{secs}
  <footer>
    <p>{t['footer']}</p>
  </footer>
</main>
</body>
</html>
'''


for code, fn in FILES.items():
    with open(os.path.join(APP, fn), 'w', encoding='utf-8', newline='\n') as f:
        f.write(page(code))

print('ok')
