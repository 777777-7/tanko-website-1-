# Full-site audit — 16 September 2026

Every page on the site scanned (1,854 files), plus content, commercial, local,
accessibility, performance and competitive perspectives. One real bug found and
fixed; everything else is either clean, a deliberate decision, or a judgement
call left for Wei Ming.

---

## 1. Technical SEO — clean

Scanned all 1,854 pages. These came back **zero**:

| Check | Result |
|---|---|
| Missing `<title>` / description / `<h1>` | 0 |
| Duplicate titles / duplicate descriptions | 0 |
| Missing or mismatched canonical | 0 |
| `og:url` not matching canonical | 0 |
| Missing `og:title` / `og:description` / `og:image` | 0 |
| `og:image` files that don't exist | 0 of 1,851 |
| Missing `alt` on `<img>` | 0 |
| Broken `<img src>` | 0 |
| Broken `srcset` entries | 0 |
| Broken internal links | 0 |
| Pages with 0 or 2+ `<h1>` | 0 |
| Heading level skips (h1→h3) | 0 |
| Images without width/height (layout shift) | 0 |
| Missing `twitter:card` | 0 |
| Invalid JSON-LD | 0 of 1,859 blocks |
| Sitemap URLs that don't exist | 0 |
| Pages missing from sitemap | 0 of 1,851 indexable |
| `http://` / mixed content | 0 |
| Orphan pages | 0 (except two deliberately noindexed) |

Sitemap count (1,851) matches indexable page count exactly.

### The one real bug — fixed

`docs/asset3/` holds **4,306 files and every one is `.webp`**. Not a single
`.jpg`. But 250 pages declared a Product schema image at
`/asset3/<name>.jpg` — **341 URLs, all 404**.

Cause: commit `af50d47d2c` ("Product and Article schema images to JPEG")
rewrote the extensions on 11 September without the `.jpg` files ever existing.

Effect: every time Google validated one of those products it fetched a dead
image. Wasted crawl budget, and a structured-data error that can suppress the
product thumbnail in results.

Fixed in `b51adb3d02`:
- 231 pages — dead URL dropped. `image[0]` (`/feed-img/…jpg`) and `image[1]`
  are real, and `image[0]` is the one Google uses, so nothing was lost.
- 19 pages — the dead URL was the *only* image, so it was repointed at the
  `.webp` that exists.

Verified after: 1,680 asset3 schema image URLs, **0 missing**. No title, h1,
description or visible content was touched.

---

## 2. Structured data — strong

| Type | Pages |
|---|---|
| BreadcrumbList | 1,850 |
| FAQPage | 1,661 |
| Product | 1,591 |
| Organization / LocalBusiness | 232 / 231 |
| ProductGroup | 153 |
| CollectionPage | 55 |
| Article | 29 |

Only `404.html`, `/review/` and `/sales/` lack breadcrumbs, and all three are
correctly excluded from search.

**74 products carry no price** in their Offer. This is Wei Ming's deliberate
decision and is left alone. It does mean those 74 cannot win a price-bearing
rich result.

---

## 3. Content quality — the real weakness

| Words in `<main>` | Pages |
|---|---|
| under 100 | 31 |
| 100–249 | 75 |
| 250–499 | 762 |
| 500–999 | 967 |
| 1,000+ | 19 |

**100 category ("range") pages are under 250 words.** These are not SKU pages —
they are the pages meant to rank for commercial terms. The thinnest:

```
 70w  /perforated-board/kp-42/
 72w  /perforated-board/kp-44/
 75w  /perforated-board/kp-43/
 75w  /perforated-board/te_211/
 76w  /perforated-board/kp-17/
```

This is the most likely explanation for **1,228 pages sitting in "discovered,
currently not indexed"** in Search Console. Google found them, looked, and did
not think they were worth indexing. No amount of waiting fixes a 70-word page.

Fixing this is real work — roughly 150–200 words each of genuine specification
and application text — and it is the single highest-value thing left on the
site.

---

## 4. Cannibalisation — still present, deliberately

Nine guide↔category pairs still target the same phrase:

