import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/+esm';
import { SUPABASE_URL, SUPABASE_ANON_KEY } from './config.js';
import { createLocalClient, hasGuestData, readGuestDb, clearGuestDb } from './local-store.js';
import { t, getLang, setLang, LANGS, LANG_NAMES, CAT_LABEL, HELP_URL, PRIVACY_URL, SITE_URL, numLocale, decimalSep } from './i18n.js';

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
// O preço é por unidade. Quantidade como número ("1,5" => 1.5; "2 un" => 2; vazio/sem número => 1)
function qtyNum(q) {
  const m = String(q ?? '').replace(',', '.').match(/\d+(?:\.\d+)?/);
  const n = m ? Number(m[0]) : 1;
  return n > 0 ? n : 1;
}
const lineTotal = (i) => Math.round((Number(i.price) || 0) * qtyNum(i.quantity) * 100) / 100;
const sumPrices = (items) => Math.round(items.reduce((s, i) => s + lineTotal(i), 0) * 100) / 100;
// Linha de detalhe do item: "6 × R$ 6,40" (quantidade × preço unitário) ou só a quantidade
const qtyLine = (i) => (i.quantity && i.price != null && qtyNum(i.quantity) !== 1 ? `${i.quantity} × ${money(i.price)}` : (i.quantity || ''));

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
  authMode: 'login', // login | signup | forgot
  recovery: false, // true enquanto o usuário define a nova senha (link do e-mail)
  prefillEmail: '',
  channels: [],
  live: false,
  guest: false, // modo sem conta: tudo fica só neste aparelho, sem Supabase
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

const realSb = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: false },
});
const localSb = createLocalClient(); // modo sem conta (localStorage)
let sb = realSb; // o app inteiro fala com `sb`: conta (Supabase) ou modo sem conta (local)
const isOnline = () => state.guest || navigator.onLine; // sem conta não depende de internet

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

/* ------------------- Alterações sem sinal (fila local) ------------------- */
// Marcar, adicionar, EDITAR e REMOVER itens sem conexão ficam guardados no aparelho e
// são enviados quando o sinal volta, na ordem em que foram feitos. O item novo já nasce
// com o id definitivo (uuid gerado aqui). Em conflito, vale o último a chegar ao servidor.
const isNetErr = (err) => !isOnline() || /fetch|network|timeout|abort|load failed|offline/i.test(String(err?.message || err?.name || err));
// Em sinal fraco a requisição pode ficar pendurada: após 8 s tratamos como falha de rede
function timed(q, ms = 8000) {
  const c = new AbortController();
  const timer = setTimeout(() => c.abort(), ms);
  return q.abortSignal(c.signal).then(
    (r) => { clearTimeout(timer); return r; },
    (e) => { clearTimeout(timer); return { data: null, error: e }; },
  );
}
const newId = () => (crypto.randomUUID ? crypto.randomUUID()
  : 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => { const r = (Math.random() * 16) | 0; return (c === 'x' ? r : (r & 3) | 8).toString(16); }));
