# PROMOTION STATE — private working file

**This file is gitignored. It never goes to GitHub or Cloudflare.**
Running memory of the promotion work. Update at the end of every run.

Last updated: **6 Sep 2026** (second session — see §14-17)

---

## 0. Read this first when Wei Ming says "start promoting"

1. §5 — **identity rules**. Facebook = Primaxs Page ONLY. LinkedIn = either.
2. §6 — which groups accept Page posts. Only post where the Page can post.
3. §7 — voice rules. §8 — post bank. §9 — images.
4. Post, then log it in §10 and update "last posted" in §6.

---

## 1. The business, in one block

```
Business name:  Primaxs Marketing (M) Sdn Bhd
Address:        No. 39, Jalan Balakong Jaya 4, Taman Industri Balakong Jaya,
                43300 Seri Kembangan, Selangor, Malaysia
Phone:          +60 3-4296 4737
Mobile:         +60 12-616 3088
WhatsApp:       +60 11-5841 9886
Email:          sales@storagesystem.my
Website:        https://www.storagesystem.com.my
Founded:        2006
Hours:          Mon-Fri 09:00-18:00, closed weekends
Role:           Wei Ming = Business Development Manager (NOT founder — uncle's company)
Brand:          Exclusive Malaysia distributor for Tanko Enterprise Co., Ltd.
                (Taiwan, manufacturing since 1975)
Range:          ~1,700 SKUs across 11 ranges
```

## 2. THE COMMERCIAL OFFER — must be in every promotional post

```
FREE delivery      — Selangor & Klang Valley
FREE installation
Outstation         — delivery quoted separately, itemised
FREE 1-year warranty against manufacturing defects, administered from the
                     Selangor office. Nothing ships back to Taiwan.
High quality       — Tanko, Taiwan, manufacturing since 1975
Ringgit quotes     — unit / project / delivery itemised separately
Stock in Selangor  — 3-7 working days Klang Valley, 5-10 Peninsular,
                     10-14 East Malaysia
```

These are the close-the-deal levers. Free delivery and free installation are
the two strongest in Malaysian industrial B2B.

---

## 3. Accounts and where each is driven from

| Channel | Status | Driven from |
|---|---|---|
| Google Business Profile | Live | Publer |
| LinkedIn personal (Wong Wei Ming) | Live | Publer |
| LinkedIn Company Page (primaxs-marketing) | Live | Publer |
| Facebook Page (Primaxs Marketing, 71 followers) | Live | **Meta Business Suite** |
| Facebook groups | 19 joined | Manual |
| B2BMap | 6 products live, free tier capped at 6 | Manual |
| Yellow Pages MY | **Advertiser account created** — see §12 | Manual |

**Publer free tier = 3 accounts.** GBP + LinkedIn personal + LinkedIn Page.
Facebook schedules natively in Meta Business Suite (free, uncapped).

**Meta Business Suite asset_id:** `1529504613734678`
- Composer: `https://business.facebook.com/latest/composer/?asset_id=1529504613734678`
- Planner: `https://business.facebook.com/latest/content_calendar?asset_id=1529504613734678`

---

## 4. Where the research lives (committed to the repo)

- `marketing/icp-and-pains.md` — 8 buying segments, 15 numbered pains, trigger events, objections
- `marketing/post-template.md` — **Malaysian Facebook register**, offer blocks in 3 languages, hashtag sets, group-search keywords, safe-volume rules
- `marketing/content-calendar.md` — link policy, cadence, post bank, execution log
- `marketing/linkedin-pack.md` — LinkedIn format research + 24-post bank
- `marketing/directory-listings.md` — canonical NAP, paste-ready descriptions
- `marketing/google-ads-*.csv` — 96 keywords, 17 ads, 49 negatives (not switched on)

---

## 4b. THE BIG UNLOCK — post to the Page AND up to 9 groups in one go

Discovered 6 Sep 2026. **This is now the primary posting method.**

Facebook's own Page composer has a native "share to groups" step. One post →
the Page **plus up to 9 groups**, published **as Primaxs Marketing**, with
multiple photos. It is Facebook's own feature, so it is not a spam workaround.

