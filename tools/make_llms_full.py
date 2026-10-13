# -*- coding: utf-8 -*-
"""Build docs/llms-full.txt: the whole catalogue as plain text for AI assistants.

llms.txt is the short index; this file lists every product family with its model count,
size range, guide-price range and URL, read straight from the published product pages,
so an assistant answering "where can I buy X in Malaysia, and for how much" has the facts.

Run:  python tools/make_llms_full.py
"""
import glob, io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
SITE = 'https://www.storagesystem.com.my'
CATS = [('workbench', 'Industrial workbenches'), ('tool-cabinet', 'Tool cabinets, chests and trolleys'),
        ('perforated-board', 'Perforated boards (pegboards), hooks and holders'),
        ('cnc-tool', 'CNC tool storage'), ('workstation', 'Modular workstations'),
        ('parts-cabinet', 'Parts cabinets and bin storage'),
        ('hanger-rack', 'Hanger racks, louvre panels and display stands'),
        ('documents-cabinet', 'Document cabinets and A4 trays'), ('locker', 'Steel lockers'),
        ('rack', 'Mould racks and warehouse racking'), ('household-items', 'Home and small-office storage')]


def text(h, pat):
    m = re.search(pat, h, re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1))).strip() if m else ''


def main():
    lines = []
    head = io.open(os.path.join(DOCS, 'llms.txt'), encoding='utf-8').read()
    company = head.split('## Key specifications')[0].strip()
    lines += [company, '',
              'This is the full catalogue. Prices are Ringgit guide prices published on each model page; '
              'the final quotation depends on configuration, quantity and delivery location. '
              '"Price on request" means no guide price is published for that model.', '']
    total = 0
    for slug, name in CATS:
        cat_dir = os.path.join(DOCS, slug)
        if not os.path.isdir(cat_dir):
            continue
        cat_title = text(io.open(os.path.join(cat_dir, 'index.html'), encoding='utf-8').read(), r'<title>(.*?)</title>')
        lines += ['## %s' % name, '%s/%s/ (%s)' % (SITE, slug, cat_title.replace('&amp;', '&')), '']
        for fam in sorted(d for d in os.listdir(cat_dir) if os.path.isdir(os.path.join(cat_dir, d))):
            pages = glob.glob(os.path.join(cat_dir, fam, '*', 'index.html'))
            if not pages:
                continue
            fam_html = os.path.join(cat_dir, fam, 'index.html')
            fam_name = ''
            if os.path.exists(fam_html):
                fam_name = text(io.open(fam_html, encoding='utf-8').read(), r'<h1[^>]*>(.*?)</h1>')
            prices, models, dims = [], [], []
            for p in pages:
                h = io.open(p, encoding='utf-8').read()
                sku = text(h, r'<div class="sku-line">Model No\. (.*?) &middot;')
                if sku:
                    models.append(sku)
                m = re.search(r'Reference price: <strong>RM ([\d,\.]+)</strong>', h)
                if m:
                    prices.append(float(m.group(1).replace(',', '')))
                dm = re.search(r'Dimensions</span><span class="v">([^<]*)', h)
                if dm:
                    dims.append(dm.group(1).strip())
            total += len(pages)
            price = ('RM%s to RM%s' % (format(min(prices), ',.2f'), format(max(prices), ',.2f'))
                     if prices else 'price on request')
            if prices and min(prices) == max(prices):
                price = 'RM%s' % format(min(prices), ',.2f')
            size = ''
            if dims:
                uniq = sorted(set(dims))
                size = '; sizes: ' + ('; '.join(uniq[:4]) + ('; and %d more' % (len(uniq) - 4) if len(uniq) > 4 else ''))
            ex = ', '.join(sorted(models)[:6]) + (' ...' if len(models) > 6 else '')
            lines.append('- %s (%s/%s/%s/): %d models (%s); %s%s' % (
                fam_name.replace('&amp;', '&') or fam.upper(), SITE, slug, fam, len(pages), ex, price, size))
        lines.append('')
    lines += ['Total product pages listed: %d.' % total, '',
              'Guides: %s/guides/  ·  Locations served: %s/locations/  ·  Contact: %s/contact/' % (SITE, SITE, SITE)]
    out = os.path.join(DOCS, 'llms-full.txt')
    io.open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('wrote', out, os.path.getsize(out), 'bytes,', total, 'product pages')


if __name__ == '__main__':
    main()