const queueKey = () => `lc:queue:${state.user.id}`;
const getQueue = () => (state.user ? store.get(queueKey()) || [] : []);
function setQueue(q) { if (!state.user) return; store.set(queueKey(), q); updatePending(); }
// Tipos: 'add' (item novo), 'edit' (campos), 'del' (remoção) e, sem tipo, a marcação (is_checked)
const isAdd = (e) => e.type === 'add';
const isEdit = (e) => e.type === 'edit';
const isDel = (e) => e.type === 'del';
const isListEntry = (e) => e.type === 'lnew' || e.type === 'lrename' || e.type === 'ldel' || e.type === 'lleave'; // criar / renomear / excluir / sair da lista
const entryItemId = (e) => (isAdd(e) ? e.row.id : e.id);
const pendingAdds = (listId) => getQueue().filter((e) => isAdd(e) && e.list_id === listId);
const findPendingAdd = (id) => getQueue().find((e) => isAdd(e) && e.row.id === id);
const isPendingAdd = (id) => !!findPendingAdd(id);
const localItem = (row) => ({ ...row, is_checked: !!row.is_checked, updated_at: new Date().toISOString() });
function pendingApplier() {
  const checks = {}, edits = {};
  for (const e of getQueue()) { if (isEdit(e)) edits[e.id] = e.patch; else if (!isAdd(e) && !isDel(e) && !isListEntry(e)) checks[e.id] = e.is_checked; }
  return (i) => {
    let o = i;
    if (i.id in checks) o = { ...o, is_checked: checks[i.id] };
    if (edits[i.id]) o = { ...o, ...edits[i.id] };
    return o;
  };
}
const withPending = (i) => pendingApplier()(i);
const pendingDels = () => new Set(getQueue().filter(isDel).map((e) => e.id));
function updatePending() {
  const el = $('#pending');
  if (!el) return;
  const n = getQueue().filter((e) => !state.listId || e.list_id === state.listId).length;
  el.hidden = !n;
  el.textContent = n ? t('pendingSync', { n }) : '';
}
// quiet = true quando estamos online: o envio é imediato e não precisa do aviso "salvo no aparelho"
function push(entry, quiet = false, keep = (e) => true) {
  const q = getQueue();
  const first = q.length === 0;
  setQueue([...q.filter(keep), entry]);
  if (first && !quiet) toast(t('queued'));
}
const enqueue = (item, is_checked) => push({ id: item.id, list_id: item.list_id, is_checked, ts: Date.now() }, false, (e) => isAdd(e) || isEdit(e) || isDel(e) || e.id !== item.id);
const enqueueAdd = (row, quiet = false) => push({ type: 'add', id: row.id, list_id: row.list_id, row, ts: Date.now() }, quiet);
function enqueueEdit(item, patch, quiet = false) {
  const prev = getQueue().find((e) => isEdit(e) && e.id === item.id);
  push({ type: 'edit', id: item.id, list_id: item.list_id, patch: { ...(prev ? prev.patch : {}), ...patch }, ts: prev ? prev.ts : Date.now() }, quiet, (e) => !(isEdit(e) && e.id === item.id));
}
// remover: as alterações pendentes do mesmo item deixam de importar
const enqueueDel = (item, quiet = false) => push({ type: 'del', id: item.id, list_id: item.list_id, ts: Date.now() }, quiet, (e) => isAdd(e) || e.id !== item.id);
// listas: renomear, excluir (dono) e sair (participante) também ficam na fila
function pendingListOps() {
  const removed = new Set(), renamed = {}, created = {};
  for (const e of getQueue()) { if (e.type === 'ldel' || e.type === 'lleave') removed.add(e.id); else if (e.type === 'lrename') renamed[e.id] = e.name; else if (e.type === 'lnew') created[e.id] = e.row; }
  return { removed, renamed, created };
}
const findPendingNew = (id) => getQueue().find((e) => e.type === 'lnew' && e.id === id);
const isPendingNewList = (id) => !!id && !!findPendingNew(id); // lista criada sem sinal que ainda não chegou ao banco
const enqueueListNew = (row, quiet = false) => push({ type: 'lnew', id: row.id, list_id: row.id, row, ts: Date.now() }, quiet);
const editPendingNewList = (id, name) => setQueue(getQueue().map((e) => (e.type === 'lnew' && e.id === id ? { ...e, row: { ...e.row, name } } : e)));
const dropListEntries = (id) => setQueue(getQueue().filter((e) => e.list_id !== id)); // a lista nunca chegou ao banco: descarta tudo dela
function dropNewListLocally(id) {
  dropListEntries(id);
  state.lists = state.lists.filter((l) => l.id !== id);
  store.set(listsKey(), state.lists);
  store.del(itemsKey(id));
  if (state.listId === id) location.hash = '#/';
}
function applyListOps(lists) {
  const { removed, renamed, created } = pendingListOps();
  const have = new Set(lists.map((l) => l.id));
  const novas = Object.values(created).filter((r) => !have.has(r.id)); // criadas sem sinal: ainda não estão no servidor
  return [...novas, ...lists].filter((l) => !removed.has(l.id)).map((l) => (renamed[l.id] ? { ...l, name: renamed[l.id] } : l));
}
const enqueueListRename = (list, name, quiet = false) => push({ type: 'lrename', id: list.id, list_id: list.id, name, ts: Date.now() }, quiet, (e) => !(e.type === 'lrename' && e.id === list.id));
// excluir/sair: tudo o que estava pendente nessa lista deixa de importar
const enqueueListGone = (list, kind, quiet = false) => push({ type: kind, id: list.id, list_id: list.id, user_id: state.user.id, ts: Date.now() }, quiet, (e) => e.list_id !== list.id);
const editPendingAdd = (id, patch) => setQueue(getQueue().map((e) => (isAdd(e) && e.row.id === id ? { ...e, row: { ...e.row, ...patch } } : e)));
const dropPendingAdd = (id) => setQueue(getQueue().filter((e) => !(isAdd(e) && e.row.id === id)));
const sameEntry = (a, b) => a.id === b.id && a.ts === b.ts && a.type === b.type;

let flushing = false;
let netToast = false;
async function flushQueue() {
  if (flushing || !state.user || !isOnline() || !getQueue().length) return;
  flushing = true;
  let sent = 0, failed = 0, failedList = 0, failedOther = 0, broke = false, waited = false;
  try {
    while (!broke && getQueue().length) {
      const snapshot = [...getQueue()]; // o que for adicionado durante o envio entra na próxima volta
      for (let k = 0; k < snapshot.length && !broke; k++) {
        const e = snapshot[k];
        let batch = [e], res;
        if (isAdd(e)) res = await timed(sb.from('shopping_items').insert(e.row));
        else if (isEdit(e)) res = await timed(sb.from('shopping_items').update(e.patch).eq('id', e.id));
        else if (isDel(e)) { // remoções seguidas vão numa chamada só
          batch = [e];
          while (k + 1 < snapshot.length && isDel(snapshot[k + 1]) && batch.length < 50) batch.push(snapshot[++k]);
          res = await timed(sb.from('shopping_items').delete().in('id', batch.map((x) => x.id)));
        } else if (e.type === 'lrename') res = await timed(sb.from('shopping_lists').update({ name: e.name }).eq('id', e.id));
        else if (e.type === 'lnew') res = await timed(sb.from('shopping_lists').insert(e.row));
        else if (e.type === 'ldel') res = await timed(sb.from('shopping_lists').delete().eq('id', e.id));
        else if (e.type === 'lleave') res = await timed(sb.from('list_members').delete().eq('list_id', e.id).eq('user_id', e.user_id));
        else res = await timed(sb.from('shopping_items').update({ is_checked: e.is_checked }).eq('id', e.id));
        const error = res.error;
        if (error && isNetErr(error)) { broke = true; break; } // sem sinal de novo: tenta mais tarde
        if (error) { // recusado de vez (ex.: lista removida): 23505 em item novo = já tinha chegado ao banco
          if (isAdd(e)) { if (error.code !== '23505') { failed++; if (state.listId === e.list_id) removeItem(e.row.id); } }
          else if (e.type === 'lnew') { if (error.code !== '23505') { failedList++; dropNewListLocally(e.id); } }
          else failedOther++;
        }
        if (batch.some((b) => Date.now() - b.ts > 3000)) waited = true; // ficou esperando sinal: vale avisar que sincronizou
        setQueue(getQueue().filter((x) => !batch.some((b) => sameEntry(x, b))));
        sent += batch.length;
      }
    }
  } finally { flushing = false; }
  if (broke && isOnline() && !netToast) { netToast = true; toast(t('queued')); } // sinal fraco: avisa uma vez
  if (!broke) netToast = false;
  if (failedList) toast(t('errCreateList'), true);
  else if (failed) toast(t('errAddItem'), true);
  else if (failedOther) toast(t('errUpdateItem'), true);
  else if (sent && !getQueue().length && waited) toast(t('synced'));
  if (sent) { if (state.listId) loadItems(); else loadLists(); }
}

