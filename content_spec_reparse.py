# -*- coding: utf-8 -*-
"""
Re-parse the #exp3 (Specification) section per variant for every tanko product.
The original extractor flattened all variants into one blob; this pulls one
structured spec block per variant (Model No / Dimensions / Material / Desktop
/ Items included list), matched to its dimensioned drawing image.

Images from asset_content/{slug}/ are re-indexed by variant order.
Outputs merged into product_content.json under key `spec_blocks`.
"""
import json, os, re, sys, time
import requests
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "product_content.json")
LISTING = os.path.join(ROOT, "listing_products.json")
IMG_ROOT = os.path.join(ROOT, "asset_content")
H = {"User-Agent": "Mozilla/5.0 Chrome/122 Safari/537.36"}
DELAY = 0.35
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
            time.sleep(1.0 * (a + 1))
    return None


ITEM_RE = re.compile(r"([A-Z][A-Z0-9\-/]{1,15})\s*[|｜]?\s*([^\n]*?)\s*x\s*(\d+)", re.I)


def clean(s):
    return re.sub(r"\s+", " ", s or "").strip(" ：:·|｜")


def parse_spec_block(block_el, img_index_for_slug, slug):
    """Parse one contentBuilder block. Returns dict or None."""
    text = block_el.get_text("\n", strip=True)
    if "Model No." not in text:
        return None
    def grab(pat, group=1, default=""):
        m = re.search(pat, text, re.I)
        return clean(m.group(group)) if m else default

    model = grab(r"Model No\.?\s*\n?\s*([A-Z0-9\-/□]+(?:\s*\([^)]+\))?)")
    dims  = grab(r"Dimensions?\s*[：:]?\s*\n?\s*([WLHDwhld0-9x×\-\s\.mm]+mm[^\n]*)")
    mat   = grab(r"Material\s*[：:]?\s*\n?\s*([^\n]+?)(?=\n|Desktop|Items|Load|$)")
    desk  = grab(r"Desktop\s*[：:]?\s*\n?\s*([^\n]+?)(?=\n|Items|Material|$)")

    # items included
    items = []
    m = re.search(r"Items included\s*[：:]?\s*\n?(.*?)(?:$)", text, re.S | re.I)
    if m:
        chunk = m.group(1)
        # normalize: each item spans multiple lines like "RA-9091\n|\nstorage cabinet\nx 1"
        chunk = re.sub(r"\n+", "\n", chunk)
        # find "SKU | desc x N" triples across newlines
        # split on lines starting with a SKU pattern
        lines = [l.strip() for l in chunk.split("\n") if l.strip()]
        i = 0
        while i < len(lines):
            if re.match(r"^[A-Z][A-Z0-9\-/]{1,15}$", lines[i]):
                sku = lines[i]
                desc = ""; qty = ""
                j = i + 1
                # skip pipe
                if j < len(lines) and lines[j] in ("|", "｜"):
                    j += 1
                # description
                if j < len(lines) and not re.match(r"^x\s*\d", lines[j], re.I):
                    desc = lines[j]; j += 1
                # optional multi-line description
                while j < len(lines) and not re.match(r"^x\s*\d|^\(", lines[j], re.I) \
                      and not re.match(r"^[A-Z][A-Z0-9\-/]{1,15}$", lines[j]):
                    desc += " " + lines[j]; j += 1
                # qty
                if j < len(lines) and re.match(r"^x\s*\d", lines[j], re.I):
                    qm = re.match(r"^x\s*(\d+)", lines[j], re.I)
                    if qm: qty = qm.group(1)
                    j += 1
                # optional trailing "(8 pcs)"
                if j < len(lines) and re.match(r"^\(", lines[j]):
                    j += 1
                items.append({"sku": sku, "desc": clean(desc), "qty": qty})
                i = j
            else:
                i += 1

    # find image for this block
    img_el = block_el.find("img")
    img_local = None
    if img_el:
        # increment the counter and use spec{n}.{ext} that content_extract saved
        n = img_index_for_slug["n"]
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            candidate = os.path.join(IMG_ROOT, slug, f"spec{n}{ext}")
            if os.path.exists(candidate):
                img_local = f"asset_content/{slug}/spec{n}{ext}"; break
        img_index_for_slug["n"] += 1

    return {
        "model_no": model, "dimensions": dims, "material": mat, "desktop": desk,
        "items_included": items, "image": img_local,
    }


def scrape_specs(slug, url):
    html = get(url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    exp3 = soup.find(id="exp3")
    if not exp3:
        return []
    counter = {"n": 1}
    blocks = []
    for cb in exp3.find_all("div", class_="contentBuilder", recursive=False):
        # skip intro block that has no Model No
        if "Model No." not in cb.get_text():
            continue
        rec = parse_spec_block(cb, counter, slug)
        if rec:
            blocks.append(rec)
    return blocks


def main():
    listing = json.load(open(LISTING, encoding="utf-8"))
    content = json.load(open(CONTENT, encoding="utf-8"))

    for i, r in enumerate(listing, 1):
        slug, url = r["slug"], r["detail_url"]
        print(f"[{i}/{len(listing)}] {slug}", flush=True)
        blocks = scrape_specs(slug, url)
        rec = content.setdefault(slug, {"slug": slug, "url": url, "features": [], "how_to_choose": [], "spec": {}})
        rec["spec_blocks"] = blocks
        if i % 10 == 0 or i == len(listing):
            json.dump(content, open(CONTENT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(content, open(CONTENT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    total = sum(len(v.get("spec_blocks", [])) for v in content.values())
    print(f"\nDone. {len(listing)} products, {total} spec blocks total, {len(failed)} failures")


if __name__ == "__main__":
    main()
