#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tag wide configuration row diagrams in family Specification tabs so they
   span full width (natural rectangle) instead of being cropped into a 3-col grid."""
import os, re
from PIL import Image

DOCS = r"C:\Users\User\Documents\GitHub\tanko-website-1-\docs"
CANDIDATE_DIRS = [
    os.path.join(DOCS, "tool-cabinet"),
    os.path.join(DOCS, "cnc-tool"),
]
RATIO = 1.6  # wide image threshold

def local(src):
    # src like /asset_content/ea-10/exp3_1.webp or /asset3/...
    if src.startswith("/"):
        return os.path.join(DOCS, src.lstrip("/").replace("/", os.sep))
    return src

changed = 0
for root in CANDIDATE_DIRS:
    if not os.path.isdir(root):
        continue
    for fam in os.listdir(root):
        idx = os.path.join(root, fam, "index.html")
        if not os.path.isfile(idx):
            continue
        html = open(idx, encoding="utf-8").read()
        before = html

        # find each <li ...><div class="pf-img"><img src="...">
        li_pat = re.compile(r'<li([^>]*?)>\s*<div class="pf-img"><img src="([^"]+)"')
        def repl(m):
            attrs, src = m.group(1), m.group(2)
            f = local(src)
            wide = False
            try:
                with Image.open(f) as im:
                    w, h = im.size
                wide = (w / h) >= RATIO
            except Exception:
                wide = False
            if wide and "pf-rowdiag" not in attrs:
                mcls = re.search(r'class="([^"]*)"', attrs)
                if mcls:
                    merged = (mcls.group(1).strip() + " pf-rowdiag").strip()
                    attrs = attrs[:mcls.start()] + 'class="' + merged + '"' + attrs[mcls.end():]
                else:
                    attrs = attrs + ' class="pf-rowdiag"'
                return '<li' + attrs + '><div class="pf-img"><img src="' + src + '"'
            return m.group(0)

        html = li_pat.sub(repl, html)
        if html != before:
            open(idx, "w", encoding="utf-8").write(html)
            changed += 1
            print("tagged:", os.path.relpath(idx, DOCS))

print("\nfiles changed:", changed)
