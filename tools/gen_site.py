import os, re

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import SITE  # clone de flrsistemas/flrsistemas.github.io
UPDATED = {'pt': '18/11/2026', 'en': 'November 18, 2026', 'es': '18/11/2026'}
EMAIL = 'contato@flrsistemas.com.br'

PREFIX = {'pt': '/', 'en': '/en/', 'es': '/es/'}
SLUG = {
    'pt': {'home': '', 'news': 'novidades/', 'help': 'ajuda/', 'contact': 'contato/', 'privacy': 'privacidade/'},
    'en': {'home': '', 'news': 'news/', 'help': 'help/', 'contact': 'contact/', 'privacy': 'privacy/'},
    'es': {'home': '', 'news': 'novedades/', 'help': 'ayuda/', 'contact': 'contacto/', 'privacy': 'privacidad/'},
}
TABS = {
    'pt': {'home': 'Apps', 'news': 'Novidades', 'help': 'Ajuda', 'contact': 'Contato', 'privacy': 'Privacidade'},
    'en': {'home': 'Apps', 'news': 'News', 'help': 'Help', 'contact': 'Contact', 'privacy': 'Privacy'},
    'es': {'home': 'Apps', 'news': 'Novedades', 'help': 'Ayuda', 'contact': 'Contacto', 'privacy': 'Privacidad'},
}
ORDER = ['home', 'news', 'help', 'contact', 'privacy']
OG = {'pt': ('pt_BR', 'og-v2.png'), 'en': ('en_US', 'og-en.png'), 'es': ('es_ES', 'og-es.png')}
TAGLINE = {'pt': 'Aplicativos para Android.', 'en': 'Apps for Android.', 'es': 'Aplicaciones para Android.'}
NAVLABEL = {'pt': 'Seções do site', 'en': 'Site sections', 'es': 'Secciones del sitio'}
CONTACT_WORD = {'pt': 'Contato', 'en': 'Contact', 'es': 'Contacto'}


def path(lang, key):
    return PREFIX[lang] + SLUG[lang][key]


def tabs_html(lang, current):
    items = ''.join(
        '<a href="%s"%s>%s</a>' % (path(lang, k), ' aria-current="page"' if k == current else '', TABS[lang][k])
        for k in ORDER)
    return '<nav class="tabs" aria-label="%s">%s</nav>' % (NAVLABEL[lang], items)


def langs_html(lang, key):
    return ''.join(
        '<a href="%s" lang="%s" hreflang="%s"%s onclick="try{localStorage.setItem(\'lang\',\'%s\')}catch(e){}">%s</a>'
        % (path(c, key), c, c, ' aria-current="page"' if c == lang else '', c, c.upper())
        for c in ('pt', 'en', 'es'))


def footer_html(lang):
    return ('  <footer>\n    <p>\n      FLR Sistemas<br>\n      %s: <a href="mailto:%s">%s</a><br>\n'
            '      <a href="%s">%s</a>\n    </p>\n  </footer>\n') % (
        CONTACT_WORD[lang], EMAIL, EMAIL, path(lang, 'privacy'), TABS[lang]['privacy'])


EXTRA_CSS = """
  /* ===== Abas de navegacao ===== */
  nav.tabs { display: flex; gap: 2px; margin: 22px 0 0; border-bottom: 1px solid var(--border); overflow-x: auto; overflow-y: hidden; scrollbar-width: none; }
  nav.tabs a { color: var(--muted); text-decoration: none; padding: 10px 14px; white-space: nowrap;
    border-bottom: 2px solid transparent; margin-bottom: -1px; }
  nav.tabs a:hover, nav.tabs a:focus-visible { color: var(--text); }
  nav.tabs a[aria-current="page"] { color: var(--text); font-weight: 600; border-bottom-color: var(--text); }
  h1.page { font-size: 1.7rem; line-height: 1.25; margin: 34px 0 6px; }
  p.intro { color: var(--muted); margin: 0 0 22px; }
  /* Novidades */
  .news-item { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 16px 20px; margin: 0 0 14px; }
  .news-item time { color: var(--muted); font-size: .85rem; }
  .news-item h3 { margin: 4px 0 6px; font-size: 1.05rem; }
  .news-item p, .news-item ul { margin: 0; color: var(--muted); font-size: .95rem; }
  .news-item ul { padding-left: 20px; }
  .tag { display: inline-block; margin-left: 6px; padding: 1px 8px; border: 1px solid var(--border); border-radius: 999px;
    font-size: .72rem; color: var(--muted); vertical-align: middle; }
  /* Ajuda */
  h2.group { font-size: 1.1rem; margin: 30px 0 12px; padding-top: 0; border-top: 0; }
  details.faq { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; margin: 0 0 10px; }
  details.faq summary { cursor: pointer; padding: 14px 18px; font-weight: 600; }
  details.faq p, details.faq ul { margin: 0; padding: 0 18px 16px; color: var(--muted); font-size: .95rem; }
  details.faq ul { padding-left: 38px; }
  /* Contato e texto corrido */
  .box { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 18px 20px; margin: 0 0 14px; }
  .box h3 { margin: 0 0 6px; font-size: 1.02rem; }
  .box p, .box ul { margin: 0; color: var(--muted); font-size: .95rem; }
  .box ul { padding-left: 20px; }
  .doc h3 { font-size: 1.05rem; margin: 28px 0 8px; }
  .doc p, .doc li { color: var(--text); }
  .doc ul { padding-left: 22px; }
  .doc li { margin: 4px 0; }
  .updated { color: var(--muted); font-size: .88rem; }
  .callout { background: var(--surface); border-left: 4px solid var(--accent); border-radius: 0 10px 10px 0; padding: 14px 18px; margin: 18px 0; }
  footer a { color: var(--muted); }
"""

# ----------------------------------------------------------------------------
# Conteudo das paginas (apenas o miolo; o cabecalho/abas/rodape sao gerados)
# ----------------------------------------------------------------------------
META = {
 'pt': {
  'news': ('Novidades', 'Novidades e atualizações dos apps da FLR Sistemas.'),
  'help': ('Ajuda', 'Perguntas frequentes sobre os apps da FLR Sistemas.'),
  'contact': ('Contato', 'Fale com a FLR Sistemas: dúvidas, sugestões e relatos de problemas.'),
  'privacy': ('Privacidade', 'Política de privacidade dos apps da FLR Sistemas.'),
 },
 'en': {
  'news': ('News', 'News and updates about FLR Sistemas apps.'),
  'help': ('Help', 'Frequently asked questions about FLR Sistemas apps.'),
  'contact': ('Contact', 'Get in touch with FLR Sistemas: questions, suggestions and problem reports.'),
  'privacy': ('Privacy', 'Privacy policy of FLR Sistemas apps.'),
 },
 'es': {
  'news': ('Novedades', 'Novedades y actualizaciones de las apps de FLR Sistemas.'),
  'help': ('Ayuda', 'Preguntas frecuentes sobre las apps de FLR Sistemas.'),
  'contact': ('Contacto', 'Habla con FLR Sistemas: dudas, sugerencias y reportes de problemas.'),
  'privacy': ('Privacidad', 'Política de privacidad de las apps de FLR Sistemas.'),
 },
}

BODY = {}

