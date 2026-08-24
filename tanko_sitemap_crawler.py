"""
Tanko.com.tw Product Sitemap Crawler (v2 — with variant extraction)
--------------------------------------------------------------------
Crawls every product category, sub-collection, pagination page, and
individual product-detail page under https://www.tanko.com.tw/en/products/,
AND parses each product-detail page for the individual model variants
(e.g. RY-01A, RY-02A, WAS-57042N) listed as text on that page, along with
their Dimensions / Material / Items included details.

Usage:
    pip install requests beautifulsoup4
    python tanko_sitemap_crawler.py

Output written to the SAME folder you run this from:
    tanko_sitemap.json

To confirm where that is, run `cd` with no arguments right before running
the script — that's exactly where the JSON will appear.
"""

import json
import os
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://www.tanko.com.tw"
PRODUCTS_URL = f"{BASE}/en/products/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; SitemapResearchBot/1.0)"}
DELAY = 1.0  # seconds between requests — be polite to their server

MODEL_NO_RE = re.compile(r"Model No\.\s*([A-Za-z0-9\-\_\.\/□]+)")
DIM_RE = re.compile(r"Dimensions?\s*[:：]\s*([^\n]+)")
MATERIAL_RE = re.compile(r"Material\s*[:：]\s*([^\n]+)")
LOAD_RE = re.compile(r"([\d,]+\s?kg\s?load\s?capacity)", re.IGNORECASE)


def get_soup(url):
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    time.sleep(DELAY)
    return BeautifulSoup(resp.text, "html.parser")


def get_top_categories():
    soup = get_soup(PRODUCTS_URL)
    cats = {}
    for a in soup.select('a[href*="/en/products/"]'):
        href = a.get("href", "")
        m = re.match(r"^/en/products/([a-z0-9\-]+)/?$", href.replace(BASE, ""))
        if not m:
            continue
        slug = m.group(1)
        name = a.get_text(strip=True)
        if not name:
            continue
        cats[slug] = {"name": name, "url": urljoin(BASE, href)}
    return cats


def get_subcategories(category_url):
    soup = get_soup(category_url)
    subs = {}
    for a in soup.select("a"):
        href = a.get("href", "")
        if "/en/products/" not in href:
            continue
        rel = href.replace(category_url.rstrip("/"), "").strip("/")
        if rel and "/" not in rel and "products-detail" not in href:
            subs[rel] = urljoin(BASE, href)
    return subs


def get_products_on_page(url):
    soup = get_soup(url)
    products = []
    for h3 in soup.select("h3 a[href*='/en/products-detail/']"):
        name = h3.get_text(strip=True)
        href = urljoin(BASE, h3.get("href"))
        products.append({"name": name, "url": href})

    next_page = None
    page_links = soup.select('a[href*="?page="]')
    if page_links:
        next_page = urljoin(BASE, page_links[0].get("href"))
    return products, next_page


def crawl_category_products(category_url, max_pages=10):
    all_products = []
    seen_urls = set()
    page_num = 1
    while page_num <= max_pages:
        url = category_url if page_num == 1 else f"{category_url.rstrip('/')}/?page={page_num}"
        products, _ = get_products_on_page(url)
        new = [p for p in products if p["url"] not in seen_urls]
        if not new:
            break
        for p in new:
            seen_urls.add(p["url"])
        all_products.extend(new)
        page_num += 1
    return all_products


def extract_variants(product_detail_url):
    """
    Parse a product-detail page's body text for repeated
    'Model No. XXX ... Dimensions: ... Material: ...' blocks.
    Returns a list of variant dicts. Falls back to an empty list
    if no Model No. pattern is found (some pages are single-variant
    and just show specs without repeating "Model No.").
    """
    soup = get_soup(product_detail_url)
    text = soup.get_text("\n", strip=True)

    model_matches = list(MODEL_NO_RE.finditer(text))
    if not model_matches:
        return []

    variants = []
    for i, m in enumerate(model_matches):
        start = m.start()
        end = model_matches[i + 1].start() if i + 1 < len(model_matches) else len(text)
        block = text[start:end]

        model_no = m.group(1).strip(" ·")
        dim_match = DIM_RE.search(block)
        mat_match = MATERIAL_RE.search(block)
        load_match = LOAD_RE.search(block)

        variants.append({
            "model_no": model_no,
            "dimensions": dim_match.group(1).strip() if dim_match else None,
            "material": mat_match.group(1).strip() if mat_match else None,
            "load_capacity": load_match.group(1).strip() if load_match else None,
        })
    return variants


def main():
    cwd = os.getcwd()
    print(f"Running from: {cwd}")
    print(f"Output will be written to: {os.path.join(cwd, 'tanko_sitemap.json')}\n")

    print("Fetching top-level categories...")
    categories = get_top_categories()
    print(f"Found {len(categories)} categories: {list(categories)}")

    result = {"categories": {}}

    for slug, info in categories.items():
        print(f"\n=== {info['name']} ({slug}) ===")
        subs = get_subcategories(info["url"])
        print(f"  Subcategories: {list(subs)}")

        products = crawl_category_products(info["url"])
        print(f"  Product-family pages found: {len(products)}")

        for p in products:
            variants = extract_variants(p["url"])
            p["variants"] = variants
            if variants:
                print(f"    {p['name']}: {len(variants)} model variant(s)")

        result["categories"][slug] = {
            "url": info["url"],
            "name": info["name"],
            "subcategories": subs,
            "products": products,
        }

    out_path = os.path.join(cwd, "tanko_sitemap.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    total_products = sum(len(c["products"]) for c in result["categories"].values())
    total_variants = sum(
        len(p.get("variants", []))
        for c in result["categories"].values()
        for p in c["products"]
    )
    print(f"\nDone.")
    print(f"  {total_products} product-family pages")
    print(f"  {total_variants} individual model variants extracted")
    print(f"  Written to: {out_path}")


if __name__ == "__main__":
    main()
