# Backlink targets — ranked action list

**Researched 12 Sep 2026.** Goal: Malaysian/regional B2B platforms that (a) rank
for industrial-storage buying terms and (b) pass a **followed** outbound link to
storagesystem.com.my on a listing we can actually get.

## How to read this file

Every row is marked with how the claim was obtained:

- **FETCHED** — I pulled the raw HTML of a live member profile and read the
  actual `<a>` tag. The anchor is quoted. This is the only evidence that counts
  for the link test.
- **INFERRED** — reasoning from something adjacent (a pricing page, a pattern
  across profiles). Not proof.
- **UNVERIFIED** — I could not get the page. Said plainly, not guessed.

Markdown converters strip `rel`, so every link test below was done on raw HTML
via `Invoke-WebRequest`, not via a page-summarising fetch.

---

## Read this first: the ranking question could not be answered from here

I could not reproduce Google Malaysia SERPs from this environment. Stating that
plainly rather than substituting guesses:

| Engine | What happened |
|---|---|
| Google (via WebSearch tool) | Works, but is **US-geolocated**. Malaysian directories did not appear in the top 10 for any buying term. Not representative of google.com.my. |
| Bing (`cc=MY`) | Returned results but its Malaysian index is junk — "workbench malaysia" returned MySQL Workbench and Salesforce Workbench; "steel locker malaysia" returned Wikipedia and the Malaysian Steel Institute. Unusable as a ranking proxy. |
| DuckDuckGo (`kl=my-en`) | One successful call, then rate-limited for the rest of the session. |

**So: treat your own hand-verified finding — NEWPAGES at #1 and #2 for "tool
cabinet malaysia" on Google MY — as the authoritative ranking data. Nothing
below overturns it.** The "does it rank" column carries only what I actually
observed, and says so.

### What I *can* evidence about ranking, structurally

This is the strongest ranking-adjacent finding of the research, and it is
FETCHED, not inferred.

Across every buying term I searched — English and Malay — the Malaysian supplier
sites that surfaced are overwhelmingly **NEWPAGES-built websites**. I confirmed
this by fetching four competitor homepages and finding the NEWPAGES footer
backlink in each:

| Competitor | Their site | NEWPAGES footer link found in raw HTML |
|---|---|---|
| Sui U Machinery | machinerytools.com.my | `<a href="https://www.newpages.com.my/v2/en/company/729126/index.html" target="_blank">NEWPAGES</a>` |
| Alliance Supplies | m.alliance-supplies.com | `<a href="https://www.newpages.com.my/v2/en/company/474044/Alliance-Supplies-Sdn-Bhd.html" class="newpages_link" target="_blank">NEWPAGES</a>` |
| SP Tools | m.sptools.com.my | `<a href="https://www.newpages.com.my/v2/en/company/728298/SP-Tools-Sdn-Bhd.html" class="newpages_link" target="_blank">NEWPAGES</a>` |
| Knight Auto | knightauto.com.my | `<a href="https://www.newpages.com.my/v2/en/company/491603/index.html" target="_blank">NEWPAGES</a>` |

The same template signature (`index.php?ws=ourproducts&cid=`,
`/ourproducts/cid/`, `?ws=showproducts&products_id=`) also appeared on ranking
results for Southern State, Acefield/isaki, SMF Tools, MAXYNE (mould rack), and
on the Malay-language term "meja kerja industri" for HHT Office, SWH Furniture
and Asiastar Furniture.

**The conclusion: NEWPAGES is not just a directory, it is the CMS that most of
our ranking competitors run their entire website on.** That is where their links
come from — the platform links to them and they link back. Answering the "where
do the competitors' links come from" part of the brief: overwhelmingly, from the
NEWPAGES network itself.

---

## THE RANKED ACTION LIST

| # | Platform | URL | Does it rank? | Followed link? | Free or paid | Signup friction | Effort |
|---|---|---|---|---|---|---|---|
| 1 | **NEWPAGES** | newpages.com.my | Your hand-verified #1/#2 for "tool cabinet malaysia". I could not re-observe from US geo. Structurally dominant — see table above. | **YES — FETCHED.** No `rel` at all. | **Free** — we are already a member | None. Account exists (company id **93368**) | Low — expand existing listing |
| 2 | **NEWPAGES.asia** | newpages.asia | **FETCHED** — appeared in my Google-tool results for a tool-cabinet query, so it is indexed | **YES — FETCHED.** Two followed links per product page | **Free** — syndicated from the NEWPAGES account | None | Near-zero — verify syndication |
| 3 | **InfoPages** | infopages.net.my | Not observed ranking for our terms (US geo). Pages carry `robots: index, follow` | **YES, when populated — FETCHED.** But **our own listing has no link at all** | **Likely paid — UNVERIFIED.** Pricing is sales-gated | Existing stub; contact sales to populate | Low — one email |
| 4 | **Malaysia Brand** | malaysiabrand.com.my | Not observed | **YES — FETCHED.** Followed links to member domains | **UNVERIFIED** — NEWPAGES sister property | UNVERIFIED — ask our NEWPAGES rep | Low — one question |
| 5 | **FMM Directory** | fmm.org.my | Not observed. Member list URL 404'd for me | **UNVERIFIED** — could not reach a member profile | **Paid** (RM500 entrance + annual) | Membership + business documents | High — but best audience |

