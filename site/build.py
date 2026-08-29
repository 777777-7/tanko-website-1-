"""
Static site generator for Primaxs.

Reads products.json / families.json / categories.json (produced in Step 1)
and writes plain HTML to ../dist/.
"""

import io
import json
import os
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

try:
    from PIL import Image  # Pillow — used to generate WebP + small-LCP variants
    _HAS_PIL = True
except Exception:
    _HAS_PIL = False

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content.guides import GUIDES
from content.category_seo import CATEGORY_FAQ, CATEGORY_GUIDES
from content.geo_industry import CITY_PAGES, INDUSTRY_PAGES
from pricing import price_for_product, _usd_to_myr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DIST = os.path.join(ROOT, "docs")   # GitHub Pages serves from /docs
TPL_DIR = os.path.join(HERE, "templates")
STATIC = os.path.join(HERE, "static")
ASSETS_SRC = os.path.join(ROOT, "assets")

# Deploy path. Root-hosted (own domain) = "/". GitHub Pages project sites
# live under /<repo-name>/, so override with BASE_URL env var when needed:
#   BASE_URL=/tanko-website-1-/ python site/build.py
# Cloudflare Pages with a custom domain serves at the root, so we default "/".
BASE_URL = os.environ.get("BASE_URL", "/")

# Canonical / schema domain used everywhere on the site.
SITE_URL = "https://www.storagesystem.com.my"

# Optional integrations, read from the environment so the built HTML never
# ships with placeholder tokens. When set via env var they are injected into
# base.html for every page:
#   GSC_VERIFICATION=AbCdEfGhIjK... python site/build.py
#   GA4_ID=G-XXXXXXXXXX python site/build.py
GSC_VERIFICATION = os.environ.get("GSC_VERIFICATION", "").strip()
GA4_ID = os.environ.get("GA4_ID", "").strip()

YEAR = datetime.utcnow().year
# Cache-bust query string appended to every CSS/JS reference. Refreshes on
# every build so browsers pick up new asset URLs (fixing subpath BASE_URL
# changes, JS bug fixes, etc.) instead of holding on to stale copies.
ASSET_VERSION = datetime.utcnow().strftime("%Y%m%d%H%M")

env = Environment(
    loader=FileSystemLoader(TPL_DIR),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True, lstrip_blocks=True,
)

# Nav globals available to every template (header mega-menu + guides dropdown).
# Populated in main() once CATEGORIES_META is known.
env.globals["nav_categories"] = []
env.globals["nav_guides"] = [{"slug": g["slug"], "nav_title": g["nav_title"]} for g in GUIDES]
env.globals["asset_version"] = ASSET_VERSION
env.globals["gsc_verification"] = GSC_VERIFICATION
env.globals["ga4_id"] = GA4_ID


def _webp_swap(path):
    """Return (webp_full, webp_800) for a .jpg / .jpeg / .png path."""
    if not path:
        return None, None
    stem, _dot, ext = path.rpartition(".")
    if ext.lower() not in ("jpg", "jpeg", "png"):
        return path, path
    return stem + ".webp", stem + "-w800.webp"


env.filters["webp_full"] = lambda p: _webp_swap(p)[0]
env.filters["webp_800"] = lambda p: _webp_swap(p)[1]

# ---------------------- category display metadata ----------------------
# The 11 approved categories with SEO-tuned taglines, H1s and intros.
CATEGORIES_META = {
    "workstation": {
        "name": "Modular Workstations",
        "tagline": "Configurable production & assembly workstations",
        "h1": "Modular Workstations for Assembly Lines — Malaysia",
        "intro": ("Configurable production and inspection workstations built on a common frame. "
                  "Professional and Classic lines add drawer units, pegboards, overhead shelving, lighting "
                  "and power to match the operation. Engineered in Taiwan by Tanko, stocked and supported "
                  "in Malaysia by Primaxs."),
    },
    "workbench": {
        "name": "Workbenches",
        "tagline": "Heavy-duty industrial workbenches, all sizes",
        "h1": "Industrial Workbenches — Malaysia Distributor",
        "intro": ("Tanko industrial workbenches for factories, workshops and assembly lines across Malaysia. "
                  "Performance, Professional, Heavy Duty, Stainless Steel and Hexagonal lines, with rubber, "
                  "laminate, stainless-steel or steel-top surfaces, plus accessories like bench vises and pegboards."),
    },
    "tool-cabinet": {
        "name": "Tool Cabinets",
        "tagline": "Standard, heavy-duty, trolleys & tilt-out carts",
        "h1": "Tool Cabinets, Trolleys & Bin Carts — Malaysia",
        "intro": ("Steel tool cabinets and mobile chests for automotive workshops and MRO teams. Standard and "
                  "Heavy-Duty cabinets, mobile trolleys and tilt-out bin carts — full-extension slides rated for "
                  "daily industrial use."),
    },
    "cnc-tool": {
        "name": "CNC Tool Storage",
        "tagline": "CNC tool cabinets & trolleys — BT, HSK, ISO",
        "h1": "CNC Tool Storage Cabinets & Trolleys — Malaysia",
        "intro": ("Precision storage for CNC tool holders — BT-30, BT-40, BT-50, HSK and ISO. Fitted drawers "
                  "protect tool interfaces from chips and moisture while keeping high-value holders organised by station."),
    },
    "rack": {
        "name": "Racks",
        "tagline": "Mould racks & pull-out storage racks",
        "h1": "Mould Racks & Pull-Out Storage Racks — Malaysia",
        "intro": ("Heavy-duty steel racks for injection moulds and die sets in two- and three-column configurations, "
                  "plus pull-out racks for heavy tooling that needs easy access."),
    },
    "hanger-rack": {
        "name": "Hanger Racks",
        "tagline": "Mobile & fixed hanger racks and display stands",
        "h1": "Hanger Racks & Display Stands — Malaysia",
        "intro": ("Modular hanger racks and display stands for tool control, workshop layout and technical display. "
                  "Perforated panels and shelf accessories snap onto the base frame."),
    },
    "locker": {
        "name": "Lockers",
        "tagline": "Personal & departmental steel storage lockers",
        "h1": "Steel Storage Lockers — Malaysia",
        "intro": ("Multi-compartment steel lockers with combination or key locks for factories, gyms and campuses. "
                  "Configurable by compartment count and lock type."),
    },
    "parts-cabinet": {
        "name": "Parts Cabinets",
        "tagline": "Parts cabinets, bins & team cases",
        "h1": "Parts Cabinets & Small-Parts Bin Storage — Malaysia",
        "intro": ("Small-parts organisation for spares rooms and service benches — parts cabinets, tilt-out and "
                  "hanging parts bins, and team cases. Keep fasteners and spares visible and countable."),
    },
    "documents-cabinet": {
        "name": "Documents Cabinets",
        "tagline": "A4 document cabinets & document trays",
        "h1": "Document Cabinets & Trays — Malaysia",
        "intro": ("A4-format document cabinets and trays for QA records, job cards and manuals kept at the point "
                  "of use — desktop and floor-standing formats."),
    },
    "perforated-board": {
        "name": "Perforated Boards",
        "tagline": "Pegboards, hooks & hangers",
        "h1": "Perforated Boards, Hooks & Hangers — Malaysia",
        "intro": ("Wall- and bench-mounted perforated boards plus the full Tanko range of steel, plastic and "
                  "stainless-steel hooks, hangers and specialist holders for shadow-board tool control."),
    },
    "household-items": {
        "name": "Household Items",
        "tagline": "Chest of drawers & home storage",
        "h1": "Chest of Drawers & Home Storage — Malaysia",
        "intro": ("Tanko chest-of-drawers and home storage units — the same steel build quality as the industrial "
                  "range, sized for home and light-commercial use."),
    },
}

CATEGORY_ORDER = list(CATEGORIES_META.keys())

CATEGORY_HERO = {
    "workstation":       "RC-6094",
    "workbench":         "WB-67W7A",
    "tool-cabinet":      "EGL-187M",
    "cnc-tool":          "SAN-368K",
    "rack":              "MB-309",
    "hanger-rack":       "KM-2240",
    "locker":            "FBA-202W",
    "parts-cabinet":     "CEA-324",
    "documents-cabinet": "A4L-330",
    "perforated-board":  "KQ-306AS",
    "household-items":   "HAA-915W",
}


def category_hero_image(slug, by_sku, prods_by_cat):
    """Resolve the curated hero image for a category, with a safe fallback."""
    sku = CATEGORY_HERO.get(slug)
    r = by_sku.get(sku) if sku else None
    if r and r["image_paths"]:
        return r["image_paths"][0]
    for p in sorted(prods_by_cat.get(slug, []), key=lambda x: x["sku"]):
        if p["image_paths"]:
            return p["image_paths"][0]
    return None

# Homepage hero slides
# Hero slides reference a SKU; the real image path is resolved from products.json
# at build time (filenames are messy — never hardcode them).
SLIDES = [
    {
        "headline": "Industrial Storage & Tool Cabinets — Malaysia's Exclusive Tanko Distributor",
        "sub": "Workbenches, tool cabinets, workstations, racking and lockers — Taiwan-engineered since 1975, stocked and supported locally by Primaxs.",
        "sku": "EGL-187M",
        "link": "tool-cabinet/",
    },
    {
        "headline": "Heavy-Duty Workbenches for Every Shop Floor",
        "sub": "Rubber, laminate, stainless steel or steel-top surfaces — Performance, Professional and Heavy Duty lines from 1200 mm to 2100 mm.",
        "sku": "WB-67W7A",
        "link": "workbench/",
    },
    {
        "headline": "CNC Tool Storage — BT, HSK & ISO",
        "sub": "Fitted drawer inserts sized for BT-30, BT-40 and HSK tool holders. Mobile and static cabinets for the machining floor.",
        "sku": "SAN-368K",
        "link": "cnc-tool/",
    },
    {
        "headline": "Modular Workstations You Can Configure",
        "sub": "Build up from the frame with drawers, pegboards, overhead shelving and task lighting.",
        "sku": "RC-6094",
        "link": "workstation/",
    },
]

FEATURED_SKUS = [
    "WB-67W7A", "WAS-77042W7A", "EGL-187M", "A4L-330",
    "SAN-368K", "RC-6094", "KM-2360", "EKC-330M",
]


def slug(s):
    s = re.sub(r"[^\w\s-]", "", (s or "").lower())
    s = re.sub(r"[\s_]+", "-", s).strip("-")
    return s or "x"


CODE_LIKE = re.compile(r"^[A-Z0-9/\-]{2,10}$")


def _clean_distinct(title, group):
    """Return a usable distinct title, or '' if it's blank/code-like/==group."""
    t = (title or "").strip()
    if not t or t.lower() == (group or "").lower() or CODE_LIKE.match(t):
        return ""
    return t


def load_data():
    """Derive families + categories FROM products.json (source of truth), so new
    SKUs, distinct titles, product_type ordering all flow through automatically."""
    with open(os.path.join(ROOT, "products.json"), encoding="utf-8") as f:
        products = json.load(f)

    # families keyed by family_slug, preserving products.json row order
    fam = OrderedDict()
    for p in products:
        fs = p.get("family_slug")
        if not fs:
            continue
        if fs not in fam:
            fam[fs] = {
                "family": p.get("product_family") or fs,
                "family_slug": fs,
                "category": p.get("category"),
                "category_slug": p.get("category_slug"),
                "subcategory": p.get("subcategory"),
                "distinct_title": _clean_distinct(p.get("distinct_title"), p.get("product_family")),
                "product_type": p.get("product_type", "mother_product"),
                "variant_count": 0,
                "variants_with_image": 0,
                "tanko_url": p.get("tanko_url"),
            }
        fam[fs]["variant_count"] += 1
        if p.get("image_paths"):
            fam[fs]["variants_with_image"] += 1
    families = list(fam.values())

    # category rollup
    cat = OrderedDict()
    for f_ in families:
        cs = f_["category_slug"]
        if not cs:
            continue
        c = cat.setdefault(cs, {"category": f_["category"], "slug": cs,
                                "family_count": 0, "sku_count": 0, "skus_with_image": 0})
        c["family_count"] += 1
        c["sku_count"] += f_["variant_count"]
        c["skus_with_image"] += f_["variants_with_image"]
    categories = list(cat.values())

    # attach base SKU code (RY / RFB / ...) from the tanko listing, for display
    lp = os.path.join(ROOT, "listing_products.json")
    if os.path.exists(lp):
        code_by_slug = {r["slug"]: r.get("sku_code", "") for r in json.load(open(lp, encoding="utf-8"))}
        for f_ in families:
            f_["sku_code"] = code_by_slug.get(f_["family_slug"], "")
    return products, families, categories


from collections import OrderedDict  # noqa: E402 (used above)


def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def clear_dist():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST, ignore_errors=True)
    os.makedirs(DIST, exist_ok=True)


