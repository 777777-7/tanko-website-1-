# -*- coding: utf-8 -*-
"""
Full SEO audit across the seven categories a 2026 audit covers:
technical, on-page, content/E-E-A-T, Core Web Vitals, off-page,
AEO/GEO readiness, local SEO.
"""
import os, re, io, sys, json, glob, collections, html as HTMLLIB
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
os.chdir(r"C:\Users\User\Documents\GitHub\tanko-website-1-")

pages = sorted(glob.glob("docs/**/*.html", recursive=True))
cache = {}
def body(p):
    if p not in cache:
        cache[p] = open(p, encoding="utf-8", errors="ignore").read()
    return cache[p]

def hdr(t):
    print("\n" + "=" * 66)
    print(t)
    print("=" * 66)

def row(label, val, ok, note=""):
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {label:<42} {str(val):>7}  {note}")
    return ok

results = []

# ─────────────── 1. TECHNICAL ───────────────
hdr("1. TECHNICAL SEO")
miss_title = miss_desc = bad_h1 = jumps = noalt = nocanon = noviewport = 0
long_title = long_desc = 0
for p in pages:
    h = body(p)
    t = re.search(r"<title>([^<]*)</title>", h)
    if not t or len(t.group(1).strip()) < 3: miss_title += 1
    elif len(HTMLLIB.unescape(t.group(1))) > 60: long_title += 1
    d = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)', h, re.I)
    if not d or len(d.group(1)) < 20: miss_desc += 1
    elif len(HTMLLIB.unescape(d.group(1))) > 160: long_desc += 1
    if len(re.findall(r"<h1[\s>]", h, re.I)) != 1: bad_h1 += 1
    if not re.search(r'rel=["\']canonical["\']', h, re.I): nocanon += 1
    if not re.search(r'name=["\']viewport["\']', h, re.I): noviewport += 1
    for img in re.findall(r"<img\b[^>]*>", h, re.I):
        if not re.search(r"\balt\s*=", img, re.I): noalt += 1
    hs = [int(x) for x in re.findall(r"<h([1-6])[\s>]", h, re.I)]
    prev = 0
    for x in hs:
        if prev and x > prev + 1: jumps += 1; break
        prev = x

results += [
 row("Pages scanned", len(pages), True),
 row("Missing <title>", miss_title, miss_title == 0),
 row("Title over 60 chars", long_title, long_title == 0),
 row("Missing meta description", miss_desc, miss_desc == 0),
 row("Meta description over 160", long_desc, long_desc == 0),
 row("Pages without exactly one h1", bad_h1, bad_h1 == 0),
 row("Heading hierarchy jumps", jumps, jumps == 0),
 row("Images without alt", noalt, noalt == 0),
 row("Missing canonical", nocanon, nocanon <= 1, "1 = /sales/ noindex"),
 row("Missing viewport", noviewport, noviewport == 0),
]
for f, label in [("docs/robots.txt", "robots.txt"), ("docs/sitemap.xml", "sitemap.xml"),
                 ("docs/_headers", "_headers"), ("docs/404.html", "404 page")]:
    results.append(row(f"{label} present", "yes" if os.path.exists(f) else "no", os.path.exists(f)))

hh = open("docs/_headers", encoding="utf-8").read()
sec = ["Strict-Transport-Security", "X-Content-Type-Options", "Referrer-Policy",
       "X-Frame-Options", "Permissions-Policy"]
n = sum(1 for s in sec if s in hh)
results.append(row("Security headers", f"{n}/5", n == 5))

sm = open("docs/sitemap.xml", encoding="utf-8").read()
results.append(row("Sitemap URLs", sm.count("<url>"), sm.count("<url>") > 1800))
results.append(row("Sitemap excludes /sales/", sm.count("/sales/"), sm.count("/sales/") == 0))

# ─────────────── 2. ON-PAGE ───────────────
hdr("2. ON-PAGE SEO")
noog = notw = noh2 = thin = 0
for p in pages:
    h = body(p)
    if not re.search(r'property=["\']og:title["\']', h, re.I): noog += 1
    if not re.search(r'name=["\']twitter:', h, re.I): notw += 1
    if len(re.findall(r"<h2[\s>]", h, re.I)) == 0: noh2 += 1
    text = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", h, flags=re.S)
    if len(text.split()) < 300: thin += 1
results += [
 row("Missing og:title", noog, noog == 0),
 row("Missing twitter card", notw, notw == 0),
 row("Pages with no h2", noh2, noh2 == 0),
 row("Thin pages (<300 words)", thin, thin == 0),
]

# ─────────────── 3. CONTENT & E-E-A-T ───────────────
hdr("3. CONTENT & E-E-A-T")
guides = len(glob.glob("docs/guides/*/index.html"))
bm_guides = sum(1 for p in glob.glob("docs/guides/*/index.html") if 'lang="ms-MY"' in body(p))
home = body("docs/index.html")
results += [
 row("Guide articles", guides, guides >= 25),
 row("Bahasa Malaysia guides", bm_guides, bm_guides >= 10),
 row("Organization schema on home", "yes" if '"Organization"' in home else "no", '"Organization"' in home),
 row("LocalBusiness schema", "yes" if '"LocalBusiness"' in home else "no", '"LocalBusiness"' in home),
 row("Author/publisher declared", "yes" if "publisher" in home else "no", "publisher" in home),
 row("About page exists", "yes" if os.path.exists("docs/about/index.html") else "no",
     os.path.exists("docs/about/index.html")),
 row("Contact page exists", "yes" if os.path.exists("docs/contact/index.html") else "no",
     os.path.exists("docs/contact/index.html")),
]
ab = body("docs/about/index.html")
results.append(row("About mentions years in trade", "yes" if re.search(r"\b(2006|since)\b", ab) else "no",
                   bool(re.search(r"\b2006\b", ab))))