# ------------------------------- PORTUGUES ----------------------------------
BODY['pt'] = {}
BODY['pt']['news'] = """
  <h1 class="page">Novidades</h1>
  <p class="intro">O que mudou nos nossos apps e no site.</p>

  <article class="news-item">
    <time datetime="2026-11-18">18/11/2026</time>
    <h3>Site com abas e política de privacidade <span class="tag">Site</span></h3>
    <p>O site ganhou menu com Apps, Novidades, Ajuda, Contato e Privacidade, e a política de privacidade do Lista de Compras.</p>
  </article>

  <article class="news-item">
    <time datetime="2026-11-18">18/11/2026</time>
    <h3>Lista de Compras: preço dos itens e total da lista <span class="tag">Lista de Compras</span></h3>
    <ul>
      <li>Campo de preço em cada item, com o total da lista dentro dela e em cada cartão da tela inicial.</li>
      <li>Preço e quantidade agora só aceitam números.</li>
      <li>Senhas novas precisam de no mínimo 8 caracteres, com letras e números.</li>
    </ul>
  </article>

  <article class="news-item">
    <time datetime="2026-11-18">18/11/2026</time>
    <h3>Lista de Compras chega à web <span class="tag">Lista de Compras</span></h3>
    <p>Listas de compras compartilhadas por e-mail, atualizadas em tempo real para todos os participantes. Funciona no navegador e instala no celular.</p>
  </article>
"""
BODY['pt']['help'] = """
  <h1 class="page">Ajuda</h1>
  <p class="intro">Respostas rápidas sobre o Lista de Compras. Dúvidas sobre o Preço Certo? Veja a <a href="/precocerto/">página do app</a>. Não achou o que procura? <a href="/contato/">Fale com a gente</a>.</p>

  <h2 class="group">Conta e acesso</h2>
  <details class="faq"><summary>Como crio a minha conta?</summary>
    <p>Na tela inicial do app, toque em "Cadastre-se", informe nome, e-mail e uma senha de no mínimo 8 caracteres, com letras e números. Você recebe um e-mail para confirmar o cadastro; depois é só entrar.</p></details>
  <details class="faq"><summary>Não recebi o e-mail de confirmação</summary>
    <p>Espere alguns minutos e olhe a caixa de spam ou lixo eletrônico. O e-mail vem de "Supabase Auth", o serviço que cuida do login. Se continuar sem chegar, escreva para nós com o e-mail que você usou.</p></details>
  <details class="faq"><summary>Esqueci a minha senha</summary>
    <p>O app ainda não tem recuperação de senha pela tela de login. Escreva para nós, do e-mail cadastrado, e ajudamos a recuperar o acesso.</p></details>
  <details class="faq"><summary>Como apago a minha conta e os meus dados?</summary>
    <p>Escreva para nós, do e-mail cadastrado, pedindo a exclusão. Veja a <a href="/privacidade/">política de privacidade</a> para saber o que é apagado.</p></details>

  <h2 class="group">Listas e itens</h2>
  <details class="faq"><summary>Como compartilho uma lista?</summary>
    <p>Abra a lista, toque no ícone de pessoas (👥), informe o e-mail de quem vai participar e toque em "Compartilhar". Só o dono da lista pode compartilhar.</p></details>
  <details class="faq"><summary>Aparece "Nenhum usuário cadastrado com este e-mail"</summary>
    <p>A pessoa precisa criar a conta no app antes, com esse mesmo e-mail. Depois disso, compartilhe de novo.</p></details>
  <details class="faq"><summary>Como excluo uma lista?</summary>
    <p>Abra a lista, toque no ícone de pessoas e em "Excluir lista". Isso apaga a lista e todos os itens para todos os participantes e não dá para desfazer. Quem não é dono vê "Sair da lista", que tira só a própria pessoa.</p></details>
  <details class="faq"><summary>Como informo o preço dos itens?</summary>
    <p>Use o campo "Preço (R$)" ao adicionar o item ou toque no item para editar. O total aparece na lista e no cartão dela. O app não multiplica por quantidade: informe o valor do item inteiro.</p></details>

  <h2 class="group">Celular e internet</h2>
  <details class="faq"><summary>Como instalo no celular?</summary>
    <p>No Android (Chrome), abra o app, toque no menu ⋮ e em "Instalar app" ou "Adicionar à tela inicial". No iPhone (Safari), toque em Compartilhar e em "Adicionar à Tela de Início".</p></details>
  <details class="faq"><summary>Funciona sem internet?</summary>
    <p>Você consegue consultar a última versão salva das suas listas. Para adicionar, marcar ou remover itens, é preciso estar conectado.</p></details>
"""
BODY['pt']['contact'] = """
  <h1 class="page">Contato</h1>
  <p class="intro">Dúvidas, sugestões ou algum problema? Escreva para nós.</p>

  <div class="box">
    <h3>E-mail</h3>
    <p><a class="button" href="mailto:contato@flrsistemas.com.br?subject=Contato%20pelo%20site">contato@flrsistemas.com.br</a></p>
  </div>

  <div class="box">
    <h3>Para agilizar</h3>
    <ul>
      <li>Diga de qual app você está falando (Preço Certo ou Lista de Compras).</li>
      <li>Descreva o que aconteceu e o que você esperava.</li>
      <li>Informe o aparelho e o navegador, se for um problema.</li>
      <li>Nunca envie a sua senha.</li>
    </ul>
  </div>

  <div class="box">
    <h3>Antes de escrever</h3>
    <p>A página de <a href="/ajuda/">Ajuda</a> responde as dúvidas mais comuns. Para pedidos sobre os seus dados, veja a <a href="/privacidade/">política de privacidade</a>.</p>
  </div>
"""
BODY['pt']['privacy'] = """
  <h1 class="page">Política de privacidade</h1>
  <p class="intro">Cada app tem a sua política, em página própria.</p>

  <div class="box">
    <h3>Preço Certo</h3>
    <p>Não coleta dados pessoais: tudo fica no seu celular.</p>
    <p style="margin-top:12px"><a class="button" href="/precocerto/privacy.html">Ler a política (em inglês)</a></p>
  </div>

  <div class="box">
    <h3>Lista de Compras</h3>
    <p>Guarda o seu nome, e-mail e as listas que você cria, só para o app funcionar. Sem anúncios nem rastreamento.</p>
    <p style="margin-top:12px"><a class="button" href="/listadecompras/privacy.html">Ler a política</a></p>
  </div>

  <p class="intro">Dúvidas sobre os seus dados? Escreva para <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a>.</p>
"""

