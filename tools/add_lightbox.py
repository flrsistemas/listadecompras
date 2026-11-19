import os, re

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import APP, SITE, PC_DOCS as PC, WORK as S

LABELS = {
    'pt': ('Fechar', 'Anterior', 'Próxima', 'Imagem ampliada'),
    'en': ('Close', 'Previous', 'Next', 'Enlarged image'),
    'es': ('Cerrar', 'Anterior', 'Siguiente', 'Imagen ampliada'),
}

SNIPPET = r'''
<!-- Lightbox: clique na imagem para ampliar -->
<style>
  .shots img, .thumb img { cursor: zoom-in; }
  .shots img:focus-visible, .thumb img:focus-visible { outline: 2px solid var(--muted, #888); outline-offset: 3px; }
  .lb { position: fixed; inset: 0; z-index: 1000; display: none; flex-direction: column; align-items: center; justify-content: center;
    padding: 16px; background: rgba(0, 0, 0, .9); }
  .lb.open { display: flex; }
  .lb img { max-width: min(94vw, 760px); max-height: 80vh; width: auto; height: auto; border-radius: 14px; background: #fff; }
  .lb p { color: #f2f2f2; margin: 12px 0 0; max-width: 92vw; text-align: center; font-size: .95rem; }
  .lb button { position: absolute; width: 46px; height: 46px; border: 0; border-radius: 999px; cursor: pointer;
    background: rgba(255, 255, 255, .16); color: #fff; font-size: 24px; line-height: 1; }
  .lb button:hover, .lb button:focus-visible { background: rgba(255, 255, 255, .3); }
  .lb .x { top: 14px; right: 14px; }
  .lb .prev { left: 12px; top: 50%; transform: translateY(-50%); }
  .lb .next { right: 12px; top: 50%; transform: translateY(-50%); }
  .lb.single .prev, .lb.single .next { display: none; }
  body.lb-open { overflow: hidden; }
</style>
<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="@@LABEL@@" hidden>
  <button class="x" type="button" aria-label="@@CLOSE@@">&times;</button>
  <button class="prev" type="button" aria-label="@@PREV@@">&#8249;</button>
  <img id="lb-img" alt="">
  <p id="lb-cap"></p>
  <button class="next" type="button" aria-label="@@NEXT@@">&#8250;</button>
</div>
<script>
(function () {
  var lb = document.getElementById('lb'); if (!lb) return;
  var big = document.getElementById('lb-img'), cap = document.getElementById('lb-cap');
  var imgs = Array.prototype.slice.call(document.querySelectorAll('.shots img, .thumb img'));
  var group = [], pos = 0, last = null;
  imgs.forEach(function (im) {
    im.setAttribute('tabindex', '0'); im.setAttribute('role', 'button');
    im.addEventListener('click', function () { open(im); });
    im.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(im); } });
  });
  function box(im) { return im.closest('.shots') || im.closest('.apps') || document; }
  function caption(im) { var f = im.closest('figure'); var c = f && f.querySelector('figcaption'); return (c && c.textContent.trim()) || im.alt || ''; }
  function show() { var im = group[pos]; big.src = im.currentSrc || im.src; big.alt = im.alt; cap.textContent = caption(im); lb.classList.toggle('single', group.length < 2); }
  function open(im) {
    var b = box(im); group = imgs.filter(function (x) { return box(x) === b; }); pos = group.indexOf(im);
    last = document.activeElement; show(); lb.hidden = false; lb.classList.add('open'); document.body.classList.add('lb-open');
    lb.querySelector('.x').focus();
  }
  function close() { lb.classList.remove('open'); lb.hidden = true; document.body.classList.remove('lb-open'); big.removeAttribute('src'); if (last) last.focus(); }
  function step(d) { if (group.length < 2) return; pos = (pos + d + group.length) % group.length; show(); }
  lb.querySelector('.x').addEventListener('click', close);
  lb.querySelector('.prev').addEventListener('click', function (e) { e.stopPropagation(); step(-1); });
  lb.querySelector('.next').addEventListener('click', function (e) { e.stopPropagation(); step(1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') close(); else if (e.key === 'ArrowLeft') step(-1); else if (e.key === 'ArrowRight') step(1);
  });
  var x0 = null;
  lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; x0 = null; if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1); });
})();
</script>
'''


def snippet(lang):
    lab, close, prev, nxt = None, None, None, None
    c, p, n, l = LABELS[lang]
    return SNIPPET.replace('@@LABEL@@', l).replace('@@CLOSE@@', c).replace('@@PREV@@', p).replace('@@NEXT@@', n)


def lang_of(html):
    m = re.search(r'<html lang="([a-zA-Z-]+)"', html)
    code = (m.group(1) if m else 'pt')[:2].lower()
    return code if code in LABELS else 'pt'


targets = [
    os.path.join(APP, 'sobre', 'index.html'), os.path.join(APP, 'sobre', 'en', 'index.html'), os.path.join(APP, 'sobre', 'es', 'index.html'),
    os.path.join(PC, 'index.html'), os.path.join(PC, 'en', 'index.html'), os.path.join(PC, 'es', 'index.html'),
    os.path.join(SITE, 'index.html'), os.path.join(SITE, 'en', 'index.html'), os.path.join(SITE, 'es', 'index.html'),
]
for p in targets:
    t = open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in t else '\n'
    t = t.replace('\r\n', '\n')
    t = re.sub(r'\n<!-- Lightbox: clique na imagem para ampliar -->.*?</script>\n(?=</body>)', '\n', t, flags=re.S)  # idempotente
    assert '</body>' in t, p
    t = t.replace('</body>', snippet(lang_of(t)).lstrip('\n') + '</body>', 1)
    open(p, 'w', encoding='utf-8', newline='').write(t.replace('\n', nl))
    print('ok', os.path.relpath(p, S if SITE in p or PC in p else APP), lang_of(t))
