# -*- coding: utf-8 -*-
"""
Label-aware content extractor v2. Reads the actual tab menu on each product
page and captures each tab's content under its real label. Handles all four
layouts we found across tanko categories:

  • Features / How to choose / Specification         (workstation, hanger-rack)
  • Features / Specification                          (most categories)
  • Features / Accessories / Specification            (tool-cabinet)
  • Features / Holders Specification / Product Spec.  (cnc-tool)

Output: product_content_v2.json  — {slug: {url, tabs: [{key, label, kind, ...}]}}
Uses images already in asset_content/ where possible (dedupes by URL) and
downloads any additional imagery to asset_content/{slug}/ with new numbering.
"""
import json, os, re, sys, time
import requests
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "product_content.json")   # v1 (used as image cache reference)
OUT = os.path.join(ROOT, "product_content_v2.json")
IMG_ROOT = os.path.join(ROOT, "asset_content")
LISTING = os.path.join(ROOT, "listing_products.json")
H = {"User-Agent": "Mozilla/5.0 Chrome/122 Safari/537.36"}
DELAY = 0.15
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


def ext_of(u):
    m = re.search(r"\.(jpg|jpeg|png|webp)(?:\?|$)", u or "", re.I)
    return "." + (m.group(1).lower() if m else "jpg")


def img_src(im):
    return im.get("data-src") or im.get("src") or ""


_URL_CACHE = {}   # url -> already-downloaded local file path (any slug)


def _seed_url_cache():
    """Fast-path: skip download if the same URL was already saved to /asset_content/
    under a different filename in a previous extraction pass."""
    # We can't reverse-map filename -> url, so instead pre-scan v1 product_content.json
    # and its features/how_to_choose entries which recorded the image URLs during their
    # ORIGINAL download. If those files exist locally, register their URL -> path.
    v1_path = os.path.join(ROOT, "product_content.json")
    if not os.path.exists(v1_path):
        return
    v1 = json.load(open(v1_path, encoding="utf-8"))
    # v1 didn't store source URLs, only local paths -> we'll re-derive by matching
    # tab positions: any existing local file is at least a valid fallback.
    # We still need URLs -> the ORIGINAL scraper stored them as .images or the like.
    # Rely on the tanko_variants.json cache too:
    tv_path = os.path.join(ROOT, "tanko_variants.json")
    if os.path.exists(tv_path):
        pass  # variants images are separate anyway
    # Cache by file body hash instead — but simpler: cache by URL during THIS run.
    # (in-run dedup is enough since many features share the same URL across variants)


def download_local(url, dest):
    if not url:
        return None
    if os.path.exists(dest):
        _URL_CACHE[url] = dest
        return True
    # in-run dedup: if we've saved this URL to some other path already, hard-link/copy
    prev = _URL_CACHE.get(url)
    if prev and os.path.exists(prev):
        try:
            import shutil
            shutil.copy(prev, dest); return True
        except Exception:
            pass
    try:
        r = session.get(url, timeout=25); r.raise_for_status()
        open(dest, "wb").write(r.content); time.sleep(DELAY)
        _URL_CACHE[url] = dest
        return True
    except Exception as e:
        failed.append({"url": url, "error": f"img: {e}"}); return False


def key_from_label(label):
    """Normalize a tab label to a stable key."""
    L = (label or "").lower().strip()
    if "feature" in L: return "features"
    if "how to choose" in L or "how to config" in L: return "howto"
    if "accessor" in L: return "accessories"
    if "holder" in L: return "holders_spec"
    if "product specification" in L: return "pspec_extra"
    if "specification" in L: return "spec_blocks"
    return re.sub(r"[^a-z0-9]+", "_", L).strip("_") or "tab"


def clean(s):
    return re.sub(r"\s+", " ", s or "").strip(" ：:·|｜")