Below the line — worth a manual look in a browser because I was bot-blocked,
**not** because I found anything good:

| Platform | URL | Status |
|---|---|---|
| Yellow Pages Malaysia | yellowpages.my | **UNVERIFIED** — 403 to every fetch method tried, including full browser headers |
| ExportHub | exporthub.com | **UNVERIFIED** — 403 |
| all.biz (we have a listing: `4617-my.all.biz`) | all.biz | **UNVERIFIED** — 403 |
| InfoisInfo Malaysia | infoisinfo.com.my | **UNVERIFIED** — homepage loads, no member profile tested |

---

## The evidence, target by target

### 1. NEWPAGES — the benchmark, confirmed independently

I did not take this on trust. I fetched raw HTML of **our own live profile** and
of a competitor's, and found the same result on both.

**Our profile** — `https://www.newpages.com.my/v2/en/company/93368/index.html`
(HTTP 200, 213,413 bytes). Two followed links to our domain, no `rel` attribute:

```html
<a href="https://www.storagesystem.com.my" target="_blank" title="Primaxs Marketing (M) Sdn Bhd" style="word-break:break-all;">
<a href="https://www.storagesystem.com.my" class="visit_website_btn" target="_blank" title="Visit Website">
```

**Knight Auto's profile** — `https://m.newpages.com.my/en/company/491603/Knight-Auto-Sdn-Bhd.html`
(HTTP 200, 95,300 bytes):

```html
<a href="https://www.knightauto.com.my" target="_blank" title="https://www.knightauto.com.my">
```

**And crucially — product/category pages carry the link too.**
`https://m.newpages.com.my/en/company/491603/products/78642/Cabinet-Tool-Cart.html`
(HTTP 200, 122,465 bytes) carries the same followed anchor.

> **This is the scaling insight.** The followed link is not one-per-company — it
> repeats on every product and category page the listing generates. We have 12
> products up. The catalogue is ~1,700 SKUs across 11 ranges. Every additional
> product page is another followed link from the platform that already outranks
> us.

**Action:** expand the NEWPAGES listing from 12 products toward full range
coverage — workbenches, tool cabinets, CNC tool storage, workstations, lockers,
parts cabinets, racking, mould racks, perforated boards. Use the deep links and
copy blocks already in `marketing/directory-listings.md`. Free, account exists,
highest return of anything in this file.

Note the URL format changed: the current canonical path is
`/v2/en/company/<id>/`. The older `/en/company/<id>/<Name>.html` form 404s on
`www` but still resolves on the `m.` subdomain.

### 2. NEWPAGES.asia — a free second property off the same account

`https://www.newpages.asia/my/en/product/2010662/5-drawer-tool-cabinet/`
(HTTP 200, 25,930 bytes) — a Sui U product syndicated from their NEWPAGES
listing. **Two** followed links, neither carrying `rel`, one of them a deep link
to the matching product page on their own site:

```html
<a href="http://www.machinerytools.com.my" target="_blank">
<a href="http://www.machinerytools.com.my/index.php?ws=showproducts&products_id=2150655" class="btn btn-sm btn-primary w-100 text-nowrap" target="_blank">
```

This domain also surfaced in my Google-tool search results, so it is indexed and
not a dead mirror.

**Action:** confirm our 12 products are syndicating to newpages.asia. If they
are, this is free and automatic and scales with action #1. If they are not, ask
the rep to switch it on. INFERRED that it is account-linked rather than a
separate signup — the Sui U product IDs match across both domains — but I did
not verify the mechanism.

### 3. InfoPages — followed link, but ours is empty and the tier is unclear

Six profiles fetched. The pattern is sharp:

