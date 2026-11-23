"""Pagina do Preço Certo (pt/en/es): "Em 3 passos" + previa dos PDFs, e rodape com Privacidade, Termos e contato rapido.

Edita docs/index.html, docs/en/index.html e docs/es/index.html do clone do precocerto. Idempotente
(o bloco fica entre marcadores e o rodape so e trocado uma vez).
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import PC_DOCS
from gen_site import FOOT_CSS  # noqa: E402  (importar gera o site de novo: e idempotente)

START, END = '<!-- quick:start -->', '<!-- quick:end -->'

L = {
 'pt': dict(
  file='index.html', what='O que ele faz', pdfs='Os dois PDFs', contact='Contato',
  h='Em 3 passos',
  steps=[('Cadastre seus insumos e custos', 'Informe o preço da embalagem e a quantidade. O app calcula sozinho o custo por grama, mililitro ou unidade.'),
         ('Monte a receita e defina a margem', 'Adicione os insumos, o modo de preparo e o rendimento. O app mostra o custo real e o preço que paga o seu trabalho.'),
         ('Gere o orçamento e a ficha em PDF', 'Um PDF para quem compra e outro para a cozinha, prontos para enviar ou imprimir.')],
  res='Exemplo do resultado', cap1='Orçamento em PDF', cap2='Ficha para a cozinha', more='Ver os dois PDFs em detalhe',
  priv='/precocerto/privacy.html', terms='/termos/', privw='Privacidade', termsw='Termos de Uso',
  quick='Enviar mensagem', subject='Preço%20Certo'),
 'en': dict(
  file='en/index.html', what='What it does', pdfs='The two PDFs', contact='Contact',
  h='In 3 steps',
  steps=[('Add your ingredients and costs', 'Enter the package price and size. The app works out the cost per gram, milliliter or unit by itself.'),
         ('Build the recipe and set your margin', 'Add the ingredients, the method and the yield. The app shows the real cost and the price that pays you for your work.'),
         ('Create the quote and kitchen sheet as PDF', 'One PDF for the customer and another for the kitchen, ready to send or print.')],
  res='Example of the result', cap1='Quote as PDF', cap2='Kitchen sheet', more='See both PDFs in detail',
  priv='/precocerto/privacy-en.html', terms='/en/terms/', privw='Privacy', termsw='Terms of Use',
  quick='Send a message', subject='Pre%C3%A7o%20Certo'),
 'es': dict(
  file='es/index.html', what='Qué hace', pdfs='Los dos PDF', contact='Contacto',
  h='En 3 pasos',
  steps=[('Registra tus insumos y costos', 'Ingresa el precio del envase y su cantidad. La app calcula sola el costo por gramo, mililitro o unidad.'),
         ('Arma la receta y define tu margen', 'Agrega los insumos, el modo de preparación y el rendimiento. La app muestra el costo real y el precio que paga tu trabajo.'),
         ('Genera el presupuesto y la ficha en PDF', 'Un PDF para quien compra y otro para la cocina, listos para enviar o imprimir.')],
  res='Ejemplo del resultado', cap1='Presupuesto en PDF', cap2='Ficha de cocina', more='Ver los dos PDF en detalle',
  priv='/precocerto/privacy-es.html', terms='/es/terminos/', privw='Privacidad', termsw='Términos de Uso',
  quick='Enviar mensaje', subject='Pre%C3%A7o%20Certo'),
}

ALT1 = {'pt': 'Um orçamento em PDF com item, quantidade, preço unitário e total. Não mostra custos nem margem.',
        'en': 'A quote as PDF with item, quantity, unit price and total. It does not show costs or margin.',
        'es': 'Un presupuesto en PDF con artículo, cantidad, precio unitario y total. No muestra costos ni margen.'}
ALT2 = {'pt': 'Uma ficha para a cozinha em PDF com os ingredientes agrupados por parte da receita e o modo de preparo. Não mostra preços.',
        'en': 'A kitchen sheet as PDF with the ingredients grouped by recipe part and the method. It does not show prices.',
        'es': 'Una ficha de cocina en PDF con los ingredientes agrupados por parte de la receta y el modo de preparación. No muestra precios.'}

for lang, c in L.items():
    p = os.path.join(PC_DOCS, c['file'].replace('/', os.sep))
    s = open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    s = s.replace('\r\n', '\n')

    steps = ''.join('      <li>\n        <h4>%s</h4>\n        <p>%s</p>\n      </li>\n' % st for st in c['steps'])
    block = (START + '\n    <h3 class="section" id="quick">' + c['h'] + '</h3>\n    <ol class="steps three">\n' + steps + '    </ol>\n'
             '    <p class="note" style="margin-top:18px">' + c['res'] + ' &middot; <a href="#pdfs">' + c['more'] + '</a></p>\n'
             '    <div class="shots docs mini">\n'
             '      <figure class="doc doc-quote"><img src="/precocerto/img/quote-pdf.png" width="597" height="844" loading="lazy" alt="' + ALT1[lang] + '">'
             '<figcaption>' + c['cap1'] + '</figcaption></figure>\n'
             '      <figure class="doc"><img src="/precocerto/img/prep-sheet.png" width="595" height="845" loading="lazy" alt="' + ALT2[lang] + '">'
             '<figcaption>' + c['cap2'] + '</figcaption></figure>\n'
             '    </div>\n    ' + END + '\n\n')
    if START in s:
        s = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n\n', lambda m: block, s, count=1, flags=re.S)
    else:
        anchor = '    <h3 class="section">%s</h3>' % c['what']
        assert s.count(anchor) == 1, (lang, 'anchor')
        s = s.replace(anchor, block + anchor)

    # ancora para a secao completa dos PDFs
    h3 = '<h3 class="section">%s</h3>' % c['pdfs']
    if h3 in s:
        s = s.replace(h3, '<h3 class="section" id="pdfs">%s</h3>' % c['pdfs'])
    assert 'id="pdfs"' in s, (lang, 'pdfs')

    # miniaturas menores na previa (CSS marcado, para poder ser trocado)
    css = """/*quick*/
  main.wide ol.steps.three { grid-template-columns: repeat(3, 1fr); }
  .shots.docs.mini { align-items: flex-start; }
  .shots.docs.mini img { width: 150px; }
  .shots.docs.mini figcaption { max-width: 150px; }
  main.wide .shots.docs.mini img { width: 170px; }
  main.wide .shots.docs.mini figcaption { max-width: 170px; }
