# -*- coding: utf-8 -*-
"""Build a Google Merchant Center TSV feed from the Product JSON-LD already on
every product page. No new data is invented -- it is an export, not a rewrite."""
import os, re, json, csv, html

# Real spec data, keyed by SKU -- used to build honest descriptions instead of
# reusing the truncated ones baked into the page schema.
SPECS = {}
for _p in json.load(open('products.json', encoding='utf-8')):
    SPECS[_p['sku']] = _p

TAIL = ('Supplied in Malaysia by Primaxs Marketing (M) Sdn Bhd, the exclusive Tanko '
        'distributor since 2006. Stock held in Selangor, quoted in Ringgit. FREE '
        'delivery and installation in Selangor and the Klang Valley; outstation '
        'delivery quoted separately and itemised. 1-year warranty against '
        'manufacturing defects, administered from our Selangor office -- nothing '
        'ships back to Taiwan.')

def build_desc(sku, name, cat):
    sp = SPECS.get(sku, {})
    bits = []
    lead = name if (name and sku in name) else ('%s (%s)' % (name, sku) if name else sku)
    bits.append(lead.rstrip('. ') + '.')
    facts = []
    if sp.get('dimensions'):
        facts.append('Dimensions %s' % sp['dimensions'].strip(' |,;').replace('|', ','))
    if sp.get('material'):
        facts.append('Material: %s' % sp['material'])
    if sp.get('load_capacity'):
        facts.append('Load capacity %s' % sp['load_capacity'])
    if sp.get('color'):
        facts.append('Colour %s' % sp['color'])
    if facts:
        bits.append('. '.join(facts) + '.')
    if cat:
        bits.append('Part of the Tanko %s range.'
                    % (cat if cat.isupper() or 'CNC' in cat or 'ESD' in cat else cat.lower()))
    bits.append(TAIL)
    return ' '.join(bits)


ROOT = 'docs'
OUT = 'marketing/google-merchant-feed.tsv'

# Google product category IDs (taxonomy 2021) mapped from our own categories.
GPC = {
    'Workbenches': '503739',
    'Workbench': '503739',            # Business & Industrial > Work Benches
    'Tool Cabinets': '4207',
    'Tool Cabinet': '4207',           # Hardware > Tool Storage & Organization > Tool Cabinets
    'CNC Tool Storage': '4207',
    'Parts Cabinets': '4207',
    'Parts Cabinet': '4207',
    'Perforated Boards': '4210',
    'Perforated Board': '4210',       # Tool Organizer Racks & Holders
    'Hanger Racks': '4210',
    'Hanger Rack': '4210',
    'Modular Workstations': '503739',
    'Modular Workstation': '503739',
    'Lockers': '4163',
    'Locker': '4163',                 # Business & Industrial > Storage > Lockers
    'Racks': '5197',
    'Rack': '5197',                   # Business & Industrial > Storage > Shelving
    'Documents Cabinets': '448',
    'Documents Cabinet': '448',       # Office Furniture > File Cabinets
    'Household Items': '6356',
}

def products_in(path):
    s = open(path, encoding='utf-8').read()
    found = []
    def walk(n):
        if isinstance(n, dict):
            if n.get('@type') == 'Product':
                found.append(n)
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            walk(json.loads(m.group(1)))
        except Exception:
            pass
    return found

def clean(t, limit):
    if not t:
        return ''
    t = html.unescape(str(t))
    t = t.replace('�', '-')           # mojibake dashes from the source data
    t = re.sub(r'\s+', ' ', t).strip()
    t = t.rstrip(' -,')
    return t[:limit]

rows = []
no_price = no_image = 0

# Pass 1: collect every Product node on the site, keyed by SKU. A SKU appears
# twice -- the full node on its own page, and a slim inlined variant on the
# family page which carries no category or description. Keep the richest.
best = {}
for dirpath, _d, files in os.walk(ROOT):
    if 'index.html' not in files:
        continue
    for node in products_in(os.path.join(dirpath, 'index.html')):
        sku = (node.get('sku') or '').strip()
        if not sku:
            continue
        prev = best.get(sku)
        if prev is None or len(node) > len(prev):
            best[sku] = node

# Pass 2: build a row per SKU
for sku, p in best.items():
    offers = p.get('offers') or {}
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    price = offers.get('price')
    link = offers.get('url') or p.get('@id', '').split('#')[0]
    imgs = p.get('image') or []
    if isinstance(imgs, str):
        imgs = [imgs]

    if not link:
        continue
    if not price:
        no_price += 1
        continue
    if not imgs:
        no_image += 1
        continue

    cat = p.get('category') or ''
    gpc = GPC.get(cat) or GPC.get(cat[:-1] if cat.endswith('s') else cat) or ''
    name = clean(p.get('name') or sku, 150)
    desc = clean(build_desc(sku, name, cat), 4000)

    rows.append({
        'id': sku,
        'title': name,
        'description': desc,
        'link': link,
        'image_link': imgs[0],
        'additional_image_link': ','.join(imgs[1:11]) if len(imgs) > 1 else '',
        'availability': 'in_stock',
        'price': '%s MYR' % str(price).replace(',', ''),
        'condition': 'new',
        'brand': 'Tanko',
        'mpn': sku,
        'identifier_exists': 'no',
        'google_product_category': gpc,
        'product_type': cat,
        'shipping': 'MY::Selangor and Klang Valley:0 MYR',
        'shipping_label': 'bulky',
    })

cols = ['id', 'title', 'description', 'link', 'image_link', 'additional_image_link',
        'availability', 'price', 'condition', 'brand', 'mpn', 'identifier_exists',
        'google_product_category', 'product_type', 'shipping', 'shipping_label']

with open(OUT, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter='\t', extrasaction='ignore')
    w.writeheader()
    for r in sorted(rows, key=lambda r: r['id']):
        w.writerow(r)

print('feed rows: %d' % len(rows))
print('skipped -- no price: %d, no image: %d' % (no_price, no_image))
print('written to %s' % OUT)
