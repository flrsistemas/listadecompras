import os, re

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import PC_DOCS as DOCS
FILES = {'pt': 'privacy.html', 'en': 'privacy-en.html', 'es': 'privacy-es.html'}
URL = {k: '/precocerto/' + v for k, v in FILES.items()}
PAGE = {'pt': '/precocerto/', 'en': '/precocerto/en/', 'es': '/precocerto/es/'}
MAIL = '<a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a>'

# CSS e links de icone da pagina atual (mantem o visual do Preco Certo)
cur = open(os.path.join(DOCS, 'privacy.html'), encoding='utf-8', newline='').read().replace('\r\n', '\n')
STYLE = re.search(r'<style>.*?</style>', cur, re.S).group(0)
if '.langs' not in STYLE:
    STYLE = STYLE.replace('</style>', '  .langs { color: var(--muted); font-size: .88rem; margin: 0 0 18px; }\n</style>')
ICONS = ('<link rel="icon" href="/precocerto/icon.svg" type="image/svg+xml">\n'
         '<link rel="icon" href="/precocerto/favicon-32.png" sizes="32x32" type="image/png">\n'
         '<link rel="apple-touch-icon" href="/precocerto/apple-touch-icon.png">\n'
         '<meta name="theme-color" content="#B85463">\n')

T = {}
T['pt'] = dict(
    lang='pt-BR', title='Política de Privacidade — Preço Certo',
    desc='Política de privacidade do app Preço Certo. O app não coleta dados pessoais.',
    back='← Página do app', h1='Política de Privacidade',
    sub='App <strong>Preço Certo</strong> &middot; FLR Sistemas &middot; Em vigor desde 17 de setembro de 2026',
    summary_t='O Preço Certo não coleta nenhum dado pessoal.',
    summary_p='Não há servidor, cadastro, login nem conta. Suas receitas, seus ingredientes e seus preços ficam guardados apenas no seu celular, e nós não temos como vê-los.',
    body=f'''  <h2>Quem somos</h2>
  <p>O Preço Certo é desenvolvido e mantido pela <strong>FLR Sistemas</strong>.
  Para qualquer dúvida sobre esta política, escreva para
  {MAIL}.</p>

  <h2>Os dados que você cria no app</h2>
  <p>Ao usar o Preço Certo, você registra informações sobre o seu negócio: nomes de
  receitas, ingredientes, embalagens, preços de compra, tempo de preparo, margem de
  lucro e observações de preparo.</p>
  <p>Todo esse conteúdo é gravado <strong>apenas no armazenamento privado do app,
  dentro do seu aparelho</strong>. Ele nunca é enviado a nenhum servidor, nem nosso nem
  de terceiros. Nós não conseguimos acessá-lo, não conseguimos recuperá-lo e não
  guardamos nenhuma cópia.</p>

  <h2>O que o app não faz</h2>
  <ul>
    <li>Não pede cadastro, login, e-mail, telefone nem qualquer identificador.</li>
    <li>Não usa análise de uso, estatísticas nem rastreamento de nenhum tipo.</li>
    <li>Não exibe anúncios nem usa identificador de publicidade.</li>
    <li>Não acessa seus contatos, fotos, câmera, microfone, localização nem arquivos.</li>
    <li>Não vende, aluga nem compartilha dados com ninguém, porque não guarda nenhum.</li>
  </ul>

  <h2>Backup do Android</h2>
  <p>O Android oferece um serviço de backup automático que copia os dados dos apps para
  o Google Drive do próprio usuário. Se esse serviço estiver ativado no seu aparelho,
  <strong>o arquivo com as suas receitas será copiado para o seu Google
  Drive</strong> e restaurado quando você reinstalar o app ou trocar de celular.</p>
  <p>Vale ser preciso sobre o que isso significa: essa cópia fica na
  <strong>sua</strong> conta Google, sob as políticas do próprio Google, e existe para que
  você não perca o seu trabalho. <strong>Nós não temos acesso a ela.</strong></p>
  <p>Você pode desativar o backup, ou apagar uma cópia existente, nas configurações do
  aparelho, em <em>Google &rsaquo; Backup</em>. A sua licença Pro não está incluída
  nesse backup.</p>

  <h2>Compra da versão Pro</h2>
  <p>A versão Pro é uma compra única, processada inteiramente pelo
  <strong>Google Play</strong>. Os dados de pagamento são tratados pelo Google, conforme a
  política de privacidade dele: nós nunca vemos, recebemos nem guardamos números de
  cartão, endereços ou dados bancários.</p>
  <p>O app guarda apenas um registro local, no seu aparelho, de que a compra foi feita,
  para liberar os recursos pagos sem precisar consultar a internet toda vez.</p>

  <h2>Permissões</h2>
  <table>
    <tr><th>Permissão</th><th>Para que serve</th></tr>
    <tr>
      <td><code>INTERNET</code></td>
      <td>Usada apenas pelo sistema de compras do Google Play, para confirmar a compra do
      Pro. Nenhuma informação sobre você é enviada por ela.</td>
    </tr>
  </table>
  <p>O app funciona normalmente sem conexão. Você pode usá-lo em modo avião o dia
  inteiro.</p>

  <h2>Crianças</h2>
  <p>O Preço Certo é uma ferramenta profissional para o trabalho de confeitaria e
  padaria e não é direcionado a crianças. Como não coleta nenhum dado, também não coleta
  dados de crianças.</p>

  <h2>Seus direitos</h2>
  <p>A Lei Geral de Proteção de Dados (LGPD, Lei 13.709/2018), e leis semelhantes em
  outros países, dão a você o direito de acessar, corrigir e apagar os seus dados
  pessoais. No Preço Certo esses direitos são exercidos no próprio aparelho, porque é
  lá que está tudo:</p>
  <ul>
    <li><strong>Acessar e corrigir:</strong> todo o conteúdo fica visível e editável
    dentro do app a qualquer momento.</li>
    <li><strong>Apagar:</strong> apagar um item dentro do app o remove de forma
    definitiva. Desinstalar o app apaga tudo de uma vez.</li>
    <li><strong>Backup:</strong> se você usa o backup do Android, lembre-se de apagar
    também a cópia no seu Google Drive, pelas configurações do aparelho.</li>
  </ul>
  <p>Não temos um banco de dados de usuários para consultar ou apagar sob pedido. Mesmo
  assim, se tiver qualquer dúvida sobre isso, escreva para
  {MAIL}.</p>

  <h2>Mudanças nesta política</h2>
  <p>Se o app passar a tratar dados de um jeito novo, esta página será atualizada antes
  de a mudança entrar no ar, e a data de vigência no topo vai mudar. Vale reler depois de
  uma atualização importante.</p>''',
    footer=f'Preço Certo &middot; FLR Sistemas<br>\n    Contato: {MAIL}<br>\n    Última atualização: 17 de setembro de 2026')