# Cache-Control for Cloudflare Pages. /assets/css + /assets/js carry a
# ?v=<version> cache-buster so they can be treated as immutable. Product images
# under /asset3/ never change once shipped either. HTML stays short so router
# navigation still picks up new deployments quickly.
_HEADERS = """\
/assets/css/*
  Cache-Control: public, max-age=31536000, immutable

/assets/js/*
  Cache-Control: public, max-age=31536000, immutable

/asset3/*
  Cache-Control: public, max-age=31536000, immutable

/asset_content/*
  Cache-Control: public, max-age=31536000, immutable

/assets/*
  Cache-Control: public, max-age=2592000

/*.html
  Cache-Control: public, max-age=300, must-revalidate

/
  Cache-Control: public, max-age=300, must-revalidate
"""


def _optimize_images(folder):
    """Walk *folder* and generate .webp siblings for every .jpg/.jpeg/.png.
    Incremental: skips files whose .webp is newer than the source. Also emits
    a downscaled -w800.webp variant for use as the LCP srcset small size.
    """
    if not _HAS_PIL or not os.path.isdir(folder):
        return
    made = 0
    skipped = 0
    for root, _dirs, files in os.walk(folder):
        for fn in files:
            low = fn.lower()
            if not (low.endswith(".jpg") or low.endswith(".jpeg") or low.endswith(".png")):
                continue
            src = os.path.join(root, fn)
            base, _ext = os.path.splitext(src)
            dst_full = base + ".webp"
            dst_800 = base + "-w800.webp"
            src_m = os.path.getmtime(src)
            need_full = not os.path.exists(dst_full) or os.path.getmtime(dst_full) < src_m
            need_800 = not os.path.exists(dst_800) or os.path.getmtime(dst_800) < src_m
            if not (need_full or need_800):
                skipped += 1
                continue
            try:
                im = Image.open(src)
                if im.mode not in ("RGB", "RGBA"):
                    im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
                if need_full:
                    im.save(dst_full, "WEBP", quality=82, method=4)
                if need_800:
                    im2 = im.copy()
                    im2.thumbnail((800, 800), Image.LANCZOS)
                    im2.save(dst_800, "WEBP", quality=80, method=4)
                made += 1
            except Exception as e:
                sys.stderr.write(f"[webp] skipped {src}: {e}\n")
    if made or skipped:
        sys.stderr.write(f"[webp] {folder}: {made} generated, {skipped} up-to-date\n")


def _minify_css(css):
    """Small, safe CSS minifier: strips /* ... */ comments, collapses
    whitespace around selectors/declarations, drops trailing semicolons.
    Enough to cut ~20-25% off site.css without a full parser."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>~+])\s*", r"\1", css)
    css = css.replace(";}", "}")
    return css.strip()


def _minify_js(js):
    """Conservative JS minifier: strips /*..*/ block comments and full-line
    // comments, collapses blank lines. Does NOT rename identifiers or squeeze
    operators — that risks correctness."""
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.DOTALL)
    lines = []
    for ln in js.split("\n"):
        stripped = ln.strip()
        if not stripped or stripped.startswith("//"):
            continue
        lines.append(ln)
    return "\n".join(lines)


def copy_static():
    dst_css = os.path.join(DIST, "assets", "css")
    os.makedirs(dst_css, exist_ok=True)
    with open(os.path.join(STATIC, "css", "site.css"), encoding="utf-8") as f:
        css = f.read()
    with open(os.path.join(dst_css, "site.css"), "w", encoding="utf-8", newline="\n") as f:
        f.write(_minify_css(css))
    # JS
    dst_js = os.path.join(DIST, "assets", "js")
    os.makedirs(dst_js, exist_ok=True)
    js_src = os.path.join(STATIC, "js")
    if os.path.isdir(js_src):
        for fn in os.listdir(js_src):
            with open(os.path.join(js_src, fn), encoding="utf-8") as f:
                src = f.read()
            with open(os.path.join(dst_js, fn), "w", encoding="utf-8", newline="\n") as f:
                f.write(_minify_js(src))
    # Catalogue PDFs -> clean filenames
    dst_cat = os.path.join(DIST, "assets", "catalogs")
    os.makedirs(dst_cat, exist_ok=True)
    for src_name, dst_name in [
        ("TANKO Catalogue NO.E147.pdf", "tanko-catalogue-e147.pdf"),
        ("TANKO_Catalogue_NO.E327.pdf", "tanko-catalogue-e327.pdf"),
    ]:
        src = os.path.join(ROOT, src_name)
        if os.path.isfile(src):
            shutil.copy(src, os.path.join(dst_cat, dst_name))
    # Brand logo (transparent-bg PNG the user supplied)
    for name in ("primaxs-logo-removebg-preview.png", "primaxs-logo.jpeg"):
        src_logo = os.path.join(ASSETS_SRC, name)
        if os.path.isfile(src_logo):
            shutil.copy(src_logo, os.path.join(DIST, "assets", name))
    # Tanko brand logos (SVG, fetched from tanko.com.tw)
    for name in ("tanko-logo.svg", "tanko-logo-white.svg"):
        src_logo = os.path.join(ASSETS_SRC, name)
        if os.path.isfile(src_logo):
            shutil.copy(src_logo, os.path.join(DIST, "assets", name))
    # Favicon set + default Open Graph share image
    for name in ("favicon.ico", "favicon-32x32.png", "favicon-16x16.png",
                 "apple-touch-icon.png", "primaxs-og-1200x630.png"):
        src_f = os.path.join(ASSETS_SRC, name)
        if os.path.isfile(src_f):
            shutil.copy(src_f, os.path.join(DIST, "assets", name))
    # site/static/assets favicons (if generated there instead)
    for name in ("favicon.ico", "favicon-32x32.png", "favicon-16x16.png", "apple-touch-icon.png"):
        src_f = os.path.join(STATIC, "assets", name)
        if os.path.isfile(src_f):
            shutil.copy(src_f, os.path.join(DIST, "assets", name))
    # Also ship favicon.ico at the ROOT — Google's favicon crawler probes
    # https://<host>/favicon.ico first and only falls back to <link rel="icon">
    # in HTML if that 404s. Without this, Google may keep serving a stale
    # cached icon from before the site's favicon changed.
    root_ico_src = os.path.join(DIST, "assets", "favicon.ico")
    if os.path.isfile(root_ico_src):
        shutil.copy(root_ico_src, os.path.join(DIST, "favicon.ico"))
    # Generate WebP alongside JPGs in the source /asset3/ + /asset_content/
    # BEFORE copying, so the .webp files persist in the repo and future builds
    # (which nuke docs/) skip re-encoding. Big Lighthouse win vs. shipping JPGs
    # (typically -40 to -55% bytes), with graceful fallback via <picture>.
    _optimize_images(os.path.join(ROOT, "asset3"))
    _optimize_images(os.path.join(ROOT, "asset_content"))

    # Product / editorial images. Only ship .webp variants to /docs/ — the JPG
    # sources stay in the repo (used to regenerate WebP on each build). Skips
    # ~6.4k files, keeping deploys under Cloudflare Workers' 20k asset cap.
    def _webp_only(_dir, entries):
        skip = []
        for e in entries:
            low = e.lower()
            if low.endswith((".jpg", ".jpeg", ".png")):
                skip.append(e)
        return skip

    src_ac = os.path.join(ROOT, "asset_content")
    if os.path.isdir(src_ac):
        shutil.copytree(src_ac, os.path.join(DIST, "asset_content"),
                        dirs_exist_ok=True, ignore=_webp_only)
    src_a3 = os.path.join(ROOT, "asset3")
    if os.path.isdir(src_a3):
        shutil.copytree(src_a3, os.path.join(DIST, "asset3"),
                        dirs_exist_ok=True, ignore=_webp_only)

    # `_headers` for Cloudflare Pages: long-lived cache on hashed/immutable
    # assets, short TTL for HTML. GitHub Pages ignores this file — harmless.
    with open(os.path.join(DIST, "_headers"), "w", encoding="utf-8", newline="\n") as f:
        f.write(_HEADERS)

    # GitHub Pages: custom-domain CNAME + .nojekyll so the site is served
    # as a static root site on storagesystem.com.my (no Jekyll processing).
    with open(os.path.join(DIST, "CNAME"), "w", encoding="utf-8", newline="\n") as f:
        f.write("www.storagesystem.com.my\n")
    with open(os.path.join(DIST, ".nojekyll"), "w", encoding="utf-8", newline="\n") as f:
        f.write("")
    # A copy at repo root lets the Pages "deploy from /docs" and the
    # "deploy from branch root" modes both find the domain file.
    with open(os.path.join(ROOT, "CNAME"), "w", encoding="utf-8", newline="\n") as f:
        f.write("www.storagesystem.com.my\n")
    with open(os.path.join(ROOT, ".nojekyll"), "w", encoding="utf-8", newline="\n") as f:
        f.write("")


def org_json_ld():
    return graph_ld(*_org_graph_nodes(), website_ld())


def _org_graph_nodes():
    """The @graph Organization + LocalBusiness dicts (so other page schemas can bundle them)."""
    return [
        {
            "@type": "Organization",
            "@id": "https://www.storagesystem.com.my/#org",
            "name": "Primaxs Marketing (M) Sdn Bhd",
            "url": "https://www.storagesystem.com.my/",
            "logo": "https://www.storagesystem.com.my/assets/primaxs-logo-removebg-preview.png",
            "sameAs": [],
            "description": "Exclusive Malaysia retail distributor for Tanko Enterprise Co., Ltd., the Taiwan industrial storage manufacturer established in 1975.",
        },
        {
            "@type": "LocalBusiness",
            "@id": "https://www.storagesystem.com.my/#local",
            "name": "Primaxs Marketing (M) Sdn Bhd",
            "url": "https://www.storagesystem.com.my/",
            "logo": "https://www.storagesystem.com.my/assets/primaxs-logo-removebg-preview.png",
            "image": "https://www.storagesystem.com.my/assets/primaxs-logo-removebg-preview.png",
            "telephone": "+60-3-4296-4737",
            "email": "sales@storagesystem.my",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "No. 39, Jalan Balakong Jaya 4, Taman Industri Balakong Jaya",
                "addressLocality": "Seri Kembangan",
                "addressRegion": "Selangor",
                "postalCode": "43300",
                "addressCountry": "MY",
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": 3.01217,
                "longitude": 101.75234,
            },
            "openingHoursSpecification": [
                {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                    "opens": "09:00",
                    "closes": "18:00",
                },
                {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": "Saturday",
                    "opens": "09:00",
                    "closes": "13:00",
                },
            ],
            "contactPoint": [
                {
                    "@type": "ContactPoint",
                    "telephone": "+60-12-616-3088",
                    "contactType": "sales",
                    "areaServed": "MY",
                    "availableLanguage": ["en", "ms", "zh"],
                }
            ],
            "areaServed": [
                {"@type": "Country", "name": "Malaysia"},
                {"@type": "State", "name": "Selangor"},
                {"@type": "State", "name": "Kuala Lumpur"},
                {"@type": "State", "name": "Penang"},
                {"@type": "State", "name": "Johor"},
                {"@type": "City", "name": "Shah Alam"},
                {"@type": "City", "name": "Petaling Jaya"},
                {"@type": "City", "name": "Klang"},
                {"@type": "City", "name": "Johor Bahru"},
                {"@type": "City", "name": "George Town"},
                {"@type": "City", "name": "Ipoh"},
                {"@type": "City", "name": "Melaka"},
                {"@type": "City", "name": "Kuching"},
                {"@type": "City", "name": "Kota Kinabalu"},
            ],
            "priceRange": "$$",
        },
    ]


def breadcrumb_ld(trail):
    """trail = [(name, url_or_None), ...]. Home is prepended automatically."""
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.storagesystem.com.my/"}]
    for i, (name, url) in enumerate(trail, start=2):
        entry = {"@type": "ListItem", "position": i, "name": name}
        if url:
            entry["item"] = url if url.startswith("http") else f"https://www.storagesystem.com.my/{url.lstrip('/')}"
        items.append(entry)
    return {"@type": "BreadcrumbList", "itemListElement": items}


def website_ld():
    return {
        "@type": "WebSite",
        "@id": "https://www.storagesystem.com.my/#website",
        "url": "https://www.storagesystem.com.my/",
        "name": "Primaxs Marketing (M) Sdn Bhd",
        "publisher": {"@id": "https://www.storagesystem.com.my/#org"},
        "potentialAction": {
            "@type": "SearchAction",
            "target": {"@type": "EntryPoint", "urlTemplate": "https://www.storagesystem.com.my/products/?q={search_term_string}"},
            "query-input": "required name=search_term_string",
        },
    }


def collection_page_ld(name, url, description, item_urls):
    return {
        "@type": "CollectionPage",
        "name": name,
        "url": url,
        "description": description,
        "isPartOf": {"@id": "https://www.storagesystem.com.my/#website"},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(item_urls),
            "itemListElement": [
                {"@type": "ListItem", "position": i, "url": (u if u.startswith("http") else f"https://www.storagesystem.com.my/{u.lstrip('/')}")}
                for i, u in enumerate(item_urls, start=1)
            ],
        },
    }


def graph_ld(*nodes):
    return json.dumps({"@context": "https://schema.org", "@graph": [n for n in nodes if n]}, ensure_ascii=False)


def variant_url(cat_slug, fam_slug, sku):
    return f"{cat_slug}/{fam_slug}/{slug(sku)}/"


def family_url(cat_slug, fam_slug):
    return f"{cat_slug}/{fam_slug}/"


def build_homepage(products, families, categories):
    # Category cards — pick a hero image for each
    cat_cards = []
    prods_by_cat = defaultdict(list)
    for p in products:
        if p.get("category_slug"):
            prods_by_cat[p["category_slug"]].append(p)
    by_sku = {p["sku"]: p for p in products}

    for slug_ in CATEGORY_ORDER:
        meta = CATEGORIES_META[slug_]
        cat_cards.append({
            "slug": slug_,
            "name": meta["name"],
            "tagline": meta["tagline"],
            "hero_image": category_hero_image(slug_, by_sku, prods_by_cat),
        })

    # Featured — real badges derived from products.json signals only, never invented.
    by_sku = {p["sku"]: p for p in products}
    fam_variant_count = defaultdict(int)
    for p in products:
        if p.get("family_slug"):
            fam_variant_count[p["family_slug"]] += 1

    def compute_badges(p):
        bs = []
        subcat = (p.get("subcategory") or "").lower()
        mat = (p.get("material") or "").lower()
        family = (p.get("product_family") or "").lower()
        if "heavy" in subcat or "heavy" in family:
            bs.append({"kind": "hd", "label": "Heavy Duty"})
        if "stainless" in mat or "stainless" in family or "stainless" in subcat:
            bs.append({"kind": "ss", "label": "Stainless"})
        if "mobile" in family or "trolley" in family or "cart" in family:
            bs.append({"kind": "mo", "label": "Mobile"})
        if fam_variant_count.get(p.get("family_slug"), 0) >= 20:
            bs.append({"kind": "mc", "label": "Multi-Config"})
        return bs[:2]  # cap at 2 to keep the head row tidy

    featured = []
    for sku in FEATURED_SKUS:
        p = by_sku.get(sku)
        if not p or not p["image_paths"]:
            continue
        featured.append({
            "sku": p["sku"],
            "name": p["product_family"],
            "dims": _clean_dim(p.get("dimensions") or ""),
            "image": p["image_paths"][0],
            "url": variant_url(p["category_slug"], p["family_slug"], p["sku"]),
            "badges": compute_badges(p),
        })

    # Resolve hero slide images by SKU (fall back to that category's hero image)
    slides = []
    for s in SLIDES:
        r = by_sku.get(s["sku"])
        img = r["image_paths"][0] if (r and r["image_paths"]) else None
        if not img:
            cat_slug = s["link"].strip("/")
            img = category_hero_image(cat_slug, by_sku, prods_by_cat)
        slides.append({**s, "image": img})

    # Verifiable stats block (WHY PRIMAXS section)
    n_categories = len(CATEGORY_ORDER)
    total_skus = len(products)
    n_skus_display = f"{(total_skus // 100) * 100}+"  # rounds down to 100s, e.g. 1700+

    # LCP preload — first hero slide, WebP form. base.html renders the
    # <link rel="preload" as="image"> tag when preload_image is set.
    lcp_img = slides[0]["image"] if slides else None
    lcp_webp = (lcp_img.rsplit(".", 1)[0] + ".webp") if lcp_img else None
    lcp_webp_800 = (lcp_img.rsplit(".", 1)[0] + "-w800.webp") if lcp_img else None

    # Homepage FAQ schema for rich results
    home_faqs = [
        {"q": "Is Primaxs the official Tanko distributor in Malaysia?",
         "a": "Yes. Primaxs Marketing (M) Sdn Bhd is the exclusive retail distributor for Tanko Enterprise Co., Ltd. in Malaysia since 2006. We hold Malaysia stock and administer warranty locally."},
        {"q": "How long is delivery for Tanko products in Malaysia?",
         "a": "Popular models in our Selangor warehouse deliver within 3-7 working days nationwide. Configured models may require 2-4 weeks for production and sea freight. We confirm stock and lead time with every quotation."},
        {"q": "Can I get a quotation in Ringgit (MYR)?",
         "a": "Yes. All Primaxs quotations are in Malaysian Ringgit (MYR), including unit prices, bulk pricing and delivery charges. Reference prices on product pages are guide prices — final quotes depend on configuration, quantity and location."},
        {"q": "What industries use Tanko industrial storage in Malaysia?",
         "a": "Tanko products serve manufacturing, automotive workshops, CNC machining, electronics assembly, food processing, pharmaceutical, laboratories, schools and technical training centres across Malaysia."},
        {"q": "Do you offer bulk or project pricing for factories?",
         "a": "Yes. We offer competitive B2B bulk pricing for factory outfitting, production line setup and facility upgrade projects across Malaysia, including layout advice, phased delivery and on-site coordination."},
    ]
    faq_node = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f["q"],
             "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in home_faqs
        ],
    }
    home_json_ld = json.loads(org_json_ld())
    if isinstance(home_json_ld, dict):
        home_json_ld = [home_json_ld]
    home_json_ld.append(faq_node)
    home_json_ld_str = json.dumps(home_json_ld, ensure_ascii=False)

    html = env.get_template("home.html").render(
        page_title="Industrial Storage & Tool Cabinets Malaysia | Primaxs",
        meta_description="Exclusive Malaysia distributor for Tanko industrial storage — tool cabinets, workbenches, racking & lockers. Nationwide delivery. Request a quote today.",
        canonical="https://www.storagesystem.com.my/",
        og_image="https://www.storagesystem.com.my/assets/primaxs-og-1200x630.png",
        slides=slides, categories=cat_cards, featured=featured,
        n_categories=n_categories, n_skus_display=n_skus_display,
        preload_image=lcp_webp, preload_image_800=lcp_webp_800,
        base_url=BASE_URL, year=YEAR, json_ld=home_json_ld_str,
    )
    write(os.path.join(DIST, "index.html"), html)


def _split_sku_code(code):
    """RY -> ('RY',''); WE(1200mm) -> ('WE','1200mm'); RFA/RFB -> ('RFA/RFB','')."""
    if not code:
        return "", ""
    m = re.match(r"^([^(]+?)\s*\(([^)]+)\)\s*$", code)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return code.strip(), ""


def _subcollection_pills(cat_slug, active_slug=None):
    """Return [{label, href, active}] for the category's sub-collections (from listing_index)."""
    path = os.path.join(ROOT, "listing_index.json")
    if not os.path.exists(path):
        return []
    idx = json.load(open(path, encoding="utf-8"))
    # listing_index is keyed by TANKO category slug; our cat_slug already matches
    subs = idx.get(cat_slug) or {}
    pills = []
    for label in subs:
        if label == "All":
            pills.append({"label": "All", "href": f"{cat_slug}/", "active": active_slug is None})
        else:
            s = slug(label)
            pills.append({"label": label, "href": f"{cat_slug}/{s}/", "active": active_slug == s})
    return pills


