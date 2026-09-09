# -*- coding: utf-8 -*-
"""Extract per-series card data from the tanko website (read-only)."""
import os, io, re, json, sys

DOCS = r'C:\Users\User\Documents\GitHub\tanko-website-1-\docs'

# Category hub dirs (not product series) per category
HUBS = {
    'cnc-tool': {'cnc-tool-cabinet', 'cnc-tool-cabinet-with-door'},
    'documents-cabinet': {'documents-cabinet'},
    'hanger-rack': {'hanger-rack', 'display-stand'},
    'locker': set(),
    'parts-cabinet': {'parts-bin', 'parts-cabinet'},
    'perforated-board': {'perforated-board'},
    'rack': {'mould-rack'},
    'tool-cabinet': {'heavy-duty-tool-cabinet', 'standard-tool-cabinet', 'tilt-out-bins-cart'},
    'workbench': {'heavy-duty', 'hexagonal', 'packing-station', 'performance', 'professional', 'stainless-steel', 'workbench-accessories'},
    'workstation': {'classic', 'professional'},
    'household-items': set(),
}

# manual merge: sub-family dir -> base family dir (same product line)
MERGE = {
    'wa-57a': 'wa-57', 'wa-57m': 'wa-57',
    'wa-67a': 'wa-67', 'wa-67m': 'wa-67',
    'wb57-ega': 'wb-57', 'wb67-ega': 'wb-67',
    'we1200': 'we', 'wet1200': 'wet',
    'wdt-48s': 'wdt-4202', 'wdt-58s': 'wdt-5203', 'wdt-68s': 'wdt-6203',
    'wbs-53022': 'wb-57', 'wbs-63022': 'wb-67',
    'wbt-5203': 'wb-57', 'wbt-6203': 'wb-67',
    'wat-5203': 'wa-57', 'wat-6203': 'wa-67', 'wat-7203': 'wa-77',
    'wd-4801': 'wd-48', 'wd-48s': 'wd-48', 'wd-4ms': 'wd-48',
    'wd-5801': 'wd-58', 'wd-58s': 'wd-58', 'wd-5ms': 'wd-58',
    'wd-6801': 'wd-68', 'wd-68s': 'wd-68', 'wd-6ms': 'wd-68',
    'was-57042': 'was-54', 'was-67053': 'was-74', 'was-77042': 'was-74',
    'wp-53': 'wp-51', 'wp-6': 'wp-51', 'wp-9_1': 'wp-51',
    'whb-881': 'whb-88', 'whb-882': 'whb-88',
    'sa_k': 'sa', 'saa-331': 'saa-231', 'sab-331': 'saa-231', 'sag-231': 'saa-231',
    'ra-6201': 'ra-6091', 'ra-9201': 'ra-9091', 're-6201': 're-6201',
    'ega-1': 'ega-1', 'eka-3ms': 'eka-3m', 'ela-1': 'ela-1',
    'kq-306as': 'kq-3',
    'a4l-330d': 'a4l-330',
    'ea-10mn': 'ea-10mn', 'ea-10n': 'ea-10n',
    'kabinet-alat': None,
}

CATS = ['workbench', 'workstation', 'tool-cabinet', 'cnc-tool', 'rack', 'locker',
        'parts-cabinet', 'perforated-board', 'documents-cabinet', 'hanger-rack', 'household-items']

def clean(s):
    return s.replace('\u00e2\u20ac\u201c', '-').replace('\u00c2\u00b7', '\u00b7').replace('\u00e2\u20ac\u02dc', "'")

out = []
for cat in CATS:
    catdir = os.path.join(DOCS, cat)
    if not os.path.isdir(catdir):
        continue
    hubs = HUBS.get(cat, set())
    for fam in sorted(os.listdir(catdir)):
        fdir = os.path.join(catdir, fam)
        if not os.path.isdir(fdir) or not os.path.exists(os.path.join(fdir, 'index.html')):
            continue
        if fam in hubs:
            continue
        base = MERGE.get(fam, fam)
        if base != fam:
            continue  # merged into base (handled when base is visited)
        fp = os.path.join(fdir, 'index.html')
        t = io.open(fp, encoding='utf-8').read()
        ti = re.search(r'<title>([^<]+)</title>', t)
        title = clean(ti.group(1)) if ti else fam
        # sku list from family JSON-LD hasVariant
        skus = []
        for m in re.finditer(r'"sku": "([^"]+)"', t):
            if m.group(1) not in skus and 'Primaxs' not in m.group(1):
                skus.append(m.group(1))
        # variant subdirs
        vdirs = [d for d in os.listdir(fdir) if os.path.isdir(os.path.join(fdir, d))]
        # first variant page for dims/specs
        dims, material, loadcap = '', '', ''
        vname = ''
        for vd in vdirs:
            vp = os.path.join(fdir, vd, 'index.html')
            if not os.path.exists(vp):
                continue
            vt = io.open(vp, encoding='utf-8').read()
            m = re.search(r'"name": "([^"]*?(?:W\d{3,5} ?x ?D|W\d{3,5})[^"]*)"', vt)
            if m:
                vname = clean(m.group(1))
                dm = re.search(r'(W\d{3,5}\s*[xX×]\s*D\d{3,5}\s*[xX×]\s*H\d{3,5}\s*mm)', vname)
                if dm:
                    dims = dm.group(1).replace(' ', '')
                break
        # load capacity + material from first variant page text
        for vd in vdirs:
            vp = os.path.join(fdir, vd, 'index.html')
            if not os.path.exists(vp):
                continue
            vt = io.open(vp, encoding='utf-8').read()
            lm = re.search(r'(?:Load|loading)[^<]{0,80}?(\d{2,4}\s*(?:kg|KG))', vt)
            if lm:
                loadcap = lm.group(1)
                break
        # photo: asset3 first sku webp, else asset_content first webp
        photo = ''
        for sku in skus:
            p = os.path.join(DOCS, 'asset3', sku + '.webp')
            if os.path.exists(p):
                photo = '/asset3/' + sku + '.webp'
                break
        if not photo:
            m = re.search(r'/(asset_content/' + re.escape(fam) + r'/[^"\s\)]+\.(?:webp|jpg|png))', t)
            if m:
                photo = '/' + m.group(1)
        out.append({'cat': cat, 'fam': fam, 'title': title, 'skus': skus[:14],
                    'dims': dims, 'loadcap': loadcap, 'photo': photo, 'vname': vname[:160]})

json.dump(out, io.open(r'C:\Users\User\Documents\GitHub\tanko-website-1-\_cards_data.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('series count:', len(out))
for o in out:
    print(' -', o['cat'], '/', o['fam'], '|', o['title'][:45], '| dims:', o['dims'], '| load:', o['loadcap'], '| photo:', o['photo'][:40], '| skus:', len(o['skus']))