**The exact sequence:**

1. Go to `facebook.com/primaxsmarketing` (make sure the top-right avatar is Primaxs)
2. Click the **分享新鲜事** composer box (NOT Meta Business Suite — that one cannot attach photos)
3. Click into the text area, wait ~4s, type the post. **If the text does not appear, click and type again** — the first attempt after opening often fails
4. Attach photos: find the file input inside the dialog, expose it, get its ref, `file_upload` (see §9)
5. Click **下一页** (Next)
6. On 帖子设置, click **分享到小组** (Share to groups)
7. Tick the groups — **match the language and product to the group**
8. Click **完成** (Done), then **发帖** (Post)

**Gotchas:**
- The group list only shows groups that **allow Page posting**. If a group is missing from that list, the Page cannot post there — that is the signal, do not hunt for it.
- The final 发帖 click misses often. **Always verify the post appears on the Page afterwards**, and redo it if not.
- Do not reuse the same group for two posts on the same day.

---

## 5. IDENTITY RULES — do not get this wrong

| Platform | Post as |
|---|---|
| **Facebook Page** | **Primaxs Marketing — ALWAYS** |
| **Facebook groups** | **Primaxs Marketing — ALWAYS.** If a group blocks Page posting, skip that group. Do not fall back to the personal profile. |
| LinkedIn personal | Wong Wei Ming |
| LinkedIn Company Page | Primaxs Marketing |

Switch identity via the Facebook top-right avatar → pick Primaxs Marketing.
**Check the composer avatar before typing.**

---

## 6. Facebook groups — 19 joined, with Page-posting status

`Page OK` = the Page can post. `Personal only` = no composer appears as the
Page → **skip, per §5**. `?` = not yet tested.

### Automotive

| Group | Members | Activity | Page posting | Last posted |
|---|---|---|---|---|
| Mekanik kereta & Info² Kereta | 390,000 | 10+/day | ? | never |
| MEKANIK KERETA ANAK MELAYU | 29,000 | 2/day | ? | never |
| Jual.beli peralatan bengkel — Selangor KL | 21,000 | 8/day | ? | never |
| **Iklan Bengkel-Bengkel Malaysia** | 3,955 | 10+/day | **Page OK** | **6 Sep 2026** |
| bengkel kereta satu malaysia | 3,095 | 7/day | ? | never |
| Workshop Bengkel kereta seluruh Malaysia | 1,187 | 4/day | ? | never |

### Chinese hardware / industrial — the highest-value cluster found

| Group | Members | Activity | Page posting | Last posted |
|---|---|---|---|---|
| 五金交流区～品牌～发展～批发 Supplier Hardware | 64,000 | 20+/day | ? | never |
| 五金机械批发/零售 | 53,000 | 90+/day | ? | never |
| **马来西亚五金广告区 malaysia hardware advertise** | 34,000 | 10+/day | **Personal only — SKIP** | (see §12) |
| 马来西亚机械与模具工业技术交流平台 | 31,000 | 30+/day | ? | never |
| 全马工业五金交易平台 | 21,000 | 50+/day | ? | never |
| 马来西亚建筑五金门业广告群 | 7,871 | 20+/day | ? | never |
| 大马五金批发交流 Hardware Wholesale & Distribution | 6,588 | 10+/day | ? | never |

### Industrial / machinery (English + Malay)

| Group | Members | Activity | Page posting | Last posted |
|---|---|---|---|---|
| second hand machinery malaysia | 75,000 | 30+/day | ? | never |
| Used Industrial Machines for Sale/Purchase | 14,000 | 60+/day | ? | never |
| 马来西亚二手机床&零件买卖 | 12,000 | 7/day | ? | never |
| MALAYSIA CONSTRUCTION MACHINERY | 6,579 | 10+/day | ? | never |
| Malaysian machineries. | 3,946 | 10+/day | ? | never |
| Malaysia Agriculture & Industry Machinery Traders | 1,758 | — | ? | never |

### Group rules learned