| Profile | Size | Website link |
|---|---|---|
| Quantum Tools Technology | 56,486 B | `<a href="https://www.quantumtoolstechnology.com" target="_blank" class="bold website-url">` — **followed** |
| Best Line Tooling | 88,564 B | `<a href="https://www.bestlinetooling.com" target="_blank" class="bold website-url">` — **followed** |
| Beyond Tool Servicing | 48,300 B | none |
| NTME Trading | 62,811 B | none |
| Spandy Tool Marketing | 16,334 B | none |
| M.E. Tools | 16,168 B | none |
| **Primaxs (ours)** | **15,377 B** | **none** |

No `rel` attribute on either link found — these are genuinely followed, and all
profiles carry `<meta name="robots" content="index, follow" />`.

**We already have a listing** —
`https://www.infopages.net.my/companies/primaxs-marketing-m-sdn-bhd-15738` — and
it is a bare 15KB stub passing us nothing.

The ~16KB profiles are bare stubs; the richer ones are enhanced listings. The
Quantum profile also carries a display-ad image from `infopagescdn.com`, so it
is a paying advertiser. **INFERRED: the website field is an upgrade, not part of
the free stub.** I could not confirm — the advertise page
(`infopages.net.my/advertise-with-us`) lists only "Online Package" and "Online
Package + Print Ads" with no prices and a sales-contact form.

**Action:** one email to InfoPages asking the direct question — *what does it
cost to add the website URL to our existing listing 15738?* If it is free or
cheap, take it; the link is genuinely followed. Do not assume either way.

### 4. Malaysia Brand — NEWPAGES sister, followed links

`http://www.malaysiabrand.com.my/` (HTTP 200, 3.5 MB) lists members with paired
links — one to their NEWPAGES profile, one to their own domain, the latter with
no `rel`:

```html
<a href="https://www.jjc.com.my" target="_blank" title="https://www.jjc.com.my">
<a href="http://www.uemachinery.com" target="_blank" title="http://www.uemachinery.com">
```

I found this because our own NEWPAGES profile links out to it, alongside
`suppliermalaysia.com`, `newjobs.com.my`, `newevent.com.my` and `homebagus.com`
— the NEWPAGES group's sister portals.

**UNVERIFIED:** whether an industrial distributor qualifies for a "brand"
directory, and whether inclusion is free with our existing membership.

**Action:** fold this into the same conversation as #2 — ask the NEWPAGES rep
which sister portals our membership already entitles us to. Cheap question,
possible free followed links.

---

## Not worth it, and why

**Do not re-research these.** Each was tested and failed. The anchor found is
quoted so the finding stands on its own.

### Verified nofollow — the link is there but passes nothing

**Seek Business** (seekbusiness.my) — **this corrects the existing plan.**
`marketing/directory-listings.md` calls this the "Highest-value listing on this
list" and records it as SUBMITTED on 5 Sep. It passes **no link equity**. Both
the CTA button and the contact-row website link are nofollowed, on every listing
I fetched:

```html
<a href="http://www.hapm.com.my/" class="ld__cta" target="_blank" rel="noopener nofollow" ...>
<a href="http://www.hapm.com.my/" target="_blank" rel="noopener nofollow" class="ld__contact-val" ...>
```

Same on a second listing (`ocania-sdn-bhd-sarawak-kuching`). The listing may
still be worth keeping for NAP consistency and direct enquiries — it is a real
directory with real traffic — but it must not be counted as a backlink. Worth
noting: its own pages carry a **sponsored** ad link to an SEO agency
(`onesearchpro.my`), which tells you what the site is monetising.

**BusinessList.my** — fails twice over. The website value is not even a direct
link; it is routed through an internal redirect, *and* nofollowed:

```html
<a href="/redir/138043?u=www.pneumatic.com.my" target="_blank" rel="noopener nofollow">www.pneumatic.com.my</a>
```

The existing plan already skipped this as paid (USD 20 basic / USD 65 a year).
Now there is a better reason: **even if you paid, the link is worthless.** Close
this one permanently.

**Listing.my** — blanket `rel="nofollow"` on every member link on the homepage:

```html
<a rel="nofollow" href="http://www.scs-mortgage.com.my/">
<a rel="nofollow" href="http://utamamotors.com.my/">
```

### Verified no outbound link at all

**B2BMap** — already established by your own check (zero external links, no
website field rendered). My research found nothing to revise. The existing plan
lists B2BMap as the top "highest value" account-gated target to do next — that
recommendation should be dropped.

**manufacturermalaysia.com** — fetched both a state page and the
`/cabinet-manufacturers/` category (493,567 bytes). Companies are listed, but
there is **not a single outbound link to any member's domain**. The only
external link on the whole site is a footer credit to an SEO agency
(`kangxiang.info/seo-malaysia/`). It is an SEO-agency content farm, not a
directory.

