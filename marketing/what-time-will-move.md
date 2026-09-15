# What waiting will actually move — and what it won't

Written 16 September 2026, at the start of a deliberate week of changing nothing
on the site and running promotion only. Numbers below are today's baseline, so
next week's comparison is arithmetic rather than impression.

---

## Today's baseline

| Metric | Source | Today |
|---|---|---|
| Clicks (28d) | Search Console | **64** |
| Impressions (28d) | Search Console | **3,470** |
| CTR | Search Console | **1.8%** |
| **Average position** | Search Console | **42.9** |
| Distinct queries | Search Console | 259 |
| **Pages indexed** | Search Console | **602** |
| Pages not indexed | Search Console | 1,239 (1,228 discovered-not-indexed, 10 × 404, 1 crawled-not-indexed) |
| Pages in sitemap | live | 1,851 |
| **Bing URLs indexed** | Bing Webmaster | **28** |
| Referring domains | Bing Webmaster | **2** (newpages 90, aseanbizs 5) |
| Copilot citations | Bing AI Performance | **6** |
| Merchant Center | Google | 1,517 products, 1,517 local inventory matched |

Per-query positions worth watching (Search Console, un-personalised averages):

| Query | Position |
|---|---|
| primaxs | 1.2 |
| tanko malaysia | 3.2 |
| tool display board | **5.5** |
| perforated board | **8.1** |
| workbench in malaysia | 17.0 |
| workbench malaysia | 21.1 |
| heavy duty tools cabinet | 39.2 |
| tool cabinet malaysia | 43.1 |
| tool cabinet | 53.4 |
| warehouse storage malaysia | 78.0 |

---

## Things that move on their own, given time

**1. The indexing backlog — the biggest one.**
602 of 1,851 pages are indexed; 1,228 are "discovered, currently not indexed",
meaning Google knows about them and has not got to them. That queue drains on
its own. Every page indexed is a page that can rank. *Watch: indexed count.*

**2. Crawl budget freed by the 404 fix.**
196 malformed `srcset` entries were sending Googlebot to 404s — about 12% of all
its requests to the site. That is fixed, but Google only learns it as it
re-crawls. Less waste means more of the same budget spent on real pages.
*Watch: Crawl Stats, the 404 share.*

**3. Internal linking already done, but not yet counted.**
Median inbound links per product page went 7 → 13, orphaned mother pages went to
zero, and 559 single-inbound pages went to zero. Those signals only register as
Google re-crawls the pages carrying the links. *Watch: average position.*

**4. Domain maturity.**
The site is young. Part of sitting at position 42.9 is simply that Google
discounts sites it has not known long. That discount fades without any action.

**5. Bing, which is badly behind and has the most headroom.**
28 URLs indexed of 1,851. IndexNow pushes all 1,851 per submission and Bing
accepts 100 manual URLs a day. This is also the AI lever: Bing's index is what
Copilot and ChatGPT search read, and we currently have 6 citations.
*Watch: Bing indexed count, AI Performance citations.*

**6. The things shipped in the last two days, once crawled.**
Unique preview image on all 1,851 pages, alt text on all 1,851, four Klang
Valley location pages, 1,517 products and 1,517 local inventory rows in Merchant
Center, and robots.txt naming 23 AI crawlers with none blocked.

**Rough timescales:** re-crawl of changed pages, days to two weeks. Indexing
backlog, weeks to months. Ranking response to crawl efficiency and internal
links, one to three months. Domain maturity, six to twelve.

---

## Things waiting will NOT move

**The link gap.** Two referring domains against Knight Auto's eleven; 90 links
against their 23,900. Time does not create links. This is the binding
constraint on "tool cabinet malaysia" at position 43, and no amount of patience
changes it. It is the NEWPAGES tier decision, and it costs money.

**Terms where we are structurally outmatched.** "steel locker malaysia" is owned
by officepro, goodview and asiastar, for whom lockers are the entire business.
Lockers are about twenty SKUs for us. Waiting will not change that arithmetic.

**Terms whose searchers want something else.** "warehouse storage malaysia"
returns Crown Workspace, Asian Tigers and Rhenus — relocation and third-party
warehousing *services*. "heavy duty tools cabinet" returns RS Online, Knight
Auto and Shopee — price comparison, not specification. Those impressions will
never convert no matter where we rank.

**Anything requiring an account we do not have.** robuta is a search engine, not
a directory. onesync is NEWPAGES' own product. MyPages' form is broken.
JawatanKosong is subscription-only.

---

## How to read next week

Measure in **Search Console**, not in a browser. Browser results — incognito
included — carry your location, device and an AI Overview that pushes organic
results down the page. Search Console averages real impressions and does not.

The honest expectation for one week of promotion and no site changes: indexed
count up, average position slightly down (better), impressions up modestly,
clicks roughly flat. One week is short. The numbers that matter move over months.
