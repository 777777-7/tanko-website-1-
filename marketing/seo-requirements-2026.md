# Everything Google wants in 2026 — checked against this site

**7 Sep 2026.** Researched, then audited item by item. Status is what the site
actually does, not what it should do.

---

## What actually changed in 2026

Four changes matter, and two of them cancel work rather than create it.

**1. AI Overviews went from a feature to the default.** They appeared on **86.7%
of business-intent searches in April 2026**, up from 56.9% a year earlier. For a
B2B supplier, the AI answer is now the first thing most buyers see.

**2. Google published its first official guidance on optimising for generative
AI in May 2026** — and the headline is reassuring: *it is still SEO*. AI
Overviews and AI Mode run on the same core ranking and quality systems as normal
Search. There is no separate discipline to learn.

**3. FAQ rich results were deprecated on 7 May 2026.** They no longer appear.
The search-appearance filter, rich result report and Rich Results Test support
were removed in June.

**4. llms.txt turned out to be nothing.** No major AI provider reads it in
production, large studies find no relationship with citation, AI crawlers do not
even request the file, and Google compared it to the keywords meta tag.

---

## The checklist

### A. Technical foundations

| Requirement | Status |
|---|---|
| HTTPS everywhere, clean 301s | **Pass** — http and apex both 301 to `https://www.` |
| Mobile-first | **Pass** — responsive, viewport on every page |
| No broken internal links | **Pass** — 0 hrefs, 0 image srcs, 0 canonicals, 0 hreflang |
| XML sitemap, accurate | **Pass** — 1,844 URLs, all resolve, `lastmod` maintained per-page |
| robots.txt, crawl budget protected | **Pass** — parameterised URLs and `/sales/` disallowed |
| Canonical on every page | **Pass** |
| Security headers | **Pass** — 5 of 5 |
| Core Web Vitals | **No field data** — GSC reports 無數據. Not a fault; there is not enough traffic yet for Google to collect it. Static signals are clean: no CLS risk, images sized and lazy, CSS 140KB |

### B. Structured data — the five types that move the needle

| Type | Status |
|---|---|
| Organization | **Pass** — sitewide |
| LocalBusiness | **Pass** — NAP, geo, hours, areaServed |
| Product | **Pass** — 1,590 with verified prices; ProductGroup variants inlined so Google can read them |
| Article | **Pass, completed today** — was missing `datePublished`, `dateModified` and `image` on all 27 guides |
| FAQPage | **Present on 1,655 pages, no longer produces rich results** — deliberately left in place. Google deprecated the feature, not the type, and unused structured data causes no harm. Removing it would be churn |
| JSON-LD only | **Pass** — no microdata anywhere |

### C. AI search / GEO

| Requirement | Status |
|---|---|
| AI crawlers explicitly allowed | **Pass** — 8 of 8: OAI-SearchBot, ChatGPT-User, PerplexityBot, Claude-SearchBot, ClaudeBot, Applebot, GPTBot, Google-Extended, CCBot |
| Aggressive scrapers blocked | **Pass** — Bytespider |
| Question-shaped headings, self-contained answers | **Partial** — the guides do this well; category pages less so |
| Content freshness signals | **Fixed today** — `dateModified` now present on all 27 guides |
| Brand mentions across external sources | **Weak — the real gap.** Brand mentions predict AI citations roughly **3x better than backlinks**. This is the Facebook groups, NEWPAGES, Yellow Pages and review work |
| llms.txt | **Deliberately not built** — see above |

### D. Content and E-E-A-T

| Requirement | Status |
|---|---|
| Intent-matched depth | **Pass** — 28 guides, 11 in Bahasa Malaysia |
| Named business, verifiable identity | **Pass** — SSM 756588-H on About and Contact, now also on `/tanko/` |
| Real specifications, not marketing copy | **Pass** |
| Images on content pages | **Fixed today** — 54 product images added; the guides previously had none |
| Case studies | **Missing** — needs 3 customers willing to be named |
| Reviews | **3 on Google, two of which say nothing.** Still the single biggest gap |

### E. Commerce surfaces

| Requirement | Status |
|---|---|
| Merchant Center free listings | **Feed built** — 1,590 products, ready to upload |
| Price visible pre-click | **Added today** — 8 category titles now carry a verified floor price |
| Accurate prices | **One error found and suppressed** — SAN-368 was public at RM113 against siblings at RM3,670–4,049 |

---

## What was done today

1. **54 product images across all 27 guides.** They had none — only the logo — so zero presence in Google Images.
2. **Article schema completed** — `datePublished`, `dateModified`, `image`.
3. **Guide prices in 8 category titles**, each checked against the real product it names.
4. **A wrong RM113 price suppressed** before a customer could hold you to it.
5. **ProductGroup variants inlined** so Google can read 1,733 variant prices.
6. **173 broken links fixed**, sitemap `lastmod` maintained per page.

---

## What is left, honestly

Everything technical is done. The audit sits at 49/50 and the last flag is a
false positive.

**What remains is not markup.** In priority order:

| # | Action | Why |
|---|---|---|
| 1 | **10 Google reviews** | Reviews are the top local ranking factor, and brand mentions predict AI citations 3x better than backlinks |
| 2 | **NEWPAGES claim** (needs the SSM cert) | Half of page one for your main query is that platform |
| 3 | **Set the real SAN-368 price** | Currently shows "on request" |
| 4 | **Keep posting** | Group posts are brand mentions, which is now a measurable AI-citation signal — not just traffic |
| 5 | Yellow Pages, BusinessList, MATRADE | Citation consistency |
| 6 | Decide on Merchant Center upload | Feed is ready |

The uncomfortable truth from the ranking data stands: the site converts at
20–29% CTR where it reaches page one. It is not a page problem. It is an
authority problem, and authority is built off-site.
