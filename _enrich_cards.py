# -*- coding: utf-8 -*-
"""Enrich card data: load capacity (family img alt), material (from title), url-encoded photo."""
import os, io, re, json

DOCS = r'C:\Users\User\Documents\GitHub\tanko-website-1-\docs'
DATA = r'C:\Users\User\Documents\GitHub\tanko-website-1-\_cards_data.json'
cards = json.load(io.open(DATA, encoding='utf-8'))

def clean(s):
    return s.replace('\u00e2\u20ac\u201c', '-').replace('\u00c2\u00b7', '\u00b7').replace('\u00e2\u20ac\u02dc', "'").replace('\u00c3\u00a2\u00e2\u20ac\u0161\u00c2\u00ac\u00e2\u20ac\u0153', '-')

for c in cards:
    fam = c['fam']
    fp = os.path.join(DOCS, c['cat'], fam, 'index.html')
    t = io.open(fp, encoding='utf-8').read()
    # load: family alt "2000kg load capacity" or any kg
    lm = re.search(r'(\d{2,4})\s*kg', t, re.I)
    c['loadcap'] = c['loadcap'] or (lm.group(1) + ' kg' if lm else '')
    # material from title/vname
    src = (c['title'] + ' ' + c['vname']).lower()
    if 'stainless' in src:
        mat = 'Stainless Steel'
    elif 'steel top' in src or 'steel-top' in src:
        mat = 'Steel Top'
    elif 'steel' in src:
        mat = 'Steel'
    elif 'plastic' in src:
        mat = 'Plastic'
    else:
        mat = 'Steel'
    c['material'] = mat
    # series display name: leading token of sku (e.g., WA, WD, MB, KPQ) for big title
    skus = c['skus']
    if skus:
        first = re.match(r'^([A-Z]{1,4})', skus[0].split(' ')[0])
        c['series_code'] = first.group(1) if first else fam.upper()
    else:
        c['series_code'] = fam.upper()
    # cap model range display
    c['model_range'] = ' \u00b7 '.join(skus[:6]) + (' \u00b7 +%d more' % (len(skus)-6) if len(skus) > 6 else '')
    # clean title
    c['title_clean'] = clean(c['title'])
    if not c['photo']:
        c['photo'] = ''

json.dump(cards, io.open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
ok = [c for c in cards if c['photo']]
print('total:', len(cards), '| with photo:', len(ok), '| with load:', sum(1 for c in cards if c['loadcap']))
for c in cards[:6]:
    print(' -', c['fam'], '|', c['series_code'], '|', c['title_clean'][:40], '| load:', c['loadcap'], '| mat:', c['material'])
