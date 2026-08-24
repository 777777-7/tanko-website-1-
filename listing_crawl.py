# -*- coding: utf-8 -*-
"""
Listing-level extraction from tanko.com.tw.

For every category and every sub-collection (sort) — e.g.
  /products/workstation/            (All)
  /products/workstation/professional/
  /products/workstation/classic/
walk all pagination and capture EVERY product card:

  h3.title      -> group_title      ("Professional Workstation")
  p.class       -> "Combination | RY" -> distinct_title + sku_code
  div.Img img   -> listing_image
  a[href]       -> detail_url / slug

Purpose: give every product family a DISTINCT title (not the repeated group
name), record which sub-collection(s) each belongs to so we can build separate
SEO sub-pages (Professional / Classic / ...), and guarantee nothing is missed.

Output: listing_products.json  +  a per-(category,subcollection) index.
Does NOT touch products.json or the site build.
"""

import io, json, os, re, sys, time
from collections import OrderedDict, defaultdict
import requests
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.tanko.com.tw"
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
     "Accept-Language": "en-US,en;q=0.9"}
DELAY = 0.4
CATEGORIES = ["workstation", "workbench", "tool-cabinet", "cnc-tool", "rack",
              "hanger-rack", "locker", "parts-cabinet", "documents-cabinet",
              "perforated-board", "household-items"]
session = requests.Session(); session.headers.update(H)
failed = []


def get(url):
    for a in range(3):
        try:
            r = session.get(url, timeout=25); r.raise_for_status()
            time.sleep(DELAY); return r.text
        except Exception as e:
            if a == 2:
                failed.append({"url": url, "error": str(e)}); return None
            time.sleep(1.2 * (a + 1))
    return None


def slug_of(u):
    return u.rstrip("/").rsplit("/", 1)[-1].lower()


def parse_cards(html, category, subcollection):
    soup = BeautifulSoup(html, "html.parser")
    cards = []
    for item in soup.select("div.productsItem"):
        a = item.select_one('a[href*="/en/products-detail/"]')
        if not a:
            continue
        detail_url = a.get("href", "").split("?")[0]
        if detail_url.startswith("/"):
            detail_url = BASE + detail_url
        h3 = item.select_one("h3.title")
        group_title = h3.get_text(strip=True) if h3 else ""
        pc = item.select_one("p.class")
        raw = pc.get_text(" ", strip=True) if pc else ""
        parts = [x.strip() for x in raw.split("|") if x.strip()]
        distinct_title = parts[0] if parts else ""
        sku_code = parts[1] if len(parts) > 1 else ""
        img = item.select_one("div.Img img")
        listing_image = (img.get("data-src") or img.get("src")) if img else ""
        cards.append({
            "slug": slug_of(detail_url),
            "detail_url": detail_url,
            "group_title": group_title,
            "distinct_title": distinct_title,
            "sku_code": sku_code,
            "listing_desc_raw": raw,
            "listing_image": listing_image,
            "category": category,
            "subcollection": subcollection,
        })
    return cards


def crawl_listing(url, category, subcollection):
    """Paginate a listing page until no new products appear."""
    out, seen, page = [], set(), 1
    while page <= 40:
        purl = url if page == 1 else f"{url}?page={page}"
        html = get(purl)
        if not html:
            break
        cards = parse_cards(html, category, subcollection)
        new = [c for c in cards if c["slug"] not in seen]
        if not new:
            break
        for c in new:
            seen.add(c["slug"])
        out.extend(new)
        page += 1
    return out


def find_subcollections(category):
    url = f"{BASE}/en/products/{category}/"
    html = get(url)
    subs = OrderedDict()
    subs[("All", url)] = None  # category root
    if html:
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.select(f'a[href*="/en/products/{category}/"]'):
            href = a.get("href", "").split("?")[0]
            m = re.search(rf"/en/products/{re.escape(category)}/([a-z0-9\-]+)/?$", href)
            if m:
                label = a.get_text(strip=True) or m.group(1)
                full = href if href.startswith("http") else BASE + href
                subs[(label, full)] = m.group(1)
    return subs


def main():
    products = OrderedDict()   # slug -> record (with subcollections set)
    by_group = defaultdict(list)   # (category, subcollection_label) -> [slug,...]

    for cat in CATEGORIES:
        subs = find_subcollections(cat)
        labels = [lbl for (lbl, _u) in subs.keys()]
        print(f"[{cat}] sub-collections: {labels}")
        for (label, url), sub_slug in subs.items():
            cards = crawl_listing(url, cat, sub_slug or "all")
            for c in cards:
                rec = products.get(c["slug"])
                if not rec:
                    rec = {**c, "subcollections": []}
                    rec.pop("subcollection", None)
                    products[c["slug"]] = rec
                # record membership (label as the sort, e.g. Professional/Classic/Hooks)
                tag = label
                if tag not in rec["subcollections"]:
                    rec["subcollections"].append(tag)
                # keep the most specific (non-"All") distinct title/desc if root was blank
                if label != "All":
                    if c["distinct_title"] and not rec.get("distinct_title"):
                        rec["distinct_title"] = c["distinct_title"]
                    if c["sku_code"] and not rec.get("sku_code"):
                        rec["sku_code"] = c["sku_code"]
                by_group[(cat, label)].append(c["slug"])
            print(f"    {label:16s}: {len(cards)} products")

    products_list = list(products.values())

    # index: category -> subcollection -> [products]
    index = defaultdict(lambda: defaultdict(list))
    for slug, rec in products.items():
        for sub in rec["subcollections"]:
            index[rec["category"]][sub].append({
                "slug": slug, "distinct_title": rec["distinct_title"],
                "sku_code": rec["sku_code"], "group_title": rec["group_title"],
            })

    with open(os.path.join(ROOT, "listing_products.json"), "w", encoding="utf-8") as f:
        json.dump(products_list, f, ensure_ascii=False, indent=2)
    with open(os.path.join(ROOT, "listing_index.json"), "w", encoding="utf-8") as f:
        json.dump({c: {s: v for s, v in subs.items()} for c, subs in index.items()},
                  f, ensure_ascii=False, indent=2)
    with open(os.path.join(ROOT, "listing_failed.json"), "w", encoding="utf-8") as f:
        json.dump(failed, f, ensure_ascii=False, indent=2)

    # report
    print("\n" + "=" * 56)
    print("LISTING EXTRACTION REPORT")
    print("=" * 56)
    print(f"Total distinct products (by slug): {len(products_list)}")
    dup_titles = defaultdict(int)
    for r in products_list:
        dup_titles[r["distinct_title"]] += 1
    blank = sum(1 for r in products_list if not r["distinct_title"])
    print(f"Products with a distinct title:    {len(products_list) - blank}")
    print(f"Products with BLANK distinct title:{blank}")
    print(f"Pages failed:                      {len(failed)}")
    print("\nSub-collections per category:")
    for cat in CATEGORIES:
        subs = sorted({s for r in products_list if r['category'] == cat for s in r['subcollections']})
        n = sum(1 for r in products_list if r["category"] == cat)
        print(f"  {cat:18s} {n:3d} products  sorts={subs}")
    print("\nSample distinct titles (should NOT all be the group name):")
    for r in products_list[:14]:
        print(f"  [{r['category']}/{'|'.join(r['subcollections'])}] "
              f"{r['group_title']} -> '{r['distinct_title']}'  (SKU {r['sku_code']})")


if __name__ == "__main__":
    main()
