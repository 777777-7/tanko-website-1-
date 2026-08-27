# SEO Optimization Summary — www.storagesystem.my (Tanko Malaysia site)

Date: 27 Aug 2026. All changes were made to the source (`site/`, `gen_sitemap.py`,
`asset_content/`, `product_content*.json`) and the site was rebuilt into `docs/`
(1806 HTML pages). `docs/` is the deploy folder — point Cloudflare Pages at it.

## What was fixed / improved

### 0. Deployed on Cloudflare — domain now `https://www.storagesystem.com.my`
- All canonical tags, JSON-LD schema (`@id`, `url`, `logo`, `image`), sitemap URLs,
  robots.txt `Sitemap:` line and every internal link now use
  **https://www.storagesystem.com.my**.
- Site rebuilt **root-hosted** (`BASE_URL=/`) so `storagesystem.com.my/` is the
  homepage (no more `/tanko-website-1/` sub-path).
- Email `sales@storagesystem.my` kept as-is (mailbox unchanged).
- **Cloudflare Pages setup:** upload the `docs/` folder as the site root
  (Build output directory = `docs`). Both `storagesystem.com.my` and
  `www.storagesystem.com.my` resolve to Cloudflare already.

### 2. Broken internal links fixed (10 guides)
- Guide articles linked to non-existent URLs like `/workbenches/`, `/tool-cabinets/`,
  `/lockers/`, etc. Added `_fix_guide_links()` in `build.py` that maps legacy slugs to
  the real category URLs (`/workbench/`, `/tool-cabinet/`, `/locker/`, …) and prefixes
  `base_url` so links work on the GitHub Pages sub-path too.
- **Verified: 1803 pages, 0 broken internal links.**

### 3. GSC + GA4 now config-driven (no placeholder junk in output)
- `site/build.py` reads `GSC_VERIFICATION` and `GA4_ID` from the environment.
- When unset, the meta tag / GA snippet are **omitted entirely** instead of shipping
  `PLACEHOLDER_REPLACE_WITH_GSC_TOKEN` / `G-XXXXXXXXXX` to real users.
- To enable once you have the tokens:
  - `$env:GSC_VERIFICATION="<token>"; $env:GA4_ID="G-XXXX"; python site/build.py`

### 4. Conversion elements added (Malaysia B2B = WhatsApp)
- Floating WhatsApp button on every page → `wa.me/60126163088`.
- WhatsApp links added to the footer, Contact page and the enquiry note.
- LocalBusiness schema now includes `contactPoint` (sales, +60 12-616 3088,
  languages en/ms/zh), `geo` coordinates, and `openingHoursSpecification`.

### 5. Branding / share assets added
- Favicon set (`favicon.ico`, 16/32 px, `apple-touch-icon.png`).
- Proper 1200×630 Open Graph / Twitter card image (`assets/primaxs-og-1200x630.png`)
  used as the default `og:image` + `twitter:image` on the homepage.
- Custom `404.html`.

### 6. Performance / Core Web Vitals
- Converted **878 opaque product-editorial PNGs → JPG (q82)** in `asset_content/`
  (~70 MB → ~27 MB). 30 transparent PNGs were kept as PNG.
- Updated references in `product_content.json` / `product_content_v2.json` accordingly.
- **Verified: 22,356 asset references, 0 missing files.**
- Lazy-loading, `fetchpriority="high"` on the hero, async GA — already in place.

### 7. New high-intent cluster content (3 new guides → 13 total)
- `esd-anti-static-workbench-malaysia` — ESD/anti-static benches for electronics/EMS
- `stainless-steel-workbench-food-pharma-malaysia` — food/pharma/lab hygienic design
- `heavy-duty-workbench-fabrication-welding-malaysia` — fabrication/welding shops
- Each with original body copy, internal links to real category pages, FAQ section,
  and FAQPage structured data. Auto-included in sitemap + guides nav + search index.

