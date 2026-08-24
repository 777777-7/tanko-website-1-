# -*- coding: utf-8 -*-
"""
Re-parse the Specification tab for families whose spec_blocks came out with
model_no but no dims/material/items — this happens where tanko's spec is
rendered as a TABLE (columns = SKUs, rows = attributes) rather than as a
per-SKU contentBuilder.

Merges richer spec_blocks back into product_content_v2.json.
"""
import json, os, re, sys, time
import requests
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "product_content_v2.json")
LISTING = os.path.join(ROOT, "listing_products.json")
IMG_ROOT = os.path.join(ROOT, "asset_content")
H = {"User-Agent": "Mozilla/5.0 Chrome/122 Safari/537.36"}
DELAY = 0.2
session = requests.Session(); session.headers.update(H)


def get(url):
    for a in range(3):
        try:
            r = session.get(url, timeout=25); r.raise_for_status()
            time.sleep(DELAY); return r.text
        except Exception:
            time.sleep(1.0 * (a + 1))
    return None


def clean(s):
    return re.sub(r"\s+", " ", s or "").strip(" ：:·|｜")


def ext_of(u):
    m = re.search(r"\.(jpg|jpeg|png|webp)(?:\?|$)", u or "", re.I)
    return "." + (m.group(1).lower() if m else "jpg")


def download(url, dest):
    if os.path.exists(dest): return True
    if not url: return False
    try:
        r = session.get(url, timeout=25); r.raise_for_status()
        open(dest, "wb").write(r.content); time.sleep(DELAY); return True
    except Exception: return False


SKU_RE = re.compile(r"^[A-Z][A-Z0-9\-/□]{2,20}$")


def parse_spec_tables(container, slug, tag):
    """Parse spec tables: header row = SKU columns, subsequent rows = attributes.
    Returns one block per SKU column with attributes flattened into a body-like
    text and a matching image (from the same or nearest contentBuilder)."""
    blocks_by_sku = {}
    # 1) Walk contentBuilders and, whenever we see a table with SKU headers,
    # produce spec entries.
    n_img = 0
    for cb in container.find_all("div", class_="contentBuilder", recursive=False):
        img_el = cb.find("img")
        img_local = None
        if img_el:
            src = img_el.get("data-src") or img_el.get("src") or ""
            n_img += 1
            fn = f"{tag}_tbl{n_img}{ext_of(src)}"
            if src and download(src, os.path.join(IMG_ROOT, slug, fn)):
                img_local = f"asset_content/{slug}/{fn}"

        for tbl in cb.find_all("table"):
            rows = []
            for tr in tbl.find_all("tr"):
                rows.append([clean(td.get_text(" ", strip=True)) for td in tr.find_all(["th","td"])])
            if not rows or len(rows) < 2:
                continue
            # Header: find the row that contains multiple SKU-like cells
            header_idx = None
            for i, r in enumerate(rows):
                skus_here = [c for c in r if SKU_RE.match(c)]
                if len(skus_here) >= 2:
                    header_idx = i; break
                # single-SKU header still counts if next rows label attrs
                if len(skus_here) == 1 and i == 0:
                    header_idx = i; break
            if header_idx is None:
                continue
            header = rows[header_idx]
            # attribute rows follow
            for r in rows[header_idx + 1:]:
                if not r: continue
                label = r[0]
                if not label: continue
                for col_i in range(1, min(len(r), len(header))):
                    sku = header[col_i]
                    if not sku or not SKU_RE.match(sku): continue
                    val = r[col_i]
                    if not val: continue
                    blocks_by_sku.setdefault(sku, {
                        "model_no": sku, "dimensions": "", "material": "",
                        "desktop": "", "items_included": [], "attrs": {},
                        "image": img_local,
                    })
                    b = blocks_by_sku[sku]
                    if img_local and not b.get("image"): b["image"] = img_local
                    L = label.lower()
                    if "dimension" in L and "outer" in L:
                        b["dimensions"] = val if not b["dimensions"] else b["dimensions"] + " · outer " + val
                    elif "outer" in L or "dimension" in L:
                        if not b["dimensions"]: b["dimensions"] = val
                        else: b["attrs"][label] = val
                    elif "material" in L:
                        b["material"] = val
                    elif "desktop" in L or "top" in L:
                        if not b["desktop"]: b["desktop"] = val
                        else: b["attrs"][label] = val
                    else:
                        b["attrs"][label] = val
    return list(blocks_by_sku.values())


def scrape(slug, url):
    html = get(url)
    if not html: return None
    soup = BeautifulSoup(html, "html.parser")
    # find the tab id labeled Specification / Product Specification
    tabs = {}
    for a in soup.select('a[href^="#exp"]'):
        tabs[a.get("href", "")[1:]] = a.get_text(strip=True)
    target_id = None
    for tid, lbl in tabs.items():
        L = lbl.lower()
        if "product specification" in L or ("specification" in L and "holder" not in L):
            target_id = tid; break
    if not target_id: return None
    el = soup.find(id=target_id)
    if not el: return None
    return parse_spec_tables(el, slug, target_id)


def main():
    v2 = json.load(open(CONTENT, encoding="utf-8"))
    listing = json.load(open(LISTING, encoding="utf-8"))
    detail_by_slug = {r["slug"]: r["detail_url"] for r in listing}

    # families to re-check: any block with model_no but empty dims/material/items,
    # or the tanko □ placeholder in model_no (their notation for "see table").
    targets = []
    for slug, d in v2.items():
        for t in d.get("tabs", []):
            if t.get("kind") != "spec_blocks":
                continue
            blocks = t.get("blocks", []) or []
            hit = False
            for b in blocks:
                mn = b.get("model_no", "") or ""
                if "□" in mn:
                    hit = True; break
                if mn and not (b.get("dimensions") or b.get("material") or b.get("items_included") or b.get("image")):
                    hit = True; break
            if hit or not blocks:
                targets.append(slug); break

    print(f"targets to re-parse: {len(targets)}")

    fixed = 0
    for i, slug in enumerate(targets, 1):
        url = detail_by_slug.get(slug)
        if not url:
            print(f"  [{i}/{len(targets)}] {slug}: no URL"); continue
        print(f"  [{i}/{len(targets)}] {slug}", flush=True)
        os.makedirs(os.path.join(IMG_ROOT, slug), exist_ok=True)
        new_blocks = scrape(slug, url)
        if not new_blocks:
            print(f"     no blocks found from tables"); continue
        # replace the Specification tab's blocks
        for t in v2[slug].get("tabs", []):
            if t.get("kind") == "spec_blocks":
                t["blocks"] = new_blocks
                fixed += 1; break

    json.dump(v2, open(CONTENT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nDone. Updated spec_blocks on {fixed} families.")


if __name__ == "__main__":
    main()
