// "Modo sem conta": guarda listas e itens só no localStorage deste aparelho, sem falar com o Supabase.
// Imita apenas o trecho da API do cliente do Supabase que o app usa (from/select/insert/update/delete,
// eq/in/order/single, channel, rpc e auth), para o resto do app funcionar igual nos dois modos.
const KEY = 'lc:guest:db';
const TABLES = { shopping_lists: 'lists', shopping_items: 'items', list_members: 'members' };
const now = () => new Date().toISOString();
const uuid = () => (crypto.randomUUID ? crypto.randomUUID()
  : 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => { const r = (Math.random() * 16) | 0; return (c === 'x' ? r : (r & 3) | 8).toString(16); }));

function load() {
  try {
    const d = JSON.parse(localStorage.getItem(KEY));
    if (d && Array.isArray(d.lists) && Array.isArray(d.items)) return { lists: d.lists, items: d.items, members: d.members || [] };
  } catch { /* vazio ou corrompido */ }
  return { lists: [], items: [], members: [] };
}
const save = (db) => localStorage.setItem(KEY, JSON.stringify(db)); // pode lançar (cota cheia): quem chama trata

export const hasGuestData = () => load().lists.length > 0;

function withDefaults(table, row) {
  if (table === 'shopping_lists') return { id: uuid(), created_at: now(), ...row };
  if (table === 'shopping_items') return { id: uuid(), category: 'Outros', is_checked: false, quantity: null, price: null, updated_at: now(), ...row };
  return { added_at: now(), ...row };
}

export function createLocalClient() {
  function from(table) {
    const key = TABLES[table];
    let op = 'select', payload = null, one = false, order = null;
    const filters = [];
    const b = {
      select() { return b; }, // depois de insert/update, devolve as linhas afetadas
      insert(p) { op = 'insert'; payload = p; return b; },
      update(p) { op = 'update'; payload = p; return b; },
      delete() { op = 'delete'; return b; },
      eq(k, v) { filters.push((r) => r[k] === v); return b; },
      in(k, arr) { filters.push((r) => arr.includes(r[k])); return b; },
      order(k, o = {}) { order = [k, o.ascending !== false]; return b; },
      single() { one = true; return b; },
      abortSignal() { return b; },
      then(res, rej) { return Promise.resolve().then(run).then(res, rej); },
    };
    function run() {
      try {
        const db = load();
        const rows = db[key];
        const match = (r) => filters.every((f) => f(r));
        let out;
        if (op === 'insert') {
          out = [].concat(payload).map((r) => withDefaults(table, r));
          for (const r of out) {
            if (table !== 'list_members' && rows.some((x) => x.id === r.id)) return { data: null, error: { code: '23505', message: 'duplicate key' } };
          }
          rows.push(...out);
          // como no banco: quem cria a lista passa a ser membro dela
          if (table === 'shopping_lists') for (const r of out) db.members.push({ list_id: r.id, user_id: r.owner_id, added_at: now(), profiles: { email: '', nome: '' } });
        } else if (op === 'update') {
          out = rows.filter(match);
          for (const r of out) Object.assign(r, payload, table === 'shopping_items' ? { updated_at: now() } : {});
        } else if (op === 'delete') {
          out = rows.filter(match);
          db[key] = rows.filter((r) => !match(r));
          if (table === 'shopping_lists') { // cascata, como no banco
            const ids = new Set(out.map((l) => l.id));
            db.items = db.items.filter((i) => !ids.has(i.list_id));
            db.members = db.members.filter((m) => !ids.has(m.list_id));
          }
        } else {
          out = rows.filter(match).map((r) => ({ ...r }));
          if (order) { const [k, asc] = order; out.sort((a, c) => (a[k] > c[k] ? 1 : a[k] < c[k] ? -1 : 0) * (asc ? 1 : -1)); }
        }
        if (op !== 'select') save(db);
        return { data: one ? (out[0] ?? null) : out, error: null };
      } catch (e) {
        return { data: null, error: { code: 'local', message: String(e?.message || e) } };
      }
    }
    return b;
  }

  return {
    from,
    rpc: async () => ({ data: null, error: { message: 'Compartilhar exige uma conta' } }),
    channel() { const ch = { on() { return ch; }, subscribe(cb) { setTimeout(() => cb && cb('SUBSCRIBED'), 0); return ch; } }; return ch; },
    removeChannel() {},
    auth: {
      getSession: async () => ({ data: { session: null } }),
      onAuthStateChange() {},
      signOut: async () => {},
    },
  };
}
