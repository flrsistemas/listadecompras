import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/+esm';
import { SUPABASE_URL, SUPABASE_ANON_KEY } from './config.js';

/* ------------------------------ Utilidades ------------------------------ */
const $ = (s, r = document) => r.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const CATS = {
  'Hortifruti': '🥬', 'Açougue': '🥩', 'Padaria': '🥖', 'Laticínios': '🧀',
  'Limpeza': '🧴', 'Mercearia': '🥫', 'Bebidas': '🥤', 'Outros': '🛒',
};
const CAT_ORDER = Object.keys(CATS);

// Palavras-chave para sugerir a categoria automaticamente
const GUESS = {
  'Hortifruti': ['banana', 'maçã', 'maca', 'laranja', 'limão', 'limao', 'tomate', 'cebola', 'alho', 'batata', 'cenoura', 'alface', 'fruta', 'verdura', 'mamão', 'uva', 'abacate', 'pepino', 'brócolis', 'couve'],
  'Açougue': ['carne', 'frango', 'linguiça', 'linguica', 'picanha', 'peixe', 'bife', 'costela', 'bacon', 'salsicha', 'fígado', 'patinho', 'alcatra', 'contra'],
  'Padaria': ['pão', 'pao', 'bolo', 'biscoito', 'bolacha', 'torrada', 'bisnaga'],
  'Laticínios': ['leite', 'queijo', 'iogurte', 'manteiga', 'requeijão', 'requeijao', 'creme de leite', 'presunto', 'mussarela', 'ovo', 'margarina'],
  'Limpeza': ['sabão', 'sabao', 'detergente', 'desinfetante', 'amaciante', 'esponja', 'papel higiênico', 'papel higienico', 'shampoo', 'sabonete', 'água sanitária', 'lixo', 'cloro'],
  'Mercearia': ['arroz', 'feijão', 'feijao', 'macarrão', 'macarrao', 'açúcar', 'acucar', 'sal', 'óleo', 'oleo', 'farinha', 'café', 'cafe', 'molho', 'milho', 'azeite', 'cereal', 'aveia'],
  'Bebidas': ['suco', 'refrigerante', 'cerveja', 'vinho', 'água', 'agua', 'coca', 'guaraná', 'guarana', 'energético', 'chá'],
};
function guessCategory(name) {
  const n = name.toLowerCase();
  for (const [cat, words] of Object.entries(GUESS)) if (words.some((w) => n.includes(w))) return cat;
  return null;
}

const brl = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
const money = (v) => brl.format(Number(v) || 0);
// Aceita "12,50", "12.50" e "1.234,56"; vazio/inválido => null
function parsePrice(s) {
  let t = String(s ?? '').trim().replace(/[^\d.,]/g, '');
  if (!t) return null;
  if (t.includes(',')) t = t.replace(/\./g, '').replace(',', '.');
  const n = Number(t);
  return Number.isFinite(n) && n >= 0 ? Math.round(n * 100) / 100 : null;
}
const priceInput = (v) => (v == null ? '' : String(v).replace('.', ','));
const sumPrices = (items) => Math.round(items.reduce((s, i) => s + (Number(i.price) || 0), 0) * 100) / 100;