# -------------------------------- INGLES ------------------------------------
BODY['en'] = {}
BODY['en']['news'] = """
  <h1 class="page">News</h1>
  <p class="intro">What changed in our apps and on the site.</p>

  <article class="news-item">
    <time datetime="2026-11-18">November 18, 2026</time>
    <h3>Site with tabs and privacy policy <span class="tag">Site</span></h3>
    <p>The site now has a menu with Apps, News, Help, Contact and Privacy, plus the privacy policy for Lista de Compras.</p>
  </article>

  <article class="news-item">
    <time datetime="2026-11-18">November 18, 2026</time>
    <h3>Lista de Compras: item prices and list total <span class="tag">Lista de Compras</span></h3>
    <ul>
      <li>A price field on every item, with the list total inside the list and on each card of the home screen.</li>
      <li>Price and quantity now accept numbers only.</li>
      <li>New passwords need at least 8 characters, with letters and numbers.</li>
    </ul>
  </article>

  <article class="news-item">
    <time datetime="2026-11-18">November 18, 2026</time>
    <h3>Lista de Compras arrives on the web <span class="tag">Lista de Compras</span></h3>
    <p>Shopping lists shared by e-mail and updated in real time for everyone on the list. Works in the browser and installs on your phone.</p>
  </article>
"""
BODY['en']['help'] = """
  <h1 class="page">Help</h1>
  <p class="intro">Quick answers about Lista de Compras (the app itself is in Portuguese). Questions about Preço Certo? See the <a href="/precocerto/en/">app page</a>. Can't find what you need? <a href="/en/contact/">Get in touch</a>.</p>

  <h2 class="group">Account and access</h2>
  <details class="faq"><summary>How do I create my account?</summary>
    <p>On the app's first screen, tap "Cadastre-se" (Sign up), enter your name, e-mail and a password of at least 8 characters, with letters and numbers. You get an e-mail to confirm the sign-up; then just sign in.</p></details>
  <details class="faq"><summary>I did not get the confirmation e-mail</summary>
    <p>Wait a few minutes and check your spam or junk folder. The e-mail comes from "Supabase Auth", the service that handles sign-in. If it still does not arrive, write to us with the e-mail you used.</p></details>
  <details class="faq"><summary>I forgot my password</summary>
    <p>The app does not have password recovery on the sign-in screen yet. Write to us from the e-mail you registered with and we will help you get back in.</p></details>
  <details class="faq"><summary>How do I delete my account and my data?</summary>
    <p>Write to us from the registered e-mail asking for deletion. See the <a href="/en/privacy/">privacy policy</a> to know what is deleted.</p></details>

  <h2 class="group">Lists and items</h2>
  <details class="faq"><summary>How do I share a list?</summary>
    <p>Open the list, tap the people icon (👥), enter the e-mail of who will join and tap "Compartilhar" (Share). Only the list owner can share it.</p></details>
  <details class="faq"><summary>It says "Nenhum usuário cadastrado com este e-mail"</summary>
    <p>That means no account exists with that e-mail. The person needs to create an account in the app first, with that same e-mail. Then share again.</p></details>
  <details class="faq"><summary>How do I delete a list?</summary>
    <p>Open the list, tap the people icon and "Excluir lista" (Delete list). This deletes the list and all its items for every member and cannot be undone. Members who are not the owner see "Sair da lista" (Leave list), which removes only themselves.</p></details>
  <details class="faq"><summary>How do I set item prices?</summary>
    <p>Use the "Preço (R$)" field when adding the item, or tap the item to edit it. The total shows on the list and on its card. The app does not multiply by quantity: enter the price for the whole item.</p></details>

  <h2 class="group">Phone and internet</h2>
  <details class="faq"><summary>How do I install it on my phone?</summary>
    <p>On Android (Chrome), open the app, tap the ⋮ menu and "Install app" or "Add to home screen". On iPhone (Safari), tap Share and "Add to Home Screen".</p></details>
  <details class="faq"><summary>Does it work offline?</summary>
    <p>You can view the last saved version of your lists. To add, check or remove items you need to be online.</p></details>
"""
BODY['en']['contact'] = """
  <h1 class="page">Contact</h1>
  <p class="intro">Questions, suggestions or a problem? Write to us.</p>

  <div class="box">
    <h3>E-mail</h3>
    <p><a class="button" href="mailto:contato@flrsistemas.com.br?subject=Contact%20from%20the%20website">contato@flrsistemas.com.br</a></p>
  </div>

  <div class="box">
    <h3>To speed things up</h3>
    <ul>
      <li>Tell us which app you mean (Preço Certo or Lista de Compras).</li>
      <li>Describe what happened and what you expected.</li>
      <li>Include your device and browser if it is a problem.</li>
      <li>Never send your password.</li>
    </ul>
  </div>

  <div class="box">
    <h3>Before you write</h3>
    <p>The <a href="/en/help/">Help</a> page answers the most common questions. For requests about your data, see the <a href="/en/privacy/">privacy policy</a>.</p>
  </div>
"""
BODY['en']['privacy'] = """
  <h1 class="page">Privacy policy</h1>
  <p class="intro">Each app has its own policy, on its own page.</p>

  <div class="box">
    <h3>Preço Certo</h3>
    <p>Collects no personal data: everything stays on your phone.</p>
    <p style="margin-top:12px"><a class="button" href="/precocerto/privacy.html">Read the policy</a></p>
  </div>

  <div class="box">
    <h3>Lista de Compras</h3>
    <p>Keeps your name, e-mail and the lists you create, only so the app can work. No ads and no tracking.</p>
    <p style="margin-top:12px"><a class="button" href="/listadecompras/privacy-en.html">Read the policy</a></p>
  </div>

  <p class="intro">Questions about your data? Write to <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a>.</p>
"""

# -------------------------------- ESPANOL -----------------------------------
BODY['es'] = {}
BODY['es']['news'] = """
  <h1 class="page">Novedades</h1>
  <p class="intro">Qué cambió en nuestras apps y en el sitio.</p>

  <article class="news-item">
    <time datetime="2026-11-18">18/11/2026</time>
    <h3>Sitio con pestañas y política de privacidad <span class="tag">Sitio</span></h3>
    <p>El sitio ahora tiene un menú con Apps, Novedades, Ayuda, Contacto y Privacidad, y la política de privacidad de Lista de Compras.</p>
  </article>

  <article class="news-item">
    <time datetime="2026-11-18">18/11/2026</time>
    <h3>Lista de Compras: precio de los artículos y total de la lista <span class="tag">Lista de Compras</span></h3>
    <ul>
      <li>Campo de precio en cada artículo, con el total de la lista dentro de ella y en cada tarjeta de la pantalla inicial.</li>
      <li>Precio y cantidad ahora solo aceptan números.</li>
      <li>Las contraseñas nuevas necesitan al menos 8 caracteres, con letras y números.</li>
    </ul>
  </article>

  <article class="news-item">
    <time datetime="2026-11-18">18/11/2026</time>
    <h3>Lista de Compras llega a la web <span class="tag">Lista de Compras</span></h3>
    <p>Listas de compras compartidas por correo y actualizadas en tiempo real para todos los participantes. Funciona en el navegador y se instala en el celular.</p>
  </article>
"""
BODY['es']['help'] = """
  <h1 class="page">Ayuda</h1>
  <p class="intro">Respuestas rápidas sobre Lista de Compras (la app está en portugués). ¿Dudas sobre Preço Certo? Mira la <a href="/precocerto/es/">página de la app</a>. ¿No encuentras lo que buscas? <a href="/es/contacto/">Escríbenos</a>.</p>

  <h2 class="group">Cuenta y acceso</h2>
  <details class="faq"><summary>¿Cómo creo mi cuenta?</summary>
    <p>En la pantalla inicial de la app, toca "Cadastre-se" (Registrarse), escribe nombre, correo y una contraseña de al menos 8 caracteres, con letras y números. Recibes un correo para confirmar el registro; después solo inicia sesión.</p></details>
  <details class="faq"><summary>No recibí el correo de confirmación</summary>
    <p>Espera unos minutos y revisa la carpeta de spam o correo no deseado. El correo llega de "Supabase Auth", el servicio que gestiona el inicio de sesión. Si sigue sin llegar, escríbenos con el correo que usaste.</p></details>
  <details class="faq"><summary>Olvidé mi contraseña</summary>
    <p>La app aún no tiene recuperación de contraseña en la pantalla de inicio de sesión. Escríbenos desde el correo registrado y te ayudamos a recuperar el acceso.</p></details>
  <details class="faq"><summary>¿Cómo elimino mi cuenta y mis datos?</summary>
    <p>Escríbenos desde el correo registrado pidiendo la eliminación. Mira la <a href="/es/privacidad/">política de privacidad</a> para saber qué se borra.</p></details>

  <h2 class="group">Listas y artículos</h2>
  <details class="faq"><summary>¿Cómo comparto una lista?</summary>
    <p>Abre la lista, toca el ícono de personas (👥), escribe el correo de quien va a participar y toca "Compartilhar" (Compartir). Solo el dueño de la lista puede compartirla.</p></details>
  <details class="faq"><summary>Aparece "Nenhum usuário cadastrado com este e-mail"</summary>
    <p>Significa que no existe una cuenta con ese correo. La persona debe crear antes la cuenta en la app, con ese mismo correo. Luego comparte de nuevo.</p></details>
  <details class="faq"><summary>¿Cómo elimino una lista?</summary>
    <p>Abre la lista, toca el ícono de personas y "Excluir lista" (Eliminar lista). Esto borra la lista y todos sus artículos para todos los participantes y no se puede deshacer. Quien no es dueño ve "Sair da lista" (Salir de la lista), que quita solo a esa persona.</p></details>
  <details class="faq"><summary>¿Cómo indico el precio de los artículos?</summary>
    <p>Usa el campo "Preço (R$)" al agregar el artículo o toca el artículo para editarlo. El total aparece en la lista y en su tarjeta. La app no multiplica por la cantidad: indica el valor del artículo completo.</p></details>

  <h2 class="group">Celular e internet</h2>
  <details class="faq"><summary>¿Cómo la instalo en el celular?</summary>
    <p>En Android (Chrome), abre la app, toca el menú ⋮ y "Instalar app" o "Añadir a la pantalla de inicio". En iPhone (Safari), toca Compartir y "Añadir a pantalla de inicio".</p></details>
  <details class="faq"><summary>¿Funciona sin internet?</summary>
    <p>Puedes consultar la última versión guardada de tus listas. Para agregar, marcar o quitar artículos hay que estar conectado.</p></details>
"""
BODY['es']['contact'] = """
  <h1 class="page">Contacto</h1>
  <p class="intro">¿Dudas, sugerencias o algún problema? Escríbenos.</p>

  <div class="box">
    <h3>Correo</h3>
    <p><a class="button" href="mailto:contato@flrsistemas.com.br?subject=Contacto%20desde%20el%20sitio">contato@flrsistemas.com.br</a></p>
  </div>

  <div class="box">
    <h3>Para agilizar</h3>
    <ul>
      <li>Di de qué app hablas (Preço Certo o Lista de Compras).</li>
      <li>Describe qué pasó y qué esperabas.</li>
      <li>Indica el dispositivo y el navegador, si es un problema.</li>
      <li>Nunca envíes tu contraseña.</li>
    </ul>
  </div>

  <div class="box">
    <h3>Antes de escribir</h3>
    <p>La página de <a href="/es/ayuda/">Ayuda</a> responde las dudas más comunes. Para solicitudes sobre tus datos, mira la <a href="/es/privacidad/">política de privacidad</a>.</p>
  </div>
"""
BODY['es']['privacy'] = """
  <h1 class="page">Política de privacidad</h1>
  <p class="intro">Cada app tiene su propia política, en su propia página.</p>

  <div class="box">
    <h3>Preço Certo</h3>
    <p>No recopila datos personales: todo se queda en tu celular.</p>
    <p style="margin-top:12px"><a class="button" href="/precocerto/privacy.html">Leer la política (en inglés)</a></p>
  </div>

  <div class="box">
    <h3>Lista de Compras</h3>
    <p>Guarda tu nombre, tu correo y las listas que creas, solo para que la app funcione. Sin anuncios ni rastreo.</p>
    <p style="margin-top:12px"><a class="button" href="/listadecompras/privacy-es.html">Leer la política</a></p>
  </div>

  <p class="intro">¿Dudas sobre tus datos? Escribe a <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a>.</p>
"""



