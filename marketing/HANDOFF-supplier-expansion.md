# Handoff brief — second-line supplier expansion

**Purpose:** give a fresh Claude (or a colleague) everything needed to continue
this work without the original conversation. Read this file first, then the
linked ones in the order given.

**Last updated:** 17 September 2026

---

## 1. Who and what

**Wong Wei Ming** — Business Development Manager at **Primaxs Marketing (M) Sdn
Bhd**, Seri Kembangan, Selangor, Malaysia. *(It is his uncle's company. He is not
the founder.)*

Primaxs has been the **exclusive Malaysia distributor for Tanko Enterprise Co.,
Ltd. of Taiwan since 2006** — industrial storage: workbenches, tool cabinets, CNC
tool storage, lockers, racking, perforated boards. 11 product categories, 1,517
products.

**The website, storagesystem.com.my, is the strategic asset.** 1,851 pages, ranks
first in Malaysia for CNC tool storage, Google Merchant Center feed, Google
Business Profile, full Bahasa Malaysia coverage. He built it. It is the main
argument in every supplier email.

**The goal of this workstream:** add a second supplier line — a Taiwanese
manufacturer without a Malaysian exclusive distributor who needs one.

---

## 2. Standing constraints — get these wrong and you cause real damage

- **Facebook: the Primaxs Marketing Page only. Never his personal profile.**
  LinkedIn posts *do* go from his personal profile.
- **74 SKUs are deliberately unpriced.** His words: *"unpriced for reason, i did
  not ask you to change, then dont change."*
- **The commercial offer belongs in every post:** free delivery Selangor/KL, free
  installation, outstation charged.
- **Every post must carry an image.** No text-only posts on any channel.
- **Every Facebook Page post cross-posts to the groups.**
- **Never quote rankings from his signed-in Chrome — use GSC.**
- He **cannot** solve CAPTCHAs, create accounts, or enter passwords.
- **NP Points are a stored balance** — spending them is a purchase and needs his
  authorisation.
- Site was frozen 16–23 Sep 2026 except when he asked.

---

## 3. The selection criteria, in the order they actually matter

This evolved over the work. The final framing is his, and it is the right one:

1. **Can he afford to stock it?** Capital per unit, stock turn, SKU matrix, floor
   space — benchmarked against the Tanko line. *A line you can stock is a line you
   can win exclusivity on. A line you cannot stock leaves you a trader forever.*
2. **Value per cubic metre.** Freight from Taiwan decides category viability.
   Bulky low-value goods do not survive the journey.
3. **Is the market open** — not merely whether the *brand* is unrepresented. These
   are different things and conflating them caused the biggest error in this work.
4. **Does it conflict with Tanko?** Check by grepping the live site, not by
   assuming.
5. **Do his existing assets transfer** — website authority, factory customers,
   installation crew, Taiwan→Port Klang import lane.

---

## 4. Where it landed

| Rank | Candidate | Status |
|---|---|---|
| **1** | **TAI SAM CORPORATION** — industrial cabinet hardware | **Email drafted, ready to send** |
| **2** | **CHUNG FU** — FM flammable liquid cabinets | **Email drafted, ready to send** |
| **3** | **YUNG CHIA** (chair.com.tw) — contract furniture | One email, low expectations, canteen range only |
| — | Castors (JEIN YI / HENG TA) | **Withdrawn.** Source locally instead |
| — | GISON / M7 air tools | Parked behind a repair-bench decision |
| — | GOOD HAND toggle clamps | Asia already covered |
| — | K-GUALDA CNC consumables | Good product, too narrow to be a line |

### The pattern worth remembering

**Everything that stocks like Tanko is a *component*. Everything with a fat margin
is *capital equipment* he cannot afford to hold.** The sensible structure is one
stocking line that turns (Tai Sam) plus one opportunistic margin line that does
not (Chung Fu). The stocking line pays the overhead; the capital line pays for the
year.

---

## 5. Read these, in this order

