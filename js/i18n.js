// Traduções do app (pt-BR é o padrão; idiomas sem tradução caem em inglês). As categorias são guardadas no banco com
// o nome em português (chave); aqui só mudam os rótulos exibidos.
export const LANGS = ['pt', 'en', 'es'];
export const LANG_NAMES = { en: 'English', pt: 'Português', es: 'Español' };
const KEY = 'lc:lang';
const HTML_LANG = { en: 'en', pt: 'pt-BR', es: 'es' };
// Os locales es-* do Intl não exibem o símbolo R$ para BRL; usamos o formato pt-BR (vírgula decimal, "R$ 1.234,60").
const NUM_LOCALE = { en: 'en-US', pt: 'pt-BR', es: 'pt-BR' };

function detect() {
  try { const s = localStorage.getItem(KEY); if (LANGS.includes(s)) return s; } catch { /* ignore */ }
  const list = (navigator.languages && navigator.languages.length) ? navigator.languages : [navigator.language || 'en'];
  for (const l of list) { const c = String(l).slice(0, 2).toLowerCase(); if (LANGS.includes(c)) return c; }
  return 'en';
}

let lang = detect();
document.documentElement.lang = HTML_LANG[lang];

export const getLang = () => lang;
export function setLang(l) {
  if (!LANGS.includes(l)) return;
  lang = l;
  try { localStorage.setItem(KEY, l); } catch { /* ignore */ }
  document.documentElement.lang = HTML_LANG[l];
}
export const numLocale = () => NUM_LOCALE[lang];
export const decimalSep = () => (lang === 'en' ? '.' : ',');

export const HELP_URL = { pt: '/listadecompras/ajuda/', en: '/listadecompras/ajuda/en/', es: '/listadecompras/ajuda/es/' };
export const PRIVACY_URL = { pt: '/listadecompras/privacy.html', en: '/listadecompras/privacy-en.html', es: '/listadecompras/privacy-es.html' };

export const CAT_LABEL = {
  en: { 'Hortifruti': 'Produce', 'Açougue': 'Butcher', 'Padaria': 'Bakery', 'Laticínios': 'Dairy', 'Limpeza': 'Cleaning', 'Mercearia': 'Pantry', 'Bebidas': 'Drinks', 'Outros': 'Other' },
  pt: { 'Hortifruti': 'Hortifruti', 'Açougue': 'Açougue', 'Padaria': 'Padaria', 'Laticínios': 'Laticínios', 'Limpeza': 'Limpeza', 'Mercearia': 'Mercearia', 'Bebidas': 'Bebidas', 'Outros': 'Outros' },
  es: { 'Hortifruti': 'Frutas y verduras', 'Açougue': 'Carnicería', 'Padaria': 'Panadería', 'Laticínios': 'Lácteos', 'Limpeza': 'Limpieza', 'Mercearia': 'Despensa', 'Bebidas': 'Bebidas', 'Outros': 'Otros' },
};

