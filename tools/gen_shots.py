import os, subprocess

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import APP, OUT as _OUT, CHROME
OUT = os.path.join(_OUT, 'shots')
CSS = 'file:///' + os.path.join(APP, 'css', 'style.css').replace('\\', '/')
os.makedirs(OUT, exist_ok=True)

# R$ conforme o formato do app em cada idioma (en: R$166.60 | pt/es: R$ 166,60)
def mk(lang):
    if lang == 'en':
        return lambda cents: 'R$%s' % ('{:,.2f}'.format(cents / 100))
    def f(cents):
        s = '{:,.2f}'.format(cents / 100).replace(',', 'X').replace('.', ',').replace('X', '.')
        return 'R$&nbsp;' + s
    return f

D = {
 'en': dict(html='en', my='🛒 My lists', out='Sign out', ph='New list (e.g. Monthly groceries)', create='Create',
            mine='Your list', shared='Shared with you',
            lists=['Monthly groceries', 'Sunday barbecue', 'Pharmacy', 'Birthday party'],
            add='Add item…', cat='Produce', qty='Qty', price='Unit price (R$)', addb='Add', total='List total', incart='In cart',
            groups=[('🥬', 'Produce'), ('🥩', 'Butcher'), ('🥖', 'Bakery'), ('🧀', 'Dairy')],
            items=[('Banana', '1.5', 780), ('Tomato', '1', 650), ('Chicken', '2', 3190), ('French bread', '6', 420), ('Milk', '6', 3840), ('Mozzarella cheese', '0.5', 2900)],
            done=[('Rice', '5', 2890), ('Coffee', '1', 1990)], bought='✅ Bought (2)', clear='Clear bought',
            email='E-mail of who will join', share='Share', owner='owner', rem='Remove', dele='Delete list', close='Close'),
 'pt': dict(html='pt-BR', my='🛒 Minhas listas', out='Sair', ph='Nova lista (ex: Mercado do Mês)', create='Criar',
            mine='Sua lista', shared='Compartilhada com você',
            lists=['Mercado do mês', 'Churrasco de domingo', 'Farmácia', 'Festa de aniversário'],
            add='Adicionar item…', cat='Hortifruti', qty='Qtd', price='Preço unitário (R$)', addb='Adicionar', total='Total da lista', incart='No carrinho',
            groups=[('🥬', 'Hortifruti'), ('🥩', 'Açougue'), ('🥖', 'Padaria'), ('🧀', 'Laticínios')],
            items=[('Banana', '1,5', 780), ('Tomate', '1', 650), ('Frango', '2', 3190), ('Pão francês', '6', 420), ('Leite', '6', 3840), ('Queijo mussarela', '0,5', 2900)],
            done=[('Arroz', '5', 2890), ('Café', '1', 1990)], bought='✅ Comprados (2)', clear='Limpar comprados',
            email='E-mail de quem vai participar', share='Compartilhar', owner='dono', rem='Remover', dele='Excluir lista', close='Fechar'),
 'es': dict(html='es', my='🛒 Mis listas', out='Salir', ph='Nueva lista (ej: Compra del mes)', create='Crear',
            mine='Tu lista', shared='Compartida contigo',
            lists=['Compra del mes', 'Asado del domingo', 'Farmacia', 'Fiesta de cumpleaños'],
            add='Agregar artículo…', cat='Frutas y verduras', qty='Cant.', price='Precio unitario (R$)', addb='Agregar', total='Total de la lista', incart='En el carrito',
            groups=[('🥬', 'Frutas y verduras'), ('🥩', 'Carnicería'), ('🥖', 'Panadería'), ('🧀', 'Lácteos')],
            items=[('Plátano', '1,5', 780), ('Tomate', '1', 650), ('Pollo', '2', 3190), ('Pan', '6', 420), ('Leche', '6', 3840), ('Queso mozzarella', '0,5', 2900)],
            done=[('Arroz', '5', 2890), ('Café', '1', 1990)], bought='✅ Comprados (2)', clear='Limpiar comprados',
            email='Correo de quien va a participar', share='Compartir', owner='dueño', rem='Quitar', dele='Eliminar lista', close='Cerrar'),
}

TOTALS = [16660, 9690, 4250, 23315]


def item(m, nm, qty=None, price=None, done=False):
    """price = total da linha (centavos); a tela mostra 'qtd x preco unitario' e o total."""
    q = float(qty.replace(',', '.')) if qty else 1.0
    unit = round(price / q) if price else None
    line = ('%s &times; %s' % (qty, m(unit))) if (qty and price and q != 1.0) else (qty or '')
    return ('<div class="item %s"><button class="check"><span class="box">✓</span></button>'
            '<button class="txt"><span class="nm">%s</span>%s</button>%s'
            '<button class="icon ghost del">✕</button></div>') % (
        'done' if done else '', nm,
        '<span class="qty">%s</span>' % line if line else '',
        '<span class="price">%s</span>' % m(price) if price else '')


