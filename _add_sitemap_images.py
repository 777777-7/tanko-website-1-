# -*- coding: utf-8 -*-
"""
_add_sitemap_images.py
在 sitemap.xml 的每个 <url> 中加入 <image:image><image:loc>...</image:loc></image:image>，
图片取该页 og:image（产品图）。保留原有 lastmod/priority 等。找不到产品图则原样保留。
"""
import os, re, io

DOCS = r"C:\Users\User\Documents\GitHub\tanko-website-1-\docs"
SITE = "https://www.storagesystem.com.my"
SITEMAP = os.path.join(DOCS, "sitemap.xml")

URL_RE = re.compile(r"<url>\s*<loc>(.*?)</loc>(.*?)</url>", re.S)
OG_RE = re.compile(r'<meta property="og:image" content="(https://www\.storagesystem\.com\.my/(?:asset3|asset_content)/[^"]+)"')

def page_og(url):
    rel = url.replace(SITE, "").strip("/")
    # 处理 index 结尾
    cands = []
    if rel:
        cands.append(os.path.join(DOCS, rel.replace("/", os.sep), "index.html"))
        cands.append(os.path.join(DOCS, rel.replace("/", os.sep) + ".html"))
    else:
        cands.append(os.path.join(DOCS, "index.html"))
    for p in cands:
        if os.path.isfile(p):
            try:
                with io.open(p, "r", encoding="utf-8") as f:
                    head = f.read(200000)
            except Exception:
                continue
            m = OG_RE.search(head)
            return m.group(1) if m else None
    return None

def main():
    with io.open(SITEMAP, "r", encoding="utf-8") as f:
        xml = f.read()
    if "xmlns:image" not in xml:
        xml = xml.replace(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
            1,
        )
    used = set()
    def repl(m):
        loc = m.group(1)
        inner = m.group(2)
        if "<image:image>" in inner:
            return m.group(0)
        img = page_og(loc)
        if not img or img in used:
            return m.group(0)
        used.add(img)
        return "<url>\n    <loc>%s</loc>%s    <image:image>\n      <image:loc>%s</image:loc>\n    </image:image>\n  </url>" % (loc, inner, img)
    new_xml, n = URL_RE.subn(repl, xml)
    if n:
        with io.open(SITEMAP, "w", encoding="utf-8") as f:
            f.write(new_xml)
    print("url entries:", n, "| images added:", len(used))
    print("new size:", os.path.getsize(SITEMAP))

if __name__ == "__main__":
    main()