def parse_item_cards(container, slug, tag):
    """Standard #exp1 pattern: repeated .item with image + heading + caption."""
    cards = []
    for i, item in enumerate(container.select(".item")):
        im = item.find("img")
        head = item.find(["h3", "h4", "h5", "strong", "b"])
        title = head.get_text(" ", strip=True) if head else ""
        full = item.get_text(" ", strip=True)
        caption = full[len(title):].strip(" |:·-") if title and full.startswith(title) else full
        caption = clean(caption)
        src = img_src(im) if im else ""
        img_local = None
        if src:
            fn = f"{tag}_{i+1}{ext_of(src)}"
            if download_local(src, os.path.join(IMG_ROOT, slug, fn)):
                img_local = f"asset_content/{slug}/{fn}"
        cards.append({"title": title, "caption": caption, "image": img_local})
    return cards


def parse_spec_blocks(container, slug, tag):
    """#exp3 pattern: per-variant .contentBuilder with one image + spec text."""
    blocks = []
    n = 1
    for cb in container.find_all("div", class_="contentBuilder", recursive=False):
        text = cb.get_text("\n", strip=True)
        if "Model No." not in text:
            continue
        def grab(pat, group=1, default=""):
            m = re.search(pat, text, re.I)
            return clean(m.group(group)) if m else default
        model = grab(r"Model No\.?\s*\n?\s*([A-Z0-9\-/□]+(?:\s*\([^)]+\))?)")
        dims  = grab(r"Dimensions?\s*[：:]?\s*\n?\s*([WLHDwhld0-9x×\-\s\.mm]+mm[^\n]*)")
        mat   = grab(r"Material\s*[：:]?\s*\n?\s*([^\n]+?)(?=\n|Desktop|Items|Load|$)")
        desk  = grab(r"Desktop\s*[：:]?\s*\n?\s*([^\n]+?)(?=\n|Items|Material|$)")

        items = []
        m = re.search(r"Items included\s*[：:]?\s*\n?(.*?)(?:$)", text, re.S | re.I)
        if m:
            lines = [l.strip() for l in re.sub(r"\n+", "\n", m.group(1)).split("\n") if l.strip()]
            i = 0
            while i < len(lines):
                if re.match(r"^[A-Z][A-Z0-9\-/]{1,15}$", lines[i]):
                    sku = lines[i]; desc = ""; qty = ""
                    j = i + 1
                    if j < len(lines) and lines[j] in ("|", "｜"): j += 1
                    if j < len(lines) and not re.match(r"^x\s*\d", lines[j], re.I):
                        desc = lines[j]; j += 1
                    while j < len(lines) and not re.match(r"^x\s*\d|^\(", lines[j], re.I) \
                          and not re.match(r"^[A-Z][A-Z0-9\-/]{1,15}$", lines[j]):
                        desc += " " + lines[j]; j += 1
                    if j < len(lines) and re.match(r"^x\s*\d", lines[j], re.I):
                        qm = re.match(r"^x\s*(\d+)", lines[j], re.I)
                        if qm: qty = qm.group(1)
                        j += 1
                    if j < len(lines) and re.match(r"^\(", lines[j]): j += 1
                    items.append({"sku": sku, "desc": clean(desc), "qty": qty})
                    i = j
                else:
                    i += 1
        img_el = cb.find("img")
        img_local = None
        if img_el:
            src = img_src(img_el)
            fn = f"{tag}_spec{n}{ext_of(src)}"
            if download_local(src, os.path.join(IMG_ROOT, slug, fn)):
                img_local = f"asset_content/{slug}/{fn}"
            n += 1
        blocks.append({"model_no": model, "dimensions": dims, "material": mat,
                       "desktop": desk, "items_included": items, "image": img_local})
    return blocks