/* ------------------------- Atualizar app (cache) ------------------------- */
// Para quando o navegador insiste numa versão antiga: baixa os arquivos novos, remove o
// service worker e os caches e recarrega. Conta, listas e alterações pendentes ficam intactas.
const SHELL_FILES = ['./', './index.html', './css/style.css', './js/app.js', './js/config.js', './js/i18n.js', './js/local-store.js', './manifest.json'];
async function appVersion() {
  try { const k = (await caches.keys()).find((x) => x.startsWith('lista-compras-')); return k ? k.replace('lista-compras-', '') : ''; } catch { return ''; }
}
// Na tela de entrada o app se atualiza sozinho, uma vez por sessão do navegador (sem mensagens; se
// falhar, segue com a versão atual). A marca evita laço de recarregamentos.
function autoRefreshOnce() {
  if (!navigator.onLine || authNotice || noAutoRefresh) return; // vindo de link de e-mail: não perde a mensagem
  try { if (sessionStorage.getItem('lc:autoref')) return; sessionStorage.setItem('lc:autoref', '1'); } catch { return; }
  refreshApp(true);
}
async function refreshApp(auto = false) {
  if (!navigator.onLine) return auto || toast(t('refreshNeedsNet'), true);
  if (!auto) toast(t('refreshing'));
  try {
    // 1) copias novas, ignorando o cache do navegador; se falhar, nada foi apagado
    const res = await Promise.all(SHELL_FILES.map((u) => fetch(u, { cache: 'reload' })));
    if (res.some((r) => !r.ok)) throw new Error('shell');
    // 2) agora sim: service worker e caches antigos (localStorage nao e tocado)
    const regs = (await navigator.serviceWorker?.getRegistrations?.()) || [];
    await Promise.all(regs.map((r) => r.unregister()));
    await Promise.all((await caches.keys()).map((k) => caches.delete(k)));
  } catch { return auto || toast(t('refreshFail'), true); }
  location.reload();
}
const appFootHtml = () => `<div class="appfoot"><button class="ghost" id="refresh-app" type="button">↻ ${esc(t('refreshApp'))}</button><span class="ver" id="app-ver"></span></div>`;
function bindAppFoot() {
  const b = $('#refresh-app');
  if (b) b.onclick = () => refreshApp();
  const show = () => appVersion().then((v) => { const el = $('#app-ver'); if (el && v) el.textContent = v; });
  show();
  navigator.serviceWorker?.ready?.then(() => setTimeout(show, 500)); // 1a visita: o cache so existe depois que o service worker instala
}

/* ------------------------------ Dicas ------------------------------------ */
// Cada dica aparece uma vez (por usuário). O botão 💡 reabre todas.
const TIP_IDS = ['welcome', 'list', 'share'];
const tipsDlg = $('#tipdlg');
const tipsKey = () => `lc:tips:${state.user.id}`;
const tipsState = () => (state.user ? store.get(tipsKey()) || {} : {});
const tipSeen = (id) => { const s = tipsState(); return !!(s.off || s[id]); };
function markTip(id) { if (!state.user) return; const s = tipsState(); s[id] = true; store.set(tipsKey(), s); }
tipsDlg.addEventListener('click', (e) => { if (e.target === tipsDlg) tipsDlg.close(); });
function showTip(id) {
  tipsDlg.innerHTML = `<div class="tip"><h3>${esc(t(`tip_${id}_t`))}</h3><div class="tipbody">${t(`tip_${id}_b`)}</div>
    <div class="row"><button type="button" class="ghost" data-off>${esc(t('tipOff'))}</button>
    <button type="button" class="primary" data-ok>${esc(t('tipOk'))}</button></div></div>`;
  tipsDlg.addEventListener('close', () => markTip(id), { once: true });
  tipsDlg.querySelector('[data-ok]').onclick = () => tipsDlg.close();
  tipsDlg.querySelector('[data-off]').onclick = () => { const s = tipsState(); s.off = true; store.set(tipsKey(), s); tipsDlg.close(); };
  tipsDlg.showModal();
}
function maybeTip(id) {
  if (!state.user || tipSeen(id)) return;
  setTimeout(() => {
    if (tipSeen(id) || document.querySelector('dialog[open]')) return;
    const here = id === 'welcome' ? !state.listId : !!state.listId; // só se ainda estiver na mesma tela
    if (state.user && here) showTip(id);
  }, 700);
}
function openTipsPanel() {
  dlg.innerHTML = `<h3>${esc(t('tipsTitle'))}</h3><div class="stack">
    ${TIP_IDS.map((id) => `<section class="tip-card"><h4>${esc(t(`tip_${id}_t`))}</h4><div class="tipbody">${t(`tip_${id}_b`)}</div></section>`).join('')}
    <div class="row" style="justify-content:space-between"><button data-reset>${esc(t('tipReset'))}</button><button data-close>${esc(t('close'))}</button></div></div>`;
  dlg.querySelector('[data-close]').onclick = () => dlg.close();
  dlg.querySelector('[data-reset]').onclick = () => { store.set(tipsKey(), {}); dlg.close(); toast(t('tipReset') + ' ✓'); };
  dlg.showModal();
}