```
/guides/perforated-board-shadow-board-tool-control-malaysia/
   vs /perforated-board/perforated-board/     shared: boards, perforated, shadow
/guides/cnc-tool-storage-management-malaysia/
   vs /cnc-tool/cnc-trolley/, /cnc-tool/enr-12/, /cnc-tool/ens-1/,
      /cnc-tool/ens-3/, /industries/cnc-machining-tool-room/
/guides/hanger-rack-louvre-panel-bin-storage-malaysia/
   vs /hanger-rack/hanger-rack/               shared: hanger, louvre, panel
/guides/heavy-duty-workbench-fabrication-welding-malaysia/
   vs /workbench/heavy-duty/                  shared: duty, heavy, workbenches
/guides/stainless-steel-workbench-food-pharma-malaysia/
   vs /industries/food-beverage-processing/   shared: food, stainless, workbenches
```

The fix for this was reverted in `064efd69a5` because my retitle script
corrupted two `<h1>` tags. **Left as-is on purpose** until the 14–16 September
Search Console data arrives and we know whether titles were ever the problem.

Separately, groups of model-line pages carry near-identical titles differing
only by model code (`/workbench/wd-48/`, `/wd-58/`, `/wd-68/`). Mild, and
probably not worth touching.

---

## 5. Commercial / conversion — good

- **0** product pages missing a quote or WhatsApp CTA.
- 12 product pages show no RM price in the body (subset of the 74 unpriced).
- Enquiry form: every field properly wrapped in a `<label>` — accessible.
- Free delivery / free installation offer present.

---

## 6. Local SEO — one thing to check

Three different phone numbers appear across the site:

| Number | Where |
|---|---|
| `+60-3-4296-4737` | LocalBusiness schema — **this is what Google reads as the NAP** |
| `+60 12-616 3088` | page body, 2,094 pages |
| `+60 11-5841 9886` | WhatsApp links, 1,856 pages |

Having several numbers is normal for a business, but the **schema number must
match the Google Business Profile primary number exactly**, or the NAP signal
is diluted. Worth one check in GBP.

Address in schema is complete and consistent:
No. 39, Jalan Balakong Jaya 4, Taman Industri Balakong Jaya, 43300 Seri
Kembangan, Selangor, MY.

`sales@storagesystem.my` (3,947 pages) — **verified working**: the domain has a
live MX record. Not a typo for `.com.my`, which has no MX at all.

---

## 7. Trust / E-E-A-T — gaps

Present: about, contact, returns, downloads, locations.

**Missing: privacy policy, terms & conditions, shipping policy, warranty page.**

For a B2B supplier asking for quotes and holding enquiry data, a privacy policy
is close to mandatory — and Google treats these pages as trust signals. Four
short pages. Worth doing after the freeze.

---

## 8. Accessibility

- Forms correctly labelled.
- Alt text on every image.
- No heading skips.
- **No skip-to-content link on any page** — the one real gap. It is a template
  change touching all 1,854 pages, so it should wait until the freeze ends.

---

## 9. Performance

| | |
|---|---|
| Median page | 44.6 KB |
| Heaviest page | 145 KB (`/tool-cabinet/ekc/`) |
| Total assets | 417.9 MB across 15,482 files |
| Heaviest asset | `tanko-catalogue-e147.pdf` — **11.7 MB** |

The 11.7 MB catalogue on `/download/` is the only performance concern, and only
for people who click it. Analytics present on every page. Caching headers set
correctly (immutable, 1 year on `/asset3/`).

---

## 10. Internal linking — healthy

| Page type | Count | Min inbound | Median |
|---|---|---|---|
| SKU | 1,591 | 2 | 13 |
| Range | 188 | 2 | 20 |
| Guide | 30 | 2 | high |
| Location | 11 | 3 | high |

No orphans apart from the two deliberately noindexed pages.

---

## What is worth doing next, in order

1. **Write the 100 thin category pages up to ~250 words.** Biggest lever on the
   site. Directly addresses 1,228 unindexed pages.
2. **Add privacy, terms, shipping, warranty pages.** Four short pages, real
   trust signal.
3. **Check the GBP phone matches the schema phone.**
4. **Decide the cannibalisation question** once 14–16 Sep GSC data lands.
5. **Add a skip-link** to the template.
6. **Links.** Still 2 referring domains against competitors' 11+. Nothing on
   the site fixes this; it is the off-site constraint.

None of 1–6 is a bug. The site as it stands is technically sound.
