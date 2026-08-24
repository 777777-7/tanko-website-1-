# -*- coding: utf-8 -*-
"""
NEW MISSION — /asset2/ full image extraction + catalog completeness audit.

Reuses tanko_variants.json (already scraped: every page, variant, SKU and its
live image URLs) so we do NOT re-hammer the AJAX endpoints. Adds:

  1. Mother/accessory classification from live PAGE STRUCTURE — by re-crawling
     each category and its sub-collections (e.g. perforated-board/hooks/,
     /hanger/). Items under hook/hanger/holder/accessory sub-collections are
     accessories; boards/benches/cabinets are mother products. Family-name
     keywords are a recorded fallback. Every item records classification_basis.
  2. Download EVERY image (all angles) for every SKU into /asset2/ with the
     required filename convention.
  3. Cross-reference against products.json ->
       new_products.json, image_mismatches.json, accessories_found.json
  4. Print the STEP-4 report. Does NOT touch products.json or the site build.

Usage:
    python asset2_build.py            # full run
    python asset2_build.py test       # small smoke test (few pages, ~few imgs)
"""

import io
import json
import os
import re
import shutil
import sys
import time
from collections import defaultdict, OrderedDict

import requests
from bs4 import BeautifulSoup
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSET2 = os.path.join(ROOT, "asset2")
VARIANTS = os.path.join(ROOT, "tanko_variants.json")
PRODUCTS = os.path.join(ROOT, "products.json")

BASE = "https://www.tanko.com.tw"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
           "Accept-Language": "en-US,en;q=0.9"}
DELAY = 0.35
TIMEOUT = 25
session = requests.Session()
session.headers.update(HEADERS)

CATEGORIES = ["workstation", "workbench", "tool-cabinet", "cnc-tool", "rack",
              "hanger-rack", "locker", "parts-cabinet", "documents-cabinet",
              "perforated-board", "household-items"]

# Sub-collection / family name tokens that mark an ACCESSORY (add-on/component).
ACCESSORY_TOKENS = [
    "hook", "hanger", "holder", "accessor", "bin", "caster", "castor", "wheel",
    "light", "lamp", "panel", "vise", "vice", "arm", "tray", "seat", "stool",
    "mat", "divider", "division", "latch", "socket", "leveler", "leveller",
    "clip", "drill", "screwdriver", "wrench", "bottle", "peg",
]
# Sub-collections that are explicitly mother products even if a token matches.
MOTHER_OVERRIDE_TOKENS = ["board", "bench", "cabinet", "locker", "rack", "workstation",
                          "trolley", "cart", "mould", "shelf", "case"]

failed = []


def get(url):
    for attempt in range(3):
        try:
            r = session.get(url, timeout=TIMEOUT)
            r.raise_for_status()
            time.sleep(DELAY)
            return r.text
        except Exception as e:
            if attempt == 2:
                failed.append({"url": url, "error": str(e)})
                return None
            time.sleep(1.2 * (attempt + 1))
    return None


def slug_of(url):
    return url.rstrip("/").rsplit("/", 1)[-1].lower()


# ---------------------------------------------------------------- classification
def crawl_subcollections():
    """
    Returns slug -> {"category":, "subcollections": set(labels)} for every
    product-detail page, discovered by walking each category and its
    sub-collection listing pages. This is the STRUCTURAL signal.
    """
    slug_map = defaultdict(lambda: {"category": None, "subcollections": set()})

    for cat in CATEGORIES:
        cat_url = f"{BASE}/en/products/{cat}/"
        html = get(cat_url)
        if not html:
            continue
        soup = BeautifulSoup(html, "html.parser")

        # sub-collection links: /en/products/{cat}/{sub}/
        subs = {}  # sub_url -> label
        for a in soup.select(f'a[href*="/en/products/{cat}/"]'):
            href = a.get("href", "").split("?")[0]
            m = re.search(rf"/en/products/{re.escape(cat)}/([a-z0-9\-]+)/?$", href)
            if m:
                sub = m.group(1)
                label = a.get_text(strip=True) or sub
                subs[urljoin_base(href)] = label

        # products directly on the category page (no sub-collection)
        for a in soup.select('a[href*="/en/products-detail/"]'):
            s = slug_of(a.get("href", "").split("?")[0])
            slug_map[s]["category"] = cat

        # each sub-collection listing
        for sub_url, label in subs.items():
            shtml = get(sub_url)
            if not shtml:
                continue
            ssoup = BeautifulSoup(shtml, "html.parser")
            for a in ssoup.select('a[href*="/en/products-detail/"]'):
                s = slug_of(a.get("href", "").split("?")[0])
                slug_map[s]["category"] = cat
                slug_map[s]["subcollections"].add(label)
        print(f"  [{cat}] subcollections: {sorted(set(subs.values()))}")

    return slug_map


def urljoin_base(href):
    if href.startswith("http"):
        return href.split("?")[0]
    return (BASE + href).split("?")[0]


