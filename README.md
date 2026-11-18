# 🛒 Lista de Compras Compartilhada

PWA estático (HTML + CSS + JS puro) com Supabase (Auth + Postgres + Realtime), pronto para o GitHub Pages.

## Estrutura
```
index.html · manifest.json · service-worker.js · supabase_setup.sql
css/style.css · js/config.js (suas chaves) · js/app.js · icons/icon.svg
.github/workflows/keep-alive.yml
```

## Passo a passo

### 1. Banco de dados
Supabase → **SQL Editor → New query** → cole todo o `supabase_setup.sql` → **Run**.

> Dica: em **Authentication → Providers → Email**, desative *Confirm email* se quiser entrar logo após o cadastro.

### 2. Chaves
- `js/config.js`: preencha `SUPABASE_URL` e `SUPABASE_ANON_KEY` (Supabase → *Project Settings → API*).
- GitHub → *Settings → Secrets and variables → Actions*: crie `SUPABASE_URL` e `SUPABASE_ANON_KEY` (mesmos valores) para o keep-alive.

### 3. Publicar
Suba o projeto ao GitHub → *Settings → Pages* → Branch `main`, pasta `/ (root)`. Domínio próprio: campo *Custom domain*.
No Supabase → *Authentication → URL Configuration*, coloque a URL do site em *Site URL*.

### 4. Testar no celular
Abra a URL (HTTPS) → Android/Chrome: menu ⋮ → *Instalar app*; iPhone/Safari: Compartilhar → *Adicionar à Tela de Início*.
Crie duas contas, compartilhe uma lista pelo ícone 👥 e veja os itens sincronizando em tempo real.

## Notas
- Só é possível compartilhar com e-mails já cadastrados.
- Offline: a última versão carregada abre do `localStorage`; alterações exigem conexão.
- Após atualizar arquivos, aumente `VERSION` no `service-worker.js` se notar cache antigo.