def parse_generic_content(container, slug, tag):
    """Fallback: capture images + any headings/paragraphs in reading order.
    Used for CNC 'Holders Specification' which uses contentBuilder blocks
    without .item cards — content is loose image + text pairs."""
    blocks = []
    n = 1
    # Walk each contentBuilder as a block
    for cb in container.find_all("div", class_="contentBuilder", recursive=False):
        img_el = cb.find("img")
        head = cb.find(["h3", "h4", "h5", "strong", "b"])
        title = head.get_text(" ", strip=True) if head else ""
        # capture all body text minus the title
        raw = cb.get_text("\n", strip=True)
        body = raw
        if title and body.startswith(title):
            body = body[len(title):].strip()
        body = re.sub(r"\n{2,}", "\n", body).strip()
        # Look for a spec table if present (Model No | dims)
        table_rows = []
        for tr in cb.select("table tr"):
            cells = [clean(td.get_text(" ", strip=True)) for td in tr.find_all(["td", "th"])]
            if any(cells): table_rows.append(cells)

        img_local = None
        if img_el:
            src = img_src(img_el)
            fn = f"{tag}_{n}{ext_of(src)}"
            if download_local(src, os.path.join(IMG_ROOT, slug, fn)):
                img_local = f"asset_content/{slug}/{fn}"
            n += 1
        if not (img_local or title or body or table_rows):
            continue
        blocks.append({"title": title, "body": body[:500], "image": img_local, "table": table_rows})
    # Fallback again: if no contentBuilder blocks, take loose images with any nearby text
    if not blocks:
        for i, im in enumerate(container.select("img")):
            src = img_src(im)
            fn = f"{tag}_{i+1}{ext_of(src)}"
            if download_local(src, os.path.join(IMG_ROOT, slug, fn)):
                blocks.append({"title": im.get("alt", ""), "body": "", "image": f"asset_content/{slug}/{fn}", "table": []})
    return blocks


def scrape(slug, url):
    html = get(url)
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")
    tab_labels = {}   # #exp{N} -> label
    for a in soup.select('a[href^="#exp"]'):
        href = a.get("href") or ""
        tid = href[1:]
        if tid and tid not in tab_labels:
            lbl = a.get_text(strip=True)
            if lbl:
                tab_labels[tid] = lbl
    if not tab_labels:
        # fallback: order-based
        for i, sec in enumerate(soup.select("[id^=exp]"), 1):
            tab_labels[sec.get("id")] = f"tab{i}"

    os.makedirs(os.path.join(IMG_ROOT, slug), exist_ok=True)
    tabs = []
    for tab_id, label in tab_labels.items():
        el = soup.find(id=tab_id)
        if not el:
            continue
        key = key_from_label(label)
        entry = {"key": key, "label": label, "tab_id": tab_id, "kind": None}
        # dispatch by key/tab_id
        if key == "features":
            entry["kind"] = "cards"
            entry["cards"] = parse_item_cards(el, slug, tab_id)
        elif key == "howto":
            entry["kind"] = "cards"
            entry["cards"] = parse_item_cards(el, slug, tab_id)
        elif key == "accessories":
            entry["kind"] = "cards"
            entry["cards"] = parse_item_cards(el, slug, tab_id)
        elif key == "holders_spec":
            entry["kind"] = "generic"
            entry["blocks"] = parse_generic_content(el, slug, tab_id)
        elif key in ("spec_blocks", "pspec_extra"):
            entry["kind"] = "spec_blocks"
            entry["blocks"] = parse_spec_blocks(el, slug, tab_id)
            # if no blocks parsed (unusual layouts), fall back
            if not entry["blocks"]:
                entry["kind"] = "generic"
                entry["blocks"] = parse_generic_content(el, slug, tab_id)
        else:
            entry["kind"] = "generic"
            entry["blocks"] = parse_generic_content(el, slug, tab_id)
        tabs.append(entry)
    return {"slug": slug, "url": url, "tabs": tabs}


def main():
    listing = json.load(open(LISTING, encoding="utf-8"))
    out = {}
    for i, r in enumerate(listing, 1):
        slug, url = r["slug"], r["detail_url"]
        print(f"[{i}/{len(listing)}] {slug}", flush=True)
        d = scrape(slug, url)
        if d:
            out[slug] = d
        if i % 10 == 0 or i == len(listing):
            json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    # summary
    from collections import Counter
    layout_counts = Counter()
    for d in out.values():
        layout_counts[tuple(t["label"] for t in d["tabs"])] += 1
    print("\nDistinct layouts:")
    for lb, c in layout_counts.most_common():
        print(f"  {c:3d}  {lb}")
    print(f"\nDone. {len(out)} products, {len(failed)} failures")


if __name__ == "__main__":
    main()
