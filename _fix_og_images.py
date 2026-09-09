# -*- coding: utf-8 -*-
"""
_fix_og_images.py
把 docs/ 下每个页面的 og:image 从通用 logo 图换成该页自己的产品主图。
仅修改 <meta property="og:image" content="..."> 行；找不到产品图则保留原值。
用法: python _fix_og_images.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
SITE = "https://www.storagesystem.com.my"
GENERIC = SITE + "/assets/primaxs-og-1200x630.png"

OG_RE = re.compile(r'(<meta property="og:image" content=")([^"]*)(")')
# 候选产品图路径：asset3 / asset_content / assets 下非 logo 图
IMG_SRC_RE = re.compile(r'<img[^>]+src="(/asset3/[^"]+|/asset_content/[^"]+)"')
DATA_SRC_RE = re.compile(r'data-src="(/asset3/[^"]+|/asset_content/[^"]+)"')
PRELOAD_RE = re.compile(r'<link rel="preload" as="image" href="(/asset3/[^"]+|/asset_content/[^"]+)"')
LD_IMG_RE = re.compile(r'"image"\s*:\s*"(https://www\.storagesystem\.com\.my/(?:asset3|asset_content)/[^"]+)"')

def first_product_image(html):
    """返回页面第一个产品图绝对 URL，找不到返回 None。"""
    m = LD_IMG_RE.search(html)
    if m:
        return m.group(1)
    m = PRELOAD_RE.search(html)
    if m:
        return SITE + m.group(1)
    m = IMG_SRC_RE.search(html)
    if m:
        return SITE + m.group(1)
    m = DATA_SRC_RE.search(html)
    if m:
        return SITE + m.group(1)
    return None

def fix_file(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    m = OG_RE.search(html)
    if not m:
        return "no-og"
    cur = m.group(2)
    if cur and cur != GENERIC:
        return "skip-already"
    img = first_product_image(html)
    if not img:
        return "keep-generic"
    new_html = OG_RE.sub(lambda mm: mm.group(1) + img + mm.group(3), html, count=1)
    if new_html != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
        return "FIXED->" + img
    return "no-change"

def main():
    changed, kept, already, noog = [], 0, 0, 0
    for dirpath, dirnames, filenames in os.walk(DOCS):
        for fn in filenames:
            if fn != "index.html":
                continue
            p = os.path.join(dirpath, fn)
            r = fix_file(p)
            if r.startswith("FIXED"):
                changed.append((os.path.relpath(p, DOCS), r[5:]))
            elif r == "keep-generic":
                kept += 1
            elif r == "skip-already":
                already += 1
            elif r == "no-og":
                noog += 1
    print("TOTAL FIXED:", len(changed))
    print("keep-generic:", kept, "| already product og:", already, "| no og line:", noog)
    for rel, img in changed[:40]:
        print(" ", rel, "->", img)

if __name__ == "__main__":
    main()
