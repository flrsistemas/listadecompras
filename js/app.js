import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/+esm';
import { SUPABASE_URL, SUPABASE_ANON_KEY } from './config.js';
import { t, getLang, setLang, LANGS, LANG_NAMES, CAT_LABEL, HELP_URL, PRIVACY_URL, numLocale, decimalSep } from './i18n.js';

/* ------------------------------ Utilidades ------------------------------ */
const $ = (s, r = document) => r.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// As chaves das categorias ficam em português no banco; só o rótulo muda por idioma.
const CATS = {
  'Hortifruti': '🥬', 'Açougue': '🥩', 'Padaria': '🥖', 'Laticínios': '🧀',
  'Limpeza': '🧴', 'Mercearia': '🥫', 'Bebidas': '🥤', 'Outros': '🛒',
};
const CAT_ORDER = Object.keys(CATS);
const catLabel = (c) => (CAT_LABEL[getLang()] || CAT_LABEL.en)[c] || c;

// Palavras-chave (pt, en, es) para sugerir a categoria automaticamente
const GUESS = {
  'Hortifruti': ['banana', 'maçã', 'maca', 'laranja', 'limão', 'limao', 'tomate', 'cebola', 'alho', 'batata', 'cenoura', 'alface', 'fruta', 'verdura', 'mamão', 'uva', 'abacate', 'pepino', 'brócolis', 'couve',
    'apple', 'orange', 'lemon', 'tomato', 'onion', 'garlic', 'potato', 'carrot', 'lettuce', 'fruit', 'vegetable', 'grape', 'avocado', 'cucumber', 'broccoli',
    'manzana', 'naranja', 'limón', 'cebolla', 'ajo', 'papa', 'patata', 'zanahoria', 'lechuga', 'aguacate', 'brócoli', 'plátano'],
  'Açougue': ['carne', 'frango', 'linguiça', 'linguica', 'picanha', 'peixe', 'bife', 'costela', 'bacon', 'salsicha', 'fígado', 'patinho', 'alcatra', 'contra',
    'meat', 'chicken', 'sausage', 'fish', 'beef', 'steak', 'ribs', 'pork',
    'pollo', 'salchicha', 'pescado', 'bistec', 'costilla', 'cerdo'],
  'Padaria': ['pão', 'pao', 'bolo', 'biscoito', 'bolacha', 'torrada', 'bisnaga',
    'bread', 'cake', 'cookie', 'biscuit', 'toast', 'pan', 'pastel', 'galleta', 'tostada'],
  'Laticínios': ['leite', 'queijo', 'iogurte', 'manteiga', 'requeijão', 'requeijao', 'creme de leite', 'presunto', 'mussarela', 'ovo', 'margarina',
    'milk', 'cheese', 'yogurt', 'yoghurt', 'butter', 'cream', 'egg', 'margarine',
    'leche', 'queso', 'yogur', 'mantequilla', 'crema', 'jamón', 'jamon', 'huevo'],
  'Limpeza': ['sabão', 'sabao', 'detergente', 'desinfetante', 'amaciante', 'esponja', 'papel higiênico', 'papel higienico', 'shampoo', 'sabonete', 'água sanitária', 'lixo', 'cloro',
    'soap', 'detergent', 'disinfectant', 'softener', 'sponge', 'toilet paper', 'bleach', 'trash',
    'jabón', 'jabon', 'desinfectante', 'suavizante', 'esponja', 'papel higiénico', 'champú', 'lejía', 'basura'],
  'Mercearia': ['arroz', 'feijão', 'feijao', 'macarrão', 'macarrao', 'açúcar', 'acucar', 'sal', 'óleo', 'oleo', 'farinha', 'café', 'cafe', 'molho', 'milho', 'azeite', 'cereal', 'aveia',
    'rice', 'beans', 'pasta', 'sugar', 'salt', 'oil', 'flour', 'coffee', 'sauce', 'corn', 'oats',
    'frijol', 'frijoles', 'azúcar', 'aceite', 'harina', 'salsa', 'maíz', 'avena'],
  'Bebidas': ['suco', 'refrigerante', 'cerveja', 'vinho', 'água', 'agua', 'coca', 'guaraná', 'guarana', 'energético', 'chá',
    'juice', 'soda', 'beer', 'wine', 'water', 'tea', 'energy drink',
    'jugo', 'refresco', 'cerveza', 'vino', 'té'],
};
const fold = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
function guessCategory(name) {
  const n = fold(name);
  const tokens = n.split(/[^a-z0-9]+/).filter(Boolean);
  for (const [cat, words] of Object.entries(GUESS)) {
    const hit = words.some((w0) => {
      const w = fold(w0);
      if (w.includes(' ')) return n.includes(w);
      return w.length <= 3 ? tokens.includes(w) : tokens.some((tk) => tk.startsWith(w));
    });
    if (hit) return cat;
  }
  return null;
}

