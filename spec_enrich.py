# -*- coding: utf-8 -*-
"""
For every family in product_content_v2.json, re-fetch the Specification tab
and save each 'Model No.' contentBuilder's RAW text into the block as `raw`.
build.py will then parse that raw text with parse_spec_caption_to_table so
multi-column tables (A4L-330D | A4M-345D | A4A-345D) render fully.
"""
import json, os, re, sys, time
import requests
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "product_content_v2.json")
LISTING = os.path.join(ROOT, "listing_products.json")
H = {"User-Agent": "Mozilla/5.0 Chrome/122 Safari/537.36"}
session = requests.Session(); session.headers.update(H)


def get(url):
    for _ in range(3):
        try:
            r = session.get(url, timeout=25); r.raise_for_status()
            time.sleep(0.15); return r.text
        except Exception: time.sleep(1)
    return None


def scrape_raw(slug, url):
    """Return list of raw-text strings, one per contentBuilder that contains Model No.,
    in document order."""
    html = get(url)
    if not html: return None
    soup = BeautifulSoup(html, "html.parser")
    # find spec tab id
    tid = None
    for a in soup.select('a[href^="#exp"]'):
        L = a.get_text(strip=True).lower()
        if "product specification" in L or ("specification" in L and "holder" not in L):
            tid = a.get("href", "")[1:]; break
    if not tid: return None
    el = soup.find(id=tid)
    if not el: return None
    out = []
    for cb in el.find_all("div", class_="contentBuilder", recursive=False):
        text = cb.get_text(" ", strip=True)
        if "Model No." in text:
            out.append(re.sub(r"\s+", " ", text))
    return out


def main():
    v2 = json.load(open(CONTENT, encoding="utf-8"))
    listing = {r["slug"]: r["detail_url"] for r in json.load(open(LISTING, encoding="utf-8"))}

    # target every family with spec_blocks
    targets = []
    for slug, d in v2.items():
        for t in d.get("tabs", []):
            if t.get("kind") == "spec_blocks":
                targets.append(slug); break
    print(f"targets: {len(targets)}")

    hit = 0
    for i, slug in enumerate(targets, 1):
        url = listing.get(slug)
        if not url: continue
        raws = scrape_raw(slug, url)
        if not raws: continue
        # match raws to spec_blocks by order — length may differ
        for t in v2[slug].get("tabs", []):
            if t.get("kind") == "spec_blocks":
                blocks = t.get("blocks", [])
                for j, b in enumerate(blocks):
                    if j < len(raws):
                        b["raw"] = raws[j]
                        hit += 1
                break
        if i % 20 == 0:
            print(f"  [{i}/{len(targets)}] {slug}: {hit} blocks enriched", flush=True)
            json.dump(v2, open(CONTENT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(v2, open(CONTENT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nDone. Enriched {hit} spec blocks across {len(targets)} families.")


if __name__ == "__main__":
    main()