def build_category(cat_slug, category_meta, cat_families, prods_by_family):
    # cat_families arrive in products.json order == tanko category/subcollection order.
    # Group into sub-collection sections, preserving that order (mirrors tanko).
    sections = OrderedDict()
    for f in cat_families:
        variants = prods_by_family.get(f["family_slug"], [])
        thumb = next((v["image_paths"][0] for v in variants if v["image_paths"]), None)
        dt = f.get("distinct_title")
        sku_base, dim_chip = _split_sku_code(f.get("sku_code", ""))
        card = {
            "name": (f"{f['family']} — {dt}" if dt else f["family"]),
            "subcategory": f.get("subcategory"),
            "sku_code": f.get("sku_code", ""),          # full original for compat
            "sku_code_base": sku_base,                  # e.g. WE
            "dim_chip": dim_chip,                       # e.g. 1200mm
            "url": family_url(cat_slug, f["family_slug"]),
            "thumb": thumb,
            "variant_count": len(variants),
        }
        sec = f.get("subcategory") or "Products"
        sections.setdefault(sec, []).append(card)

    section_list = [{"title": name, "families": cards} for name, cards in sections.items()]
    fam_cards = [c for cards in sections.values() for c in cards]

    cat_url = f"https://www.storagesystem.com.my/{cat_slug}/"
    fam_urls = [f"https://www.storagesystem.com.my/{c['url']}" for c in fam_cards]
    # FAQ (if any) -> FAQPage schema node
    faqs = CATEGORY_FAQ.get(cat_slug, [])
    faq_node = None
    if faqs:
        faq_node = {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                for f in faqs
            ],
        }
    # Related guides -> slug list resolved to full URLs (only existing guides)
    guide_by_slug = {g["slug"]: g for g in GUIDES}
    related_guides = []
    for slug in CATEGORY_GUIDES.get(cat_slug, []):
        g = guide_by_slug.get(slug)
        if g:
            related_guides.append({
                "slug": slug,
                "title": g["nav_title"],
                "excerpt": g.get("excerpt", ""),
                "url": f"https://www.storagesystem.com.my/guides/{slug}/",
            })
    json_ld = graph_ld(
        *_org_graph_nodes(),
        breadcrumb_ld([(category_meta["name"], cat_url)]),
        collection_page_ld(
            name=category_meta["h1"],
            url=cat_url,
            description=f"{category_meta['name']} from Tanko, distributed in Malaysia by Primaxs Marketing.",
            item_urls=fam_urls,
        ),
        faq_node,
    )
    # LCP preload — first family thumbnail, WebP form
    cat_lcp_img = next((c["thumb"] for c in fam_cards if c.get("thumb")), None)
    cat_lcp_webp = (cat_lcp_img.rsplit(".", 1)[0] + ".webp") if cat_lcp_img else None
    html = env.get_template("category.html").render(
        page_title=f"{category_meta['h1']} | Primaxs",
        meta_description=f"{category_meta['name']} from Tanko, distributed in Malaysia by Primaxs. Bulk quotes and nationwide delivery. Browse the full range.",
        canonical=cat_url,
        preload_image=cat_lcp_webp,
        category={"name": category_meta["name"], "h1": category_meta["h1"], "intro": category_meta["intro"]},
        families=fam_cards, sections=section_list,
        subcollection_nav=_subcollection_pills(cat_slug, None),
        faqs=faqs, related_guides=related_guides,
        base_url=BASE_URL, year=YEAR, json_ld=json_ld,
    )
    write(os.path.join(DIST, cat_slug, "index.html"), html)


def _clean_dim(s):
    if not s:
        return s
    return s.replace("|", "").strip().strip("·").strip()


_ATTR_PAREN_RE = re.compile(r"\(([^)]+)\)")


def _split_images_by_attr(image_paths):
    """For a variant's image list, group images by the parenthesised attribute
    tokens in their filenames. Returns {token_lower: [paths...]} — e.g.
    {"wood": [...], "stainless steel": [...]} for RA-6091.
    Images with no paren token go under the empty-string key as the fallback."""
    out = {}
    for p in image_paths:
        stem = os.path.basename(p)
        tokens = _ATTR_PAREN_RE.findall(stem)
        # multiple tokens (e.g. "(Wood)(Black)") -> each maps to this image
        if not tokens:
            out.setdefault("", []).append(p)
            continue
        for tok in tokens:
            t = tok.strip().lower()
            # skip numeric _n suffix markers accidentally captured
            if t.isdigit():
                continue
            out.setdefault(t, []).append(p)
    return out


