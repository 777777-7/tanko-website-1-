"""
Tanko.com.tw Variant Scraper (v3 — AJAX endpoint, no Playwright)
----------------------------------------------------------------
Extracts EVERY product variant across the whole tanko.com.tw catalog,
including color / material / size combinations that the earlier scrapers
missed. Works entirely over plain HTTP — no browser automation needed.

How it works
    1. Crawl the 11 product categories (paginated) to find every
       /en/products-detail/{slug}/ page.
    2. On each product-detail page, extract:
         - indexId (from JS references in the HTML)
         - all radio-input spec groups from <ul class="specList">
           each group is a "level" (Combination, Top, Panel Set, ...)
           each option carries a data-id like 1320, 1945, ...
    3. Compute the cross-product of all levels.
    4. For each combination, hit
         /en/products/act/?act=8&indexId=X&package1Id=A&package2Id=B...
       to get the exact Model No. that combination resolves to.
    5. Hit /en/products-item/?indexId=X&packageNId=... to get the
       variant image URLs.
    6. Save one flat list of variants to tanko_variants.json.

Usage
    python -m pip install requests beautifulsoup4
    python tanko_variant_scraper.py

Output (in the folder you run it from)
    tanko_variants.json  — one entry per real SKU/variant
    tanko_variants.csv   — same data as a flat spreadsheet

Both files are overwritten on each run.
"""

import csv
import itertools
import json
import os
import re
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://www.tanko.com.tw"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
DELAY = 0.4          # seconds between requests — be polite
TIMEOUT = 20
MAX_RETRIES = 3

CATEGORIES = [
    "workstation", "workbench", "tool-cabinet", "cnc-tool", "rack",
    "hanger-rack", "locker", "parts-cabinet", "documents-cabinet",
    "perforated-board", "household-items",
]

session = requests.Session()
session.headers.update(HEADERS)


def get(url):
    """GET with retries and delay."""
    for attempt in range(MAX_RETRIES):
        try:
            r = session.get(url, timeout=TIMEOUT)
            r.raise_for_status()
            time.sleep(DELAY)
            return r.text
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                print(f"    ! give up on {url}: {e}")
                return None
            time.sleep(1.5 * (attempt + 1))
    return None


def find_product_detail_urls():
    """Walk every category (and its pagination) to collect product-detail URLs."""
    seen = set()
    for cat in CATEGORIES:
        page = 1
        while True:
            url = f"{BASE}/en/products/{cat}/" + (f"?page={page}" if page > 1 else "")
            print(f"  crawl {url}")
            html = get(url)
            if not html:
                break
            soup = BeautifulSoup(html, "html.parser")
            hits = 0
            for a in soup.select('a[href*="/en/products-detail/"]'):
                href = urljoin(BASE, a.get("href", "").split("?")[0])
                if href.endswith("/") and href not in seen:
                    seen.add(href)
                    hits += 1
            # Follow sub-collections too (they share the same URL pattern)
            for a in soup.select(f'a[href*="/en/products/{cat}/"]'):
                sub = urljoin(BASE, a.get("href", "").split("?")[0])
                if sub != url.split("?")[0] and sub not in seen:
                    seen.add(sub)  # mark visited so we don't loop
                    sub_html = get(sub)
                    if sub_html:
                        sub_soup = BeautifulSoup(sub_html, "html.parser")
                        for aa in sub_soup.select('a[href*="/en/products-detail/"]'):
                            href = urljoin(BASE, aa.get("href", "").split("?")[0])
                            if href.endswith("/") and href not in seen:
                                seen.add(href)
                                hits += 1
            if hits == 0 and page > 1:
                break
            page += 1
            if page > 30:  # safety cap
                break
    return sorted(u for u in seen if "/products-detail/" in u)