/*quick-end*/
"""
    # remove versoes anteriores (com ou sem marcas) e grava a atual
    s = re.sub(r'/\*quick\*/.*?/\*quick-end\*/\n', '', s, flags=re.S)
    s = re.sub(r'\n  \.shots\.docs\.mini img \{ width: 150px; \}\n.*?main\.wide \.shots\.docs\.mini figcaption \{ max-width: 170px; \}\n', '\n', s, flags=re.S)
    s = s.replace('</style>', css + '</style>', 1)
    if 'footer .quick' not in s:
        s = s.replace('</style>', FOOT_CSS + '</style>', 1)

    # rodape: privacidade, termos e contato rapido
    foot_re = re.compile(r'(%s: <a href="mailto:contato@flrsistemas\.com\.br">contato@flrsistemas\.com\.br</a>)\n(\s*)</p>' % c['contact'])
    if 'class="quick"' not in s:
        assert foot_re.search(s), (lang, 'footer')
        s = foot_re.sub(lambda m: (m.group(1) + '<br>\n      <a href="%s">%s</a> &middot; <a href="%s">%s</a>\n%s</p>\n'
                                   '    <p><a class="quick" href="mailto:contato@flrsistemas.com.br?subject=%s">&#9993; %s</a></p>' % (
            c['priv'], c['privw'], c['terms'], c['termsw'], m.group(2), c['subject'], c['quick'])), s, count=1)

    open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
    print('ok', lang)