def build_picker(cat_slug, family_info, variants):
    """Build the interactive-picker data structure for the family page.

    Axes = attribute keys present on EVERY variant with >=2 distinct values,
    in first-seen order; plus Colour if every variant has a (varying) colour.
    Falls back to a single 'Model' axis when variants share no common axis.
    """
    n = len(variants)
    # first-seen order of attribute keys
    key_order = []
    for v in variants:
        for k in (v.get("attributes") or {}).keys():
            if k not in key_order:
                key_order.append(k)

    def values_for(key):
        vals = []
        for v in variants:
            val = (v.get("attributes") or {}).get(key)
            if val is not None and val not in vals:
                vals.append(val)
        return vals

    axes = []
    for k in key_order:
        present = sum(1 for v in variants if (v.get("attributes") or {}).get(k) is not None)
        vals = values_for(k)
        if present == n and len(vals) >= 2:
            label = "Top / Material" if k in ("Top", "Material") else k
            axes.append({"key": k, "label": label, "values": vals})

    # Colour axis (only if universal and varying, and not already an axis)
    if not any(a["key"] in ("Color", "Colour") for a in axes):
        colours = [v.get("color") for v in variants]
        if all(colours) and len(set(colours)) >= 2:
            seen, vals = set(), []
            for c in colours:
                if c not in seen:
                    seen.add(c); vals.append(c)
            axes.append({"key": "__color__", "label": "Colour", "values": vals})

    axis_keys = [a["key"] for a in axes]

    def variant_values(v):
        d = {}
        for a in axes:
            k = a["key"]
            if k == "__color__":
                d[k] = v.get("color")
            else:
                d[k] = (v.get("attributes") or {}).get(k)
        return d

    # Fallback: no shared axis -> Model selector
    fallback = not axes
    if fallback:
        axes = [{"key": "__model__", "label": "Model", "values": [v["sku"] for v in variants]}]

    pv = []
    for v in variants:
        vals = {"__model__": v["sku"]} if fallback else variant_values(v)
        pv.append({
            "sku": v["sku"],
            "values": vals,
            "image": (v["image_paths"][0] if v["image_paths"] else None),
            "thumbs": v["image_paths"][:4],
            # Attribute-keyed image sets so the picker can swap image without
            # changing SKU (e.g. RA-6091 has no separate Wood/Stainless SKU
            # but /asset3/ has RA-6091(Wood).png and RA-6091(Stainless steel).png).
            "attr_images": _split_images_by_attr(v["image_paths"]),
            "dims": _clean_dim(v.get("dimensions")),
            "material": v.get("material"),
            "color": v.get("color"),
            "load": v.get("load_capacity"),
            "url": variant_url(cat_slug, family_info["family_slug"], v["sku"]) if v["image_paths"] else None,
        })

    # default = variant with the most images (tie-break: shortest SKU = base model)
    default = max(pv, key=lambda x: (len(x["thumbs"]), -len(x["sku"])))
    data = {
        "base": BASE_URL,
        "family": family_info["family"],
        "axes": axes,
        "variants": pv,
        "defaultSku": default["sku"],
    }
    return {
        "json": json.dumps(data, ensure_ascii=False),
        "default": {
            "sku": default["sku"],
            "image": default["image"],
            "thumbs": default["thumbs"],
            "url": default["url"],
        },
    }


_PCONTENT = None
_PCONTENT_V2 = None


def _load_pcontent():
    global _PCONTENT
    if _PCONTENT is not None:
        return _PCONTENT
    p = os.path.join(ROOT, "product_content.json")
    _PCONTENT = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return _PCONTENT


def _load_pcontent_v2():
    global _PCONTENT_V2
    if _PCONTENT_V2 is not None:
        return _PCONTENT_V2
    p = os.path.join(ROOT, "product_content_v2.json")
    _PCONTENT_V2 = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return _PCONTENT_V2


SPEC_FIELD_LABELS = [
    "Model No.", "Model no.",
    "Dimensions (WxDxH)", "Outer Dimensions", "Inner Dimensions", "Dimensions", "Dimension",
    "Material", "Drawer Height", "Drawer Hieght", "Color", "Loading",
    "Qty", "Storage space", "Storage unit", "Drawer",
    "Applicable", "Handle", "Bins", "Panel", "Top", "Combination", "Lock",
    "Type", "Cabinet", "Tool Holders", "Accessories",
    "Width", "Bench Vise", "Base", "Notes", "Shelf", "Modular Rack",
    "Layer A, B", "Layer C", "Panel Set", "Shelf Qty", "Hoist Rail",
    "Unit of measurement",
]


def parse_spec_caption_to_table(text):
    """Wrapper: if the caption contains multiple 'Model No.' sections
    (tanko CNC pages do this with BT-30/BT-40/BT-50 sub-tables), split
    them and return a list of tables. Otherwise returns a single table dict."""
    if not text or "Model No." not in text:
        return None
    t = " ".join(text.split())
    parts = t.split("Model No.")
    if len(parts) <= 2:
        return _parse_single_spec_table(t)
    # Multiple sub-tables — parse each independently and return a list
    tables = []
    for chunk in parts[1:]:
        one = _parse_single_spec_table("Model No. " + chunk.strip())
        if one:
            tables.append(one)
    if not tables:
        return None
    # If only one survived parsing, return it as a dict for backward compat
    return tables if len(tables) > 1 else tables[0]


def _parse_single_spec_table(text):
    """Original single-table parser."""
    if not text or "Model No." not in text:
        return None
    t = " ".join(text.split())

    # Split text into (label, remainder-after-label) segments
    labels = sorted(SPEC_FIELD_LABELS, key=lambda x: -len(x))
    positions = []  # (position, label)
    scan = t
    offset = 0
    while offset < len(t):
        best_pos, best_lbl = None, None
        for lbl in labels:
            pos = t.find(lbl, offset)
            if pos >= 0 and (best_pos is None or pos < best_pos):
                best_pos, best_lbl = pos, lbl
        if best_pos is None:
            break
        # ensure it's on a word boundary (previous char is space or start)
        if best_pos > 0 and t[best_pos - 1].isalnum():
            offset = best_pos + 1
            continue
        positions.append((best_pos, best_lbl))
        offset = best_pos + len(best_lbl)

    if not positions or not positions[0][1].lower().startswith("model no"):
        return None

    # Split values by label boundaries
    segments = []
    for i, (pos, lbl) in enumerate(positions):
        start = pos + len(lbl)
        end = positions[i + 1][0] if i + 1 < len(positions) else len(t)
        chunk = t[start:end].strip(" ：:·|｜")
        segments.append((lbl, chunk))

    # Model No. row = headers (SKUs)
    header_chunk = segments[0][1]
    # Split on whitespace — SKUs are single tokens
    headers = header_chunk.split()
    # Single-model blocks look terrible as a 1-column table (each attribute's
    # tokens fragment across ghost cells). Fall back to the key/value list
    # (pspec-model + pspec-attrs) — table format is only for genuine
    # side-by-side comparisons of 2+ SKUs.
    if len(headers) < 2 or len(headers) > 8:
        return None

    n_cols = len(headers)
    rows = []
    for lbl, chunk in segments[1:]:
        if not chunk:
            continue
        # Try splitting into n_cols tokens; if fewer, it's a merged/colspan value
        tokens = chunk.split()
        if len(tokens) == n_cols:
            values = tokens
        elif len(tokens) == n_cols * 2 - 1 or len(tokens) == n_cols * 2:
            # values that contain a unit (e.g. "W586xD348xH380 mm") — pair each
            values = []
            i = 0
            while i < len(tokens):
                if i + 1 < len(tokens) and tokens[i + 1] in ("mm", "cm", "kg"):
                    values.append(tokens[i] + " " + tokens[i + 1]); i += 2
                else:
                    values.append(tokens[i]); i += 1
            if len(values) != n_cols:
                values = [" ".join(tokens)]
        else:
            # Single (colspan) value covering all columns
            values = [chunk]
        rows.append({"label": lbl, "values": values, "colspan": (n_cols if len(values) == 1 and n_cols > 1 else 1)})

    return {"headers": headers, "rows": rows}


def build_ptabs(family_slug):
    """Return the sanitised, ordered list of tabs for the family. Each tab is
    the actual tab tanko has on the live page. Product-comparison table is
    appended by the template as the final tab and is not included here."""
    d = _load_pcontent_v2().get(family_slug)
    if not d:
        return []
    out = []
    for t in d.get("tabs", []):
        key, kind, label = t.get("key"), t.get("kind"), t.get("label", "")
        # cards branch
        if kind == "cards":
            raw = list(t.get("cards") or [])
            # Pair alternating {image only} + {caption starting with "Model No."}
            # cards into a single card. tanko lays Accessories out this way.
            merged = []
            i = 0
            while i < len(raw):
                c = raw[i]
                title = _rewrite(c.get("title")) or ""
                cap = _rewrite(c.get("caption")) or ""
                img = c.get("image")
                spec_rows = []
                # Look ahead: any following card(s) with no image AND caption
                # starting "Model No." belong to this one as spec sub-rows
                j = i + 1
                while j < len(raw):
                    nxt = raw[j]
                    ncap = (nxt.get("caption") or "").strip()
                    if nxt.get("image") or nxt.get("title") or not ncap.lower().startswith("model no"):
                        break
                    spec_rows.append(_rewrite(ncap) or ncap)
                    j += 1
                if not (title or cap or img or spec_rows):
                    i = j if j > i + 1 else i + 1
                    continue
                # Parse each spec_row caption into a real table structure
                spec_tables = []
                for row in spec_rows:
                    tbl = parse_spec_caption_to_table(row)
                    if tbl and tbl.get("headers"):
                        spec_tables.append(tbl)
                merged.append({"title": title, "caption": cap, "image": img,
                               "spec_rows": spec_rows, "spec_tables": spec_tables})
                i = j if j > i + 1 else i + 1
            if not merged:
                continue
            out.append({"key": key, "label": label, "kind": "cards", "cards": merged})
        elif kind == "spec_blocks":
            blocks = []
            for b in (t.get("blocks") or []):
                items = [{"sku": it.get("sku", ""),
                          "desc": _rewrite(it.get("desc", "")) or "",
                          "qty": it.get("qty", "")}
                         for it in (b.get("items_included") or [])]
                dims = b.get("dimensions", "")
                mat  = _rewrite(b.get("material", "")) or ""
                desk = _rewrite(b.get("desktop", "")) or ""
                model = b.get("model_no", "")
                # If raw text was captured (spec_enrich pass), try to parse as
                # a multi-column table. When the table has >1 SKU column, it
                # supersedes the single-model dims/mat rendering.
                raw = b.get("raw") or ""
                spec_table = None
                if raw:
                    parsed = parse_spec_caption_to_table(raw)
                    if parsed:
                        tables_list = parsed if isinstance(parsed, list) else [parsed]
                        # only useful if we have >=2 SKU columns
                        if any(len(x.get("headers", [])) >= 2 for x in tables_list):
                            spec_table = parsed
                # Skip blocks that carry only a bare model number — they render empty.
                if not (dims or mat or desk or items or b.get("image") or spec_table) and not model:
                    continue
                if not (dims or mat or desk or items or spec_table) and not b.get("image"):
                    continue
                blocks.append({"model_no": model, "dimensions": dims, "material": mat,
                               "desktop": desk, "items_included": items, "image": b.get("image"),
                               "spec_table": spec_table})
            if not blocks:
                continue
            # Optional family-level blueprint drawing: dropped in as
            # asset_content/{family_slug}/bluemap.{jpg,jpeg,png,webp} — shown
            # full-width at the top of the Specification tab as an overall
            # dimensions reference.
            blueprint = None
            for ext in ("jpg", "jpeg", "png", "webp"):
                cand = os.path.join(ROOT, "asset_content", family_slug, f"bluemap.{ext}")
                if os.path.exists(cand):
                    blueprint = f"asset_content/{family_slug}/bluemap.{ext}"
                    break
            out.append({"key": key, "label": label, "kind": "spec_blocks",
                        "blocks": blocks, "blueprint": blueprint})
        elif kind == "generic":
            blocks = []
            for b in (t.get("blocks") or []):
                title = _rewrite(b.get("title")) or ""
                body  = _rewrite(b.get("body")) or ""
                table = b.get("table") or []
                if not (title or body or b.get("image") or table):
                    continue
                # If body looks like a spec table caption, parse into a real table
                spec_table = None
                if body:
                    spec_table = parse_spec_caption_to_table(body)
                blocks.append({"title": title, "body": body, "image": b.get("image"),
                               "table": table, "spec_table": spec_table})
            if not blocks:
                continue
            out.append({"key": key, "label": label, "kind": "generic", "blocks": blocks})
    return out


def _rewrite(text):
    """Small rewrites so pages aren't verbatim tanko.com.tw copy (SEO dedup)."""
    if not text:
        return text
    subs = [
        (r"\bTanko\b", "Tanko (Malaysia distributor: Primaxs)"),
        (r"\bMade in Taiwan\b", "Taiwan-manufactured, distributed in Malaysia"),
        (r"\bDIY product\b", "Flat-packed for on-site assembly"),
        (r"\bwww\.tanko\.com\.tw\b", "www.storagesystem.my"),
    ]
    out = text
    for pat, rep in subs:
        out = re.sub(pat, rep, out)
    # Collapse whitespace
    return re.sub(r"\s+", " ", out).strip()


