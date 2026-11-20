# 🛒 Lista de Compras

Listas de compras compartilhadas em tempo real. PWA estático (HTML + CSS + JS puro, sem build) com Supabase
(Auth + Postgres + Realtime), publicado no GitHub Pages em **https://flrsistemas.com.br/listadecompras/**.
Parte da [FLR Sistemas](https://flrsistemas.com.br/).

## O que o app faz
- **Listas compartilhadas por e-mail**, com atualização em tempo real para todos os participantes.
- **Itens** com categoria (sugerida pelo nome), quantidade e **preço unitário**; o app multiplica e mostra o total
  do item, da lista e de cada cartão. A barra do topo mostra o que já está **no carrinho** e o total da lista.
- **Funciona sem sinal:** marcar, adicionar, editar e remover itens e criar, renomear, excluir e sair de listas ficam
  numa fila no aparelho e são enviados, em ordem, quando a conexão volta (itens e listas pendentes aparecem com ⏳).
- **Modo sem conta** ("Usar sem conta"): as listas ficam só no `localStorage` do aparelho, sem nenhuma chamada ao
  Supabase e sem compartilhamento; ao criar uma conta dá para importar essas listas. Limpar os dados do navegador apaga tudo (o app avisa).
- **Conta:** cadastro com confirmação de senha e de e-mail, "Esqueci minha senha" e aviso de e-mail já cadastrado.
- **3 idiomas** (pt-BR, en, es), escolhidos pelo idioma do aparelho; dicas de uso (💡) e botão **"↻ Atualizar página"**
  (limpa service worker e caches sem apagar conta, listas nem alterações pendentes).

## Estrutura
```
index.html · manifest.json · service-worker.js · supabase_setup.sql · supabase_test_rls.sql
css/style.css · icons/ (SVG e PNG)
js/app.js          interface, rotas, fila offline, dicas, autenticação
js/i18n.js         textos em pt/en/es
js/local-store.js  "banco" local do modo sem conta (imita o cliente do Supabase)
js/config.js       SUPABASE_URL e SUPABASE_ANON_KEY (a anon key é pública por desenho; a segurança é o RLS)
sobre/ ajuda/ privacy*.html   páginas de apresentação, ajuda e privacidade (GERADAS, ver tools/)
tools/             geradores dessas páginas e do site da FLR Sistemas
.github/workflows/keep-alive.yml
```

## Banco de dados (Supabase)
1. SQL Editor → **New query** → cole o `supabase_setup.sql` → **Run** (idempotente: pode rodar de novo).
2. `supabase_test_rls.sql` testa as políticas de RLS e termina com um erro proposital que desfaz tudo (nada fica gravado).
3. Authentication → **URL Configuration:** *Site URL* e *Redirect URLs* com `https://flrsistemas.com.br/listadecompras/`
   (os e-mails de confirmação e de nova senha voltam para o app).
4. Para o `keep-alive` do GitHub Actions, crie os secrets `SUPABASE_URL` e `SUPABASE_ANON_KEY` no repositório.

## Publicar
GitHub → *Settings → Pages* → Branch `main`, pasta `/ (root)`. O domínio próprio vem da conta dona do Pages.
Depois de mudar arquivos do app, aumente `VERSION` no `service-worker.js` (e use "↻ Atualizar página" no celular).

## Páginas geradas e site da empresa
As páginas `sobre/`, `ajuda/` e `privacy*.html` **não são editadas à mão**: saem dos scripts em `tools/`, junto com o site
da FLR Sistemas (`flrsistemas/flrsistemas.github.io`) e as páginas do Preço Certo. Veja [`tools/README.md`](tools/README.md).

## Notas
- Só é possível compartilhar com e-mails já cadastrados, e só depois que a lista chegou ao servidor.
- Em conflito entre alterações feitas sem sinal e alterações de outra pessoa no mesmo item, vale a que chegar por último.
- Ao entrar numa conta num aparelho que tem listas do modo sem conta, o app oferece **importá-las** (copiadas como listas novas; dá para manter ou remover as cópias locais).