- **Iklan Bengkel-Bengkel Malaysia**: "hanya untuk iklan bengkel-bengkel... produk berkaitan bengkel... Target Untuk bengkel kenderaan sahaja." → ads are the purpose; **vehicle workshops only**, so tool cabinets/trolleys/benches, never warehouse racking.
- **大马五金批发交流**: membership questionnaire (region + "do you need marketing"). Answered Central Malaysia / "No, I can handle myself". **First post needs admin approval.**
- **马来西亚五金广告区**: description "这里是五金的分享区". Feed is wall-to-wall supplier ads with prices and phone numbers — the right register, but Page posting is blocked.

### Tool & power-tool groups — joined 6 Sep (second wave)

| Group | Members | Activity | Page posting | Last posted |
|---|---|---|---|---|
| **Power Tools Malaysia** | 100,000 | 20/day | **Page OK** | **6 Sep 2026** |
| Malaysia Power Tools (Second Hand & New) | 68,000 | 5/day | **Page OK** | **6 Sep 2026** |
| Jual Beli Barang Hardware/ Tools | 65,000 | 40+/day | **Page OK** | **6 Sep 2026** |
| Hardware Tools Global Sourcing and Supply | 12,000 | 80+/day | **Page OK** | **6 Sep 2026** |

Facebook refused further joins after these four — Tools & hand tools & Hardware
(17k), Hardware Building Material & Machinery (10k) and My Power Tools Beli
Sewa Swap (21k) are still open and should be the first joins next session.

### Not yet joined — do these next

| Group | Members | Why |
|---|---|---|
| Jual Beli Barang Hardware/ Tools | 65,000 | Tool buy/sell, huge |
| Hardware,Furniture Hardware & All Hardware Products | 41,000 | Import/export traders |
| Hardware Tools Global Sourcing and Supply | 12,000 | 80+/day |
| Hardware, Building Material & Machinery Malaysia | 10,000 | 50+/day |
| 马来西亚紧固件及五金材料广告区 | 10,000 | 20/day |
| 马来西亚建筑材料供应 | 8,078 | 10/day |
| 新柔 金属制造 社区 JB-SG Metal Process | 2,283 | Johor metal processing — CNC fit |
| 马来西亚烧焊/焊接讨论区 Malaysia Welder Group | 1,935 | Welding → heavy duty benches |

**Rate limit: Facebook stops accepting joins after ~12 in a session.** Cap at
5-6 per day.

---

## 7. Voice rules — how not to sound like AI

**LinkedIn and Malaysian Facebook are opposites.** Full detail in
`marketing/post-template.md`. Summary:

| | LinkedIn | Malaysian Facebook / groups |
|---|---|---|
| Emoji | Never | Yes, as section markers |
| Length | 1,300–1,900 chars | Short, scannable |
| Links | Costs ~60% reach | Expected |
| Offer block | No | **Mandatory** |
| Hashtags | Max 3 | 5–8 niche |

**Never write:** "elevate", "unlock", "solutions", "seamless", "in today's
fast-paced", emoji bullet spam, three rhetorical questions, "Are you looking
for...".

**Always:** open with a specific number or a specific failure. Use real specs
(100kg vs 200kg slides, 900/1,500/3,000mm aisles, 740-760mm bench height,
BT-30/BT-40/BT-50/HSK-40/HSK-63). Admit a downside somewhere.

**Reference for the local register:** CT Hardware (89k followers, 5 Klang
Valley stores) — bold headline, emoji markers, hard offer block, price, phone.

---

## 8. Post bank — rotate these