def parse_spec_groups(soup):
    """
    Return [{label, level, options: [{data_id, label}]}, ...]
    from the <ul class="specList"> block.
    Returns [] if the page has no configurator (single-variant product).
    """
    groups = []
    for li in soup.select("ul.specList > li"):
        cls = " ".join(li.get("class", []))
        m = re.search(r"level(\d+)", cls)
        level = int(m.group(1)) if m else len(groups) + 1
        label_el = li.find("label")
        group_label = label_el.get_text(strip=True).rstrip(":：") if label_el else f"spec{level}"
        options = []
        for item in li.select("div.item"):
            inp = item.find("input")
            lab = item.find("label")
            if not inp or not lab:
                continue
            data_id = inp.get("data-id")
            if not data_id:
                continue
            options.append({
                "data_id": data_id,
                "label": lab.get_text(strip=True),
            })
        if options:
            groups.append({"label": group_label, "level": level, "options": options})
    groups.sort(key=lambda g: g["level"])
    return groups


def extract_index_id(html):
    m = re.search(r"indexId[\"'\s:=]+(\d+)", html)
    return m.group(1) if m else None


def extract_static_specs(soup):
    """Pull the static Specification / description block (dimensions, material, load...)."""
    spec_text_parts = []
    for sel in ["div.introBox", "div.tabContent", "div#tabContent2", "div.specification"]:
        for el in soup.select(sel):
            t = el.get_text("\n", strip=True)
            if t:
                spec_text_parts.append(t)
    text = "\n".join(spec_text_parts)

    def grab(pat):
        m = re.search(pat, text, re.I)
        return m.group(1).strip() if m else ""

    return {
        "dimensions": grab(r"Dimensions?\s*[:：]\s*([^\n]+)"),
        "material": grab(r"Material\s*[:：]\s*([^\n]+)"),
        "load_capacity": grab(r"Load(?:ing)?\s*(?:capacity|weight)\s*[:：]\s*([^\n]+)"),
        "raw_snippet": text[:600],
    }


def fetch_model_no(index_id, combo):
    """
    combo is a list of data_id strings in level order.
    Endpoint uses package1Id, package2Id, ... in level order.
    Returns the resolved Model No. string, or None.
    """
    params = [f"act=8", f"indexId={index_id}"]
    for i, data_id in enumerate(combo, start=1):
        params.append(f"package{i}Id={data_id}")
    url = f"{BASE}/en/products/act/?" + "&".join(params)
    html = get(url)
    if not html:
        return None
    m = re.search(r'<span class="text">\s*([^<]+?)\s*</span>', html)
    return m.group(1).strip() if m else None


