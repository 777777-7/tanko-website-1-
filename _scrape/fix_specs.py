#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix heavy-duty tool cabinet variant spec pages:
   1) replace wrong spec-list rows with real dimensions/slide/material
   2) inject the correct per-variant drawer-configuration row image
   Does not touch anything else."""
import re, os, sys

BASE = r"C:\Users\User\Documents\GitHub\tanko-website-1-\docs\tool-cabinet"

# width class -> (W mm, D mm)
WIDTH = {
    "ea-7":  {"ea": (566, 607), "eb": (718, 607), "ed": (718, 759), "h": 700},
    "ea-10": {"ea": (566, 607), "eb": (718, 607), "ed": (718, 759), "h": 1000},
    "ea-12": {"ea": (566, 607), "eb": (718, 607), "ed": (718, 759), "h": 1200},
    "ea-7m": {"ea": (566, 640), "eb": (718, 640), "ed": None,        "h": 850},
}

# family -> list of (folder_basename_without_t/m, specN)
def row_map(fam):
    if fam == "ea-7":
        rows = {
            "ea": (["ea-7041","ea-7042","ea-7051","ea-7052"],
                   ["ea-7053","ea-7054","ea-7061","ea-7073"]),
            "eb": (["eb-7041","eb-7042","eb-7051","eb-7052"],
                   ["eb-7053","eb-7054","eb-7061","eb-7073"]),
        }
    elif fam == "ea-10":
        rows = {
            "ea": (["ea-10051","ea-10052","ea-10061","ea-10062"],
                   ["ea-10071","ea-10072","ea-10073","ea-10091"]),
            "eb": (["eb-10051","eb-10052","eb-10061","eb-10062"],
                   ["eb-10071","eb-10072","eb-10073","eb-10091"]),
            "ed": (["ed-10051","ed-10052","ed-10061","ed-10062"],
                   ["ed-10071","ed-10072","ed-10073","ed-10091"]),
        }
    elif fam == "ea-12":
        rows = {
            "ea": (["ea-12051","ea-12052","ea-12071","ea-12072"],
                   ["ea-12073","ea-12074","ea-12081","ea-12082"]),
            "eb": (["eb-12051","eb-12052","eb-12071","eb-12072"],
                   ["eb-12073","eb-12074","eb-12081","eb-12082"]),
            "ed": (["ed-12051","ed-12052","ed-12071","ed-12072"],
                   ["ed-12073","ed-12074","ed-12081","ed-12082"]),
        }
    elif fam == "ea-7m":
        rows = {
            "ea": (["ea-7041","ea-7042","ea-7051","ea-7052"],
                   ["ea-7053","ea-7054","ea-7061","ea-7081"]),
            "eb": (["eb-7041","eb-7042","eb-7051","eb-7052"],
                   ["eb-7053","eb-7054","eb-7061","eb-7081"]),
        }
    return rows

def pick_spec(fam, folder):
    f = folder.lower()
    # strip suffix
    base = f
    is_t = False
    is_ma = False
    if fam == "ea-7m":
        if base.endswith("ma"):
            base = base[:-2]; is_ma = True
        elif base.endswith("m"):
            base = base[:-1]
    else:
        if base.endswith("t"):
            base = base[:-1]; is_t = True
    rows = row_map(fam)
    for wc, (r1, r2) in rows.items():
        if base in r1:
            return spec_index(wc, 1, fam), base, is_t, is_ma
        if base in r2:
            return spec_index(wc, 2, fam), base, is_t, is_ma
    return None, base, is_t, is_ma

def spec_index(wc, row, fam):
    # order per family: ea rows first, then eb, then ed
    if fam == "ea-7":
        order = {"ea": 1, "eb": 3}
    elif fam == "ea-7m":
        order = {"ea": 1, "eb": 3}
    else:
        order = {"ea": 1, "eb": 3, "ed": 5}
    return order[wc] + (row - 1)

def fmt(fam, folder):
    info, base, is_t, is_ma = pick_spec(fam, folder)
    w = WIDTH[fam]
    wc = base[:2]
    if wc == "ed" and "ed" not in w:
        wc = "eb"
    W, D = w[wc]
    H = w["h"]
    if fam == "ea-7m" and is_ma:
        # EB with panel set 1380
        D = 640; W = 718; H = 1380
    dim = f"W{W}&times;D{D}&times;H{H} mm"
    if fam == "ea-7m":
        slide = "4&Prime;&times;2&Prime; PU castors, 1000 kg load capacity"
        mat = "Cabinet: Steel &middot; Handle: Plastic"
        if is_ma:
            slide = "4&Prime;&times;2&Prime; PU castors, 1000 kg load capacity &middot; with back panel set"
    else:
        if is_t:
            slide = "T drawer &mdash; 100% extension, 200 kg per drawer"
        else:
            slide = "Standard drawer &mdash; 90% extension, 100 kg per drawer"
        mat = "Steel &middot; grey body, blue drawers"
    return info, dim, slide, mat, is_t, is_ma

changed = 0
for fam in ["ea-7", "ea-10", "ea-12", "ea-7m"]:
    fdir = os.path.join(BASE, fam)
    for folder in sorted(os.listdir(fdir)):
        idx = os.path.join(fdir, folder, "index.html")
        if not os.path.isfile(idx):
            continue
        with open(idx, "r", encoding="utf-8") as fh:
            html = fh.read()
        before = html

        info, dim, slide, mat, is_t, is_ma = fmt(fam, folder)
        spec_img = f"/asset_content/{fam}/spec{info}.webp"

        # 1) Replace the wrong spec rows (Cabinet slide system + Drawers) with correct ones
        # existing wrong pattern:
        # <li ...>Cabinet (slide system)</span>...<li ...>Drawers</span><span ...>NUMBER</span></li>
        new_rows = (
            f'<li><span class="k">Dimensions</span><span class="v">{dim}</span></li>'
            f'<li><span class="k">Slide system</span><span class="v">{slide}</span></li>'
            f'<li><span class="k">Material</span><span class="v">{mat}</span></li>'
        )
        pat = re.compile(
            r'<li><span class="k">Cabinet \(slide system\)</span>.*?<li><span class="k">Drawers</span><span class="v">[^<]*</span></li>',
            re.S)
        if pat.search(html):
            html = pat.sub(new_rows, html, count=1)
        else:
            # fallback: insert Dimensions at start of spec-list
            html = html.replace('<ul class="spec-list">',
                                '<ul class="spec-list">' + new_rows, 1)

        # 2) Inject the row image into variant-gallery (once)
        if spec_img not in html:
            inject = (f'<img src="{spec_img}" alt="Drawer configuration and dimensions" '
                      f'class="spec-row-img" loading="lazy">')
            # insert right after the closing </div> of variant-thumbs, before closing .variant-gallery
            m = re.search(r'(<div class="variant-thumbs">.*?</div>)', html, re.S)
            if m:
                html = html[:m.end(1)] + "\n" + inject + html[m.end(1):]
            else:
                # append after main gallery img
                html = re.sub(r'(<div class="variant-gallery">\s*<img[^>]+>)',
                              r'\1\n' + inject, html, count=1)

        if html != before:
            with open(idx, "w", encoding="utf-8") as fh:
                fh.write(html)
            changed += 1
            print(f"OK  {fam}/{folder}  spec{info}")

print(f"\nTotal changed: {changed}")