| # | Hook | Pain | Product | Images |
|---|---|---|---|---|
| G1 | 15 min finding a spanner, 3x a day, 100+ hrs/yr per tech | 1 | Pegboard, shadow board | `KP-4114`, `KP-4120`, `KH-306A` |
| G2 | A BT-40 holder costs more than the cabinet storing it | 3 | CNC tool cabinets | `EA-10031-11N`, `EA-10031-222MN` |
| G3 | Drawer slides bind when loaded — why cabinets get replaced | 6 | Tool cabinets | `EGA-10061`, `EGA-10091` |
| G4 | Loker besi: start with the user, not the wall (BM) | 7 | Lockers | `FBA-202W`, `FBA-204AW` |
| G5 | Workbench top is a task decision, not a taste decision | 5 | Workbenches | `WE-47W (White)`, `WAS-54022F` |
| G6 | Import vs local — the lines missing from the comparison | 13 | All | `WAS-54022F`, `RA-6091...` |
| G7 | Moulds on ordinary racking — concentrated vs distributed | 11 | Mould racks | `MB-206`, `MB-208` |
| G8 | The spares room needs an address system, not more cabinets | 10 | Parts cabinets | `TKI-1308`, `TKI-1308-2` |
| G9 | An ESD bench with no verified ground gives no protection | 9 | ESD benches | `WAS-54022F2` |
| G10 | Five things to send for a same-day quote | 14 | All | any 3 |
| G11 | **Range post** — all categories, shows breadth | — | All | one per category |

---

## 9. Images

Source: **`asset3/`** in the repo root — 2,151 `.jpg` files, named by SKU.
(`docs/asset3/` is WebP-only; use the root folder for uploads.)

- **Group posts: 3–5 images, always.** No image = almost no reach.
- **Range posts: one image per category** — workbench, tool cabinet, CNC, locker, racking. Shows breadth and pulls more clicks.
- Never mix SKUs inside a single-product post.

```bash
ls asset3/ | grep -i "^EGA-100" | grep "\.jpg$"
```

**How to attach (the native picker cannot be driven):**
1. Open the composer and type the text first
2. `document.querySelectorAll('input[type=file]')` → find the one with `image` in `accept`
3. Make it visible + give it an `aria-label`, then `read_page` to get its `ref_N`
4. `file_upload` with that ref and absolute paths
5. Confirm via `read_page` — attachment worked if "移除帖子附件" (remove attachment) appears

**Where photo upload works and where it does not — tested 6 Sep 2026:**

| Surface | Multi-photo upload | Note |
|---|---|---|
| Facebook **group** composer | **Works** — file input exists, use the ref trick above | Proven with 5 images |
| **Meta Business Suite** composer | **Does not work** — the photo button opens the OS picker directly and creates no file input | But it auto-attaches the website's OG card, which is a Primaxs-branded graphic and looks good |
| Facebook **Page** timeline composer | **Not found** in the current Page layout while in "manage page" view | Needs another route — try the Professional Dashboard, or post from the group composer pattern |

**Practical rule:** Business Suite for scheduled Page posts (OG card carries the
visual). Group composer when you need 3–5 real product photos.

---

## 10. Post log

| Date | Channel | Post | Status |
|---|---|---|---|
| 6 Sep | Facebook Page | Tool-search arithmetic (G1) | **PUBLISHED** |
| 8 Sep 09:00 | Facebook Page | CNC taper (G2) | Scheduled |
| 11 Sep 09:00 | Facebook Page | Loker besi BM (G4) | Scheduled |
| 15 Sep 09:00 | Facebook Page | Workbench tops (G5) | Scheduled |
| 18 Sep 09:00 | Facebook Page | Drawer slides EN (G3) | Scheduled |
| 18 Sep 15:00 | Facebook Page | 工具柜滑轨 中文 (G3) | Scheduled |
| 22 Sep 09:00 | Facebook Page | Kabinet alat BM + full offer (G11) | Scheduled |
| 25 Sep 09:00 | Facebook Page | Mould racks EN + full offer (G7) | Scheduled |
| 8 Sep 09:00 | LinkedIn personal | Humidity — three failures | Scheduled |
| 10 Sep 09:00 | LinkedIn personal | Drawer slides | Scheduled |
| 15 Sep 09:00 | LinkedIn personal | Spares room address system | Scheduled |
| 17 Sep 09:00 | LinkedIn personal | Racking aisle width | Scheduled |
| 22 Sep 09:00 | LinkedIn personal | ESD grounding | Scheduled |
| 24 Sep 09:00 | LinkedIn personal | Import vs local (link post) | Scheduled |
| **16 Sep 09:00** | **LinkedIn Company Page** | Workbench 3 questions + full offer | Scheduled |
| 6 Sep | FB group: Iklan Bengkel | Kabinet alat BM | **PUBLISHED as Page** |
| 6 Sep | **LinkedIn Company Page** | Steel lockers + full offer, 3 photos | **PUBLISHED** |
| 6 Sep | **LinkedIn personal** | Workbench top materials, 3 photos | **PUBLISHED** |