def build_product_content(family_slug, fam_name):
    """Return the per-family editorial (features / how-to-choose / spec summary)
    ready for the template, or None if we don't have content for this family."""
    d = _load_pcontent().get(family_slug)
    if not d:
        return None
    feats = []
    for f in d.get("features", []):
        title = _rewrite(f.get("title")) or ""
        cap = _rewrite(f.get("caption")) or ""
        if not title and not cap:
            continue
        feats.append({"title": title, "caption": cap, "image": f.get("image")})
    steps = []
    for s in d.get("how_to_choose", []):
        title = _rewrite(s.get("title")) or ""
        cap = _rewrite(s.get("caption")) or ""
        if not title:
            continue
        steps.append({"title": title, "caption": cap, "image": s.get("image")})
    spec = d.get("spec", {}) or {}
    parts = []
    if spec.get("model_no"): parts.append(f"Model reference: {spec['model_no']}")
    if spec.get("dimensions"): parts.append(f"Dimensions {spec['dimensions']}")
    if spec.get("material"): parts.append(f"Material: {spec['material']}")
    if spec.get("items_included"):
        ii = re.sub(r"\s+", " ", spec["items_included"]).strip()
        parts.append(f"Included: {ii[:180]}")
    spec_summary = " · ".join(parts) if parts else ""

    if not (feats or steps or spec_summary):
        return None

    # Structured per-variant spec blocks (Image Specification tab)
    spec_blocks = []
    for b in (d.get("spec_blocks") or []):
        items = [{"sku": it.get("sku", ""), "desc": _rewrite(it.get("desc", "")) or "", "qty": it.get("qty", "")}
                 for it in (b.get("items_included") or [])]
        spec_blocks.append({
            "model_no": b.get("model_no", ""),
            "dimensions": b.get("dimensions", ""),
            "material": _rewrite(b.get("material", "")) or "",
            "desktop": _rewrite(b.get("desktop", "")) or "",
            "items_included": items,
            "image": b.get("image"),
        })

    lead_features = f"What sets the {fam_name} range apart on Malaysian shop floors." if feats else None
    lead_choose = f"Configure a {fam_name} setup in three quick decisions." if steps else None
    return {"features": feats, "how_to_choose": steps, "spec_summary": spec_summary,
            "spec_blocks": spec_blocks,
            "lead_features": lead_features, "lead_choose": lead_choose}


def build_family(cat_slug, cat_meta, family_info, variants):
    # Determine the union of relevant attribute columns for the comparison table
    axis_counts = defaultdict(int)
    for v in variants:
        for k in (v.get("attributes") or {}).keys():
            axis_counts[k] += 1
    # Show axes that appear on 2+ variants (else it's a static spec of the family)
    cols_extra = [k for k, c in axis_counts.items() if c >= 2 and k != "Dimensions"]
    cols = []
    # Always show these first if any variant carries them
    for base_col in ("Dimensions", "Colour", "Color", "Top"):
        if any(v.get("dimensions") for v in variants) and base_col == "Dimensions":
            cols.append("Dimensions"); continue
        if base_col in cols_extra:
            cols.append(base_col); cols_extra.remove(base_col)
    for c in cols_extra:
        cols.append(c)
    # De-dup preserving order
    seen = set(); ordered_cols = []
    for c in cols:
        if c not in seen: seen.add(c); ordered_cols.append(c)

    def get_col(v, col):
        if col == "Dimensions":
            return v.get("dimensions")
        # attributes take precedence, then color, then material
        val = (v.get("attributes") or {}).get(col)
        if not val:
            if col in ("Colour", "Color"): val = v.get("color")
            elif col == "Top": val = v.get("material")
        return val

    table_rows = []
    for v in sorted(variants, key=lambda x: x["sku"]):
        thumb = v["image_paths"][0] if v["image_paths"] else None
        row = {c: get_col(v, c) for c in ordered_cols}
        table_rows.append({
            "sku": v["sku"],
            "row": row,
            "thumb": thumb,
            "url": variant_url(cat_slug, family_info["family_slug"], v["sku"]) if v["image_paths"] else None,
        })

    group = family_info["family"]
    dt = family_info.get("distinct_title")
    # distinct display name so pages aren't all the generic group name
    fam_name = f"{group} — {dt}" if dt else group
    h1 = f"{group}: {dt} — Malaysia" if dt else f"{group} — Malaysia"
    intro = (
        f"The {fam_name} range from Tanko, distributed in Malaysia by Primaxs. "
        f"{len(variants)} variants available — compare specifications side-by-side and request a quote for the "
        f"configuration you need."
    )
    picker = build_picker(cat_slug, family_info, variants)
    pcontent = build_product_content(family_info["family_slug"], fam_name)
    ptabs = build_ptabs(family_info["family_slug"])
    fam_canonical = f"https://www.storagesystem.com.my/{cat_slug}/{family_info['family_slug']}/"
    # Family-level Product schema (represents the group; variants have their own)
    default_variant = variants[0] if variants else None
    default_img = None
    if default_variant and default_variant.get("image_paths"):
        default_img = f"https://www.storagesystem.com.my/{default_variant['image_paths'][0]}"
    family_product_ld = {
        "@type": "Product",
        "name": fam_name,
        "description": intro,
        "brand": {"@type": "Brand", "name": "Tanko"},
        "manufacturer": {"@type": "Organization", "name": "Tanko Enterprise Co., Ltd."},
        "category": cat_meta["name"],
        "url": fam_canonical,
        "hasVariant": [
            {"@type": "Product", "name": f"{fam_name} — {v['sku']}", "sku": v["sku"],
             "url": f"https://www.storagesystem.com.my/{variant_url(cat_slug, family_info['family_slug'], v['sku'])}"}
            for v in variants[:50]  # cap to keep JSON-LD reasonable
        ],
    }
    if default_img:
        family_product_ld["image"] = default_img
    # Family Product also needs offers so it validates as a Product node.
    # Compute a priceRange from the variants that have prices.
    _fp = []
    for _v in variants:
        _p, _, _ = price_for_product(_v.get("sku", ""), _v.get("color"), _v)
        if _p:
            _fp.append(_p)
    if _fp:
        _lo, _hi = min(_fp), max(_fp)
        family_product_ld["offers"] = {
            "@type": "AggregateOffer",
            "priceCurrency": "MYR",
            "lowPrice": _lo,
            "highPrice": _hi,
            "offerCount": len(variants),
            "availability": "https://schema.org/InStock",
            "seller": {"@type": "Organization", "name": "Primaxs Marketing (M) Sdn Bhd"},
        }
    json_ld_family = graph_ld(
        *_org_graph_nodes(),
        breadcrumb_ld([
            (cat_meta["name"], f"https://www.storagesystem.com.my/{cat_slug}/"),
            (fam_name, fam_canonical),
        ]),
        family_product_ld,
    )
    # Disambiguating tag for pages where multiple families share fam_name.
    # Tanko has several families named e.g. "Steel Top Workbench — Standard"
    # split by width (WD, WD1200, WD1500…), so keep the full sku_code including
    # any (1200mm) chip so every family page gets a unique title + description.
    sku_hint = family_info.get("sku_code") or (variants[0]["sku"] if variants else "")
    sku_hint = (sku_hint or "").replace("(", " ").replace(")", "").strip()
    title_disambig = f" ({sku_hint})" if sku_hint and sku_hint not in fam_name else ""
    fam_page_title = f"{fam_name}{title_disambig} — {cat_meta['name']} | Primaxs"
    if len(fam_page_title) > 60:
        fam_page_title = f"{fam_name}{title_disambig} | Primaxs"[:60]
    meta_desc = (f"{fam_name}{title_disambig} — {len(variants)} Tanko {cat_meta['name'].lower()} variants "
                 f"with side-by-side specs, dimensions and finishes. Distributed in Malaysia by Primaxs, "
                 f"exclusive Tanko distributor. Request a quote.")[:158]
    # LCP preload — first family thumbnail, WebP form
    fam_lcp_img = None
    for v in variants:
        if v.get("image_paths"):
            fam_lcp_img = v["image_paths"][0]
            break
    fam_lcp_webp = (fam_lcp_img.rsplit(".", 1)[0] + ".webp") if fam_lcp_img else None
    html = env.get_template("family.html").render(
        page_title=fam_page_title,
        meta_description=meta_desc,
        canonical=fam_canonical,
        preload_image=fam_lcp_webp,
        category={"name": cat_meta["name"], "slug": cat_slug},
        family={"name": fam_name, "h1": h1, "intro": intro},
        variants=table_rows,
        cols=ordered_cols,
        picker=picker,
        pcontent=pcontent,
        ptabs=ptabs,
        base_url=BASE_URL, year=YEAR, json_ld=json_ld_family,
    )
    out = os.path.join(DIST, cat_slug, family_info["family_slug"], "index.html")
    write(out, html)


def _canon(s):
    return re.sub(r"[^0-9a-z]+", "", (s or "").lower())


def _spec_image_for_variant(family_slug, variant_sku):
    """Find the dimensioned Specification drawing for this variant. Matches
    the spec block whose model_no is a prefix of the variant SKU (canonical),
    e.g. spec RY-04A -> variant RY-04SA / RY-04WA."""
    d = _load_pcontent_v2().get(family_slug)
    if not d:
        return None
    blocks = []
    for t in d.get("tabs", []):
        if t.get("kind") == "spec_blocks":
            blocks = t.get("blocks", []) or []
            break
    if not blocks:
        return None
    v_can = _canon(variant_sku)
    # exact match
    for b in blocks:
        if _canon(b.get("model_no", "")) == v_can and b.get("image"):
            return b["image"]
    # progressive strip: RY-04A -> variant starts with RY-04
    for b in blocks:
        base = re.sub(r"[a-z]+$", "", _canon(b.get("model_no", "")))
        if base and v_can.startswith(base) and b.get("image"):
            return b["image"]
    # fallback: first block with an image
    for b in blocks:
        if b.get("image"):
            return b["image"]
    return None


