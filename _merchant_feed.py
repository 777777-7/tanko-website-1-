# -*- coding: utf-8 -*-
"""
_merchant_feed.py
扫描 docs 下所有产品变体页（含 Reference price），生成 Google Merchant Center XML feed。
价格 = 页面参考价（RM），无价格（Price on request）不收录。
输出: docs/merchant-feed.xml
"""
import os, re, io, html, datetime

DOCS = r"C:\Users\User\Documents\GitHub\tanko-website-1-\docs"
SITE = "https://www.storagesystem.com.my"
OUT = os.path.join(DOCS, "merchant-feed.xml")

PRICE_RE = re.compile(r'class="ref-price">Reference price: <strong>RM\s*([\d,]+\.?\d*)</strong>')
PRICE_ON_REQ_RE = re.compile(r'class="ref-price">[^<]*Price on request', re.I)
OG_URL_RE = re.compile(r'<meta property="og:url" content="([^"]+)"')
OG_IMG_RE = re.compile(r'<meta property="og:image" content="([^"]+)"')
TITLE_RE = re.compile(r'<title>([^<]+)</title>')
H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S)
SKU_RE = re.compile(r'"sku"\s*:\s*"([^"]+)"')
DESC_RE = re.compile(r'<meta name="description" content="([^"]+)"')

def clean(s):
    return html.escape(re.sub(r'<[^>]+>', '', s), quote=True).strip()

def main():
    items = []
    seen = set()
    for dirpath, dirnames, filenames in os.walk(DOCS):
        for fn in filenames:
            if fn != "index.html":
                continue
            p = os.path.join(dirpath, fn)
            try:
                with io.open(p, "r", encoding="utf-8") as f:
                    txt = f.read(400000)
            except Exception:
                continue
            m_price = PRICE_RE.search(txt)
            if not m_price:
                continue  # 无价格或 Price on request
            price = m_price.group(1).replace(",", "")
            m_url = OG_URL_RE.search(txt)
            if not m_url:
                continue
            url = m_url.group(1)
            if url in seen:
                continue
            seen.add(url)
            m_sku = SKU_RE.search(txt) or re.search(r'itemprop="sku"[^>]*>([^<]+)<', txt)
            sku = m_sku.group(1) if m_sku else url.rstrip("/").split("/")[-1]
            m_img = OG_IMG_RE.search(txt)
            img = m_img.group(1) if m_img else ""
            m_title = H1_RE.search(txt)
            title = clean(m_title.group(1)) if m_title else sku
            m_desc = DESC_RE.search(txt)
            desc = html.unescape(m_desc.group(1)) if m_desc else ""
            # 产品类型 = 站点路径结构（第 2 段起）
            parts = url.replace(SITE, "").strip("/").split("/")
            ptype = " > ".join(p.capitalize() for p in parts[:-1]) if len(parts) > 1 else "Storage"
            items.append((sku, title, url, img, price, desc, ptype))

    now = datetime.date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">',
             '  <channel>',
             '    <title>Primaxs Marketing Tanko Malaysia Products</title>',
             '    <link>%s/products/</link>' % SITE,
             '    <description>High-spec Tanko industrial storage products in Malaysia - exclusive distributor Primaxs Marketing</description>']
    for sku, title, url, img, price, desc, ptype in items:
        lines.append('    <item>')
        lines.append('      <g:id>%s</g:id>' % html.escape(sku, quote=True))
        lines.append('      <g:title>%s</g:title>' % html.escape(title, quote=True))
        lines.append('      <g:link>%s</g:link>' % html.escape(url, quote=True))
        lines.append('      <g:image_link>%s</g:image_link>' % html.escape(img, quote=True))
        lines.append('      <g:price>%s MYR</g:price>' % price)
        lines.append('      <g:availability>in stock</g:availability>')
        lines.append('      <g:condition>new</g:condition>')
        lines.append('      <g:brand>Tanko</g:brand>')
        lines.append('      <g:identifier_exists>FALSE</g:identifier_exists>')
        lines.append('      <g:product_type>%s</g:product_type>' % html.escape(ptype, quote=True))
        lines.append('      <g:description>%s</g:description>' % html.escape(desc, quote=True))
        lines.append('    </item>')
    lines.append('  </channel>')
    lines.append('</rss>')

    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("items:", len(items))
    print("size:", os.path.getsize(OUT))
    # 样例
    for it in items[:3]:
        print("  ", it[0], "|", it[1][:40], "| RM", it[4], "|", it[2][:60])

if __name__ == "__main__":
    main()
