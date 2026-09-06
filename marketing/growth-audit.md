# Growth audit — what is still missing, ranked by revenue impact

**6 Sep 2026.** Written after auditing the live site, the SERPs Primaxs competes
in, the existing directory footprint, and research into how Malaysian industrial
buyers actually buy.

The promotion work so far has been **top-of-funnel only** — posts, groups,
followers. This audit covers everything else in the chain between "a buyer
exists" and "a buyer sends a list".

---

## 1. How Malaysian industrial buyers actually buy

This is the frame everything below is judged against.

| Stage | What happens | Where Primaxs stands |
|---|---|---|
| **1. Problem → search** | Buyer Googles a specific problem ("ESD workbench Malaysia"), then **judges the top 5 results in about 15 seconds** on whether the company looks real | Site is strong. Ranking is partial. |
| **2. Peer validation** | Asks contacts for a recommendation — in Malaysia this happens **inside WhatsApp groups**: industry associations, alumni, supplier chats. Invisible to any analytics. **This is where deals are won.** | **Nothing here at all.** |
| **3. Trust verification** | Checks SSM registration, ISO, MOF supplier status, case studies, named people | SSM yes, ISO yes. **Case studies no. Reviews no. MOF no.** |
| **4. Internal approval** | Multiple stakeholders — specifier, procurement, approver — each with different objections | Guides cover this well |

**The one-sentence version:** Primaxs passes the 15-second test on the website
and fails it everywhere a buyer looks *next*.

---

## 2. What is already working — do not touch

- 1,845-page site, full LocalBusiness + Organization + FAQ schema, clean 301s to `https://www.`
- 28 guides, 11 of them in Bahasa Malaysia — almost no competitor does this
- 6 industry pages, 6 location pages
- WhatsApp float button, quote basket, working enquiry form
- **SSM number already published** on `/about/` and `/contact/` — exactly what a step-3 buyer looks for
- 23 Facebook groups joined, 15 confirmed group placements, LinkedIn + GBP live

---

## 3. THE GAPS — ranked

### TIER 1 — buyers arrive and do not convert

**G1. Almost no social proof anywhere. The biggest single gap in the business.**

- `grep -rli "testimonial|customer review|case study"` across 1,845 pages returns **0 results**
- Google Business Profile: **3 reviews**, two of them from single-review accounts with no sentence in them ("Nice products , beautiful price reasonable"), one rating-only from seven years ago
- Facebook Page: reviews not enabled

Reviews are **the number one local ranking factor** — roughly 20% of local SEO
weight, by quantity, velocity and sentiment — and they now feed Google's AI
Overviews as well. A competitor with 12 reviews outranks a better company with 0.

Nearly two decades of customers exist. Three of them are visible, and none of those three names a product or describes a job — which is exactly the text Google reads. Full plan in [`review-engine.md`](review-engine.md).

**This cannot be fixed by writing anything.** Testimonials have to be real. What
can be built is the machine that collects them — see the plan.

---

### TIER 2 — buyers never arrive

**G2. A competitor owns the Tanko brand search.**

`my-ise.com/brands-overview/tanko` — "MY INDUSTRIAL SOLUTION ENTERPRISE" — ranks
for Tanko in Malaysia. Their entire contact detail is **a Gmail address**. No
company number, no address, no phone. Their claim: *"MYISE provides sourcing and
quotation support for TANKO products."*

Primaxs is the **exclusive Malaysia distributor** and has **no `/tanko/` brand
page at all**. Only 7 of 1,845 pages carry "Tanko" in the title tag.

Every buyer who searches the brand — the warmest traffic that exists — can land
on a Gmail account instead of the actual distributor.

**G3. NEWPAGES owns the Malaysian industrial SERP, and the Primaxs listing on it is broken.**

Search almost any industrial term in Malaysia and page one is NEWPAGES-built
sites, recognisable by the URL pattern `index.php?ws=ourproducts&cid=`:

| Competitor | Where |
|---|---|
| **Knight Auto Sdn Bhd** | **Seri Kembangan — the same town as Primaxs** |
| Alliance Supplies Sdn Bhd | Selangor / nationwide |
| SP Tools Sdn Bhd | Subang Jaya |
| Sui U Machinery & Tools | Setapak |
| Mr. Mark Tools | Johor |
| Acefield / isaki | Johor, Selangor |