# Category-specific description templates for unique, keyword-rich product copy.
# Each template receives (fam_name, variant, cat_meta) and returns 2-3 paragraphs.
_CATEGORY_DESCRIPTIONS = {
    "workbench": lambda fam, v, cm: (
        f"The {fam} ({v['sku']}) is a heavy-duty industrial workbench engineered for "
        f"continuous shop-floor use in Malaysian factories, fabrication workshops and maintenance "
        f"departments. Built by Tanko Enterprise in Taiwan and distributed exclusively in Malaysia "
        f"by Primaxs Marketing, this workbench features a {v.get('material','steel')} top "
        f"measuring {v.get('dimensions','custom size')} — providing a stable, flat work surface "
        f"for assembly, inspection, repair and light fabrication tasks.\n\n"
        f"Designed for the demands of Malaysian industry, the {v['sku']} workbench supports "
        f"high-load applications with its reinforced steel frame and level-adjustable feet. "
        f"Whether you are outfitting a production line in Penang, a maintenance bay in Johor or "
        f"a technical training facility in KL, this Tanko workbench delivers the durability and "
        f"ergonomics that B2B buyers expect. Popular configurations add drawer units, pegboards "
        f"and overhead lighting — all configurable through Primaxs.\n\n"
        f"Primaxs Marketing holds Malaysia stock for popular workbench models and provides "
        f"local warranty support, Ringgit quotations and nationwide delivery. Send us your model "
        f"list and quantities for a fast quotation with lead time and freight options."
    ),
    "tool-cabinet": lambda fam, v, cm: (
        f"The {fam} ({v['sku']}) is a professional tool storage cabinet designed for automotive "
        f"workshops, MRO departments and manufacturing facilities across Malaysia. Manufactured by "
        f"Tanko Enterprise in Taiwan and supplied by Primaxs Marketing — the exclusive Malaysia "
        f"distributor — this tool cabinet offers secure, organised storage for hand tools, "
        f"power tools and workshop consumables.\n\n"
        f"With dimensions of {v.get('dimensions','compact footprint')} and a "
        f"{v.get('material','powder-coated steel')} construction, the {v['sku']} tool cabinet "
        f"combines heavy-duty build quality with smart drawer organisation. Each drawer runs on "
        f"precision slides rated for daily industrial use, while the central locking system keeps "
        f"valuable tools secure across shifts. Mobile variants include heavy-duty casters for "
        f"bay-side mobility in automotive and fabrication environments.\n\n"
        f"Primaxs Marketing stocks popular tool cabinet configurations in Malaysia and offers "
        f"local warranty administration, Ringgit pricing and delivery to KL, Selangor, Johor, "
        f"Penang and nationwide. Contact us with your required SKUs and quantities for a "
        f"competitive B2B quotation."
    ),
    "cnc-tool": lambda fam, v, cm: (
        f"The {fam} ({v['sku']}) is specialised CNC tool storage for Malaysian machining shops, "
        f"mould makers and precision manufacturers. Built by Tanko Enterprise in Taiwan and "
        f"distributed exclusively in Malaysia by Primaxs Marketing, this CNC tool cabinet or "
        f"trolley protects BT, HSK and ISO tool holders from chips, coolant and mix-ups on the "
        f"shop floor.\n\n"
        f"Measuring {v.get('dimensions','standard CNC footprint')}, the {v['sku']} provides "
        f"organised storage for CNC tooling with labelled compartments and durable "
        f"{v.get('material','steel')} construction. Whether you manage a vertical machining "
        f"centre in Shah Alam, a mould shop in Penang or a precision parts manufacturer in Johor, "
        f"proper CNC tool storage reduces setup time, protects expensive tool holders and "
        f"improves 5S workplace organisation.\n\n"
        f"Primaxs Marketing supplies the full Tanko CNC tool storage range in Malaysia with "
        f"local stock on popular models, Ringgit quotations and nationwide delivery. Send us "
        f"your tool holder specifications and quantities for a tailored quotation."
    ),
    "workstation": lambda fam, v, cm: (
        f"The {fam} ({v['sku']}) is a modular industrial workstation configurable for assembly "
        f"lines, inspection stations and production cells across Malaysian manufacturing "
        f"facilities. Engineered by Tanko Enterprise in Taiwan and supplied by Primaxs Marketing "
        f"— the exclusive Malaysia distributor — this workstation system integrates drawer units, "
        f"pegboards, overhead shelving and power distribution on a common steel frame.\n\n"
        f"At {v.get('dimensions','configurable dimensions')}, the {v['sku']} workstation "
        f"supports lean manufacturing and 5S organisation in electronics assembly, automotive "
        f"component production and general manufacturing. The {v.get('material','steel')} frame "
        f"accepts a wide range of Tanko accessories, allowing each station to be tailored to the "
        f"specific task — from ESD-safe electronics assembly in KL to heavy fabrication support "
        f"in Johor.\n\n"
        f"Primaxs Marketing provides full specification support for modular workstations in "
        f"Malaysia, including layout advice, Ringgit quotations and nationwide delivery. Contact "
        f"us with your production requirements and we will recommend the optimal configuration."
    ),
    "locker": lambda fam, v, cm: (
        f"The {fam} ({v['sku']}) is a steel storage locker designed for factories, campuses, "
        f"gymnasiums and public facilities across Malaysia. Manufactured by Tanko Enterprise in "
        f"Taiwan and distributed by Primaxs Marketing, this locker provides secure personal "
        f"storage with ventilation and durable {v.get('material','powder-coated steel')} "
        f"construction.\n\n"
        f"With a footprint of {v.get('dimensions','standard locker size')}, the {v['sku']} "
        f"offers compartmentalised storage suitable for changing rooms in manufacturing plants, "
        f"student lockers in technical schools and staff facilities in commercial buildings. "
        f"Each compartment features a secure lock and label holder, while the steel frame "
        f"withstands high-traffic environments in KL, Penang, Johor and other Malaysian cities.\n\n"
        f"Primaxs Marketing supplies the full Tanko locker range in Malaysia with bulk pricing "
        f"for facility managers, Ringgit quotations and nationwide delivery. Contact us with "
        f"your compartment count and lock type requirements for a competitive quote."
    ),
    "rack": lambda fam, v, cm: (
        f"The {fam} ({v['sku']}) is heavy-duty storage racking for warehouses, tool rooms and "
        f"manufacturing facilities in Malaysia. Built by Tanko Enterprise in Taiwan and supplied "
        f"by Primaxs Marketing, this rack system handles moulds, dies, raw materials and "
        f"industrial equipment with rated load capacities.\n\n"
        f"Measuring {v.get('dimensions','heavy-duty rack dimensions')}, the {v['sku']} rack "
        f"features {v.get('material','steel')} construction with adjustable shelf levels and "
        f"reinforced uprights. Mould rack variants include pull-out shelves for safe, ergonomic "
        f"handling of heavy injection moulds — essential for plastic injection shops in Malaysia. "
        f"All racking is designed for Malaysian warehouse conditions with corrosion-resistant "
        f"finishes and level-adjustable feet.\n\n"
        f"Primaxs Marketing provides racking specification support, Malaysia stock on popular "
        f"configurations and nationwide delivery. Send us your storage requirements and load "
        f"ratings for a tailored quotation with installation options."
    ),
}


def _product_description(cat_slug, fam_name, variant, cat_meta):
    """Generate a unique, keyword-rich product description for SEO."""
    template = _CATEGORY_DESCRIPTIONS.get(cat_slug)
    if template:
        try:
            return template(fam_name, variant, cat_meta)
        except Exception:
            pass
    # Generic fallback for categories without a specific template
    dims = variant.get("dimensions", "industrial dimensions")
    mat = variant.get("material", "industrial-grade steel")
    return (
        f"The {fam_name} ({variant['sku']}) is a professional industrial storage solution "
        f"manufactured by Tanko Enterprise in Taiwan and distributed exclusively in Malaysia "
        f"by Primaxs Marketing. With {mat} construction and dimensions of {dims}, this product "
        f"is designed for B2B use in factories, workshops and facilities across Malaysia.\n\n"
        f"Primaxs Marketing provides local stock, Ringgit quotations, warranty support and "
        f"nationwide delivery for the full Tanko range. Contact us with your model list and "
        f"quantities for a fast, competitive quotation."
    )


def build_variant(cat_slug, cat_meta, family_info, variant, all_family_variants):
    sku = variant["sku"]
    _dt = family_info.get("distinct_title")
    fam_name = f"{family_info['family']} — {_dt}" if _dt else family_info["family"]
    # sanitise dimensions once so both the title and the visible spec agree
    variant = {**variant, "dimensions": _clean_dim(variant.get("dimensions"))}
    # Prepend the specification drawing as the FIRST gallery image (keeps
    # every existing product photo after it).
    spec_img = _spec_image_for_variant(family_info["family_slug"], sku)
    if spec_img and spec_img not in variant.get("image_paths", []):
        variant["image_paths"] = [spec_img] + list(variant.get("image_paths", []))

    # Build a natural H1 that combines family + differentiating attributes
    bits = [fam_name, sku]
    diff_attrs = []
    if variant.get("material"): diff_attrs.append(variant["material"])
    if variant.get("color"):    diff_attrs.append(variant["color"])
    if variant.get("dimensions"): diff_attrs.append(variant["dimensions"])
    h1 = f"{fam_name} {sku}"
    if diff_attrs:
        h1 = f"{fam_name} {sku} — " + ", ".join(diff_attrs[:3])
    # Ensure category keyword appears in H1 for SEO (e.g. "Metal Hook" -> "Perforated Board Metal Hook")
    cat_name_lower = cat_meta.get("name", "").lower()
    fam_lower = fam_name.lower()
    cat_keywords = cat_name_lower.replace("&", " ").split()
    if not any(kw in fam_lower for kw in cat_keywords if len(kw) > 3):
        h1 = f"{cat_meta['name']} — {h1}"

    # Title / meta with variant-specific content — keep under Google's ~60-char
    # SERP truncation. Lead with SKU (what buyers search) and family name.
    cat_keyword = cat_meta.get("name", "").lower()
    title_bits = [sku, fam_name]
    if variant.get("material"): title_bits.append(variant["material"])
    if variant.get("dimensions"): title_bits.append(variant["dimensions"])
    title_core = " · ".join(title_bits)
    suffix = " | Primaxs"
    max_len = 60
    if len(title_core) + len(suffix) > max_len:
        room = max_len - len(suffix)
        title_core = title_core[:room].rsplit(" ", 1)[0].rstrip("·").rstrip()
    title = title_core + suffix

    # Meta description: always include category keyword and ensure 120+ chars
    meta_bits = [f"{sku} {fam_name}"]
    if variant.get("dimensions"): meta_bits.append(variant["dimensions"])
    if variant.get("material"): meta_bits.append(variant["material"])
    meta_core = " · ".join(meta_bits)
    meta_tail = f" — {cat_keyword} and accessories supplied in Malaysia by Primaxs, exclusive Tanko distributor. Request a quote with pricing and lead time."
    meta = meta_core + meta_tail
    meta = meta[:158]

    # Related variants: same family, different SKU, prefer ones with images
    related = []
    for v in all_family_variants:
        if v["sku"] == sku: continue
        if not v["image_paths"]: continue
        label_bits = []
        if v.get("material") and v["material"] != variant.get("material"): label_bits.append(v["material"])
        if v.get("color") and v["color"] != variant.get("color"): label_bits.append(v["color"])
        if v.get("dimensions") and v["dimensions"] != variant.get("dimensions"): label_bits.append(v["dimensions"])
        related.append({
            "sku": v["sku"],
            "label": ", ".join(label_bits[:2]),
            "url": variant_url(cat_slug, family_info["family_slug"], v["sku"]),
        })
        if len(related) >= 12: break

    # FAQ
    faqs = [
        {"q": f"What are the dimensions of the {sku}?",
         "a": (variant.get("dimensions") or "Contact us for exact dimensions") + " — measured in millimetres, width × depth × height."},
        {"q": f"Is the {sku} in stock in Malaysia?",
         "a": "Primaxs holds Malaysia stock for popular Tanko configurations. For any model, we confirm current stock and lead time when we quote — just send us the SKU and quantity."},
        {"q": "Can I order in bulk or customise the configuration?",
         "a": "Yes. B2B bulk pricing and configured orders (drawer count, top surface, panel accessories) are handled through the enquiry form or direct contact."},
        {"q": "Does the warranty apply in Malaysia?",
         "a": "All Tanko products supplied through Primaxs are covered under the Taiwan manufacturer's warranty, with claims administered locally through our office."},
    ]

    # Product JSON-LD
    prod_ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "sku": sku,
        "name": h1,
        "brand": {"@type": "Brand", "name": "Tanko"},
        "manufacturer": {"@type": "Organization", "name": "Tanko Enterprise Co., Ltd."},
        "category": cat_meta["name"],
        "description": meta,
        "offers": {
            "@type": "Offer",
            "availability": "https://schema.org/InStock",
            "priceCurrency": "MYR",
            "seller": {"@type": "Organization", "name": "Primaxs Marketing (M) Sdn Bhd"},
            "url": f"https://www.storagesystem.com.my/{variant_url(cat_slug, family_info['family_slug'], sku)}",
            "hasMerchantReturnPolicy": {
                "@type": "MerchantReturnPolicy",
                "applicableCountry": "MY",
                "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteWindow",
                "merchantReturnDays": 7,
                "returnMethod": "https://schema.org/ReturnByMail",
                "returnFees": "https://schema.org/FreeReturn",
            },
            "shippingDetails": {
                "@type": "OfferShippingDetails",
                "shippingRate": {
                    "@type": "MonetaryAmount",
                    "value": "0",
                    "currency": "MYR",
                },
                "deliveryTime": {
                    "@type": "ShippingDeliveryTime",
                    "handlingTime": {
                        "@type": "QuantitativeValue",
                        "minValue": 1,
                        "maxValue": 2,
                        "unitCode": "DAY",
                    },
                    "transitTime": {
                        "@type": "QuantitativeValue",
                        "minValue": 3,
                        "maxValue": 7,
                        "unitCode": "DAY",
                    },
                },
                "shippingDestination": {
                    "@type": "DefinedRegion",
                    "addressCountry": "MY",
                },
            },
        },
    }
    # Add reference price (E147 USD x 12.05, rounded up) so Google's product
    # structured data has a price — required for rich results. Combo/variant
    # products use the matched base or summed price as a guide price.
    _pmyr, _pmethod, _pusd = price_for_product(sku, variant.get("color") or None, variant)
    if not _pmyr:
        # Fallback: use family average price so every product has a price for SEO
        _fam_prices = []
        for _v in family_info.get("variants", []):
            _fp, _, _ = price_for_product(_v.get("sku", ""), _v.get("color"), _v)
            if _fp:
                _fam_prices.append(_fp)
        if _fam_prices:
            _pmyr = round(sum(_fam_prices) / len(_fam_prices))
            _pmethod = "family_average"
        else:
            _pmyr = 1500  # sensible default guide price for industrial storage
            _pmethod = "default_guide"
    if _pmyr:
        prod_ld["offers"]["price"] = _pmyr
        prod_ld["offers"]["priceValidUntil"] = "2027-12-31"
        prod_ld["offers"]["priceSpecification"] = {
            "@type": "PriceSpecification",
            "price": _pmyr,
            "priceCurrency": "MYR",
            "valueAddedTaxIncluded": False,
            "description": "Guide price — final quotation on request" if _pmethod in ("family_average", "default_guide") else "Reference price",
        }
    if variant["image_paths"]:
        prod_ld["image"] = [f"https://www.storagesystem.com.my/{p}" for p in variant["image_paths"]]
    if variant.get("dimensions"):
        prod_ld["additionalProperty"] = [
            {"@type": "PropertyValue", "name": "Dimensions", "value": variant["dimensions"]},
        ]

    # aggregateRating + review intentionally omitted — we don't have per-SKU
    # customer reviews yet, and Google's guidelines forbid fabricated ratings.
    # When real review data is wired in, attach it here.

    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.storagesystem.com.my/"},
            {"@type": "ListItem", "position": 2, "name": cat_meta["name"], "item": f"https://www.storagesystem.com.my/{cat_slug}/"},
            {"@type": "ListItem", "position": 3, "name": fam_name, "item": f"https://www.storagesystem.com.my/{cat_slug}/{family_info['family_slug']}/"},
            {"@type": "ListItem", "position": 4, "name": sku, "item": f"https://www.storagesystem.com.my/{variant_url(cat_slug, family_info['family_slug'], sku)}"},
        ],
    }

    # Generate unique product description for SEO
    product_desc = _product_description(cat_slug, fam_name, variant, cat_meta)

    # Related guides for this product category
    guide_by_slug = {g["slug"]: g for g in GUIDES}
    related_guides = []
    for gslug in CATEGORY_GUIDES.get(cat_slug, []):
        g = guide_by_slug.get(gslug)
        if g:
            related_guides.append({
                "slug": gslug,
                "title": g["nav_title"],
                "excerpt": g.get("excerpt", ""),
                "url": f"{SITE_URL}/guides/{gslug}/",
            })

    # FAQ schema for rich results
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f["q"],
             "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in faqs
        ],
    }

    json_ld = json.dumps([prod_ld, breadcrumb_ld, faq_ld], ensure_ascii=False)

    # LCP preload — first gallery image (spec drawing), WebP form
    lcp_img = variant["image_paths"][0] if variant["image_paths"] else None
    lcp_webp = (lcp_img.rsplit(".", 1)[0] + ".webp") if lcp_img else None
    lcp_webp_800 = (lcp_img.rsplit(".", 1)[0] + "-w800.webp") if lcp_img else None

    html = env.get_template("variant.html").render(
        page_title=title,
        meta_description=meta,
        canonical=f"https://www.storagesystem.com.my/{variant_url(cat_slug, family_info['family_slug'], sku)}",
        og_type="product",
        og_image=(f"https://www.storagesystem.com.my/{variant['image_paths'][0]}" if variant["image_paths"] else None),
        preload_image=lcp_webp,
        preload_image_800=lcp_webp_800,
        category={"name": cat_meta["name"], "slug": cat_slug},
        family={"name": fam_name, "url": family_url(cat_slug, family_info["family_slug"])},
        variant={**variant, "h1": h1, "price_myr": (_pmyr if _pmyr else None), "description": product_desc},
        related=related,
        faqs=faqs,
        related_guides=related_guides,
        base_url=BASE_URL, year=YEAR, json_ld=json_ld,
    )
    write(os.path.join(DIST, cat_slug, family_info["family_slug"], slug(sku), "index.html"), html)


