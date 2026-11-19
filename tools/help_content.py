# Conteudo organizado da pagina Ajuda (pt, en, es)

CSS = """
  <style>
    .help-search { width: 100%; padding: 12px 16px; border-radius: 12px; border: 1px solid var(--border);
      background: var(--surface); color: var(--text); font: inherit; margin: 0 0 16px; }
    .help-search:focus { outline: 2px solid var(--muted); outline-offset: 1px; }
    .topics { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 8px; padding: 0; list-style: none; }
    .topics a { display: inline-block; padding: 7px 14px; border: 1px solid var(--border); border-radius: 999px;
      color: var(--muted); text-decoration: none; font-size: .92rem; background: var(--surface); }
    .topics a:hover, .topics a:focus-visible { color: var(--text); border-color: var(--muted); }
    section.faq-group { margin: 30px 0 0; scroll-margin-top: 16px; }
    section.faq-group h2 { display: flex; align-items: center; gap: 10px; font-size: 1.15rem; margin: 0 0 12px; padding: 0; border: 0; }
    section.faq-group h2 .ico { width: 34px; height: 34px; display: grid; place-items: center; border-radius: 10px;
      background: var(--surface); border: 1px solid var(--border); font-size: 1.05rem; }
    section.faq-group .count { margin-left: auto; font-size: .8rem; color: var(--muted); font-weight: 400; }
    .faq-list { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }
    .faq-list details { border-top: 1px solid var(--border); }
    .faq-list details:first-child { border-top: 0; }
    .faq-list summary { cursor: pointer; padding: 15px 18px; font-weight: 600; list-style: none; display: flex; gap: 12px; align-items: baseline; }
    .faq-list summary::-webkit-details-marker { display: none; }
    .faq-list summary::after { content: "+"; margin-left: auto; color: var(--muted); font-weight: 400; font-size: 1.2rem; line-height: 1; }
    .faq-list details[open] summary::after { content: "\\2212"; }
    .faq-list details[open] summary { padding-bottom: 8px; }
    .faq-list details p { margin: 0; padding: 0 18px 16px; color: var(--muted); font-size: .95rem; }
    .faq-list details p + p { padding-top: 0; margin-top: -6px; }
    .faq-list summary:hover { background: rgba(255,255,255,.03); }
    .help-empty { display: none; color: var(--muted); padding: 24px 0; text-align: center; }
    .help-cta { margin-top: 36px; }
  </style>
"""

SCRIPT = """
  <script>
    (function () {
      var q = document.getElementById('help-q');
      if (!q) return;
      var empty = document.getElementById('help-empty');
      q.addEventListener('input', function () {
        var t = q.value.trim().toLowerCase(), any = false;
        document.querySelectorAll('section.faq-group').forEach(function (g) {
          var shown = 0;
          g.querySelectorAll('details').forEach(function (d) {
            var ok = !t || d.textContent.toLowerCase().indexOf(t) !== -1;
            d.style.display = ok ? '' : 'none';
            if (ok) { shown++; if (t) d.open = true; }
          });
          g.style.display = shown ? '' : 'none';
          if (shown) any = true;
        });
        empty.style.display = any ? 'none' : 'block';
      });
    })();
  </script>
"""