def read(p):
    with open(p, encoding='utf-8', newline='') as f:
        return f.read()


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)


# O CSS e reaproveitado da home atual (ja tem abas, icones e miniaturas)
STYLE_RE = re.compile(r'<style>.*?</style>', re.S)
home_style = STYLE_RE.search(read(os.path.join(SITE, 'index.html'))).group(0)
assert 'nav.tabs' in home_style and '.app-head' in home_style

# ------------------------------ Home (3 idiomas) -----------------------------
APPS = '/listadecompras/'
HOME = {
 'en': dict(
  desc='FLR Sistemas | Creating smart solutions. Turning complex logic into simple, efficient apps.',
  alt='FLR Sistemas: creating smart solutions', h2='Our apps', about='About the app', open='Open the app',
  cards=[
   ('Preço Certo', '/img/precocerto-icon.svg', 'Android app · for bakers and confectioners', '/precocerto/img/home.webp', 944, 2000,
    'Preço Certo app home screen',
    'Know the real cost of every recipe and the price that pays you for your work. Creates a quote and a kitchen sheet as PDF.',
    '/precocerto/en/', None),
   ('Lista de Compras', '/img/listadecompras-icon.svg', 'Web app (PWA) · for anyone sharing the household shopping', '/listadecompras/sobre/img/lista-itens-en.png', 1000, 2260,
    'Shopping list screen with items, prices and the total',
    'Create shopping lists and share them by e-mail: everything updates in real time for everyone. Add each item\'s price and see the list total. Installs on your phone like an app.',
    '/listadecompras/sobre/en/', '/listadecompras/'),
  ]),
 'pt': dict(
  desc='FLR Sistemas | Criando soluções inteligentes. Transformando lógica complexa em aplicativos simples e eficientes.',
  alt='FLR Sistemas: criando soluções inteligentes', h2='Nossos apps', about='Conhecer o app', open='Abrir o app',
  cards=[
   ('Preço Certo', '/img/precocerto-icon.svg', 'App Android · para quem trabalha com confeitaria', '/precocerto/img/home.webp', 944, 2000,
    'Tela inicial do app Preço Certo',
    'Saiba o custo real de cada receita e o preço que paga o seu trabalho. Gera orçamento e ficha de cozinha em PDF.',
    '/precocerto/', None),
   ('Lista de Compras', '/img/listadecompras-icon.svg', 'App web (PWA) · para quem divide as compras da casa', '/listadecompras/sobre/img/lista-itens-pt.png', 1000, 2260,
    'Tela de uma lista de compras com itens, preços e o total',
    'Crie listas de compras e compartilhe por e-mail: tudo se atualiza em tempo real para todos. Anote o preço de cada item e veja o total da lista. Instala no celular como um app.',
    '/listadecompras/sobre/', '/listadecompras/'),
  ]),
 'es': dict(
  desc='FLR Sistemas | Creando soluciones inteligentes. Transformando lógica compleja en aplicaciones simples y eficientes.',
  alt='FLR Sistemas: creando soluciones inteligentes', h2='Nuestras apps', about='Conocer la app', open='Abrir la app',
  cards=[
   ('Preço Certo', '/img/precocerto-icon.svg', 'App Android · para quien trabaja en repostería', '/precocerto/img/home.webp', 944, 2000,
    'Pantalla inicial de la app Preço Certo',
    'Conoce el costo real de cada receta y el precio que paga tu trabajo. Genera presupuesto y ficha de cocina en PDF.',
    '/precocerto/es/', None),
   ('Lista de Compras', '/img/listadecompras-icon.svg', 'App web (PWA) · para quien comparte las compras del hogar', '/listadecompras/sobre/img/lista-itens-es.png', 1000, 2260,
    'Pantalla de una lista de compras con artículos, precios y el total',
    'Crea listas de compras y compártelas por correo: todo se actualiza en tiempo real para todos. Anota el precio de cada artículo y mira el total de la lista. Se instala en el celular como una app.',
    '/listadecompras/sobre/es/', '/listadecompras/'),
  ]),
}
ICON_LINKS = ('<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
              '<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">\n'
              '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
              '<meta name="theme-color" content="#121418">\n')
PLAY = 'https://play.google.com/store/apps/details?id=br.com.flrsistemas.precocerto.app'


def redirect_script(key):
    return ("<script>\n  /* Escolha automatica de idioma, so na primeira visita e so na pagina padrao (pt). */\n"
            "  (function () {\n    try {\n"
            "      var salvo = localStorage.getItem('lang');\n"
            "      var l = salvo || String((navigator.languages && navigator.languages[0]) || navigator.language || 'pt').slice(0, 2).toLowerCase();\n"
            "      if (l !== 'pt') location.replace(l === 'es' ? '%s' : '%s');\n"
            "    } catch (e) {}\n  })();\n</script>\n") % (path('es', key), path('en', key))