let brl = null;
let brlLang = '';
function money(v) {
  if (!brl || brlLang !== getLang()) { brl = new Intl.NumberFormat(numLocale(), { style: 'currency', currency: 'BRL' }); brlLang = getLang(); }
  return brl.format(Number(v) || 0);
}
// Aceita "12,50", "12.50" e "1.234,56"; vazio/inválido => null
function parsePrice(s) {
  let x = String(s ?? '').trim().replace(/[^\d.,]/g, '');
  if (!x) return null;
  if (x.includes(',')) x = x.replace(/\./g, '').replace(',', '.');
  const n = Number(x);
  return Number.isFinite(n) && n >= 0 ? Math.round(n * 100) / 100 : null;
}
// Campos numéricos: só dígitos e um separador decimal (vírgula ou ponto)
const cleanNum = (v) => {
  let x = String(v ?? '').replace(/[^\d.,]/g, '');
  const i = x.search(/[.,]/);
  if (i >= 0) x = x.slice(0, i + 1) + x.slice(i + 1).replace(/[.,]/g, '');
  return x;
};
function bindNumeric(root) {
  root.querySelectorAll('[data-num]').forEach((el) => {
    el.addEventListener('input', () => { const c = cleanNum(el.value); if (c !== el.value) el.value = c; });
  });
}
// Quantidade numérica ("2", "1,5" ou "1.5"); vazio/inválido => null
function parseQty(s) {
  const x = cleanNum(s).replace(/^[.,]+|[.,]+$/g, '');
  return x && Number(x.replace(',', '.')) > 0 ? x.replace(/[.,]/, decimalSep()) : null;
}
const priceInput = (v) => (v == null ? '' : String(v).replace('.', decimalSep()));
const sumPrices = (items) => Math.round(items.reduce((s, i) => s + (Number(i.price) || 0), 0) * 100) / 100;

function toast(msg, isErr = false) {
  const el = $('#toast');
  el.textContent = msg;
  el.className = 'toast' + (isErr ? ' err' : '');
  el.hidden = false;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => (el.hidden = true), 3200);
}

const store = {
  get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* quota/privado */ } },
  del(k) { try { localStorage.removeItem(k); } catch { /* ignore */ } },
};

/* ------------------------------ Estado ---------------------------------- */
const state = {
  user: null,
  lists: [],
  listId: null,
  items: [],
  members: [],
  totals: {},
  authMode: 'login',
  channels: [],
  live: false,
};

const app = $('#app');
const dlg = $('#dlg');

const configured = SUPABASE_URL.startsWith('http') && !SUPABASE_ANON_KEY.startsWith('COLE_');
if (!configured) {
  app.innerHTML = `<div class="card" style="padding:20px;margin-top:10vh">
    <h1>⚙️ Setup pending</h1>
    <p>Open <code>js/config.js</code> and fill in <code>SUPABASE_URL</code> and <code>SUPABASE_ANON_KEY</code>.</p></div>`;
  throw new Error('Supabase not configured (js/config.js)');
}