**Homepage-level only — no member link found, profile pages not individually
tested:** myindustryguide.com, thepages.com.my, suppliermalaysia.my,
tradeindia.com/my, tradekey.com, streetdirectory.com, malaysialistings.com (its
homepage links only to its own sister sites: freelistingindia, freelistingusa,
getlisteduae and so on — a template network, low value), and MATRADE's
`malaysiaservices.matrade.gov.my`. Flagging honestly: for these I fetched a
landing page rather than a member profile, so the finding is weaker than the
nofollow ones above. None showed enough promise to justify hunting further.

### Dead, parked or unreachable

| Target | What I found |
|---|---|
| **industry.com.my** | HTTP 200 but it is a **parked Hostinger default page** (16,369 bytes, links only to `hpanel.hostinger.com` support articles). There is no directory here. Remove from all lists. |
| **malaysiacentral.com** | Connection failed — unreachable. It is on the existing plan's target list; drop it. |
| **selangorpages.com** | DNS does not resolve |
| **trade42.com.my** | DNS does not resolve |
| **easyexport.my** | No response (your earlier finding, unchanged) |
| **MATRADE products directory** | The documented URL `matrade.gov.my/en/directory-hub/malaysia-products-directory` returned 404 |
| **FMM member list** | `fmm.org.my/Member_List.aspx` returned 404 |

MATRADE and FMM are both genuine institutions and both are member-gated with
real cost and document requirements — they are worth pursuing for audience,
grants and credibility, but **I could not verify that either passes a followed
link**, and neither is a free listing. Do not do them for SEO.

### Bot-blocked — no verdict either way

`yellowpages.my`, `exporthub.com`, `all.biz` and `mysbusiness.com` all returned
**403** to every method available to me, including a full browser header set and
the page-summarising fetch tool. I have **no** evidence for or against these.

Yellow Pages MY and all.biz are the two worth five minutes each in a real
browser — we appear to already have an all.biz listing (`4617-my.all.biz`). To
check one by hand: open the profile, right-click the website link → Inspect, and
read the `rel` attribute. If it says `nofollow`, `ugc` or `sponsored`, bin it.

---

## What to actually do, in order

1. **Expand the NEWPAGES listing.** Free, account exists, verified followed
   link, and it multiplies per product page. Everything else in this file is a
   rounding error next to this.
2. **Confirm newpages.asia syndication** is on for our products. Free.
3. **Email InfoPages** — what does it cost to put the website URL on listing
   15738? The link is followed; only the price is unknown.
4. **Ask the NEWPAGES rep** which sister portals (malaysiabrand.com.my and the
   others) our membership already includes.
5. **Hand-check yellowpages.my and all.biz** in a browser, since I was blocked.
6. **Correct the record** in `marketing/directory-listings.md`: Seek Business is
   nofollow, B2BMap should no longer be the top priority, BusinessList is
   worthless even paid, and industry.com.my / malaysiacentral.com are dead.

### One strategic note

The honest summary of this research is that **the verified list is short**. Only
the NEWPAGES family passed the followed-link test cleanly on a listing we can
have. Malaysian B2B directories have almost uniformly moved to nofollow, to
internal redirects, or to showing no website link at all.

That is not a reason to keep hunting for more directories — it is a reason to go
deep on the one platform that demonstrably works, which is also the platform our
top-ranking competitors have built their entire web presence on.

---

## Verification pass — 12 Sep, after the research

Two claims above were re-tested by hand against live HTML. One holds, one does
not.

### HOLDS: our NEWPAGES profile carries two followed links

```
<a href="https://www.storagesystem.com.my" target="_blank"
   title="Primaxs Marketing (M) Sdn Bhd" style="word-break:break-all;">
<a href="https://www.storagesystem.com.my" class="visit_website_btn"
   target="_blank" title="Visit Website">
```

No `rel` on either. Confirmed on `newpages.com.my/v2/en/company/93368/index.html`.

### DOES NOT HOLD: "the link repeats on every product page"

This was offered as the scaling insight — get more products up, get more
followed links. **It does not apply to our listing.**

Our profile renders its 12 products as inline images
(`/member_listing_product/2026....jpg`). There are **no per-product URLs** on it,
so there are no extra pages and no extra links. The `/products/78642/...`
example in the research came from a different, upgraded member.

Checked: zero `/products/` links on our profile, and none on Knight Auto's
either. Per-product pages appear to be an upgraded-tier feature.

**What this changes:** adding more NEWPAGES products is still worth doing for
reach — the 5 Timeline posts earn 278–393 impressions each — but it does **not**
multiply backlinks. We have the two links that listing will ever give us. Budget
effort accordingly, and do not pay for an upgrade on the assumption that more
products means more links without testing that first.