def build_home(lang):
    h = HOME[lang]
    loc, ogimg = OG[lang]
    hl = ''.join('<link rel="alternate" hreflang="%s" href="https://flrsistemas.com.br%s">\n' % (c, path(c, 'home')) for c in ('pt', 'en', 'es'))
    cards = []
    for name, icon, what, thumb, tw, th, talt, desc, about_url, open_url in h['cards']:
        acts = '        <a class="button" href="%s">%s</a>\n' % (about_url, h['about'])
        if open_url:
            acts += '        <a class="link" href="%s">%s</a>\n' % (open_url, h['open'])
        else:
            acts += '        <a class="link" href="%s">Google Play</a>\n' % PLAY
        cards.append(f'''    <!-- ============================================================
         APP: {name}
         ============================================================ -->
    <article class="app">
      <div class="app-head">
        <img class="app-icon" src="{icon}" alt="" width="48" height="48">
        <div>
          <h3>{name}</h3>
          <p class="what">{what}</p>
        </div>
      </div>
      <div class="thumb"><img src="{thumb}" width="{tw}" height="{th}" loading="lazy" alt="{talt}"></div>
      <p class="desc">
        {desc}
      </p>
      <div class="actions">
{acts}      </div>
    </article>
''')
    script = ('<script>\n' + redirect_script('home').split('<script>\n', 1)[1]) if lang == 'pt' else ''
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>FLR Sistemas — apps</title>
<meta name="description" content="{h['desc']}">
<link rel="canonical" href="https://flrsistemas.com.br{path(lang, 'home')}">
{hl}<link rel="alternate" hreflang="x-default" href="https://flrsistemas.com.br{path('pt', 'home')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="FLR Sistemas">
<meta property="og:locale" content="{loc}">
<meta property="og:title" content="FLR Sistemas — apps">
<meta property="og:description" content="{h['desc']}">
<meta property="og:url" content="https://flrsistemas.com.br{path(lang, 'home')}">
<meta property="og:image" content="https://flrsistemas.com.br/img/{ogimg}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{h['alt']}">
<meta name="twitter:card" content="summary_large_image">
{ICON_LINKS}{home_style}
{script}</head>
<body>
<main>

  <nav class="langs langs-solo" aria-label="Language">{langs_html(lang, 'home')}</nav>

  <header class="site">
    <h1 class="company">FLR Sistemas</h1>
    <p class="tagline">{TAGLINE[lang]}</p>
  </header>

  {tabs_html(lang, 'home')}

  <h2>{h['h2']}</h2>
  <div class="apps">

{chr(10).join(cards)}
  </div>

