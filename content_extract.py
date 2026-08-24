# -*- coding: utf-8 -*-
"""
Extract the Features / How-to-choose / Specification tab content (images + text)
from every tanko product-detail page, download the images to /asset_content/,
and save raw data to product_content.json (keyed by family slug).

Rewriting into original SEO copy happens in the build step (so we can iterate
without re-scraping). This only captures the raw facts + images.
"""
import json, os, re, sys, time
import requests
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_IMG = os.path.join(ROOT, "asset_content")
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
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


def img_src(im):
    return im.get("data-src") or im.get("src") or ""


def ext_of(u):
    m = re.search(r"\.(jpg|jpeg|png|webp)(?:\?|$)", u or "", re.I)
    return "." + (m.group(1).lower() if m else "jpg")


def download(url, dest):
    if os.path.exists(dest):
        return True
    try:
        r = session.get(url, timeout=25); r.raise_for_status()
        open(dest, "wb").write(r.content); time.sleep(DELAY); return True
    except Exception as e:
        failed.append({"url": url, "error": f"img: {e}"}); return False


def item_title_caption(item):
    # title = first heading/strong; caption = remaining text
    head = item.find(["h3", "h4", "h5", "strong", "b"])
    title = head.get_text(" ", strip=True) if head else ""
    full = item.get_text(" ", strip=True)
    caption = full
    if title and full.startswith(title):
        caption = full[len(title):].strip(" |:·-")
    caption = re.sub(r"\s+", " ", caption).strip()
    return title, caption


def scrape(slug, url, imgdir):
    html = get(url)
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")
    os.makedirs(imgdir, exist_ok=True)
    data = {"slug": slug, "url": url, "features": [], "how_to_choose": [], "spec": {}}

    # Features (#exp)
    exp = soup.find(id="exp")
    if exp:
        for i, item in enumerate(exp.select(".item")):
            im = item.find("img")
            if not im:
                continue
            title, caption = item_title_caption(item)
            src = img_src(im)
            fn = f"feat{i+1}{ext_of(src)}"
            if src and download(src, os.path.join(imgdir, fn)):
                data["features"].append({"title": title, "caption": caption,
                                         "image": f"asset_content/{slug}/{fn}"})

    # How to choose (#exp2)
    exp2 = soup.find(id="exp2")
    if exp2:
        for i, item in enumerate(exp2.select(".item")):
            im = item.find("img")
            title, caption = item_title_caption(item)
            src = img_src(im) if im else ""
            fn = f"choose{i+1}{ext_of(src)}"
            rec = {"title": title, "caption": caption, "image": None}
            if src and download(src, os.path.join(imgdir, fn)):
                rec["image"] = f"asset_content/{slug}/{fn}"
            data["how_to_choose"].append(rec)

    # Specification (#exp3)
    exp3 = soup.find(id="exp3")
    if exp3:
        text = exp3.get_text("\n", strip=True)
        def grab(pat):
            m = re.search(pat, text, re.I)
            return m.group(1).strip() if m else ""
        data["spec"] = {
            "model_no": grab(r"Model No\.?\s*[:：]?\s*([^\n]+)"),
            "dimensions": grab(r"Dimensions?\s*[:：]\s*([^\n]+)"),
            "material": grab(r"Material\s*[:：]\s*([^\n]+)"),
            "items_included": grab(r"Items included\s*[:：]?\s*([^\n]+(?:\n[^\n]+){0,6})"),
            "raw": text[:1200],
            "images": [],
        }
        for i, im in enumerate(exp3.select("img")):
            src = img_src(im)
            fn = f"spec{i+1}{ext_of(src)}"
            if src and download(src, os.path.join(imgdir, fn)):
                data["spec"]["images"].append(f"asset_content/{slug}/{fn}")

    return data


def main():
    listing = json.load(open(os.path.join(ROOT, "listing_products.json"), encoding="utf-8"))
    os.makedirs(OUT_IMG, exist_ok=True)
    result = {}
    out_path = os.path.join(ROOT, "product_content.json")
    for i, r in enumerate(listing, 1):
        slug, url = r["slug"], r["detail_url"]
        print(f"[{i}/{len(listing)}] {slug}")
        d = scrape(slug, url, os.path.join(OUT_IMG, slug))
        if d:
            result[slug] = d
        if i % 10 == 0 or i == len(listing):
            json.dump(result, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(result, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(failed, open(os.path.join(ROOT, "content_failed.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    nfeat = sum(len(v["features"]) for v in result.values())
    nimg = len([f for _, _, fs in os.walk(OUT_IMG) for f in fs])
    print(f"\nDone. {len(result)} products, {nfeat} feature cards, {nimg} images, {len(failed)} failures")


if __name__ == "__main__":
    main()