DATA = {
 'pt': dict(
  title='Ajuda',
  intro='Respostas rápidas sobre o <strong>Lista de Compras</strong>. Dúvidas sobre o Preço Certo? Veja a <a href="%(pc)s">página do app</a>.',
  search='Buscar uma pergunta…', empty='Nenhuma pergunta encontrada. Tente outra palavra ou fale com a gente.',
  count=('pergunta', 'perguntas'),
  cta_t='Não encontrou o que procurava?',
  cta_p='Escreva para nós e respondemos por e-mail. Para pedidos sobre os seus dados, veja também a <a href="%(priv)s">política de privacidade</a>.',
  cta_b='Falar com a gente',
  groups=[
   ('start', '🚀', 'Começando', [
    ('Como crio a minha conta?', ['Na tela inicial do app, toque em "Cadastre-se", informe nome, e-mail e uma senha de no mínimo 8 caracteres, com letras e números, e repita a senha no campo "Confirmar senha". Você recebe um e-mail para confirmar o cadastro; depois é só entrar.']),
    ('Não recebi o e-mail de confirmação', ['Espere alguns minutos e olhe a caixa de spam ou lixo eletrônico. O e-mail vem de "Supabase Auth", o serviço que cuida do login. Se continuar sem chegar, escreva para nós com o e-mail que você usou.']),
    ('O link do e-mail diz que expirou ou já foi usado', ['O link de confirmação vale por pouco tempo e só funciona uma vez. Alguns provedores de e-mail "abrem" o link antes de você, para checar se é seguro, e isso gasta o link. Tente entrar com o seu e-mail e senha: se o cadastro já estiver confirmado, vai funcionar. Se não, cadastre-se de novo ou escreva para nós.', 'Ao confirmar, o link leva de volta ao app, que mostra "E-mail confirmado! Agora é só entrar".']),
    ('Posso usar sem criar conta?', ['Sim. Na tela de entrada, toque em "Usar sem conta". O app avisa e, depois, funciona normalmente, mas as suas listas ficam salvas só neste aparelho e neste navegador, sem enviar nada para a internet. Não há compartilhamento nem cópia em outro aparelho. Se você limpar os dados ou o cache do navegador/do site, ou desinstalar o app, as listas são perdidas, sem como recuperar. O botão "Atualizar app" não apaga as listas.', 'Para guardar com segurança e compartilhar, crie uma conta: toque em "Criar conta" no aviso amarelo do topo. Ao entrar na sua conta neste mesmo aparelho, o app mostra um aviso verde "Importar": as listas do modo sem conta são copiadas para a conta, e você escolhe se mantém ou remove as cópias daqui. Se tocar em "Agora não", o aviso volta na próxima vez que abrir o app.']),
    ('Como instalo no celular?', ['No Android (Chrome), abra o app, toque no menu ⋮ e em "Instalar app" ou "Adicionar à tela inicial".', 'No iPhone (Safari), toque em Compartilhar e em "Adicionar à Tela de Início".']),
    ('Onde vejo as dicas de uso de novo?', ['Toque no ícone 💡, no topo das telas "Minhas listas" e da lista. Lá estão todas as dicas, e o botão "Mostrar as dicas de novo" faz os avisos voltarem a aparecer sozinhos.']),
    ('Posso mudar o idioma do app?', ['Sim. O app existe em inglês, português e espanhol e começa no idioma do seu aparelho. Para trocar, use o seletor de idioma na tela de entrada ou no topo da tela "Minhas listas".']),
   ]),
   ('lists', '🛒', 'Listas e itens', [
    ('Como crio uma lista?', ['Na tela "Minhas listas", digite um nome, como "Mercado do mês", e toque em "Criar".']),
    ('Como adiciono, edito e marco itens?', ['Dentro da lista, digite o nome no campo "Adicionar item…", escolha a categoria (o app sugere uma) e, se quiser, informe quantidade e preço. Toque em "Adicionar".', 'Para marcar como comprado, toque no quadradinho do item. Para editar, toque no nome. Para remover, toque no ✕.']),
    ('Como informo o preço dos itens?', ['Informe o preço de uma unidade no campo "Preço unitário (R$)", ao adicionar o item ou ao editá-lo. O app multiplica pela quantidade: 6 itens de R$ 6,40 aparecem como R$ 38,40. O total aparece dentro da lista e no cartão dela. Sem quantidade, o app considera 1.']),
    ('Como vejo quanto já está no carrinho?', ['A barra no topo da lista mostra, à esquerda, o valor dos itens já marcados ("No carrinho", com a contagem, como 2/8) e, à direita, o total da lista inteira. A barrinha embaixo mostra quanto da lista já foi para o carrinho. Quem compartilha a lista vê os mesmos valores em tempo real, então ninguém pega item repetido.']),
    ('Como limpo os itens já comprados?', ['Na lista, toque em "Limpar comprados", ao lado do título "Comprados". Isso remove só os itens marcados, para todos os participantes.']),
    ('Como renomeio uma lista?', ['Abra a lista, toque no ícone de pessoas (👥), mude o nome no campo do topo e toque em "Salvar". Só o dono da lista pode renomear. Funciona também sem sinal.']),
    ('Como excluo uma lista?', ['Abra a lista, toque no ícone de pessoas (👥) e em "Excluir lista". Isso apaga a lista e todos os itens para todos os participantes e não dá para desfazer. Só o dono vê esse botão.']),
   ]),
   ('share', '🤝', 'Compartilhamento', [
    ('Como compartilho uma lista?', ['Abra a lista, toque no ícone de pessoas (👥), informe o e-mail de quem vai participar e toque em "Compartilhar". Só o dono da lista pode compartilhar.']),
    ('Aparece "No hay ningún usuario registrado con este correo"', ['A pessoa precisa criar a conta no app antes, com esse mesmo e-mail. Depois disso, compartilhe de novo.']),
    ('Como removo alguém da lista?', ['Abra a lista, toque em 👥 e em "Remover", ao lado do nome. Só o dono pode remover participantes.']),
    ('Como saio de uma lista que compartilharam comigo?', ['Abra a lista, toque em 👥 e em "Sair da lista". Isso tira só você; a lista continua para os outros.']),
   ]),
   ('account', '🔒', 'Conta e dados', [
    ('O app diz que o e-mail já está cadastrado', ['Esse e-mail já tem conta. A senha que você digitou no cadastro é ignorada e a conta continua com a senha anterior. Toque em "Entrar" e use a sua senha; se não lembrar, use "Esqueci minha senha".']),
    ('Esqueci a minha senha', ['Na tela de entrada, toque em "Esqueci minha senha", informe o seu e-mail e toque em "Enviar link". Abra o e-mail que você receber (veja também o spam) e toque no link: o app abre e pede a nova senha, duas vezes. Use no mínimo 8 caracteres, com letras e números.', 'O link vale por pouco tempo e só funciona uma vez. Se expirar, peça outro.']),
    ('Como apago a minha conta e os meus dados?', ['Escreva para nós, do e-mail cadastrado, pedindo a exclusão. Veja a <a href="%(priv)s">política de privacidade</a> para saber o que é apagado.']),
    ('O app está com uma versão antiga ou estranho. O que faço?', ['Toque em "↻ Atualizar app", no fim da tela "Minhas listas" ou da tela de entrada. Ele baixa a versão mais nova e recarrega o app, sem precisar trocar de navegador. Sua conta, suas listas e as alterações que aguardam sinal não são apagadas. É preciso estar conectado.']),
    ('Funciona sem internet?', ['Você consegue consultar a última versão salva das suas listas, marcar e desmarcar, adicionar, editar e remover itens, e também limpar os comprados. As alterações ficam guardadas no aparelho (os itens com alteração pendente aparecem com ⏳), aparece o aviso "aguardando sinal" e tudo é enviado sozinho, na mesma ordem, quando a conexão volta.', 'Criar, renomear, excluir e sair de uma lista também funcionam sem sinal. Compartilhar a lista e mudar participantes ainda precisam de conexão (uma lista criada sem sinal só pode ser compartilhada depois de enviada). Se outra pessoa mexer no mesmo item enquanto você está sem sinal, vale a alteração que chegar por último.']),
   ]),
  ]),
 'en': dict(
  title='Help',
  intro='Quick answers about <strong>Lista de Compras</strong>. Questions about Preço Certo? See the <a href="%(pc)s">app page</a>.',
  search='Search a question…', empty='No questions found. Try another word or get in touch.',
  count=('question', 'questions'),
  cta_t="Can't find what you need?",
  cta_p='Write to us and we reply by e-mail. For requests about your data, see also the <a href="%(priv)s">privacy policy</a>.',
  cta_b='Get in touch',
  groups=[
   ('start', '🚀', 'Getting started', [
    ('How do I create my account?', ['On the app\'s first screen, tap "Sign up", enter your name, e-mail and a password of at least 8 characters, with letters and numbers, and repeat it in the "Confirm password" field. You get an e-mail to confirm the sign-up; then just sign in.']),
    ('I did not get the confirmation e-mail', ['Wait a few minutes and check your spam or junk folder. The e-mail comes from "Supabase Auth", the service that handles sign-in. If it still does not arrive, write to us with the e-mail you used.']),
    ('The e-mail link says it expired or was already used', ['The confirmation link is valid for a short time and works only once. Some e-mail providers "open" the link before you do, to check it is safe, and that uses it up. Try signing in with your e-mail and password: if the sign-up is already confirmed, it will work. If not, sign up again or write to us.', 'When you confirm, the link takes you back to the app, which shows "E-mail confirmed! Now just sign in".']),
    ('Can I use it without an account?', ['Yes. On the sign-in screen, tap "Use without an account". The app warns you and then works normally, but your lists are saved only on this device and in this browser, with nothing sent to the internet. There is no sharing and no copy on another device. If you clear the browser data or the site cache, or uninstall the app, the lists are lost with no way to recover them. The "Update app" button does not erase the lists.', 'To keep them safe and share them, create an account: tap "Create account" in the yellow notice at the top. When you sign in on this same device, the app shows a green "Import" notice: the no-account lists are copied to your account, and you choose whether to keep or remove the copies here. If you tap "Not now", the notice comes back the next time you open the app.']),
    ('How do I install it on my phone?', ['On Android (Chrome), open the app, tap the ⋮ menu and "Install app" or "Add to home screen".', 'On iPhone (Safari), tap Share and "Add to Home Screen".']),
    ('Where can I see the usage tips again?', ['Tap the 💡 icon at the top of the "My lists" screen and of the list. All the tips are there, and the "Show the tips again" button makes the notices appear on their own again.']),
    ('Can I change the app language?', ['Yes. The app comes in English, Portuguese and Spanish and starts in your device language. To switch, use the language selector on the sign-in screen or at the top of the "My lists" screen.']),
   ]),
   ('lists', '🛒', 'Lists and items', [
    ('How do I create a list?', ['On the "My lists" screen, type a name, like "Monthly groceries", and tap "Create".']),
    ('How do I add, edit and check items?', ['Inside the list, type the name in "Add item…", pick the category (the app suggests one) and, if you like, enter quantity and price. Tap "Add".', 'To mark an item as bought, tap its checkbox. To edit, tap the name. To remove it, tap the ✕.']),
    ('How do I set item prices?', ['Enter the price of one unit in the "Unit price (R$)" field, when adding the item or editing it. The app multiplies it by the quantity: 6 items at R$6.40 show as R$38.40. The total shows inside the list and on its card. With no quantity, the app counts 1.']),
    ('How do I see how much is already in the cart?', ['The bar at the top of the list shows, on the left, the value of the items already checked ("In cart", with the count, like 2/8) and, on the right, the total of the whole list. The thin bar below shows how much of the list is already in the cart. Everyone sharing the list sees the same values in real time, so nobody picks a duplicate.']),
    ('How do I clear the items already bought?', ['In the list, tap "Clear bought", next to the "Bought" heading. This removes only the checked items, for every member.']),
    ('How do I rename a list?', ['Open the list, tap the people icon (👥), change the name in the field at the top and tap "Save". Only the list owner can rename it. It also works with no signal.']),
    ('How do I delete a list?', ['Open the list, tap the people icon (👥) and "Delete list". This deletes the list and all its items for every member and cannot be undone. Only the owner sees this button.']),
   ]),
   ('share', '🤝', 'Sharing', [
    ('How do I share a list?', ['Open the list, tap the people icon (👥), enter the e-mail of who will join and tap "Share". Only the list owner can share it.']),
    ('It says "No registered user with this e-mail"', ['That means no account exists with that e-mail. The person needs to create an account in the app first, with that same e-mail. Then share again.']),
    ('How do I remove someone from the list?', ['Open the list, tap 👥 and "Remove" next to the name. Only the owner can remove members.']),
    ('How do I leave a list that was shared with me?', ['Open the list, tap 👥 and "Leave list". This removes only you; the list stays for the others.']),
   ]),
   ('account', '🔒', 'Account and data', [
    ('The app says the e-mail is already registered', ['That e-mail already has an account. The password you typed when signing up is ignored and the account keeps its previous password. Tap "Sign in" and use your password; if you do not remember it, use "Forgot my password".']),
    ('I forgot my password', ['On the sign-in screen, tap "Forgot my password", enter your e-mail and tap "Send link". Open the e-mail you receive (check spam too) and tap the link: the app opens and asks for the new password, twice. Use at least 8 characters, with letters and numbers.', 'The link is valid for a short time and works only once. If it expires, ask for another.']),
    ('How do I delete my account and my data?', ['Write to us from the registered e-mail asking for deletion. See the <a href="%(priv)s">privacy policy</a> to know what is deleted.']),
    ('The app looks outdated or odd. What do I do?', ['Tap "↻ Update app" at the bottom of the "My lists" screen or the sign-in screen. It downloads the newest version and reloads the app, with no need to switch browsers. Your account, your lists and the changes waiting for signal are not erased. You need to be online.']),
    ('Does it work offline?', ['You can view the last saved version of your lists, check and uncheck, add, edit and remove items, and also clear the bought ones. The changes are kept on the device (items with a pending change show a ⏳), a "waiting for signal" notice appears, and everything is sent automatically, in the same order, when the connection returns.', 'Creating, renaming, deleting and leaving a list also work with no signal. Sharing the list and changing members still need a connection (a list created with no signal can only be shared after it has been sent). If someone else changes the same item while you have no signal, the change that arrives last wins.']),
   ]),
  ]),
 'es': dict(
  title='Ayuda',
  intro='Respuestas rápidas sobre <strong>Lista de Compras</strong>. ¿Dudas sobre Preço Certo? Mira la <a href="%(pc)s">página de la app</a>.',
  search='Buscar una pregunta…', empty='No se encontraron preguntas. Prueba otra palabra o escríbenos.',
  count=('pregunta', 'preguntas'),
  cta_t='¿No encontraste lo que buscabas?',
  cta_p='Escríbenos y respondemos por correo. Para solicitudes sobre tus datos, mira también la <a href="%(priv)s">política de privacidad</a>.',
  cta_b='Escríbenos',
  groups=[
   ('start', '🚀', 'Primeros pasos', [
    ('¿Cómo creo mi cuenta?', ['En la pantalla inicial de la app, toca "Regístrate", escribe nombre, correo y una contraseña de al menos 8 caracteres, con letras y números, y repítela en el campo "Confirmar contraseña". Recibes un correo para confirmar el registro; después solo inicia sesión.']),
    ('No recibí el correo de confirmación', ['Espera unos minutos y revisa la carpeta de spam o correo no deseado. El correo llega de "Supabase Auth", el servicio que gestiona el inicio de sesión. Si sigue sin llegar, escríbenos con el correo que usaste.']),
    ('El enlace del correo dice que expiró o ya se usó', ['El enlace de confirmación vale por poco tiempo y solo funciona una vez. Algunos proveedores de correo "abren" el enlace antes que tú, para comprobar que es seguro, y eso lo gasta. Intenta iniciar sesión con tu correo y contraseña: si el registro ya está confirmado, funcionará. Si no, regístrate de nuevo o escríbenos.', 'Al confirmar, el enlace te lleva de vuelta a la app, que muestra "¡Correo confirmado! Ahora solo inicia sesión".']),
    ('¿Puedo usarla sin crear una cuenta?', ['Sí. En la pantalla de inicio de sesión, toca "Usar sin cuenta". La app te avisa y luego funciona con normalidad, pero tus listas se guardan solo en este dispositivo y en este navegador, sin enviar nada a internet. No hay compartir ni copia en otro dispositivo. Si borras los datos o la caché del navegador/del sitio, o desinstalas la app, las listas se pierden, sin forma de recuperarlas. El botón "Actualizar app" no borra las listas.', 'Para guardarlas con seguridad y compartirlas, crea una cuenta: toca "Crear cuenta" en el aviso amarillo de arriba. Al iniciar sesión en este mismo dispositivo, la app muestra un aviso verde "Importar": las listas del modo sin cuenta se copian a tu cuenta y eliges si conservas o quitas las copias de aquí. Si tocas "Ahora no", el aviso vuelve la próxima vez que abras la app.']),
    ('¿Cómo la instalo en el celular?', ['En Android (Chrome), abre la app, toca el menú ⋮ y "Instalar app" o "Añadir a la pantalla de inicio".', 'En iPhone (Safari), toca Compartir y "Añadir a pantalla de inicio".']),
    ('¿Dónde veo de nuevo los consejos de uso?', ['Toca el ícono 💡 en la parte de arriba de las pantallas "Mis listas" y de la lista. Ahí están todos los consejos, y el botón "Mostrar los consejos de nuevo" hace que los avisos vuelvan a aparecer solos.']),
    ('¿Puedo cambiar el idioma de la app?', ['Sí. La app existe en inglés, portugués y español y empieza en el idioma de tu dispositivo. Para cambiarlo, usa el selector de idioma en la pantalla de inicio de sesión o en la parte de arriba de "Mis listas".']),
   ]),
   ('lists', '🛒', 'Listas y artículos', [
    ('¿Cómo creo una lista?', ['En la pantalla "Mis listas", escribe un nombre, como "Compra del mes", y toca "Crear".']),
    ('¿Cómo agrego, edito y marco artículos?', ['Dentro de la lista, escribe el nombre en "Agregar artículo…", elige la categoría (la app sugiere una) y, si quieres, indica cantidad y precio. Toca "Agregar".', 'Para marcarlo como comprado, toca el cuadradito del artículo. Para editar, toca el nombre. Para quitarlo, toca la ✕.']),
    ('¿Cómo indico el precio de los artículos?', ['Indica el precio de una unidad en el campo "Precio unitario (R$)", al agregar el artículo o al editarlo. La app lo multiplica por la cantidad: 6 artículos de R$ 6,40 aparecen como R$ 38,40. El total aparece dentro de la lista y en su tarjeta. Sin cantidad, la app cuenta 1.']),
    ('¿Cómo veo cuánto ya está en el carrito?', ['La barra de arriba de la lista muestra, a la izquierda, el valor de los artículos ya marcados ("En el carrito", con la cuenta, como 2/8) y, a la derecha, el total de toda la lista. La barrita de abajo muestra cuánto de la lista ya fue al carrito. Quien comparte la lista ve los mismos valores en tiempo real, así nadie toma un artículo repetido.']),
    ('¿Cómo limpio los artículos ya comprados?', ['En la lista, toca "Limpiar comprados", junto al título "Comprados". Esto quita solo los artículos marcados, para todos los participantes.']),
    ('¿Cómo renombro una lista?', ['Abre la lista, toca el ícono de personas (👥), cambia el nombre en el campo de arriba y toca "Guardar". Solo el dueño de la lista puede renombrarla. También funciona sin señal.']),
    ('¿Cómo elimino una lista?', ['Abre la lista, toca el ícono de personas (👥) y "Eliminar lista". Esto borra la lista y todos sus artículos para todos los participantes y no se puede deshacer. Solo el dueño ve este botón.']),
   ]),
   ('share', '🤝', 'Compartir', [
    ('¿Cómo comparto una lista?', ['Abre la lista, toca el ícono de personas (👥), escribe el correo de quien va a participar y toca "Compartir". Solo el dueño de la lista puede compartirla.']),
    ('Aparece "No hay ningún usuario registrado con este correo"', ['Significa que no existe una cuenta con ese correo. La persona debe crear antes la cuenta en la app, con ese mismo correo. Luego comparte de nuevo.']),
    ('¿Cómo quito a alguien de la lista?', ['Abre la lista, toca 👥 y "Quitar" junto al nombre. Solo el dueño puede quitar participantes.']),
    ('¿Cómo salgo de una lista que compartieron conmigo?', ['Abre la lista, toca 👥 y "Salir de la lista". Esto te quita solo a ti; la lista sigue para los demás.']),
   ]),
   ('account', '🔒', 'Cuenta y datos', [
    ('La app dice que el correo ya está registrado', ['Ese correo ya tiene cuenta. La contraseña que escribiste al registrarte se ignora y la cuenta mantiene su contraseña anterior. Toca "Iniciar sesión" y usa tu contraseña; si no la recuerdas, usa "Olvidé mi contraseña".']),
    ('Olvidé mi contraseña', ['En la pantalla de inicio de sesión, toca "Olvidé mi contraseña", escribe tu correo y toca "Enviar enlace". Abre el correo que recibas (revisa también el spam) y toca el enlace: la app se abre y pide la contraseña nueva, dos veces. Usa al menos 8 caracteres, con letras y números.', 'El enlace vale por poco tiempo y solo funciona una vez. Si expira, pide otro.']),
    ('¿Cómo elimino mi cuenta y mis datos?', ['Escríbenos desde el correo registrado pidiendo la eliminación. Mira la <a href="%(priv)s">política de privacidad</a> para saber qué se borra.']),
    ('La app se ve desactualizada o rara. ¿Qué hago?', ['Toca "↻ Actualizar app" al final de la pantalla "Mis listas" o de la pantalla de inicio de sesión. Descarga la versión más nueva y recarga la app, sin necesidad de cambiar de navegador. Tu cuenta, tus listas y los cambios que esperan señal no se borran. Hay que estar conectado.']),
    ('¿Funciona sin internet?', ['Puedes consultar la última versión guardada de tus listas, marcar y desmarcar, agregar, editar y quitar artículos, y también limpiar los comprados. Los cambios quedan guardados en el dispositivo (los artículos con un cambio pendiente muestran ⏳), aparece el aviso "esperando señal" y todo se envía solo, en el mismo orden, cuando vuelve la conexión.', 'Crear, renombrar, eliminar y salir de una lista también funcionan sin señal. Compartir la lista y cambiar participantes aún necesitan conexión (una lista creada sin señal solo se puede compartir después de enviada). Si otra persona cambia el mismo artículo mientras no tienes señal, vale el cambio que llegue al final.']),
   ]),
  ]),
}


