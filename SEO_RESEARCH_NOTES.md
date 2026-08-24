# SEO Research Notes — 2026-08-24

Compiled during the overnight autonomous session to guide the technical SEO
pass on primaxs.com.my. Each section cites the source that informed the
decision; every claim below either drove a change in this codebase or is
carried forward as a recommendation.

---

## 1. Core Web Vitals thresholds (2026)

Google grades three field metrics at the **75th percentile of real users
over a 28-day rolling window** in the Chrome User Experience Report (CrUX).
A page passes only when **all three** are "good".

| Metric | Good  | Needs improvement | Poor  |
|--------|-------|-------------------|-------|
| LCP    | ≤ 2.5s | 2.5 – 4.0s        | > 4.0s |
| INP    | ≤ 200ms | 200 – 500ms       | > 500ms |
| CLS    | ≤ 0.1  | 0.1 – 0.25        | > 0.25 |

- The March 2026 core update strengthened the ranking weight of these
  metrics — sites that pass rise, sites that fail fall, sometimes sharply.
- INP replaced FID in March 2024 and is now fully in effect for 2026.

Sources:
- [Core Web Vitals 2026 — thresholds & SEO impact (Meteora)](https://meteoraweb.com/en/analisi-dei-dati-e-metriche/core-web-vitals-2026-lcp-inp-cls-thresholds-and-seo-impact)
- [Most important Core Web Vitals metrics in 2026 (NitroPack)](https://nitropack.io/blog/most-important-core-web-vitals-metrics/)
- [Core Web Vitals Guide 2026 (W3Era)](https://www.w3era.com/blog/seo/core-web-vitals-guide/)

**Applied to this site:**
- Google Fonts are `preconnect`ed and loaded with `display=swap` (no FOIT).
- Product images use `loading="lazy"` on everything except the LCP element
  in each family/variant hero.
- Site.css is a single file (126KB) — no render-blocking third-party CSS.
- JS is `defer`-loaded and total shipped JS is ~30 KB (basket, picker,
  search, product tabs) — well under any INP concern.
- The one remaining CWV risk is oversized product PNGs in `asset3/`
  (~1 GB, ~1100 files 500KB–1MB, 10 over 1MB). See §7 for the follow-up.

---

## 2. Google's search results landscape in 2026 (AI Overviews)

- Google AI Overviews now appear on ~31% of SERPs (up from ~10k queries in
  Aug 2024 to ~173k by May 2025).
- Ranking #1 organically is worth less than being *cited inside* an AI
  Overview, a featured snippet, or a "People also ask" box.
- Google places heavier weight on demonstrated first-hand experience and
  original content over generic industry writeups.

Sources:
- [10 B2B SEO Best Practices for Pipeline Growth in 2026 (Fame)](https://www.fame.so/post/10-actionable-b2b-seo-best-practices-for-pipeline-growth-in-2026)
- [8 B2B SEO Best Practices for 2026 (Directive)](https://directiveconsulting.com/blog/b2b-seo-best-practices/)
- [B2B SEO Best Practices for 2026 (Grey Matter)](https://gogreymatter.com/blog/b2b-seo-best-practices/)

**Applied to this site:**
- Every family and variant page carries `Product` schema + `BreadcrumbList`
  schema — the exact data required to be selected as an AI-Overview source.
- Every guide article carries `Article` + `FAQPage` + `BreadcrumbList` —
  FAQPage schema is the highest-hit pattern for AI Overview inclusion.
- Copy leads with a direct answer (product spec, buyer guidance) instead of
  a keyword-stuffed intro paragraph. AI extractors prefer answer-first
  40–60-word sections.

---

## 3. Answer Engine Optimization (ChatGPT / Perplexity / Claude)

- ChatGPT Search has **~87 % citation overlap with Bing** — Bing indexation
  is prerequisite for ChatGPT visibility.
- Perplexity indexes new content in days if `PerplexityBot` is permitted.
- ChatGPT Search takes 1–3 weeks for new content to surface.
- All major answer engines respect standard robots.txt directives.

Sources:
- [Answer Engine Optimization: Complete AEO Guide 2026 (Frase)](https://www.frase.io/blog/what-is-answer-engine-optimization-the-complete-guide-to-getting-cited-by-ai)
- [How to get cited by ChatGPT / Perplexity / Google AI 2026 (ChatFeatured)](https://blog.chatfeatured.com/how-to-get-cited-by-chatgpt-perplexity-and-google-ai-the-2026-guide)
- [AEO Checklist 2026 (AuthorityTech)](https://authoritytech.io/curated/answer-engine-optimization-checklist-chatgpt-perplexity-claude-2026)
- [Robots.txt & AI Crawlers in 2026 (DataImpulse)](https://dataimpulse.com/blog/robots-txt-ai-crawlers/)
- [AI Crawler Management 2026 (AliceLabs)](https://alicelabs.ai/en/insights/ai-crawler-management)

**Applied to this site:**

- `robots.txt` explicitly `Allow`s every real-time AI answer bot:
  `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Perplexity-User`,
  `Claude-SearchBot`, `Claude-User`, `ClaudeBot`, `Applebot`,
  `Applebot-Extended`.
- Training crawlers `GPTBot`, `Google-Extended`, `anthropic-ai`, `CCBot`
  are also allowed — the business goal is B2B brand and product visibility,
  and blocking training crawlers means Primaxs is invisible to future
  models that would otherwise reference it.
- Aggressive scrapers (`Bytespider`) are blocked.
- Content is answer-first: FAQ sections on every variant page directly
  answer buyer questions (dimensions, stock, bulk, warranty).

---

## 4. Structured data (schema.org JSON-LD)

Google's rich-result eligibility for the categories that matter here:

| Page type       | Schema now emitted                                      |
|-----------------|---------------------------------------------------------|
| Homepage        | Organization, LocalBusiness, WebSite (+SearchAction)    |
| Products index  | Organization, LocalBusiness, WebSite, BreadcrumbList, CollectionPage |
| Category        | Organization, LocalBusiness, BreadcrumbList, CollectionPage |
| Sub-collection  | Organization, LocalBusiness, BreadcrumbList, CollectionPage |
| Family          | Organization, LocalBusiness, BreadcrumbList, Product (with hasVariant) |
| Variant         | Product, BreadcrumbList                                 |
| Guides index    | Organization, LocalBusiness, WebSite, BreadcrumbList, CollectionPage |
| Guide article   | Article, BreadcrumbList, FAQPage                        |
| About / Contact | Organization, LocalBusiness, WebSite                    |

The `LocalBusiness` node now includes a full `PostalAddress` (Balakong Jaya
street, Selangor, 43300 MY), `telephone`, `email`, and `logo` — the
minimum Google requires for a Local rich result. Manual verification of a
sample page's JSON should be run once via Google's Rich Results Test after
the site is live: <https://search.google.com/test/rich-results>.

Sources:
- [Local Business Schema JSON-LD examples](https://jsonld.com/local-business/)
- [LocalBusiness — schema.org spec](https://schema.org/LocalBusiness)

---

## 5. Meta title + description discipline

Best practice for 2026:
- Title tag under ~60 characters (Google truncates around 55–60 in mobile
  SERPs).
- Description under 155–160 characters.
- Every URL should have a unique title and unique description.

Sources:
- [Google Search Console best practices 2026 (SalesHive)](https://saleshive.com/blog/google-search-console-best-practices-use-2025)
- [SEO best practices 2026 (Whitehat)](https://whitehat-seo.co.uk/blog/seo-basics)

**Applied to this site:**
- Variant title suffix trimmed from " | Primaxs Malaysia" (18 char) to
  " | Primaxs" (10 char); max_len reduced 70 → 60. Result: pages with
  over-length titles dropped from **1,355 → 11** (remaining 11 are guide
  titles + category index titles, all under 68 chars — acceptable).
- Family titles now include the base SKU code when multiple families share
  a name (`Steel Top Workbench — Standard (WD)` vs `(WD1200)` vs `(WD1500)`).
  Duplicate titles across the sitemap dropped from **29 pairs → 1 pair**.
- Guide meta descriptions all trimmed to ≤ 155 chars.
- Duplicate meta descriptions dropped from **17 → 0**.

---

## 6. Content architecture & topical authority

- Pillar-and-cluster model builds topical authority: one comprehensive
  pillar per topic (e.g., "Tool cabinet buying guide") with clusters of
  supporting content (specific SKU comparisons, use-case pages, FAQs).
- Content should be segmented by ICP vertical (automotive workshop, MRO,
  factory production line) rather than by keyword.

**Applied to this site:**
- 10 buying-guide articles already published, each targeting a distinct
  pillar (workbench, tool cabinet, CNC storage, locker, workstation/5S,
  perforated board, small-parts, racking, "Tanko vs importing", and the
  category overview).
- Every guide links to relevant category and family pages (natural
  clustering).
- Every family page is 1 click from its category, 2 clicks from home.

**Opportunity (deferred, does not block launch):** 3–5 more cluster pages
under the highest-intent verticals — e.g., "Automotive workshop tool
cabinet configuration guide (Malaysia)", "Warehouse racking safe stacking
practices", "ESD workbench requirements for electronics assembly". These
add mid-funnel query surface area without requiring new SKUs.

---

## 7. Image weight — key follow-up

`asset3/` mirrors the product photography from tanko. As of tonight:

- 2,151 files, ~1.07 GB total
- 10 files over 1 MB
- 1,107 files 512 KB – 1 MB
- 679 files 256 – 512 KB
- 195 files 100 – 256 KB
- 160 files under 100 KB

Individual product photos of 500 KB – 1 MB are LCP-hostile — a category or
family page loading a 900 KB hero on 4G will fail the 2.5 s LCP target for
Malaysian mobile users.

**Recommendation (needs user approval before running — mass rename is
destructive):** convert opaque product PNGs to JPEG quality 82 progressive
and resize any dimension over 1600px. Expected savings ~75 %, taking the
folder from ~1 GB to ~250 MB and dropping the average hero image from
~700 KB to ~150 KB.

`asset_content/` (289 MB, 4,281 files) is mostly fine — 3,631 files
already under 100 KB — the 14 files over 250 KB there are hexagonal
workbench photos and could be re-encoded in the same pass.

The compression script would also need to update every path in
`products.json` and the built HTML (PNG → JPG rename). Held for morning
review — see `MORNING_HANDOFF.md`.

---

## 8. Google Search Console + Bing Webmaster setup

- GSC is the primary source of truth for query data, index coverage, and
  CWV field metrics.
- Bing Webmaster Tools matters more than it used to because ChatGPT Search
  reads Bing's index — being missing from Bing means being missing from
  ChatGPT citations.

Full step-by-step handoff for the user is in
[`MORNING_HANDOFF.md`](MORNING_HANDOFF.md), including verification
options (DNS TXT, HTML meta tag, HTML file upload) and how to submit
`https://primaxs.com.my/sitemap.xml`.

---

## 9. What was NOT changed and why

- **Prices:** kept off every page. Standing rule.
- **Reviews / testimonials / staff photos / award badges:** not fabricated.
  Standing rule.
- **URL structure:** unchanged. Existing routes work; changing slugs would
  cost more in redirect complexity than it would gain in keyword tuning.
- **Client-side rendering:** no framework added. Every page is fully
  server-rendered HTML — bots see the full content, no JS execution
  needed. This is a foundational advantage vs SPA competitors.
- **Third-party analytics:** not added tonight. When the user is ready,
  GA4 or Plausible can be dropped into `base.html` in one edit.

---

## Summary of concrete changes made tonight

1. `sitemap.xml` (1,798 URLs) + `robots.txt` generated, wired into
   `build.py` so every rebuild refreshes them. Robots explicitly welcomes
   AI answer engines.
2. LocalBusiness schema now carries full PostalAddress + phone + email.
3. WebSite (+ SearchAction) schema added on home and all top-level indexes.
4. BreadcrumbList added on every product/category/subcollection/guide URL.
5. CollectionPage schema added on category, sub-collection, products index,
   guides index.
6. Family pages emit aggregate `Product` schema with `hasVariant`.
7. Variant page titles cut to under 60 chars, distinct across the sitemap.
8. Family page titles disambiguated by SKU code — duplicates 29 → 1.
9. Guide meta descriptions all under 155 chars; no over-length remaining.
10. All 4 empty-alt images fixed at template source.
11. All 1,799 pages: exactly one H1, no missing meta, no orphan URLs.