# ─────────────── 4. CORE WEB VITALS (static proxies) ───────────────
hdr("4. CORE WEB VITALS — static signals")
nodim = nolazy = noprldA = 0
for p in pages:
    h = body(p)
    imgs = re.findall(r"<img\b[^>]*>", h, re.I)
    for i in imgs:
        if not (re.search(r"\bwidth=", i) and re.search(r"\bheight=", i)): nodim += 1
    for i in imgs[1:]:
        src = re.search(r'src="([^"]+)"', i)
        if src and src.group(1).endswith(".svg"): continue   # above-fold logo
        if 'loading=' not in i: nolazy += 1
    if 'rel="preload"' not in h: noprldA += 1
results += [
 row("Images without width/height (CLS)", nodim, nodim == 0),
 row("Below-fold images not lazy", nolazy, nolazy == 0),
 row("Pages without LCP preload", noprldA, noprldA < len(pages) * 0.15,
     "hub pages legitimately have none"),
]
css = os.path.getsize("docs/assets/css/site.css")
results.append(row("site.css size (KB)", round(css/1024), css < 200*1024))
results.append(row("Cache headers on assets", "yes" if "max-age=31536000" in hh else "no",
                   "max-age=31536000" in hh))
webp = len(glob.glob("docs/asset3/*.webp"))
jpg  = len(glob.glob("docs/asset3/*.jpg"))
results.append(row("WebP served (jpg in docs)", f"{webp} webp / {jpg} jpg", jpg == 0,
                   "0 jpg = WebP-only"))

# ─────────────── 5. AEO / GEO READINESS ───────────────
hdr("5. AEO / GEO — AI answer engine readiness")
faq = sum(1 for p in pages if "FAQPage" in body(p))
prod = sum(1 for p in pages if '"Product"' in body(p) or "ProductGroup" in body(p))
bc   = sum(1 for p in pages if "BreadcrumbList" in body(p))
rob = open("docs/robots.txt", encoding="utf-8").read()
ai_bots = ["OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Claude-SearchBot",
           "ClaudeBot", "GPTBot", "Google-Extended", "anthropic-ai"]
allowed = sum(1 for b in ai_bots if b in rob)
results += [
 row("Pages with FAQPage schema", faq, faq >= 30),
 row("Pages with Product schema", prod, prod > 1500),
 row("Pages with BreadcrumbList", bc, bc > 1800),
 row("AI crawlers explicitly allowed", f"{allowed}/{len(ai_bots)}", allowed == len(ai_bots)),
 row("Sitemap referenced in robots", "yes" if "Sitemap:" in rob else "no", "Sitemap:" in rob),
]

# ─────────────── 6. LOCAL SEO ───────────────
hdr("6. LOCAL SEO")
nap_addr = "Jalan Balakong Jaya" in home
nap_tel  = "+60-3-4296-4737" in home or "4296" in home
geo      = 'name="geo.position"' in home
loc_pages = len(glob.glob("docs/locations/*/index.html"))
ind_pages = len(glob.glob("docs/industries/*/index.html"))
results += [
 row("NAP address in schema", "yes" if nap_addr else "no", nap_addr),
 row("Telephone in schema", "yes" if nap_tel else "no", nap_tel),
 row("Geo coordinates meta", "yes" if geo else "no", geo),
 row("Location landing pages", loc_pages, loc_pages >= 5),
 row("Industry landing pages", ind_pages, ind_pages >= 5),
 row("areaServed in schema", "yes" if "areaServed" in home else "no", "areaServed" in home),
 row("openingHours in schema", "yes" if "openingHours" in home else "no", "openingHours" in home),
]

# ─────────────── 7. INTERNATIONAL / HREFLANG ───────────────
hdr("7. INTERNATIONAL — hreflang integrity")
alt_pages = [p for p in pages if body(p).count('rel="alternate"') > 2]
broken = 0
for p in alt_pages:
    h = body(p)
    pairs = re.findall(r'hreflang="([^"]+)" href="([^"]+)"', h)
    langs = [l for l, _ in pairs]
    if "x-default" not in langs: broken += 1
results += [
 row("Pages with language alternates", len(alt_pages), len(alt_pages) == 42,
     "10 guide pairs + 11 cat pairs = 42"),
 row("Alternate sets missing x-default", broken, broken == 0),
]
ms = sum(1 for p in pages if '<html lang="ms-MY">' in body(p))
results.append(row("Pages declaring ms-MY", ms, ms == 21, "10 guides + 11 categories"))

# ─────────────── SCORE ───────────────
hdr("SCORE")
passed = sum(1 for r in results if r)
total = len(results)
print(f"\n  {passed} / {total} checks passing  ({round(passed/total*100)}%)\n")