const sb = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: false },
});

/* ------------------------------ Idioma ---------------------------------- */
function langSelectHtml() {
  return `<select class="lang-sel" id="lang-sel" aria-label="${esc(t('language'))}">
    ${LANGS.map((l) => `<option value="${l}" ${l === getLang() ? 'selected' : ''}>${LANG_NAMES[l]}</option>`).join('')}
  </select>`;
}
function bindLangSelect() {
  const sel = $('#lang-sel');
  if (!sel) return;
  sel.onchange = () => { setLang(sel.value); updateBanner(); route(); };
}

/* ------------------------------ Offline --------------------------------- */
function updateBanner() {
  const b = $('#banner');
  b.hidden = navigator.onLine;
  b.textContent = t('offlineBanner');
}
window.addEventListener('online', () => { updateBanner(); route(); toast(t('online')); });
window.addEventListener('offline', updateBanner);

/* ------------------------------ Auth ------------------------------------ */
async function init() {
  updateBanner();
  const { data: { session } } = await sb.auth.getSession();
  state.user = session?.user ?? null;

  sb.auth.onAuthStateChange((event, sess) => {
    const newId = sess?.user?.id ?? null;
    if (newId === (state.user?.id ?? null)) return; // ignora TOKEN_REFRESHED etc.
    state.user = sess?.user ?? null;
    if (!state.user) { teardownRealtime(); state.lists = []; }
    route();
  });

  window.addEventListener('hashchange', route);
  route();
}

function renderAuth(info = '', isErr = false) {
  const login = state.authMode === 'login';
  const L = getLang();
  app.innerHTML = `
  <section class="auth">
    <img class="logo" src="icons/icon.svg" alt="">
    <h1>Lista de Compras</h1>
    <p class="sub">${esc(t('tagline'))}</p>
    <form class="card" id="auth-form">
      ${login ? '' : `<input name="nome" placeholder="${esc(t('name'))}" autocomplete="name" required>`}
      <input name="email" type="email" placeholder="${esc(t('email'))}" autocomplete="email" required>
      <input name="password" type="password" placeholder="${esc(login ? t('password') : t('passwordNew'))}"
             ${login ? '' : `minlength="8" pattern="(?=.*[A-Za-z])(?=.*\\d).{8,}" title="${esc(t('passwordHint'))}"`}
             autocomplete="${login ? 'current-password' : 'new-password'}" required>
      ${info ? `<div class="msg ${isErr ? 'err' : ''}">${esc(info)}</div>` : ''}
      <button class="primary" type="submit">${esc(login ? t('signin') : t('signup'))}</button>
    </form>
    <button class="switch" id="switch-mode" type="button">
      ${esc(login ? t('noAccount') : t('haveAccount'))}
    </button>
    <p class="sub"><a href="${HELP_URL[L]}" target="_blank" rel="noopener">${esc(t('help'))}</a> &middot; <a href="${PRIVACY_URL[L]}" target="_blank" rel="noopener">${esc(t('privacy'))}</a></p>
    <p class="sub">${langSelectHtml()}</p>
  </section>`;

  bindLangSelect();
  $('#switch-mode').onclick = () => { state.authMode = login ? 'signup' : 'login'; renderAuth(); };
  $('#auth-form').onsubmit = async (e) => {
    e.preventDefault();
    const f = new FormData(e.target);
    const email = f.get('email').trim();
    const password = f.get('password');
    const btn = e.target.querySelector('button');
    btn.disabled = true;
    try {
      if (login) {
        const { error } = await sb.auth.signInWithPassword({ email, password });
        if (error) throw error;
      } else {
        const { data, error } = await sb.auth.signUp({
          email, password,
          options: { data: { nome: f.get('nome').trim() } },
        });
        if (error) throw error;
        if (!data.session) {
          state.authMode = 'login';
          renderAuth(t('accountCreated'));
        }
      }
    } catch (err) {
      renderAuth(translateError(err), true);
    }
  };
}

