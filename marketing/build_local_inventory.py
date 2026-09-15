# -*- coding: utf-8 -*-
"""Generate docs/local-inventory.xml for Google free LOCAL listings.

WHY THIS AND NOT THE SHOPPING TAB. Search Console keeps prompting to "show your
333 products on the Shopping tab". Standard free listings require a working
online checkout, and Google names "websites offering only quote requests instead
of direct purchases" as a disapproval reason (abuse of the network). Enabling
that prompt risks suspension.

Free LOCAL listings are the honest alternative. The policy states plainly:
"Your site doesn't require an online checkout and payment option."
Malaysia is a supported country. They surface on Search, Maps, Images and Lens.

WHAT THIS FILE IS. A supplemental overlay on the primary feed, not a second
catalogue. Google is explicit that products should be submitted once, in one
data source, and the local inventory file only adds store-level availability.
So g:id here is copied verbatim from merchant-feed.xml and never regenerated.

Attributes, per the local inventory data specification:
    g:id           required, must equal the primary feed id exactly
    g:store_code   required, case-sensitive, must match Business Profile
    g:availability required
    g:price        optional, overrides the primary price for this store
    g:quantity     DELIBERATELY OMITTED - see below

ON QUANTITY. The spec lists it optional; the upload guide lists it required. We
do not track per-SKU stock counts, and the policy requires accurate inventory
data. Inventing 1,517 quantities would be a policy breach, so the file ships
without them. If the first fetch errors on missing quantity, the honest fix is
real counts from Wei Ming, not a made-up number.

ON pickup_method / pickup_sla. Omitted. Optional since Sept 2024 and Google now
advises against including them. Pickup in Google's model means order online then
collect; there is no online ordering step here, so asserting a pickup SLA would
be a claim we cannot back.
"""
import os
import re
import sys
import html

APPLY = '--apply' in sys.argv
ROOT = 'docs'
SRC = os.path.join(ROOT, 'merchant-feed.xml')
OUT = os.path.join(ROOT, 'local-inventory.xml')

# Set in Google Business Profile first: More settings > Advanced > Store code.
# Must match exactly, including case. Never change it once chosen.
# Google assigns the store code itself; it is NOT ours to choose. Read off
# Business Profile Manager (business.google.com/locations, column 商店代码)
# on 15 Sep 2026. The first build used a readable 'PRIMAXS-BALAKONG' and
# Merchant Center rejected all 1,517 rows with '[Business Profile] Invalid
# store code'. If the listing is ever re-created, re-read this value.
STORE_CODE = '11724893644651686981'

if not os.path.isfile(SRC):
    raise SystemExit('primary feed not found: %s' % SRC)

src = open(SRC, encoding='utf-8').read()
items = re.findall(r'<item>(.*?)</item>', src, re.S)
rows = []
for it in items:
    i = re.search(r'<g:id>(.*?)</g:id>', it, re.S)
    p = re.search(r'<g:price>(.*?)</g:price>', it, re.S)
    a = re.search(r'<g:availability>(.*?)</g:availability>', it, re.S)
    if not i:
        continue
    rows.append({
        'id': html.unescape(i.group(1)).strip(),
        'price': html.unescape(p.group(1)).strip() if p else None,
        'availability': html.unescape(a.group(1)).strip() if a else 'in_stock',
    })

# sanity: ids must be unique and non-empty
ids = [r['id'] for r in rows]
assert all(ids), 'blank id in primary feed'
dupes = len(ids) - len(set(ids))

out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">',
       '  <channel>',
       '    <title>Primaxs Marketing (M) Sdn Bhd - Local Inventory</title>',
       '    <link>https://www.storagesystem.com.my</link>',
       '    <description>Local inventory for the Taman Industri Balakong Jaya '
       'premises, Seri Kembangan, Selangor.</description>']
for r in rows:
    out.append('    <item>')
    out.append('      <g:id>%s</g:id>' % html.escape(r['id'], quote=True))
    out.append('      <g:store_code>%s</g:store_code>' % STORE_CODE)
    out.append('      <g:availability>%s</g:availability>' % r['availability'])
    if r['price']:
        out.append('      <g:price>%s</g:price>' % html.escape(r['price'], quote=True))
    out.append('    </item>')
out += ['  </channel>', '</rss>']
body = '\n'.join(out)

print('MODE:', 'APPLY' if APPLY else 'DRY RUN')
print('items in primary feed :', len(items))
print('rows written          :', len(rows))
print('duplicate ids         :', dupes)
print('store code            :', STORE_CODE)
print('size                  : %.1f KB' % (len(body) / 1024))
print('\nfirst row:')
print('\n'.join(body.split('\n')[6:13]))

if APPLY:
    if dupes:
        raise SystemExit('REFUSING TO WRITE: duplicate ids would trigger "Product ID already used"')
    open(OUT, 'w', encoding='utf-8').write(body)
    print('\nwrote', OUT)
