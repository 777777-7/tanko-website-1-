# -*- coding: utf-8 -*-
"""
_apply_home_optimizations.py
1) 首页 + 产品页: RC-6094(Stainless steel) 图 → RY-04SA（工作台卡片换成 RY 工作台）
2) 首页 og:image → RY-04SA
3) 首页/产品页 meta description + og:description → 高规格卖点文案
4) og:title 增强
"""
import io, re

DOCS = r"C:\Users\User\Documents\GitHub\tanko-website-1-\docs"
SITE = "https://www.storagesystem.com.my"

HOME = DOCS + r"\index.html"
PROD = DOCS + r"\products\index.html"

HOME_DESC = "Malaysia&#39;s exclusive Tanko distributor since 2006. High-spec made-in-Taiwan steel workbenches, CNC tool cabinets, lockers &amp; racking for factories &amp; workshops. Ringgit pricing, fast quote."
HOME_TITLE = "High-Spec Industrial Storage &amp; Tool Cabinets Malaysia | Primaxs"
HOME_OG = SITE + "/asset3/RY-04SA.webp"

PROD_DESC = "Browse Tanko industrial storage in Malaysia \u2014 high-spec made-in-Taiwan workbenches, CNC tool cabinets, workstations, racking &amp; lockers for factories &amp; workshops. Exclusive distributor, fast quote."
PROD_TITLE = "All Tanko Products | High-Spec Industrial Storage Malaysia | Primaxs"

def repl(path, pairs, label):
    with io.open(path, "r", encoding="utf-8") as f:
        html = f.read()
    before = html
    for old, new in pairs:
        html = html.replace(old, new)
    if html != before:
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(label, "CHANGED")
    else:
        print(label, "no-change")

# --- homepage ---
repl(HOME, [
    ('<meta property="og:image" content="' + SITE + '/assets/primaxs-og-1200x630.png">',
     '<meta property="og:image" content="' + HOME_OG + '">'),
    ('RC-6094(Stainless steel)-w800.webp', 'RY-04SA-w800.webp'),
    ('RC-6094(Stainless steel).webp', 'RY-04SA.webp'),
    ('<meta name="description" content="Malaysia&#39;s exclusive Tanko distributor since 2006. Workbenches, tool cabinets, CNC storage &amp; lockers \u2014 Selangor stock, Ringgit pricing, quote in one day.">',
     '<meta name="description" content="' + HOME_DESC + '">'),
    ('<meta property="og:description" content="Malaysia&#39;s exclusive Tanko distributor since 2006. Workbenches, tool cabinets, CNC storage &amp; lockers \u2014 Selangor stock, Ringgit pricing, quote in one day.">',
     '<meta property="og:description" content="' + HOME_DESC + '">'),
    ('<meta property="og:title" content="Industrial Storage &amp; Tool Cabinets Malaysia | Primaxs">',
     '<meta property="og:title" content="' + HOME_TITLE + '">'),
], "home")

# --- products page ---
repl(PROD, [
    ('RC-6094(Stainless steel)-w800.webp', 'RY-04SA-w800.webp'),
    ('RC-6094(Stainless steel).webp', 'RY-04SA.webp'),
], "prod-imgs")

# products meta description/og:description/og:title via regex (exact current values unknown)
def repl_meta(path, desc, title, label):
    with io.open(path, "r", encoding="utf-8") as f:
        html = f.read()
    before = html
    html = re.sub(r'(<meta name="description" content=")[^"]*(">)', r'\g<1>' + desc + r'\g<2>', html, count=1)
    html = re.sub(r'(<meta property="og:description" content=")[^"]*(">)', r'\g<1>' + desc + r'\g<2>', html, count=1)
    html = re.sub(r'(<meta property="og:title" content=")[^"]*(">)', r'\g<1>' + title + r'\g<2>', html, count=1)
    if html != before:
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(label, "meta CHANGED")
    else:
        print(label, "meta no-change")

repl_meta(PROD, PROD_DESC, PROD_TITLE, "products")

# verify
import subprocess
