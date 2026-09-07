# -*- coding: utf-8 -*-
"""Reprice the site from the merged Tanko agent lists (E147 over NO.146).

RM = ceil(USD) * 12.05
"""
import os, re, json, math, sys, csv, collections

SCR = os.path.dirname(os.path.abspath(__file__))
RATE = 12.05
APPLY = '--apply' in sys.argv
ROOT = 'docs'
SCRIPT = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)

data = json.load(open(os.path.join(SCR, 'merged_usd.json')))
PLAIN = data['plain']
COL = {tuple(k.split('|')): v for k, v in data['col'].items()}

SITE_COL = re.compile(r'^(.*?)\s*\(([A-Za-z ]+)\)\s*$')


def _one(sku):
    """USD for a single (non-combo) SKU, resolving colour variants."""
    sku = sku.strip()
    m = SITE_COL.match(sku)
    if m:
        key, col = m.group(1).strip(), m.group(2).strip().upper()
        if (key, col) in COL:
            return COL[(key, col)]
        if key in PLAIN:
            return PLAIN[key]
    if sku in PLAIN:
        return PLAIN[sku]
    m2 = re.match(r'^(.*?)\(([A-Za-z ]+)\)$', sku)
    if m2:
        k2, c2 = m2.group(1).strip(), m2.group(2).strip().upper()
        if (k2, c2) in COL:
            return COL[(k2, c2)]
        if k2 in PLAIN:
            return PLAIN[k2]
    return None


def usd_for(sku):
    """USD for a site SKU. Combos ("A + B", and "A(C) + B" where C is itself a
    listed part) sum their components, per Wei Ming: add the prices, then
    round up, then multiply."""
    direct = _one(sku)
    if direct is not None:
        return direct

    parts = [p.strip() for p in sku.split('+')] if '+' in sku else [sku]
    total, resolved = 0.0, True
    for part in parts:
        # a parenthesised token that is itself a listed SKU is a component,
        # not a colour
        extra = []
        m = re.match(r'^(.*?)\(([^)]+)\)\s*$', part)
        if m and m.group(2).strip() in PLAIN:
            part, extra = m.group(1).strip(), [m.group(2).strip()]
        vals = [_one(x) for x in [part] + extra]
        if any(v is None for v in vals):
            resolved = False
            break
        total += sum(vals)
    return total if (resolved and total > 0) else None


def rm(u):
    return round(math.ceil(u) * RATE, 2)


prod_pages = fam_pages = 0
prices_set = variants_set = aggs = visible = 0
newly = []
unmatched = set()

for dirpath, _d, files in os.walk(ROOT):
    if 'index.html' not in files:
        continue
    p = os.path.join(dirpath, 'index.html')
    s = open(p, encoding='utf-8').read()
    if '"Product"' not in s and '"ProductGroup"' not in s:
        continue
    out = s
    touched = False

    for m in list(SCRIPT.finditer(s)):
        raw = m.group(1)
        try:
            d = json.loads(raw)
        except Exception:
            continue
        hit = [False]

        def walk(n):
            global prices_set, variants_set, aggs
            if isinstance(n, dict):
                t = n.get('@type')
                if t == 'Product':
                    sku = n.get('sku')
                    if sku:
                        u = usd_for(sku)
                        if u is None:
                            unmatched.add(sku)
                        else:
                            val = rm(u)
                            o = n.get('offers')
                            if isinstance(o, dict):
                                if o.get('price') != val:
                                    o['price'] = val
                                    ps = o.get('priceSpecification')
                                    if isinstance(ps, dict):
                                        ps['price'] = val
                                    hit[0] = True
                                    prices_set += 1
                if t == 'ProductGroup':
                    prices = []
                    for v in n.get('hasVariant') or []:
                        if not isinstance(v, dict):
                            continue
                        vs = v.get('sku')
                        o = v.get('offers')
                        if isinstance(o, dict) and vs:
                            u = usd_for(vs)
                            if u is not None and o.get('price') != rm(u):
                                o['price'] = rm(u)
                                hit[0] = True
                                variants_set += 1
                            if o.get('price'):
                                prices.append(float(o['price']))
                    off = n.get('offers')
                    if isinstance(off, dict) and prices:
                        lo, hi = min(prices), max(prices)
                        if off.get('lowPrice') != lo or off.get('highPrice') != hi:
                            off['lowPrice'] = lo
                            off['highPrice'] = hi
                            off['offerCount'] = len(prices)
                            hit[0] = True
                            aggs += 1
                for v in n.values():
                    walk(v)
            elif isinstance(n, list):
                for v in n:
                    walk(v)

        walk(d)
        if hit[0]:
            out = out.replace(raw, json.dumps(d, ensure_ascii=False), 1)
            touched = True

    msku = re.search(r'Model No\.\s*([A-Z0-9][A-Z0-9\-\(\)\+ ]*?)\s*&middot;', out)
    if msku:
        sku = msku.group(1).strip()
        u = usd_for(sku)
        if u is not None:
            new_txt = 'RM {:,.2f}'.format(rm(u))
            mcur = re.search(r'<div class="ref-price">Reference price: <strong>([^<]*)</strong>', out)
            cur = mcur.group(1) if mcur else ''
            if cur != new_txt:
                out = re.sub(r'(<div class="ref-price">Reference price: <strong>)[^<]*(</strong>)',
                             lambda mm: mm.group(1) + new_txt + mm.group(2), out)
                visible += 1
                touched = True
                if cur in ('on request', ''):
                    newly.append((sku, new_txt))

    if touched:
        if 'hasVariant' in out:
            fam_pages += 1
        else:
            prod_pages += 1
        if APPLY:
            open(p, 'w', encoding='utf-8').write(out)

print('MODE:', 'APPLY' if APPLY else 'DRY RUN')
print('product pages   : %d' % prod_pages)
print('family pages    : %d' % fam_pages)
print('  schema prices : %d' % prices_set)
print('  variants      : %d' % variants_set)
print('  aggregates    : %d' % aggs)
print('  visible RM    : %d' % visible)
print('  SKUs with no price in either list: %d' % len(unmatched))
print('  sample unmatched:', sorted(unmatched)[:10])