| 6 Sep | **FB Page + 5 groups** | Tool storage EN "where do your tools live", 5 photos, full offer | **PUBLISHED as Page** — Power Tools Malaysia, Malaysia Power Tools, Jual Beli Barang Hardware/Tools, Hardware Tools Global Sourcing, Malaysia Agriculture (~247k members) |

**Group cross-posts CONFIRMED by Facebook notifications** — 15 placements:
second hand machinery malaysia · 五金机械批发/零售 · 五金交流区 ·
马来西亚机械与模具工业技术交流平台 · 大马五金批发交流 ·
Jual.beli peralatan bengkel (**admin approved the photo post**) ·
MEKANIK KERETA ANAK MELAYU · bengkel kereta satu malaysia ·
Iklan Bengkel-Bengkel Malaysia · Workshop Bengkel kereta seluruh Malaysia ·
Power Tools Malaysia · Malaysia Power Tools (Second Hand & New) ·
Jual Beli Barang Hardware/Tools · Hardware Tools Global Sourcing ·
Malaysia Agriculture & Industry Machinery Traders

**Keyboard shortcuts were NOT disabled.** The dialog that appeared was dismissed
with X, not "停用". Verified at facebook.com/settings/?tab=accessibility —
no shortcut override is set. The fix for the "/" problem is to avoid the
character, not to change Wei Ming's settings.
| 6 Sep | **FB Page + 5 groups** | CNC tool storage EN, 4 photos, full offer | **PUBLISHED as Page** — 五金机械批发/零售, second hand machinery malaysia, 五金交流区, 马来西亚机械与模具, 大马五金批发交流 (~230k members) |
| 6 Sep | **FB Page + 5 groups** | Kabinet alat BM, 4 photos, full offer | **PUBLISHED as Page** — Jual.beli peralatan bengkel, MEKANIK KERETA ANAK MELAYU, bengkel kereta satu malaysia, Iklan Bengkel, Workshop Bengkel (~58k members) |

Google Business Profile: 7 posts queued through 23 Oct.

---

## 11. Still to do

**Posts not yet scheduled:** LinkedIn personal 29 Sep + 1 Oct; LinkedIn Company
Page 23 + 30 Sep; Facebook Page 29 Sep onward.

**Group posting:** use the §4b share-to-groups flow. Groups still unused:
马来西亚二手机床, 马来西亚建筑五金门业广告群, MALAYSIA CONSTRUCTION MACHINERY,
Malaysian machineries, Malaysia Agriculture & Industry Machinery Traders,
Used Industrial Machines for Sale/Purchase.

**Chinese range post (工业储存设备) — attempted FOUR times, still not published.**
Attempts 1-3 failed because of the "/" shortcut bug (now diagnosed, see §13).
Attempt 4 used "、" instead, the text landed correctly, 5 photos attached and
6 groups were selected — and it still did not appear on the Page.

At that point I stopped rather than try a fifth time. Four attempts on one post
in a session is already the pattern that gets Pages restricted, and the other
posts that day went out fine, so this is most likely a per-post throttle.

**Next run: retry it FIRST, before any other Facebook activity**, using the
slash-free copy. Groups queued: 大马五金批发交流, 马来西亚二手机床,
马来西亚建筑五金门业广告群, MALAYSIA CONSTRUCTION MACHINERY,
Malaysian machineries, Malaysia Agriculture & Industry Machinery Traders.

**Join:** the 8 groups in §6.

---

## 11b. Facebook Page info — completed 6 Sep 2026