### 8. Category pages enriched (11 categories — SEO + UX)
- Every category page now has a **FAQ section + FAQPage schema** (3–5 original,
  Malaysia-focused Q&As each) targeting featured snippets.
- **Related guides** block added on each category page, strengthening internal
  linking to the guide content.
- Trust/marketing call-out on every category page (exclusive distributor,
  nationwide delivery, Ringgit pricing, local warranty).

### 9. New differentiated content (based on tanko.tw + Malaysia buyer research)
- `tanko-workbench-pricing-quote-guide-malaysia` — answers the "how much / price
  Malaysia" search intent honestly: quote-based B2B pricing, what drives cost, how
  to get a quotation. **No public prices published** (pricing stays in your uncle's
  quotations).
- `meja-kerja-industri-malaysia` — **Bahasa Malaysia** workbench buying guide
  (targets "meja kerja" searches competitors mostly ignore).
- `kabinet-alat-penyimpanan-bengkel-malaysia` — **Bahasa Malaysia** tool cabinet
  guide (targets "kabinet alat" searches).
- Malay-language content is a real differentiator: tanko.tw is Chinese-only and most
  Malaysian competitors are English-only, so these pages face little competition.

### 10. Homepage marketing & beautification
- **Trust bar** under the hero: EXCLUSIVE distributor / LOCAL Selangor stock /
  NATIONWIDE delivery / SUPPORT — key local-channel selling points for B2B buyers.
- **Industries we serve expanded from 4 → 6** rows: added Electronics & EMS and
  Food/Pharma/Labs, each linking to its dedicated guide (more internal linking).
- **Contact page**: added "Buying from us — what to expect" trust section
  (quoting, delivery, warranty & support, payment) answering Malaysian B2B
  buyer questions.

## Verification results (final build)
- HTML pages: **1806**
- Broken internal links: **0**
- Missing asset references: **0**
- Invalid JSON-LD blocks: **0** (all 1806 pages parse)
- Old-domain leftovers: **0** · Sub-path leftovers: **0**

## Technical SEO checklist (all in place)
- Canonical tags on every page → `https://www.storagesystem.com.my/...`
- `robots.txt` with `Sitemap:` line + AI answer-engine crawlers allowed
  (OAI-SearchBot, ChatGPT-User, Perplexity, Claude, Applebot, GPTBot, Google-Extended)
- `sitemap.xml` with 1805 URLs (prioritised: homepage 1.0 → variants 0.5)
- JSON-LD: Organization + LocalBusiness (geo, hours, phone) on all pages;
  Product + Offer (SKU, MYR) on variant pages; BreadcrumbList everywhere;
  FAQPage on category + guide pages; WebSite SearchAction for sitelinks
- Meta: `robots: index,follow`, geo meta (MY-10 / Seri Kembangan),
  Open Graph (locale en_MY, url, image fallback), Twitter card, theme-color
- Favicon set + 1200×630 OG share image
- `lang="en-MY"` + Malaysian content (incl. Bahasa Malaysia guides)

## How to rebuild
```
python site/build.py     # writes docs/ (upload this folder to Cloudflare Pages)
```
For GitHub Pages project sites (sub-path) use: `BASE_URL=/repo-name/ python site/build.py`

## Next steps you own
1. In **Cloudflare Pages**: create/update the project, set the **build output
   directory to `docs`** (or upload the `docs/` folder directly), and add the
   custom domain `storagesystem.com.my` (+ `www`).
2. Add the site to **Google Search Console** and submit `https://www.storagesystem.com.my/sitemap.xml`.
3. Set `GSC_VERIFICATION` + `GA4_ID` env vars and rebuild (see above).
4. **Redirect www ⇄ non-www**: in Cloudflare add a redirect rule so
   `storagesystem.com.my` → `https://www.storagesystem.com.my` (canonical host is `www`).
5. Consider creating a **Google Business Profile** for the Balakong address to feed
   the local/geo signals in the schema.
