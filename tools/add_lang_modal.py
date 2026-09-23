# -*- coding: utf-8 -*-
"""Add a one-time language chooser to the homepages.

Deliberately NOT a full-screen blocker: Google penalises intrusive interstitials
on mobile, which would undercut the SEO work this supports. It is a compact
dialog, dismissible by button, backdrop click or Escape, and it appears once per
visitor - the choice is remembered in localStorage.

Injected only on / and /zh/. Idempotent.

Run:  python tools/add_lang_modal.py [--dry]
"""
import io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
MARKER = 'id="lang-modal"'

HOMEPAGES = [
    (os.path.join(DOCS, 'index.html'), 'en-MY'),
    (os.path.join(DOCS, 'zh', 'index.html'), 'zh-Hans-MY'),
    (os.path.join(DOCS, 'ms', 'index.html'), 'ms-MY'),
]

COPY = {
    'en-MY': dict(
        title='Choose your language',
        sub='You can change this any time from the menu.',
        close='Close language chooser',
    ),
    'ms-MY': dict(
        title='Pilih bahasa anda',
        sub='Anda boleh menukarnya bila-bila masa dari menu.',
        close='Tutup pemilih bahasa',
    ),
    'zh-Hans-MY': dict(
        title='选择语言',
        sub='之后可随时在菜单中更改。',
        close='关闭语言选择',
    ),
}

OPTIONS = [
    ('/',    'en-MY',      'English',              'EN'),
    ('/ms/', 'ms-MY',      'Bahasa Malaysia',      'BM'),
    ('/zh/', 'zh-Hans-MY', '中文',         '中文'),
]

SNIPPET = """
<div id="lang-modal" hidden>
  <div class="lang-modal__backdrop" data-lang-dismiss></div>
  <div class="lang-modal__card" role="dialog" aria-modal="true" aria-labelledby="lang-modal-title">
    <h2 id="lang-modal-title">%(title)s</h2>
    <p>%(sub)s</p>
    <div class="lang-modal__opts">
%(opts)s
    </div>
    <button type="button" class="lang-modal__x" data-lang-dismiss aria-label="%(close)s">&times;</button>
  </div>
</div>
<script>
(function(){
  var KEY='primaxs-lang';
  var el=document.getElementById('lang-modal');
  if(!el) return;
  var store=null;
  try{ store=window.localStorage; }catch(e){}
  var seen=null;
  try{ seen=store&&store.getItem(KEY); }catch(e){}
  if(seen) return;                       // already chose once - never nag again
  el.hidden=false;
  document.documentElement.classList.add('lang-modal-open');
  function remember(v){ try{ store&&store.setItem(KEY,v||'dismissed'); }catch(e){} }
  function close(){
    el.hidden=true;
    document.documentElement.classList.remove('lang-modal-open');
    remember('dismissed');
  }
  el.addEventListener('click',function(ev){
    var a=ev.target.closest('[data-lang-go]');
    if(a){ remember(a.getAttribute('data-lang-go')); return; }
    if(ev.target.closest('[data-lang-dismiss]')) close();
  });
  document.addEventListener('keydown',function(ev){ if(ev.key==='Escape') close(); });
})();
</script>
"""

CSS = """
/* ---- one-time language chooser (homepage only) ---- */
#lang-modal[hidden]{display:none}
#lang-modal{position:fixed;inset:0;z-index:9998;display:flex;align-items:center;justify-content:center;padding:16px}
.lang-modal__backdrop{position:absolute;inset:0;background:rgba(10,13,19,.55)}
.lang-modal__card{position:relative;background:#fff;color:#0a0d13;border-radius:10px;
  padding:28px 28px 24px;max-width:380px;width:100%;box-shadow:0 12px 40px rgba(0,0,0,.28);text-align:center}
.lang-modal__card h2{margin:0 0 .35rem;font-size:1.15rem;line-height:1.3}
.lang-modal__card p{margin:0 0 1.1rem;font-size:.86rem;opacity:.72}
.lang-modal__opts{display:flex;flex-direction:column;gap:.5rem}
.lang-modal__opts a{display:block;padding:.7rem 1rem;border:1px solid #d7dbe0;border-radius:6px;
  text-decoration:none;color:inherit;font-weight:600;transition:border-color .15s,background .15s}
.lang-modal__opts a:hover,.lang-modal__opts a:focus{border-color:#c8102e;background:#faf3f4}
.lang-modal__x{position:absolute;top:8px;right:10px;background:none;border:0;font-size:1.5rem;
  line-height:1;cursor:pointer;color:#8b9099;padding:4px 8px}
.lang-modal__x:hover{color:#0a0d13}
html.lang-modal-open{overflow:hidden}
@media (prefers-reduced-motion:reduce){.lang-modal__opts a{transition:none}}
"""


def build(lang):
    c = COPY[lang]
    opts = []
    for href, code, full, short in OPTIONS:
        cur = ' aria-current="true"' if code == lang else ''
        opts.append('      <a href="%s" hreflang="%s" data-lang-go="%s"%s>%s</a>'
                    % (href, code, code, cur, full))
    return SNIPPET % dict(title=c['title'], sub=c['sub'], close=c['close'],
                          opts='\n'.join(opts))


def main(dry=False):
    for path, lang in HOMEPAGES:
        if not os.path.exists(path):
            print('   missing   %s' % path)
            continue
        with io.open(path, encoding='utf-8') as fh:
            html = fh.read()
        if MARKER in html:
            print('   already   %s' % os.path.relpath(path, ROOT))
            continue
        i = html.rfind('</body>')
        if i < 0:
            print('   no-body   %s' % os.path.relpath(path, ROOT))
            continue
        html = html[:i] + build(lang) + html[i:]
        if not dry:
            with io.open(path, 'w', encoding='utf-8', newline='') as fh:
                fh.write(html)
        print('   added     %s' % os.path.relpath(path, ROOT))

    css_path = os.path.join(DOCS, 'assets', 'css', 'site.css')
    with io.open(css_path, encoding='utf-8') as fh:
        css = fh.read()
    if 'lang-modal__card' in css:
        print('   already   site.css')
    elif not dry:
        with io.open(css_path, 'a', encoding='utf-8', newline='') as fh:
            fh.write(CSS)
        print('   added     site.css')


if __name__ == '__main__':
    main('--dry' in sys.argv)