| Field | Value | Status |
|---|---|---|
| Bio | "Exclusive Malaysia distributor for Tanko industrial storage since 2006. Workbenches, tool cabinets, CNC tool storage, lockers, racking. Selangor stock. FREE delivery & installation in Selangor/KL. 1-year warranty. Ringgit quotes." (226/255) | **Done** |
| Phone | +60 3-4296 4737 | **Done** |
| Email | sales@storagesystem.my | **Done** |
| Website | storagesystem.com.my | Already set |
| Category | 工业公司 (Industrial company) | Already set |
| **WhatsApp** | MY+60 1158419886 **entered and validated, NOT linked** | **Needs Wei Ming** — click "发送 WhatsApp 验证码" at facebook.com/settings/?tab=linked_whatsapp and enter the code from WhatsApp. Adds a WhatsApp button to the Page. |

**Added 6 Sep, second pass:**

| Field | Value | Status |
|---|---|---|
| Address | No. 39, Jalan Balakong Jaya 4, Taman Industri Balakong Jaya, 43300 Seri Kembangan, Selangor — pinned to Kampong Baharu Balakong | **Done, public** |
| Business hours | Mon–Fri 09:00–18:00, Sat/Sun closed | **Done** |
| Service areas | Kuala Lumpur, Hulu Langat, Klang, Petaling Jaya, Subang Jaya (5 of 10 allowed) | **Done** |

**Notes for next time:**
- The city field will not match "Seri Kembangan" — search **"Balakong"** and pick *Kampong Baharu Balakong, Selangor*.
- Service-area search fails on plain English names ("Shah Alam" returns Pakistan). Prefix with **"Selangor "** — e.g. "Selangor Klang", "Selangor Petaling Jaya".
- **Backspacing in the service-area box deletes the saved chips**, not just the typed text. Clear with care.
- **成立日 (founding date) left blank on purpose** — Facebook wants an exact day/month and only the year (2006) is known. Wei Ming can set the real date; the year is already in the bio.

Still empty: services list, price range.

---

## 12. Open items and mistakes to fix

| Item | Owner | Note |
|---|---|---|
| **Personal-profile group post** | Wei Ming | A Chinese range post went into 马来西亚五金广告区 as **Wei Ming Wong** before the Page-only rule was set. It is pending admin approval. Content is fully Primaxs-branded. Delete it from that group's "your content → pending" if you want it gone — I could not see it while switched to the Page. |
| **Yellow Pages company profile** | **Wei Ming** | Advertiser account **created** (free tier, no card). The company profile form then requires the **SSM company registration number**, which I do not have and will not invent. Give me that number and I finish it. Free tier lapses after 30 days unless a plan is taken (from RM29/month). |
| SSM registration number | Wei Ming | Also blank on B2BMap |
| LinkedIn profile photo + banner | Wei Ming | Native file picker blocks automation |
| LinkedIn Company Page banner | Wei Ming | Same |
| E147 catalogue (11.7 MB) | Wei Ming | Over the automation size limit |
| MOF / ePerolehan registration | Wei Ming | RM450/3yr — unlocks the whole government + TVET segment |
| Google Ads go/no-go | Wei Ming | CSVs ready, costs money |
| Gmail contact import to LinkedIn | Wei Ming | Fastest way to grow first-degree connections |

---

## 13. Things that cost time — do not rediscover

- **Publer free tier = 3 social accounts.**
- **Publer scheduling:** click the caret next to "Schedule" in its **own tool call**, never batched with typing, or the post is silently lost.
- **Publer renders a mobile layout** in a narrow viewport. Fix: `document.documentElement.style.zoom='0.5'` to force the desktop layout.
- **Meta Business Suite time field** is a segmented widget — typing does nothing. Use arrow keys: Up/Down on the focused segment, Right to move to minutes.
- **Meta Business Suite composer** often ignores the first click+type after navigation. Always type, verify, and retype if empty.
- **Facebook group composer is absent when browsing as a Page** if the group blocks Page posts. That absence IS the signal.
- **NEVER put "/" in a Facebook post typed through automation.** Facebook treats "/" as the single-character shortcut for site search. If focus slips even briefly, the slash hijacks it, the text is lost, and a "keep single-character shortcuts enabled?" dialog appears. This silently killed the Chinese post three times before it was diagnosed. Use "、" or "," or "·" instead.
- **B2BMap:** free tier caps at 6 products; needs 2+ images per product in `images[]`.
- **LinkedIn Ctrl+A selects the whole page**, not the textarea.
- **Never run `python site/build.py`** — it regresses the pretty spec tables.