function toast(msg, isErr = false) {
  const t = $('#toast');
  t.textContent = msg;
  t.className = 'toast' + (isErr ? ' err' : '');
  t.hidden = false;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => (t.hidden = true), 3200);
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
    <h1>⚙️ Configuração pendente</h1>
    <p>Abra <code>js/config.js</code> e preencha <code>SUPABASE_URL</code> e <code>SUPABASE_ANON_KEY</code>.</p></div>`;
  throw new Error('Supabase não configurado (js/config.js)');
}

const sb = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: false },
});

/* ------------------------------ Offline --------------------------------- */
function updateBanner() {
  const b = $('#banner');
  b.hidden = navigator.onLine;
  b.textContent = '📡 Sem conexão — mostrando a última versão salva';
}
window.addEventListener('online', () => { updateBanner(); route(); toast('Conexão restabelecida'); });
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
  app.innerHTML = `
  <section class="auth">
    <img class="logo" src="icons/icon.svg" alt="">
    <h1>Lista de Compras</h1>
    <p class="sub">Compartilhe suas listas em tempo real</p>
    <form class="card" id="auth-form">
      ${login ? '' : '<input name="nome" placeholder="Seu nome" autocomplete="name" required>'}
      <input name="email" type="email" placeholder="E-mail" autocomplete="email" required>
      <input name="password" type="password" placeholder="Senha (mín. 6 caracteres)" minlength="6"
             autocomplete="${login ? 'current-password' : 'new-password'}" required>
      ${info ? `<div class="msg ${isErr ? 'err' : ''}">${esc(info)}</div>` : ''}
      <button class="primary" type="submit">${login ? 'Entrar' : 'Criar conta'}</button>
    </form>
    <button class="switch" id="switch-mode" type="button">
      ${login ? 'Não tem conta? Cadastre-se' : 'Já tem conta? Entrar'}
    </button>
  </section>`;

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
          renderAuth('Conta criada! Confirme seu e-mail (veja a caixa de entrada) e depois entre.');
        }
      }
    } catch (err) {
      renderAuth(traduzErro(err), true);
    }
  };
}

function traduzErro(err) {
  const m = err?.message || String(err);
  if (/Invalid login/i.test(m)) return 'E-mail ou senha incorretos.';
  if (/already registered/i.test(m)) return 'Este e-mail já está cadastrado.';
  if (/Email not confirmed/i.test(m)) return 'Confirme seu e-mail antes de entrar.';
  if (/rate limit/i.test(m)) return 'Muitas tentativas. Aguarde um pouco.';
  if (/fetch|network/i.test(m)) return 'Sem conexão com o servidor.';
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
  if (lr.error) { if (navigator.onLine) toast('Erro ao carregar listas', true); return; }
  state.lists = lr.data;
  store.set(listsKey(), lr.data);
  if (!ir.error) {
    const t = {};
    for (const r of ir.data) t[r.list_id] = (t[r.list_id] || 0) + (Number(r.price) || 0);
    state.totals = t;
    store.set(totalsKey(), t);
  }
  if (!state.listId) renderLists();
}

function renderLists() {
  const me = state.user.id;
  app.innerHTML = `
  <div class="topbar">
    <h1>🛒 Minhas listas</h1>
    <button class="ghost" id="logout" title="Sair">Sair</button>
  </div>
  <form class="newlist" id="newlist">
    <input name="name" placeholder="Nova lista (ex: Mercado do Mês)" maxlength="80" required>
    <button class="primary" type="submit">Criar</button>
  </form>
  <div class="list-cards">
    ${state.lists.length ? state.lists.map((l) => `
      <button class="list-card" data-open="${l.id}">
        <span class="ico">${l.owner_id === me ? '📋' : '🤝'}</span>
        <span class="grow"><span class="name">${esc(l.name)}</span><br>
          <span class="meta">${l.owner_id === me ? 'Sua lista' : 'Compartilhada com você'}</span></span>
        <span class="total">${money(Math.round((state.totals[l.id] || 0) * 100) / 100)}</span>
        <span>›</span>
      </button>`).join('') : '<div class="empty">Nenhuma lista ainda.<br>Crie a primeira acima 👆</div>'}
  </div>`;

  $('#logout').onclick = logout;
  $('#newlist').onsubmit = async (e) => {
    e.preventDefault();
    const name = new FormData(e.target).get('name').trim();
    if (!name) return;
    const { data, error } = await sb.from('shopping_lists').insert({ name, owner_id: state.user.id }).select().single();
    if (error) return toast('Não foi possível criar a lista', true);
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
  if (error) { if (navigator.onLine) toast('Erro ao carregar itens', true); return; }
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
    $('#list-title').textContent = l ? l.name : 'Lista';
    return;
  }
  app.innerHTML = `
  <div class="topbar">
    <button class="icon ghost" id="back" aria-label="Voltar">←</button>
    <h1 id="list-title">${esc(l ? l.name : 'Lista')}</h1>
    <span class="live ${state.live ? 'on' : ''}" id="live" title="Sincronização em tempo real"></span>
    <button class="icon ghost" id="share" aria-label="Compartilhar e opções">👥</button>
  </div>
  <form class="card add-form" id="add-form" autocomplete="off">
    <input class="name" name="name" placeholder="Adicionar item…" maxlength="120" required enterkeyhint="done">
    <select name="category" aria-label="Categoria">
      ${CAT_ORDER.map((c) => `<option value="${c}">${CATS[c]} ${c}</option>`).join('')}
    </select>
    <input name="quantity" placeholder="Qtd (2 un)" maxlength="30" style="grid-column:2/3;grid-row:2" aria-label="Quantidade">
    <input name="price" placeholder="Preço (R$)" inputmode="decimal" maxlength="12" style="grid-column:1/2;grid-row:3" aria-label="Preço">
    <button class="primary" type="submit" style="grid-column:2/3;grid-row:3">Adicionar</button>
  </form>
  <div class="total-bar" id="total-bar"></div>
  <div id="items"></div>`;

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
    if (!navigator.onLine) return toast('Sem conexão: não é possível adicionar agora', true);
    const row = { list_id: state.listId, name, quantity: f.quantity.value.trim() || null, price: parsePrice(f.price.value), category: f.category.value, created_by: state.user.id };
    f.name.value = ''; f.quantity.value = ''; f.price.value = ''; manualCat = false;
    f.name.focus();
    const { data, error } = await sb.from('shopping_items').insert(row).select().single();
    if (error) return toast('Erro ao adicionar item', true);
    upsertItem(data);
  };
}

function renderItems() {
  const box = $('#items');
  if (!box) return;
  const sorted = [...state.items].sort((a, b) => a.name.localeCompare(b.name, 'pt-BR'));
  const pending = sorted.filter((i) => !i.is_checked);
  const done = sorted.filter((i) => i.is_checked);

  const itemHtml = (i) => `
    <div class="item ${i.is_checked ? 'done' : ''}" data-id="${i.id}">
      <button class="check" data-act="toggle" aria-label="Marcar item"><span class="box">✓</span></button>
      <button class="txt" data-act="edit">
        <span class="nm">${esc(i.name)}</span>
        ${i.quantity ? `<span class="qty">${esc(i.quantity)}</span>` : ''}
      </button>
      ${i.price != null ? `<span class="price">${money(i.price)}</span>` : ''}
      <button class="icon ghost del" data-act="del" aria-label="Remover">✕</button>
    </div>`;

  let html = '';
  if (!state.items.length) html = '<div class="empty">Lista vazia.<br>Adicione o primeiro item acima 👆</div>';

  for (const cat of CAT_ORDER) {
    const g = pending.filter((i) => (CATS[i.category] ? i.category : 'Outros') === cat);
    if (g.length) html += `<h2>${CATS[cat]} ${cat}</h2>${g.map(itemHtml).join('')}`;
  }
  if (done.length) {
    html += `<h2 class="bar"><span>✅ Comprados (${done.length})</span>
      <button class="danger" data-act="clear">Limpar comprados</button></h2>${done.map(itemHtml).join('')}`;
  }
  box.innerHTML = html;

  const total = sumPrices(state.items);
  const bar = $('#total-bar');
  if (bar) bar.innerHTML = `<span>Total da lista</span><strong>${money(total)}</strong>`;
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
  if (!navigator.onLine) return toast('Sem conexão: tente novamente quando voltar o sinal', true);
  const prev = it.is_checked;
  upsertItem({ ...it, is_checked: !prev });
  const { error } = await sb.from('shopping_items').update({ is_checked: !prev }).eq('id', id);
  if (error) { upsertItem({ ...it, is_checked: prev }); toast('Erro ao atualizar item', true); }
}

async function deleteItem(id) {
  const it = state.items.find((x) => x.id === id);
  if (!it) return;
  if (!navigator.onLine) return toast('Sem conexão', true);
  removeItem(id);
  const { error } = await sb.from('shopping_items').delete().eq('id', id);
  if (error) { upsertItem(it); toast('Erro ao remover item', true); }
}

async function clearChecked() {
  const n = state.items.filter((i) => i.is_checked).length;
  if (!n || !confirm(`Remover ${n} item(ns) comprado(s)?`)) return;
  if (!navigator.onLine) return toast('Sem conexão', true);
  const { error } = await sb.from('shopping_items').delete().eq('list_id', state.listId).eq('is_checked', true);
  if (error) return toast('Erro ao limpar comprados', true);
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
  <h3>Editar item</h3>
  <form id="edit-form">
    <input name="name" value="${esc(it.name)}" maxlength="120" required>
    <input name="quantity" value="${esc(it.quantity || '')}" placeholder="Quantidade (ex: 2 un, 1 kg)" maxlength="30">
    <input name="price" value="${esc(priceInput(it.price))}" placeholder="Preço (R$)" inputmode="decimal" maxlength="12">
    <select name="category">
      ${CAT_ORDER.map((c) => `<option value="${c}" ${c === it.category ? 'selected' : ''}>${CATS[c]} ${c}</option>`).join('')}
    </select>
    <div class="row">
      <button type="button" data-close>Cancelar</button>
      <button class="primary" type="submit">Salvar</button>
    </div>
  </form>`;
  dlg.querySelector('[data-close]').onclick = () => dlg.close();
  dlg.querySelector('#edit-form').onsubmit = async (e) => {
    e.preventDefault();
    const f = e.target.elements;
    const patch = { name: f.name.value.trim(), quantity: f.quantity.value.trim() || null, price: parsePrice(f.price.value), category: f.category.value };
    if (!patch.name) return;
    dlg.close();
    if (!navigator.onLine) return toast('Sem conexão', true);
    const { data, error } = await sb.from('shopping_items').update(patch).eq('id', id).select().single();
    if (error) return toast('Erro ao salvar', true);
    upsertItem(data);
  };
  dlg.showModal();
}