Their title tags are crude keyword-plus-location stuffing — *"Tool Storage
Selangor, Malaysia, Kuala Lumpur (KL), Seri Kembangan, Setapak Supplier,
Suppliers, Supply, Supplies"* — and in this vertical it still works.

**Primaxs already has a NEWPAGES listing: `newpages.com.my/company/93368`.** It is
unclaimed, carries **the wrong address** (Taman Lembah Maju, KL), has **no website
link**, no description and no products. It is currently doing active harm: a wrong
NAP citation for a local business.

**G4. Directory citations are inconsistent.** Old listings on `infopages.net.my`,
`all.biz` and `contact.page` carry outdated addresses and pre-Tanko descriptions
(some still say FAMI). Inconsistent name/address/phone across the web directly
weakens local ranking.

**G5. Yellow Pages and B2BMap were never actually blocked.** Both stalled on
"needs the SSM registration number" — which is **already published on the
company's own About page**: `756588-H` / `200601036829`, incorporated
15 December 2006. Self-inflicted block.

**G6. No Google Merchant Center free listings.** Malaysia is supported. Free
placements across Search, Images, the Shopping tab, Maps and Lens. **1,736 product
pages already emit `priceCurrency` schema**, so the feed is mostly built already —
it just has to be exported.

---

### TIER 3 — channels never opened

**G7. WhatsApp Business catalogue.** Research says peer validation happens inside
WhatsApp groups. A catalogue link is the thing that actually gets forwarded in
those chats. The float button exists; there is no catalogue behind it.

**G8. Marketplaces — Shopee / Lazada Malaysia.** Live demand for tool cabinets and
workbenches, and several competitors are already there. Two benefits beyond the
sales themselves: marketplace listings rank in Google, and marketplaces
**generate reviews**, which feeds straight back into G1.

**G9. MOF / ePerolehan registration** — RM450 for 3 years, unlocks the entire
government, university and TVET segment. Wei Ming's call.

**G10. No email capture.** The E147 catalogue is a natural lead magnet and is
currently gated behind nothing. No list exists.

**G11. No video.** Reels get roughly 4.8x the shares of static images. A
20-second phone clip of a drawer taking 200kg would outperform every post
written so far.

---

## 4. THE PLAN

### Do now — no dependency on Wei Ming

| # | Action | Fixes | Why it ranks here |
|---|---|---|---|
| 1 | Build a `/tanko/` brand hub page | G2 | Warmest traffic in the funnel is currently going to a Gmail address |
| 2 | Review-collection system: GBP short link + ask scripts in EN / BM / 中文 | G1 | The number one ranking factor is sitting at zero |
| 3 | Finish Yellow Pages + B2BMap with the real SSM number | G5 | Already 90% done, unblocked by a fact already on the site |
| 4 | Claim and correct the NEWPAGES listing | G3 | A wrong NAP is actively costing ranking today |
| 5 | Export a Google Merchant Center product feed | G6 | The data already exists in the page schema |
| 6 | Keep posting and joining groups | — | Compounding, already running |

### Needs Wei Ming — about 5 minutes each, high value

| Action | Unlocks |
|---|---|
| **Send `storagesystem.com.my/review` to 10 past customers** | G1 — the biggest gap in the business |
| Name 3 customers who will allow a case study | G1 |
| WhatsApp verification code | WhatsApp button on the Page |
| Go / no-go on Shopee + Lazada | G8 |
| Go / no-go on MOF (RM450 / 3 yrs) | G9 |
| One 20-second phone video of a loaded drawer | G11 |

---

## 5. The honest ranking of what will actually move revenue

1. **Ten Google reviews.** Nothing else on this page comes close.
2. **The `/tanko/` page**, because brand searchers are already sold and are being lost.
3. **NEWPAGES and the directory cleanup**, because that is the SERP this industry lives in.
4. Merchant Center free listings.
5. Everything social. It builds the credibility layer that makes 1–4 convert — but it is not the traffic engine, and treating it as one would be the wrong read.
