"""Termos de Uso dos apps da FLR Sistemas (pt, en, es). Usado por gen_site.py.

Texto-padrao, simples e sem revisao juridica: revise antes de depender dele em disputas.
"""

EMAIL = 'contato@flrsistemas.com.br'

TERMS = {
 'pt': dict(
  title='Termos de Uso', desc='Termos de Uso dos apps Preço Certo e Lista de Compras, da FLR Sistemas.',
  updated='Última atualização: 23 de novembro de 2026',
  intro='Estes termos valem para os apps <strong>Preço Certo</strong> e <strong>Lista de Compras</strong>, da FLR Sistemas, e para este site. Eles são curtos de propósito.',
  sections=[
   ('1. Aceitação', ['Ao baixar ou usar os apps, você concorda com estes termos. Se não concordar, não use os apps.']),
   ('2. Os apps', ['<strong>Preço Certo:</strong> app Android que calcula o custo e o preço de venda de receitas e gera orçamento e ficha de cozinha em PDF. Funciona no seu celular, sem conta.',
                   '<strong>Lista de Compras:</strong> app web (PWA) para criar e compartilhar listas de compras. A conta é opcional: dá para usar sem conta, com as listas só no aparelho.']),
   ('3. Uso permitido', ['Use os apps para fins pessoais ou profissionais lícitos. Não tente burlar a segurança, acessar dados de outras pessoas, sobrecarregar o serviço nem usar os apps para algo ilegal ou para prejudicar alguém.']),
   ('4. Conta e compartilhamento (Lista de Compras)', ['Você é responsável pela senha e pelo e-mail da sua conta. Ao convidar alguém para uma lista, essa pessoa passa a ver os itens, os preços e o nome e o e-mail dos participantes. O dono da lista pode remover participantes e excluir a lista.',
                   'No modo sem conta, as listas ficam só neste aparelho e neste navegador, sem cópia de segurança. Limpar os dados do navegador, ou desinstalar o app, apaga tudo, sem como recuperar.']),
   ('5. O seu conteúdo', ['As listas, receitas, preços e orçamentos que você cria são seus. Você só nos autoriza a guardá-los e exibi-los para você e para quem você convidar, o que for necessário para o app funcionar.']),
   ('6. Valores e orçamentos (Preço Certo)', ['Os cálculos usam os valores que você informa e são uma ajuda para decidir. Confira preços, margens e orçamentos antes de usá-los com clientes. O app não é consultoria contábil, fiscal ou jurídica.']),
   ('7. Disponibilidade e mudanças', ['Os apps são oferecidos “como estão”, sem garantia de funcionamento ininterrupto. Podemos corrigir, alterar, suspender ou encerrar recursos. Mudanças relevantes são avisadas em Novidades.']),
   ('8. Limitação de responsabilidade', ['Na medida permitida pela lei, a FLR Sistemas não responde por lucros cessantes, danos indiretos nem por perda de dados causada por limpeza do aparelho ou do navegador, uso indevido ou indisponibilidade. Nada aqui limita direitos que a lei não permita limitar, como os do consumidor.']),
   ('9. Encerramento', ['Você pode parar de usar os apps quando quiser e pedir a exclusão da conta e dos dados escrevendo para o e-mail abaixo. Podemos suspender contas que violem estes termos.']),
   ('10. Propriedade intelectual', ['O nome, os logotipos e o código dos apps pertencem à FLR Sistemas. Estes termos não transferem esses direitos.']),
   ('11. Privacidade', ['O tratamento dos seus dados está descrito na <a href="/privacidade/">política de privacidade</a> de cada app.']),
   ('12. Mudanças nestes termos', ['Quando mudarmos estes termos, publicamos a nova versão nesta página, com a data de atualização.']),
   ('13. Lei aplicável', ['Valem as leis do Brasil. Em relações de consumo, vale o foro do domicílio do consumidor.']),
   ('14. Contato', ['Dúvidas sobre estes termos: <a href="mailto:%s">%s</a>.' % (EMAIL, EMAIL)]),
  ]),
 'en': dict(
  title='Terms of Use', desc='Terms of Use for the Preço Certo and Lista de Compras apps, by FLR Sistemas.',
  updated='Last updated: November 23, 2026',
  intro='These terms apply to the <strong>Preço Certo</strong> and <strong>Lista de Compras</strong> apps by FLR Sistemas, and to this website. They are short on purpose.',
  sections=[
   ('1. Acceptance', ['By downloading or using the apps, you agree to these terms. If you do not agree, do not use the apps.']),
   ('2. The apps', ['<strong>Preço Certo:</strong> an Android app that calculates the cost and selling price of recipes and creates a quote and a kitchen sheet as PDF. It works on your phone, with no account.',
                    '<strong>Lista de Compras:</strong> a web app (PWA) to create and share shopping lists. An account is optional: you can use it without one, with the lists kept only on the device.']),
   ('3. Acceptable use', ['Use the apps for lawful personal or professional purposes. Do not try to bypass security, access other people\'s data, overload the service, or use the apps for anything illegal or to harm anyone.']),
   ('4. Account and sharing (Lista de Compras)', ['You are responsible for your account password and e-mail. When you invite someone to a list, that person can see the items, the prices and the name and e-mail of the members. The list owner can remove members and delete the list.',
                    'In no-account mode, lists stay only on this device and in this browser, with no backup. Clearing the browser data, or uninstalling the app, erases everything with no way to recover it.']),
   ('5. Your content', ['The lists, recipes, prices and quotes you create are yours. You only allow us to store them and show them to you and to the people you invite, as needed for the app to work.']),
   ('6. Prices and quotes (Preço Certo)', ['The calculations use the values you enter and are an aid for deciding. Check prices, margins and quotes before using them with customers. The app is not accounting, tax or legal advice.']),
   ('7. Availability and changes', ['The apps are provided "as is", with no guarantee of uninterrupted operation. We may fix, change, suspend or discontinue features. Relevant changes are announced in News.']),
   ('8. Limitation of liability', ['To the extent permitted by law, FLR Sistemas is not liable for lost profits, indirect damages, or data loss caused by clearing the device or browser, misuse or unavailability. Nothing here limits rights that the law does not allow to be limited, such as consumer rights.']),
   ('9. Termination', ['You can stop using the apps at any time and ask for your account and data to be deleted by writing to the e-mail below. We may suspend accounts that violate these terms.']),
   ('10. Intellectual property', ['The name, logos and code of the apps belong to FLR Sistemas. These terms do not transfer those rights.']),
   ('11. Privacy', ['How we handle your data is described in each app\'s <a href="/en/privacy/">privacy policy</a>.']),
   ('12. Changes to these terms', ['When we change these terms, we publish the new version on this page, with the update date.']),
   ('13. Governing law', ['The laws of Brazil apply. In consumer relations, the courts of the consumer\'s home apply.']),
   ('14. Contact', ['Questions about these terms: <a href="mailto:%s">%s</a>.' % (EMAIL, EMAIL)]),
  ]),
 'es': dict(
  title='Términos de Uso', desc='Términos de Uso de las apps Preço Certo y Lista de Compras, de FLR Sistemas.',
  updated='Última actualización: 23 de noviembre de 2026',
  intro='Estos términos valen para las apps <strong>Preço Certo</strong> y <strong>Lista de Compras</strong>, de FLR Sistemas, y para este sitio. Son breves a propósito.',
  sections=[
   ('1. Aceptación', ['Al descargar o usar las apps, aceptas estos términos. Si no estás de acuerdo, no uses las apps.']),
   ('2. Las apps', ['<strong>Preço Certo:</strong> app Android que calcula el costo y el precio de venta de recetas y genera presupuesto y ficha de cocina en PDF. Funciona en tu celular, sin cuenta.',
                    '<strong>Lista de Compras:</strong> app web (PWA) para crear y compartir listas de compras. La cuenta es opcional: puedes usarla sin cuenta, con las listas solo en el dispositivo.']),
   ('3. Uso permitido', ['Usa las apps con fines personales o profesionales lícitos. No intentes eludir la seguridad, acceder a datos de otras personas, sobrecargar el servicio ni usar las apps para algo ilegal o para perjudicar a alguien.']),
   ('4. Cuenta y compartir (Lista de Compras)', ['Eres responsable de la contraseña y del correo de tu cuenta. Al invitar a alguien a una lista, esa persona verá los artículos, los precios y el nombre y el correo de los participantes. El dueño de la lista puede quitar participantes y eliminar la lista.',
                    'En el modo sin cuenta, las listas quedan solo en este dispositivo y en este navegador, sin copia de seguridad. Borrar los datos del navegador, o desinstalar la app, lo elimina todo, sin forma de recuperarlo.']),
   ('5. Tu contenido', ['Las listas, recetas, precios y presupuestos que creas son tuyos. Solo nos autorizas a guardarlos y mostrarlos a ti y a quienes invites, lo necesario para que la app funcione.']),
   ('6. Valores y presupuestos (Preço Certo)', ['Los cálculos usan los valores que ingresas y son una ayuda para decidir. Revisa precios, márgenes y presupuestos antes de usarlos con clientes. La app no es asesoría contable, fiscal ni jurídica.']),
   ('7. Disponibilidad y cambios', ['Las apps se ofrecen "tal como están", sin garantía de funcionamiento ininterrumpido. Podemos corregir, cambiar, suspender o terminar funciones. Los cambios relevantes se anuncian en Novedades.']),
   ('8. Limitación de responsabilidad', ['En la medida permitida por la ley, FLR Sistemas no responde por lucro cesante, daños indirectos ni por pérdida de datos causada por limpiar el dispositivo o el navegador, uso indebido o indisponibilidad. Nada aquí limita derechos que la ley no permite limitar, como los del consumidor.']),
   ('9. Terminación', ['Puedes dejar de usar las apps cuando quieras y pedir la eliminación de tu cuenta y tus datos escribiendo al correo de abajo. Podemos suspender cuentas que infrinjan estos términos.']),
   ('10. Propiedad intelectual', ['El nombre, los logotipos y el código de las apps pertenecen a FLR Sistemas. Estos términos no transfieren esos derechos.']),
   ('11. Privacidad', ['El tratamiento de tus datos se describe en la <a href="/es/privacidad/">política de privacidad</a> de cada app.']),
   ('12. Cambios en estos términos', ['Cuando cambiemos estos términos, publicaremos la nueva versión en esta página, con la fecha de actualización.']),
   ('13. Ley aplicable', ['Rigen las leyes de Brasil. En las relaciones de consumo, rige el fuero del domicilio del consumidor.']),
   ('14. Contacto', ['Dudas sobre estos términos: <a href="mailto:%s">%s</a>.' % (EMAIL, EMAIL)]),
  ]),
}


def terms_body(lang):
    t = TERMS[lang]
    out = ['\n  <h1 class="page">%s</h1>\n  <p class="updated">%s</p>\n  <p class="intro">%s</p>\n\n  <div class="doc">\n' % (t['title'], t['updated'], t['intro'])]
    for h, paras in t['sections']:
        out.append('    <h3>%s</h3>\n' % h)
        for p in paras:
            out.append('    <p>%s</p>\n' % p)
    out.append('  </div>\n')
    return ''.join(out)