T['en'] = dict(
    lang='en', title='Privacy Policy — Preço Certo',
    desc='Privacy policy for the Preço Certo app. The app collects no personal data.',
    back='← App page', h1='Privacy Policy',
    sub='<strong>Preço Certo</strong> app &middot; FLR Sistemas &middot; Effective September 17, 2026',
    summary_t='Preço Certo collects no personal data.',
    summary_p="There is no server, no sign-up, no login and no account. Your recipes, your ingredients and your prices are stored only on your phone, and we have no way of seeing them.",
    body=f'''  <h2>Who we are</h2>
  <p>Preço Certo is developed and maintained by <strong>FLR Sistemas</strong>.
  For any question about this policy, write to
  {MAIL}.</p>

  <h2>The data you create in the app</h2>
  <p>As you use Preço Certo you enter information about your business: recipe
  names, ingredients, packaging, purchase prices, preparation time, profit
  margin and preparation notes.</p>
  <p>All of that content is written <strong>only to the app's private storage,
  inside your device</strong>. It is never sent to any server, ours or anyone
  else's. We cannot access it, we cannot recover it, and we keep no copy of it.</p>

  <h2>What the app does not do</h2>
  <ul>
    <li>It does not ask for a sign-up, login, email, phone number or any identifier.</li>
    <li>It uses no analytics, usage statistics or tracking of any kind.</li>
    <li>It shows no advertising and uses no advertising identifier.</li>
    <li>It does not access your contacts, photos, camera, microphone, location or files.</li>
    <li>It does not sell, rent or share data with anyone &mdash; because it holds none.</li>
  </ul>

  <h2>Android backup</h2>
  <p>Android offers an automatic backup service that copies app data to the
  user's own Google Drive. If that service is turned on for your device,
  <strong>the file containing your recipes will be copied to your Google
  Drive</strong> and restored when you reinstall the app or move to a new phone.</p>
  <p>It is worth being precise about what this means: that copy lives in
  <strong>your</strong> Google account, under Google's own policies, and exists so
  that you do not lose your work. <strong>We have no access to it.</strong></p>
  <p>You can turn the backup off, or delete an existing copy, in your device
  settings under <em>Google &rsaquo; Backup</em>. Your Pro licence is not included
  in that backup.</p>

  <h2>Buying the Pro version</h2>
  <p>The Pro version is a one-time purchase, processed entirely by
  <strong>Google Play</strong>. Payment details are handled by Google under its
  own privacy policy &mdash; we never see, receive or store card numbers, addresses or
  banking information.</p>
  <p>The app stores only a local record on your device that the purchase was
  made, so that it can unlock the paid features without having to check the
  internet every time.</p>

  <h2>Permissions</h2>
  <table>
    <tr><th>Permission</th><th>What it is for</th></tr>
    <tr>
      <td><code>INTERNET</code></td>
      <td>Used only by Google Play's purchase system, to confirm the Pro
      purchase. No information about you is sent through it.</td>
    </tr>
  </table>
  <p>The app works normally with no connection. You can use it in airplane mode
  all day.</p>

  <h2>Children</h2>
  <p>Preço Certo is a professional tool for confectionery and bakery work and is
  not directed at children. Since it collects no data at all, it also collects no
  data from children.</p>

  <h2>Your rights</h2>
  <p>Brazil's General Data Protection Law (LGPD, Law 13.709/2018), and similar
  laws elsewhere, give you the right to access, correct and delete your personal
  data. With Preço Certo those rights are exercised on the device itself, because
  that is where everything is:</p>
  <ul>
    <li><strong>Access and correct:</strong> all content is visible and editable
    inside the app at any time.</li>
    <li><strong>Delete:</strong> deleting an item inside the app removes it
    permanently. Uninstalling the app erases everything at once.</li>
    <li><strong>Backup:</strong> if you use Android backup, remember to delete
    the copy in your Google Drive as well, through your device settings.</li>
  </ul>
  <p>We hold no user database to query or erase on request. Even so, if you have
  any question about this, write to
  {MAIL}.</p>

  <h2>Changes to this policy</h2>
  <p>If the app ever begins handling data in a new way, this page will be updated
  before that change goes live, and the effective date at the top will change.
  It is worth re-reading after a major update.</p>''',
    footer=f'Preço Certo &middot; FLR Sistemas<br>\n    Contact: {MAIL}<br>\n    Last updated: September 17, 2026')