/* ------------------------------ Offline --------------------------------- */
function updateBanner() {
  const b = $('#banner');
  b.hidden = isOnline();
  b.textContent = t('offlineBanner');
}
window.addEventListener('online', () => { updateBanner(); flushQueue(); route(); toast(t('online')); });
window.addEventListener('offline', updateBanner);

/* ------------------------------ Auth ------------------------------------ */
// Volta do link do e-mail de confirmação: o Supabase devolve o resultado no #hash da página
// (type=signup em caso de sucesso, error_code=otp_expired se o link expirou ou já foi usado).
let authNotice = null;
let noAutoRefresh = false; // a tela de entrada mostrou uma mensagem do e-mail: não recarregar
let recoveryTokens = null;
function consumeAuthCallback() {
  const h = location.hash.replace(/^#/, '');
  if (!/(^|&)(type=(signup|email|recovery)|error(_code)?=)/.test(h)) return; // os nossos hashes começam com '/'
  const p = new URLSearchParams(h);
  if (p.get('error') || p.get('error_code')) {
    authNotice = { msg: t(p.get('error_code') === 'otp_expired' ? 'confirmExpired' : 'confirmError'), err: true };
  } else if (p.get('type') === 'recovery') { // link de "esqueci minha senha"
    if (p.get('access_token') && p.get('refresh_token')) recoveryTokens = { access_token: p.get('access_token'), refresh_token: p.get('refresh_token') };
    else authNotice = { msg: t('confirmError'), err: true };
  } else {
    authNotice = { msg: t('emailConfirmed'), err: false };
  }
  history.replaceState(null, '', location.pathname + location.search); // tira os tokens do endereço
}
const APP_URL = new URL('./', location.href).href; // endereço do app, sem hash nem busca

async function init() {
  updateBanner();
  consumeAuthCallback();
  const fromEmailLink = authNotice || recoveryTokens; // veio de um link do e-mail: abre a conta, não o modo sem conta
  if (store.get('lc:guest') && !fromEmailLink) enterGuest(); // sem conta: nem consulta o Supabase
  else {
    store.del('lc:guest');
    const { data: { session } } = await realSb.auth.getSession();
    state.user = session?.user ?? null;
  }

  realSb.auth.onAuthStateChange((event, sess) => {
    if (state.guest) return; // no modo sem conta, a conta não interessa
    const newId = sess?.user?.id ?? null;
    if (newId === (state.user?.id ?? null)) return; // ignora TOKEN_REFRESHED etc.
    state.user = sess?.user ?? null;
    if (!state.user) { teardownRealtime(); state.lists = []; }
    route();
  });

  if (recoveryTokens) { // veio do e-mail de nova senha: abre uma sessão temporária e mostra a tela de nova senha
    state.recovery = true;
    const { data, error } = await sb.auth.setSession(recoveryTokens);
    recoveryTokens = null;
    if (error || !data?.session) { state.recovery = false; authNotice = { msg: t('confirmExpired'), err: true }; } else state.user = data.session.user;
  }

  window.addEventListener('hashchange', route);
  route();
  if (authNotice && state.user) { toast(authNotice.msg, authNotice.err); authNotice = null; } // já estava logado neste aparelho
  flushQueue();
}

/* ------------------------------ Modo sem conta ---------------------------- */
function enterGuest() {
  store.set('lc:guest', true);
  sb = localSb;
  state.guest = true;
  state.recovery = false;
  state.user = { id: 'guest', email: '' };
  try { navigator.storage?.persist?.(); } catch { /* pedido opcional */ } // pede ao navegador para não apagar os dados sozinho
}
async function exitGuest(toSignup = false) {
  store.del('lc:guest');
  teardownRealtime(); // ainda com o cliente local
  state.guest = false;
  sb = realSb;
  state.lists = []; state.items = []; state.listId = null;
  state.authMode = toSignup ? 'signup' : 'login';
  const { data: { session } } = await realSb.auth.getSession();
  state.user = session?.user ?? null;
  if (location.hash !== '#/') location.hash = '#/';
  route();
}
function openGuestWarning() {
  dlg.classList.remove('guest');
  dlg.innerHTML = `<h3>${esc(t('guestTitle'))}</h3><div class="tipbody">${t('guestWarn')}</div>
    <div class="row"><button type="button" data-close>${esc(t('cancel'))}</button><button class="primary" type="button" id="guest-ok">${esc(t('guestContinue'))}</button></div>`;
  dlg.querySelector('[data-close]').onclick = () => dlg.close();
  dlg.querySelector('#guest-ok').onclick = () => { dlg.close(); enterGuest(); route(); };
  dlg.showModal();
}

/* ---------------- Importar as listas do modo sem conta para a conta ---------------- */
let importDismissed = false; // "Agora não": some até recarregar o app
function openImportDialog() {
  const g = readGuestDb();
  const nl = g.lists.length, ni = g.items.length;
  dlg.classList.remove('guest');
  dlg.innerHTML = `<h3>${esc(t('importTitle'))}</h3><div class="tipbody"><p>${esc(t('importBody', { l: nl, i: ni }))}</p></div>
    <div class="msg err" id="import-err" hidden></div>
    <div class="row" style="flex-wrap:wrap">
      <button type="button" data-close>${esc(t('importLater'))}</button>
      <button type="button" id="imp-keep">${esc(t('importKeep'))}</button>
      <button class="primary" type="button" id="imp-move">${esc(t('importMove'))}</button>
    </div>`;
  dlg.querySelector('[data-close]').onclick = () => { importDismissed = true; dlg.close(); renderLists(); };
  const run = async (clear) => {
    const btns = dlg.querySelectorAll('button');
    btns.forEach((b) => (b.disabled = true));
    const err = await importGuestLists(g);
    if (err) {
      const box = dlg.querySelector('#import-err');
      box.textContent = t('importFail'); box.hidden = false;
      btns.forEach((b) => (b.disabled = false));
      return;
    }
    if (clear) clearGuestDb();
    importDismissed = !clear ? true : false;
    dlg.close();
    toast(t('importDone', { l: nl }));
    await loadLists();
    renderLists();
  };
  dlg.querySelector('#imp-keep').onclick = () => run(false);
  dlg.querySelector('#imp-move').onclick = () => run(true);
  dlg.showModal();
}
// Cria na conta cópias das listas e itens do aparelho (ids novos: nunca colide com nada).
// Devolve null se deu certo, ou o erro. Se falhar no meio, apaga o que já criou nesta tentativa.
async function importGuestLists(g) {
  if (!navigator.onLine) return { message: 'offline' };
  const me = state.user.id;
  const idMap = {};
  const created = [];
  for (const l of g.lists) {
    const id = newId();
    idMap[l.id] = id;
    const { error } = await timed(realSb.from('shopping_lists').insert({ id, name: l.name, owner_id: me }));
    if (error) { await rollbackImport(created); return error; }
    created.push(id);
  }
  const rows = g.items.filter((i) => idMap[i.list_id]).map((i) => ({
    id: newId(), list_id: idMap[i.list_id], name: i.name, quantity: i.quantity ?? null, price: i.price ?? null,
    category: i.category || 'Outros', is_checked: !!i.is_checked, created_by: me,
  }));
  for (let k = 0; k < rows.length; k += 200) {
    const { error } = await timed(realSb.from('shopping_items').insert(rows.slice(k, k + 200)));
    if (error) { await rollbackImport(created); return error; }
  }
  return null;
}
async function rollbackImport(ids) {
  if (ids.length) { try { await realSb.from('shopping_lists').delete().in('id', ids); } catch { /* melhor esforço */ } }
}

const PASS_PATTERN ='(?=.*[A-Za-z])(?=.*\\d).{8,}';
// "Confirmar senha": o navegador avisa na hora se os dois campos forem diferentes
function bindPassMatch(form) {
  const p1 = form.elements.password, p2 = form.elements.password2;
  if (!p1 || !p2) return;
  const chk = () => p2.setCustomValidity(p2.value && p2.value !== p1.value ? t('errPassMismatch') : '');
  p1.addEventListener('input', chk);
  p2.addEventListener('input', chk);
}

function renderAuth(info = '', isErr = false) {
  if (!info && authNotice) { info = authNotice.msg; isErr = authNotice.err; authNotice = null; noAutoRefresh = true; }
  const mode = state.authMode;
  const login = mode === 'login', forgot = mode === 'forgot';
  const L = getLang();
  const pre = esc(state.prefillEmail || '');
  const fields = forgot
    ? `<p class="hint">${esc(t('forgotHelp'))}</p>
      <input name="email" type="email" value="${pre}" placeholder="${esc(t('email'))}" autocomplete="email" required>`
    : `${login ? '' : `<input name="nome" placeholder="${esc(t('name'))}" autocomplete="name" required>`}
      <input name="email" type="email" value="${pre}" placeholder="${esc(t('email'))}" autocomplete="email" required>
      <input name="password" type="password" placeholder="${esc(login ? t('password') : t('passwordNew'))}"
             ${login ? '' : `minlength="8" pattern="${PASS_PATTERN}" title="${esc(t('passwordHint'))}"`}
             autocomplete="${login ? 'current-password' : 'new-password'}" required>
      ${login ? `<button class="link-btn" id="forgot" type="button">${esc(t('forgot'))}</button>`
              : `<input name="password2" type="password" placeholder="${esc(t('passwordConfirm'))}" autocomplete="new-password" required>`}`;
  app.innerHTML = `
  <a class="back-site" href="${SITE_URL[L]}" title="${esc(t('backToSite'))}" aria-label="${esc(t('backToSite'))}">← FLR Sistemas</a>
  <section class="auth">
    <img class="logo" src="icons/icon.svg" alt="">
    <h1>Lista de Compras</h1>
    <p class="sub">${esc(t('tagline'))}</p>
    <form class="card" id="auth-form">
      ${fields}
      ${info ? `<div class="msg ${isErr ? 'err' : ''}">${esc(info)}</div>` : ''}
      <button class="primary" type="submit">${esc(forgot ? t('sendLink') : login ? t('signin') : t('signup'))}</button>
    </form>
    <button class="switch" id="switch-mode" type="button">
      ${esc(forgot ? t('backToLogin') : login ? t('noAccount') : t('haveAccount'))}
    </button>
    ${forgot ? '' : `<button class="ghost guest-btn" id="guest-btn" type="button">${esc(t('guestBtn'))}</button>`}
    <p class="sub"><a href="${HELP_URL[L]}" target="_blank" rel="noopener">${esc(t('help'))}</a> &middot; <a href="${PRIVACY_URL[L]}" target="_blank" rel="noopener">${esc(t('privacy'))}</a></p>
    <p class="sub">${langSelectHtml()}</p>
    ${appFootHtml()}
  </section>`;

  bindLangSelect();
  bindAppFoot();
  autoRefreshOnce();
  const form = $('#auth-form');
  bindPassMatch(form);
  const keepEmail = () => { state.prefillEmail = form.elements.email.value.trim(); };
  $('#switch-mode').onclick = () => { keepEmail(); state.authMode = forgot || !login ? 'login' : 'signup'; renderAuth(); };
  $('#guest-btn')?.addEventListener('click', openGuestWarning);
  const fg = $('#forgot');
  if (fg) fg.onclick = () => { keepEmail(); state.authMode = 'forgot'; renderAuth(); };
  form.onsubmit = async (e) => {
    e.preventDefault();
    const f = new FormData(e.target);
    const email = f.get('email').trim();
    const password = f.get('password');
    if (!login && !forgot && password !== f.get('password2')) { return renderAuth(t('errPassMismatch'), true); }
    const btn = e.target.querySelector('button[type=submit]');
    btn.disabled = true;
    try {
      if (forgot) {
        const { error } = await sb.auth.resetPasswordForEmail(email, { redirectTo: APP_URL });
        if (error) throw error;
        state.authMode = 'login';
        return renderAuth(t('forgotSent')); // não diz se o e-mail existe ou não
      }
      if (login) {
        const { error } = await sb.auth.signInWithPassword({ email, password });
        if (error) throw error;
      } else {
        const { data, error } = await sb.auth.signUp({
          email, password,
          options: { data: { nome: f.get('nome').trim() }, emailRedirectTo: APP_URL },
        });
        if (error) throw error;
        // Com confirmação de e-mail ligada, o Supabase NÃO devolve erro para um e-mail que já existe
        // (para não revelar quem tem conta): devolve um usuário sem 'identities'. A senha digitada aqui
        // é ignorada e a conta continua com a senha antiga. Avisamos o usuário.
        if (Array.isArray(data.user?.identities) && data.user.identities.length === 0) {
          state.authMode = 'login';
          state.prefillEmail = email;
          return renderAuth(`${t('errExists')} ${t('existsHint')}`, true);
        }
        if (!data.session) {
          state.authMode = 'login';
          renderAuth(t('accountCreated'));
        }
      }
    } catch (err) {
      state.prefillEmail = email;
      renderAuth(translateError(err), true);
    }
  };
}

// Tela de nova senha (depois de abrir o link do e-mail "esqueci minha senha")
function renderNewPassword(info = '', isErr = false) {
  app.innerHTML = `
  <section class="auth">
    <img class="logo" src="icons/icon.svg" alt="">
    <h1>Lista de Compras</h1>
    <p class="sub">${esc(t('newPassTitle'))}</p>
    <form class="card" id="np-form">
      <input name="password" type="password" placeholder="${esc(t('newPass'))}" minlength="8" pattern="${PASS_PATTERN}" title="${esc(t('passwordHint'))}" autocomplete="new-password" required>
      <input name="password2" type="password" placeholder="${esc(t('confirmNewPass'))}" autocomplete="new-password" required>
      ${info ? `<div class="msg ${isErr ? 'err' : ''}">${esc(info)}</div>` : ''}
      <button class="primary" type="submit">${esc(t('savePass'))}</button>
    </form>
    <button class="switch" id="np-cancel" type="button">${esc(t('cancel'))}</button>
  </section>`;
  const form = $('#np-form');
  bindPassMatch(form);
  $('#np-cancel').onclick = async () => { state.recovery = false; await logout(); route(); };
  form.onsubmit = async (e) => {
    e.preventDefault();
    const password = form.elements.password.value;
    if (password !== form.elements.password2.value) return renderNewPassword(t('errPassMismatch'), true);
    e.target.querySelector('button[type=submit]').disabled = true;
    const { error } = await sb.auth.updateUser({ password });
    if (error) return renderNewPassword(translateError(error), true);
    state.recovery = false;
    toast(t('passwordChanged'));
    route(); // já está logado: abre as listas
  };
}

function translateError(err) {
  const m = err?.message || String(err);
  if (/Invalid login/i.test(m)) return t('errBadLogin');
  if (/already registered/i.test(m)) return t('errExists');
  if (/Email not confirmed/i.test(m)) return t('errNotConfirmed');
  if (/password.*(at least|characters|weak|contain)|weak_password/i.test(m)) return t('errWeak');
  if (/different from the old|same_password/i.test(m)) return t('errSamePass');
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
  if (state.guest) return exitGuest(false); // sair do modo sem conta: as listas continuam neste aparelho
  teardownRealtime();
  await sb.auth.signOut();
}

/* ------------------------------ Roteamento ------------------------------ */
function route() {
  if (state.recovery) { if (state.user) return renderNewPassword(); state.recovery = false; }
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
  maybeTip('welcome');
  await loadLists();
  setupListsChannel();
}

async function loadLists() {
  const [lr, ir] = await Promise.all([
    sb.from('shopping_lists').select('*').order('created_at', { ascending: false }),
    sb.from('shopping_items').select('list_id, price, quantity'),
  ]);
  if (lr.error) { if (isOnline()) toast(t('errLoadLists'), true); return; }
  state.lists = applyListOps(lr.data); // excluídas/renomeadas sem sinal continuam valendo
  store.set(listsKey(), state.lists);
  if (!ir.error) {
    const totals = {};
    for (const r of ir.data) totals[r.list_id] = (totals[r.list_id] || 0) + lineTotal(r);
    state.totals = totals;
    store.set(totalsKey(), totals);
  }
  if (!state.listId) renderLists();
}

function renderLists() {
  const me = state.user.id;
  const { renamed: renamedPending, created: createdPending } = pendingListOps();
  app.innerHTML = `
  <div class="topbar">
    <h1>${esc(t('myLists'))}</h1>
    <button class="icon ghost" id="tips-btn" aria-label="${esc(t('tipsBtn'))}" title="${esc(t('tipsBtn'))}">💡</button>
    ${langSelectHtml()}
    <button class="ghost" id="logout" title="${esc(t('signout'))}">${esc(t('signout'))}</button>
  </div>
  ${state.guest ? `<div class="guest-banner"><span>⚠️ ${esc(t('guestBanner'))}</span><button type="button" id="guest-signup">${esc(t('guestSignup'))}</button></div>` : ''}
  ${!state.guest && !importDismissed && hasGuestData() ? `<div class="guest-banner import-banner"><span>📥 ${esc(t('importBanner'))}</span><button type="button" id="import-open">${esc(t('importBtn'))}</button></div>` : ''}
  <form class="newlist" id="newlist">
    <input name="name" placeholder="${esc(t('newListPh'))}" maxlength="80" required>
    <button class="primary" type="submit">${esc(t('create'))}</button>
  </form>
  <div class="pending" id="pending" hidden></div>
  <div class="list-cards">
    ${state.lists.length ? state.lists.map((l) => `
      <button class="list-card" data-open="${l.id}">
        <span class="ico">${l.owner_id === me ? '📋' : '🤝'}</span>
        <span class="grow"><span class="name">${esc(l.name)}${renamedPending[l.id] || createdPending[l.id] ? ' ⏳' : ''}</span><br>
          <span class="meta">${esc(l.owner_id === me ? t('yourList') : t('sharedWithYou'))}</span></span>
        <span class="total">${money(Math.round((state.totals[l.id] || 0) * 100) / 100)}</span>
        <span>›</span>
      </button>`).join('') : `<div class="empty">${t('noLists')}</div>`}
  </div>
  ${appFootHtml()}`;

  bindLangSelect();
  bindAppFoot();
  updatePending();
  $('#tips-btn').onclick = openTipsPanel;
  $('#logout').onclick = logout;
  $('#guest-signup')?.addEventListener('click', () => exitGuest(true));
  $('#import-open')?.addEventListener('click', openImportDialog);
  $('#newlist').onsubmit = async (e) => {
    e.preventDefault();
    const name = new FormData(e.target).get('name').trim();
    if (!name) return;
    // a lista aparece e abre na hora; o envio vai pela fila (na ordem certa, antes dos itens dela)
    const row = { id: newId(), name, owner_id: state.user.id, created_at: new Date().toISOString() };
    state.lists = [row, ...state.lists];
    store.set(listsKey(), state.lists);
    enqueueListNew(row, isOnline());
    flushQueue();
    location.hash = `#/list/${row.id}`;
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
  maybeTip('list');

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
  if (error) { if (isOnline()) toast(t('errLoadItems'), true); return; }
  applyItems(id, data);
}
function applyItems(id, data) {
  if (state.listId !== id) return;
  // marcações e itens novos ainda não enviados continuam valendo
  const adds = pendingAdds(id).filter((a) => !data.some((d) => d.id === a.row.id)).map((a) => localItem(a.row));
  const dels = pendingDels(), apply = pendingApplier();
  state.items = [...data.filter((d) => !dels.has(d.id)).map(apply), ...adds];
  store.set(itemsKey(id), state.items);
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
    ${state.guest ? '' : `<span class="live ${state.live ? 'on' : ''}" id="live" title="${esc(t('liveTitle'))}"></span>`}
    <button class="icon ghost" id="tips-btn" aria-label="${esc(t('tipsBtn'))}" title="${esc(t('tipsBtn'))}">💡</button>
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
  <div class="pending" id="pending" hidden></div>
  <div class="total-bar" id="total-bar"></div>
  <div id="items"></div>`;

  updatePending();
  bindNumeric(app);
  $('#back').onclick = () => (location.hash = '#/');
  $('#share').onclick = openShareDialog;
  $('#tips-btn').onclick = openTipsPanel;
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
    const row = { id: newId(), list_id: state.listId, name, quantity: parseQty(f.quantity.value), price: parsePrice(f.price.value), category: f.category.value, created_by: state.user.id, is_checked: false };
    f.name.value = ''; f.quantity.value = ''; f.price.value = ''; manualCat = false;
    f.name.focus();
    upsertItem(localItem(row)); // aparece na hora, com ou sem sinal
    if (!isOnline() || isPendingNewList(row.list_id)) { enqueueAdd(row, isOnline()); return flushQueue(); } // lista nova ainda não enviada: o item espera na fila, depois dela
    const { error } = await timed(sb.from('shopping_items').insert(row));
    if (error && error.code !== '23505') {
      if (isNetErr(error)) return enqueueAdd(row); // sinal fraco: guarda e envia depois
      removeItem(row.id);
      toast(t('errAddItem'), true);
    }
  };
}

function renderItems() {
  const box = $('#items');
  if (!box) return;
  const sorted = [...state.items].sort((a, b) => a.name.localeCompare(b.name, numLocale()));
  const pending = sorted.filter((i) => !i.is_checked);
  const done = sorted.filter((i) => i.is_checked);

  const pend = new Set(getQueue().filter((e) => !isDel(e)).map(entryItemId));
  const itemHtml = (i) => `
    <div class="item ${i.is_checked ? 'done' : ''}" data-id="${i.id}">
      <button class="check" data-act="toggle" aria-label="${esc(t('markItem'))}"><span class="box">✓</span></button>
      <button class="txt" data-act="edit">
        <span class="nm">${esc(i.name)}${pend.has(i.id) ? ` <span class="pend" title="${esc(t('waitingSignal'))}">⏳</span>` : ''}</span>
        ${qtyLine(i) ? `<span class="qty">${esc(qtyLine(i))}</span>` : ''}
      </button>
      ${i.price != null ? `<span class="price">${money(lineTotal(i))}</span>` : ''}
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
  const inCart = state.items.filter((i) => i.is_checked);
  const cart = sumPrices(inCart);
  const pct = state.items.length ? Math.round((inCart.length / state.items.length) * 100) : 0;
  const bar = $('#total-bar');
  if (bar) {
    bar.innerHTML = `<div class="tb-col"><span>🛒 ${esc(t('inCart'))} (${inCart.length}/${state.items.length})</span><strong>${money(cart)}</strong></div>
      <div class="tb-col end"><span>${esc(t('totalList'))}</span><strong>${money(total)}</strong></div>
      <div class="tb-prog" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}"><i style="width:${pct}%"></i></div>`;
  }
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
  const next = !it.is_checked;
  upsertItem({ ...it, is_checked: next }); // vale na hora, mesmo sem sinal
  if (isPendingAdd(id)) { editPendingAdd(id, { is_checked: next }); return flushQueue(); } // item ainda não enviado: a marca vai junto
  if (!isOnline()) return enqueue(it, next);
  const { error } = await timed(sb.from('shopping_items').update({ is_checked: next }).eq('id', id));
  if (error) {
    if (isNetErr(error)) return enqueue(it, next); // sinal fraco: guarda e envia depois
    upsertItem({ ...it, is_checked: !next });
    return toast(t('errUpdateItem'), true);
  }
  const isMark = (e) => !isAdd(e) && !isEdit(e) && !isDel(e) && e.id === id;
  if (getQueue().some(isMark)) setQueue(getQueue().filter((e) => !isMark(e))); // o envio de agora vale mais que a marcação antiga
}

async function deleteItem(id) {
  const it = state.items.find((x) => x.id === id);
  if (!it) return;
  if (isPendingAdd(id)) { dropPendingAdd(id); return removeItem(id); } // nunca chegou ao banco: basta descartar
  removeItem(id); // some da tela na hora, com ou sem sinal
  enqueueDel(it, isOnline());
  flushQueue();
}

async function clearChecked() {
  const checked = state.items.filter((i) => i.is_checked);
  if (!checked.length || !confirm(t('confirmClear', { n: checked.length }))) return;
  for (const i of checked) { if (isPendingAdd(i.id)) dropPendingAdd(i.id); else enqueueDel(i, isOnline()); }
  state.items = state.items.filter((i) => !i.is_checked);
  persistItems();
  renderItems();
  flushQueue();
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
    // só vão os campos que mudaram: uma edição sem sinal não desfaz o que outra pessoa alterou nos outros campos
    const same = (k) => (k === 'price' ? (Number(it.price) || 0) === (Number(patch.price) || 0) && (it.price == null) === (patch.price == null) : (it[k] ?? null) === (patch[k] ?? null));
    for (const k of Object.keys(patch)) if (same(k)) delete patch[k];
    if (!Object.keys(patch).length) return;
    upsertItem({ ...it, ...patch }); // vale na hora, com ou sem sinal
    if (isPendingAdd(id)) return editPendingAdd(id, patch); // item novo ainda não enviado: edita a cópia da fila
    enqueueEdit(it, patch, isOnline());
    flushQueue();
  };
  dlg.showModal();
}

function openShareDialog() {
  const l = currentList();
  const owner = isOwner();
  const me = state.user.id;
  dlg.classList.toggle('guest', !!state.guest); // sem conta: sem lista de participantes
  dlg.innerHTML = `
  <h3>👥 ${esc(l?.name || t('listDefault'))}</h3>
  <div class="stack">
    ${owner && !state.guest && !tipSeen('share') ? `<div class="msg tiphint" id="share-tip"><strong>${esc(t('tip_share_t'))}</strong><br>${t('tip_share_b')}<br><button type="button" data-tip-ok>${esc(t('tipOk'))}</button></div>` : ''}
    ${owner ? `<form id="rename-form" class="newlist"><input name="name" value="${esc(l?.name || '')}" maxlength="80" required aria-label="${esc(t('renameList'))}" placeholder="${esc(t('renameList'))}"><button class="primary" type="submit">${esc(t('save'))}</button></form>` : ''}
    ${state.guest ? `<div class="msg">${esc(t('guestNoShare'))}</div>` : owner && isPendingNewList(l?.id) ? `<div class="msg">${esc(t('listNotSent'))}</div>` : ''}
    ${owner && !state.guest && !isPendingNewList(l?.id) ? `
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
  const tipOk = dlg.querySelector('[data-tip-ok]');
  if (tipOk) tipOk.onclick = () => { markTip('share'); dlg.querySelector('#share-tip').remove(); };

  const rf = dlg.querySelector('#rename-form');
  if (rf) rf.onsubmit = (e) => {
    e.preventDefault();
    const name = e.target.elements.name.value.trim();
    if (!name || name === l.name) return;
    dlg.close();
    const cur = currentList();
    cur.name = name; // vale na hora, com ou sem sinal
    store.set(listsKey(), state.lists);
    $('#list-title').textContent = name;
    if (isPendingNewList(cur.id)) editPendingNewList(cur.id, name); // ainda não enviada: troca o nome na fila
    else enqueueListRename(cur, name, isOnline());
    flushQueue();
  };

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
    const gone = currentList();
    dlg.close();
    if (isPendingNewList(gone.id)) dropListEntries(gone.id); // nunca chegou ao banco: basta descartar
    else enqueueListGone(gone, 'ldel', isOnline()); // some na hora; o servidor recebe quando houver sinal
    afterListGone();
    flushQueue();
  };
  const leave = dlg.querySelector('#leave-list');
  if (leave) leave.onclick = async () => {
    if (!confirm(t('confirmLeave'))) return;
    const gone = currentList();
    dlg.close();
    enqueueListGone(gone, 'lleave', isOnline());
    afterListGone();
    flushQueue();
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
        if (!pendingDels().has(p.new.id)) upsertItem(withPending(p.new));
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
      if (status === 'SUBSCRIBED') { flushQueue(); loadItems(); }
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
  if (document.visibilityState !== 'visible' || !state.user || !isOnline()) return;
  flushQueue();
  if (state.listId) loadItems(); else loadLists();
});

/* ------------------------------ PWA ------------------------------------- */
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./service-worker.js').catch((e) => console.warn('SW failed', e));
  });
}

init();
