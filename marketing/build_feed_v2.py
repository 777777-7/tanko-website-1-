# -*- coding: utf-8 -*-
"""Build docs/merchant-feed.xml from the product pages themselves.

WHY THIS REPLACES THE OLD ONE. There were two feeds and both were half broken.

  _merchant_feed.py -> docs/merchant-feed.xml   (the one actually deployed)
      Took g:description from the page's <meta name="description">, which is
      capped near 155 characters for SEO. Result: all 1,517 descriptions were
      EXACTLY 158 characters and 1,468 of them ended mid-word --
      "...exclusive Tanko distributor. Request a quot". It also carried none of
      mpn, google_product_category, additional_image_link or shipping, and
      emitted product_type as slug case: "Cnc-tool > Ea-10mn".

  marketing/build_merchant_feed.py -> google-merchant-feed.tsv  (never deployed)
      Good descriptions (442-634 chars, none truncated) and the full attribute
      set, but every image URL was wrong: it pointed at /asset3/<SKU>.jpg and
      /asset_content/<range>/<shot>.jpg, which do not exist -- those folders
      hold .webp. 1,590 of 1,591 main images and 1,504 additional images were
      dead links.

This build reads each product page, which is now the single source of truth: the
spec list carries load capacity and material, and og:image points at a real
1200x1200 JPEG in /feed-img/ (fixed 12 Sep). Nothing is invented; every value
either comes off the page or is a constant commercial term that applies to all
items.
"""
import os
import re
import csv
import json
import html
import sys

ROOT = 'docs'
OUT = os.path.join(ROOT, 'merchant-feed.xml')
BASE = 'https://www.storagesystem.com.my'
APPLY = '--apply' in sys.argv

TAIL = ('Supplied in Malaysia by Primaxs Marketing (M) Sdn Bhd, the exclusive Tanko '
        'distributor since 2006. Stock held in Selangor and quoted in Ringgit. Free '
        'delivery and installation in Selangor and the Klang Valley; outstation '
        'delivery quoted separately. 1-year warranty against manufacturing defects, '
        'administered from our Selangor office.')

# our top-level range -> Google product taxonomy id
GPC = {
    'workbench': '503739',          # Business & Industrial > Work Benches
    'workstation': '503739',
    'tool-cabinet': '4207',         # Tool Storage & Organization > Tool Cabinets
    'cnc-tool': '4207',
    'parts-cabinet': '4207',
    'hanger-rack': '4207',
    'perforated-board': '4207',
    'rack': '5millones',            # replaced below; kept explicit to avoid a silent wrong id
    'locker': '4163',               # Furniture > Cabinets & Storage > Lockers
    'documents-cabinet': '448',     # Office Furniture > File Cabinets
    'household-items': '448',
}
GPC['rack'] = '4210'                # Storage Racks

PRETTY = {
    'workbench': 'Workbenches', 'workstation': 'Modular Workstations',
    'tool-cabinet': 'Tool Cabinets & Trolleys', 'cnc-tool': 'CNC Tool Storage',
    'parts-cabinet': 'Parts Cabinets & Bins', 'hanger-rack': 'Hanger Racks',
    'perforated-board': 'Perforated Boards', 'rack': 'Mould & Storage Racks',
    'locker': 'Steel Lockers', 'documents-cabinet': 'Document Cabinets',
    'household-items': 'Home & Office Storage',
}


def txt(x):
    x = re.sub(r'<[^>]+>', ' ', x)
    x = html.unescape(x)
    return re.sub(r'\s+', ' ', x).strip()


