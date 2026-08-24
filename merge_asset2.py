# -*- coding: utf-8 -*-
"""
Merge plan for the /asset2/ extraction into the site data.

DEFAULT = --dry-run: computes and previews all four changes, writes
merge_preview.json, and modifies NOTHING.

Four changes:
  1. ADD  the 17 new SKUs (missed families) to products.json
  2. SWAP the 12 mismatched images -> clean /asset2/ versions
  3. APPLY distinct listing titles to product families (kills generic repeats)
  4. BUILD sub-collection SEO pages (Professional / Classic / Heavy Duty / ...)

Run:  python merge_asset2.py            # dry-run preview (safe)
      python merge_asset2.py --apply    # writes products.json.new + report
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
APPLY = "--apply" in sys.argv


def load(n): return json.load(open(os.path.join(ROOT, n), encoding="utf-8"))
def canon(s): return re.sub(r"[^0-9a-z]+", "", (s or "").lower())
def san(s): return re.sub(r"\s+", " ", (s or "").replace("/", "-").replace("□", "")).strip()


NEW_FAMILY_CAT = {
    "Professional Workstation": ("Modular Workstation", "modular-workstations", "Professional"),
    "Classic Workstation":      ("Modular Workstation", "modular-workstations", "Classic"),
    "Hanging bin":              ("Documents & Parts Cabinet", "parts-cabinets", "Hanging Bin"),
    "Packing Station":          ("Workbench", "workbenches", "Packing Station"),
    "Ultra Thin LED Light":     ("Workbench", "workbenches", "Accessories"),
}


def asset2_image_for(sku):
    base = san(sku)
    for suffix in ("", "_(variation)", "_(variation)_2"):
        for ext in (".jpg", ".png", ".jpeg", ".webp"):
            fn = base + suffix + ext
            if os.path.exists(os.path.join(ROOT, "asset2", fn)):
                return "asset2/" + fn
    return None


def clean_title(t):
    # tanko sometimes packs "Title｜SKU" with a full-width pipe; keep the title part
    return re.split(r"[|｜]", t or "")[0].strip()


def slugify(s):
    s = re.sub(r"[^\w\s-]", "", (s or "").lower())
    return re.sub(r"[\s_]+", "-", s).strip("-")


def main():
    products = load("products.json")
    missed = load("missed_families_full.json")
    mismatches = load("image_mismatches.json")
    listing = load("listing_products.json")
    listing_index = load("listing_index.json")

    pj_canon = {canon(r["sku"]) for r in products}

    # ---- 1. new SKU rows
    new_rows = []
    for p in missed:
        fam = p.get("family", "")
        cat, cat_slug, sub = NEW_FAMILY_CAT.get(fam, (None, None, None))
        fam_slug = p["slug"]
        for v in p.get("variants", []):
            sku = san(v.get("model_no") or v.get("sku_id") or "")
            if not sku or canon(sku) in pj_canon:
                continue
            combo = v.get("combo_labels", {}) or {}
            img = asset2_image_for(sku)
            new_rows.append({
                "sku": sku,
                "product_family": fam,
                "family_slug": fam_slug,
                "category": cat, "category_slug": cat_slug, "subcategory": sub,
                "color": combo.get("Color") or combo.get("Colour"),
                "dimensions": p["static_specs"].get("dimensions") or None,
                "material": combo.get("Top") or combo.get("Material") or p["static_specs"].get("material") or None,
                "load_capacity": p["static_specs"].get("load_capacity") or None,
                "attributes": {k: val for k, val in combo.items() if k not in ("Color", "Colour", "Model No.")},
                "image_paths": [img] if img else [],
                "tanko_url": p["url"],
                "evidence": {"tanko": True, "pdf": False, "image": bool(img)},
                "_source": "asset2_supplement",
            })
            pj_canon.add(canon(sku))

    # ---- 2. image swaps
    swaps = []
    for m in mismatches:
        new_img = asset2_image_for(m["sku"])
        if new_img:
            swaps.append({"sku": m["sku"], "old": m["old_image"], "new": new_img, "hamming": m["hamming"]})

    # ---- 3. distinct titles by family_slug
    listing_by_slug = {r["slug"]: r for r in listing}
    fam_slugs = {r["family_slug"] for r in products if r.get("family_slug")}
    title_updates = []
    for fs in sorted(fam_slugs):
        L = listing_by_slug.get(fs)
        if not L:
            continue
        dt = clean_title(L.get("distinct_title"))
        if dt and dt.lower() != (L.get("group_title") or "").lower():
            # flag titles that are just an uppercase SKU code (e.g. "CEA", "DA") for review
            looks_like_code = bool(re.fullmatch(r"[A-Z0-9/\-]{2,10}", dt))
            title_updates.append({"family_slug": fs, "group": L["group_title"],
                                   "distinct_title": dt, "sku_code": L["sku_code"],
                                   "review": looks_like_code})

    # ---- 4. sub-collection SEO pages
    subpages = []
    for cat, subs in listing_index.items():
        for sub, items in subs.items():
            if sub == "All":
                continue
            subpages.append({"tanko_category": cat, "subcollection": sub,
                             "slug": slugify(sub), "product_count": len(items)})

    preview = {
        "add_new_skus": new_rows,
        "image_swaps": swaps,
        "distinct_title_updates": title_updates,
        "subcollection_pages": subpages,
        "summary": {
            "new_skus": len(new_rows),
            "image_swaps": len(swaps),
            "distinct_titles": len(title_updates),
            "subcollection_pages": len(subpages),
            "products_json_before": len(products),
            "products_json_after": len(products) + len(new_rows),
        },
    }
    json.dump(preview, open(os.path.join(ROOT, "merge_preview.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    s = preview["summary"]
    print("=" * 58)
    print("MERGE PLAN — DRY RUN (nothing written to products.json/site)" if not APPLY
          else "MERGE PLAN — APPLYING")
    print("=" * 58)
    print(f"1. Add new SKUs:            {s['new_skus']}  -> products.json {s['products_json_before']} -> {s['products_json_after']}")
    print(f"2. Image swaps (mismatch): {s['image_swaps']}")
    print(f"3. Distinct-title updates: {s['distinct_titles']} families")
    print(f"4. Sub-collection pages:   {s['subcollection_pages']}")
    print()
    print("New SKUs to add:")
    for r in new_rows:
        print(f"   {r['sku']:18s} {r['category']}/{r['subcategory']:16s} {r['product_family']:24s} img={'Y' if r['image_paths'] else 'N'}")
    print("\nImage swaps (old combo-shot -> clean /asset2/):")
    for r in swaps:
        print(f"   {r['sku']:16s} h{r['hamming']}  {os.path.basename(r['old'])}  ->  {os.path.basename(r['new'])}")
    print("\nSample distinct-title updates:")
    for r in title_updates[:12]:
        print(f"   [{r['family_slug']:14s}] {r['group']:26s} -> '{r['distinct_title']}'")
    print(f"   ... {len(title_updates)} total")
    print("\nSub-collection SEO pages to build:")
    for r in subpages:
        print(f"   {r['tanko_category']:16s}/{r['slug']:24s} ({r['product_count']} products)")

    print("\nPreview written: merge_preview.json")
    if APPLY:
        apply_merge(products, new_rows, swaps, title_updates)


def apply_merge(products, new_rows, swaps, title_updates):
    # accessory SKU set (from live-site classification) — used for ordering
    acc = load("accessories_found.json")
    acc_canon = {canon(r["sku"]) for r in acc}
    for r in new_rows:
        # TE-211 etc. carry their kind via the missed-families classification
        pass
    acc_canon |= {canon(r["sku"]) for r in new_rows
                  if r["product_family"] in ("Hanging bin",)}  # TE-211 -> accessory

    swap_by_canon = {canon(s["sku"]): s["new"] for s in swaps}
    # (a) only NON-flagged (clean) distinct titles
    title_by_slug = {t["family_slug"]: t["distinct_title"]
                     for t in title_updates if not t.get("review")}

    applied_swaps = applied_titles = 0
    def enrich(r):
        nonlocal applied_swaps, applied_titles
        c = canon(r["sku"])
        if c in swap_by_canon:
            r["image_paths"] = [swap_by_canon[c]] + [p for p in r.get("image_paths", []) if p != swap_by_canon[c]]
            applied_swaps += 1
        if r.get("family_slug") in title_by_slug:
            r["distinct_title"] = title_by_slug[r["family_slug"]]
            applied_titles += 1
        r["product_type"] = "accessory" if c in acc_canon else "mother_product"
        return r

    all_rows = [enrich(r) for r in products] + \
               [enrich({k: v for k, v in r.items() if k != "_source"}) for r in new_rows]

    # ORDER: mother products first, then accessories (stable within each group)
    mothers = [r for r in all_rows if r["product_type"] == "mother_product"]
    accessories = [r for r in all_rows if r["product_type"] == "accessory"]
    merged = mothers + accessories

    json.dump(merged, open(os.path.join(ROOT, "products.json.new"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"\nAPPLIED -> products.json.new")
    print(f"  total rows:        {len(merged)}  ({len(mothers)} mother + {len(accessories)} accessory)")
    print(f"  image swaps done:  {applied_swaps}")
    print(f"  titles applied:    {applied_titles}  (clean only; {sum(1 for t in title_updates if t.get('review'))} code-like skipped)")
    print(f"  ordering:          mother products first, accessories last")
    print(f"  (products.json UNCHANGED — review products.json.new, then rename to go live)")


if __name__ == "__main__":
    main()
