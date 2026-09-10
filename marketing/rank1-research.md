# Getting to position 1 in Malaysia — evidence-based research

**Researched 10 Sep 2026** for Primaxs Marketing (M) Sdn Bhd / `storagesystem.com.my`.

This file is research, not a plan of record. It builds on
[`ranking-position.md`](ranking-position.md), [`indexing-diagnosis.md`](indexing-diagnosis.md),
[`seo-requirements-2026.md`](seo-requirements-2026.md) and
[`directory-listings.md`](directory-listings.md), and **corrects two of their
recommendations** (see §3).

---

## 0. Method, and what I could not verify

Read this before trusting anything below.

**What I could verify.** I fetched competitor pages directly and measured them —
word count, JSON-LD types, image counts, tables, prices, headings, CMS,
and the raw `rel=` attribute on outbound links. Those numbers are real and
reproducible. I also measured `docs/` locally with the same method, so
site-versus-competitor comparisons are like-for-like.

**What I could not verify.** *I was unable to pull live google.com.my result
pages.* Direct navigation to Google was blocked by this environment; Bing
returned unrelated results for the test query; DuckDuckGo served a CAPTCHA
(which I am not permitted to solve). The search tool available to me is
**US-locale**, so the result sets in §1 are *candidate* competitors, not a
verified google.com.my top 5.

**Therefore: every "who ranks 1–5" statement in §1 is inference, not
observation.** The competitor *page measurements* are observation. Before acting
on §1's ordering, someone with a Malaysian IP should spend 20 minutes checking
the five SERPs by hand and correcting the tables. That is the single cheapest
piece of missing evidence in this whole document.

Labels used throughout:

- **[VERIFIED]** — I fetched the page/document and measured or quoted it.
- **[INFERENCE]** — my reasoning from verified inputs. Could be wrong.
- **[UNVERIFIED]** — reported by a source I did not independently confirm.

---

## 1. The five striking-distance keywords

### 1.1 The headline finding

**The pages beating this site are, on every measurable dimension, worse pages.**

This is not a figure of speech. Measured:

| Page | Words (main) | JSON-LD schema | Images | Spec table | Prices | FAQ | Platform |
|---|---|---|---|---|---|---|---|
| [machlab.com.my Omnibench heavy-duty workbench](https://www.machlab.com.my/omnibench-heavy-duty-workbench/) | ~400 | **none** | 10 | no | no | no | WordPress |
| [my-ise.com/brands-overview/tanko](https://www.my-ise.com/brands-overview/tanko) | ~550–600 | **none** | 1 (logo only) | no | no | no | Wix |
| [Knight Auto workbenches category](https://m.knightauto.com.my/index.php?ws=ourproducts&cid=136573&cat=Tool-Storage-Tool-Boxes&subcat=Workbenches&lang=en) | ~2,500–3,000 | **none** | 35 products | no | **yes, RM28–RM2,990** | no | NEWPAGES |
| [NEWPAGES Sui U profile](https://www.newpages.com.my/v2/en/company/729126/Sui-U-Machinery---Tools-\(M\)-Sdn-Bhd.html) | 5,493 | **none** | 32 product links | no | yes | no | NEWPAGES |
| **`storagesystem.com.my/workbench/`** | **1,624** | **CollectionPage, ItemList (57 ListItem), FAQPage, LocalBusiness, Organization, BreadcrumbList, ContactPoint, GeoCoordinates** | **56, all with `alt`** | **0** | yes (from RM904) | yes | static |

[VERIFIED] — all rows fetched and counted 10 Sep 2026. The `storagesystem` row
was measured directly from `docs/workbench/index.html`.

Sitewide, `docs/` contains **1,848 HTML pages, 1,846 of which carry JSON-LD**,
including **1,744 pages with `Product` schema** and 153 with `ProductGroup`.
**Not one competitor page I fetched had any structured data at all.** [VERIFIED]

**[INFERENCE] The conclusion this forces:** on-page content and markup are not
what is holding these five keywords at positions 10–45. If they were, the site
would already be winning — it is objectively the better-built page in every case
I measured. What the winners have that this site does not is *off-page*:
domain history, inbound links, transactional signals, and platform
distribution. Section 3 and §6 are therefore where the leverage actually is,
and any plan that answers "improve the page" is answering the wrong question.

### 1.2 Per keyword

Ordering within each table is **[INFERENCE]** from US-locale results plus the
known competitive landscape. Treat as a candidate set to be verified.

#### "stainless steel workbench" — currently 10.7

Candidates: [SMT System Metal Technology](https://www.smtsystems.com/collections/workbench-workstation)
(Penang, Shopify, claims grade-304 electropolished),
[Soon Rex](https://www.soonrex.com.my/workbench/),
[Puncak Steel](https://www.puncaksteel.com/collection/table),
[Office Furnitures Malaysia](https://www.officefurnituresmalaysia.com/product-category/stainless-steel-furniture1/stainless-steel-table/),
[Berjaya Gate](https://berjayagate.com.my/industrial-stainless-steel-work-tables-malaysia/).

**The specific gap [INFERENCE]:** this query splits into two intents Google
serves differently — *commercial-kitchen* stainless tables (Puncak Steel,
Berjaya) and *cleanroom/lab* stainless benches (SMT, Machlab). The site's
matching asset is the guide
`docs/guides/stainless-steel-workbench-food-pharma-malaysia/`, which targets the
second intent. There is **no stainless product category page** — only a guide.
Competitors rank a *category/collection* page. That mismatch is the most likely
reason for a stalled position 10.7.

#### "heavy duty workbench malaysia" — currently 11.5

Candidates: [Lazada tag page](https://www.lazada.com.my/tag/heavy-duty-workbench-table/),
[Machlab Omnibench](https://www.machlab.com.my/omnibench-heavy-duty-workbench/),
[BESTOOL](https://www.bestool.com.my/showproducts/productid/4533888/),
[Knight Auto](https://m.knightauto.com.my/index.php?ws=ourproducts&cid=136573&cat=Tool-Storage-Tool-Boxes&subcat=Workbenches&lang=en),
[LCH Tooling](https://www.lchtooling.com/index.php?ws=tag&tag_id=73889),
[TOPTUL Malaysia](https://www.toptulmalaysia.com/product/heavy-duty-workbench-for-most-workshop-applications/),
[Artsystem](http://www.artsystem.com.my/laboratory/industrial-workbench-new.html).

**The specific gap [VERIFIED, partly]:** Machlab's page is ~400 words with no
schema and no prices. Knight Auto's shows **live RM prices on 35 products in one
category view**. The site's `/workbench/` page shows "from RM904" but does not
put a per-model price next to each of its 57 listed items in a scannable table —
it has **0 `<table>` elements**. Knight Auto and LCH Tooling both rank on the
NEWPAGES platform (see §3).

#### "mould rack manufacturers" — currently 20.7

Candidates are overwhelmingly **non-Malaysian**: [Oswal Engineering (India)](https://oswalengineering.com/mould-racks.html),
[MEK Engineering](https://mekengineering.com/warehouse-shelving-systems/die-moulds/),
[Kingmore (China)](https://www.kingmoreracking.com/mold-rack/),
[OTS Racking (China)](https://www.otsrack.com/mold-rack/),
[Green Valley (USA)](https://greenvalleyinc.com/rack-storage-systems/mold-storage-racks/),
[Thomasnet](https://www.thomasnet.com/suppliers/usa/mold-storage-racks-65611345).

**[INFERENCE] This is the most winnable of the five, and it is being fought
wrong.** The unqualified query "mould rack manufacturers" is a *global*
manufacturer query dominated by Chinese and Indian racking factories. Primaxs is
a *distributor*, not a manufacturer, and cannot credibly out-rank a factory on
that word. The GSC data already shows the winnable variant sitting alongside it:
**"mould rack manufacturers malaysia" at 20.7 with 10 impressions**
(`ranking-position.md`). The site has `docs/rack/mould-rack/` plus the guide
`warehouse-racking-mould-rack-shelving-malaysia`. Geo-qualify the target,
stop chasing the bare head term.

#### "industrial workbench" — currently 28.8

Candidates: [Machlab](https://www.machlab.com.my/workbenches/) and
[Artsystem](http://www.artsystem.com.my/catalogue/industrial-workbench.html)
appear repeatedly, both as *manufacturers*, plus
[SMT](https://www.smtsystems.com/collections/workbench-workstation) and
[Soon Rex](https://www.soonrex.com.my/workbench/).

**[INFERENCE]** Bare "industrial workbench" is a global head term with no
Malaysian qualifier; position 28.8 on 16 impressions is a low-value fight. The
Malaysian variants in `ranking-position.md` ("workbench malaysia" 21.8,
"workbench in malaysia" 19.0, "steel workbench" 17.3) are the same page's job
and are closer. Same conclusion as mould rack: **qualify or drop.**

#### "tool cabinet malaysia" — currently 44.4, 70 impressions, 0 clicks

This is the largest impression pool on the site and the worst position.
Candidates: [Knight Auto](https://m.knightauto.com.my/index.php?ws=ourproducts&cid=78642&cat=Tool-Storage-Tool-Boxes&subcat=Cabinet-Tool-Cart&lang=en),
[Sui U Machinery](https://m.machinerytools.com.my/index.php?ws=ourproducts&cid=364459&cat=Tool-Storage-Trolley&subcat=Tool-Storage&page=2),
[Alliance Supplies](https://www.alliancesuppliesonline.com.my/ourproducts/cid/489926/cat/storage-solutions-tool-boxes/),
[Southern State](https://www.southernstate.com.my/ourproducts/cid/26705/cat/tool-box-and-cabinet/),
[Milwaukee Tool Malaysia](https://www.milwaukeetool.my/packout-cabinet),
[HardwareMart](https://www.hardwaremart.my/product/bigred-180pcs-tools-8-drawer-tools-cabinet-tools-storage-kabinet-heavy-duty-multi-layer-cart/),
[Borong](https://market.borong.com/v/teguh-jayamas-sdn-bhd/product/Heavy-duty-Metal-Tool-Cabinet/109181).

**[VERIFIED] Four of those seven — Knight Auto, Sui U, Alliance Supplies,
Southern State — run the identical `index.php?ws=ourproducts&cid=` URL template.
That is the NEWPAGES CMS.** See §3.1: this is the single most important
structural fact in this document.

`ranking-position.md` concluded "position 44 does not become position 8 through
on-page work." I agree, and §3.1 explains the mechanism.

---

## 2. Which page format wins, per keyword

| Keyword | Format that wins | Evidence | What the site has |
|---|---|---|---|
| stainless steel workbench | **Category / collection page** with product grid | SMT, Puncak Steel, OFM all rank collection URLs [INFERENCE from result titles] | Only a *guide*. **Format mismatch.** |
| heavy duty workbench malaysia | **Category page with visible RM prices per item** | Knight Auto shows RM28–RM2,990 across 35 items on one page [VERIFIED] | Category page, floor price only, no per-item table |
| mould rack manufacturers | **Manufacturer's own deep product page** | Oswal, Kingmore, OTS, Green Valley are all factories with dedicated mould-rack product pages [INFERENCE] | Distributor category page — structurally cannot win the unqualified term |
| industrial workbench | **Manufacturer category page** | Machlab and Artsystem both rank `/workbenches/` and `/catalogue/industrial-workbench.html` [INFERENCE] | Category page; competing as distributor vs manufacturer |
| tool cabinet malaysia | **Directory-platform category listing** | 4 of 7 candidates are NEWPAGES-templated category pages [VERIFIED] | Own-domain category page, no platform presence |

**[INFERENCE] The pattern across all five:** buying guides do *not* win these
queries. Every candidate that ranks is a **category page with products and
prices on it**, or a **platform listing**. The site's 28 guides are excellent
AI-citation and long-tail assets — the GSC data shows guide-adjacent terms
converting at 20–29% CTR — but they are the wrong format for these five
commercial head terms. Do not write more guides expecting these five to move.

---

## 3. Malaysian B2B platforms and directories — verified link status

I checked the actual HTML, not the marketing claims. `rel=` attributes were read
from raw source.

### 3.1 NEWPAGES — the finding that matters most

**[VERIFIED, all of the following]**

NEWPAGES is not merely a directory that ranks. It is a **CMS that hosts its
members' own websites**. Knight Auto, Sui U, Alliance Supplies and Southern
State all serve `index.php?ws=ourproducts&cid=` URLs on their *own* domains, and
Knight Auto's footer reads "Powered by NEWPAGES" linking to newpages.com.my.
Members get a package of ranking assets:

1. Their own domain, built on the NEWPAGES template
2. A company profile on `newpages.com.my` — e.g. Sui U at
   [`/v2/en/company/729126/`](https://www.newpages.com.my/v2/en/company/729126/Sui-U-Machinery---Tools-\(M\)-Sdn-Bhd.html), 5,493 words
3. **A followed link.** The Sui U profile links `<a href="http://www.machinerytools.com.my" target="_blank">` — **no `rel="nofollow"`**. The entire 168KB page carries exactly one `nofollow`, and it is not this link.
4. Per-product pages on the newpages domain — Sui U has **32** product links on its profile
5. Mirror subdomains: `machinerytools.newpages.com.my`, `machinerytools.n.my`, `machinerytools.newstore.my` — I confirmed `machinerytools.newpages.com.my` returns a real 603-byte member page titled "Sui U Machinery & Tools (M) Sdn Bhd :: Powered by www.newpages.com.my"

**Primaxs already has a NEWPAGES listing** —
[`/v2/en/company/93368/`](https://www.newpages.com.my/v2/en/company/93368/Primaxs-Marketing-\(M\)-Sdn-Bhd.html).
Measured against Sui U's:

| | Primaxs (93368) | Sui U (729126) |
|---|---|---|
| Page exists, HTTP 200 | yes | yes |
| Title | already well-optimised, lists all 7 categories | generic |
| Followed links to own site | **2**, both to `https://www.storagesystem.com.my` | 1 |
| **Product pages on NEWPAGES** | **0** | **32** |
| Member subdomain provisioned | **no** — `primaxs.newpages.com.my` falls through to the generic NEWPAGES homepage, identical to a nonsense subdomain I tested as a control | **yes** |

**[INFERENCE] This is the highest impact-per-effort item on the whole list.**
The account exists, the copy is already good, and the followed links are already
there. What is missing is *product inventory on the platform* — the exact asset
the four competitors beating this site on "tool cabinet malaysia" all have. The
control test (a fake subdomain returning the same page as `primaxs.`) is
reasonable evidence the listing is on a free/basic tier.

**[UNVERIFIED]** NEWPAGES pricing. Their own marketing claims "26 million
keywords ranked on Google's first page" and "9,500 businesses"
([newpages.net](https://www.newpages.net/),
[newpages.com.my](http://www.newpages.com.my/)) — that is a vendor claim, not a
measurement, and I did not confirm it. Get a written quote before paying.

**[VERIFIED]** NEWPAGES pages contain **zero JSON-LD structured data**. Their
ranking is not coming from markup.

### 3.2 The rest, checked

| Platform | Ranks for these terms? | Free/paid | Followed link? | Effort | Verdict |
|---|---|---|---|---|---|
| **NEWPAGES** | **Yes — 4 of 7 "tool cabinet malaysia" candidates** [VERIFIED] | Listing exists free; product/subdomain tier paid [INFERENCE] | **Yes, dofollow** [VERIFIED] | Low — account exists | **Do this first** |
| **B2BMap** | Not seen in any of my 5 result sets [VERIFIED absence, weak evidence] | Free tier | **No link at all.** I fetched a live free profile ([ALL IT Hypermarket](https://b2bmap.com/all-it-hypermarket-sdn-bhd/contact-info)) — it shows Home/Product/Contact and a contact form, and **displays no website URL whatsoever**. Zero outbound anchors to the member's domain. [VERIFIED] | Low | **Deprioritise.** `directory-listings.md` ranks B2BMap as high-value; on this evidence that is wrong for link purposes. Brand-mention value only. |
| **Lazada MY** | **Yes** — `lazada.com.my/tag/heavy-duty-workbench-table/` appeared for "heavy duty workbench malaysia" [VERIFIED it appeared] | Free to list, commission on sale | Marketplace, no SEO link | Medium (seller onboarding) | Marginal — see §4.4 |
| **Shopee MY** | Not seen in my result sets | Free to list | No | Medium | Marginal |
| **Alibaba** | `alibaba.com/workbench-malaysia-suppliers.html` appeared twice [VERIFIED it appeared] | Free + paid Gold Supplier | No | Medium | Export-oriented; wrong buyer |
| **Carousell MY** | Not seen | Free | No | Low | No |
| **Made-in-China** | Not seen for MY terms | Free + paid | Homepage carries 276 `nofollow` attributes [VERIFIED] | Medium | No — it sells Chinese factories against you |
| **Yellow Pages MY** | Not seen | Free + paid | Not verified on a listing page | Low | NAP citation only |
| **EasyExport** | Could not reach — `easyexport.my` failed to resolve/connect [VERIFIED failure] | — | — | — | **Cannot recommend; may be defunct** |
| **FMM** | Not seen in organic | Members only, RM500 entrance + annual (per `directory-listings.md`, unverified by me) | Not verified | High | Audience quality, not SEO |
| **ePerolehan / MOF** | Not an SEO channel | Application + registration fee; cert valid **3 years**; required to be invited to quotations RM50k–RM500k and tenders >RM500k ([ePerolehan](https://www.eperolehan.gov.my/en/online-registration), [MISHU](https://mishu.my/blog/business-licenses/mof-license-application/)) | n/a | High | **Revenue channel, not a ranking channel.** Schools/campuses are already in the ICP. |

---

## 4. Which Google features are realistically winnable in 2026

The best locale-specific evidence I found is a **Malaysian SERP study**:
[Sterrific, "Do Shopee & Lazada Own Google Malaysia? 455 SERPs Checked"](https://www.sterrific.com.my/blog/shopee-lazada-google-malaysia-serp-study/).
Methodology, quoted [VERIFIED — I fetched and read the article]: 60 commercial
Malaysian keywords across 4 verticals, SERPs pulled via **Ahrefs serp-overview,
country = Malaysia, 11 June 2026**, top 10 per query, 455 results classified.

**Caveat, stated plainly:** the four verticals are electronics, fashion &
beauty, home & living, and automotive parts — **consumer, not industrial B2B**.
It is also an agency's own study promoting its services. The SERP-feature
prevalence figures probably transfer; the marketplace-share figures probably do
not transfer cleanly to B2B. Treat the numbers as directional.

Its measured feature prevalence on Malaysian SERPs:

- Shopping carousels on **51.7%** of SERPs
- AI Overviews on **51.7%**
- People Also Ask on **68.3%**
- Average "top 10" contains **7.6 real organic results** — only 1 of 60 SERPs served a full ten

### 4.1 Merchant Center free product listings — **the strongest single opportunity**

[VERIFIED] Malaysia is a supported country for Shopping ads and free listings
([Google Merchant Center Help](https://support.google.com/merchants/answer/7101265?hl=en)).
Free listings are genuinely free — no account, listing or per-product fee — and
surface products in "Search, Images, Lens, YouTube, Gemini, the Shopping tab,
and the products module on Business Profile"
([Google](https://support.google.com/merchants/answer/13889434?hl=en)).
`price` and `availability` are **required for all products** [VERIFIED, same
source]. Merchants must follow the free-listings policies and add return-policy
information to the website.

Two things make this unusually well-suited here:

1. **The feed already exists.** `marketing/google-merchant-feed.tsv`, 1,517 SKUs with real RM prices, per the git log. `seo-requirements-2026.md` records it as "ready to upload".
2. **The returns policy page already exists** — commit `7edfcf97f8` added `/returns/`, and `docs/` shows 1,591 pages carrying `MerchantReturnPolicy` and `OfferShippingDetails` schema [VERIFIED locally]. That is precisely the Google requirement.

**[INFERENCE, important and worth testing rather than assuming]:** the shopping
carousel is the one large SERP surface that is *not* won by ranking. Sterrific
puts it plainly — you enter it via a Merchant Center feed, not via organic
position. If that carousel really does sit on ~half of Malaysian commercial
SERPs, then a site stuck at average position 47.5 organically could appear
*above* the organic results it cannot reach. **This is the only recommendation
in this document that does not depend on out-ranking anybody.**

Caveat [VERIFIED]: Merchant Center verifies landing pages with **Googlebot**,
comparing feed price against the page or its structured data
([Google](https://support.google.com/merchants/answer/14990960?hl=en)). So the
pages must be crawlable — they are; `robots.txt` allows them. Whether inclusion
in the carousel requires the page to be in the *organic index* I could **not**
find documented either way. Given 1,228 pages are unindexed, this is a material
unknown — upload a small batch first and observe.

### 4.2 Local pack — winnable, and cheap

[UNVERIFIED aggregate, multiple secondary sources agree] Google Business Profile
signals are reported at ~32% of local pack weight and review signals ~16–20%,
with **review velocity and owner response rate** weighted more heavily after the
March 2026 core update
([StoreRocket](https://storerocket.io/learn/local-seo-ranking-factors),
[DigitalApplied](https://www.digitalapplied.com/blog/local-seo-march-2026-core-update-gbp-optimization-guide)).
These are agency compilations, not Google statements. I did not find a primary
source.

The site has 3 Google reviews, two of them empty (`growth-audit.md`). Every
prior document in this folder reaches the same conclusion. Nothing in my
research contradicts it.

### 4.3 AI Overview citations — winnable, already half-built

[VERIFIED] `robots.txt` in `docs/` explicitly allows 8 AI crawlers
(OAI-SearchBot, ChatGPT-User, PerplexityBot, Claude-SearchBot, ClaudeBot,
Applebot, GPTBot, CCBot) and blocks Bytespider.

[UNVERIFIED, secondary] Only ~38% of URLs cited in AI Overviews also rank in the
organic top 10; 44.2% of LLM citations come from the first 30% of a text;
syndicated content generates up to 325% more citations than own-site-only
publishing ([Semrush](https://www.semrush.com/blog/manufacturing-seo-ai-search/),
[Position Digital](https://www.position.digital/blog/ai-seo-statistics/)). I did
not verify these figures.

[VERIFIED from Sterrific] On Malaysian SERPs where no authoritative local page
exists, AI Overviews assemble answers from **marketplace category pages and
Facebook posts** — the study documents Overviews for "telefon murah", "harga
tayar" and "katil queen" citing Shopee, TikTok and Facebook sellers.

**[INFERENCE]** The 28 guides — 11 already in Bahasa Malaysia — are the right
asset for this, and it is the one surface where being the better-written page
actually pays without needing authority first.

### 4.4 The Bahasa Malaysia flank — the cheapest unexploited surface

[VERIFIED from Sterrific] On BM queries, marketplaces hold **4× their English
share** and are present on 10 of 12 BM queries; social/UGC takes **28.2% of BM
organic results vs 12.8% on English**. The study's own reading: "Shopee doesn't
outrank Malaysian brands in BM. It outranks their absence." It also cites an
earlier study finding BM keywords easier to rank in 10 of 13 matched pairs,
never harder [UNVERIFIED — I did not fetch that earlier study].

The site already has 11 BM guides (`meja-kerja-industri-malaysia`,
`kabinet-alat-penyimpanan-bengkel-malaysia`, `loker-besi-malaysia`,
`rak-gudang-rak-acuan-malaysia`, and others) [VERIFIED locally]. It has **no BM
category pages** — and §2 established that category pages, not guides, win
commercial queries.

### 4.5 Not winnable / not worth it

- **FAQ rich results** — deprecated 7 May 2026 (`seo-requirements-2026.md`). The 1,655 `FAQPage` blocks harm nothing; leave them.
- **HowTo rich results** — long deprecated.
- **"Perspectives"** — a forum/social surface. Not available to a distributor's own site.
- **Image pack** — the site has 12,966 image files and full `alt` coverage on the pages I sampled (56/56 on `/workbench/`) [VERIFIED]. Sterrific logged image packs but published no prevalence figure, so **I cannot say whether image packs appear on these SERPs at all.** Unknown, not "winnable".

---

## 5. Why a big catalogue stays "Discovered — not indexed"

### What Google actually documents [VERIFIED]

[Google's crawl budget guide](https://developers.google.com/crawling/docs/crawl-budget),
**last updated 22 July 2026** (note: it moved from
`/search/docs/crawling-indexing/large-site-managing-crawl-budget` to
`/crawling/docs/crawl-budget`), says it applies to:

- large sites (1M+ pages) changing weekly
- medium+ sites (10k+ pages) changing daily
- **"sites with a large portion of their total URLs classified by Search Console as Discovered - currently not indexed"** — this site, exactly

Its recommended actions, as documented:

- **Consolidate duplicate content** — focus crawling on unique content, not URLs
- **Improve loading speed** — server response times and resources
- **Use HTTP caching** — support `304 (Not Modified)`
- **Debug crawl budget issues** — check for availability problems
- Block low-value-add URLs (infinite scroll, sort variants) with **robots.txt, not noindex**

Note what Google does **not** say: it never explains what causes the status, and
it recommends no fix involving more internal links or resubmitting sitemaps.
I attempted to fetch the Google Search Central community guide on this topic
but its body is JavaScript-rendered and I could not extract it — **unverified**.

### Independent guidance [VERIFIED — fetched]

[Uproer, "Why is My Ecommerce Site Not Being Indexed?"](https://uproer.com/articles/ecommerce-indexing-issues/)
(published 2019, **last modified 23 Dec 2025**) identifies two causes — poor
crawl efficiency and near-duplicate product/category content — and recommends:

- Reduce crawlable non-indexable URLs (their case: Google crawling **15,000+ URLs for one category page** via faceted navigation)
- **"Canonical tags alone are not a solution for improving crawl efficiency. Google can still crawl canonicalized URLs!"**
- Breadcrumb links with schema
- HTML pagination instead of infinite scroll
- **Detailed Product schema markup** to help Google assess uniqueness
- Ensure content renders in HTML, not JavaScript
- **"Create individual XML sitemaps for the various sections of your website. Your product pages should be in their own XML sitemap, separate from that of your category pages."**

### Measured against this site [VERIFIED locally]

| Guidance | Status here |
|---|---|
| Faceted-navigation URL explosion | **Not a problem** — static site, `robots.txt` disallows `?q=`, `?utm_`, `?gclid=`, `?fbclid=` |
| JavaScript rendering | **Not a problem** — fully static HTML |
| Product schema for uniqueness | **Done** — 1,744 pages, 153 with `ProductGroup` |
| Breadcrumbs with schema | **Done** — 1,844 `BreadcrumbList` |
| HTML pagination, not infinite scroll | **Fine** |
| Near-duplicate variant pages | **This is the problem** — 99.1% textual similarity measured in `indexing-diagnosis.md` |
| **Segmented XML sitemaps** | **NOT DONE — `docs/sitemap.xml` is a single flat `<urlset>` of 1,846 URLs. It is not a sitemap index. Products, categories and guides are all in one file.** |
| Consolidate duplicates | **Partly done** — family pages like `docs/cnc-tool/ea-10mn/` already carry **6 `<table>` elements**. Variant pages are still indexable: only **2 pages sitewide** carry `noindex`. |

**Two concrete, previously unrecorded gaps [VERIFIED]:**

1. **The sitemap is not segmented.** This is cheap to fix, is explicitly recommended by current (Dec 2025) guidance, and — the real payoff — makes GSC report indexation *per section*, which is the only way to measure whether any of this works.
2. **The consolidation described as "option 2" in `indexing-diagnosis.md` is half-built.** The family-page variant tables exist. The `noindex, follow` on variant pages does not. Doing one without the other gets neither benefit.

**[INFERENCE]** `indexing-diagnosis.md`'s conclusion stands and is supported by
Google's own doc: the deeper cause is authority, and crawl budget follows it. But
the two gaps above are real, cheap, and currently unaddressed.

---

## 6. Ranked by impact ÷ effort

| # | Action | Impact | Effort | Why, in one line |
|---|---|---|---|---|
| **1** | **Verify the 5 SERPs by hand from a Malaysian IP** and correct §1 | High | **20 min** | Every recommendation ranked below §1 depends on a competitor set I could not observe directly |
| **2** | **Upload the Merchant Center feed** (1,517 SKUs, already built) | High | **Hours** | Only surface reachable without out-ranking anyone; Malaysia supported; carousel on ~half of MY SERPs; feed + `/returns/` + `MerchantReturnPolicy` schema all already exist |
| **3** | **Load products onto the existing NEWPAGES listing** (93368) | High | Low–Med | Primaxs has **0** products there; Sui U has **32**; 4 of 7 "tool cabinet malaysia" competitors are NEWPAGES sites; the dofollow link is already in place |
| **4** | **Get 10 real Google reviews** | High | Wei Ming's time | Reviews are ~16–20% of local pack weight; profile has 3, two empty; every prior doc says the same |
| **5** | **Split `sitemap.xml` into a sitemap index** (products / categories / guides / locations) | Medium | **1–2 hours** | Explicitly recommended by current guidance; the only way to *measure* indexation per section |
| **6** | **Build a stainless-steel workbench category page** | Medium | Half a day | Position 10.7 with only a guide behind it — a format mismatch, and the closest keyword to page one |
| **7** | **Add per-model RM price tables to category pages** (currently **0** `<table>`) | Medium | 1 day | Knight Auto shows 35 prices in one view; the site shows a floor price only |
| **8** | **Finish the consolidation** — `noindex, follow` on variant SKU pages | Medium | 1 day | Family tables already exist; without the noindex neither half pays off |
| **9** | **Build BM category pages** (not more BM guides) | Medium | 2–3 days | BM is 4× easier and marketplaces fill the vacuum; 11 BM *guides* exist, 0 BM *category* pages |
| **10** | **Re-target "mould rack" and "industrial workbench" to geo-qualified variants** | Medium | Hours | Unqualified head terms are manufacturer/global queries a distributor cannot win |
| **11** | MOF / ePerolehan registration | Med (revenue, not rank) | High | Required for RM50k+ government quotations; schools/campuses already in ICP |
| **12** | ~~B2BMap listing~~ — **downgrade** | Low | Low | **Verified: free B2BMap profiles display no website link at all.** `directory-listings.md` overrates this |
| **13** | Made-in-China, Alibaba, Carousell, EasyExport | ~Zero | — | Nofollow, wrong buyer, or (EasyExport) unreachable and possibly defunct |

---

## 7. Corrections to existing documents in this folder

1. **`directory-listings.md`** lists B2BMap as a priority free listing. [VERIFIED] A live free B2BMap profile shows **no outbound website link of any kind**. Keep it for brand mentions if you like; do not count it as a link.
2. **`directory-listings.md`** lists EasyExport-style directories generically. [VERIFIED] `easyexport.my` did not respond at all on 10 Sep 2026.
3. **`seo-requirements-2026.md`** ranks "NEWPAGES claim" at #2 but frames it as a citation. [VERIFIED] It is much more than that — it is a followed link *plus* a product-hosting platform that four direct competitors are ranking through, and the account already exists.
4. **`indexing-diagnosis.md`** presents consolidation as a future decision. [VERIFIED] It is already half-implemented — family variant tables exist; the `noindex` half does not.

---

## 8. Open questions I could not close

- **The actual google.com.my top 5 for all five keywords.** Blocked (see §0). Highest-value 20 minutes available.
- **NEWPAGES pricing and what tier unlocks product pages and the member subdomain.** Requires contacting them.
- **Whether Merchant Center free listings require the landing page to be in the organic index.** Not documented either way in what I could find. Materially affects recommendation #2 given 1,228 unindexed pages — test with a small batch.
- **Backlink profiles.** No Ahrefs/Majestic access; every statement about competitor authority in this document is inference from observable page quality, not link data.
- **Whether image packs appear on these SERPs.** Unknown.
- **Why `my-ise.com` outranks a demonstrably better site for Tanko-brand queries.** Their page is ~550 words on Wix with no schema, no SKUs, no images and no prices [VERIFIED]. On page quality it should lose. The cause is off-page and I could not measure it.

---

## 9. SERPs verified by hand — 10 Sep 2026 [VERIFIED, not inference]

§0 and §1 of this document are explicitly labelled inference because live
`google.com.my` results could not be fetched at the time. They now have been,
via `google.com/search?gl=my&hl=en`, and **three of the conclusions in §1 need
correcting.**

### Measured positions

| Keyword | Primaxs | What ranks above |
|---|---|---|
| **mould rack malaysia** | **4** | ttf.com.my, mega-rack.my, yesdisplay.com.my |
| **stainless steel workbench malaysia** | **10** | berjayacke, Shopee, machinerytools, MISUMI, rcmesin, puncaksteel, officefurnitures, soonrex, ongplas |
| heavy duty workbench malaysia | not in top 10 | Knight Auto, Machlab, TOPTUL, Artsystem, Techno, JTE, Newtech, MISUMI, RS |
| tool cabinet malaysia | not in top 10 | Knight Auto, machinerytools, TOPTUL, RS, JTE, CT Hardware, Milwaukee, Shopee, TTF |

### Correction 1 — we are already on page one for two terms

GSC average position blends every impression including deep long-tail ones.
The head terms actually sit at **4** and **10**, not 20.7 and 10.7. Two page-one
placements already exist and are worth protecting, not rebuilding.

### Correction 2 — the stainless category-page theory was wrong

§1.2 argued the stalled position was a format mismatch: "competitors rank a
category/collection page, we only have a guide." Two things were wrong. A
stainless **category page already existed** (`/workbench/stainless-steel/`),
and Google is not ranking it or the guide — it ranks a single **SKU page**,
`Stainless Steel Workbench — Standard (WD-68S)`.

So the fix was not "build a category page". It was that the category page was
413 words with no prices and no product links, which is why Google preferred a
product page over it. That page has now been rebuilt with a 23-line price
table; whether it displaces the SKU page is the thing to watch.

### Correction 3 — this keyword is mostly a commercial-kitchen query

Eight of the ten results are **stainless kitchen work tables** — "Boost Kitchen
Efficiency", "2 and 3 Tier", "with Back Splash", Shopee listings. Only MISUMI
and Primaxs are industrial. Ranking higher here means winning traffic that
largely wants a RM600 kitchen prep table, not a RM3,000 lab bench.

That reframes the opportunity. Either target the food-production intent
explicitly — Tanko stainless genuinely suits it — or shift effort to qualified
terms with the right intent (`cleanroom workbench malaysia`, `food grade
workbench malaysia`, `laboratory workbench malaysia`), where the competition
is MISUMI rather than nine kitchen suppliers.

### Confirmed decisively — the NEWPAGES finding

§3.1 is right, and stronger than stated. NEWPAGES-built sites hold:

```
tool cabinet malaysia          #1 Knight Auto   #2 machinerytools (Sui U)
heavy duty workbench malaysia  #1 Knight Auto
mould rack malaysia            #7 alliance-supplies
stainless steel workbench      #3 machinerytools (Sui U)
```

Four of our keywords have a NEWPAGES site in the top 3. Primaxs has the
listing and the followed link already; the products are what is missing.

### What the mould-rack result teaches

Position 4 is our best, and it is the **category page** ranking, with the price
in the title tag: *"Mould Racks Malaysia — from RM9,471 | Primaxs"*. A category
page carrying a real Ringgit figure is the format that is working. That is the
pattern now applied to the six workbench range pages.

**Method:** `google.com/search?q=<term>&gl=my&hl=en&num=20`, organic `h3`
results only, packs and ads excluded, 10 Sep 2026. Not personalised-search
free — treat as indicative to within a position or two.