def token_is_accessory(text):
    t = (text or "").lower()
    if any(mt in t for mt in MOTHER_OVERRIDE_TOKENS):
        # e.g. "Perforated Board" contains 'board' -> mother even though nearby hooks exist
        # but if it ALSO clearly names an accessory token as the primary noun, prefer accessory
        pass
    hit = next((tok for tok in ACCESSORY_TOKENS if tok in t), None)
    override = next((mt for mt in MOTHER_OVERRIDE_TOKENS if mt in t), None)
    return hit, override


def classify(slug, family, subcollections):
    """
    Returns (kind, basis). kind in {"mother_product","accessory"}.
    Priority: structural sub-collection > family keyword > mother default.
    """
    # 1) structural: any sub-collection label that is an accessory grouping
    for label in sorted(subcollections):
        hit, override = token_is_accessory(label)
        if hit and not override:
            return "accessory", f"subcollection:{label}"
        if hit and override:
            # ambiguous label (e.g. "Perforated Board") -> treat as mother
            return "mother_product", f"subcollection:{label}"
    # 2) family-name keyword
    hit, override = token_is_accessory(family)
    if hit and not override:
        return "accessory", f"family-keyword:{hit}"
    # 3) default
    return "mother_product", "mother-default"


# ---------------------------------------------------------------- naming + download
def sanitize(sku):
    s = (sku or "").strip()
    s = s.replace("/", "-").replace("\\", "-").replace("□", "").replace(":", "-")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def ext_of(url):
    m = re.search(r"\.(jpg|jpeg|png|webp)(?:\?|$)", url, re.I)
    return "." + (m.group(1).lower() if m else "jpg")


def plan_filenames(product):
    """
    For one product page, decide the /asset2/ filename for each image.
    Returns list of (sku, filename, image_url, confident_bool).

    Rule for '(variation)': if the SAME model_no is produced by more than one
    configurator combination (i.e. a spec axis like colour is NOT reflected in
    the SKU), its images can't be pinned to a specific variant -> mark
    '(variation)'. Otherwise images are confident angle shots -> _2, _3, ...
    """
    by_sku = OrderedDict()
    for v in product.get("variants", []):
        sku = sanitize(v.get("model_no") or v.get("sku_id") or "")
        if not sku:
            continue
        by_sku.setdefault(sku, []).append(v)

    out = []
    for sku, entries in by_sku.items():
        ambiguous = len(entries) > 1
        # gather unique image urls in order
        seen, urls = set(), []
        for v in entries:
            for u in v.get("images", []):
                if u and u not in seen:
                    seen.add(u); urls.append(u)
        if not urls:
            continue
        if ambiguous:
            for i, u in enumerate(urls):
                suffix = "_(variation)" + (f"_{i+1}" if i else "")
                out.append((sku, f"{sku}{suffix}{ext_of(u)}", u, False))
        else:
            for i, u in enumerate(urls):
                suffix = "" if i == 0 else f"_{i+1}"
                out.append((sku, f"{sku}{suffix}{ext_of(u)}", u, True))
    return out


def download_all(plans):
    os.makedirs(ASSET2, exist_ok=True)
    url_cache = {}   # url -> saved local path (first)
    saved = 0
    variation_files = []
    for sku, fname, url, confident in plans:
        dest = os.path.join(ASSET2, fname)
        if os.path.exists(dest):
            saved += 1
            if not confident:
                variation_files.append(fname)
            continue
        try:
            if url in url_cache and os.path.exists(url_cache[url]):
                shutil.copy(url_cache[url], dest)
            else:
                r = session.get(url, timeout=TIMEOUT)
                r.raise_for_status()
                with open(dest, "wb") as fh:
                    fh.write(r.content)
                url_cache[url] = dest
                time.sleep(DELAY)
            saved += 1
            if not confident:
                variation_files.append(fname)
        except Exception as e:
            failed.append({"url": url, "error": f"download: {e}"})
    return saved, variation_files


# ---------------------------------------------------------------- image hashing
def ahash(path):
    try:
        im = Image.open(path).convert("L").resize((8, 8))
        px = list(im.getdata())
        avg = sum(px) / len(px)
        bits = 0
        for i, p in enumerate(px):
            if p >= avg:
                bits |= (1 << i)
        return bits
    except Exception:
        return None


def hamming(a, b):
    return bin(a ^ b).count("1")


def canon(s):
    return re.sub(r"[^0-9a-z]+", "", (s or "").lower())