function translateError(err) {
  const m = err?.message || String(err);
  if (/Invalid login/i.test(m)) return t('errBadLogin');
  if (/already registered/i.test(m)) return t('errExists');
  if (/Email not confirmed/i.test(m)) return t('errNotConfirmed');
  if (/password.*(at least|characters|weak|contain)|weak_password/i.test(m)) return t('errWeak');
  if (/rate limit/i.test(m)) return t('errRate');
  if (/fetch|network/i.test(m)) return t('errNetwork');
  return m;
}
// Mensagens que o banco devolve (em português) viram texto no idioma atual
function translateServerMsg(m) {
  if (/Somente o dono/i.test(m)) return t('srvOwnerOnly');
  if (/Nenhum usu[aá]rio/i.test(m)) return t('srvNoUser');
  return m;
}

async function logout() {
  teardownRealtime();
  await sb.auth.signOut();
}

/* ------------------------------ Roteamento ------------------------------ */
function route() {
  if (!state.user) { teardownRealtime(); return renderAuth(); }
  const m = location.hash.match(/^#\/list\/([0-9a-f-]+)/i);
  if (m) openList(m[1]); else showLists();
}

/* ------------------------------ Listas ---------------------------------- */
const listsKey = () => `lc:lists:${state.user.id}`;
const itemsKey = (id) => `lc:items:${id}`;
const membersKey = (id) => `lc:members:${id}`;
const totalsKey = () => `lc:totals:${state.user.id}`;

async function showLists() {
  teardownItemsChannel();
  state.listId = null;
  state.lists = store.get(listsKey()) || state.lists;
  state.totals = store.get(totalsKey()) || state.totals;
  renderLists();
  await loadLists();
  setupListsChannel();
}

async function loadLists() {
  const [lr, ir] = await Promise.all([
    sb.from('shopping_lists').select('*').order('created_at', { ascending: false }),
    sb.from('shopping_items').select('list_id, price'),
  ]);
  if (lr.error) { if (navigator.onLine) toast(t('errLoadLists'), true); return; }
  state.lists = lr.data;
  store.set(listsKey(), lr.data);
  if (!ir.error) {
    const totals = {};
    for (const r of ir.data) totals[r.list_id] = (totals[r.list_id] || 0) + (Number(r.price) || 0);
    state.totals = totals;
    store.set(totalsKey(), totals);
  }
  if (!state.listId) renderLists();
}

function renderLists() {
  const me = state.user.id;
  app.innerHTML = `
  <div class="topbar">
    <h1>${esc(t('myLists'))}</h1>
    ${langSelectHtml()}
    <button class="ghost" id="logout" title="${esc(t('signout'))}">${esc(t('signout'))}</button>
  </div>
  <form class="newlist" id="newlist">
    <input name="name" placeholder="${esc(t('newListPh'))}" maxlength="80" required>
    <button class="primary" type="submit">${esc(t('create'))}</button>
  </form>
  <div class="list-cards">
    ${state.lists.length ? state.lists.map((l) => `
      <button class="list-card" data-open="${l.id}">
        <span class="ico">${l.owner_id === me ? '📋' : '🤝'}</span>
        <span class="grow"><span class="name">${esc(l.name)}</span><br>
          <span class="meta">${esc(l.owner_id === me ? t('yourList') : t('sharedWithYou'))}</span></span>
        <span class="total">${money(Math.round((state.totals[l.id] || 0) * 100) / 100)}</span>
        <span>›</span>
      </button>`).join('') : `<div class="empty">${t('noLists')}</div>`}
  </div>`;

  bindLangSelect();
  $('#logout').onclick = logout;
  $('#newlist').onsubmit = async (e) => {
    e.preventDefault();
    const name = new FormData(e.target).get('name').trim();
    if (!name) return;
    const { data, error } = await sb.from('shopping_lists').insert({ name, owner_id: state.user.id }).select().single();
    if (error) return toast(t('errCreateList'), true);
    location.hash = `#/list/${data.id}`;
  };
  app.querySelectorAll('[data-open]').forEach((b) => (b.onclick = () => (location.hash = `#/list/${b.dataset.open}`)));
}

function setupListsChannel() {
  teardownRealtime();
  const ch = sb.channel('lists-' + state.user.id)
    .on('postgres_changes', { event: '*', schema: 'public', table: 'list_members' }, () => { if (!state.listId) loadLists(); })
    .on('postgres_changes', { event: '*', schema: 'public', table: 'shopping_items' }, () => { if (!state.listId) loadLists(); })
    .subscribe();
  state.channels.push(ch);
}

/* ------------------------------ Lista aberta ---------------------------- */
async function openList(id) {
  teardownRealtime();
  state.listId = id;
  state.items = store.get(itemsKey(id)) || [];
  state.members = store.get(membersKey(id)) || [];
  if (!state.lists.length) state.lists = store.get(listsKey()) || [];
  renderListShell();
  renderItems();

  await Promise.all([loadItems(), loadMembers(), state.lists.some((l) => l.id === id) ? null : loadLists()]);
  if (state.listId !== id) return;
  renderListShell(true); // atualiza título/permissões sem perder foco do formulário
  setupItemsChannel(id);
}

const currentList = () => state.lists.find((l) => l.id === state.listId);
const isOwner = () => currentList()?.owner_id === state.user.id;

async function loadItems() {
  const id = state.listId;
  const { data, error } = await sb.from('shopping_items').select('*').eq('list_id', id);
  if (error) { if (navigator.onLine) toast(t('errLoadItems'), true); return; }
  applyItems(id, data);
}
function applyItems(id, data) {
  if (state.listId !== id) return;
  state.items = data;
  store.set(itemsKey(id), data);
  renderItems();
}

async function loadMembers() {
  const id = state.listId;
  const { data, error } = await sb.from('list_members').select('user_id, profiles(email, nome)').eq('list_id', id);
  if (error || state.listId !== id) return;
  state.members = data;
  store.set(membersKey(id), data);
}

function renderListShell(soft = false) {
  const l = currentList();
  if (soft && $('#items')) {
    $('#list-title').textContent = l ? l.name : t('listDefault');
    return;
  }
  app.innerHTML = `
  <div class="topbar">
    <button class="icon ghost" id="back" aria-label="${esc(t('back'))}">←</button>
    <h1 id="list-title">${esc(l ? l.name : t('listDefault'))}</h1>
    <span class="live ${state.live ? 'on' : ''}" id="live" title="${esc(t('liveTitle'))}"></span>
    <button class="icon ghost" id="share" aria-label="${esc(t('shareOptions'))}">👥</button>
  </div>
  <form class="card add-form" id="add-form" autocomplete="off">
    <input class="name" name="name" placeholder="${esc(t('addItemPh'))}" maxlength="120" required enterkeyhint="done">
    <select name="category" aria-label="${esc(t('category'))}">
      ${CAT_ORDER.map((c) => `<option value="${c}">${CATS[c]} ${esc(catLabel(c))}</option>`).join('')}
    </select>
    <input name="quantity" data-num placeholder="${esc(t('qtyPh'))}" inputmode="decimal" maxlength="8" style="grid-column:2/3;grid-row:2" aria-label="${esc(t('qtyLabel'))}">
    <input name="price" data-num placeholder="${esc(t('pricePh'))}" inputmode="decimal" maxlength="12" style="grid-column:1/2;grid-row:3" aria-label="${esc(t('priceLabel'))}">
    <button class="primary" type="submit" style="grid-column:2/3;grid-row:3">${esc(t('add'))}</button>
  </form>
  <div class="total-bar" id="total-bar"></div>
  <div id="items"></div>`;

  bindNumeric(app);
  $('#back').onclick = () => (location.hash = '#/');
  $('#share').onclick = openShareDialog;
  const form = $('#add-form');
  const catSel = form.elements.category;
  let manualCat = false;
  catSel.onchange = () => (manualCat = true);
  form.elements.name.oninput = (e) => {
    if (manualCat) return;
    const g = guessCategory(e.target.value);
    if (g) catSel.value = g;
  };
  form.onsubmit = async (e) => {
    e.preventDefault();
    const f = form.elements;
    const name = f.name.value.trim();
    if (!name) return;
    if (!navigator.onLine) return toast(t('noConnAdd'), true);
    const row = { list_id: state.listId, name, quantity: parseQty(f.quantity.value), price: parsePrice(f.price.value), category: f.category.value, created_by: state.user.id };
    f.name.value = ''; f.quantity.value = ''; f.price.value = ''; manualCat = false;
    f.name.focus();
    const { data, error } = await sb.from('shopping_items').insert(row).select().single();
    if (error) return toast(t('errAddItem'), true);
    upsertItem(data);
  };
}

function renderItems() {
  const box = $('#items');
  if (!box) return;
  const sorted = [...state.items].sort((a, b) => a.name.localeCompare(b.name, numLocale()));
  const pending = sorted.filter((i) => !i.is_checked);
  const done = sorted.filter((i) => i.is_checked);

  const itemHtml = (i) => `
    <div class="item ${i.is_checked ? 'done' : ''}" data-id="${i.id}">
      <button class="check" data-act="toggle" aria-label="${esc(t('markItem'))}"><span class="box">✓</span></button>
      <button class="txt" data-act="edit">
        <span class="nm">${esc(i.name)}</span>
        ${i.quantity ? `<span class="qty">${esc(i.quantity)}</span>` : ''}
      </button>
      ${i.price != null ? `<span class="price">${money(i.price)}</span>` : ''}
      <button class="icon ghost del" data-act="del" aria-label="${esc(t('remove'))}">✕</button>
    </div>`;

  let html = '';
  if (!state.items.length) html = `<div class="empty">${t('emptyList')}</div>`;

  for (const cat of CAT_ORDER) {
    const g = pending.filter((i) => (CATS[i.category] ? i.category : 'Outros') === cat);
    if (g.length) html += `<h2>${CATS[cat]} ${esc(catLabel(cat))}</h2>${g.map(itemHtml).join('')}`;
  }
  if (done.length) {
    html += `<h2 class="bar"><span>${esc(t('bought', { n: done.length }))}</span>
      <button class="danger" data-act="clear">${esc(t('clearBought'))}</button></h2>${done.map(itemHtml).join('')}`;
  }
  box.innerHTML = html;

  const total = sumPrices(state.items);
  const bar = $('#total-bar');
  if (bar) bar.innerHTML = `<span>${esc(t('totalList'))}</span><strong>${money(total)}</strong>`;
  if (state.listId) state.totals[state.listId] = total;
}

// Delegação de eventos dos itens
document.addEventListener('click', (e) => {
  const btn = e.target.closest('[data-act]');
  if (!btn || !state.listId) return;
  const row = btn.closest('.item');
  const id = row?.dataset.id;
  const act = btn.dataset.act;
  if (act === 'toggle') toggleItem(id);
  else if (act === 'del') deleteItem(id);
  else if (act === 'edit') openEditDialog(id);
  else if (act === 'clear') clearChecked();
});

function persistItems() { store.set(itemsKey(state.listId), state.items); }

function upsertItem(item) {
  const i = state.items.findIndex((x) => x.id === item.id);
  if (i >= 0) state.items[i] = item; else state.items.push(item);
  persistItems();
  renderItems();
}
function removeItem(id) {
  state.items = state.items.filter((x) => x.id !== id);
  persistItems();
  renderItems();
}

async function toggleItem(id) {
  const it = state.items.find((x) => x.id === id);
  if (!it) return;
  if (!navigator.onLine) return toast(t('noConnRetry'), true);
  const prev = it.is_checked;
  upsertItem({ ...it, is_checked: !prev });
  const { error } = await sb.from('shopping_items').update({ is_checked: !prev }).eq('id', id);
  if (error) { upsertItem({ ...it, is_checked: prev }); toast(t('errUpdateItem'), true); }
}

async function deleteItem(id) {
  const it = state.items.find((x) => x.id === id);
  if (!it) return;
  if (!navigator.onLine) return toast(t('noConn'), true);
  removeItem(id);
  const { error } = await sb.from('shopping_items').delete().eq('id', id);
  if (error) { upsertItem(it); toast(t('errRemoveItem'), true); }
}

async function clearChecked() {
  const n = state.items.filter((i) => i.is_checked).length;
  if (!n || !confirm(t('confirmClear', { n }))) return;
  if (!navigator.onLine) return toast(t('noConn'), true);
  const { error } = await sb.from('shopping_items').delete().eq('list_id', state.listId).eq('is_checked', true);
  if (error) return toast(t('errClear'), true);
  state.items = state.items.filter((i) => !i.is_checked);
  persistItems();
  renderItems();
}

/* ------------------------------ Diálogos -------------------------------- */
dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });

function openEditDialog(id) {
  const it = state.items.find((x) => x.id === id);
  if (!it) return;
  dlg.innerHTML = `
  <h3>${esc(t('editItem'))}</h3>
  <form id="edit-form">
    <input name="name" value="${esc(it.name)}" maxlength="120" required>
    <input name="quantity" data-num value="${esc(parseQty(it.quantity) || '')}" placeholder="${esc(t('quantityPh'))}" inputmode="decimal" maxlength="8">
    <input name="price" data-num value="${esc(priceInput(it.price))}" placeholder="${esc(t('pricePh'))}" inputmode="decimal" maxlength="12">
    <select name="category">
      ${CAT_ORDER.map((c) => `<option value="${c}" ${c === it.category ? 'selected' : ''}>${CATS[c]} ${esc(catLabel(c))}</option>`).join('')}
    </select>
    <div class="row">
      <button type="button" data-close>${esc(t('cancel'))}</button>
      <button class="primary" type="submit">${esc(t('save'))}</button>
    </div>
  </form>`;
  bindNumeric(dlg);
  dlg.querySelector('[data-close]').onclick = () => dlg.close();
  dlg.querySelector('#edit-form').onsubmit = async (e) => {
    e.preventDefault();
    const f = e.target.elements;
    const patch = { name: f.name.value.trim(), quantity: parseQty(f.quantity.value), price: parsePrice(f.price.value), category: f.category.value };
    if (!patch.name) return;
    dlg.close();
    if (!navigator.onLine) return toast(t('noConn'), true);
    const { data, error } = await sb.from('shopping_items').update(patch).eq('id', id).select().single();
    if (error) return toast(t('errSave'), true);
    upsertItem(data);
  };
  dlg.showModal();
}