| File | What it holds |
|---|---|
| [taisam-email-2026-09.md](taisam-email-2026-09.md) | **#1 candidate. Email + verified contact** |
| [chungfu-approach-2026-09.md](chungfu-approach-2026-09.md) | **#2. Email + the zero-stock analysis** |
| [second-line-inventory-economics-2026-09.md](second-line-inventory-economics-2026-09.md) | The stocking-criteria ranking *(carries a correction banner)* |
| [castor-demand-malaysia-2026-09.md](castor-demand-malaysia-2026-09.md) | Why castors were withdrawn |
| [three-plans-compared-2026-09.md](three-plans-compared-2026-09.md) | Yung Chia vs castors vs Tai Sam |
| [yungchia-full-catalogue-2026-09.md](yungchia-full-catalogue-2026-09.md) | All 279 Yung Chia products |
| [second-line-cp-ranking-2026-09.md](second-line-cp-ranking-2026-09.md) | Earlier 性价比 scoring |
| [gison-m7-deep-dive-2026-09.md](gison-m7-deep-dive-2026-09.md) | Air tools + Tanko conflict method |
| [taiwan-supplier-catalogues-2026-09.md](taiwan-supplier-catalogues-2026-09.md) | Catalogues + export-market filter |
| [second-line-supplier-research-2026-09.md](second-line-supplier-research-2026-09.md) | Original demand research |

---

## 6. Research methods that worked — reuse them

- **Taiwantrade's "Main Export Market" field is the territory filter.** If Malaysia
  is absent, the brand may be available. **It does not mean the market is open** —
  check the Malaysian competitive field separately. This distinction is the single
  most important lesson here.
- **Conflict-check by grepping the live site**, not by assuming:
  `grep -ril "hinge" docs --include=index.html | wc -l`
- **JS-rendered catalogues:** fetching paginated HTML returns an empty template.
  Find the data endpoint in the network log instead. Yung Chia's whole catalogue
  came from `dist/includes/app.php?action=GetProductList&cate=0` in one call.
- **Taiwantrade blocks plain fetches (403).** Use a browser tool.
- **Freight:** Kaohsiung → Port Klang is 5–10 days direct. Production lead time,
  not shipping, dominates delivery on made-to-order goods.

---

## 7. Corrections made during this work — do not re-introduce them

These were all wrong at some point and were retracted:

- **"Contact Bright Jing Chin first"** — they are an Exporter only, with no brand
  to be exclusive for, covering all Asia.
- **"Malaysia is empty for GISON"** — Hup Sheng Hardware carries 127 GISON SKUs
  across 34 categories.
- **"Castors are the #1 opening"** — JEIN YI's *territory* being open is not the
  *market* being open. KSW has 12 branches since 1992; UKAI carries 9 imported
  brands since 1989. Germany and Japan hold the premium tier, China holds price.
  No slot for a Taiwanese mid-tier brand.
- **"Yung Chia is a school furniture company"** — education is 32 of 253 finished
  products, 13%. It is a contract furniture maker whose biggest specialism is
  fixed and public seating, and it has 23 office task chairs.

---

## 8. Open items

- **Send the Tai Sam email** — `sales@tai-sam.com.tw`, copy `info@yoeshin.com.tw`
- **Send the Chung Fu email** — *no verified address yet; their Taiwantrade record
  has an enquiry form only. Finding a direct address is an open task.*
- **Yung Chia** — one email; the deciding question is whether their Singapore
  office (opened 2019) already covers Malaysia
- **Confirm the Tanko agreement has no clause restricting other suppliers**
- **Decide the stock commitment** Wei Ming could realistically make — Tai Sam's
  question 3 invites it
- **Test locally before importing:** castors and factory canteen sets, both as
  attach sales to the existing installed base

### Unrelated site work still outstanding

- 4 pages need GSC indexing: `/perforated-board/hangers/`, `/workbench/wa-57a/`,
  `/workbench/wa-67a/`, `/perforated-board/kp-47/kp-4701/`
- ~100 thin category pages under 250 words
- Missing privacy / terms / shipping / warranty pages
- Add a skip-link; resolve the cannibalisation question
- Check the GBP primary phone matches schema `+60-3-4296-4737`
- Facebook Page CTA button

---

## 9. Standing caution on every figure here

Company facts, founding years, certifications and export-market lists come from
the companies' own records and are cited in each file. **Prices, MOQ, margins,
freight costs and market sizes are not verified anywhere in this work** — every
document says so in its own final section. Rankings and scores are judgement, not
measurement, and the underlying unit-cost figures are market ballpark rather than
Primaxs's landed cost. **Substitute real numbers and the conclusions may move.**
