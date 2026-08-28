# -*- coding: utf-8 -*-
"""
E147 Tanko price mapping for storagesystem.com.my
Maps product SKUs to MYR retail prices.

Pricing rule (confirmed with site owner):
  USD list price (E147) x 12.05, rounded UP to next integer -> MYR

Match strategies:
  1. exact SKU match
  2. color-suffix match  (e.g. "DA-31 (BLACK)" -> base "DA-31" + color BLACK)
  3. variant-suffix match (e.g. "WAS-54031F5A" -> base "WAS-54031F")
  4. combo products ("A + B + C") -> sum of component prices

Same SKU may have different prices per colour (e.g. Gray cheaper than others).
"""
import json
import math
import os
import re

EXCHANGE = 12.05  # USD -> MYR rate used by the owner

_COLOR_SYN = {
    "BLACK": "BLACK", "WHITE": "WHITE", "GRAY": "GRAY", "GREY": "GRAY",
    "RED": "RED", "BLUE": "BLUE", "YELLOW": "YELLOW", "GREEN": "GREEN",
    "ORANGE": "ORANGE", "PINK": "PINK", "STAINLESS": "STAINLESS",
}
_COLOR_RE = re.compile(r"\(([^()]*)\)")
_SKU_RE = re.compile(r"^[A-Z][A-Z0-9]{0,4}-\d{2,4}[A-Z0-9]*(?:-\d+[A-Z]*)?$")
_COLOR_SUFFIX_RE = re.compile(
    r"^(.*?)\s*\((BLACK|WHITE|GRAY|GREY|RED|BLUE|YELLOW|GREEN|ORANGE|PINK)\)$",
    re.IGNORECASE,
)

# ---- E147 source data ----
_e147_entries = None
_e147_by_sku = None  # sku -> {"default": price, "colors": {COLOR: price}}


def _load_e147():
    global _e147_entries, _e147_by_sku
    if _e147_entries is not None:
        return
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "_e147_v7.json")
    if not os.path.exists(src):
        # fall back to project root copy
        alt = os.path.join(os.path.dirname(here), "_e147_v7.json")
        src = alt if os.path.exists(alt) else src
    with open(src, encoding="utf-8") as f:
        _e147_entries = json.load(f)

    _e147_by_sku = {}
    for entry in _e147_entries:
        sku = entry["sku"]
        price = float(entry["price"].replace(",", ""))
        color = _extract_color(entry.get("words", []))
        rec = _e147_by_sku.setdefault(sku, {"default": price, "colors": {}})
        if color:
            rec["colors"].setdefault(color, price)
        else:
            rec["default"] = price


def _extract_color(words):
    txt = " ".join(words or [])
    for m in _COLOR_RE.findall(txt):
        cu = m.strip().upper()
        if cu in _COLOR_SYN:
            return _COLOR_SYN[cu]
    return None


def _usd_to_myr(usd):
    """USD x 12.05, round UP to next integer (MYR)."""
    return int(math.ceil(usd * EXCHANGE))


def _price_for_sku(sku, color=None):
    """Return (usd_price, method) for a resolved base SKU, or (None, reason)."""
    _load_e147()
    rec = _e147_by_sku.get(sku)
    if not rec:
        return None, "sku-missing"
    if color:
        cprice = rec["colors"].get(color)
        if cprice:
            return cprice, "color"
    return rec["default"], "default"


def resolve_sku(sku):
    """Return (base_sku, color) for a product SKU, or (None, None)."""
    _load_e147()
    if not sku:
        return None, None
    sku = sku.strip()
    # exact
    if sku in _e147_by_sku:
        return sku, None
    # color suffix
    m = _COLOR_SUFFIX_RE.match(sku)
    if m:
        base = m.group(1).strip()
        color = _COLOR_SYN.get(m.group(2).upper())
        if base in _e147_by_sku and color:
            return base, color
    # variant suffix: strip trailing -NNN / -NNNA
    m2 = re.match(r"^(.*)-\d+[A-Z]*$", sku)
    if m2:
        base2 = m2.group(1)
        if base2 in _e147_by_sku:
            return base2, None
    # digital-family fallback: e.g. WAS-54031F5A -> WAS-54031F
    # handled by caller using _family_fallback
    return None, None


def _family_fallback(sku):
    """Try longest matching E147 SKU that is a prefix of the product SKU.
    Returns (base_sku, usd_price) or (None, None)."""
    _load_e147()
    best = None
    for candidate in _e147_by_sku:
        if sku.startswith(candidate) and len(candidate) > 1:
            if best is None or len(candidate) > len(best):
                best = candidate
    if best is None:
        return None, None
    return best, _e147_by_sku[best]["default"]


def price_for_product(sku, color=None, attributes=None):
    """Get MYR price for a product.
    Returns (myr_price, method, usd_price) or (None, method, None)."""
    if not sku:
        return None, "no-sku", None
    sku = sku.strip()

    # Combo product: "A + B + C"
    if "+" in sku:
        parts = [p.strip() for p in re.split(r"\s*\+\s*", sku)]
        total = 0.0
        missing = []
        for part in parts:
            base, c = resolve_sku(part)
            if base is None:
                base, c = _family_fallback(part)
            if base is None:
                # try stripping color from part inline
                m = _COLOR_SUFFIX_RE.match(part)
                if m and m.group(1).strip() in _e147_by_sku:
                    base = m.group(1).strip()
                    c = _COLOR_SYN.get(m.group(2).upper())
            if base is None:
                missing.append(part)
                continue
            price, _ = _price_for_sku(base, c)
            total += price
        if missing:
            return None, "combo-partial:" + ",".join(missing[:3]), total if total else None
        return _usd_to_myr(total), "combo", total

    # single product
    base, c = resolve_sku(sku)
    if base is None:
        base, c = _family_fallback(sku)
        if base is None:
            return None, "nomatch", None
        price, method = _price_for_sku(base, c)
        return _usd_to_myr(price), "family:" + method, price

    if color and not c:
        # try the product's own color against base sku
        price, method = _price_for_sku(base, color)
        if price is not None:
            return _usd_to_myr(price), "color:" + method, price
    price, method = _price_for_sku(base, c)
    if price is None:
        return None, "nomatch", None
    return _usd_to_myr(price), method, price


def load_price_map():
    """Build a dict: sku -> {"price_myr": int, "method": str, "usd": float}
    for all products in products.json. Returns (map, stats)."""
    _load_e147()
    here = os.path.dirname(os.path.abspath(__file__))
    prods_path = os.path.join(os.path.dirname(here), "products.json")
    with open(prods_path, encoding="utf-8") as f:
        products = json.load(f)

    result = {}
    stats = {}
    for p in products:
        sku = p.get("sku", "")
        color = p.get("color") or None
        myr, method, usd = price_for_product(sku, color, p)
        if myr is None:
            stats["unmatched"] = stats.get("unmatched", 0) + 1
            continue
        method_top = method.split(":")[0]
        stats[method_top] = stats.get(method_top, 0) + 1
        result[sku] = {"price_myr": myr, "method": method, "usd": round(usd, 2) if usd else None}
    return result, stats


if __name__ == "__main__":
    pmap, stats = load_price_map()
    print("PRICE MAP SIZE:", len(pmap))
    print("STATS:", json.dumps(stats, ensure_ascii=False, indent=2))
    # sample
    import itertools
    for sku, info in itertools.islice(pmap.items(), 15):
        print(f"  {sku:22s} -> RM {info['price_myr']:>7d}  ({info['method']})")
    # save
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_price_map.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(pmap, f, ensure_ascii=False, indent=1)
    print("saved", out)