items, skipped = [], []
for dp, dn, fn in os.walk(ROOT):
    if 'index.html' not in fn:
        continue
    rel = dp.replace(os.sep, '/')[len(ROOT):].strip('/')
    if rel.count('/') != 2:
        continue
    parts = rel.split('/')
    mother = parts[0]
    if mother not in GPC:
        continue
    s = open(os.path.join(dp, 'index.html'), encoding='utf-8').read()

    sku = parts[2].upper()
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    title = txt(h1.group(1)) if h1 else sku
    price = re.search(r'Reference price:\s*<strong>RM\s*([\d,]+(?:\.\d+)?)', s)
    img = re.search(r'<meta property="og:image" content="([^"]+)"', s)
    if not price or not img:
        skipped.append((rel, 'no price' if not price else 'no image'))
        continue

    # --- description built from the specs actually on the page --------------
    specs = {}
    m = re.search(r'<ul class="spec-list">(.*?)</ul>', s, re.S)
    if m:
        for k, v in re.findall(r'<li><span class="k">(.*?)</span><span class="v">(.*?)</span></li>',
                               m.group(1), re.S):
            specs[txt(k)] = txt(v)

    facts = []
    for key in ('Dimensions', 'Load capacity', 'Material', 'Drawers',
                'Tool Holders', 'Colour', 'Included'):
        if specs.get(key):
            facts.append('%s: %s' % (key, specs[key]))

    desc = title.rstrip('. ') + '. '
    if facts:
        desc += '. '.join(facts) + '. '
    desc += 'Part of the Tanko %s range. ' % PRETTY[mother]
    desc += TAIL
    desc = re.sub(r'\s+', ' ', desc).strip()

    items.append({
        'id': sku,
        'title': title[:150],
        'description': desc,
        'link': '%s/%s/' % (BASE, rel),
        'image_link': img.group(1),
        'availability': 'in_stock',
        'price': '%s MYR' % price.group(1).replace(',', ''),
        'condition': 'new',
        'brand': 'Tanko',
        'mpn': sku,
        'identifier_exists': 'no',
        'google_product_category': GPC[mother],
        'product_type': '%s > %s' % (PRETTY[mother], specs.get('Colour', '') or 'Standard'),
        'shipping': 'MY::Selangor and Klang Valley:0 MYR',
        'shipping_label': 'selangor-free',
    })

L = [len(i['description']) for i in items]
trunc = sum(1 for i in items if not i['description'].rstrip().endswith(('.', '!', '?')))
print('items built            :', len(items))
print('skipped                :', len(skipped))
print('description min/med/max: %d / %d / %d' % (min(L), sorted(L)[len(L) // 2], max(L)))
print('truncated mid-sentence :', trunc)

# every image must actually exist on disk
missing = [i['id'] for i in items
           if not os.path.isfile(ROOT + i['image_link'].replace(BASE, ''))]
print('images missing on disk :', len(missing), missing[:5])

if APPLY:
    if missing or trunc:
        print('REFUSING TO WRITE: feed has missing images or truncated text')
        raise SystemExit(1)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">',
           '  <channel>',
           '    <title>Primaxs Marketing (M) Sdn Bhd - Tanko Industrial Storage Malaysia</title>',
           '    <link>%s</link>' % BASE,
           '    <description>Tanko industrial storage in Malaysia - workbenches, tool '
           'cabinets, CNC tool storage, racks and lockers from the exclusive '
           'distributor Primaxs Marketing.</description>']
    for i in items:
        out.append('    <item>')
        for k, v in i.items():
            out.append('      <g:%s>%s</g:%s>' % (k, html.escape(str(v), quote=True), k))
        out.append('    </item>')
    out += ['  </channel>', '</rss>']
    open(OUT, 'w', encoding='utf-8').write('\n'.join(out))
    print('wrote', OUT, os.path.getsize(OUT), 'bytes')

    with open('marketing/google-merchant-feed.tsv', 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(items[0].keys()), delimiter='\t')
        w.writeheader()
        w.writerows(items)
    print('wrote marketing/google-merchant-feed.tsv')
else:
    print('\nDRY RUN. sample:')
    print(json.dumps(items[0], ensure_ascii=False, indent=1)[:900])