const DICT = {
  en: {
    tagline: 'Share your lists in real time',
    name: 'Your name', email: 'E-mail', password: 'Password',
    passwordNew: 'Password (min. 8, with letters and numbers)',
    passwordHint: 'At least 8 characters, with letters and numbers',
    signin: 'Sign in', signup: 'Create account',
    noAccount: 'No account? Sign up', haveAccount: 'Already have an account? Sign in',
    help: 'Help', privacy: 'Privacy policy', language: 'Language',
    accountCreated: 'Account created! Confirm your e-mail (check your inbox) and then sign in.',
    errBadLogin: 'Wrong e-mail or password.', errExists: 'This e-mail is already registered.',
    errNotConfirmed: 'Confirm your e-mail before signing in.',
    errWeak: 'Weak password: use at least 8 characters, with letters and numbers.',
    errRate: 'Too many attempts. Please wait a bit.', errNetwork: 'No connection to the server.',
    offlineBanner: '📡 No connection — you can still check items; they sync when the signal returns', online: 'Connection restored',
    queued: 'Saved on this device. It will sync when the signal returns.', pendingSync: '⏳ {n} change(s) waiting for signal', synced: 'Changes synced',
    myLists: '🛒 My lists', signout: 'Sign out', newListPh: 'New list (e.g. Monthly groceries)', create: 'Create',
    yourList: 'Your list', sharedWithYou: 'Shared with you',
    noLists: 'No lists yet.<br>Create the first one above 👆',
    errLoadLists: 'Error loading lists', errCreateList: 'Could not create the list',
    listDefault: 'List', back: 'Back', liveTitle: 'Real-time sync', shareOptions: 'Share and options',
    addItemPh: 'Add item…', category: 'Category', qtyPh: 'Qty', qtyLabel: 'Quantity', pricePh: 'Unit price (R$)', priceLabel: 'Unit price', add: 'Add',
    noConnAdd: 'No connection: cannot add right now', errAddItem: 'Error adding item', errLoadItems: 'Error loading items',
    markItem: 'Mark item', remove: 'Remove', emptyList: 'Empty list.<br>Add the first item above 👆',
    bought: '✅ Bought ({n})', clearBought: 'Clear bought', totalList: 'List total',
    noConnRetry: 'No connection: try again when you are back online', errUpdateItem: 'Error updating item',
    noConn: 'No connection', errRemoveItem: 'Error removing item',
    confirmClear: 'Remove {n} bought item(s)?', errClear: 'Error clearing bought items',
    editItem: 'Edit item', quantityPh: 'Quantity', cancel: 'Cancel', save: 'Save', errSave: 'Error saving',
    shareEmailPh: 'E-mail of who will join', share: 'Share', sharing: 'Sharing…', shared: 'List shared!',
    user: 'User', owner: 'owner', you: 'you', noMembers: 'No members',
    deleteList: 'Delete list', leaveList: 'Leave list', close: 'Close',
    errRemoveMember: 'Error removing member', confirmDelete: 'Delete this list and all its items for every member?',
    errDeleteList: 'Error deleting list', confirmLeave: 'Leave this list?', errLeave: 'Error leaving the list',
    srvOwnerOnly: 'Only the list owner can share it', srvNoUser: 'No registered user with this e-mail',
    tipsBtn: 'Tips', tipsTitle: '💡 Tips', tipOk: 'Got it', tipOff: "Don't show tips again", tipReset: 'Show the tips again',
    tip_welcome_t: 'Welcome to Lista de Compras! 👋',
    tip_welcome_b: '<ul><li><b>Create a list</b> in the field above, like "Monthly groceries".</li><li><b>Invite whoever shops with you</b> with the 👥 icon inside the list. Everyone sees the check marks instantly.</li><li><b>Install it on your phone:</b> in the browser menu ⋮ tap "Install app" (iPhone: Share → Add to Home Screen).</li></ul>',
    tip_list_t: 'How to use the list 🛒',
    tip_list_b: '<ul><li><b>Tap the checkbox</b> to mark an item as bought. Tap the <b>name</b> to edit it and the ✕ to remove it.</li><li><b>Unit price × quantity:</b> enter the price of one unit and the quantity; the app calculates the item total and the list total.</li><li><b>No signal?</b> You can still check items: they sync when the connection returns.</li></ul>',
    tip_share_t: 'Sharing the list 👥',
    tip_share_b: 'The person needs an account in the app, with the <b>same e-mail</b> you type. Members see and check items, and can leave the list whenever they want. Only you, the owner, can delete the list.',
  },
  pt: {
    tagline: 'Compartilhe suas listas em tempo real',
    name: 'Seu nome', email: 'E-mail', password: 'Senha',
    passwordNew: 'Senha (mín. 8, com letras e números)',
    passwordHint: 'Mínimo de 8 caracteres, com letras e números',
    signin: 'Entrar', signup: 'Criar conta',
    noAccount: 'Não tem conta? Cadastre-se', haveAccount: 'Já tem conta? Entrar',
    help: 'Ajuda', privacy: 'Política de privacidade', language: 'Idioma',
    accountCreated: 'Conta criada! Confirme seu e-mail (veja a caixa de entrada) e depois entre.',
    errBadLogin: 'E-mail ou senha incorretos.', errExists: 'Este e-mail já está cadastrado.',
    errNotConfirmed: 'Confirme seu e-mail antes de entrar.',
    errWeak: 'Senha fraca: use no mínimo 8 caracteres, com letras e números.',
    errRate: 'Muitas tentativas. Aguarde um pouco.', errNetwork: 'Sem conexão com o servidor.',
    offlineBanner: '📡 Sem conexão — você ainda pode marcar itens; eles sincronizam quando o sinal voltar', online: 'Conexão restabelecida',
    queued: 'Salvo no aparelho. Será enviado quando o sinal voltar.', pendingSync: '⏳ {n} alteração(ões) aguardando sinal', synced: 'Alterações sincronizadas',
    myLists: '🛒 Minhas listas', signout: 'Sair', newListPh: 'Nova lista (ex: Mercado do Mês)', create: 'Criar',
    yourList: 'Sua lista', sharedWithYou: 'Compartilhada com você',
    noLists: 'Nenhuma lista ainda.<br>Crie a primeira acima 👆',
    errLoadLists: 'Erro ao carregar listas', errCreateList: 'Não foi possível criar a lista',
    listDefault: 'Lista', back: 'Voltar', liveTitle: 'Sincronização em tempo real', shareOptions: 'Compartilhar e opções',
    addItemPh: 'Adicionar item…', category: 'Categoria', qtyPh: 'Qtd', qtyLabel: 'Quantidade', pricePh: 'Preço unitário (R$)', priceLabel: 'Preço unitário', add: 'Adicionar',
    noConnAdd: 'Sem conexão: não é possível adicionar agora', errAddItem: 'Erro ao adicionar item', errLoadItems: 'Erro ao carregar itens',
    markItem: 'Marcar item', remove: 'Remover', emptyList: 'Lista vazia.<br>Adicione o primeiro item acima 👆',
    bought: '✅ Comprados ({n})', clearBought: 'Limpar comprados', totalList: 'Total da lista',
    noConnRetry: 'Sem conexão: tente novamente quando voltar o sinal', errUpdateItem: 'Erro ao atualizar item',
    noConn: 'Sem conexão', errRemoveItem: 'Erro ao remover item',
    confirmClear: 'Remover {n} item(ns) comprado(s)?', errClear: 'Erro ao limpar comprados',
    editItem: 'Editar item', quantityPh: 'Quantidade', cancel: 'Cancelar', save: 'Salvar', errSave: 'Erro ao salvar',
    shareEmailPh: 'E-mail de quem vai participar', share: 'Compartilhar', sharing: 'Compartilhando…', shared: 'Lista compartilhada!',
    user: 'Usuário', owner: 'dono', you: 'você', noMembers: 'Sem membros',
    deleteList: 'Excluir lista', leaveList: 'Sair da lista', close: 'Fechar',
    errRemoveMember: 'Erro ao remover membro', confirmDelete: 'Excluir esta lista e todos os itens para todos os membros?',
    errDeleteList: 'Erro ao excluir lista', confirmLeave: 'Sair desta lista?', errLeave: 'Erro ao sair da lista',
    srvOwnerOnly: 'Somente o dono da lista pode compartilhá-la', srvNoUser: 'Nenhum usuário cadastrado com este e-mail',
    tipsBtn: 'Dicas', tipsTitle: '💡 Dicas', tipOk: 'Entendi', tipOff: 'Não mostrar mais dicas', tipReset: 'Mostrar as dicas de novo',
    tip_welcome_t: 'Bem-vindo ao Lista de Compras! 👋',
    tip_welcome_b: '<ul><li><b>Crie uma lista</b> no campo acima, como "Mercado do mês".</li><li><b>Convide quem compra com você</b> pelo ícone 👥 dentro da lista. Todos veem as marcações na hora.</li><li><b>Instale no celular:</b> no menu ⋮ do navegador, toque em "Instalar app" (iPhone: Compartilhar → Adicionar à Tela de Início).</li></ul>',
    tip_list_t: 'Como usar a lista 🛒',
    tip_list_b: '<ul><li><b>Toque no quadradinho</b> para marcar como comprado. Toque no <b>nome</b> para editar e no ✕ para remover.</li><li><b>Preço unitário × quantidade:</b> informe o preço de uma unidade e a quantidade; o app calcula o total do item e o da lista.</li><li><b>Sem sinal?</b> Pode marcar os itens do mesmo jeito: eles sincronizam quando a conexão voltar.</li></ul>',
    tip_share_t: 'Compartilhar a lista 👥',
    tip_share_b: 'A pessoa precisa ter uma conta no app, com o <b>mesmo e-mail</b> que você digitar. Quem participa vê e marca os itens, e pode sair da lista quando quiser. Só você, o dono, pode excluir a lista.',
  },
  es: {
    tagline: 'Comparte tus listas en tiempo real',
    name: 'Tu nombre', email: 'Correo', password: 'Contraseña',
    passwordNew: 'Contraseña (mín. 8, con letras y números)',
    passwordHint: 'Mínimo 8 caracteres, con letras y números',
    signin: 'Iniciar sesión', signup: 'Crear cuenta',
    noAccount: '¿No tienes cuenta? Regístrate', haveAccount: '¿Ya tienes cuenta? Inicia sesión',
    help: 'Ayuda', privacy: 'Política de privacidad', language: 'Idioma',
    accountCreated: '¡Cuenta creada! Confirma tu correo (revisa la bandeja de entrada) y luego inicia sesión.',
    errBadLogin: 'Correo o contraseña incorrectos.', errExists: 'Este correo ya está registrado.',
    errNotConfirmed: 'Confirma tu correo antes de iniciar sesión.',
    errWeak: 'Contraseña débil: usa al menos 8 caracteres, con letras y números.',
    errRate: 'Demasiados intentos. Espera un poco.', errNetwork: 'Sin conexión con el servidor.',
    offlineBanner: '📡 Sin conexión — aún puedes marcar artículos; se sincronizan cuando vuelva la señal', online: 'Conexión restablecida',
    queued: 'Guardado en el dispositivo. Se enviará cuando vuelva la señal.', pendingSync: '⏳ {n} cambio(s) esperando señal', synced: 'Cambios sincronizados',
    myLists: '🛒 Mis listas', signout: 'Salir', newListPh: 'Nueva lista (ej: Compra del mes)', create: 'Crear',
    yourList: 'Tu lista', sharedWithYou: 'Compartida contigo',
    noLists: 'Aún no hay listas.<br>Crea la primera arriba 👆',
    errLoadLists: 'Error al cargar las listas', errCreateList: 'No se pudo crear la lista',
    listDefault: 'Lista', back: 'Volver', liveTitle: 'Sincronización en tiempo real', shareOptions: 'Compartir y opciones',
    addItemPh: 'Agregar artículo…', category: 'Categoría', qtyPh: 'Cant.', qtyLabel: 'Cantidad', pricePh: 'Precio unitario (R$)', priceLabel: 'Precio unitario', add: 'Agregar',
    noConnAdd: 'Sin conexión: no se puede agregar ahora', errAddItem: 'Error al agregar el artículo', errLoadItems: 'Error al cargar los artículos',
    markItem: 'Marcar artículo', remove: 'Quitar', emptyList: 'Lista vacía.<br>Agrega el primer artículo arriba 👆',
    bought: '✅ Comprados ({n})', clearBought: 'Limpiar comprados', totalList: 'Total de la lista',
    noConnRetry: 'Sin conexión: inténtalo de nuevo cuando vuelva la señal', errUpdateItem: 'Error al actualizar el artículo',
    noConn: 'Sin conexión', errRemoveItem: 'Error al quitar el artículo',
    confirmClear: '¿Quitar {n} artículo(s) comprado(s)?', errClear: 'Error al limpiar los comprados',
    editItem: 'Editar artículo', quantityPh: 'Cantidad', cancel: 'Cancelar', save: 'Guardar', errSave: 'Error al guardar',
    shareEmailPh: 'Correo de quien va a participar', share: 'Compartir', sharing: 'Compartiendo…', shared: '¡Lista compartida!',
    user: 'Usuario', owner: 'dueño', you: 'tú', noMembers: 'Sin participantes',
    deleteList: 'Eliminar lista', leaveList: 'Salir de la lista', close: 'Cerrar',
    errRemoveMember: 'Error al quitar al participante', confirmDelete: '¿Eliminar esta lista y todos sus artículos para todos los participantes?',
    errDeleteList: 'Error al eliminar la lista', confirmLeave: '¿Salir de esta lista?', errLeave: 'Error al salir de la lista',
    srvOwnerOnly: 'Solo el dueño de la lista puede compartirla', srvNoUser: 'No hay ningún usuario registrado con este correo',
    tipsBtn: 'Consejos', tipsTitle: '💡 Consejos', tipOk: 'Entendido', tipOff: 'No mostrar más consejos', tipReset: 'Mostrar los consejos de nuevo',
    tip_welcome_t: '¡Bienvenido a Lista de Compras! 👋',
    tip_welcome_b: '<ul><li><b>Crea una lista</b> en el campo de arriba, como "Compra del mes".</li><li><b>Invita a quien compra contigo</b> con el ícono 👥 dentro de la lista. Todos ven las marcas al instante.</li><li><b>Instálala en el celular:</b> en el menú ⋮ del navegador toca "Instalar app" (iPhone: Compartir → Añadir a pantalla de inicio).</li></ul>',
    tip_list_t: 'Cómo usar la lista 🛒',
    tip_list_b: '<ul><li><b>Toca el cuadradito</b> para marcar como comprado. Toca el <b>nombre</b> para editar y la ✕ para quitar.</li><li><b>Precio unitario × cantidad:</b> indica el precio de una unidad y la cantidad; la app calcula el total del artículo y el de la lista.</li><li><b>¿Sin señal?</b> Puedes marcar los artículos igual: se sincronizan cuando vuelva la conexión.</li></ul>',
    tip_share_t: 'Compartir la lista 👥',
    tip_share_b: 'La persona necesita una cuenta en la app, con el <b>mismo correo</b> que escribas. Quien participa ve y marca los artículos, y puede salir de la lista cuando quiera. Solo tú, el dueño, puedes eliminar la lista.',
  },
};

export function t(key, vars) {
  let s = (DICT[lang] && DICT[lang][key]) ?? DICT.en[key] ?? key;
  if (vars) for (const k of Object.keys(vars)) s = s.split('{' + k + '}').join(vars[k]);
  return s;
}
