"""Caminhos usados pelos geradores. Podem ser trocados por variaveis de ambiente."""
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(TOOLS)  # repositorio do app (flrsistemas/listadecompras)
WORK = os.environ.get('FLR_WORK', os.path.join(os.path.expanduser('~'), 'flr-work'))
SITE = os.environ.get('FLR_SITE', os.path.join(WORK, 'site'))  # clone de flrsistemas/flrsistemas.github.io
PC = os.environ.get('FLR_PC', os.path.join(WORK, 'pc'))        # clone de flrsistemas/precocerto
PC_DOCS = os.path.join(PC, 'docs')
OUT = os.environ.get('FLR_OUT', os.path.join(WORK, 'out'))     # temporarios: capturas, icones e a arvore de teste
CHROME = os.environ.get('CHROME', r'C:\Program Files\Google\Chrome\Application\chrome.exe')  # capturas e icones
