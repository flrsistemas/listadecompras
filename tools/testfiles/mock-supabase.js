// Supabase simulado para testar o app sem login nem rede.
// window.__db.fail = true => toda chamada falha como "Failed to fetch" (sem sinal)
export function createClient() {
  const db = (window.__db = window.__db || {});
  db.calls = db.calls || [];
  db.fail = !!db.fail;
  db.hang = !!db.hang;

  function builder(table) {
    let op = 'select', payload = null; const filters = [];
    const b = {
      select() { return b; },
      update(p) { op = 'update'; payload = p; return b; },
      insert(p) { op = 'insert'; payload = p; return b; },
      delete() { op = 'delete'; return b; },
      eq(k, v) { filters.push([k, v]); return b; },
      in(k, arr) { filters.push([k, arr, 'in']); return b; },
      order() { return b; }, single() { return b; },
      abortSignal(sig) { b._sig = sig; return b; },
      then(res, rej) { return run().then(res, rej); },
    };
    async function run() {
      if (db.hang) {
        return new Promise((resolve) => { b._sig && b._sig.addEventListener('abort', () => resolve({ data: null, error: { message: 'AbortError: signal is aborted' } })); });
      }
      if (db.fail) return { data: null, error: { message: 'TypeError: Failed to fetch' } };
      db.calls.push({ table, op, payload, filters });
      if (table === 'shopping_lists') {
        const m = (l) => filters.every(([k, v]) => l[k] === v);
        if (op === 'insert') {
          if (db.rejectListInserts) return { data: null, error: { code: '42501', message: 'new row violates row-level security policy' } };
          if (db.lists.some((l) => l.id === payload.id)) return { data: null, error: { code: '23505', message: 'duplicate key' } };
          db.lists.unshift({ ...payload });
          return { data: null, error: null };
        }
        if (op === 'update') { db.lists.filter(m).forEach((l) => Object.assign(l, payload)); return { data: null, error: null }; }
        if (op === 'delete') {
          const ids = db.lists.filter(m).map((l) => l.id);
          db.lists = db.lists.filter((l) => !ids.includes(l.id));
          db.items = db.items.filter((i) => !ids.includes(i.list_id)); // cascata
          return { data: null, error: null };
        }
        return { data: db.lists.map((l) => ({ ...l })), error: null };
      }
      if (table === 'list_members') {
        if (op === 'delete') {
          db.left = (db.left || []).concat([filters.map((f) => f.join('=')).join('&')]);
          db.lists = db.lists.filter((l) => !(filters.find((f) => f[0] === 'list_id' && f[1] === l.id) && l.owner_id !== 'u1')); // saiu: a lista some para mim
          return { data: null, error: null };
        }
        return { data: db.members || [], error: null };
      }
      if (table === 'shopping_items') {
        if (op === 'insert') {
          if (db.rejectInserts) return { data: null, error: { code: '42501', message: 'new row violates row-level security policy' } };
          if (db.items.some((i) => i.id === payload.id)) return { data: null, error: { code: '23505', message: 'duplicate key value violates unique constraint' } };
          db.items.push({ updated_at: new Date().toISOString(), ...payload });
          return { data: null, error: null };
        }
        const match = (i) => filters.every(([k, v, kind]) => (kind === 'in' ? v.includes(i[k]) : i[k] === v));
        if (op === 'update') {
          db.items.filter(match).forEach((i) => Object.assign(i, payload));
          return { data: null, error: null };
        }
        if (op === 'delete') {
          db.items = db.items.filter((i) => !match(i));
          return { data: null, error: null };
        }
        return { data: db.items.map((i) => ({ ...i })), error: null };
      }
      return { data: [], error: null };
    }
    return b;
  }

  return {
    from: builder,
    rpc: async () => ({ error: null }),
    auth: {
      getSession: async () => (window.__sessionCalls = (window.__sessionCalls || 0) + 1, { data: { session: window.__noSession ? null : { user: { id: 'u1', email: 'teste@example.com' } } } }),
      signUp: async (args) => { window.__signUpArgs = args; return { data: { user: { identities: args.email === 'existente@exemplo.com' ? [] : [{}] }, session: null }, error: null }; },
      signInWithPassword: async () => ({ error: { message: 'Invalid login credentials' } }),
      onAuthStateChange(cb) { window.__authCb = cb; },
      resetPasswordForEmail: async (email, opts) => { window.__resetArgs = { email, opts }; return { error: null }; },
      setSession: async (tok) => {
        window.__setSessionArgs = tok;
        if (tok.access_token === 'bad') return { data: { session: null }, error: { message: 'invalid JWT' } };
        const user = { id: 'u1', email: 'teste@example.com' };
        window.__noSession = false;
        window.__authCb && window.__authCb('SIGNED_IN', { user });
        return { data: { session: { user } }, error: null };
      },
      updateUser: async (attrs) => {
        window.__updateArgs = attrs;
        if (attrs.password === 'Igual1234') return { error: { message: 'New password should be different from the old password.' } };
        return { data: {}, error: null };
      },
      signOut: async () => {},
    },
    channel() { const ch = { on() { return ch; }, subscribe(cb) { window.__subscribe = cb; setTimeout(() => cb && cb('SUBSCRIBED'), 30); return ch; } }; return ch; },
    removeChannel() {},
  };
}
