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
| 10 Oct 2026 (evening) | GSC 28d to 6 Oct re-read: page-one zero-click pages found (stainless guide pos 7.4 / 388 impr / 0 clicks; perforated guide pos 4.9 / 127 / 1). Retitled 5 pages for B2B intent. New guide /guides/new-factory-storage-fit-out-checklist-malaysia/ (2,159 words; indexing requested; IndexNow). Organization JSON-LD on all pages: legalName, foundingDate, SSM ids, sameAs LinkedIn / Maps CID / NewPages. llms.txt: all phones, Samsung, old-address correction. IndexNow: all 1,973 URLs. Bing Webmaster: sitemap resubmitted (last read 11 Sep); **Copilot cited the site 85 times since 13 Sep** (28 on 7 Oct). Brave: own site absent from top 8 for "Primaxs Marketing Sdn Bhd"; wrong directories (contact.page "Packaging Machinery" KL, all.biz KL) rank instead. Yelp correction submitted to moderators (Balakong address, 03-4296 4737, website); all.biz support asked to attach listing 4617 and fix it; Hotfrog listing filled (ALTCHA + submit left for Wei Ming); MATRADE step 1 filled. Posters + copy for week of 12 Oct written (fit-out checklist, steel vs hardboard). Plan: growth-plan-update-2026-10-10.md. |
| 14 Oct 2026 | GSC 28d: the trolley comparison guide sits at pos 7–12 for head tool-cabinet terms (tool drawer 7.0, tool box cabinet 8.1, tool storage cabinets 9.1, tool chest 10.4, tool cabinet 12.1) and the tool cabinet guide at 14.5 for "tool cabinet malaysia", 9.4 "roller cabinet", 7.0 "workshop cabinet". Both retitled to those terms. The site-wide Guides menu (desktop + mobile, ~1,977 pages) now links the trolley comparison, metal pegboard, showroom pegboard, fit-out checklist and training workshop guides. **Note:** these five aren't in site/content/guides.py, so a rebuild would drop them from the menu (never rebuild docs/). New guide /guides/training-workshop-benches-tool-storage-malaysia/ (Budget 2027 TVET; HRD Corp ALAT stated honestly: cabinets are not claimable). Social: FB 中文 showroom post + 3 groups, 7 LinkedIn invites (Vertiv, Collins Aerospace, Chery Malaysia plant/facilities). |
| 14 Oct 2026 (afternoon) | **CTR pass (GSC 28d to 11 Oct):** the stainless guide's 0.2% CTR is not a title problem. About 380 of its 444 impressions are for a competitor brand ("marya ... stainless steel workbench"), so leave it. "perforated board malaysia" sits at pos 3.5 (guide 3.9, category 5.5) with 0 clicks, but both were retitled 10 Oct, after most of this window: re-read around 24 Oct. "primaxs": homepage pos 2.0, 36% CTR (fine). "mould rack manufacturers malaysia" at pos 4.4 with 0 clicks: the /rack/ description now names Tanko as the Taiwan manufacturer since 1975 (title left alone, changed 10 Oct). /workbench/ ranks 26–35 for "industrial workbench" and "workbench malaysia" despite 2,044 words: an authority gap, not on-page. **Indexing:** the training guide was already indexed the same day. Request indexing accepted for the retitled trolley and tool cabinet guides. IndexNow accepted 15 URLs plus /rack/. **Bing AI Performance:** 91 Copilot citations (85 on 10 Oct). Cited pages: /workstation/ 28, BM tool-cabinet guide 14, /kabinet-alat/ 14, perforated guide 9, /perforated-board/ 8, meja-kerja guide 4. The Malay layer earns AI citations even with ~0 Google clicks. The only sampled grounding query is "production workstation". So /workstation/ got price-range and size FAQs (FAQPage now 7), and llms.txt now gives a starting guide price per category. |
| 15 Oct 2026 | **Ranking audit after Wei Ming saw two quiet days:** no URL changed. 9 existing titles changed 9 to 14 Oct; GSC to 12 Oct shows none lost position (/locker/ improved 15-20 → 5; rack, stainless and perforated held at 3-6; heavy-duty flat at 8-11). The /sales/ dashboard shows 11 and 9 WhatsApp clicks on 12 and 13 Oct, 2 on 14 Oct, 1 email on 15 Oct: leads are lumpy, not broken. New standing rule: no title or URL changes on ranking pages, additive only. **Structured-data fix (schema only, 1,744 EN pages, one ld+json line each):** the return policy said 7-day free returns, while the real /returns/ policy is no change-of-mind returns, so it is now MerchantReturnNotPermitted with a merchantReturnLink. The RM0 nationwide shipping and 3-7 day transit claim was removed (delivery is free in Selangor/KL only). The Tanko manufacturer had carried Primaxs's sameAs links since 14 Sep and now points to tanko.com.tw/en/. 813 ProductGroup variants got real sizes; 12 document-cabinet families with unpublished sizes dropped 'size' from variesBy. GSC merchant listings were 10 invalid / 7 valid with "size missing" critical; validation started. build.py mirrored. IndexNow accepted 1,744 URLs. docs/zh still carries the old schema until the next build_lang run. |
| 15 Oct 2026 (evening) | **Indexing:** 1,940 indexed, 79 not. 404s traced to the language layers: every /zh/ nav linked four unbuilt /zh/ category pages (/zh/workbench/, /zh/workstation/, /zh/hanger-rack/, /zh/parts-cabinet/), and the Malay home linked /ms/<category>/ instead of the real Malay slugs. 1,307 links were repointed (zh → EN page, ms → /meja-kerja/ etc.). build_lang.py now links only to pages that pass coverage or already exist, and maps Malay via hreflang. Site-wide internal link check: 0 broken (checker decodes %20). **Speed (PageSpeed mobile):** homepage perf 69 → 86, LCP 12.3 s → 3.1 s, CLS 0. The preload pointed at an unused file and the hero was a 447 KB PNG. Hero and category cut-outs are now WebP (600w + full) via <picture> with PNG fallback; layout verified identical (page height and every image box, mobile and desktop). 317 category/family pages had broken preloads (`imagesrcset="/ 800w, …"` made phones preload the homepage HTML as an image); they now mirror their <img>, and the base.html template is fixed. /workbench/ mobile: perf 87, SEO 100, best practices 100, a11y 92 (contrast + colour-only links, not changed: a visual design call). **New guide:** /guides/data-centre-fit-out-workbenches-spares-storage-malaysia/ (1,669 words; Knight Frank Johor 1,110MW live / 8,542MW pipeline, BMI 2GW under construction, MIDA Q1 RM34.6bn). ESD stated honestly as quoted per project. Registered in the index, sitemap and llms.txt, linked from the ESD guide, IndexNow + Google request indexing done. |
| 18 Oct 2026 | GSC 28d: **184 clicks / 7,970 impr / pos 22.6** (was 169 / 6,930 / 25.9 on 6 Oct). The 14 Oct retitles held: trolley guide 8-10, tool cabinet guide 10-13 (same range as before), no rollback. **Sitemaps:** every product URL had lastmod 2026-09-15 despite the 15 Oct structured-data fix. lastmod now comes from git: the last significant change per page, ignoring site-wide menu/footer sweeps (>100 files) except the structured-data commit. Updated 1,591 products, 184 categories/families, 17 guides, 92 zh; index resubmitted in GSC ("已成功提交"). **New guide:** /guides/esd-storage-anti-static-bins-drawers-malaysia/. Built because 'esd storage' had 103 impr at pos 79 and 'esd box' 33 at 68, both landing on the workbench guide. It covers TKI-2 "-9" anti-static drawers (10^4-10^6 ohm), TKI-83 black bins and the KPQ-4302/4304 sets, plus the S541 resistance classes. Request indexing + IndexNow done. Internal links to the data centre guide were added from /workstation/, the fit-out checklist and the electronics page. Bing Webmaster recommendations: "No pages found". Copilot: /perforated-board/ citations 8 → 10. Next content gaps from GSC 90d: "workshop storage bins" (144 impr, pos 46); the warehouse cluster ("warehouse storage malaysia" 192 at pos 65) is a catalogue gap (no pallet racking), so not a target. |
| 19 Oct 2026 | Daily routine. Both new guides are already indexed (data centre fit-out, ESD storage). **Bins gap:** "workshop storage bins" 146 impr at pos 46 sitewide, landing on /guides/ and /parts-cabinet/. The parts-bin guide already ranks 14.8 for it, so instead of a new page (cannibalisation risk) it got a section, "Workshop storage bins: which type for which job" (TA-1 PE team bins, TKI-83 hanging bins with an anti-static option, TC-11 PC tilt-out bins for oily parts, drawer cabinets, KH-306A louvred board) and a FAQ (FAQPage updated). Title unchanged. Sitemap lastmod set to 19 Oct, IndexNow + request indexing done. |
| 21 Oct 2026 | Daily routine. GSC 28d to ~18 Oct: **181 clicks / 8,340 impr / pos 22.6** (was 184 / 7,970 / 22.6). ESD storage guide confirmed indexed. **Tool drawer gap:** 'tool drawer' 84 impr and 'tool box cabinet' 81 impr; the trolley comparison guide ranks ~7 for both with 0 clicks (/tool-cabinet/ ~47). Additive only: new section 'Tool drawers and tool box cabinets: what to check' (per-drawer load 45/50/100/200kg, extension, EA first-drawer division boxes / 3x3 / 2x2 dividers, central lock, link to heavy-duty workbenches) + 2 FAQs (FAQPage now 8), dateModified 21 Oct. Title unchanged. Mirrored in tools/guides_src. Link check 0 broken; sitemap lastmod from git (6 entries); live verified; IndexNow 200; request indexing accepted. |
