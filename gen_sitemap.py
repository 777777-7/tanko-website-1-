# -*- coding: utf-8 -*-
"""
Generate sitemap.xml + robots.txt covering every real page in dist/.
Excludes assets, JSON, static files. Uses lastmod = build date.
"""
import os, sys, io, datetime, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "docs")   # GitHub Pages serves from /docs
DOMAIN = "https://www.storagesystem.com.my"
TODAY = datetime.date.today().isoformat()

# Priority + change-freq by page type — order matters; first match wins
PRIORITY = [
    ("^index\\.html$",                             1.0,  "weekly"),
    ("^products/index\\.html$",                    0.9,  "weekly"),
    ("^(about|contact|enquiry|download)/index\\.html$", 0.6, "monthly"),
    ("^(locations|industries)/index\\.html$",      0.8,  "weekly"),
    ("^(locations|industries)/[a-z0-9_-]+/index\\.html$", 0.7, "monthly"),
    ("^guides/[a-z0-9_-]+/index\\.html$",          0.7,  "monthly"),
    ("^[a-z-]+/index\\.html$",                     0.9,  "weekly"),    # category
    ("^[a-z-]+/[a-z0-9_-]+/[a-z0-9_()-]+/index\\.html$", 0.5, "monthly"),  # variant
    ("^[a-z-]+/[a-z0-9_-]+/index\\.html$",         0.7,  "monthly"),   # sub-cat + family
]

def rank(rel):
    for pat, prio, freq in PRIORITY:
        if re.match(pat, rel): return prio, freq
    return 0.5, "monthly"

def find_pages():
    pages = []
    for root, dirs, files in os.walk(DIST):
        # skip asset dirs
        rel_root = os.path.relpath(root, DIST).replace("\\", "/")
        if rel_root.startswith(("assets", "asset3", "asset_content", "asset2")):
            continue
        for f in files:
            if f == "index.html":
                rel = os.path.relpath(os.path.join(root, f), DIST).replace("\\", "/")
                pages.append(rel)
    return sorted(pages)

def url_for(rel):
    # index.html at root -> /
    # foo/index.html -> /foo/
    if rel == "index.html": return DOMAIN + "/"
    return DOMAIN + "/" + rel[:-len("index.html")]

def main():
    pages = find_pages()
    print(f"pages found: {len(pages)}")

    # sitemap.xml
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for rel in pages:
        prio, freq = rank(rel)
        u = url_for(rel)
        lines.append("  <url>")
        lines.append(f"    <loc>{u}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    with open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"sitemap.xml: {len(pages)} URLs written")

    # robots.txt — explicitly permissive to real-time AI answer engines,
    # so Primaxs stays citable inside ChatGPT / Perplexity / Claude answers
    # to Malaysia B2B storage queries.
    robots = f"""# Primaxs Marketing (M) Sdn Bhd — robots.txt

# Default policy: allow every well-behaved crawler
User-agent: *
Allow: /
Disallow: /search_index.json

# --- Real-time AI answer engines (explicit allow for clarity) ---
# These fetch a page when a user asks the assistant a question and cite it back.
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Perplexity-User
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Applebot
Allow: /
User-agent: Applebot-Extended
Allow: /

# --- Training crawlers (allow — brand + product visibility is the goal) ---
User-agent: GPTBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: CCBot
Allow: /

# --- Aggressive scrapers we don't want (block) ---
User-agent: Bytespider
Disallow: /

Sitemap: {DOMAIN}/sitemap.xml
"""
    with open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(robots)
    print("robots.txt written")

    # basic breakdown by page type
    from collections import Counter
    types = Counter()
    for rel in pages:
        depth = rel.count("/")
        if rel == "index.html": t = "homepage"
        elif depth == 1: t = "top-level (about/contact/products/…)"
        elif depth == 2:
            top = rel.split("/")[0]
            if top == "guides": t = "guide article"
            else: t = f"category or sub-collection: {top}"
        elif depth == 3: t = f"family: {rel.split('/')[0]}"
        elif depth == 4: t = f"variant: {rel.split('/')[0]}"
        else: t = f"depth-{depth}"
        types[t] += 1
    print("\nby type:")
    for k, v in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {v:5d}  {k}")

if __name__ == "__main__":
    main()
