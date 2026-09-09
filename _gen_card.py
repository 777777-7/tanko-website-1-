# -*- coding: utf-8 -*-
"""Generate dark premium 1080x1080 catalogue cards (HTML) for a set of series."""
import os, io, json, re, sys, urllib.parse

DOCS = r'C:\Users\User\Documents\GitHub\tanko-website-1-\docs'
DATA = r'C:\Users\User\Documents\GitHub\tanko-website-1-\_cards_data.json'
OUT = r'C:\Users\User\Doubao\chats\2026-09-01\new-chat\catalogue-cards'
LOGO = os.path.join(DOCS, 'assets', 'tanko-logo-white.svg')

cards = json.load(io.open(DATA, encoding='utf-8'))
byfam = {c['fam']: c for c in cards}

def photo_url(rel):
    p = os.path.join(DOCS, rel.lstrip('/'))
    if not os.path.exists(p):
        return None
    return 'file:///' + urllib.parse.quote(p.replace('\\', '/'), safe='/:() +')

TMPL = """<!doctype html><html><head><meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1080px; height:1080px; overflow:hidden; }
  body {
    font-family:'Segoe UI', Arial, sans-serif;
    background:
      radial-gradient(1200px 700px at 50% -10%, rgba(64,84,140,.28), transparent 60%),
      radial-gradient(900px 600px at 108% 108%, rgba(255,102,0,.10), transparent 55%),
      linear-gradient(160deg,#0e1014 0%, #151922 55%, #0d0f13 100%);
    color:#f2f4f8; display:flex; flex-direction:column; position:relative;
  }
  .top { display:flex; align-items:center; justify-content:space-between; padding:44px 54px 0; }
  .brand { display:flex; align-items:center; gap:16px; }
  .brand img { height:52px; }
  .brand .word { font-size:30px; font-weight:800; letter-spacing:6px; color:#fff; }
  .chip { border:1px solid rgba(255,255,255,.22); border-radius:999px; padding:10px 22px; font-size:17px; letter-spacing:3px; color:#cfd6e4; }
  .stage { flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:18px 60px 0; }
  .photo { max-width:660px; max-height:470px; display:flex; align-items:center; justify-content:center; }
  .photo img { max-width:660px; max-height:470px; object-fit:contain; filter:drop-shadow(0 22px 44px rgba(0,0,0,.55)); }
  .dims { margin-top:26px; background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.14); border-radius:12px; padding:12px 26px; font-size:26px; font-weight:700; letter-spacing:1px; color:#ffb066; }
  .name { margin-top:20px; font-size:64px; font-weight:800; letter-spacing:10px; text-align:center; line-height:1.05; }
  .sub { margin-top:8px; font-size:27px; font-weight:600; color:#b9c2d4; text-align:center; letter-spacing:1px; }
  .models { margin-top:14px; font-size:19px; color:#8f9ab0; text-align:center; letter-spacing:1px; max-width:900px; }
  .specs { margin-top:20px; display:flex; gap:14px; }
  .spec { border:1px solid rgba(255,255,255,.18); border-radius:10px; padding:10px 22px; font-size:19px; color:#e8ecf4; }
  .spec b { color:#ffb066; font-size:21px; }
  .tw { margin-top:18px; font-size:16px; letter-spacing:4px; color:#77839b; }
  .foot { border-top:1px solid rgba(255,255,255,.10); padding:26px 54px 34px; text-align:center; background:rgba(0,0,0,.25); }
  .foot .co { font-size:22px; font-weight:700; letter-spacing:2px; color:#fff; }
  .foot .dist { font-size:16px; letter-spacing:2px; color:#9aa6bd; margin-top:4px; }
  .foot .cta { margin-top:12px; font-size:20px; color:#ffb066; font-weight:700; letter-spacing:1px; }
</style></head><body>
  <div class="top">
    <div class="brand"><img src="file:///{LOGO}" alt="Tanko"><div class="word">TANKO</div></div>
    <div class="chip">EST. 1975 &middot; MADE IN TAIWAN</div>
  </div>
  <div class="stage">
    <div class="photo"><img src="{PHOTO}" alt="{ALT}"></div>
    {DIMS}
    <div class="name">{CODE} SERIES</div>
    <div class="sub">{SUB}</div>
    <div class="models">{MODELS}</div>
    <div class="specs">
      <div class="spec">LOAD CAPACITY &nbsp;<b>{LOAD}</b></div>
      <div class="spec">MATERIAL &nbsp;<b>{MAT}</b></div>
    </div>
    <div class="tw">TANKO &middot; INDUSTRIAL STORAGE SOLUTIONS</div>
  </div>
  <div class="foot">
    <div class="co">PRIMAXS MARKETING (M) SDN BHD</div>
    <div class="dist">EXCLUSIVE MALAYSIA DISTRIBUTOR OF TANKO</div>
    <div class="cta">www.storagesystem.com.my &nbsp;&middot;&nbsp; WhatsApp +6012-616-3088</div>
  </div>
</body></html>"""

def build(c, outdir):
    ph = photo_url(c['photo'])
    if not ph:
        return None
    dims = c['dims']
    dims_html = '<div class="dims">%s</div>' % dims if dims else ''
    sub = re.sub(r'\s*\([^)]*\)$', '', c['title_clean'])
    sub = sub.replace('â€”', '-').replace('\u2014', '-').strip()
    html = TMPL.replace('{LOGO}', LOGO.replace('\\', '/')).replace('{PHOTO}', ph) \
        .replace('{ALT}', (c['title_clean'] + ' ' + c['fam']).upper()) \
        .replace('{DIMS}', dims_html) \
        .replace('{CODE}', (c['series_code'] or 'TANKO').upper()) \
        .replace('{SUB}', sub) \
        .replace('{MODELS}', c['model_range'] or '') \
        .replace('{LOAD}', c['loadcap'] or 'On Request') \
        .replace('{MAT}', c['material'] or 'Steel')
    os.makedirs(outdir, exist_ok=True)
    hp = os.path.join(outdir, c['fam'] + '.html')
    io.open(hp, 'w', encoding='utf-8').write(html)
    return hp

if __name__ == '__main__':
    fams = sys.argv[1].split(',') if len(sys.argv) > 1 else ['wa-57']
    od = os.path.join(OUT, 'html')
    for f in fams:
        c = byfam.get(f)
        if not c:
            print('MISS', f); continue
        hp = build(c, od)
        print('BUILT', f, '->', hp)
