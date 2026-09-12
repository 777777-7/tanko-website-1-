# Why we are not ranking #1, and what actually changes it

Measured 13 September 2026. Every number below comes from Search Console, Bing
Webmaster Tools, or a live SERP check — nothing is estimated.

---

## 1. The single clearest fact

90 days of Search Console: **238 queries, 2,150 impressions, 9 clicks.**

| Where we sit | Impressions | Clicks | CTR |
|---|--:|--:|--:|
| Page 1 (position ≤10) | 97 | 7 | **7.2%** |
| Page 2 (11–20) | 75 | 1 | 1.3% |
| **Page 3+ (21+)** | **1,978** | **1** | **0.05%** |

**92% of our impressions are on page 3 or worse.** They convert to nothing.
This is not a click-through-rate problem, a title problem or an image problem.
Every one of those is already fixed. It is a *position* problem.

The demand is real and we are nowhere near it:

| Query | Impressions | Our position |
|---|--:|--:|
| tool cabinet malaysia | 110 | **43.5** |
| tool cabinet | 96 | 55.6 |
| warehouse storage malaysia | 81 | 83.0 |
| heavy duty tools cabinet | 68 | 40.2 |
| tool cabinet heavy duty | 66 | 41.9 |
| tools storage cabinet | 57 | 41.0 |

Compare what we *do* win:

| Query | Position | CTR |
|---|--:|--:|
| primaxs | 1.2 | 50% |
| tanko malaysia | 3.2 | 20% |
| tool display board | 5.8 | 22% |
| perforated board | 8.4 | 12.5% |

The pattern is unmistakable: **we rank for our own brand and for terms nobody
competes on. We are on page 4–8 for everything with commercial volume.**

---

## 2. The reason: authority, and there is no way around it

You do not move from position 43 to position 1 with on-page work. Positions
40–80 against established sellers is an authority gap. Authority is links.

| | storagesystem.com.my | knightauto.com.my (#1) |
|---|--:|--:|
| Web mentions of the domain | **1,170** | **104,000** |
| External sites Google shows linking us | **2** (Facebook, NEWPAGES) | 7+ on page one alone |
| Referring domains in Bing Webmaster | **none recorded** | — |

And the site is **three weeks old** — the repository was created 24 August 2026.

Google does not hand a three-week-old site with two referring domains the #1
spot over a decade-old supplier. Nothing on the page changes that.

---

## 3. ⚠ The finding that matters most

**`storagesystem.my` — the domain in your own email address — issues a
permanent 301 redirect to `tanko.com.tw`.**

```
http://storagesystem.my  ->  301 Moved Permanently  ->  https://tanko.com.tw/
```

A 301 is the strongest redirect there is; it passes essentially all of a
domain's accumulated authority to the destination. So:

- Every link anyone has ever made to `storagesystem.my` since 2006 is
  **crediting Tanko, not Primaxs**
- Every customer who reads `sales@storagesystem.my` on a quotation, a business
  card or Tanko's own contact page and types that domain into a browser lands on
  **your supplier's Taiwanese site**, not your catalogue
- Your own brand equity is being donated to the manufacturer

**This is a DNS/hosting change only you can make, and it is the highest-value
thing on this entire list.** Point `storagesystem.my` at
`https://www.storagesystem.com.my/` with a 301 instead. It costs nothing, takes
minutes, and it stops the leak permanently.

---

## 4. "Rank #1 for every product" — the honest answer

No site ranks #1 for every product. Not Knight Auto, not RS Components. What is
achievable is **page one for the terms that convert**, and on a three-week-old
domain the order matters.

**We already win where competition is thin.** Live checks today:

| Query | Our position |
|---|--:|
| `"EGA-10061"` (SKU code) | **#2** — behind only Tanko itself |
| `BT-40 tool trolley malaysia` | **#4** |
| `perforated board malaysia` | **#3** |

That is the whole strategy, and it is already working. With 619 real SKUs, every
model code, taper size and specification is a term we can own outright *now*,
while the head terms remain out of reach for at least a year.

Head terms like "tool cabinet malaysia" are a 2027 target, not a 2026 one.

---

## 5. What actually moves this, in order of value

| # | Action | Who | Value |
|---|---|---|---|
| 1 | **Repoint `storagesystem.my` → `storagesystem.com.my`** | Wei Ming (DNS) | Highest. Stops a permanent authority leak. |
| 2 | **Tanko adds our website to their distributor page** | Emailed 12 Sep | A link from the manufacturer is the most relevant link that exists in this industry. |
| 3 | **Google reviews** — 4 so far, at 5.0 | Wei Ming | Drives the map pack, which is where local B2B buyers actually click. |
| 4 | Indexation: 1,228 pages still "discovered, not indexed" | In progress | Cannot rank what is not indexed. Internal linking was rebuilt 12 Sep; needs weeks. |
| 5 | NEWPAGES paid tier — *only if* they confirm per-product followed links | Emailed 12 Sep | Their sites hold #1 and #2 for our head terms. Worth knowing the mechanism. |
| 6 | InfoPages record 15738 — add the website link | Emailed 12 Sep | Currently name/address/phone only, no link. |
| 7 | Trade association listings (FMM, MATRADE) | Wei Ming — costs money | Real, relevant links. Membership decision, not a technical one. |
| 8 | Customer and supplier links | Wei Ming | The most durable links a B2B supplier gets, and the hardest to buy. |

**What is *not* worth doing:** mass directory submission. Low-quality links do
not move a site from 43 to 1, and Google discounts or penalises them. Two
excellent links beat two hundred poor ones.

---

## 6. What has already been done on-site

These are finished and correct; they are not the bottleneck:

- 0 identical product descriptions (was 1,504 near-twins)
- Every mother page owns its cluster of trade names
- Internal linking rebuilt — 0 orphaned pages, median inbound links 7 → 13
- Preview images: 1,841 pages at 1200×1200, 0 broken, 0 missing
- Schema, sitemaps, IndexNow, hreflang, breadcrumbs all clean

The on-page work is done. **The remaining gap is entirely off-page.**
