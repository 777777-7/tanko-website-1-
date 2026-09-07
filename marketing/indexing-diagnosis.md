# Why 1,228 pages are not in Google — diagnosed

**7 Sep 2026.** From Google Search Console, `storagesystem.com.my`.

```
Indexed             602
Not indexed       1,240
  Not found (404)     10    <- fixed, see below
  Discovered - currently not indexed   1,228
  Crawled - currently not indexed          1
```

---

## The 404s: fixed

Google reported 10 URLs returning 404. The cause was a link written
`href="workbench/"` instead of `href="/workbench/"`. On a page at
`/guides/foo/` that resolves to `/guides/foo/workbench/`, which does not exist.

**There were 173 of them across 39 files** — Google had simply not crawled the
rest yet, so the count was going to keep climbing. All 173 are fixed; every
destination was verified to exist first. Zero relative `href`s remain in `docs/`,
and the generator under `site/` never had the bug, so it will not regress.

One entry in the GSC list, `/tool-cabinet/ea-12/ea-12072t/`, **returns 200 and is
in the sitemap** — that report is stale (last crawled 30 Aug) and clears itself
on revalidation.

---

## The 1,228: not a bug, and worth understanding before "fixing"

**"Discovered – currently not indexed"** means Google found the URL, usually via
the sitemap, and **chose not to spend crawl budget on it.** It is not an error,
not a penalty, and not something a code change makes go away.

### The measurement

Two adjacent product pages, compared on their `<main>` content:

```
/cnc-tool/ea-10mn/ea-10031-111mn/
/cnc-tool/ea-10mn/ea-10031-222mn/

similarity: 99.1%
```

The complete list of differences between them:

| | Page A | Page B |
|---|---|---|
| SKU string | EA-10031-111MN | EA-10031-222MN |
| Price | 4631 | 4718 |
| Taper | BT-30 | BT-40 |

Everything else — all 479 words — is identical. Five sibling SKUs in that family
all came out at exactly 479 words.

**That is the textbook signature of the "Discovered – not indexed" state.** Google
sampled a handful of the 1,700 product pages, found them near-identical, and
concluded the rest were not worth crawling. On a site with 33 search clicks a
month and very few inbound links, the crawl budget it allocates is small, and it
spends it on the pages that differ from each other.

### What this is *not*

- Not a robots.txt or sitemap problem — the URLs are discovered fine.
- Not a rendering or speed problem — the 602 indexed pages prove crawling works.
- Not something more internal links will fix on its own.

---

## The three honest options

### 1. Accept it

1,700 near-identical SKU pages do not each need to rank. What actually ranks and
converts is the category pages, the 28 guides, the location and industry pages,
and now `/tanko/`. Those are indexed. A quote-only B2B catalogue does not need
every variant in the index to sell.

**This is a legitimate choice and costs nothing.**

### 2. Consolidate — the standard fix

Keep the **family** pages indexable (`/cnc-tool/ea-10mn/`) and put a full variant
table on each — every SKU, price, dimensions and taper in one comparable place.
Set the individual variant pages to `noindex, follow`, so they stay reachable for
people and keep passing link equity, but stop competing with each other.

Effect: roughly 1,700 thin pages collapse into a few hundred genuinely useful
ones. Crawl budget concentrates. The family pages get stronger because the
content that was scattered across near-duplicates is now on one page.

Trade-off: a search for a bare SKU like "EA-10031-111MN" would land on the family
page rather than a dedicated page. Given those pages are **not indexed today**,
nothing is actually being given up.

**This is the recommended option if anything is done at all.**

### 3. Differentiate every SKU

Genuinely unique content on each of 1,700 pages — real application notes, photos,
use cases. Correct in principle, not realistic at this scale, and would take
months.

---

## The uncomfortable part

The deeper cause is **authority, not markup**. Google crawls a site as much as it
thinks the site is worth. 33 clicks a month and almost no inbound links buys very
little crawl budget, and no amount of technical tidying changes that.

What raises it is the unglamorous list already in
[`growth-audit.md`](growth-audit.md):

1. **Google reviews** — the profile sits at 3, two of which say nothing
2. **Real citations** — NEWPAGES, Yellow Pages, the directory cleanup
3. **Inbound links** — supplier directories, association listings, MOF registration
4. Time

Option 2 above is worth doing and will help. But it is second-order next to
having ten real reviews and a corrected NEWPAGES listing.

---

## Recommended sequence

| # | Action | Effort |
|---|---|---|
| 1 | 404 fix — **done, deployed** | — |
| 2 | Let Google revalidate the 404s (already started 7 Sep) | none |
| 3 | The authority work in `growth-audit.md` — reviews first | Wei Ming |
| 4 | Decide on consolidation (option 2) once 1–3 are moving | a day's work |

Do not request indexing on 1,228 URLs by hand. It does not override the quality
assessment, and it burns the daily quota that is better spent on new guides and
category pages.