{footer_html(lang)}
</main>
</body>
</html>
'''


# ------------- Ajuda e Privacidade: indices (cada app tem a sua pagina) -------
_BOX = ('  <div class="box">\n    <h3>%s</h3>\n    <p>%s</p>\n'
        '    <p style="margin-top:12px"><a class="button" href="%s">%s</a></p>\n  </div>\n')


def index_body(h, intro, apps, foot):
    boxes = '  <div class="boxes">\n' + '\n'.join(_BOX % a for a in apps) + '  </div>\n'
    return '\n  <h1 class="page">%s</h1>\n  <p class="intro">%s</p>\n\n%s\n  <p class="intro">%s</p>\n' % (h, intro, boxes, foot)


BODY['en']['help'] = index_body('Help', 'Pick the app to see its frequently asked questions.',
    [('Preço Certo', 'The step-by-step is on the app page.', '/precocerto/en/#how', 'See the step-by-step'),
     ('Lista de Compras', 'Questions in 4 groups: getting started, lists and items, sharing, account and data. With search.', '/listadecompras/ajuda/en/', 'Open the help')],
    'Can\'t find what you need? <a href="/en/contact/">Get in touch</a>.')
BODY['pt']['help'] = index_body('Ajuda', 'Escolha o app para ver as perguntas frequentes.',
    [('Preço Certo', 'O passo a passo está na página do app.', '/precocerto/#how', 'Ver o passo a passo'),
     ('Lista de Compras', 'Perguntas em 4 grupos: primeiros passos, listas e itens, compartilhamento, conta e dados. Com busca.', '/listadecompras/ajuda/', 'Abrir a ajuda')],
    'Não achou o que procura? <a href="/contato/">Fale com a gente</a>.')
BODY['es']['help'] = index_body('Ayuda', 'Elige la app para ver sus preguntas frecuentes.',
    [('Preço Certo', 'El paso a paso está en la página de la app.', '/precocerto/es/#how', 'Ver el paso a paso'),
     ('Lista de Compras', 'Preguntas en 4 grupos: primeros pasos, listas y artículos, compartir, cuenta y datos. Con búsqueda.', '/listadecompras/ajuda/es/', 'Abrir la ayuda')],
    '¿No encontraste lo que buscabas? <a href="/es/contacto/">Escríbenos</a>.')

BODY['en']['privacy'] = index_body('Privacy policy', 'Each app has its own policy, on its own page.',
    [('Preço Certo', 'Collects no personal data: everything stays on your phone.', '/precocerto/privacy-en.html', 'Read the policy'),
     ('Lista de Compras', 'Keeps your name, e-mail and the lists you create, only so the app can work. No ads and no tracking.', '/listadecompras/privacy-en.html', 'Read the policy')],
    'Questions about your data? Write to <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a>.')
BODY['pt']['privacy'] = index_body('Política de privacidade', 'Cada app tem a sua política, em página própria.',
    [('Preço Certo', 'Não coleta dados pessoais: tudo fica no seu celular.', '/precocerto/privacy.html', 'Ler a política'),
     ('Lista de Compras', 'Guarda o seu nome, e-mail e as listas que você cria, só para o app funcionar. Sem anúncios nem rastreamento.', '/listadecompras/privacy.html', 'Ler a política')],
    'Dúvidas sobre os seus dados? Escreva para <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a>.')
BODY['es']['privacy'] = index_body('Política de privacidad', 'Cada app tiene su propia política, en su propia página.',
    [('Preço Certo', 'No recopila datos personales: todo se queda en tu celular.', '/precocerto/privacy-es.html', 'Leer la política'),
     ('Lista de Compras', 'Guarda tu nombre, tu correo y las listas que creas, solo para que la app funcione. Sin anuncios ni rastreo.', '/listadecompras/privacy-es.html', 'Leer la política')],
    '¿Dudas sobre tus datos? Escribe a <a href="mailto:contato@flrsistemas.com.br">contato@flrsistemas.com.br</a>.')


_NEWS = {
 'en': ('2026-11-18', 'November 18, 2026', 'Site and Lista de Compras in 3 languages', 'Site',
        'The site is available in Portuguese, English and Spanish. The Lista de Compras app was translated too: it starts in your device language, and you can switch it on the sign-in screen.'),
 'pt': ('2026-11-18', '18/11/2026', 'Site e Lista de Compras em 3 idiomas', 'Site',
        'O site está disponível em português, inglês e espanhol. O app Lista de Compras também foi traduzido: ele começa no idioma do seu aparelho, e você pode trocar na tela de entrada.'),
 'es': ('2026-11-18', '18/11/2026', 'Sitio y Lista de Compras en 3 idiomas', 'Sitio',
        'El sitio está disponible en portugués, inglés y español. La app Lista de Compras también fue traducida: empieza en el idioma de tu dispositivo y puedes cambiarlo en la pantalla de inicio de sesión.'),
}
for _l, (_dt, _lbl, _h, _tag, _p) in _NEWS.items():
    _art = ('  <article class="news-item">\n    <time datetime="%s">%s</time>\n    <h3>%s <span class="tag">%s</span></h3>\n'
            '    <p>%s</p>\n  </article>\n\n') % (_dt, _lbl, _h, _tag, _p)
    _i = BODY[_l]['news'].index('  <article class="news-item">')
    BODY[_l]['news'] = BODY[_l]['news'][:_i] + _art + BODY[_l]['news'][_i:]

_NEWS2 = {
 'en': ('2026-11-19', 'November 19, 2026', 'Lista de Compras: price × quantity', 'Lista de Compras',
        'The price is now per unit and the app multiplies it by the quantity: 6 items at R$6.40 count as R$38.40, in the item, in the list total and on each list card. Items already saved keep their price, so review the ones that have a quantity.'),
 'pt': ('2026-11-19', '19/11/2026', 'Lista de Compras: preço × quantidade', 'Lista de Compras',
        'O preço agora é por unidade e o app multiplica pela quantidade: 6 itens de R$ 6,40 valem R$ 38,40, no item, no total da lista e em cada cartão. Os itens já salvos mantêm o preço informado, então vale revisar os que têm quantidade.'),
 'es': ('2026-11-19', '19/11/2026', 'Lista de Compras: precio × cantidad', 'Lista de Compras',
        'El precio ahora es por unidad y la app lo multiplica por la cantidad: 6 artículos de R$ 6,40 valen R$ 38,40, en el artículo, en el total de la lista y en cada tarjeta. Los artículos ya guardados mantienen su precio, así que conviene revisar los que tienen cantidad.'),
}
for _l, (_dt, _lbl, _h, _tag, _p) in _NEWS2.items():
    _art = ('  <article class="news-item">\n    <time datetime="%s">%s</time>\n    <h3>%s <span class="tag">%s</span></h3>\n'
            '    <p>%s</p>\n  </article>\n\n') % (_dt, _lbl, _h, _tag, _p)
    _i = BODY[_l]['news'].index('  <article class="news-item">')
    BODY[_l]['news'] = BODY[_l]['news'][:_i] + _art + BODY[_l]['news'][_i:]

_NEWS3 = {
 'en': ('2026-11-19', 'November 19, 2026', 'Lista de Compras: check items with no signal', 'Lista de Compras',
        'Checking and unchecking items now works with no signal or a weak one. The changes are saved on the phone, a "waiting for signal" notice appears, and they are sent automatically when the connection returns.'),
 'pt': ('2026-11-19', '19/11/2026', 'Lista de Compras: marque itens sem sinal', 'Lista de Compras',
        'Marcar e desmarcar itens agora funciona sem sinal ou com sinal fraco. As marcações ficam salvas no celular, aparece o aviso "aguardando sinal" e elas são enviadas sozinhas quando a conexão volta.'),
 'es': ('2026-11-19', '19/11/2026', 'Lista de Compras: marca artículos sin señal', 'Lista de Compras',
        'Marcar y desmarcar artículos ahora funciona sin señal o con señal débil. Los cambios se guardan en el celular, aparece el aviso "esperando señal" y se envían solos cuando vuelve la conexión.'),
}
for _l, (_dt, _lbl, _h, _tag, _p) in _NEWS3.items():
    _art = ('  <article class="news-item">\n    <time datetime="%s">%s</time>\n    <h3>%s <span class="tag">%s</span></h3>\n'
            '    <p>%s</p>\n  </article>\n\n') % (_dt, _lbl, _h, _tag, _p)
    _i = BODY[_l]['news'].index('  <article class="news-item">')
    BODY[_l]['news'] = BODY[_l]['news'][:_i] + _art + BODY[_l]['news'][_i:]

_NEWS4 = {
 'en': ('2026-11-19', 'November 19, 2026', 'Lista de Compras: tips inside the app', 'Lista de Compras',
        'The app now shows short tips the first time you use each screen: creating a list, checking items and sharing. They appear once, and the 💡 button brings them back any time.'),
 'pt': ('2026-11-19', '19/11/2026', 'Lista de Compras: dicas dentro do app', 'Lista de Compras',
        'O app agora mostra dicas rápidas na primeira vez que você usa cada tela: criar uma lista, marcar itens e compartilhar. Elas aparecem uma vez só, e o botão 💡 traz todas de volta quando quiser.'),
 'es': ('2026-11-19', '19/11/2026', 'Lista de Compras: consejos dentro de la app', 'Lista de Compras',
        'La app ahora muestra consejos rápidos la primera vez que usas cada pantalla: crear una lista, marcar artículos y compartir. Aparecen una sola vez, y el botón 💡 los trae de vuelta cuando quieras.'),
}
for _l, (_dt, _lbl, _h, _tag, _p) in _NEWS4.items():
    _art = ('  <article class="news-item">\n    <time datetime="%s">%s</time>\n    <h3>%s <span class="tag">%s</span></h3>\n'
            '    <p>%s</p>\n  </article>\n\n') % (_dt, _lbl, _h, _tag, _p)
    _i = BODY[_l]['news'].index('  <article class="news-item">')
    BODY[_l]['news'] = BODY[_l]['news'][:_i] + _art + BODY[_l]['news'][_i:]

_NEWS5 = {
 'en': ('2026-11-19', 'November 19, 2026', 'Lista de Compras: add items with no signal', 'Lista de Compras',
        'You can now add new items with no signal or a weak one. They appear in the list right away with a ⏳, are kept on the phone and are saved to the database automatically when the connection returns.'),
 'pt': ('2026-11-19', '19/11/2026', 'Lista de Compras: adicione itens sem sinal', 'Lista de Compras',
        'Agora dá para adicionar itens novos sem sinal ou com sinal fraco. Eles aparecem na lista na hora, com um ⏳, ficam guardados no celular e são gravados no banco de dados sozinhos quando a conexão volta.'),
 'es': ('2026-11-19', '19/11/2026', 'Lista de Compras: agrega artículos sin señal', 'Lista de Compras',
        'Ahora puedes agregar artículos nuevos sin señal o con señal débil. Aparecen en la lista al instante con un ⏳, quedan guardados en el celular y se graban en la base de datos solos cuando vuelve la conexión.'),
}
for _l, (_dt, _lbl, _h, _tag, _p) in _NEWS5.items():
    _art = ('  <article class="news-item">\n    <time datetime="%s">%s</time>\n    <h3>%s <span class="tag">%s</span></h3>\n'
            '    <p>%s</p>\n  </article>\n\n') % (_dt, _lbl, _h, _tag, _p)
    _i = BODY[_l]['news'].index('  <article class="news-item">')
    BODY[_l]['news'] = BODY[_l]['news'][:_i] + _art + BODY[_l]['news'][_i:]

_NEWS6 = {
 'en': ('2026-11-19', 'November 19, 2026', 'Lista de Compras: edit and remove items with no signal', 'Lista de Compras',
        'Editing, removing and clearing bought items now also works with no signal. The changes are saved on the phone, items with a pending change show a ⏳, and everything is sent in order when the connection returns.'),
 'pt': ('2026-11-19', '19/11/2026', 'Lista de Compras: edite e remova itens sem sinal', 'Lista de Compras',
        'Editar, remover e limpar comprados agora também funciona sem sinal. As alterações ficam salvas no celular, os itens com alteração pendente aparecem com ⏳, e tudo é enviado em ordem quando a conexão volta.'),
 'es': ('2026-11-19', '19/11/2026', 'Lista de Compras: edita y quita artículos sin señal', 'Lista de Compras',
        'Editar, quitar y limpiar los comprados ahora también funciona sin señal. Los cambios se guardan en el celular, los artículos con un cambio pendiente muestran ⏳ y todo se envía en orden cuando vuelve la conexión.'),
}
for _l, (_dt, _lbl, _h, _tag, _p) in _NEWS6.items():
    _art = ('  <article class="news-item">\n    <time datetime="%s">%s</time>\n    <h3>%s <span class="tag">%s</span></h3>\n'
            '    <p>%s</p>\n  </article>\n\n') % (_dt, _lbl, _h, _tag, _p)
    _i = BODY[_l]['news'].index('  <article class="news-item">')
    BODY[_l]['news'] = BODY[_l]['news'][:_i] + _art + BODY[_l]['news'][_i:]

_NEWS7 = {
 'en': ('2026-11-19', 'November 19, 2026', 'Lista de Compras: "Update app" button', 'Lista de Compras',
        'If the app looks outdated, tap "↻ Update app" at the bottom of the lists screen or the sign-in screen. It downloads the newest version and reloads, with no need to switch browsers. Your account, lists and pending changes are kept.'),
 'pt': ('2026-11-19', '19/11/2026', 'Lista de Compras: botão "Atualizar app"', 'Lista de Compras',
        'Se o app parecer desatualizado, toque em "↻ Atualizar app" no fim da tela de listas ou da tela de entrada. Ele baixa a versão mais nova e recarrega, sem precisar trocar de navegador. Sua conta, suas listas e as alterações pendentes ficam como estão.'),
 'es': ('2026-11-19', '19/11/2026', 'Lista de Compras: botón "Actualizar app"', 'Lista de Compras',
        'Si la app se ve desactualizada, toca "↻ Actualizar app" al final de la pantalla de listas o de inicio de sesión. Descarga la versión más nueva y recarga, sin necesidad de cambiar de navegador. Tu cuenta, tus listas y los cambios pendientes se mantienen.'),
}
for _l, (_dt, _lbl, _h, _tag, _p) in _NEWS7.items():
    _art = ('  <article class="news-item">\n    <time datetime="%s">%s</time>\n    <h3>%s <span class="tag">%s</span></h3>\n'
            '    <p>%s</p>\n  </article>\n\n') % (_dt, _lbl, _h, _tag, _p)
    _i = BODY[_l]['news'].index('  <article class="news-item">')
    BODY[_l]['news'] = BODY[_l]['news'][:_i] + _art + BODY[_l]['news'][_i:]

_NEWS8 = {
 'en': ('2026-11-19', 'November 19, 2026', 'Lista de Compras: cart bar', 'Lista de Compras',
        'The top of the list now shows how much is already in the cart, how many items that is (like 2/8) and the total of the list, with a progress bar. It updates in real time for everyone sharing the list, even with no signal.'),
 'pt': ('2026-11-19', '19/11/2026', 'Lista de Compras: barra do carrinho', 'Lista de Compras',
        'O topo da lista agora mostra quanto já está no carrinho, quantos itens são (como 2/8) e o total da lista, com uma barra de progresso. Atualiza em tempo real para todos que compartilham a lista, até sem sinal.'),
 'es': ('2026-11-19', '19/11/2026', 'Lista de Compras: barra del carrito', 'Lista de Compras',
        'La parte de arriba de la lista ahora muestra cuánto ya está en el carrito, cuántos artículos son (como 2/8) y el total de la lista, con una barra de progreso. Se actualiza en tiempo real para todos los que comparten la lista, incluso sin señal.'),
}
for _l, (_dt, _lbl, _h, _tag, _p) in _NEWS8.items():
    _art = ('  <article class="news-item">\n    <time datetime="%s">%s</time>\n    <h3>%s <span class="tag">%s</span></h3>\n'
            '    <p>%s</p>\n  </article>\n\n') % (_dt, _lbl, _h, _tag, _p)
    _i = BODY[_l]['news'].index('  <article class="news-item">')
    BODY[_l]['news'] = BODY[_l]['news'][:_i] + _art + BODY[_l]['news'][_i:]

_NEWS9 = {
 'en': ('2026-11-19', 'November 19, 2026', 'Lista de Compras: rename, delete and leave lists with no signal', 'Lista de Compras',
        'Lists got a new "Rename" field (owner only, inside the 👥 window), and renaming, deleting and leaving a list now work with no signal too. The list changes on screen right away and the change is sent when the connection returns.'),
 'pt': ('2026-11-19', '19/11/2026', 'Lista de Compras: renomeie, exclua e saia de listas sem sinal', 'Lista de Compras',
        'As listas ganharam o campo "Renomear" (só o dono, na janela do 👥), e renomear, excluir e sair de uma lista agora também funcionam sem sinal. A lista muda na tela na hora e a alteração é enviada quando a conexão volta.'),
 'es': ('2026-11-19', '19/11/2026', 'Lista de Compras: renombra, elimina y sal de listas sin señal', 'Lista de Compras',
        'Las listas tienen un nuevo campo "Renombrar" (solo el dueño, en la ventana del 👥), y renombrar, eliminar y salir de una lista ahora también funcionan sin señal. La lista cambia en pantalla al instante y el cambio se envía cuando vuelve la conexión.'),
}
for _l, (_dt, _lbl, _h, _tag, _p) in _NEWS9.items():
    _art = ('  <article class="news-item">\n    <time datetime="%s">%s</time>\n    <h3>%s <span class="tag">%s</span></h3>\n'
            '    <p>%s</p>\n  </article>\n\n') % (_dt, _lbl, _h, _tag, _p)
    _i = BODY[_l]['news'].index('  <article class="news-item">')
    BODY[_l]['news'] = BODY[_l]['news'][:_i] + _art + BODY[_l]['news'][_i:]

_NEWS10 = {
 'en': ('2026-11-19', 'November 19, 2026', 'Lista de Compras: e-mail confirmation takes you back to the app', 'Lista de Compras',
        'The link in the confirmation e-mail now opens the app itself, which shows "E-mail confirmed! Now just sign in". If the link has expired or was already used, the app explains it.'),
 'pt': ('2026-11-19', '19/11/2026', 'Lista de Compras: a confirmação de e-mail volta para o app', 'Lista de Compras',
        'O link do e-mail de confirmação agora abre o próprio app, que mostra "E-mail confirmado! Agora é só entrar". Se o link tiver expirado ou já tiver sido usado, o app explica.'),
 'es': ('2026-11-19', '19/11/2026', 'Lista de Compras: la confirmación del correo vuelve a la app', 'Lista de Compras',
        'El enlace del correo de confirmación ahora abre la propia app, que muestra "¡Correo confirmado! Ahora solo inicia sesión". Si el enlace expiró o ya se usó, la app lo explica.'),
}
for _l, (_dt, _lbl, _h, _tag, _p) in _NEWS10.items():
    _art = ('  <article class="news-item">\n    <time datetime="%s">%s</time>\n    <h3>%s <span class="tag">%s</span></h3>\n'
            '    <p>%s</p>\n  </article>\n\n') % (_dt, _lbl, _h, _tag, _p)
    _i = BODY[_l]['news'].index('  <article class="news-item">')
    BODY[_l]['news'] = BODY[_l]['news'][:_i] + _art + BODY[_l]['news'][_i:]

_NEWS11 = {
 'en': ('2026-11-19', 'November 19, 2026', 'Lista de Compras: confirm password and "Forgot my password"', 'Lista de Compras',
        'Sign-up now asks you to type the password twice. And if you forget it, the sign-in screen has a "Forgot my password" link: you get an e-mail with a link and set a new password in the app.'),
 'pt': ('2026-11-19', '19/11/2026', 'Lista de Compras: confirmar senha e "Esqueci minha senha"', 'Lista de Compras',
        'O cadastro agora pede a senha duas vezes. E, se você esquecer a senha, a tela de entrada tem o link "Esqueci minha senha": você recebe um e-mail com um link e define uma nova senha dentro do app.'),
 'es': ('2026-11-19', '19/11/2026', 'Lista de Compras: confirmar contraseña y "Olvidé mi contraseña"', 'Lista de Compras',
        'El registro ahora pide la contraseña dos veces. Y si la olvidas, la pantalla de inicio de sesión tiene el enlace "Olvidé mi contraseña": recibes un correo con un enlace y defines una contraseña nueva dentro de la app.'),
}
for _l, (_dt, _lbl, _h, _tag, _p) in _NEWS11.items():
    _art = ('  <article class="news-item">\n    <time datetime="%s">%s</time>\n    <h3>%s <span class="tag">%s</span></h3>\n'
            '    <p>%s</p>\n  </article>\n\n') % (_dt, _lbl, _h, _tag, _p)
    _i = BODY[_l]['news'].index('  <article class="news-item">')
    BODY[_l]['news'] = BODY[_l]['news'][:_i] + _art + BODY[_l]['news'][_i:]

_NEWS12 = {
 'en': ('2026-11-19', 'November 19, 2026', 'Lista de Compras: create lists with no signal', 'Lista de Compras',
        'You can now create a new list with no signal or a weak one. It opens right away, you can already add items to it, and everything is saved to the database in order when the connection returns. Sharing it only works after it has been sent.'),
 'pt': ('2026-11-19', '19/11/2026', 'Lista de Compras: crie listas sem sinal', 'Lista de Compras',
        'Agora dá para criar uma lista nova sem sinal ou com sinal fraco. Ela abre na hora, você já pode adicionar itens nela, e tudo é gravado no banco de dados em ordem quando a conexão volta. Compartilhar só funciona depois que a lista for enviada.'),
 'es': ('2026-11-19', '19/11/2026', 'Lista de Compras: crea listas sin señal', 'Lista de Compras',
        'Ahora puedes crear una lista nueva sin señal o con señal débil. Se abre al instante, ya puedes agregarle artículos, y todo se graba en la base de datos en orden cuando vuelve la conexión. Compartirla solo funciona después de que se envíe.'),
}
for _l, (_dt, _lbl, _h, _tag, _p) in _NEWS12.items():
    _art = ('  <article class="news-item">\n    <time datetime="%s">%s</time>\n    <h3>%s <span class="tag">%s</span></h3>\n'
            '    <p>%s</p>\n  </article>\n\n') % (_dt, _lbl, _h, _tag, _p)
    _i = BODY[_l]['news'].index('  <article class="news-item">')
    BODY[_l]['news'] = BODY[_l]['news'][:_i] + _art + BODY[_l]['news'][_i:]

_NEWS13 = {
 'en': ('2026-11-19', 'November 19, 2026', 'Lista de Compras: use it without an account', 'Lista de Compras',
        'On the sign-in screen, "Use without an account" opens the app with no sign-up. Your lists stay only on the device and nothing goes to the internet, so clearing the browser data erases them. There is no sharing in this mode, and you can create an account any time.'),
 'pt': ('2026-11-19', '19/11/2026', 'Lista de Compras: use sem criar conta', 'Lista de Compras',
        'Na tela de entrada, "Usar sem conta" abre o app sem cadastro. As listas ficam só no aparelho e nada vai para a internet, então limpar os dados do navegador apaga tudo. Nesse modo não há compartilhamento, e você pode criar uma conta quando quiser.'),
 'es': ('2026-11-19', '19/11/2026', 'Lista de Compras: úsala sin crear una cuenta', 'Lista de Compras',
        'En la pantalla de inicio de sesión, "Usar sin cuenta" abre la app sin registro. Las listas quedan solo en el dispositivo y no se envía nada a internet, así que borrar los datos del navegador lo elimina todo. En este modo no hay compartir, y puedes crear una cuenta cuando quieras.'),
}
for _l, (_dt, _lbl, _h, _tag, _p) in _NEWS13.items():
    _art = ('  <article class="news-item">\n    <time datetime="%s">%s</time>\n    <h3>%s <span class="tag">%s</span></h3>\n'
            '    <p>%s</p>\n  </article>\n\n') % (_dt, _lbl, _h, _tag, _p)
    _i = BODY[_l]['news'].index('  <article class="news-item">')
    BODY[_l]['news'] = BODY[_l]['news'][:_i] + _art + BODY[_l]['news'][_i:]

# Links internos de Novidades/Contato para os novos enderecos
LINKFIX = {'pt': [], 'en': [], 'es': []}
for _l, _fixes in LINKFIX.items():
    for _k in ('news', 'contact'):
        for _a, _b in _fixes:
            BODY[_l][_k] = BODY[_l][_k].replace(_a, _b)

# Agrupa cartoes em grades (as paginas de texto usam a mesma largura das demais abas)
for _l in ('pt', 'en', 'es'):
    _c = BODY[_l]['contact']
    if '<div class="boxes">' not in _c:
        _i = _c.index('<div class="box">')
        BODY[_l]['contact'] = _c[:_i] + '<div class="boxes">\n  ' + _c[_i:].rstrip() + '\n  </div>\n'
    _n = BODY[_l]['news']
    if '<div class="news-list">' not in _n:
        _i = _n.index('<article class="news-item">')
        BODY[_l]['news'] = _n[:_i] + '<div class="news-list">\n  ' + _n[_i:].rstrip() + '\n  </div>\n'


# --------------------------- Paginas internas -------------------------------
def sub_page(lang, key):
    title_word, desc = META[lang][key]
    title = '%s — FLR Sistemas' % title_word
    loc, ogimg = OG[lang]
    hl = ''.join('<link rel="alternate" hreflang="%s" href="https://flrsistemas.com.br%s">\n' % (c, path(c, key)) for c in ('pt', 'en', 'es'))
    script = redirect_script(key) if lang == 'pt' else ''
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://flrsistemas.com.br{path(lang, key)}">
{hl}<link rel="alternate" hreflang="x-default" href="https://flrsistemas.com.br{path('pt', key)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="FLR Sistemas">
<meta property="og:locale" content="{loc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://flrsistemas.com.br{path(lang, key)}">
<meta property="og:image" content="https://flrsistemas.com.br/img/{ogimg}">
<meta name="twitter:card" content="summary_large_image">
{ICON_LINKS}{home_style}
{script}</head>
<body>
<main>

  <nav class="langs langs-solo" aria-label="Language">{langs_html(lang, key)}</nav>

  <header class="site">
    <p class="company" style="font-size:2.1rem;line-height:1.2;margin:0;font-weight:700"><a href="{PREFIX[lang]}" style="text-decoration:none">FLR Sistemas</a></p>
    <p class="tagline">{TAGLINE[lang]}</p>
  </header>

  {tabs_html(lang, key)}
{BODY[lang][key]}
{footer_html(lang)}
</main>
</body>
</html>
'''


def out_path(url):
    return os.path.join(SITE, url.strip('/').replace('/', os.sep), 'index.html') if url.strip('/') else os.path.join(SITE, 'index.html')


for lang in ('en', 'pt', 'es'):
    write(out_path(path(lang, 'home')), build_home(lang))
    for key in ('news', 'help', 'contact', 'privacy'):
        write(out_path(path(lang, key)), sub_page(lang, key))


# ----------------- Enderecos antigos redirecionam para os novos --------------
def stub(old_url, new_url):
    html = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Redirecting…</title>\n'
            '<meta name="robots" content="noindex">\n<link rel="canonical" href="https://flrsistemas.com.br%s">\n'
            '<meta http-equiv="refresh" content="0; url=%s">\n</head>\n<body>\n<p><a href="%s">%s</a></p>\n</body>\n</html>\n') % (
        new_url, new_url, new_url, new_url)
    write(out_path(old_url), html)


stub('/pt/', '/')
for _k in ('news', 'help', 'contact', 'privacy'):
    stub('/pt/' + SLUG['pt'][_k], path('pt', _k))
    stub('/' + SLUG['en'][_k], path('en', _k))
print('ok')