T['es'] = dict(
    lang='es', title='Política de Privacidad — Preço Certo',
    desc='Política de privacidad de la app Preço Certo. La app no recopila datos personales.',
    back='← Página de la app', h1='Política de Privacidad',
    sub='App <strong>Preço Certo</strong> &middot; FLR Sistemas &middot; En vigor desde el 17 de septiembre de 2026',
    summary_t='Preço Certo no recopila ningún dato personal.',
    summary_p='No hay servidor, registro, inicio de sesión ni cuenta. Tus recetas, tus ingredientes y tus precios se guardan solo en tu celular, y nosotros no tenemos forma de verlos.',
    body=f'''  <h2>Quiénes somos</h2>
  <p>Preço Certo es desarrollada y mantenida por <strong>FLR Sistemas</strong>.
  Para cualquier duda sobre esta política, escribe a
  {MAIL}.</p>

  <h2>Los datos que creas en la app</h2>
  <p>Al usar Preço Certo registras información sobre tu negocio: nombres de recetas,
  ingredientes, envases, precios de compra, tiempo de preparación, margen de ganancia
  y notas de preparación.</p>
  <p>Todo ese contenido se escribe <strong>solo en el almacenamiento privado de la app,
  dentro de tu dispositivo</strong>. Nunca se envía a ningún servidor, ni nuestro ni de
  terceros. No podemos acceder a él, no podemos recuperarlo y no guardamos ninguna
  copia.</p>

  <h2>Lo que la app no hace</h2>
  <ul>
    <li>No pide registro, inicio de sesión, correo, teléfono ni ningún identificador.</li>
    <li>No usa análisis de uso, estadísticas ni rastreo de ningún tipo.</li>
    <li>No muestra anuncios ni usa identificador de publicidad.</li>
    <li>No accede a tus contactos, fotos, cámara, micrófono, ubicación ni archivos.</li>
    <li>No vende, alquila ni comparte datos con nadie, porque no guarda ninguno.</li>
  </ul>

  <h2>Copia de seguridad de Android</h2>
  <p>Android ofrece un servicio de copia de seguridad automática que copia los datos de
  las apps al Google Drive del propio usuario. Si ese servicio está activado en tu
  dispositivo, <strong>el archivo con tus recetas se copiará a tu Google Drive</strong> y
  se restaurará cuando reinstales la app o cambies de celular.</p>
  <p>Conviene ser precisos sobre lo que eso significa: esa copia vive en
  <strong>tu</strong> cuenta de Google, bajo las políticas del propio Google, y existe
  para que no pierdas tu trabajo. <strong>No tenemos acceso a ella.</strong></p>
  <p>Puedes desactivar la copia de seguridad, o borrar una copia existente, en los ajustes
  del dispositivo, en <em>Google &rsaquo; Copia de seguridad</em>. Tu licencia Pro no
  está incluida en esa copia.</p>

  <h2>Compra de la versión Pro</h2>
  <p>La versión Pro es una compra única, procesada por completo por
  <strong>Google Play</strong>. Los datos de pago los trata Google según su propia
  política de privacidad: nosotros nunca vemos, recibimos ni guardamos números de
  tarjeta, direcciones ni datos bancarios.</p>
  <p>La app guarda solo un registro local, en tu dispositivo, de que la compra se
  realizó, para desbloquear las funciones de pago sin tener que consultar internet cada
  vez.</p>

  <h2>Permisos</h2>
  <table>
    <tr><th>Permiso</th><th>Para qué sirve</th></tr>
    <tr>
      <td><code>INTERNET</code></td>
      <td>Lo usa solo el sistema de compras de Google Play, para confirmar la compra del
      Pro. Por él no se envía ninguna información sobre ti.</td>
    </tr>
  </table>
  <p>La app funciona con normalidad sin conexión. Puedes usarla en modo avión todo el
  día.</p>

  <h2>Niños</h2>
  <p>Preço Certo es una herramienta profesional para el trabajo de repostería y
  panadería y no está dirigida a niños. Como no recopila ningún dato, tampoco recopila
  datos de niños.</p>

  <h2>Tus derechos</h2>
  <p>La Ley General de Protección de Datos de Brasil (LGPD, Ley 13.709/2018), y leyes
  similares en otros países, te dan derecho a acceder, corregir y eliminar tus datos
  personales. En Preço Certo esos derechos se ejercen en el propio dispositivo, porque
  ahí está todo:</p>
  <ul>
    <li><strong>Acceder y corregir:</strong> todo el contenido es visible y editable
    dentro de la app en cualquier momento.</li>
    <li><strong>Eliminar:</strong> borrar un elemento dentro de la app lo quita de forma
    permanente. Desinstalar la app borra todo de una vez.</li>
    <li><strong>Copia de seguridad:</strong> si usas la copia de seguridad de Android,
    recuerda borrar también la copia en tu Google Drive, desde los ajustes del
    dispositivo.</li>
  </ul>
  <p>No tenemos una base de datos de usuarios que consultar o borrar a petición. Aun así,
  si tienes cualquier duda sobre esto, escribe a
  {MAIL}.</p>

  <h2>Cambios en esta política</h2>
  <p>Si la app llegara a tratar datos de una forma nueva, esta página se actualizará
  antes de que el cambio entre en vigor, y la fecha de vigencia de arriba cambiará. Vale
  la pena releerla tras una actualización importante.</p>''',
    footer=f'Preço Certo &middot; FLR Sistemas<br>\n    Contacto: {MAIL}<br>\n    Última actualización: 17 de septiembre de 2026')


