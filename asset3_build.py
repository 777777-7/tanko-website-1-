# -*- coding: utf-8 -*-
"""
/asset3/ — re-extract product images with ATTRIBUTE-BASED variant naming.

Instead of {SKU}_(variation), name each image by the attribute that actually
distinguishes it, taken from the live combo labels:
    TA-115(Gray).jpg   TA-115(Blue).jpg
    WD-48S(Wood).jpg   WD-48S(Stainless steel).jpg
Multiple angles of the exact same variant -> _2, _3.

Built by COPYING from /asset2/ where the same image URL was already downloaded
(fast, no re-download); only URLs missing from asset2 are fetched.

Also writes asset3_images.json: {SKU: [asset3/relative/paths...]} so the site
build can fill image_paths straight from here.
"""
import json, os, re, shutil, sys, time
from collections import OrderedDict, defaultdict
import requests

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from asset2_build import plan_filenames  # settles stdout wrapping at import time
ASSET2 = os.path.join(ROOT, "asset2")
ASSET3 = os.path.join(ROOT, "asset3")
VARIANTS = os.path.join(ROOT, "tanko_variants.json")
MISSED = os.path.join(ROOT, "missed_families_full.json")

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122 Safari/537.36"})


def san(s):
    s = (s or "").strip().replace("/", "-").replace("\\", "-").replace("□", "").replace(":", "-")
    return re.sub(r"\s+", " ", s).strip()


def san_attr(s):
    # keep attribute value readable but filesystem-safe
    return re.sub(r"[\\/:*?\"<>|]", "-", (s or "").strip())


def ext_of(url):
    m = re.search(r"\.(jpg|jpeg|png|webp)(?:\?|$)", url or "", re.I)
    return "." + (m.group(1).lower() if m else "jpg")


# ---- rebuild asset2 URL->file index (old naming) so we can copy locally
def asset2_url_index():
    """Recompute the asset2 plan to map image URL -> existing asset2 file path."""
    with open(VARIANTS, encoding="utf-8") as f:
        products = json.load(f)
    if os.path.exists(MISSED):
        products = products + json.load(open(MISSED, encoding="utf-8"))
    url2path = {}
    for p in products:
        for sku, fname, url, conf in plan_filenames(p):
            fp = os.path.join(ASSET2, fname)
            if url not in url2path and os.path.exists(fp):
                url2path[url] = fp
    return url2path, products


def distinguishing_keys(entries):
    keys = []
    for e in entries:
        for k in (e.get("combo_labels") or {}).keys():
            if k not in keys and k != "Model No.":
                keys.append(k)
    return [k for k in keys if len({str((e.get("combo_labels") or {}).get(k)) for e in entries}) > 1]


def plan_v3(product):
    by_sku = OrderedDict()
    for v in product.get("variants", []):
        sku = san(v.get("model_no") or v.get("sku_id") or "")
        if sku:
            by_sku.setdefault(sku, []).append(v)
    plans = []  # (sku, fname, url)
    for sku, entries in by_sku.items():
        dkeys = distinguishing_keys(entries)
        for e in entries:
            combo = e.get("combo_labels") or {}
            suffix = "".join(f"({san_attr(combo[k])})" for k in dkeys if combo.get(k))
            seen, urls = set(), []
            for u in e.get("images", []):
                if u and u not in seen:
                    seen.add(u); urls.append(u)
            for i, u in enumerate(urls):
                fname = f"{sku}{suffix}" + (f"_{i+1}" if i else "") + ext_of(u)
                plans.append((sku, fname, u))
    return plans


def main():
    os.makedirs(ASSET3, exist_ok=True)
    url2path, products = asset2_url_index()
    print(f"asset2 URL index: {len(url2path)} urls")

    all_plans = []
    for p in products:
        all_plans.extend(plan_v3(p))
    # de-dup by filename (same sku+attr+url can recur)
    seen_f = set()
    plans = []
    for sku, fname, url in all_plans:
        if fname in seen_f:
            continue
        seen_f.add(fname); plans.append((sku, fname, url))
    print(f"planned {len(plans)} asset3 files")

    copied = downloaded = 0
    sku_images = defaultdict(list)
    for sku, fname, url in plans:
        dest = os.path.join(ASSET3, fname)
        rel = "asset3/" + fname
        if not os.path.exists(dest):
            src = url2path.get(url)
            if src and os.path.exists(src):
                shutil.copy(src, dest); copied += 1
            else:
                try:
                    r = session.get(url, timeout=25); r.raise_for_status()
                    open(dest, "wb").write(r.content); downloaded += 1
                    time.sleep(0.3)
                except Exception as e:
                    print(f"  ! {fname}: {e}"); continue
        sku_images[sku].append(rel)

    json.dump({k: v for k, v in sku_images.items()},
              open(os.path.join(ROOT, "asset3_images.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    n = len(os.listdir(ASSET3))
    variation_left = [f for f in os.listdir(ASSET3) if "(variation)" in f]
    print(f"\nasset3 files on disk: {n}")
    print(f"  copied from asset2: {copied}   downloaded fresh: {downloaded}")
    print(f"  SKUs with images:   {len(sku_images)}")
    print(f"  legacy '(variation)' files remaining (should be 0): {len(variation_left)}")
    print("\nSample attribute-named files:")
    for f in sorted(os.listdir(ASSET3)):
        if "(" in f and "variation" not in f:
            print("   ", f)
        if sorted(os.listdir(ASSET3)).index(f) > 400:
            break
    # show a few TA-115 examples specifically
    print("\nTA-115 files:")
    for f in sorted(os.listdir(ASSET3)):
        if f.startswith("TA-115"):
            print("   ", f)


if __name__ == "__main__":
    main()
