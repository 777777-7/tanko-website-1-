# -*- coding: utf-8 -*-
"""
For families where spec_blocks have model_no but img=null, re-scrape the
Specification tab and pair each 'Model No.' contentBuilder with the IMAGE
contentBuilder that immediately precedes it (tanko's alternating layout).
Downloads the image locally, writes it back into product_content_v2.json.
"""
import json, os, re, sys, time
import requests
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "product_content_v2.json")
LISTING = os.path.join(ROOT, "listing_products.json")
IMG = os.path.join(ROOT, "asset_content")
H = {"User-Agent": "Mozilla/5.0 Chrome/122 Safari/537.36"}
session = requests.Session(); session.headers.update(H)


def get(url):
    for _ in range(3):
        try:
            r = session.get(url, timeout=25); r.raise_for_status()
            time.sleep(0.2); return r.text
        except Exception: time.sleep(1)
    return None


def ext_of(u):
    m = re.search(r"\.(jpg|jpeg|png|webp)(?:\?|$)", u or "", re.I)
    return "." + (m.group(1).lower() if m else "jpg")


def download(url, dest):
    if os.path.exists(dest): return True
    try:
        r = session.get(url, timeout=25); r.raise_for_status()
        open(dest, "wb").write(r.content); time.sleep(0.2); return True
    except Exception: return False


def scrape_spec_pairs(slug, url):
    """Return list of {model_no, dimensions, material, image_local}
    by pairing each 'Model No.' contentBuilder with the previous img-only one."""
    html = get(url)
    if not html: return None
    soup = BeautifulSoup(html, "html.parser")
    # find spec-labelled tab
    tid = None
    for a in soup.select('a[href^="#exp"]'):
        L = a.get_text(strip=True).lower()
        if "product specification" in L or ("specification" in L and "holder" not in L):
            tid = a.get("href", "")[1:]; break
    if not tid: return None
    el = soup.find(id=tid)
    if not el: return None
    cbs = el.find_all("div", class_="contentBuilder", recursive=False)

    out = []
    prev_img_url = None
    n = 1
    os.makedirs(os.path.join(IMG, slug), exist_ok=True)
    for cb in cbs:
        img_el = cb.find("img")
        text = cb.get_text("\n", strip=True)
        has_model = "Model No." in text
        img_url = None
        if img_el:
            img_url = img_el.get("data-src") or img_el.get("src") or None
        if has_model:
            # pair with img_url from THIS cb or the previous one
            src = img_url or prev_img_url
            img_local = None
            if src:
                fn = f"exp{tid[-1] if tid[-1].isdigit() else 'X'}_paired{n}{ext_of(src)}"
                if download(src, os.path.join(IMG, slug, fn)):
                    img_local = f"asset_content/{slug}/{fn}"
            n += 1
            # parse a few common fields (light-touch, just enough to render)
            def grab(pat, group=1):
                m = re.search(pat, text, re.I)
                return re.sub(r"\s+", " ", m.group(group)).strip() if m else ""
            out.append({
                "model_no": grab(r"Model No\.?\s*\n?\s*([A-Z0-9\-/□]+(?:\s*\([^)]+\))?)"),
                "dimensions": grab(r"Dimensions?\s*[：:]?\s*\n?\s*([WLHDwhld0-9x×\-\s\.mm]+mm[^\n]*)"),
                "material": grab(r"Material\s*[：:]?\s*\n?\s*([^\n]+?)(?=\n|Desktop|Items|Load|$)"),
                "desktop": grab(r"Desktop\s*[：:]?\s*\n?\s*([^\n]+?)(?=\n|Items|Material|$)"),
                "items_included": [],
                "image": img_local,
            })
            prev_img_url = None
        elif img_url:
            prev_img_url = img_url
        else:
            prev_img_url = None
    return out


def main():
    v2 = json.load(open(CONTENT, encoding="utf-8"))
    listing = {r["slug"]: r["detail_url"] for r in json.load(open(LISTING, encoding="utf-8"))}

    # find families where >=1 spec_block has model_no + null image
    targets = []
    for slug, d in v2.items():
        for t in d.get("tabs", []):
            if t.get("kind") == "spec_blocks":
                for b in t.get("blocks", []):
                    if b.get("model_no") and not b.get("image"):
                        targets.append(slug); break
                break
    # de-dup
    targets = list(dict.fromkeys(targets))
    print(f"families to repair: {len(targets)}")

    fixed = 0
    for i, slug in enumerate(targets, 1):
        url = listing.get(slug)
        if not url:
            print(f"  [{i}/{len(targets)}] {slug}: no URL"); continue
        new_blocks = scrape_spec_pairs(slug, url)
        if not new_blocks:
            print(f"  [{i}/{len(targets)}] {slug}: no blocks"); continue
        # replace blocks with the paired versions where they beat the old (had null image)
        for t in v2[slug].get("tabs", []):
            if t.get("kind") == "spec_blocks":
                # only replace if the new version has more images than the old
                old_imgs = sum(1 for b in t.get("blocks", []) if b.get("image"))
                new_imgs = sum(1 for b in new_blocks if b.get("image"))
                if new_imgs > old_imgs:
                    # keep items_included from old if we already had them
                    old_by_model = {b.get("model_no",""): b for b in t.get("blocks", [])}
                    for nb in new_blocks:
                        ob = old_by_model.get(nb["model_no"])
                        if ob:
                            if ob.get("items_included"): nb["items_included"] = ob["items_included"]
                            if not nb["desktop"] and ob.get("desktop"): nb["desktop"] = ob["desktop"]
                            if not nb["material"] and ob.get("material"): nb["material"] = ob["material"]
                    t["blocks"] = new_blocks
                    fixed += 1
                    print(f"  [{i}/{len(targets)}] {slug}: repaired ({old_imgs}→{new_imgs} imgs)")
                else:
                    print(f"  [{i}/{len(targets)}] {slug}: no improvement")
                break
        if i % 10 == 0:
            json.dump(v2, open(CONTENT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(v2, open(CONTENT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nDone. Repaired {fixed} families.")


if __name__ == "__main__":
    main()