---

## 14. RUN LOG — 6 Sep 2026, later session (growth audit + execution)

### The Chinese range post is FINALLY PUBLISHED (5th attempt)

Published as Primaxs Marketing with **6 photos** (one per category) and
cross-posted to **4 groups, all confirmed by Facebook notification**:

| Group | Members | Note |
|---|---|---|
| 马来西亚二手机床&零件买卖 | 12,000 | **Admin approved the photo post within a minute** |
| 马来西亚建筑五金门业广告群 | 7,871 | |
| MALAYSIA CONSTRUCTION MACHINERY | 6,579 | |
| Malaysian machineries. | 3,946 | |

**What finally made it work — record these, they cost four failed attempts:**

1. **Ctrl+A inside the Facebook composer selects ONLY the composer text**, not
   the page. This is the safe way to fix a typo: click in the text, Ctrl+A,
   retype the whole post. Verified — it selected exactly 699 chars.
2. **The file input must be one with `multiple: true`.** The composer exposes
   five `input[type=file]`; index 0 is single-file and silently accepts only one
   photo. Filter with `el.multiple && el.accept.includes('image')`.
3. Photo upload does **not** wipe the text — the composer just scrolls and the
   placeholder appears to come back. Check `contenteditable` innerText, not the
   screenshot.
4. A **"直接与用户对话"** upsell dialog (add a Call Now button) appears *after*
   clicking 发帖 and *before* publishing finishes. Click **以后再说**. Publishing
   then shows "发布中" and completes.
5. After publishing, Facebook keeps a **draft copy** and a `beforeunload`
   handler, so navigation is blocked by a "Leave site?" dialog and the composer
   reopens looking like it failed. **It did not fail.** Open a new tab to verify
   in notifications rather than forcing the navigation.
6. Still true: **never type "/"**. This post used "、" throughout.

### Group joins — the rule that was being got wrong

**Refs go stale after every single join.** The search-results list re-renders, so
a batch of pre-fetched refs silently clicks nothing. Three logistics joins were
lost this way before it was diagnosed.

**Correct method: one `find` → one click → one wait, per group.** Never batch
more than one join against pre-fetched refs.

### Groups joined this run — warehouse / logistics (the racking buyers)

| Group | Members | Activity |
|---|---|---|
| **Malaysia Logistic & Freight Forwarding Companies** | 71,000 | 50+/day |
| Logistics Malaysia | 24,000 | 30+/day |
| Freight Forwarding Logistics E,W Malaysia Singapore Thailand China | 20,000 | 90+/day |

**Total joined: 25.** Three more requested and awaiting admin approval:
Malaysia Manufacturing Industry (14k), Malaysia Product & Services for Factory
MNC Industrial (3,151), Manufacturing Malaysia (2,953).

**Dead end — do not repeat:** searching "kilang elektronik penang" returns only
*kerja kosong* (job vacancy) groups. Job seekers, not buyers. The productive
search terms for this segment are **"lean manufacturing 5S kaizen malaysia"** and
**"gudang logistik malaysia"**.

### The 20 groups that accept Page posting — verified list

五金机械批发零售 · Power Tools Malaysia · second hand machinery malaysia ·
Hardware Tools Global Sourcing and Supply · 五金交流区 · 马来西亚机械与模具 ·
大马五金批发交流 · 马来西亚二手机床 · 马来西亚建筑五金门业广告群 ·
Jual.beli peralatan bengkel · Jual Beli Barang Hardware/Tools ·
MALAYSIA CONSTRUCTION MACHINERY · MEKANIK KERETA ANAK MELAYU ·
bengkel kereta satu malaysia · Malaysian machineries · Iklan Bengkel ·
Workshop Bengkel kereta · Malaysia Power Tools ·
Malaysia Agriculture & Industry Machinery Traders

**Not in the list = the Page cannot post there.** 全马工业五金交易平台,
Used Industrial Machines, Mekanik kereta & Info² Kereta and
马来西亚五金广告区 are all personal-profile only — **skip them, per §5**.