def scenes(lang):
    d = D[lang]
    m = mk(lang)
    head = ('<!DOCTYPE html><html lang="%s"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<link rel="stylesheet" href="%s"></head><body><main id="app">') % (d['html'], CSS)
    owners = ['mine', 'shared', 'mine', 'shared']
    icons = {'mine': '📋', 'shared': '🤝'}
    cards = ''.join(
        '<button class="list-card"><span class="ico">%s</span><span class="grow"><span class="name">%s</span><br>'
        '<span class="meta">%s</span></span><span class="total">%s</span><span>›</span></button>' % (
            icons[o], n, d[o], m(tt)) for n, o, tt in zip(d['lists'], owners, TOTALS))
    lists = head + ('<div class="topbar"><h1>%s</h1><button class="ghost">%s</button></div>'
                    '<form class="newlist"><input placeholder="%s"><button class="primary" type="button">%s</button></form>'
                    '<div class="list-cards">%s</div></main></body></html>') % (d['my'], d['out'], d['ph'], d['create'], cards)

    it = d['items']
    body = ('<div class="topbar"><button class="icon ghost">←</button><h1>%s</h1><span class="live on"></span><button class="icon ghost">👥</button></div>'
            '<form class="card add-form"><input class="name" placeholder="%s"><select><option>🥬 %s</option></select>'
            '<input placeholder="%s" style="grid-column:2/3;grid-row:2">'
            '<input placeholder="%s" style="grid-column:1/2;grid-row:3">'
            '<button class="primary" type="button" style="grid-column:2/3;grid-row:3">%s</button></form>'
            '<div class="total-bar"><div class="tb-col"><span>🛒 %s (2/8)</span><strong>%s</strong></div><div class="tb-col end"><span>%s</span><strong>%s</strong></div><div class="tb-prog"><i style="width:25%%"></i></div></div><div id="items">'
            '<h2>%s %s</h2>%s%s<h2>%s %s</h2>%s<h2>%s %s</h2>%s<h2>%s %s</h2>%s%s'
            '<h2 class="bar"><span>%s</span><button class="danger">%s</button></h2>%s%s</div></main>') % (
        d['lists'][0], d['add'], d['cat'], d['qty'], d['price'], d['addb'], d['incart'], m(4880), d['total'], m(TOTALS[0]),
        d['groups'][0][0], d['groups'][0][1], item(m, *it[0]), item(m, *it[1]),
        d['groups'][1][0], d['groups'][1][1], item(m, *it[2]),
        d['groups'][2][0], d['groups'][2][1], item(m, *it[3]),
        d['groups'][3][0], d['groups'][3][1], item(m, *it[4]), item(m, *it[5]),
        d['bought'], d['clear'], item(m, *d['done'][0], done=True), item(m, *d['done'][1], done=True))
    items = head + body + '</body></html>'

    dialog = ('<dialog id="d"><h3>👥 %s</h3><div class="stack"><form class="stack"><input type="email" placeholder="%s">'
              '<button class="primary" type="button">%s</button></form><ul class="members">'
              '<li><span class="grow">Ana Souza<br><small>ana@example.com</small></span><span class="tag">%s</span></li>'
              '<li><span class="grow">Carlos Lima<br><small>carlos@example.com</small></span><button class="danger">%s</button></li>'
              '<li><span class="grow">Marta Lima<br><small>marta@example.com</small></span><button class="danger">%s</button></li></ul>'
              '<div class="row" style="justify-content:space-between"><button class="danger">%s</button><button>%s</button></div></div></dialog>'
              '<script>document.getElementById("d").showModal();</script>') % (
        d['lists'][0], d['email'], d['share'], d['owner'], d['rem'], d['rem'], d['dele'], d['close'])
    share = head + body + dialog + '</body></html>'
    return {'lista-listas': lists, 'lista-itens': items, 'lista-compartilhar': share}


for lang in ('en', 'pt', 'es'):
    for name, html in scenes(lang).items():
        hp = os.path.join(OUT, '%s-%s.html' % (name, lang))
        with open(hp, 'w', encoding='utf-8') as f:
            f.write(html)
        png = os.path.join(OUT, '%s-%s.png' % (name, lang))
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=500,1130',
                        '--force-device-scale-factor=2', '--virtual-time-budget=2000', '--screenshot=' + png,
                        'file:///' + hp.replace('\\', '/')], check=True, capture_output=True, timeout=60)
        print(name, lang, os.path.getsize(png))