function openShareDialog() {
  const l = currentList();
  const owner = isOwner();
  const me = state.user.id;
  dlg.innerHTML = `
  <h3>👥 ${esc(l?.name || 'Lista')}</h3>
  <div class="stack">
    ${owner ? `
    <form id="share-form" class="stack">
      <input name="email" type="email" placeholder="E-mail de quem vai participar" required>
      <button class="primary" type="submit">Compartilhar</button>
      <div class="msg" id="share-msg" hidden></div>
    </form>` : ''}
    <ul class="members">
      ${state.members.map((m) => `
        <li><span class="grow">${esc(m.profiles?.nome || m.profiles?.email || 'Usuário')}
          <br><small>${esc(m.profiles?.email || '')}</small></span>
          ${m.user_id === l?.owner_id ? '<span class="tag">dono</span>'
            : owner ? `<button class="danger" data-rm="${m.user_id}">Remover</button>`
            : m.user_id === me ? '<span class="tag">você</span>' : ''}
        </li>`).join('') || '<li>Sem membros</li>'}
    </ul>
    <div class="row" style="justify-content:space-between">
      ${owner ? '<button class="danger" id="del-list">Excluir lista</button>'
              : '<button class="danger" id="leave-list">Sair da lista</button>'}
      <button data-close>Fechar</button>
    </div>
  </div>`;

  dlg.querySelector('[data-close]').onclick = () => dlg.close();

  const sf = dlg.querySelector('#share-form');
  if (sf) sf.onsubmit = async (e) => {
    e.preventDefault();
    const email = e.target.elements.email.value.trim();
    const msg = $('#share-msg');
    msg.hidden = false; msg.className = 'msg'; msg.textContent = 'Compartilhando…';
    const { error } = await sb.rpc('share_list', { p_list_id: state.listId, p_email: email });
    if (error) { msg.className = 'msg err'; msg.textContent = error.message; return; }
    await loadMembers();
    openShareDialog();
    toast('Lista compartilhada!');
  };

  dlg.querySelectorAll('[data-rm]').forEach((b) => (b.onclick = async () => {
    const { error } = await sb.from('list_members').delete().eq('list_id', state.listId).eq('user_id', b.dataset.rm);
    if (error) return toast('Erro ao remover membro', true);
    await loadMembers();
    openShareDialog();
  }));

  const del = dlg.querySelector('#del-list');
  if (del) del.onclick = async () => {
    if (!confirm('Excluir esta lista e todos os itens para todos os membros?')) return;
    const { error } = await sb.from('shopping_lists').delete().eq('id', state.listId);
    if (error) return toast('Erro ao excluir lista', true);
    dlg.close(); afterListGone();
  };
  const leave = dlg.querySelector('#leave-list');
  if (leave) leave.onclick = async () => {
    if (!confirm('Sair desta lista?')) return;
    const { error } = await sb.from('list_members').delete().eq('list_id', state.listId).eq('user_id', me);
    if (error) return toast('Erro ao sair da lista', true);
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
    navigator.serviceWorker.register('./service-worker.js').catch((e) => console.warn('SW falhou', e));
  });
}

init();
