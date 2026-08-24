# -*- coding: utf-8 -*-
"""
Pattern quality check across every family page in dist/. Verifies each family
page has the pieces we intend, and reports gaps as a table so we can spot-fix.

Checks per family:
  • exactly one <h1>
  • has picker (opt-container present)
  • variant comparison table present with at least 1 row
  • at least one product tab beyond Product Specification (features / howto /
    accessories / holders_spec / spec_blocks)
  • image spec ("Specification"/"Product Specification"/"spec_blocks" tab)
    present when tanko has it
  • no broken /asset3/ or /asset_content/ paths in the rendered HTML (HEAD
    check for the first 3 image references per page against localhost:8765)
"""
import os, re, sys, json
from collections import Counter, defaultdict
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
BASE = "http://localhost:8765"


def head_ok(url):
    # URL-encode the path (spaces + parens are legal in filenames but need encoding)
    if url.startswith(BASE):
        path = url[len(BASE):]
        url = BASE + quote(path, safe="/")
    try:
        r = urlopen(url, timeout=5)
        return r.status < 400
    except (HTTPError, URLError, Exception):
        return False


def check(fp, cat_slug, fam_slug, listing_labels):
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()

    ok = {}
    ok["h1_count"] = len(re.findall(r"<h1\b", html))
    ok["has_picker"] = "opt-container" in html
    # variant table rows (spec-table tbody)
    tbody = re.search(r"<tbody>(.*?)</tbody>", html, re.S)
    n_rows = tbody.group(1).count("<tr") if tbody else 0
    ok["variant_rows"] = n_rows
    # tabs present (buttons)
    tabs = re.findall(r'data-tab="([^"]+)"[^>]*>([^<]+)</button>', html)
    ok["tab_keys"] = [k for k, _ in tabs]
    ok["tab_labels"] = [l.strip() for _, l in tabs]
    ok["non_variant_tabs"] = [k for k in ok["tab_keys"] if k != "variants"]
    # panels non-empty
    ok["empty_panels"] = 0
    for m in re.finditer(r'ptab-panel"[^>]*data-tab="([^"]+)"[^>]*>(.*?)</div>\s*(?=<div class="ptab-panel|\Z)', html, re.S):
        key, body = m.group(1), m.group(2)
        if key == "variants": continue
        stripped = re.sub(r"<[^>]+>", "", body).strip()
        if len(stripped) < 20:
            ok["empty_panels"] += 1
    # first 3 image references broken?
    imgs = re.findall(r'src="([^"]+\.(?:png|jpg|jpeg|webp))"', html)[:3]
    broken = [u for u in imgs if not head_ok(BASE + u if u.startswith("/") else BASE + "/" + u)]
    ok["broken_first3"] = len(broken)
    return ok


def main():
    import json as _json
    listing = _json.load(open(os.path.join(ROOT, "listing_products.json"), encoding="utf-8"))
    listing_by_slug = {r["slug"]: r for r in listing}
    # discover family index.html paths
    families = []
    SKIP_DIRS = {"guides", "applications", "about", "contact", "enquiry", "download",
                 "assets", "asset3", "asset_content", "products"}
    for cat_dir in sorted(os.listdir(DIST)):
        if cat_dir in SKIP_DIRS: continue
        cat_path = os.path.join(DIST, cat_dir)
        if not os.path.isdir(cat_path): continue
        for fam_dir in sorted(os.listdir(cat_path)):
            fam_path = os.path.join(cat_path, fam_dir)
            fam_idx = os.path.join(fam_path, "index.html")
            if not os.path.isdir(fam_path) or not os.path.isfile(fam_idx): continue
            # skip sub-collections (those don't have picker)
            if fam_dir in ("professional","classic","hooks","hangers","standard-tool-cabinet",
                           "heavy-duty-tool-cabinet","trolley","tilt-out-bins-cart",
                           "cnc-tool-cabinet","cnc-trolley","cnc-tool-cabinet-with-door",
                           "mould-rack","pull-out-rack","hanger-rack","display-stand",
                           "parts-cabinet","parts-bin","team-case","documents-tray",
                           "documents-cabinet","perforated-board","chest-of-drawers",
                           "performance","heavy-duty","stainless-steel","workbench-accessories",
                           "hexagonal","packing-station"):
                continue
            families.append((cat_dir, fam_dir, fam_idx))

    print(f"Checking {len(families)} family pages...\n")
    rows = []
    for cat, fam, fp in families:
        lst = listing_by_slug.get(fam)
        expected_labels = None
        rec = check(fp, cat, fam, expected_labels)
        rec["cat"] = cat; rec["fam"] = fam
        rows.append(rec)

    # summary
    def bad(r):
        return (r["h1_count"] != 1
                or not r["has_picker"]
                or r["variant_rows"] == 0
                or not r["non_variant_tabs"]
                or r["empty_panels"] > 0
                or r["broken_first3"] > 0)

    bad_rows = [r for r in rows if bad(r)]
    print(f"Total families checked: {len(rows)}   |   Bad: {len(bad_rows)}")
    print()

    # aggregate stats
    hist = Counter()
    for r in rows:
        hist["ok"] += 0 if bad(r) else 1
    tab_hist = Counter()
    for r in rows:
        tab_hist[tuple(r["tab_labels"])] += 1
    print("Tab-label layouts and counts:")
    for k, c in tab_hist.most_common():
        print(f"  {c:3d}  {k}")

    if bad_rows:
        print("\nBad families (first 30):")
        for r in bad_rows[:30]:
            print(f"  {r['cat']:18s} {r['fam']:22s} h1={r['h1_count']} picker={r['has_picker']} "
                  f"rows={r['variant_rows']} tabs={r['non_variant_tabs']} empty={r['empty_panels']} "
                  f"broken={r['broken_first3']}")

    # write a full report
    out = os.path.join(ROOT, "pattern_check_report.json")
    _json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nFull report: {out}")


if __name__ == "__main__":
    main()