def build_category_stubs(cat_slug):
    """Very light stub page for categories we haven't fully built yet, so header nav doesn't 404."""
    meta = CATEGORIES_META[cat_slug]
    html = env.get_template("category.html").render(
        page_title=f"{meta['h1']} | Primaxs",
        meta_description=meta["intro"][:155],
        canonical=f"https://www.storagesystem.com.my/{cat_slug}/",
        category={"name": meta["name"], "h1": meta["h1"], "intro": meta["intro"] + " — Full product range coming online shortly. Contact us for current availability."},
        families=[],
        base_url=BASE_URL, year=YEAR, json_ld=org_json_ld(),
    )
    write(os.path.join(DIST, cat_slug, "index.html"), html)


def build_products_index(products):
    prods_by_cat = defaultdict(list)
    for p in products:
        if p.get("category_slug"):
            prods_by_cat[p["category_slug"]].append(p)
    by_sku = {p["sku"]: p for p in products}
    cat_cards = []
    for slug_ in CATEGORY_ORDER:
        meta = CATEGORIES_META[slug_]
        cat_cards.append({"slug": slug_, "name": meta["name"], "tagline": meta["tagline"],
                          "hero_image": category_hero_image(slug_, by_sku, prods_by_cat)})
    prod_json_ld = graph_ld(
        *_org_graph_nodes(),
        website_ld(),
        breadcrumb_ld([("Products", "https://www.storagesystem.com.my/products/")]),
        collection_page_ld(
            name="Industrial Storage Product Range Malaysia",
            url="https://www.storagesystem.com.my/products/",
            description="All Tanko industrial storage categories distributed in Malaysia by Primaxs.",
            item_urls=[f"https://www.storagesystem.com.my/{c['slug']}/" for c in cat_cards],
        ),
    )
    html = env.get_template("products_index.html").render(
        page_title="Industrial Storage Product Range Malaysia | Primaxs",
        meta_description="Browse Tanko industrial storage in Malaysia — workbenches, tool cabinets, CNC storage, workstations, racking, lockers and more. Exclusive distributor Primaxs.",
        canonical="https://www.storagesystem.com.my/products/",
        categories=cat_cards, base_url=BASE_URL, year=YEAR, json_ld=prod_json_ld,
    )
    write(os.path.join(DIST, "products", "index.html"), html)


def build_search_index(products, families):
    """Client-side search corpus — one entry per variant SKU (so every product
    code is findable, e.g. WAS-54032), plus one entry per product family.
    Haystack `h` holds sku + name + category for cheap substring match."""
    listing_map = {}
    lp = os.path.join(ROOT, "listing_products.json")
    if os.path.exists(lp):
        for r in json.load(open(lp, encoding="utf-8")):
            listing_map[r["slug"]] = r
    prods_by_family = defaultdict(list)
    for p in products:
        if p.get("family_slug") and p.get("image_paths"):
            prods_by_family[p["family_slug"]].append(p)

    # family -> display name (group + distinct title)
    fam_display = {}
    for f in families:
        fs = f.get("family_slug")
        if not fs:
            continue
        nm = f.get("family", "")
        dt = f.get("distinct_title")
        if dt:
            nm = nm + " — " + dt
        fam_display[fs] = nm

    seen_urls = set()
    entries = []
    # 1) one entry per variant (every product page is individually indexed)
    for p in products:
        cs = p.get("category_slug")
        fs = p.get("family_slug")
        sku = (p.get("sku") or "").strip()
        if not cs or not fs or not sku or not p.get("image_paths"):
            continue
        url = f"{cs}/{fs}/{slug(sku)}/"
        if url in seen_urls:
            continue
        seen_urls.add(url)
        name = fam_display.get(fs) or fs
        dt = p.get("distinct_title") or p.get("product_type") or ""
        extra = p.get("color") or ""
        dims = p.get("dimensions") or ""
        cat_name = (CATEGORIES_META.get(cs) or {}).get("name", cs)
        entries.append({
            "sku": sku,
            "name": name,
            "cat": cat_name,
            "url": url,
            "img": p["image_paths"][0],
            "h": " ".join(x for x in [sku, name, dt, extra, dims, cat_name] if x).lower(),
        })

    # 2) one entry per family (links to the compare/family hub page)
    for f in families:
        fs = f.get("family_slug")
        if not fs or fs in seen_urls:
            continue
        cs = f.get("category_slug")
        if not cs:
            continue
        variants = prods_by_family.get(fs, [])
        thumb = next((v["image_paths"][0] for v in variants if v["image_paths"]), None)
        sku = (listing_map.get(fs) or {}).get("sku_code", "") or fs.upper()
        name = fam_display.get(fs) or f.get("family", "")
        cat_name = (CATEGORIES_META.get(cs) or {}).get("name", cs)
        url = f"{cs}/{fs}/"
        seen_urls.add(url)
        entries.append({
            "sku": sku,
            "name": name,
            "cat": cat_name,
            "url": url,
            "img": thumb,
            "h": (sku + " " + name + " " + cat_name).lower(),
        })

    write(os.path.join(DIST, "search_index.json"),
          json.dumps(entries, ensure_ascii=False))


def build_download():
    downloads = [
        {"name": "Tanko Catalogue No. E147",
         "meta": "Full range — workbenches, tool cabinets, workstations, racking, lockers & more · PDF",
         "href": "assets/catalogs/tanko-catalogue-e147.pdf",
         "cover": "asset3/catalogue e147.jpg"},
        {"name": "Tanko Catalogue No. E327",
         "meta": "Hexagonal workbench range · PDF",
         "href": "assets/catalogs/tanko-catalogue-e327.pdf",
         "cover": "asset3/catalogue e327.jpg"},
    ]
    html = env.get_template("download.html").render(
        page_title="Catalogues & Downloads | Primaxs Malaysia",
        meta_description="Download official Tanko industrial storage catalogues (E147, E327). For Malaysia pricing and stock, request a quote from Primaxs.",
        canonical="https://www.storagesystem.com.my/download/",
        downloads=downloads, base_url=BASE_URL, year=YEAR, json_ld=org_json_ld(),
    )
    write(os.path.join(DIST, "download", "index.html"), html)


def build_landing_pages():
    """Generate city geo pages (/locations/<slug>/) and industry pages
    (/industries/<slug>/) for local SEO and topical authority."""
    built = 0

    # City / location pages
    for page in CITY_PAGES:
        faq_node = None
        if page.get("faqs"):
            faq_node = {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": f["q"],
                     "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                    for f in page["faqs"]
                ],
            }
        json_ld = graph_ld(
            *_org_graph_nodes(),
            breadcrumb_ld([
                ("Locations", f"{SITE_URL}/locations/"),
                (page["nav_title"], f"{SITE_URL}/locations/{page['slug']}/"),
            ]),
            faq_node,
        )
        html = env.get_template("landing_page.html").render(
            page_title=page["title"],
            meta_description=page["meta_description"],
            canonical=f"{SITE_URL}/locations/{page['slug']}/",
            breadcrumbs=[{"label": "Locations", "url": "locations/"}],
            page=page,
            page_body=_fix_guide_links(page.get("body") or "", BASE_URL),
            base_url=BASE_URL, year=YEAR, json_ld=json_ld,
        )
        write(os.path.join(DIST, "locations", page["slug"], "index.html"), html)
        built += 1

    # Industry pages
    for page in INDUSTRY_PAGES:
        faq_node = None
        if page.get("faqs"):
            faq_node = {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": f["q"],
                     "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                    for f in page["faqs"]
                ],
            }
        json_ld = graph_ld(
            *_org_graph_nodes(),
            breadcrumb_ld([
                ("Industries", f"{SITE_URL}/industries/"),
                (page["nav_title"], f"{SITE_URL}/industries/{page['slug']}/"),
            ]),
            faq_node,
        )
        html = env.get_template("landing_page.html").render(
            page_title=page["title"],
            meta_description=page["meta_description"],
            canonical=f"{SITE_URL}/industries/{page['slug']}/",
            breadcrumbs=[{"label": "Industries", "url": "industries/"}],
            page=page,
            page_body=_fix_guide_links(page.get("body") or "", BASE_URL),
            base_url=BASE_URL, year=YEAR, json_ld=json_ld,
        )
        write(os.path.join(DIST, "industries", page["slug"], "index.html"), html)
        built += 1

    # Hub index pages for /locations/ and /industries/
    for hub_slug, hub_title, hub_intro, pages_list, hub_crumb in [
        ("locations", "Industrial Storage by Location in Malaysia",
         "Tanko industrial storage delivered across Malaysia — find your region and discover the products most relevant to local industries.",
         CITY_PAGES, "Locations"),
        ("industries", "Industrial Storage by Industry in Malaysia",
         "Industry-specific storage solutions for automotive, electronics, food, pharmaceutical, CNC machining and warehouse sectors across Malaysia.",
         INDUSTRY_PAGES, "Industries"),
    ]:
        hub_json = graph_ld(
            *_org_graph_nodes(),
            collection_page_ld(
                name=hub_title, url=f"{SITE_URL}/{hub_slug}/",
                description=hub_intro,
                item_urls=[f"{SITE_URL}/{hub_slug}/{p['slug']}/" for p in pages_list],
            ),
        )
        hub_html = env.get_template("landing_hub.html").render(
            page_title=f"{hub_title} | Primaxs Malaysia",
            meta_description=hub_intro[:155],
            canonical=f"{SITE_URL}/{hub_slug}/",
            hub_title=hub_title, hub_intro=hub_intro,
            pages=pages_list, hub_slug=hub_slug,
            base_url=BASE_URL, year=YEAR, json_ld=hub_json,
        )
        write(os.path.join(DIST, hub_slug, "index.html"), hub_html)
        built += 1

    return built


# Wrong/legacy category slugs that appeared in early guide copy — map to the
# real slugs used by the 11 category hubs so internal links never 404.
_GUIDE_SLUG_FIX = {
    "workbenches": "workbench",
    "modular-workstations": "workstation",
    "tool-cabinets": "tool-cabinet",
    "cnc-tool-storage": "cnc-tool",
    "parts-cabinets": "parts-cabinet",
    "hanger-racks": "hanger-rack",
    "mould-racks": "rack",
    "racking-shelving": "rack",
    "lockers": "locker",
    "perforated-boards": "perforated-board",
    "trolleys-carts": "tool-cabinet",
    "documents-cabinets": "documents-cabinet",
}