# ---------------------------------------------------------------- main
def main():
    test = len(sys.argv) > 1 and sys.argv[1] == "test"

    with open(VARIANTS, encoding="utf-8") as f:
        products = json.load(f)
    with open(PRODUCTS, encoding="utf-8") as f:
        products_json = json.load(f)

    if test:
        products = [p for p in products if p["slug"] in
                    ("locker-white", "ry", "kp-4")][:3] or products[:2]
        print(f"[TEST] {len(products)} pages")

    print("== classify: crawl category sub-collections (structural signal) ==")
    slug_map = {} if test else crawl_subcollections()

    # classify every page
    classified = []
    for p in products:
        s = p["slug"].lower()
        info = slug_map.get(s, {"category": None, "subcollections": set()})
        kind, basis = classify(s, p.get("family", ""), info["subcollections"])
        p["_kind"] = kind
        p["_basis"] = basis
        p["_category_crawled"] = info["category"]
        classified.append(p)

    mothers = [p for p in classified if p["_kind"] == "mother_product"]
    accessories = [p for p in classified if p["_kind"] == "accessory"]
    print(f"  mother pages: {len(mothers)}   accessory pages: {len(accessories)}")

    # process mother products BEFORE accessories (ordering requirement)
    ordered = mothers + accessories

    print("== plan filenames + download images to /asset2/ ==")
    all_plans = []
    for p in ordered:
        all_plans.extend(plan_filenames(p))
    print(f"  {len(all_plans)} image files planned")
    saved, variation_files = download_all(all_plans)
    print(f"  downloaded/exists: {saved}   variation-flagged: {len(variation_files)}")

    # ---- cross-reference against products.json
    pj_by_canon = {}
    for r in products_json:
        pj_by_canon.setdefault(canon(r["sku"]), r)

    live_skus = OrderedDict()  # canon -> {sku, kind, family, url, basis, n_images}
    for p in ordered:
        for sku, entries in group_by_sku(p).items():
            n_imgs = sum(len(v.get("images", [])) for v in entries)
            live_skus.setdefault(canon(sku), {
                "sku": sku, "kind": p["_kind"], "family": p.get("family", ""),
                "url": p["url"], "basis": p["_basis"], "n_images": n_imgs,
            })

    new_products = [v for k, v in live_skus.items() if k not in pj_by_canon]
    new_mothers = [v for v in new_products if v["kind"] == "mother_product"]
    accessories_found = [v for v in live_skus.values() if v["kind"] == "accessory"]

    # ---- image mismatches: old local image vs new /asset2 image (perceptual hash)
    mismatches = []
    compared = 0
    for r in products_json:
        if not r.get("image_paths"):
            continue
        old_rel = r["image_paths"][0]
        old_path = os.path.join(ROOT, old_rel.replace("/", os.sep))
        new_path = os.path.join(ASSET2, sanitize(r["sku"]) + ".jpg")
        if not os.path.exists(new_path):
            # try png
            alt = os.path.join(ASSET2, sanitize(r["sku"]) + ".png")
            new_path = alt if os.path.exists(alt) else None
        if not new_path or not os.path.exists(old_path):
            continue
        h_old, h_new = ahash(old_path), ahash(new_path)
        if h_old is None or h_new is None:
            continue
        compared += 1
        dist = hamming(h_old, h_new)
        if dist > 12:
            mismatches.append({
                "sku": r["sku"], "hamming": dist,
                "old_image": old_rel,
                "new_image": os.path.relpath(new_path, ROOT).replace(os.sep, "/"),
            })
    mismatches.sort(key=lambda x: -x["hamming"])

    # ---- write reports
    def dump(name, obj):
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=2)

    dump("new_products.json", new_products)
    dump("image_mismatches.json", mismatches)
    dump("accessories_found.json", accessories_found)
    dump("asset2_failed.json", failed)

    # ---- STEP 4 report
    print("\n" + "=" * 60)
    print("STEP 4 REPORT")
    print("=" * 60)
    mother_skus_live = sum(1 for v in live_skus.values() if v["kind"] == "mother_product")
    print(f"Mother-product SKUs found (live):        {mother_skus_live}")
    print(f"Mother-product SKUs already in products:  {mother_skus_live - len(new_mothers)}")
    print(f"  -> NEW mother SKUs (gap):               {len(new_mothers)}")
    print(f"Accessory SKUs found (live):             {len(accessories_found)}")
    print(f"Total live SKUs:                         {len(live_skus)}")
    print(f"products.json SKU count:                 {len(products_json)}")
    print(f"NEW SKUs total (mother+accessory):       {len(new_products)}")
    print(f"Images downloaded to /asset2/:           {saved}")
    print(f"  -> flagged '(variation)':              {len(variation_files)}")
    print(f"Image mismatches flagged (hamming>12):   {len(mismatches)}  (compared {compared})")
    print(f"Pages/URLs failed:                       {len(failed)}")
    print()
    print("Sample '(variation)' filenames:")
    for fn in variation_files[:10]:
        print("   ", fn)
    print()
    print("Reports written: new_products.json, image_mismatches.json, "
          "accessories_found.json, asset2_failed.json")


def group_by_sku(product):
    by_sku = OrderedDict()
    for v in product.get("variants", []):
        sku = sanitize(v.get("model_no") or v.get("sku_id") or "")
        if sku:
            by_sku.setdefault(sku, []).append(v)
    return by_sku


if __name__ == "__main__":
    main()