function openShareDialog() {
  const l = currentList();
  const owner = isOwner();
  const me = state.user.id;
  dlg.innerHTML = `
  <h3>👥 ${esc(l?.name || t('listDefault'))}</h3>
  <div class="stack">
    ${owner ? `
    <form id="share-form" class="stack">
      <input name="email" type="email" placeholder="${esc(t('shareEmailPh'))}" required>
      <button class="primary" type="submit">${esc(t('share'))}</button>
      <div class="msg" id="share-msg" hidden></div>
    </form>` : ''}
    <ul class="members">
      ${state.members.map((m) => `
        <li><span class="grow">${esc(m.profiles?.nome || m.profiles?.email || t('user'))}
          <br><small>${esc(m.profiles?.email || '')}</small></span>
          ${m.user_id === l?.owner_id ? `<span class="tag">${esc(t('owner'))}</span>`
            : owner ? `<button class="danger" data-rm="${m.user_id}">${esc(t('remove'))}</button>`
            : m.user_id === me ? `<span class="tag">${esc(t('you'))}</span>` : ''}
        </li>`).join('') || `<li>${esc(t('noMembers'))}</li>`}
    </ul>
    <div class="row" style="justify-content:space-between">
      ${owner ? `<button class="danger" id="del-list">${esc(t('deleteList'))}</button>`
              : `<button class="danger" id="leave-list">${esc(t('leaveList'))}</button>`}
      <button data-close>${esc(t('close'))}</button>
    </div>
  </div>`;

  dlg.querySelector('[data-close]').onclick = () => dlg.close();

  const sf = dlg.querySelector('#share-form');
  if (sf) sf.onsubmit = async (e) => {
    e.preventDefault();
    const email = e.target.elements.email.value.trim();
    const msg = $('#share-msg');
    msg.hidden = false; msg.className = 'msg'; msg.textContent = t('sharing');
    const { error } = await sb.rpc('share_list', { p_list_id: state.listId, p_email: email });
    if (error) { msg.className = 'msg err'; msg.textContent = translateServerMsg(error.message); return; }
    await loadMembers();
    openShareDialog();
    toast(t('shared'));
  };

  dlg.querySelectorAll('[data-rm]').forEach((b) => (b.onclick = async () => {
    const { error } = await sb.from('list_members').delete().eq('list_id', state.listId).eq('user_id', b.dataset.rm);
    if (error) return toast(t('errRemoveMember'), true);
    await loadMembers();
    openShareDialog();
  }));

  const del = dlg.querySelector('#del-list');
  if (del) del.onclick = async () => {
    if (!confirm(t('confirmDelete'))) return;
    const { error } = await sb.from('shopping_lists').delete().eq('id', state.listId);
    if (error) return toast(t('errDeleteList'), true);
    dlg.close(); afterListGone();
  };
  const leave = dlg.querySelector('#leave-list');
  if (leave) leave.onclick = async () => {
    if (!confirm(t('confirmLeave'))) return;
    const { error } = await sb.from('list_members').delete().eq('list_id', state.listId).eq('user_id', me);
    if (error) return toast(t('errLeave'), true);
    dlg.close(); afterListGone();
  };
  dlg.showModal();
}

