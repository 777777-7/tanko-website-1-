# -*- coding: utf-8 -*-
"""
Rewrite products.json so its category / sub-category structure MIRRORS
tanko.com.tw exactly (11 categories, each with tanko's sub-collections in
tanko's order). Uses listing_products.json as the authoritative structure.

Keeps asset3 image_paths, specs, attributes, distinct_title. Re-orders rows to
tanko order (category -> sub-collection -> family -> variant) so the site build
renders them arranged like tanko.
"""
import json, os, re
from collections import OrderedDict

ROOT = os.path.dirname(os.path.abspath(__file__))

# tanko categories in tanko order: slug -> display name
TANKO_CATS = OrderedDict([
    ("workstation",       "Modular Workstation"),
    ("workbench",         "Workbench"),
    ("tool-cabinet",      "Tool Cabinet"),
    ("cnc-tool",          "CNC Tool Storage"),
    ("rack",              "Rack"),
    ("hanger-rack",       "Hanger Rack"),
    ("locker",            "Locker"),
    ("parts-cabinet",     "Parts Cabinet"),
    ("documents-cabinet", "Documents Cabinet"),
    ("perforated-board",  "Perforated Board"),
    ("household-items",   "Household Items"),
])
CAT_ORDER = {c: i for i, c in enumerate(TANKO_CATS)}


def main():
    listing = json.load(open(os.path.join(ROOT, "listing_products.json"), encoding="utf-8"))
    products = json.load(open(os.path.join(ROOT, "products.json"), encoding="utf-8"))

    # family_slug -> listing record (+ tanko order index)
    L = {}
    sub_order = {}  # (cat, sub) -> order index (first-appearance = tanko order)
    for i, r in enumerate(listing):
        r["_order"] = i
        L[r["slug"]] = r
        cat = r["category"]
        for s in r["subcollections"]:
            if s == "All":
                continue
            key = (cat, s)
            if key not in sub_order:
                sub_order[key] = len(sub_order)

    def primary_sub(rec):
        for s in rec["subcollections"]:
            if s != "All":
                return s
        return None

    unmatched = []
    for p in products:
        fs = p.get("family_slug")
        rec = L.get(fs)
        if not rec:
            unmatched.append(p["sku"])
            continue
        cat = rec["category"]
        sub = primary_sub(rec)
        p["category"] = TANKO_CATS.get(cat, cat)
        p["category_slug"] = cat
        p["subcategory"] = sub
        # distinct title from listing (cleaned of full-width pipe SKU tail)
        dt = re.split(r"[|｜]", rec.get("distinct_title") or "")[0].strip()
        if dt and dt.lower() != (rec.get("group_title") or "").lower() and not re.fullmatch(r"[A-Z0-9/\-]{2,10}", dt):
            p["distinct_title"] = dt
        else:
            p.pop("distinct_title", None)
        p["_cat_order"] = CAT_ORDER.get(cat, 99)
        p["_sub_order"] = sub_order.get((cat, sub), -1)
        p["_fam_order"] = rec["_order"]

    # sort: category -> sub-collection -> family (tanko order); stable keeps variant order
    products.sort(key=lambda p: (p.get("_cat_order", 99), p.get("_sub_order", -1),
                                 p.get("_fam_order", 0)))
    for p in products:
        for k in ("_cat_order", "_sub_order", "_fam_order"):
            p.pop(k, None)

    # backup + write
    bak = os.path.join(ROOT, "products.json.prestructure.bak")
    if not os.path.exists(bak):
        json.dump(json.load(open(os.path.join(ROOT, "products.json"), encoding="utf-8")),
                  open(bak, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(products, open(os.path.join(ROOT, "products.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # report
    from collections import Counter, defaultdict
    cat_fam = defaultdict(set)
    for p in products:
        if p.get("family_slug"):
            cat_fam[p["category_slug"]].add(p["family_slug"])
    print("Restructured products.json ->", len(products), "rows; unmatched:", len(unmatched))
    print("\nFamilies per tanko category:")
    for c in TANKO_CATS:
        fams = cat_fam.get(c, set())
        subs = OrderedDict()
        for p in products:
            if p["category_slug"] == c and p.get("family_slug"):
                subs.setdefault(p.get("subcategory") or "(none)", set()).add(p["family_slug"])
        print(f"  {c:18s} {len(fams):3d} families")
        for s, sf in subs.items():
            print(f"        - {s:24s} {len(sf)} families")


if __name__ == "__main__":
    main()