def page(code):
    t = T[code]
    langs = ' &middot; '.join(
        ('<strong>%s</strong>' % c.upper()) if c == code else '<a href="%s" hreflang="%s">%s</a>' % (URL[c], c, c.upper())
        for c in ('pt', 'en', 'es'))
    alts = ''.join('<link rel="alternate" hreflang="%s" href="https://flrsistemas.com.br%s">\n' % (c, URL[c]) for c in ('pt', 'en', 'es'))
    alts += '<link rel="alternate" hreflang="x-default" href="https://flrsistemas.com.br%s">\n' % URL['pt']
    return f'''<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="https://flrsistemas.com.br{URL[code]}">
{alts}{ICONS}{STYLE}
</head>
<body>
<main>
  <p class="langs"><a href="{PAGE[code]}">{t['back']}</a> &middot; {langs}</p>
  <h1>{t['h1']}</h1>
  <p class="sub">{t['sub']}</p>
  <div class="summary">
    <p><strong>{t['summary_t']}</strong></p>
    <p style="margin-top:8px">{t['summary_p']}</p>
  </div>

{t['body']}

  <footer>
    <p>{t['footer']}</p>
  </footer>
</main>
</body>
</html>
'''


for code, fn in FILES.items():
    with open(os.path.join(DOCS, fn), 'w', encoding='utf-8', newline='\n') as f:
        f.write(page(code))

# Links de privacidade nas paginas do app: cada idioma abre a politica no proprio idioma
LINKS = {
    'index.html': ('/precocerto/privacy.html', 'Política de privacidade'),
    'en/index.html': ('/precocerto/privacy-en.html', 'Privacy policy'),
    'es/index.html': ('/precocerto/privacy-es.html', 'Política de privacidad'),
}
for rel, (href, label) in LINKS.items():
    p = os.path.join(DOCS, rel.replace('/', os.sep))
    s = open(p, encoding='utf-8', newline='').read()
    s2 = re.sub(r'<a class="link" href="/precocerto/privacy[^"]*">[^<]*</a>',
                '<a class="link" href="%s">%s</a>' % (href, label), s, count=1)
    assert s2 != s or ('href="%s">%s' % (href, label)) in s, rel
    open(p, 'w', encoding='utf-8', newline='').write(s2)
print('ok')
