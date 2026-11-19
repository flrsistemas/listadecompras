"""Regenera as paginas geradas (app, empresa e Preco Certo) e confere os links.

  python tools/build.py            paginas + conferencia de links
  python tools/build.py --shots    refaz antes as capturas de tela do app (precisa do Chrome)
"""
import os, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import APP, TOOLS, OUT, SITE, PC_DOCS

for need in (SITE, PC_DOCS):
    if not os.path.isdir(need):
        sys.exit('Falta a pasta %s. Veja tools/README.md (como clonar os repositorios).' % need)


def run(script):
    print('>>', script)
    subprocess.run([sys.executable, os.path.join(TOOLS, script)], check=True, cwd=TOOLS)


if '--shots' in sys.argv:
    run('gen_shots.py')
    for f in os.listdir(os.path.join(OUT, 'shots')):
        if f.endswith('.png'):
            shutil.copyfile(os.path.join(OUT, 'shots', f), os.path.join(APP, 'sobre', 'img', f))

for script in ('gen_privacy.py', 'gen_sobre.py', 'gen_ajuda.py', 'gen_pc_privacy.py', 'gen_site.py', 'add_wide.py', 'add_lightbox.py', 'check_links.py'):
    run(script)
print('Pronto. Confira `git status` nos 3 repositorios e publique o que mudou.')
