# Weekly SEO + promotion playbook — storagesystem.com.my

Written 3 Oct 2026. On-page SEO is in good shape (titles, schema, sitemaps, hreflang, internal links).
From here, rankings move on four things only: **new pages that match real searches, pages Google
actually indexes, links from other sites, and people clicking.** Everything below feeds one of those.

**Rule for every task: research first, with live data.** GSC for our own numbers, SEOmator for
volume and difficulty, a live Google search (gl=my) for what currently ranks, People Also Ask and the
AI Overview. Never write from old notes.

Time budget: about 4–5 hours a week, split across five short sessions.

---

## Monday — measure (45 min)

| # | Task | Where | What to record |
|---|---|---|---|
| 1 | Performance, last 28 days vs previous 28 | GSC → Performance (URL-prefix property `https://www.storagesystem.com.my/`) | Clicks, impressions, CTR, average position. Baseline 2 Oct 2026: **151 clicks, 6,120 impressions, 2.5% CTR, position 30** |
| 2 | **Striking-distance queries:** position 8–20 with 20+ impressions | GSC → Queries, filter by position | These get a content upgrade this week (task 9) |
| 3 | **Zero-click queries:** 100+ impressions, 0 clicks | GSC → Queries | Title/description test candidates (task 14) |
| 4 | Indexing count | GSC → Pages | Indexed vs not indexed. Baseline 23 Sep: 1,320 indexed / 554 not |
| 5 | Confirm last week's pushes are live | `curl -s URL \| grep` | Cloudflare sometimes skips a build. If stale, push an empty commit (see memory: deploy reality) |
| 6 | Enquiries | WhatsApp + sales@ inbox | Count of new enquiries and which page they came from. This is the only number that pays |

## Tuesday — research (45 min)

| # | Task | Where |
|---|---|---|
| 7 | 10–12 keyword lookups on seeds from Monday's GSC list | SEOmator Keywords Explorer (Malaysia–English). **Free plan = 50 lookups a month, so about 12 a week.** Sub-tabs of a keyword already looked up are free; the Google Keyword Planner tab lists up to ~1,500 related terms |
| 8 | Live SERP check for the chosen topic | google.com/search?q=…&gl=my&hl=en — note People Also Ask, the AI Overview, and whether the top results are thin (marketplaces, Pinterest, unrelated pages) |

Pick the topic where: MY volume ≥ 50, keyword difficulty low, and the current top 10 is weak.
If an existing page already ranks for it, **upgrade that page instead of writing a new one**.

## Wednesday — publish (90 min)

| # | Task | How |
|---|---|---|
| 9 | One new guide **or** one deep upgrade of a striking-distance page | New guide: write `tools/guides_src/<name>.py` and run `python tools/make_guide.py <name>`. Only real product data from `docs/` (models, loads, Ringgit prices). 1,200+ words, a comparison table, the PAA questions as FAQ |
| 10 | Internal links | Link to it from its category page's "Related guides" and from 1–2 related guides |
| 11 | Register it | `docs/guides/index.html`, `docs/sitemap-guides.xml`, `docs/llms.txt`, then `python tools/add_lang_picker.py` |
| 12 | Ship and verify | Commit, push, check the Cloudflare build ran, then `curl` the live URL |
| 13 | Request indexing | GSC → URL inspection → Request indexing, for the new/updated URLs (quota ≈ 10 a day) |

## Thursday — links and listings (60 min)

| # | Task | Notes |
|---|---|---|
| 14 | Title/description test on one zero-click page | Change one page only, note the date, judge after 28 days. Do not touch pages already converting (perforated board, tool display board) |
| 15 | 2–3 genuine link or citation opportunities | Free only — no paid links, no PBNs, no link swaps at scale. Best sources: Tanko's distributor listing, Malaysian industrial directories with a real editorial check, trade associations, customer case studies (with their permission), supplier/partner pages, answering real questions on forums with a useful reply |
| 16 | Google Business Profile | One post linking the week's guide, plus new photos. Reply to every review. Ask each customer who received goods this week for a review |
| 17 | NAP consistency | Any listing with the wrong address (e.g. the old Ampang NewPages duplicate) gets corrected or reported |

## Friday — social and outreach (60 min)