def fetch_variant_images(index_id, combo):
    params = [f"indexId={index_id}"]
    for i, data_id in enumerate(combo, start=1):
        params.append(f"package{i}Id={data_id}")
    url = f"{BASE}/en/products-item/?" + "&".join(params)
    html = get(url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    imgs = []
    for li in soup.select("ul.albumListMain li.albumItem"):
        src = li.get("data-src") or (li.find("img") or {}).get("src")
        if src:
            imgs.append(src)
    return imgs


def scrape_product(url):
    html = get(url)
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")

    index_id = extract_index_id(html)
    groups = parse_spec_groups(soup)
    static_specs = extract_static_specs(soup)

    # Product family name + category from breadcrumb / title
    title_el = soup.select_one("h1.articleTitle") or soup.find("h1")
    family = title_el.get_text(strip=True) if title_el else ""
    breadcrumb = " > ".join(
        a.get_text(strip=True) for a in soup.select("nav.breadcrumb a, .breadcrumb a, .breadcrumb li")
    )
    slug = url.rstrip("/").rsplit("/", 1)[-1]

    result = {
        "url": url,
        "slug": slug,
        "family": family,
        "breadcrumb": breadcrumb,
        "index_id": index_id,
        "static_specs": static_specs,
        "spec_groups": groups,
        "variants": [],
    }

    # No spec groups → single-variant page. Grab the visible Model No.
    if not groups:
        m = re.search(r"Model No\.\s*([A-Za-z0-9\-□/]+)", html)
        model = m.group(1) if m else None
        result["variants"].append({
            "model_no": model,
            "combo_labels": {},
            "images": [],
        })
        return result

    if not index_id:
        print(f"    ! no indexId on {url}, skipping variant expansion")
        return result

    # Cross-product of all levels
    option_lists = [g["options"] for g in groups]
    group_labels = [g["label"] for g in groups]
    total = 1
    for opts in option_lists:
        total *= len(opts)
    print(f"    {slug}: {len(groups)} spec group(s), {total} combinations")

    invalid = 0
    for combo in itertools.product(*option_lists):
        data_ids = [opt["data_id"] for opt in combo]
        combo_labels = {group_labels[i]: combo[i]["label"] for i in range(len(combo))}
        model_no = fetch_model_no(index_id, data_ids)
        # Empty response = Tanko doesn't sell this combination (e.g. Stainless
        # Steel only offered in the smallest KQ-3 size). Skip it.
        if not model_no:
            invalid += 1
            continue
        images = fetch_variant_images(index_id, data_ids)
        result["variants"].append({
            "model_no": model_no,
            "sku_id": normalize_sku_id(model_no),
            "combo_labels": combo_labels,
            "data_ids": data_ids,
            "images": images,
        })
    if invalid:
        print(f"      ({invalid} combinations not offered — skipped)")

    return result


def normalize_sku_id(model_no):
    """
    Return the SKU string in the same format as the local image filenames
    under assets/product/. Confirmed by inspection:
        'KQ-306A (Black)'   matches  'KQ-306A (Black).png'    (space before '(')
        'RY-04SA'           matches  'RY-04SA.png'
        'FBA-204AW'         matches  'FBA-204AW.png'
    So we just trim whitespace, no other transformation needed.
    """
    return (model_no or "").strip()


def canonical_sku(s):
    """
    Reduce a SKU or filename stem to a lookup key that survives every
    naming convention actually used under assets/product/:
        'RY-01SA'                 -> 'ry01sa'
        'KQ-306A (Black)'         -> 'kq306ablack'
        'KQ-306A (Black).png'     -> 'kq306ablack'   (via os.path.splitext)
        'EKB-308AM-blue'          -> 'ekb308amblue'
        'EKB-308AM (Blue)'        -> 'ekb308amblue'
        'FBA-204W'                -> 'fba204w'
    Anything that isn't a letter or digit is stripped, then lowercased.
    """
    return re.sub(r"[^0-9a-zA-Z]+", "", s or "").lower()


def build_candidate_skus(model_no, combo_labels):
    """
    Return every candidate SKU string worth trying against the image index.
    Handles the case where Tanko's model_no doesn't reflect a spec dimension
    (like color for EGL/EKB pages) but the local image filename does.

    Formats tried, per spec-label value:
        '{model} ({Value})'      — 'KQ-306A (Black)'
        '{model}({Value})'       — 'KQ-306A(Black)'
        '{model} ({VALUE})'      — 'EGL-185M (BLACK)'
        '{model}({VALUE})'       — 'EGL-185M(BLACK)'
        '{model}-{value}'        — 'EKB-308AM-blue'
        '{model}-{value-slug}'   — 'EKC-220M-ta-112'  (spaces / parens -> hyphens)
    Plus all pairwise combinations of spec-label values (color + accessory).
    """
    base = (model_no or "").strip()
    if not base:
        return []
    values = [str(v).strip() for v in (combo_labels or {}).values() if v]
    candidates = [base]

    # Abbreviations seen in local image filenames vs Tanko's spec labels
    ABBREV = {
        "stainless steel": ["S STEEL", "SS", "S-STEEL", "STAINLESS"],
        "stainless steel(s)": ["S STEEL", "SS"],
        "stainless": ["S STEEL", "SS"],
    }

    def suffixes(val):
        v = val.strip()
        if not v:
            return []
        # If the value itself embeds a "(colour)" tail like 'EGL-185M (black)',
        # peel just the inner token and use that as the suffix.
        m = re.match(r"^(.+?)\s*\(([^)]+)\)\s*$", v)
        inner_tail = m.group(2) if m else None
        slug = re.sub(r"[^0-9a-zA-Z]+", "-", v.lower()).strip("-")
        out = [
            f"{base} ({v})",
            f"{base}({v})",
            f"{base} ({v.upper()})",
            f"{base}({v.upper()})",
            f"{base}-{v.lower()}",
            f"{base}-{slug}",
            v,
        ]
        if inner_tail:
            out += [
                f"{base}({inner_tail})",
                f"{base} ({inner_tail})",
                f"{base}({inner_tail.upper()})",
                f"{base} ({inner_tail.upper()})",
                f"{base}-{inner_tail.lower()}",
            ]
        # Abbreviation aliases (e.g. 'Stainless steel' -> 'S STEEL')
        for abbr in ABBREV.get(v.lower(), []):
            out += [
                f"{base} ({abbr})",
                f"{base}({abbr})",
                f"{base}-{abbr.lower().replace(' ','-')}",
            ]
        return out

    for val in values:
        candidates.extend(suffixes(val))
    # Try pairwise for pages with color + accessory (or size + color)
    for i in range(len(values)):
        for j in range(len(values)):
            if i == j:
                continue
            v1_slug = re.sub(r"[^0-9a-zA-Z]+", "-", values[i].lower()).strip("-")
            v2_slug = re.sub(r"[^0-9a-zA-Z]+", "-", values[j].lower()).strip("-")
            candidates.append(f"{base}-{v1_slug}-{v2_slug}")
            candidates.append(f"{base}({values[i]})({values[j]})")
            candidates.append(f"{base} ({values[i]}) ({values[j]})")
    return candidates


def load_image_index(image_dir):
    """Map canonical stem -> full path, so we can cross-reference SKUs."""
    if not image_dir or not os.path.isdir(image_dir):
        return {}
    idx = {}
    for name in os.listdir(image_dir):
        stem, _ext = os.path.splitext(name)
        key = canonical_sku(stem)
        if key and key not in idx:
            idx[key] = os.path.join(image_dir, name)
    return idx


def flatten_for_csv(products):
    rows = []
    for p in products:
        for v in p["variants"]:
            rows.append({
                "sku_id": v.get("sku_id") or "",
                "model_no": v.get("model_no") or "",
                "family": p["family"],
                "slug": p["slug"],
                "url": p["url"],
                "combo": json.dumps(v.get("combo_labels", {}), ensure_ascii=False),
                "dimensions": p["static_specs"].get("dimensions", ""),
                "material": p["static_specs"].get("material", ""),
                "load_capacity": p["static_specs"].get("load_capacity", ""),
                "image_count": len(v.get("images", [])),
                "first_image": (v.get("images") or [""])[0],
                "local_image": v.get("local_image", ""),
            })
    return rows


def annotate_with_local_images(products, image_index):
    """
    For each variant, attach:
        local_image        — path to the matching file in assets/product/, or ""
        local_image_match  — 'exact' | 'case-insensitive' | 'missing'
    Also returns two orphan lists.
    """
    matched_keys = set()
    # Build a secondary index that also groups '(1)', '(2)' angle-shot suffixes
    # by their base key, so we can attach them as extra images.
    extras_index = {}
    for stem_lower, path in image_index.items():
        base = re.sub(r"\d+$", "", stem_lower)  # canonical form already stripped parens
        if base and base != stem_lower:
            extras_index.setdefault(base, []).append(path)

    for p in products:
        for v in p["variants"]:
            candidates = build_candidate_skus(
                v.get("model_no") or v.get("sku_id"),
                v.get("combo_labels", {}),
            )
            hit_key, hit_path = "", ""
            for cand in candidates:
                k = canonical_sku(cand)
                if k and k in image_index:
                    hit_key, hit_path = k, image_index[k]
                    break
            v["local_image"] = hit_path
            v["local_image_match"] = "matched" if hit_path else "missing"
            # Attach extra-angle photos that share the same base
            if hit_key:
                matched_keys.add(hit_key)
                extras = extras_index.get(hit_key, [])
                if extras:
                    v["local_image_extras"] = extras
                    for ep in extras:
                        matched_keys.add(canonical_sku(os.path.splitext(os.path.basename(ep))[0]))

    all_scraped_keys = set()
    for p in products:
        for v in p["variants"]:
            for cand in build_candidate_skus(v.get("model_no") or v.get("sku_id"), v.get("combo_labels", {})):
                all_scraped_keys.add(canonical_sku(cand))
    orphan_images = sorted(
        os.path.basename(path) for key, path in image_index.items()
        if key not in all_scraped_keys
    )
    missing_images = sorted(
        v.get("sku_id") for p in products for v in p["variants"]
        if v.get("local_image_match") == "missing" and v.get("sku_id")
    )
    return matched_keys, orphan_images, missing_images


def safe_write(path, writer_fn):
    """
    Write via writer_fn(f). If `path` is locked (e.g. open in Excel), fall
    back to a numbered sibling instead of crashing.
    """
    for candidate in [path] + [
        f"{os.path.splitext(path)[0]}_{i}{os.path.splitext(path)[1]}"
        for i in range(1, 20)
    ]:
        try:
            with open(candidate, "w", encoding="utf-8", newline="") as f:
                writer_fn(f)
            return candidate
        except PermissionError:
            continue
    raise PermissionError(f"Could not write to {path} or any fallback name")


def main():
    cwd = os.getcwd()
    out_json = os.path.join(cwd, "tanko_variants.json")
    out_csv = os.path.join(cwd, "tanko_variants.csv")
    print(f"Running from: {cwd}")
    print(f"Output JSON:  {out_json}")
    print(f"Output CSV:   {out_csv}")

    # Optional smoke-test mode: `python tanko_variant_scraper.py test`
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        product_urls = [
            f"{BASE}/en/products-detail/ry/",
            f"{BASE}/en/products-detail/locker-white/",
            f"{BASE}/en/products-detail/was-57042/",
        ]
        print(f"\n[SMOKE TEST] Only scraping {len(product_urls)} known pages.")
    else:
        print("\n== Step 1: discover product-detail URLs across all categories ==")
        product_urls = find_product_detail_urls()
        print(f"  found {len(product_urls)} product-detail pages")

    print("\n== Step 2: expand every variant per page ==")
    products = []
    for i, url in enumerate(product_urls, 1):
        print(f"[{i}/{len(product_urls)}] {url}")
        data = scrape_product(url)
        if data:
            products.append(data)
        # Incremental save — safe against crashes
        if i % 10 == 0 or i == len(product_urls):
            with open(out_json, "w", encoding="utf-8") as f:
                json.dump(products, f, ensure_ascii=False, indent=2)

    # Cross-reference against the local image folder if present
    image_dir = os.path.join(cwd, "assets", "product")
    image_index = load_image_index(image_dir)
    if image_index:
        print(f"\n== Step 3: cross-reference against {len(image_index)} local images ==")
        matched, orphan_images, missing_images = annotate_with_local_images(products, image_index)
        print(f"  matched  : {len(matched)}")
        print(f"  missing  : {len(missing_images)}  (SKUs on Tanko with no image on disk)")
        print(f"  orphans  : {len(orphan_images)}  (images on disk with no SKU from Tanko)")
        safe_write(
            os.path.join(cwd, "tanko_image_audit.json"),
            lambda f: json.dump(
                {"missing_images": missing_images, "orphan_images": orphan_images},
                f, ensure_ascii=False, indent=2,
            ),
        )
    else:
        print(f"\n(no image folder found at {image_dir} — skipping cross-reference)")

    saved_json = safe_write(out_json, lambda f: json.dump(products, f, ensure_ascii=False, indent=2))

    rows = flatten_for_csv(products)
    default_cols = [
        "sku_id", "model_no", "family", "slug", "url", "combo",
        "dimensions", "material", "load_capacity",
        "image_count", "first_image", "local_image",
    ]
    def write_csv(f):
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else default_cols)
        w.writeheader()
        w.writerows(rows)
    saved_csv = safe_write(out_csv, write_csv)

    total_variants = sum(len(p["variants"]) for p in products)
    print(f"\nDone.  {len(products)} product pages  ->  {total_variants} total variants")
    print(f"        {saved_json}")
    print(f"        {saved_csv}")


if __name__ == "__main__":
    main()
