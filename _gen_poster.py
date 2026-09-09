# -*- coding: utf-8 -*-
"""Generate 4 big catalogue posters (2160x2160) with all product series in ascending order."""
import os, io, json, re, urllib.parse

DOCS = r'C:\Users\User\Documents\GitHub\tanko-website-1-\docs'
DATA = r'C:\Users\User\Documents\GitHub\tanko-website-1-\_cards_data.json'
OUT = r'C:\Users\User\Doubao\chats\2026-09-01\new-chat\catalogue-cards\posters'
LOGO = os.path.join(DOCS, 'assets', 'tanko-logo-white.svg').replace('\\', '/')

cards = [c for c in json.load(io.open(DATA, encoding='utf-8')) if c.get('photo')]

def sku_key(c):
    skus = c.get('skus') or []
    first = skus[0] if skus else c['fam'].upper()
    m = re.match(r'^([A-Z]{1,4})[- ]?(\d{0,4})', first)
    return (m.group(1) if m else c['fam'].upper(), int(m.group(2)) if m and m.group(2) else 999, c['fam'])

cards.sort(key=sku_key)
N = 4
chunks = [cards[i::N] for i in range(N)]  # ascending interleave
# better: contiguous chunks
chunks = [cards[i*28:(i+1)*28] for i in range(N)]
chunks = [ch for ch in chunks if ch]

def photo_url(rel):
    p = os.path.join(DOCS, rel.lstrip('/'))
    if not os.path.exists(p):
        return None
    return 'file:///' + urllib.parse.quote(p.replace('\\', '/'), safe='/:() +')

def sub_title(c):
    t = c.get('title_clean') or c['title']
    t = t.split('(')[0].strip().rstrip('-').strip()
    t = re.sub(r'\s*[—-]\s*$', '', t)
    return t[:60]

POSTER = """<!doctype html><html><head><meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:2160px; height:2160px; overflow:hidden; }
  body {
    font-family:'Segoe UI', Arial, sans-serif;
    background:
      radial-gradient(1400px 800px at 50% -8%, rgba(64,84,140,.30), transparent 60%),
      radial-gradient(1000px 700px at 108% 106%, rgba(255,102,0,.10), transparent 55%),
      linear-gradient(160deg,#0e1014 0%, #151922 55%, #0d0f13 100%);
    color:#f2f4f8; display:flex; flex-direction:column; padding:52px 56px 40px;
  }
  .head { display:flex; align-items:center; justify-content:space-between; padding-bottom:30px; border-bottom:1px solid rgba(255,255,255,.12); }
  .brand { display:flex; align-items:center; gap:20px; }
  .brand img { height:64px; }
  .brand .word { font-size:40px; font-weight:800; letter-spacing:6px; }
  .head .right { text-align:right; }
  .head .t { font-size:30px; font-weight:700; letter-spacing:3px; color:#ffb066; }
  .head .n { font-size:20px; color:#8f9ab0; letter-spacing:2px; margin-top:4px; }
  .grid { flex:1; display:grid; grid-template-columns:repeat(6,1fr); grid-auto-rows:1fr; gap:16px; padding:34px 0 26px; }
  .cell { background:rgba(255,255,255,.035); border:1px solid rgba(255,255,255,.08); border-radius:18px; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:12px 10px 14px; overflow:hidden; }
  .cell .ph { flex:1; width:100%; display:flex; align-items:center; justify-content:center; min-height:0; }
  .cell .ph img { max-width:88%; max-height:100%; object-fit:contain; }
  .cell .code { margin-top:10px; font-size:27px; font-weight:800; letter-spacing:1px; color:#fff; text-align:center; }
  .cell .sub { margin-top:3px; font-size:17px; color:#93a0b8; text-align:center; line-height:1.15; max-height:2.4em; overflow:hidden; }
  .foot { border-top:1px solid rgba(255,255,255,.12); padding-top:26px; text-align:center; }
  .foot .co { font-size:30px; font-weight:700; letter-spacing:2px; }
  .foot .dist { font-size:20px; letter-spacing:2px; color:#9aa6bd; margin-top:4px; }
  .foot .cta { margin-top:10px; font-size:26px; color:#ffb066; font-weight:700; letter-spacing:1px; }
</style></head><body>
  <div class="head">
    <div class="brand"><img src="file:///{LOGO}" alt="Tanko"><div class="word">TANKO</div></div>
    <div class="right"><div class="t">INDUSTRIAL STORAGE &amp; WORKBENCH SYSTEMS</div><div class="n">{RANGE} &middot; POSTER {N} OF {TOT}</div></div>
  </div>
  <div class="grid">{CELLS}</div>
  <div class="foot">
    <div class="co">PRIMAXS MARKETING (M) SDN BHD</div>
    <div class="dist">EXCLUSIVE MALAYSIA DISTRIBUTOR OF TANKO</div>
    <div class="cta">www.storagesystem.com.my &nbsp;&middot;&nbsp; WhatsApp +6012-616-3088</div>
  </div>
</body></html>"""

def cell_html(c):
    ph = photo_url(c['photo'])
    if not ph:
        return ''
    code = (c.get('series_code') or 'TANKO').upper()
    label = c['fam'].upper().replace('_', '-')
    return ('<div class="cell"><div class="ph"><img src="%s" alt="%s"></div>'
            '<div class="code">%s</div><div class="sub">%s</div></div>') % (
        ph, label, label, sub_title(c))

os.makedirs(OUT, exist_ok=True)
html_dir = os.path.join(OUT, 'html')
os.makedirs(html_dir, exist_ok=True)

for idx, chunk in enumerate(chunks, 1):
    first = chunk[0]['fam'].upper().replace('_', '-')
    last = chunk[-1]['fam'].upper().replace('_', '-')
    cells = ''.join(cell_html(c) for c in chunk)
    html = POSTER.replace('{LOGO}', LOGO).replace('{RANGE}', first + ' \u2013 ' + last) \
        .replace('{N}', str(idx)).replace('{TOT}', str(len(chunks))).replace('{CELLS}', cells)
    hp = os.path.join(html_dir, 'poster-%d.html' % idx)
    io.open(hp, 'w', encoding='utf-8').write(html)
    print('poster %d: %s (%d series: %s..%s)' % (idx, hp, len(chunk), first, last))
