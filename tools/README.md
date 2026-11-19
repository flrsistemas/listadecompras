# tools/ — geradores das páginas

Estes scripts (Python 3, sem dependências) geram:
- no **app** (este repositório): `sobre/` (apresentação), `ajuda/` e `privacy*.html`, nos 3 idiomas;
- no **site da empresa** (`flrsistemas/flrsistemas.github.io`): página inicial, abas Novidades/Ajuda/Contato/Privacidade
  (pt na raiz, `/en/` e `/es/`), favicons e redirecionamentos dos endereços antigos;
- no **Preço Certo** (`flrsistemas/precocerto`, pasta `docs/`): as políticas de privacidade (pt, en, es), a largura das
  páginas e a ampliação de imagens.

## Como usar
1. Clone os dois outros repositórios ao lado (pasta padrão `~/flr-work`, ou aponte com `FLR_WORK`):
   ```bash
   mkdir -p ~/flr-work && cd ~/flr-work
   gh repo clone flrsistemas/flrsistemas.github.io site
   gh repo clone flrsistemas/precocerto pc
   ```
2. Rode o build a partir deste repositório:
   ```bash
   python tools/build.py            # gera as páginas e confere os links
   python tools/build.py --shots    # antes, refaz as capturas de tela (precisa do Google Chrome)
   ```
3. Veja `git status` nos 3 repositórios, teste (abaixo) e faça commit e push só do que mudou.

Variáveis opcionais: `FLR_WORK`, `FLR_SITE`, `FLR_PC`, `FLR_OUT` (temporários) e `CHROME` (caminho do Chrome). Ver `config.py`.

## Onde editar cada coisa
| O que | Arquivo |
|---|---|
| Notícias (Novidades), textos do site, cartões, abas, redirecionamentos | `gen_site.py` (as notícias são os blocos `_NEWS…`, a mais nova por último) |
| Perguntas e respostas da Ajuda do app (pt/en/es) | `help_content.py` |
| Apresentação do app (`sobre/`) e capturas de tela | `gen_sobre.py`, `gen_shots.py` |
| Página de Ajuda do app | `gen_ajuda.py` (usa `help_content.py`) |
| Política de privacidade do app / do Preço Certo | `gen_privacy.py` / `gen_pc_privacy.py` |
| Largura das páginas, ampliação de imagens | `add_wide.py`, `add_lightbox.py` |
| Ícones (PNG e favicon) | `icons/*.svg` + `gen_icons.py` |

Os scripts são **idempotentes**: rodar de novo não duplica nada. Depois de editar um deles, rode o build completo, porque
`add_wide.py` e `add_lightbox.py` precisam rodar depois dos geradores.

## Testar
- `build.py` termina montando a árvore do site em `OUT/tree` (`/`, `/listadecompras/`, `/precocerto/`) e checando links internos.
- Para ver no navegador: `python -m http.server 8766 --directory ~/flr-work/out/tree` e abrir `http://localhost:8766/`.
- `testfiles/` tem uma página (`/test/app-test.html`) que roda o app inteiro com um **Supabase simulado**
  (`mock-supabase.js`), sem login nem rede. Parâmetros: `?lang=pt|en|es`, `nosession=1` (tela de entrada),
  `start=lists`, `keep=1` (mantém o localStorage), `fail=1` (as chamadas falham como "sem sinal"),
  `hash=%23…` (simula o retorno de um link de e-mail). Também dá para usar `__db` no console para ver as chamadas.

## Observações
- Os geradores escrevem com fim de linha LF; o Git normaliza. Se `git status` mostrar arquivos "modificados" sem diferença
  de conteúdo, é só isso (`git add -A && git diff --cached --stat` confirma).
- Aumentar `VERSION` em `service-worker.js` depois de mudar o app (e `SHELL_FILES` em `js/app.js` se criar arquivos novos).