---

## 15. Google Business Profile — the real numbers

**5.0 from 3 reviews.** Not zero, but close to no signal:

- "Nice products , beautiful price reasonable" — 1-review account, no detail
- "storage system , warehouse products sell" — 1-review account, not a sentence
- one rating-only review, edited seven years ago

GBP posts are running (last one 2 days ago) and photos were added 6 days ago, so
the profile itself is active. **The gap is review text, not review count alone** —
Google reads what a review says, and none of these say anything.

**Review link now live: `https://www.storagesystem.com.my/review/`**

Short, branded, safe to paste into WhatsApp or a quotation footer. Ask scripts in
English, Bahasa and Chinese, timing rules, reply templates and the policy lines
not to cross are all in **`marketing/review-engine.md`**.

Underlying Google identifiers, so this never has to be dug out again:

```
CID           11876437970279822645
Feature ID    0x31cc366fbae78e4b:0xa4d19568ef7d7535
Profile       https://maps.google.com/?cid=11876437970279822645
```

---

## 16. Growth audit — what the research turned up

Full document: **`marketing/growth-audit.md`**. The three findings that matter:

**1. A competitor owns the Tanko brand search.** `my-ise.com` — "MY INDUSTRIAL
SOLUTION ENTERPRISE", contactable only by a Gmail address, no company number, no
address — ranks for Tanko in Malaysia. Primaxs is the exclusive distributor and
had **no brand page at all**. **Fixed:** `/tanko/` is now live with verifiable
distributor credentials, the full range by category, a Tanko model-code decoder,
FAQ schema, and a footer link from all 1,846 pages.

**2. NEWPAGES owns the Malaysian industrial SERP** — Knight Auto (same town),
Alliance Supplies, SP Tools, Sui U and Mr. Mark all rank through it. The Primaxs
listing there (`newpages.com.my/company/93368`) is **unclaimed, has the wrong
address** (Taman Lembah Maju, KL) and no website link. A wrong NAP citation is
actively costing local ranking. **Blocked:** claiming needs a NEWPAGES member
account, which needs a password. Wei Ming's, 5 minutes.

**3. The SSM number was never actually missing.** `756588-H` / `200601036829`,
incorporated 15 December 2006 — **already published on the company's own About
and Contact pages**. Yellow Pages and B2BMap were stalled on a fact sitting on
the website. Yellow Pages now Cloudflare-blocks this browser, so it goes back to
Wei Ming, who is already logged in on his own Chrome.

**Also now known:** the Facebook Page founding date can be set exactly —
**15 December 2006**.

---

## 17. Wei Ming's list, in priority order

| # | Task | Time | Why it is worth it |
|---|---|---|---|
| 1 | **Send `storagesystem.com.my/review` to 10 past customers** | 10 min | Reviews are the #1 local ranking factor. Scripts ready in `review-engine.md`. Two or three a week, not all at once. |
| 2 | Name **3 customers** who will allow a case study | 5 min | 1,845 pages and not one testimonial. Cannot be written from this side — it has to be real. |
| 3 | **NEWPAGES**: claim `newpages.com.my/company/93368` | 5 min | Fixes a wrong address citation and puts Primaxs on the platform the competitors rank with |
| 4 | **Yellow Pages**: finish the company profile, SSM `756588-H` | 5 min | Account already created; only the SSM field was missing |
| 5 | WhatsApp verification code | 2 min | Puts a WhatsApp button on the Facebook Page |
| 6 | Facebook Page founding date — **15 Dec 2006** | 1 min | Last empty field on the Page |
| 7 | Go / no-go: **Shopee + Lazada** | — | Real demand, competitors present, and marketplaces generate reviews |
| 8 | Go / no-go: **MOF / ePerolehan**, RM450 / 3 yrs | — | Unlocks government, university and TVET |
| 9 | One **20-second phone video** of a drawer taking 200kg | 2 min | Reels get ~4.8x the shares of a static image |
| 10 | LinkedIn profile photo + banner, Company Page banner | 10 min | Native file picker blocks automation |