| # | Task | Rules |
|---|---|---|
| 18 | Facebook Page post + share to groups | Post as **Primaxs Marketing only**. Research the pain first, then the product. Image attached **before** typing. Offer block in every post: free delivery and installation in Selangor/KL, outstation itemised, 1-year warranty. Never type "/". Match groups to the product |
| 19 | LinkedIn: one post (personal) + one Company Page post | 1,300–1,900 characters, no emoji, max 3 hashtags, real specs, admit one downside. Turn the week's guide into the post |
| 20 | LinkedIn: 20–25 connection requests | Target maintenance, plant, facilities, engineering and procurement managers at Malaysian factories, workshops, labs and TVET colleges. Short personal note. **No delivery-time claims** in messages |
| 21 | Follow up last week's accepted connections | One message each, via the `/messaging/compose` link. Verify by screenshot |

## Monthly (first week of the month)

- Re-pull GSC 28 days; compare against the previous month in `marketing/` notes.
- Merchant listings report in GSC (28 invalid vs 6 valid at the last check) — fix the top error.
- Chinese layer: close untranslated strings for the 80 remaining `/zh/` pages (`tools/build_lang.py zh --dry` shows the gap).
- Refresh SEOmator lookups budget plan for the month.

## What counts as progress

| Metric | Baseline (2 Oct 2026) | Target by end of Dec 2026 |
|---|---|---|
| Clicks / 28 days | 151 | 300 |
| Impressions / 28 days | 6,120 | 12,000 |
| Average position | 30 | under 20 |
| Queries in top 10 | (pull Monday) | double |
| Indexed pages | 1,320 (23 Sep) | 1,500+ |
| Enquiries from the site | (count Monday) | track weekly |

Page 1 for head terms like "tool cabinet" takes months on a domain that only went live in
September 2026. The fastest wins come from long-tail and comparison queries where the current
top 10 is weak. That is the reason for one research-led page a week rather than bulk content.

---

## Log

| Week of | Done |
|---|---|
| 29 Sep – 3 Oct 2026 | GSC pulled (369 queries). SEOmator: tool cabinet 260, tool trolley 210, shadow board 140, pegboard 3,600, metal pegboard 110, all KD 0. Published `/guides/tool-trolley-vs-tool-chest-vs-tool-cabinet-malaysia/` and `/guides/metal-pegboard-malaysia/`. Expanded the shadow-board guide in place (it already ranks for "shadow board for tools"). Fixed the nav language dropdown overflowing the screen and bumped the CSS version. Deployed and verified live. IndexNow accepted 7 URLs; sitemap-guides.xml resubmitted in GSC (Request indexing returned an error, retry Monday). GSC indexing now 1,544 indexed / 333 not (was 1,320 / 554 on 23 Sep). Tanko link-request email saved as a Gmail draft. Social drafts A-C in social-queue.md awaiting go-ahead |
| 6 – 9 Oct 2026 | Claude in Chrome was offline, so no GSC, SEOmator or social posting this run. **Locker gap:** live SERP showed office-furniture sellers own "steel locker malaysia" at RM200–900, so we compete on substance instead: /locker/ and /loker-besi/ now carry a per-model table (compartment inside size, Act 446 hostel minimum pass/fail, published price, price per door) and 6 new FAQs with schema; locker title/description retargeted to staff and hostel lockers; the steel locker guide gained an Act 446 section. **New guide:** /guides/workbench-height-ergonomics-malaysia/ (2,228 words; DOSH Standing at Work 2024 + CCOHS elbow rule + every Tanko bench height), linked from the how-to-choose guide's height sentence to avoid cannibalising its #1 for "workbench height malaysia". IndexNow accepted 7 URLs. Locker posters (EN/ZH) and 5 post drafts saved in social-queue.md, awaiting go-ahead. Found 41 product pages showing a build-default RM1,500 price (marketing/price-placeholders-2026-10-09.md), not changed. Carry over to when Chrome is back: GSC Monday pull + request indexing for the 6 changed URLs, SEOmator "workbench height" volume, LinkedIn follow-ups and 20–25 invites, the posts. |
| 9–10 Oct 2026 (Chrome back) | GSC 28d to 6 Oct: **169 clicks / 6,930 impr / 2.4% CTR / pos 25.9** (was 151 / 6,120 / 30), 449 queries, 177 in the top 10. Indexing **1,930 indexed / 64 not** (was 1,544 / 333). New metal pegboard guide already at pos 5.7; "staff locker" pos 3.7. Request indexing accepted for the workbench height guide, /locker/, steel locker guide, /loker-besi/. SEOmator: "workbench height" only 10–20/mo, "adjustable work table" 50 (6 of 50 lookups left). Social: FB EN post + 9 groups, FB 中文 post + 3–4 groups, LinkedIn personal/Page and GBP scheduled 12–13 Oct, 8 LinkedIn follow-ups, 21 new invites with notes, FB comment answered. |
