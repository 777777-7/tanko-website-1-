# -*- coding: utf-8 -*-
"""Parse both Tanko agent price lists and merge them.

NO.146   dated 114/04/25 -> ROC 114 = April 2025
NO.E147  dated 115/03/25 -> ROC 115 = March 2026   <-- newer

E147 wins on any SKU present in both. NO.146 fills everything E147 omits.
"""
import fitz, re, json, math, os, sys

SCR = os.path.dirname(os.path.abspath(__file__))
RATE = 12.05
COLOURS = {'WHITE', 'BLACK', 'GRAY', 'GREY', 'BLUE', 'RED', 'GREEN', 'YELLOW',
           'ORANGE', 'SILVER', 'IVORY', 'BEIGE'}

SKU_RE = re.compile(r'^([A-Z][A-Z0-9]*(?:[-_][A-Z0-9]+)+)\s+(.+)$')
PRICE_RE = re.compile(r'^([0-9][0-9,]*\.[0-9]{2})$')


def parse(path):
    doc = fitz.open(path)
    lines = []
    for i in range(doc.page_count):
        lines += [l.rstrip() for l in doc[i].get_text().split('\n')]
    plain, col = {}, {}
    i = 0
    while i < len(lines):
        m = SKU_RE.match(lines[i].strip())
        if not m:
            i += 1
            continue
        sku, rest = m.group(1), m.group(2)
        price, j, hop = None, i + 1, 0
        while j < len(lines) and hop < 3:
            c = lines[j].strip().replace(',', '')
            p = PRICE_RE.match(c)
            if p:
                price = float(p.group(1))
                break
            rest += ' ' + lines[j].strip()
            j += 1
            hop += 1
        if price is None:
            i += 1
            continue
        cs = [x.strip('() ').upper() for x in re.findall(r'\(([^)]+)\)', rest)]
        cc = next((x for x in cs if x in COLOURS), None)
        if cc:
            col[(sku, cc)] = price
        plain.setdefault(sku, price)
        i = j + 1
    return plain, col


P146 = r'C:\Users\User\Downloads\NO.146 Agent（USD）-00 (1).pdf'
P147 = r'C:\Users\User\Downloads\NO.E147 Agent USD price list-00 (1).pdf'

p146, c146 = parse(P146)
p147, c147 = parse(P147)

print('NO.146 (Apr 2025) : %4d SKUs, %3d colour variants' % (len(p146), len(c146)))
print('E147   (Mar 2026) : %4d SKUs, %3d colour variants' % (len(p147), len(c147)))
print('  only in E147    : %4d' % len(set(p147) - set(p146)))
print('  only in NO.146  : %4d' % len(set(p146) - set(p147)))
print('  in both         : %4d' % len(set(p146) & set(p147)))

both = set(p146) & set(p147)
diff = [(s, p146[s], p147[s]) for s in both if abs(p146[s] - p147[s]) > 0.005]
print('    price differs : %4d' % len(diff))
for s, a, b in sorted(diff)[:8]:
    print('      %-14s 146=$%-9s E147=$%s' % (s, a, b))

# merged: E147 takes precedence
plain = dict(p146)
plain.update(p147)
col = dict(c146)
col.update(c147)
print()
print('MERGED: %d SKUs, %d colour variants' % (len(plain), len(col)))

json.dump({'plain': plain,
           'col': {'%s|%s' % k: v for k, v in col.items()}},
          open(os.path.join(SCR, 'merged_usd.json'), 'w'), indent=0)
print('written merged_usd.json')
