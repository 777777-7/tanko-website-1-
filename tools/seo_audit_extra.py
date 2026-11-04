# -*- coding: utf-8 -*-
"""Checks seo_audit.py does not cover: JSON-LD validity, duplicate titles and
descriptions, orphan pages (no inbound body links), the thin page, and which
templates the width/height-less images come from. Read-only; prints a report.
Usage: python tools/seo_audit_extra.py"""
import os, re, io, sys, json, glob, collections, html as H
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

pages = sorted(glob.glob("docs/**/*.html", recursive=True))
def url(p):
    u = "/" + os.path.relpath(p, "docs").replace(os.sep, "/")
    return u[:-10] if u.endswith("index.html") else u
src = {p: open(p, encoding="utf-8", errors="ignore").read() for p in pages}
skip = lambda p: "/sales/" in p or p.endswith("404.html") or "/review/" in p

bad_json, titles, descs, noindex = [], collections.defaultdict(list), collections.defaultdict(list), set()
inbound = collections.Counter()
img_nodim = collections.Counter()
words = {}
for p, s in src.items():
    if 'name="robots" content="noindex' in s: noindex.add(p)
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(b)
        except Exception as e: bad_json.append((url(p), str(e)[:60]))
    t = re.search(r"<title>(.*?)</title>", s, re.S); d = re.search(r'<meta name="description" content="([^"]*)"', s)
    if t: titles[H.unescape(t.group(1)).strip()].append(url(p))
    if d: descs[H.unescape(d.group(1)).strip()].append(url(p))
    main = re.search(r"<main.*?</main>", s, re.S)
    body = main.group(0) if main else s
    for h in set(re.findall(r'href="(/[^"#?]*)"', body)):
        inbound[h if h.endswith("/") or "." in h.split("/")[-1] else h + "/"] += 1
    for im in re.findall(r"<img\b[^>]*>", s):
        if "width=" not in im or "height=" not in im:
            m = re.search(r'src="([^"]+)"', im)
            img_nodim[re.sub(r"[^/]+$", "*", m.group(1)) if m else "?"] += 1
    txt = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", body, flags=re.S)
    words[url(p)] = len(txt.split())

print("Invalid JSON-LD blocks:", len(bad_json)); [print("  ", *x) for x in bad_json[:15]]
dt = {k: v for k, v in titles.items() if len(v) > 1}
print("Duplicate titles:", len(dt)); [print("  ", len(v), "x", k[:70], "|", v[:3]) for k, v in sorted(dt.items(), key=lambda x: -len(x[1]))[:12]]
dd = {k: v for k, v in descs.items() if len(v) > 1}
print("Duplicate descriptions:", len(dd)); [print("  ", len(v), "x", k[:70], "|", v[:3]) for k, v in sorted(dd.items(), key=lambda x: -len(x[1]))[:12]]
orph = [url(p) for p in pages if not skip(p) and p not in noindex and inbound[url(p)] == 0 and "/zh/" not in p]
print("Pages with no inbound links from any page body (EN/MS):", len(orph)); [print("  ", u) for u in orph[:40]]
print("Thinnest indexable pages:"); [print("  ", n, u) for u, n in sorted(((u, n) for u, n in words.items() if "/sales/" not in u and "404" not in u), key=lambda x: x[1])[:8]]
print("Images without width/height, by folder:"); [print("  ", n, k) for k, n in img_nodim.most_common(12)]