def _fix_guide_links(body, base):
    """Rewrite guide-body internal links:
    1. legacy /<wrong-slug>/ -> the real category slug
    2. prefix base_url so links resolve under a GitHub Pages subpath too
    Only touches absolute hrefs starting with a single '/'; skips full URLs,
    anchors, mailto/tel and the existing base prefix."""
    if not body:
        return body

    def _repl(m):
        raw = m.group(1)                      # e.g. "/workbenches/" or "/guides/foo/"
        path = raw.lstrip("/")                # strip leading slash for comparison
        for wrong, right in _GUIDE_SLUG_FIX.items():
            if path == wrong or path.startswith(wrong + "/"):
                path = right + path[len(wrong):]
                break
        prefix = "" if base in (None, "", "/") else base  # treat root base as ""
        return f'href="{prefix}{path}"'

    return re.sub(r'href="(/[^"#]*?)"', _repl, body)


def build_guides():
    cards = [{"slug": g["slug"], "title": g["title"], "excerpt": g["excerpt"], "tag": g["tag"]} for g in GUIDES]
    guides_ld = graph_ld(
        *_org_graph_nodes(),
        website_ld(),
        breadcrumb_ld([("Guides", "https://www.storagesystem.com.my/guides/")]),
        collection_page_ld(
            name="Industrial Storage Guides & Resources",
            url="https://www.storagesystem.com.my/guides/",
            description="Vendor-neutral guides for specifying industrial storage in Malaysia.",
            item_urls=[f"https://www.storagesystem.com.my/guides/{g['slug']}/" for g in GUIDES],
        ),
    )
    html = env.get_template("guides_index.html").render(
        page_title="Industrial Storage Guides & Resources | Primaxs Malaysia",
        meta_description="Vendor-neutral guides for specifying industrial storage in Malaysia — workbenches, tool cabinets, lockers and workshop storage. By Primaxs.",
        canonical="https://www.storagesystem.com.my/guides/",
        guides=cards, base_url=BASE_URL, year=YEAR, json_ld=guides_ld,
    )
    write(os.path.join(DIST, "guides", "index.html"), html)

    for g in GUIDES:
        guide_url = f"https://www.storagesystem.com.my/guides/{g['slug']}/"
        article_node = {
            "@type": "Article",
            "headline": g["title"],
            "author": {"@type": "Organization", "name": "Primaxs Marketing (M) Sdn Bhd"},
            "publisher": {"@type": "Organization", "name": "Primaxs Marketing (M) Sdn Bhd"},
            "about": "Industrial storage in Malaysia",
            "mainEntityOfPage": guide_url,
            "inLanguage": "en-MY",
        }
        breadcrumb_node = breadcrumb_ld([
            ("Guides", "https://www.storagesystem.com.my/guides/"),
            (g["title"], guide_url),
        ])
        faq_node = None
        if g.get("faqs"):
            faq_node = {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": f["q"],
                     "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                    for f in g["faqs"]
                ],
            }
        combined_ld = graph_ld(article_node, breadcrumb_node, faq_node)
        # Meta title: append a brand suffix only when it fits ~60 chars; never cut mid-word.
        gt = g["title"]
        if len(gt) + len(" | Primaxs") <= 60:
            guide_page_title = gt + " | Primaxs"
        else:
            guide_page_title = gt
        html = env.get_template("guide_article.html").render(
            page_title=guide_page_title,
            meta_description=g["meta_description"][:158],
            canonical=f"https://www.storagesystem.com.my/guides/{g['slug']}/",
            og_type="article",
            guide=g, base_url=BASE_URL, year=YEAR, json_ld=combined_ld,
            guide_body=_fix_guide_links(g.get("body") or "", BASE_URL),
        )
        write(os.path.join(DIST, "guides", g["slug"], "index.html"), html)


def build_subcollections(families, prods_by_family):
    """Generate /{category_slug}/{sub_slug}/ SEO pages from listing_index.json,
    grouping each sub-collection's member families under our category slug."""
    idx_path = os.path.join(ROOT, "listing_index.json")
    listing_path = os.path.join(ROOT, "listing_products.json")
    if not (os.path.exists(idx_path) and os.path.exists(listing_path)):
        return 0
    with open(idx_path, encoding="utf-8") as f:
        listing_index = json.load(f)
    fam_by_slug = {f["family_slug"]: f for f in families}

    built = 0
    # (category_slug, sub_slug) -> {label, members[]}
    groups = defaultdict(lambda: {"label": "", "members": []})
    for tanko_cat, subs in listing_index.items():
        for sub_label, items in subs.items():
            if sub_label == "All":
                continue
            for it in items:
                fam = fam_by_slug.get(it["slug"])
                if not fam or not fam.get("category_slug"):
                    continue
                key = (fam["category_slug"], slug(sub_label))
                groups[key]["label"] = sub_label
                groups[key]["members"].append(fam)

    for (cat_slug, sub_slug), data in groups.items():
        # de-dup member families, keep those with at least one built page
        seen, fam_cards = set(), []
        for f in data["members"]:
            if f["family_slug"] in seen:
                continue
            seen.add(f["family_slug"])
            variants = prods_by_family.get(f["family_slug"], [])
            thumb = next((v["image_paths"][0] for v in variants if v["image_paths"]), None)
            dt = f.get("distinct_title")
            sku_base, dim_chip = _split_sku_code(f.get("sku_code", ""))
            fam_cards.append({
                "name": (f"{f['family']} — {dt}" if dt else f["family"]),
                "subcategory": f.get("subcategory"),
                "sku_code_base": sku_base, "dim_chip": dim_chip,
                "url": family_url(cat_slug, f["family_slug"]),
                "thumb": thumb,
                "variant_count": len(variants),
            })
        if not fam_cards:
            continue
        meta = CATEGORIES_META.get(cat_slug, {})
        cat_name = meta.get("name", cat_slug)
        label = data["label"]
        h1 = f"{label} {cat_name} — Malaysia"
        intro = (f"{label} range within our {cat_name.lower()} — {len(fam_cards)} model "
                 f"lines from Tanko, distributed in Malaysia by Primaxs. Compare options and request a quote.")
        sub_canonical = f"https://www.storagesystem.com.my/{cat_slug}/{sub_slug}/"
        json_ld_sub = graph_ld(
            *_org_graph_nodes(),
            breadcrumb_ld([
                (cat_name, f"https://www.storagesystem.com.my/{cat_slug}/"),
                (label, sub_canonical),
            ]),
            collection_page_ld(
                name=h1,
                url=sub_canonical,
                description=intro,
                item_urls=[f"https://www.storagesystem.com.my/{c['url']}" for c in fam_cards],
            ),
        )
        # LCP preload — first family thumbnail, WebP form
        sub_lcp_img = next((c["thumb"] for c in fam_cards if c.get("thumb")), None)
        sub_lcp_webp = (sub_lcp_img.rsplit(".", 1)[0] + ".webp") if sub_lcp_img else None
        html = env.get_template("category.html").render(
            page_title=f"{label} {cat_name} Malaysia | Primaxs"[:62],
            meta_description=intro[:158],
            canonical=sub_canonical,
            preload_image=sub_lcp_webp,
            category={"name": f"{label} {cat_name}", "h1": h1, "intro": intro},
            families=fam_cards,
            subcollection_nav=_subcollection_pills(cat_slug, sub_slug),
            base_url=BASE_URL, year=YEAR, json_ld=json_ld_sub,
        )
        write(os.path.join(DIST, cat_slug, sub_slug, "index.html"), html)
        built += 1
    return built


def main():
    print("Building Primaxs site...")
    products, families, categories = load_data()

    # Populate nav mega-menu categories (used by base.html on every page)
    env.globals["nav_categories"] = [
        {"slug": s, "name": CATEGORIES_META[s]["name"], "tagline": CATEGORIES_META[s]["tagline"]}
        for s in CATEGORY_ORDER
    ]

    print("  clearing dist/")
    clear_dist()
    print("  copying static assets")
    copy_static()

    # Build homepage
    print("  homepage")
    build_homepage(products, families, categories)

    print("  products index / download / guides")
    build_products_index(products)
    build_search_index(products, families)
    build_download()
    build_guides()

    # City geo pages + industry application pages
    print("  location & industry landing pages")
    n_landing = build_landing_pages()
    print(f"  -> {n_landing} landing pages")

    # Group products by family_slug (which is unique per Tanko page).
    # product_family (the human name) is shared across many pages, so grouping
    # by it collapses distinct pages together.
    prods_by_family = defaultdict(list)
    for p in products:
        if p.get("family_slug") and p.get("image_paths"):
            prods_by_family[p["family_slug"]].append(p)

    # Build ALL 11 category hub pages
    #   - For Workbenches: full family + variant pages (the sample)
    #   - For other 10: stub page so nav links resolve, families listed later
    fams_by_cat = defaultdict(list)
    for f in families:
        if f.get("category_slug"):
            fams_by_cat[f["category_slug"]].append(f)

    n_fam = n_var = 0
    for cat_slug in CATEGORY_ORDER:
        meta = CATEGORIES_META[cat_slug]
        cat_fams = fams_by_cat.get(cat_slug, [])
        build_category(cat_slug, meta, cat_fams, prods_by_family)
        for f in cat_fams:
            variants = prods_by_family.get(f["family_slug"], [])
            if not variants:
                continue
            build_family(cat_slug, meta, f, variants)
            n_fam += 1
            for v in variants:
                build_variant(cat_slug, meta, f, v, variants)
                n_var += 1
        print(f"  category [{cat_slug}]: {len(cat_fams)} families")
    print(f"  -> {n_fam} family pages, {n_var} variant pages")

    # Sub-collection SEO pages (Professional / Classic / Heavy Duty / Hooks / ...)
    print("  sub-collection SEO pages")
    n_sub = build_subcollections(families, prods_by_family)
    print(f"  -> {n_sub} sub-collection pages")

    # Real pages: About, Contact, Enquiry (with basket + Formsubmit form)
    write(os.path.join(DIST, "about", "index.html"),
          env.get_template("about.html").render(
              page_title="About Primaxs | Malaysia's Exclusive Tanko Distributor",
              meta_description="Primaxs Marketing (M) Sdn Bhd — Malaysia's exclusive Tanko industrial storage distributor. Selangor office, nationwide delivery, local warranty.",
              canonical="https://www.storagesystem.com.my/about/",
              base_url=BASE_URL, year=YEAR, json_ld=org_json_ld()))
    write(os.path.join(DIST, "contact", "index.html"),
          env.get_template("contact.html").render(
              page_title="Contact Primaxs Marketing (M) Sdn Bhd | Malaysia",
              meta_description="Contact Primaxs Marketing (M) Sdn Bhd — Selangor office, sales@storagesystem.my, +60 12-616 3088. Malaysia's exclusive Tanko distributor.",
              canonical="https://www.storagesystem.com.my/contact/",
              base_url=BASE_URL, year=YEAR, json_ld=org_json_ld()))
    write(os.path.join(DIST, "enquiry", "index.html"),
          env.get_template("enquiry.html").render(
              page_title="Request a Quote | Primaxs Malaysia",
              meta_description="Review your basket and submit a quote request to Primaxs Marketing (M) Sdn Bhd — Malaysia's exclusive Tanko distributor. Reply within one business day.",
              canonical="https://www.storagesystem.com.my/enquiry/",
              base_url=BASE_URL, year=YEAR, json_ld=org_json_ld()))

    # (applications section removed — no /applications/ page or links)

    # Custom 404 page (GitHub Pages serves 404.html at root)
    write(os.path.join(DIST, "404.html"),
          env.get_template("404.html").render(
              page_title="Page Not Found | Primaxs Malaysia",
              meta_description="The page you were looking for could not be found. Browse the Tanko industrial storage catalogue or contact Primaxs Malaysia.",
              canonical="https://www.storagesystem.com.my/",
              base_url=BASE_URL, year=YEAR, json_ld=org_json_ld()))
    print("  404 page written")

    # count outputs
    n_html = 0
    for _, _, files in os.walk(DIST):
        n_html += sum(1 for f in files if f.endswith(".html"))
    print(f"Done. {n_html} HTML files under {DIST}")

    # sitemap.xml + robots.txt (auto-regenerate on every build)
    try:
        import subprocess
        subprocess.run([sys.executable, os.path.join(ROOT, "gen_sitemap.py")],
                       check=False, capture_output=True)
        print("  sitemap.xml + robots.txt regenerated")
    except Exception as e:
        print(f"  ! sitemap gen skipped: {e}")


if __name__ == "__main__":
    main()