function afterListGone() {
  state.lists = state.lists.filter((l) => l.id !== state.listId);
  store.set(listsKey(), state.lists);
  store.del(itemsKey(state.listId));
  store.del(membersKey(state.listId));
  location.hash = '#/';
}

/* ------------------------------ Realtime -------------------------------- */
function setLive(on) {
  state.live = on;
  const el = $('#live');
  if (el) el.classList.toggle('on', on);
}

function setupItemsChannel(listId) {
  teardownRealtime();
  const ch = sb.channel('items-' + listId)
    .on('postgres_changes', { event: '*', schema: 'public', table: 'shopping_items' }, (p) => {
      if (state.listId !== listId) return;
      if (p.eventType === 'DELETE') {
        if (p.old?.id) removeItem(p.old.id);
      } else if (p.new?.list_id === listId) {
        upsertItem(p.new);
      }
    })
    .on('postgres_changes', { event: '*', schema: 'public', table: 'list_members' }, async (p) => {
      const rec = p.new?.list_id ? p.new : p.old;
      if (rec?.list_id && rec.list_id !== listId) return;
      await loadMembers();
    })
    .subscribe((status) => {
      setLive(status === 'SUBSCRIBED');
      // Ao reconectar, sincroniza o que foi perdido
      if (status === 'SUBSCRIBED') loadItems();
    });
  state.channels.push(ch);
}

function teardownItemsChannel() { teardownRealtime(); }
function teardownRealtime() {
  state.channels.forEach((c) => sb.removeChannel(c));
  state.channels = [];
  state.live = false;
}

// Ao voltar para o app (celular desbloqueado / aba reaberta) ressincroniza
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState !== 'visible' || !state.user || !navigator.onLine) return;
  if (state.listId) loadItems(); else loadLists();
});

/* ------------------------------ PWA ------------------------------------- */
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./service-worker.js').catch((e) => console.warn('SW failed', e));
  });
}

init();
