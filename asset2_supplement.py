# -*- coding: utf-8 -*-
"""
Supplemental pass: scrape the product families that the earlier variant scrape
MISSED (found via listing_products.json cross-check) and fold their images into
/asset2/ with the same naming convention. Also refresh the audit reports so the
new SKUs show up as the real gap.

Does NOT modify products.json or the site build.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from tanko_variant_scraper import scrape_product, BASE
from asset2_build import (plan_filenames, download_all, classify, canon,
                          group_by_sku, sanitize)

MISSING_SLUGS = ["rfa_rfb", "sa_k", "te_211", "wkt_5102", "wp-9_1"]


def main():
    listing = {r["slug"]: r for r in json.load(open(os.path.join(ROOT, "listing_products.json"), encoding="utf-8"))}
    products_json = json.load(open(os.path.join(ROOT, "products.json"), encoding="utf-8"))
    pj_canon = {canon(r["sku"]) for r in products_json}

    print("== scrape missed families ==")
    scraped = []
    for slug in MISSING_SLUGS:
        url = f"{BASE}/en/products-detail/{slug}/"
        print(f"  {slug} ...")
        data = scrape_product(url)
        if not data:
            print(f"    ! failed {slug}")
            continue
        info = listing.get(slug, {})
        subs = set(info.get("subcollections", []))
        kind, basis = classify(slug, data.get("family", ""), subs)
        data["_kind"] = kind
        data["_basis"] = basis
        data["_distinct_title"] = info.get("distinct_title", "")
        data["_subcollections"] = sorted(subs)
        n = len(data.get("variants", []))
        print(f"    family={data.get('family')!r} distinct={info.get('distinct_title')!r} "
              f"kind={kind} variants={n}")
        scraped.append(data)

    # persist full scraped records so the merge step has dimensions/specs/variants
    json.dump(scraped, open(os.path.join(ROOT, "missed_families_full.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n== download images to /asset2/ ==")
    plans = []
    for p in scraped:
        plans.extend(plan_filenames(p))
    saved, variation_files = download_all(plans)
    print(f"  planned {len(plans)}  saved/exists {saved}  variation-flagged {len(variation_files)}")

    # new SKUs from these families
    new_skus = []
    for p in scraped:
        for sku, entries in group_by_sku(p).items():
            if canon(sku) not in pj_canon:
                new_skus.append({
                    "sku": sku, "kind": p["_kind"], "family": p.get("family", ""),
                    "distinct_title": p.get("_distinct_title", ""),
                    "subcollections": p.get("_subcollections", []),
                    "url": p["url"], "n_images": sum(len(v.get("images", [])) for v in entries),
                })

    # merge into new_products.json (append, de-dup by sku)
    np_path = os.path.join(ROOT, "new_products.json")
    existing = json.load(open(np_path, encoding="utf-8")) if os.path.exists(np_path) else []
    have = {canon(r["sku"]) for r in existing}
    for r in new_skus:
        if canon(r["sku"]) not in have:
            existing.append(r); have.add(canon(r["sku"]))
    json.dump(existing, open(np_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("\n== supplemental report ==")
    print(f"  families scraped: {len(scraped)}")
    print(f"  NEW SKUs added (not in products.json): {len(new_skus)}")
    print(f"  images added to /asset2/: {saved}")
    print(f"  new_products.json now holds: {len(existing)} rows")
    print("\n  new SKUs:")
    for r in new_skus:
        print(f"    {r['sku']:16s} [{r['kind']}] {r['family']} / {r['distinct_title']}  ({r['n_images']} imgs)")


if __name__ == "__main__":
    main()