def build_help(lang, links):
    d = DATA[lang]
    fmt = lambda s: s % links
    one, many = d['count']
    chips = ''.join('<li><a href="#%s">%s %s</a></li>' % (gid, ico, name) for gid, ico, name, _ in d['groups'])
    groups = []
    for gid, ico, name, qs in d['groups']:
        items = '\n'.join(
            '      <details><summary>%s</summary>\n        %s</details>' % (
                q, '\n        '.join('<p>%s</p>' % fmt(p) for p in ps))
            for q, ps in qs)
        n = len(qs)
        groups.append(
            '  <section class="faq-group" id="%s">\n    <h2><span class="ico">%s</span>%s<span class="count">%d %s</span></h2>\n'
            '    <div class="faq-list">\n%s\n    </div>\n  </section>' % (gid, ico, name, n, one if n == 1 else many, items))
    return CSS + ('\n  <h1 class="page">%s</h1>\n  <p class="intro">%s</p>\n\n'
            '  <input class="help-search" id="help-q" type="search" placeholder="%s" aria-label="%s">\n'
            '  <ul class="topics">%s</ul>\n\n%s\n\n'
            '  <p class="help-empty" id="help-empty">%s</p>\n\n'
            '  <div class="box help-cta">\n    <h3>%s</h3>\n    <p>%s</p>\n    <p style="margin-top:12px"><a class="button" href="%s">%s</a></p>\n  </div>\n%s') % (
        d['title'], fmt(d['intro']), d['search'], d['search'], chips, '<div class="faq-cols">\n' + '\n\n'.join(groups) + '\n</div>', d['empty'],
        d['cta_t'], fmt(d['cta_p']), links['contact'], d['cta_b'], SCRIPT)
