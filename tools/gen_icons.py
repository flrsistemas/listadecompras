import os, struct, subprocess

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import APP, TOOLS, OUT as _OUT, CHROME
OUT = os.path.join(_OUT, 'icons')
os.makedirs(OUT, exist_ok=True)
APP_SVG = os.path.join(APP, 'icons', 'icon.svg')
PC_SVG = os.path.join(TOOLS, 'icons', 'precocerto.svg')
FLR_SVG = os.path.join(TOOLS, 'icons', 'flr.svg')
FLR_FAV = os.path.join(TOOLS, 'icons', 'flr-favicon.svg')


def url(p):
    return 'file:///' + p.replace('\\', '/')


def render(svg, size, name, inset=None, bg='#ffffff'):
    """Renderiza o SVG em size x size. inset (0-1) reduz o desenho para a zona segura de icones 'maskable'."""
    inner = 512 if inset is None else int(512 * inset)
    off = (512 - inner) // 2
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:%s;overflow:hidden}'
            'img{position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx}</style></head><body>'
            '<img src="%s"></body></html>') % (bg, off, off, inner, inner, url(svg))
    hp = os.path.join(OUT, name + '.html')
    open(hp, 'w', encoding='utf-8').write(html)
    png = os.path.join(OUT, name + '.png')
    if os.path.exists(png):
        os.remove(png)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=512,512',
                    '--force-device-scale-factor=%s' % (size / 512), '--virtual-time-budget=2000',
                    '--screenshot=' + png, url(hp)], check=True, capture_output=True, timeout=60)
    with open(png, 'rb') as f:
        d = f.read(24)
    w, h = struct.unpack('>II', d[16:24])
    print(name, w, h, os.path.getsize(png))
    assert (w, h) == (size, size), (name, w, h)


def make_ico(png_path, ico_path):
    data = open(png_path, 'rb').read()
    w, h = struct.unpack('>II', data[16:24])
    entry = struct.pack('<BBBBHHII', w if w < 256 else 0, h if h < 256 else 0, 0, 0, 1, 32, len(data), 22)
    open(ico_path, 'wb').write(struct.pack('<HHH', 0, 1, 1) + entry + data)


# Lista de Compras
render(APP_SVG, 192, 'app-icon-192')
render(APP_SVG, 512, 'app-icon-512')
render(APP_SVG, 512, 'app-maskable-512', inset=0.72, bg='#16a34a')
render(APP_SVG, 180, 'app-apple-touch-180')
render(APP_SVG, 32, 'app-favicon-32')
# Preco Certo
render(PC_SVG, 192, 'pc-icon-192')
render(PC_SVG, 512, 'pc-icon-512')
render(PC_SVG, 180, 'pc-apple-touch-180')
render(PC_SVG, 32, 'pc-favicon-32')
# FLR Sistemas
render(FLR_SVG, 180, 'flr-apple-touch-180')
render(FLR_SVG, 512, 'flr-icon-512')
render(FLR_FAV, 32, 'flr-favicon-32')
render(FLR_FAV, 48, 'flr-favicon-48')
make_ico(os.path.join(OUT, 'flr-favicon-32.png'), os.path.join(OUT, 'flr-favicon.ico'))
make_ico(os.path.join(OUT, 'pc-favicon-32.png'), os.path.join(OUT, 'pc-favicon.ico'))
print('ok')
