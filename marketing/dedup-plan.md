# Thin/duplicate content diagnosis and unique-paragraph generator design

**Scope:** 1,589 SKU pages + 180 family pages + 10 category indexes across the ten product
directories in `docs/`. 1,846 URLs are submitted in `docs/sitemap.xml`; 1,228 sit in Search
Console as *Discovered — currently not indexed*.

**Status of this document:** analysis and design only. No file under `docs/` was modified.
All measurements below were produced by throwaway scripts in the session scratchpad
(`extract_text.py`, `analyze_dupes.py`, `analyze_sections.py`, `page_fields.py`,
`field_inventory.py`, `analyze_templates.py`, `consolidation.py`, `gen_prototype.py`).

**Method.** Every page's `<body>` was stripped of `script`/`style`/`svg`, tags removed,
entities unescaped, whitespace collapsed. Two text views are measured: **whole page**
(everything a crawler renders) and **main only** (`<main id="main-content">`, i.e. excluding
the mega-menu header and site footer). Similarity is reported two ways — **tf-cosine** on the
whole-page token multiset (this is the number that corresponds to the "99.1% similar" figure)
and **5-gram shingle Jaccard** on the main content (a stricter, phrase-order-sensitive measure).

---

## 1. The measurement

### 1.1 Headline: how much of a page is boilerplate

Every SKU page carries an identical 554-word chrome block. On the sample page
`/workbench/wa-57/wa-57f/` that is 417 words of mega-menu header (the 24 guide titles and
the location/industry lists are rendered **twice** — desktop nav and mobile nav — so
"How to Choose a Workbench" and "Kuala Lumpur" each appear 3× in the rendered text) plus a
91-word footer.

"Boilerplate share" below = the fraction of visible **word occurrences** on a page whose word
type also appears on ≥90% of its sibling pages in the same category.

| category | median visible words | chrome | main | boilerplate share (whole page) | boilerplate share (main only) |
|---|--:|--:|--:|--:|--:|
| workbench | 1178 | 554 | 624 | 95.8% | 90.9% |
| tool-cabinet | 1058 | 554 | 504 | 95.7% | 90.7% |
| perforated-board | 986 | 554 | 432 | 93.2% | 81.7% |
| workstation | 1031 | 554 | 477 | 95.9% | 90.3% |
| cnc-tool | 1006 | 554 | 452 | 96.9% | 93.1% |
| parts-cabinet | 934 | 554 | 380 | 96.3% | 88.1% |
| hanger-rack | 924 | 554 | 370 | 94.5% | 85.4% |
| documents-cabinet | 917 | 554 | 363 | 96.6% | 91.5% |
| locker | 966 | 554 | 412 | 96.6% | 92.0% |
| rack | 988 | 554 | 434 | 96.4% | 91.0% |

**Stripping the nav and footer does not rescue the page.** Even inside `<main>`, 81–93% of
words are shared with 90%+ of siblings. The duplication is in the body copy, not just the
chrome.

### 1.2 The real unique-token count per page

"Unique word types" = distinct word types on the page whose document frequency **within the
category** is exactly 1. This is the direct answer to *how many words does this page
contribute that no sibling does.*

| category | SKU pages | median unique word types | mean | pages with ZERO unique word types | median near-unique types (df ≤ 10% of siblings) |
|---|--:|--:|--:|--:|--:|
| workbench | 893 | **1** | 0.69 | **402** | 15 |
| tool-cabinet | 219 | **1** | 0.79 | 74 | 4 |
| perforated-board | 113 | **0** | 0.61 | 84 | 3 |
| workstation | 86 | **1** | 0.66 | 39 | 6 |
| cnc-tool | 90 | **0** | 0.42 | 55 | 2 |
| parts-cabinet | 71 | **1** | 0.69 | 29 | 6 |
| hanger-rack | 59 | **0** | 0.47 | 34 | 2 |
| documents-cabinet | 28 | **1** | 1.36 | 1 | 2 |
| locker | 20 | **1** | 1.50 | 2 | 2 |
| rack | 10 | **2** | 2.20 | 0 | 2 |

A typical Tanko SKU page contributes **zero to two word types** its siblings do not — and
inspection shows those types are almost always the digits of the reference price. Examples
pulled from the corpus:

```
workbench/wa-57/wa-56tg        unique = 0   []
workbench/wa-57/wa-56tg4a      unique = 1   ['3846']            <- price digits
tool-cabinet/ea-10/ea-10052    unique = 1   ['349']             <- price digits
perforated-board/kp-17/kp-17   unique = 3   ['kp-17','shelf','w900xd300']
```

The SKU code itself is usually *not* unique, because every sibling page lists it in its
"Related variants" block. There is no page in the corpus whose vocabulary meaningfully
differs from its neighbours'.

### 1.3 Similarity to the nearest sibling

| category | median cosine vs nearest sibling | median 5-gram Jaccard | pages with cosine > 0.99 |
|---|--:|--:|--:|
| **workbench** | **99.39%** | 84.83% | **892 of 893 (100%)** |
| documents-cabinet | 99.34% | 78.46% | 27 of 28 (96%) |
| cnc-tool | 99.33% | 79.96% | 90 of 90 (100%) |
| hanger-rack | 99.31% | 76.41% | 53 of 59 (90%) |
| parts-cabinet | 99.22% | 77.30% | 65 of 71 (92%) |
| workstation | 99.22% | 78.14% | 68 of 86 (79%) |
| perforated-board | 99.20% | 77.78% | 70 of 113 (62%) |
| rack | 99.18% | 76.35% | 10 of 10 (100%) |
| locker | 99.17% | 76.72% | 16 of 20 (80%) |
| tool-cabinet | 99.17% | 82.84% | 213 of 219 (97%) |

**1,504 of 1,589 SKU pages (94.7%) are >99% cosine-identical to at least one sibling.**
Workbench is the worst-offending category on every axis: largest (893 pages), highest
median cosine (99.39%), highest median shingle Jaccard (84.83%), most pages with zero unique
vocabulary (402).

Word-level diff on the single closest pair in each category:

| category | pair | words | identical words | words that differ |
|---|---|--:|--:|--:|
| workbench | `wkt-5102w1` vs `wkt-5102w1wpk-21` | 1231 | 1221 | **10 (0.81%)** |
| cnc-tool | `eb-7031-22mn` vs `eb-7031-33mn` | 1089 | 1079 | 10 (0.92%) |
| documents-cabinet | `a4a-345d` vs `a4m-345d` | 998 | 989 | 9 (0.90%) |
| locker | `fba-202aw` vs `fba-204aw` | 1026 | 1016 | 10 (0.97%) |
| perforated-board | `kp-7108` vs `kp-7203` | 1049 | 1033 | 16 (1.53%) |
| rack | `me-321` vs `me-322` | 1044 | 1027 | 17 (1.63%) |
| parts-cabinet | `tki-8302` vs `tki-8304` | 1034 | 1017 | 17 (1.64%) |
| hanger-rack | `km-2360` vs `km-2306` | 1009 | 992 | 17 (1.68%) |
| tool-cabinet | `ekc-110m` vs `ekc-210m` | 1128 | 1108 | 20 (1.77%) |
| workstation | `rc-6094-rpq-6063a-rph-61` vs `…-61wood` | 1155 | 1133 | 22 (1.90%) |

Between 9 and 22 words out of ~1,000 differ between the closest pairs. That is the mechanism
behind "Discovered — currently not indexed": Google has crawled enough of the pattern to
predict the rest and is declining to spend crawl budget confirming it.

### 1.4 Where the words go, and how many prose skeletons exist

Median words per section on a SKU page:

| section | cnc-tool | docs-cab | hanger | locker | parts | perf-board | rack | tool-cab | workbench | workstation |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| chrome (nav + footer + modals) | 554 | 554 | 554 | 554 | 554 | 554 | 554 | 554 | 554 | 554 |
| product-description ("About the …") | 155 | 86 | 84 | 133 | 82 | 82 | 133 | 155 | 171 | 148 |
| related (sibling variant list) | 134 | 127 | 132 | 133 | 134 | 155 | 125 | 134 | 149 | 131 |
| related-guides | 44 | 25 | 22 | 24 | 44 | 67 | 43 | 88 | 173 | 68 |
| serving-malaysia | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 40 |

Distinct text variants across all 1,589 SKU pages, per section:

| section | pages | distinct texts | largest single variant |
|---|--:|--:|--:|
| serving-malaysia | 1589 | **1** | 1589 pages |
| related-guides | 1589 | **10** | 893 pages |
| product-description | 1589 | 1589 | 1 |
| related (variant list) | 1589 | 1589 | 1 |
| spec/hero section | 1589 | 1589 | 1 |

The "serving Malaysia" block is byte-identical on all 1,589 pages. The "related guides"
block has only 10 distinct forms — one per category — so 893 workbench pages carry the same
173-word guide block verbatim.

The `product-description` paragraph *looks* unique (1,589 distinct strings) but is not.
Masking SKU codes, `WxDxH` dimensions and numbers collapses it:

| category | SKU pages | distinct raw paragraphs | **distinct prose skeletons** | biggest skeleton |
|---|--:|--:|--:|--:|
| workbench | 893 | 893 | 78 | 28 pages |
| tool-cabinet | 219 | 219 | **12** | **128 pages** |
| perforated-board | 113 | 113 | 70 | 18 pages |
| workstation | 86 | 86 | 36 | 15 pages |
| cnc-tool | 90 | 90 | **5** | 30 pages |
| parts-cabinet | 71 | 71 | 7 | 24 pages |
| hanger-rack | 59 | 59 | 10 | 18 pages |
| documents-cabinet | 28 | 28 | 11 | 8 pages |
| locker | 20 | 20 | **1** | **20 pages** |
| rack | 10 | 10 | 2 | 8 pages |

**1,589 description paragraphs are generated from 232 prose skeletons.** All 20 locker pages
share one. 128 tool-cabinet pages share one.

How much of each paragraph actually varies:

| category | median paragraph words | template slots filled | % variable | % fixed prose |
|---|--:|--:|--:|--:|
| workbench | 175 | 5 | 2.9% | **97.1%** |
| tool-cabinet | 161 | 6 | 3.7% | 96.3% |
| perforated-board | 82 | 3 | 3.7% | 96.3% |
| workstation | 153 | 4 | 2.6% | 97.4% |
| cnc-tool | 156 | 5 | 3.2% | 96.8% |
| parts-cabinet | 83 | 4 | 4.8% | 95.2% |
| hanger-rack | 88 | 6 | 6.8% | 93.2% |
| documents-cabinet | 88 | 5 | 5.7% | 94.3% |
| locker | 133 | 4 | 3.0% | 97.0% |
| rack | 135 | 6 | 4.4% | 95.6% |

**This is the defect.** The existing description generator is mad-libs: 96–97% fixed prose,
3–4% substituted slots.

### 1.5 Worst offenders — top 30 per category

Ranked by whole-page tf-cosine against the most similar sibling. `unique word types` is the
count from §1.2. Full tables: see the appendix at the end of this file.

---

## 2. What genuinely distinguishing data already exists

Harvested from the live pages' `<li><span class="k">…</span><span class="v">…</span></li>`
spec lists (excluding the four generic rows — Origin, Availability, Lead time, Warranty —
which are identical on every page), cross-checked against `products.json` (1,761 records,
covers 1,338 of the 1,589 SKU pages), `marketing/google-merchant-feed.tsv` (1,591 rows),
`tanko_catalog_extracted.csv` (334 rows, `load_capacity_hint` column), `families.json`
(147 families), `_cards_data.json` (117 family cards) and `categories.json`.

### 2.1 Field coverage — count of SKU pages carrying a non-empty value

See appendix table A2. Summary of the fields that matter:

| field | populated on | notes |
|---|--:|---|
| **Dimensions (WxDxH mm)** | **1,241 / 1,589 (78%)** | missing on 176 tool-cabinet, 60 cnc-tool, 40 parts-cabinet, 34 perf-board, 19 documents-cabinet pages |
| **Material / Top** | **1,187 / 1,589 (75%)** | absent for the whole cnc-tool category (0/90) |
| **Reference price (RM)** | **1,515 / 1,589 (95%)** | 1,242 distinct values — the single most differentiating field in the corpus |
| Panel set / Panel / Panel Set | 739 / 1,589 | workbench 672, hanger-rack 43, workstation 24 |
| Colour | 223 / 1,589 | perf-board 84, documents-cabinet 27, tool-cabinet 16, cnc-tool 15, hanger-rack 15, parts-cabinet 10, workbench 56 |
| Type | 199 / 1,589 | perf-board 33 (hook/hanger types), hanger-rack 36, workbench 96 |
| Drawers / Drawer / Drawer Qty | 216 / 1,589 | **see data defect D1 below** |
| Cabinet / Cabinet (slide system) | 275 / 1,589 | cnc-tool 60, parts-cabinet 55, tool-cabinet 160 |
| Tool Holders (BT/HSK/ISO) | 90 / 1,589 | the entire cnc-tool category, 5 distinct values |
| **Load capacity** | **228 / 1,589 (14.3%)** | **workbench 184/893, tool-cabinet 16/219, workstation 16/86, parts-cabinet 9/71, perf-board 2/113, locker 1/20, rack 1/10, cnc-tool 0/90, hanger-rack 0/59, documents-cabinet 0/28** |
| ≥2 product images | 283 / 1,589 (18%) | tool-cabinet 150, cnc-tool 75, workstation 29 |

Joining `tanko_catalog_extracted.csv`'s `load_capacity_hint` lifts load coverage from 228 to
**298 of 1,589 (18.8%)**. Observed values: workbench {100 kg ×134, 600 kg ×65, 2000 kg ×7,
50 kg ×1, 45 kg ×1}; tool-cabinet {400 kg ×21, 60 kg ×8, 45 kg ×5, 100 kg ×1, 600 kg ×1,
35 kg ×1}; workstation {100 kg ×6, 200 kg ×6, 45 kg ×4}; cnc-tool {400 kg ×15};
parts-cabinet {400 kg ×5, 1000 kg ×4, 210 kg ×1, 900 kg ×1, 50 kg ×1, 15 kg ×1, 10 kg ×1};
perf-board {5 kg ×4, 12 kg ×1, 10 kg ×1}; locker {30 kg ×1}; rack {1000 kg ×1}.

**Constraint restated:** load ratings may only be stated on the ~298 SKUs that carry one.
Steel gauge, coating thickness and weld spec do not exist anywhere in the repo and must not
appear in generated copy. Warranty language is fixed at *1-year against manufacturing
defects, administered from the Selangor office*.

### 2.2 How many facts each SKU actually has to work with

| category | 1 field | 2 fields | 3 fields | 4+ fields | median |
|---|--:|--:|--:|--:|--:|
| workbench | 4 | 96 | 490 | 303 | 3 |
| tool-cabinet | 6 | 171 | 17 | 25 | 2 |
| perforated-board | 0 | 34 | 53 | 26 | 3 |
| workstation | 0 | 7 | 54 | 25 | 3 |
| cnc-tool | 0 | 75 | 15 | 0 | 2 |
| parts-cabinet | 13 | 27 | 11 | 20 | 2 |
| hanger-rack | 0 | 0 | 0 | 59 | 4 |
| documents-cabinet | **19** | 8 | 0 | 1 | **1** |
| locker | 0 | 0 | 0 | 20 | 4 |
| rack | 0 | 0 | 0 | 10 | 4 |

Counting price + sibling-comparison as facts, the whole corpus distributes as:
4 SKUs have 2 facts, 77 have 3, 398 have 4, 650 have 5, 426 have 6, 34 have 7+.

### 2.3 Field distinctness — how much separation a field can actually buy

| category | distinct dims | distinct tops | distinct panel sets | distinct load ratings | distinct prices | SKUs with load |
|---|--:|--:|--:|--:|--:|--:|
| workbench | 35 | 19 | 18 | 4 | 591 | 184/893 |
| tool-cabinet | 15 | 3 | 0 | 5 | 176 | 16/219 |
| perforated-board | 22 | 7 | 0 | 2 | 11 | 2/113 |
| workstation | 27 | 4 | 6 | 3 | 78 | 16/86 |
| cnc-tool | 5 | 0 | 0 | 0 | 65 | 0/90 |
| parts-cabinet | 27 | 0 | 0 | 6 | 60 | 9/71 |
| hanger-rack | 10 | 1 | 18 | 0 | 39 | 0/59 |
| documents-cabinet | 8 | 1 | 0 | 0 | 27 | 0/28 |
| locker | 4 | 1 | 0 | 1 | 19 | 1/20 |
| rack | 6 | 1 | 0 | 1 | 9 | 1/10 |

**cnc-tool has 90 SKUs sharing 5 dimension values, no top material, no load rating, one
colour, 5 tool-holder values.** Its only real separator is price. This is the category where
generation cannot rescue the pages.

### 2.4 Data defects the generator must guard against

- **D1 — poisoned Drawers field.** `Drawers` on tool-cabinet pages holds the SKU numeral,
  not a count: `EA-10051` renders `Drawers: 10051`. 160 tool-cabinet pages are affected.
  A generator that reads this field will emit "10051 drawers". Must be validated (reject any
  value that is not 1–20) or the field dropped.
- **D2 — load capacity not inherited by accessory variants.** `EGM-1703M` carries
  `Load capacity: 60kg`; its own accessory variant `EGM-1703M-EGP-03M` does not. The parent's
  rating may be inherited only where the accessory does not change the load path — otherwise
  omit.
- **D3 — family name contains the SKU.** `documents-cabinet` H1s read
  *"Documents cabinet (Desktop) — 2 columns A4M-212 — White"*, so naive
  `"{sku} is part of the {family} range"` produces the SKU twice in one sentence.
- **D4 — dimension format inconsistency.** `W845xD510xH1441 mm` (space before mm) vs
  `W1500xD650xH786mm`. Parse with a tolerant regex; re-emit in one canonical form.
- **D5 — spec/live divergence.** `products.json` covers only 1,338 of 1,589 SKU pages and
  carries dimensions for only 1,000. The **pages** are richer than `products.json` for
  tool-cabinet (43 on-page dims vs 33 in `products.json`) and poorer elsewhere. The generator
  must read the union, page fields first, `products.json` second, `tanko_catalog_extracted.csv`
  third for load hints only.
- **D6 — warranty copy contradicts policy.** Live pages say *"Tanko manufacturer warranty ·
  local claim administration by Primaxs"* and the FAQ says *"covered under the Taiwan
  manufacturer's warranty"*. The merchant feed and `/returns/` say *1-year against
  manufacturing defects, administered from Selangor*. These must be reconciled to the
  `/returns/` wording in the same pass.

---

## 3. Generator design

### 3.1 Principle: facts select sentences, sentences are not filled

The current generator has one sentence sequence and swaps tokens into it. The replacement
inverts that: **each fact the SKU actually has licenses a sentence; a fact it lacks removes
the sentence entirely.** Two SKUs with different fact sets produce structurally different
paragraphs, not the same paragraph with different nouns. Two SKUs with the *same* fact set
are separated by computed comparative values, which differ because the SKUs' neighbours
differ.

The three anti-spin rules, in priority order:

1. **Never synonym-swap.** No thesaurus rotation over a fixed skeleton — that is exactly the
   pattern a spun-content classifier is trained on. Variation comes from *which* assertions
   appear and *what numbers they contain*.
2. **Every sentence must carry a number or a proper noun the reader could not have guessed.**
   A sentence with no SKU-specific payload is boilerplate and is dropped.
3. **Deterministic seeding.** All ordering and form selection is keyed on
   `sha256(sku + salt)`, so a re-run produces byte-identical output and the diff of a rebuild
   is empty unless underlying data changed.

### 3.2 The six sentence generators

**S1 — Dimension framing (licensed by: Dimensions).** Four *structurally different*
framings, chosen by `hash(sku,'dim') % 4` — not four phrasings of one sentence, four
different things to say about the same measurement:

- length-first: *"WA-57F gives you 1500 mm of working length on a 650 mm deep top, standing 786 mm high."*
- footprint-first: *"At W1500xD650xH786 mm the WA-57F takes 0.98 m² of floor."* (m² is computed)
- axis-first: *"The WA-57S3 measures 1500 mm across and 650 mm front-to-back, with the work surface set at 786 mm."*
- compact: *"Footprint on the WA-57F is 1500 × 650 mm, 786 mm to the top face."*

Fallback where Dimensions is absent (348 SKUs): identity sentence naming the range.

**S2 — Sibling comparison (licensed by: Dimensions + ≥1 dimensioned sibling in the family).**
Computed, never templated. Two branches:

- *same-height sibling exists*: compute the width delta and name the specific sibling —
  *"That is 300 mm wider than the WA-56TG at the same 786 mm height, so the two line up
  flush when benched together."* The delta and the sibling name differ per SKU.
- *no same-height sibling*: rank the SKU's width within the family's width set —
  *"Of the 4 widths built on the Heavy Duty Workbench frame it is the third, spanning
  1200–2100 mm across the range."*

This is the mechanism that separates SKUs whose own field values are identical: the WA-57F
and the WA-67F have the same top and panel set, but different neighbours and therefore
different comparison sentences.

**S3 — Top material → application fit (licensed by: Material / Top).** Not a marketing
adjective — the *use case Tanko itself specifies*, which is already printed verbatim in the
Step-1 block on every family page in `docs/` and is therefore repo-verifiable:

| top code | construction (from family page) | specified for (from family page) |
|---|---|---|
| N — rubber | high-density fibreboard with green rubber mat, PVC edge protection | machine maintenance, production lines, garages |
| F — laminate | plywood with grey laminate and PVC edges, for high-temperature environments | electronics, research labs, hospitals, metrology |
| S — stainless | 1.2 mm stainless sheet over high-density core | toolmakers, workshops, research labs |
| W — wood | finger-jointed rubber wood | toolmakers, equipment maintenance |
| TG/TH — Tanko top | multi-layer laminate, PVC on four edges | research labs, schools |

**S4 — Load rating (licensed by: Load capacity present — 298 SKUs only).** Where the SKU has
both a rating and a width, the sentence states the span the rating applies over:
*"Rated to 600 kg, it will carry a 600 kg assembly across the full 1800 mm span without a
mid-support."* Where a rating exists without dimensions, the bare rating. **On the other
1,291 SKUs this sentence does not exist.** No inferred, inherited or category-default rating.

**S5 — Configuration (licensed by: any of Panel set / Drawers / Cabinet / Tool Holders /
Bins / Lock / Storage unit / Colour / Type).** One clause per populated field, joined into a
single sentence. Sentence length therefore varies with how configured the SKU is, which is
itself a differentiator. Subject to D1 validation.

**S6 — Price positioning (licensed by: Reference price — 1,515 SKUs).** Computed delta
against the nearest-priced sibling in the same family, naming it:
*"Reference price is RM 2,494.35, RM 108.45 above the WA-57W in the same range."*
Price is the highest-cardinality field in the corpus (1,242 distinct values) and the delta
plus the named sibling makes this sentence near-unique by construction.

**Closers.** Two fixed obligations that must appear on every page — the standing commercial
offer (free delivery and installation in Selangor/KL, outstation charged) and the warranty
line — are rotated across 6 phrasings by `hash(sku,'close') % 6` so they are not one
identical sentence on 1,589 pages, and are always placed last so the differentiating content
occupies the snippet-eligible opening.

**Ordering.** S1 always opens (the identity + measurement the reader searched for). S2–S6 are
permuted by `hash(sku,'ord')`. Closers always last.

### 3.3 Length banding

Word budget is set by fact count, not padded to a target:

| facts available | target band | rationale |
|---|---|---|
| 6+ | 130–150 words | all six generators fire |
| 4–5 | 100–130 words | S4 or S5 absent |
| 3 | 80–100 words | dimension + comparison + price |
| ≤2 | **do not generate — consolidate** | see §4 |

### 3.4 Measured prototype result

A working prototype (`gen_prototype.py`) was run over all 1,589 SKUs using only the fields
inventoried in §2. Results:

| metric | current live pages | prototype output |
|---|--:|--:|
| distinct prose skeletons (SKU/number-masked) | **232** | **1,453** |
| largest single skeleton | 128 pages | 5 pages |
| median max 5-gram Jaccard vs nearest sibling | 76–85% | **51.0%** |
| paragraphs in the 80–150 word band | — | 924 / 1,589 |
| paragraphs under 80 words | — | **665** |

Per-category prototype Jaccard (5-gram, paragraph only):

| category | n | median max | p90 | worst | >0.50 | >0.65 |
|---|--:|--:|--:|--:|--:|--:|
| workbench | 893 | 52.5% | 63.6% | 96.2% | 573 | 70 |
| tool-cabinet | 219 | 50.5% | 60.0% | 68.8% | 114 | 4 |
| perforated-board | 113 | 57.3% | 90.9% | 91.5% | 95 | 32 |
| workstation | 86 | 40.3% | 48.3% | 61.5% | 6 | 0 |
| cnc-tool | 90 | 46.5% | 57.1% | 83.6% | 36 | 3 |
| parts-cabinet | 71 | 41.6% | 54.7% | 78.1% | 16 | 4 |
| hanger-rack | 59 | 43.0% | 55.0% | 79.1% | 9 | 2 |
| documents-cabinet | 28 | 47.4% | 50.5% | 53.8% | 3 | 0 |
| locker | 20 | 47.6% | 67.7% | 67.7% | 4 | 4 |
| rack | 10 | 31.9% | 37.8% | 37.8% | 0 | 0 |

**The honest conclusion from this run: generation alone is not sufficient.** 665 paragraphs
fall below 80 words because the SKU has nothing more to say, and 573 workbench paragraphs
still exceed 0.50 Jaccard against a sibling. Re-running the same generator over only the
post-consolidation page set (§4) improves it — median 48.4%, p90 61.5%, only 59 pages above
0.65 — but does not fix cnc-tool or perforated-board, which have no separating fields at all.
**Generation must be paired with consolidation, not used instead of it.**

Sample output, WA-57F (85 words, all facts from repo data):

> Footprint on the WA-57F is 1500 × 650 mm, 786 mm to the top face. Reference price is
> RM 2,494.35, RM 108.45 above the WA-57W in the same range. The top is a grey laminate face
> on plywood, which Tanko specifies for electronics assembly, research labs, hospitals and
> metrology rooms. Delivery and installation in Selangor and the Klang Valley are free;
> outstation freight is quoted separately. Covered by a 1-year warranty against manufacturing
> defects, administered from our Selangor office.

### 3.5 Non-paragraph work the same pass must do

Rewriting 150 words inside a 1,178-word page still leaves the page 87% boilerplate. Three
structural fixes carry more weight than the paragraph:

1. **Collapse the duplicated navigation.** The 24 guide titles, 6 locations and 6 industries
   are rendered twice per page (desktop nav + mobile nav). Rendering once and driving the
   mobile drawer from the same DOM removes ~250 of the 554 chrome words — a 21% cut in
   whole-page boilerplate on every page in the site.
2. **Make `related-guides` category-specific and short.** Workbench pages carry a 173-word,
   8-guide block identical across 893 pages. Cut to the 3 guides relevant to the SKU's top
   material and duty class.
3. **Cut or vary `serving-malaysia`.** 40 words, byte-identical on all 1,589 pages, zero
   informational value on a SKU page. Delete it from SKU pages; keep it on category and
   family pages.

Together these remove ~460 shared words per page; combined with a 120-word unique paragraph
the boilerplate share on a workbench SKU page falls from 95.8% to roughly 78% — still high,
but in the range where a distinctive paragraph is a meaningful fraction of the page.

---

## 4. Consolidation

Four rules were applied to the 1,589 SKU pages, in priority order, each SKU claimed once.

| rule | what it catches | groups | pages in | pages after | **removed** |
|---|---|--:|--:|--:|--:|
| **R1 colour-only** | identical spec dict except Colour; slug differs only by a colour token | 49 | 130 | 49 | **81** |
| **R2 accessory-bundle** | slug is `<base SKU>-<accessory SKU>` and the base page exists in the same family | 23 | 81 | 23 | **58** |
| **R3 panel-set ladder** | identical dims + top, differing only by panel set (`X`, `X2`, `X3`, `X4A`, `X5A`, `X6A`) | 136 | 659 | 136 | **523** |
| **R4 spec-identical** | identical non-generic spec dict — nothing on the page distinguishes them at all | 18 | 47 | 18 | **29** |
| **TOTAL** | | 226 | 917 | 226 | **691** |

**1,589 SKU pages → 898 after consolidation (691 removed, 43.5%).**

Per category:

| category | SKUs | R1 | R2 | R3 | R4 | removed | kept |
|---|--:|--:|--:|--:|--:|--:|--:|
| workbench | 893 | 27 | 0 | 492 | 2 | **521** | 372 |
| perforated-board | 113 | 47 | 0 | 0 | 0 | 47 | 66 |
| hanger-rack | 59 | 6 | 0 | 31 | 0 | 37 | 22 |
| parts-cabinet | 71 | 0 | 26 | 0 | 8 | 34 | 37 |
| workstation | 86 | 0 | 23 | 0 | 0 | 23 | 63 |
| tool-cabinet | 219 | 1 | 9 | 0 | 5 | 15 | 204 |
| documents-cabinet | 28 | 0 | 0 | 0 | 14 | 14 | 14 |
| cnc-tool | 90 | 0 | 0 | 0 | 0 | 0 | 90 |
| locker | 20 | 0 | 0 | 0 | 0 | 0 | 20 |
| rack | 10 | 0 | 0 | 0 | 0 | 0 | 10 |

### 4.1 Recommended tiers

**Tier 1 — do first, zero information loss (168 pages removed).** R1 + R2 + R4. These
variants are not separately searched for and carry no fact the parent page cannot state in a
table row.

- *R1 colour-only, 81 pages.* Biggest groups: `perforated-board/kq-3` (−36),
  `perforated-board/kpq-4301` (−10), `workbench/we` (−7), `workbench/we1200` (−7),
  `workbench/wet1200` (−7), `workbench/wet` (−6), `hanger-rack/db-3` (−4),
  `hanger-rack/da-3` (−2). Verified examples: `WE-58W-BLACK` / `WE-58W-WHITE` — identical
  dims, identical top, **identical price RM 1,217.05**, differing only in the word Black vs
  White. `KQ-308A-BLUE` / `KQ-308A-GRAY`. `DA-32-BLACK` / `DA-32-WHITE`.
  → One page per model with a colour selector; the colour becomes a `<select>` and a
  merchant-feed `item_group_id`, not a URL.
- *R2 accessory-bundle, 58 pages.* Biggest: `parts-cabinet/tki-2` (−16),
  `parts-cabinet/tki-1` (−10), `tool-cabinet/egl-1` (−4), `tool-cabinet/egm-1` (−4),
  `workstation/saa-331` (−4), `workstation/sab-331` (−4), `workstation/rc-6094` (−3),
  and 7 more workstation families at −2 each. Verified: `EGL-185M` /
  `EGL-185M-EGP-03L` (+ top chest, +RM 518.15) / `EGL-185M-EGQ-02A` (+ side panel,
  +RM 96.40) — same cabinet, same dims, different bundled accessory.
  → One page for the base cabinet with an "add-on" table listing each accessory SKU, its
  add-on price, and the resulting bundle SKU.
- *R4 spec-identical, 29 pages.* `documents-cabinet/a4l-330` (−5), `a4l-204` (−4),
  `a4l-104` (−2), and 12 further families at −1 or −2. **These are a data gap, not real
  duplicates.** `ELA-185M` and `ELA-187M` differ by drawer count (5 vs 7 per the model code)
  but the repo holds no drawer field for either — `products.json` has
  `attributes: {"Accessories": "None"}` for both. Since the differentiating fact cannot be
  honestly stated, the honest move is to consolidate rather than generate filler.
  → One page per spec signature listing every SKU in a table with its price.

**Tier 2 — recommended, larger judgement call (523 pages removed).** R3, the workbench and
hanger-rack panel-set ladders. Each base model appears six times: bare, `+2` perforated
board, `+3` board+shelf, `+4A` board+socket, `+5A` board+shelf+socket, `+6A`
board+shelf+socket+light. Dimensions and top are identical across all six; only the panel
set and the price change. Biggest groups: `workbench/wa-57` (−32), `wa-67` (−30),
`was-67053` (−30), `wat-6203` (−30), `was-54` (−24), `was-57042` (−24), `wat-5203` (−24),
plus 6 families at −20 and the rest smaller.

Nobody searches "WA-67TG5A". They search "1800mm heavy duty workbench with pegboard and
socket". One page per (family × top material × dimension) with a panel-set selector serves
that query better than six thin pages competing with each other, and it lets the paragraph
spend its 150 words on the top material and load rating instead of the accessory ladder.

**Not consolidated:** cnc-tool (90), locker (20), rack (10). No rule fires — their SKUs
genuinely differ (tool-holder taper, lock type, shelf count) even though the *pages* do not
say so distinctly. These need the data recovered from the Tanko catalogue PDFs, not merging.

### 4.2 SKUs too thin to say anything unique

42 SKUs have ≤1 distinguishing spec value and no load rating:

| category | count | examples |
|---|--:|---|
| documents-cabinet | 19 | A4A-106, A4M-106, A4A-115, A4M-115, A4A-206P, A4A-212, A4M-206P, A4LM-10203 |
| parts-cabinet | 13 | TA-115, TA-120, TA-154, TC-111, TC-112, TC-113, TKI-301, TKI-302 |
| tool-cabinet | 6 | EKC-110M, EKC-210M, EKC-220M, EKC-310M, EKC-320M, EKC-330M |
| workbench | 4 | WP511024, WP511025, WP511026, WP511028 |

**Honest fallback for these 42: do not generate.** In order of preference —

1. If an R1/R2/R4 sibling exists, consolidate into it (this already absorbs the 19
   documents-cabinet SKUs and 10 of the parts-cabinet SKUs).
2. Otherwise `<link rel="canonical">` the SKU page to its family page and drop it from
   `docs/sitemap.xml`, keeping the URL live so basket links and the merchant feed do not
   404. A page that cannot be made distinct should not be asking for an index slot.
3. Only recover the SKU as an indexable page once real data exists for it. The two Tanko
   catalogue PDFs in the repo root (`TANKO Catalogue NO.E147.pdf`,
   `TANKO_Catalogue_NO.E327.pdf`) are the source; the EKC-*M layer configuration
   (`Layer A, B: All (L)` vs `(M)+(L)`) is already in `products.json` and just is not being
   rendered — that is a rendering fix, not a data-collection problem.

### 4.3 Consolidation is not free — what else must change

- 691 URLs must 301 to their consolidated parent, with a `#variant=SKU` anchor so the
  selector opens on the right variant.
- `docs/sitemap.xml` drops from 1,846 to ~1,155 URLs.
- `marketing/google-merchant-feed.tsv` keeps all 1,591 SKU rows (Google wants the SKU) but
  `link` changes to the consolidated URL + anchor and `item_group_id` must be added.
- The basket / WhatsApp send-list stores SKU codes, so it is unaffected as long as the SKU
  stays addressable on the parent page.

---

## 5. Verification standard

A generator run may be committed only if **every** check below passes. These thresholds are
calibrated against the measured prototype (§3.4) run over the post-consolidation page set,
so they are known to be achievable.

**V1 — Factual containment (hard gate, zero tolerance).** Every number, unit, model code and
material word in generated copy must be traceable to a field in the source record. Implement
as: extract all `\d+`, all SKU-shaped tokens and all words from a controlled material
vocabulary from each generated paragraph; assert each appears in that SKU's source field set
or in the fixed commercial/warranty closers. **Any unmatched token fails the run.**
Additionally, assert the corpus-wide absence of the forbidden vocabulary:
`gauge`, `mm thick`, `powder coat` + thickness, `weld`, `EN `, `ISO 9001`, `SGS`,
`5-year`, `10-year`, `lifetime` — grep must return zero hits across `docs/`.

**V2 — Load-rating provenance.** The set of SKUs whose generated paragraph contains a `kg`
figure must be exactly the 298 SKUs with a load value in the merged source. Assert set
equality, both directions.

**V3 — Pairwise similarity of the generated paragraph.**
- median max 5-gram Jaccard against any sibling in the same category ≤ **0.50**
- p90 ≤ **0.62**
- **no more than 15 pages** site-wide above **0.70**
- **zero pages** above **0.80**

(Prototype achieved median 0.484 / p90 0.615 / 59 pages above 0.65 on the consolidated set;
tightening to these numbers requires the S2 comparison branch to fire more often, which
consolidation itself enables.)

**V4 — Whole-page similarity.** Re-run `analyze_dupes.py` on the rebuilt `docs/`. Required:
- median whole-page tf-cosine against nearest sibling ≤ **0.93** (currently 0.992)
- pages with cosine > 0.99: **0** (currently 1,504)
- pages with cosine > 0.97: ≤ **50**

**V5 — Skeleton diversity.** Masking SKU codes, dimensions and numbers, the number of
distinct prose skeletons across all SKU pages must be ≥ **0.90 × page count**, and the
largest single skeleton must cover ≤ **8 pages**. (Current: 232 skeletons for 1,589 pages,
largest covers 128.)

**V6 — Unique vocabulary floor.** Median unique word types per page (df = 1 within category)
≥ **12**, and **no page** may have fewer than **4**. (Current: median 1, with 720 pages at
zero.)

**V7 — Boilerplate ceiling.** Median whole-page boilerplate share (word occurrences whose
type appears on ≥90% of siblings) ≤ **80%**. (Current: 93–97%.) This check is what forces the
nav/guides/serving-Malaysia work in §3.5 to actually happen.

**V8 — Length band.** ≥ 95% of generated paragraphs between 80 and 150 words; none below 70;
none above 165. Any SKU that cannot reach 80 words must have been routed to consolidation or
canonicalisation instead — assert that the set of sub-80-word pages is empty.

**V9 — Determinism.** Run the generator twice into two scratch directories; `diff -r` must be
empty. This makes an accidental rebuild a no-op and protects the hand-maintained pretty spec
tables noted in the repo's branch model.

**V10 — Structural integrity.** Rebuild must not change page count except by the planned 691
consolidations; every removed URL must have a 301 rule; `docs/sitemap.xml` URL count must
equal the live indexable page count; every `link` in
`marketing/google-merchant-feed.tsv` must resolve to a 200.

**V11 — Human read of a stratified sample.** 30 paragraphs — 3 per category, drawn from the
richest, median and thinnest fact-count deciles — read end to end before commit. The test is
whether a buyer learns something from the paragraph that the spec table above it did not
already say. If not, the sentence generators are producing restatement, not content.

---

## Appendix

### A1 — Worst 30 offenders per category

Ranked by whole-page tf-cosine against the most similar sibling in the same category.
`unique word types` = distinct word types on the page with document frequency 1 within the
category.

#### workbench — top 30

| # | page | cosine vs nearest sibling | 5-gram Jaccard | unique word types | nearest sibling |
|--:|---|--:|--:|--:|---|
| 1 | `/workbench/wkt_5102/wkt-5102w1/` | 99.704% | 86.55% | 0 | `wkt-5102w1wpk-21` |
| 2 | `/workbench/wkt_5102/wkt-5102w1wpk-21/` | 99.704% | 86.55% | 0 | `wkt-5102w1` |
| 3 | `/workbench/wkt_5102/wkt-5102f1/` | 99.704% | 86.26% | 0 | `wkt-5102f1wpk-21` |
| 4 | `/workbench/wkt_5102/wkt-5102f1wpk-21/` | 99.704% | 86.26% | 0 | `wkt-5102f1` |
| 5 | `/workbench/wb67-ega/wb-67n2-ega-7041/` | 99.479% | 85.51% | 0 | `wb-67n3-ega-7041` |
| 6 | `/workbench/wb67-ega/wb-67n3-ega-7041/` | 99.479% | 85.51% | 0 | `wb-67n2-ega-7041` |
| 7 | `/workbench/wb67-ega/wb-67n4a-ega-7041/` | 99.478% | 85.48% | 1 | `wb-67n5a-ega-7041` |
| 8 | `/workbench/wb57-ega/wb-57n4a-ega-7041/` | 99.477% | 85.48% | 0 | `wb-57n5a-ega-7041` |
| 9 | `/workbench/wb57-ega/wb-57f4a-ega-7041/` | 99.477% | 85.48% | 1 | `wb-57f5a-ega-7041` |
| 10 | `/workbench/wb57-ega/wb-57f5a-ega-7041/` | 99.477% | 85.48% | 1 | `wb-57f4a-ega-7041` |
| 11 | `/workbench/wb57-ega/wb-57n5a-ega-7041/` | 99.477% | 85.48% | 1 | `wb-57n4a-ega-7041` |
| 12 | `/workbench/wb67-ega/wb-67f2-ega-7041/` | 99.475% | 85.44% | 0 | `wb-67f3-ega-7041` |
| 13 | `/workbench/wb67-ega/wb-67f3-ega-7041/` | 99.475% | 85.44% | 0 | `wb-67f2-ega-7041` |
| 14 | `/workbench/wb67-ega/wb-67f4a-ega-7041/` | 99.475% | 85.42% | 1 | `wb-67f5a-ega-7041` |
| 15 | `/workbench/wb67-ega/wb-67f5a-ega-7041/` | 99.475% | 85.42% | 1 | `wb-67f4a-ega-7041` |
| 16 | `/workbench/wb67-ega/wb-67n5a-ega-7041/` | 99.468% | 85.53% | 0 | `wb-67n6a-ega-7041` |
| 17 | `/workbench/wb57-ega/wb-57f6a-ega-7041/` | 99.467% | 85.26% | 0 | `wb-57f5a-ega-7041` |
| 18 | `/workbench/wb57-ega/wb-57n6a-ega-7041/` | 99.467% | 85.26% | 0 | `wb-57n5a-ega-7041` |
| 19 | `/workbench/wb57-ega/wb-57f2-ega-7041/` | 99.467% | 85.23% | 0 | `wb-57f3-ega-7041` |
| 20 | `/workbench/wb57-ega/wb-57f3-ega-7041/` | 99.467% | 85.23% | 0 | `wb-57f2-ega-7041` |
| 21 | `/workbench/wb67-ega/wb-67f6a-ega-7041/` | 99.465% | 85.19% | 0 | `wb-67f5a-ega-7041` |
| 22 | `/workbench/wb57-ega/wb-57n3-ega-7041/` | 99.462% | 85.09% | 0 | `wb-57n4a-ega-7041` |
| 23 | `/workbench/we/we-58w7-white/` | 99.460% | 85.07% | 0 | `we-58w8-white` |
| 24 | `/workbench/we/we-58w8-black/` | 99.458% | 85.91% | 0 | `we-58w9-black` |
| 25 | `/workbench/we/we-58w9-black/` | 99.458% | 85.91% | 0 | `we-58w8-black` |
| 26 | `/workbench/wet/wet-5102w8-black/` | 99.458% | 86.47% | 0 | `wet-5102w9-black` |
| 27 | `/workbench/wet/wet-5102w9-black/` | 99.458% | 86.47% | 0 | `wet-5102w8-black` |
| 28 | `/workbench/wb57-ega/wb-57n2-ega-7041/` | 99.456% | 84.96% | 0 | `wb-57n3-ega-7041` |
| 29 | `/workbench/was-77042/was-77042n5a/` | 99.455% | 86.41% | 0 | `was-77042n6a` |
| 30 | `/workbench/was-77042/was-77042n4a/` | 99.454% | 86.11% | 0 | `was-77042n5a` |

#### tool-cabinet — top 30

| # | page | cosine vs nearest sibling | 5-gram Jaccard | unique word types | nearest sibling |
|--:|---|--:|--:|--:|---|
| 1 | `/tool-cabinet/ekc/ekc-110m/` | 99.948% | 79.22% | 1 | `ekc-210m` |
| 2 | `/tool-cabinet/ekb-3m/ekb-3am/` | 99.795% | 77.29% | 0 | `ekb-3am-gray` |
| 3 | `/tool-cabinet/egl-1/egl-185m/` | 99.737% | 82.13% | 0 | `egl-185m-egp-03l` |
| 4 | `/tool-cabinet/egl-1/egl-185m-egp-03l/` | 99.737% | 82.13% | 0 | `egl-185m` |
| 5 | `/tool-cabinet/egl-1/egl-187m/` | 99.724% | 81.80% | 0 | `egl-187m-egp-03l` |
| 6 | `/tool-cabinet/egl-1/egl-187m-egp-03l/` | 99.724% | 81.80% | 0 | `egl-187m` |
| 7 | `/tool-cabinet/eka-3m/eka-3m/` | 99.721% | 80.23% | 0 | `eka-3m-eka-p03` |
| 8 | `/tool-cabinet/eka-3m/eka-3m-eka-p03/` | 99.721% | 80.23% | 1 | `eka-3m` |
| 9 | `/tool-cabinet/ekb-3m/ekb-308am/` | 99.621% | 78.65% | 0 | `ekb-308m` |
| 10 | `/tool-cabinet/ekb-3m/ekb-308m/` | 99.621% | 78.65% | 0 | `ekb-308am` |
| 11 | `/tool-cabinet/ekb-3m/ekb-316m/` | 99.613% | 77.56% | 2 | `ekb-308m` |
| 12 | `/tool-cabinet/egl-1/egl-185m-egq-02a/` | 99.510% | 81.07% | 0 | `egl-185m-egp-03l` |
| 13 | `/tool-cabinet/egl-1/egl-185ma/` | 99.421% | 80.14% | 1 | `egl-187m` |
| 14 | `/tool-cabinet/ea-10/ea-10072/` | 99.370% | 83.86% | 0 | `ea-10073` |
| 15 | `/tool-cabinet/ea-10/ea-10073/` | 99.370% | 83.86% | 0 | `ea-10072` |
| 16 | `/tool-cabinet/egm-1/egm-1705m-egp-03m/` | 99.367% | 82.39% | 0 | `egm-1703m-egp-03m` |
| 17 | `/tool-cabinet/egm-1/egm-1703m-egp-03m/` | 99.367% | 82.39% | 1 | `egm-1705m-egp-03m` |
| 18 | `/tool-cabinet/egm-1/egm-1703m/` | 99.360% | 81.95% | 0 | `egm-1705m` |
| 19 | `/tool-cabinet/egm-1/egm-1705m/` | 99.360% | 81.95% | 0 | `egm-1703m` |
| 20 | `/tool-cabinet/els-2/els-274ma/` | 99.356% | 82.12% | 0 | `els-276ma` |
| 21 | `/tool-cabinet/els-2/els-276ma/` | 99.356% | 82.12% | 0 | `els-274ma` |
| 22 | `/tool-cabinet/egm-1/egm-1703m-egq-02a/` | 99.354% | 81.39% | 0 | `egm-1705m-egq-02a` |
| 23 | `/tool-cabinet/egm-1/egm-1705m-egq-02a/` | 99.354% | 81.39% | 0 | `egm-1703m-egq-02a` |
| 24 | `/tool-cabinet/egm-1/egm-1703ma/` | 99.353% | 81.98% | 0 | `egm-1705ma` |
| 25 | `/tool-cabinet/egm-1/egm-1705ma/` | 99.353% | 81.98% | 0 | `egm-1703ma` |
| 26 | `/tool-cabinet/ega-1/ega-10061/` | 99.349% | 81.20% | 0 | `ega-10091` |
| 27 | `/tool-cabinet/ega-1/ega-10091/` | 99.349% | 81.20% | 0 | `ega-10061` |
| 28 | `/tool-cabinet/ea-7m/ea-7053ma/` | 99.346% | 81.41% | 0 | `ea-7054ma` |
| 29 | `/tool-cabinet/ea-7m/ea-7052m/` | 99.346% | 81.38% | 0 | `ea-7052ma` |
| 30 | `/tool-cabinet/ea-7m/ea-7052ma/` | 99.346% | 81.38% | 0 | `ea-7052m` |

#### perforated-board — top 30

| # | page | cosine vs nearest sibling | 5-gram Jaccard | unique word types | nearest sibling |
|--:|---|--:|--:|--:|---|
| 1 | `/perforated-board/kp-7/kp-7108/` | 99.968% | 75.05% | 0 | `kp-7203` |
| 2 | `/perforated-board/kp-6/kp-6208/` | 99.573% | 79.31% | 0 | `kp-6308` |
| 3 | `/perforated-board/kp-6/kp-6308/` | 99.573% | 79.31% | 0 | `kp-6208` |
| 4 | `/perforated-board/kp-6/kp-6104/` | 99.556% | 78.90% | 1 | `kp-6208` |
| 5 | `/perforated-board/kp-6/kp-6103/` | 99.541% | 78.49% | 1 | `kp-6104` |
| 6 | `/perforated-board/kp-6/kp-6101/` | 99.541% | 77.68% | 1 | `kp-6103` |
| 7 | `/perforated-board/kp-6/kpq-b/` | 99.540% | 79.31% | 1 | `kp-6308` |
| 8 | `/perforated-board/kq-3/kq-308a-blue/` | 99.529% | 76.34% | 0 | `kq-308a-gray` |
| 9 | `/perforated-board/kq-3/kq-308a-black/` | 99.529% | 75.61% | 0 | `kq-308a-white` |
| 10 | `/perforated-board/kq-3/kq-306a-blue/` | 99.525% | 75.99% | 0 | `kq-306a-gray` |
| 11 | `/perforated-board/kq-3/kq-306a-black/` | 99.525% | 74.90% | 0 | `kq-306a-gray` |
| 12 | `/perforated-board/kq-3/kq-308a-gray/` | 99.444% | 77.64% | 0 | `kq-308a-red` |
| 13 | `/perforated-board/kq-3/kq-308a-red/` | 99.444% | 77.64% | 0 | `kq-308a-gray` |
| 14 | `/perforated-board/kq-3/kq-308a-white/` | 99.444% | 77.64% | 0 | `kq-308a-red` |
| 15 | `/perforated-board/kq-3/kq-306a-gray/` | 99.439% | 77.31% | 0 | `kq-306a-red` |
| 16 | `/perforated-board/kq-3/kq-306a-red/` | 99.439% | 77.31% | 0 | `kq-306a-gray` |
| 17 | `/perforated-board/kq-3/kq-306a-white/` | 99.439% | 77.31% | 0 | `kq-306a-red` |
| 18 | `/perforated-board/kpq-4301/kpq-4302-blackanti-static/` | 99.435% | 81.74% | 0 | `kpq-4304-blackanti-static` |
| 19 | `/perforated-board/kpq-4301/kpq-4304-blackanti-static/` | 99.435% | 81.74% | 0 | `kpq-4302-blackanti-static` |
| 20 | `/perforated-board/kpq-4301/kpq-4302-red/` | 99.428% | 81.55% | 0 | `kpq-4304-red` |
| 21 | `/perforated-board/kpq-4301/kpq-4301-red/` | 99.427% | 81.55% | 0 | `kpq-4304-red` |
| 22 | `/perforated-board/kpq-4301/kpq-4303-red/` | 99.427% | 81.55% | 0 | `kpq-4304-red` |
| 23 | `/perforated-board/kpq-4301/kpq-4302-yellow/` | 99.389% | 80.98% | 0 | `kpq-4304-yellow` |
| 24 | `/perforated-board/kp-3/kp-3108/` | 99.389% | 80.28% | 0 | `kp-3112` |
| 25 | `/perforated-board/kp-3/kp-3112/` | 99.389% | 80.28% | 0 | `kp-3108` |
| 26 | `/perforated-board/kp-3/kp-3116/` | 99.389% | 80.28% | 0 | `kp-3112` |
| 27 | `/perforated-board/kp-3/kp-3130/` | 99.389% | 80.28% | 0 | `kp-3116` |
| 28 | `/perforated-board/kp-3/kp-3208/` | 99.389% | 80.28% | 0 | `kp-3212` |
| 29 | `/perforated-board/kp-3/kp-3212/` | 99.389% | 80.28% | 0 | `kp-3208` |
| 30 | `/perforated-board/kp-3/kp-3216/` | 99.389% | 80.28% | 0 | `kp-3212` |

#### workstation — top 30

| # | page | cosine vs nearest sibling | 5-gram Jaccard | unique word types | nearest sibling |
|--:|---|--:|--:|--:|---|
| 1 | `/workstation/rc-6094/rc-6094-rpq-6063a-rph-61/` | 99.666% | 78.54% | 0 | `rc-6094-rpq-6063a-rph-61wood` |
| 2 | `/workstation/rc-6094/rc-6094-rpq-6063a-rph-61wood/` | 99.666% | 78.54% | 0 | `rc-6094-rpq-6063a-rph-61` |
| 3 | `/workstation/rb-6098/rb-6098/` | 99.659% | 78.01% | 1 | `rb-6098-rpq-6103a` |
| 4 | `/workstation/ra-6091/ra-6091-rpq-6103a/` | 99.658% | 78.01% | 0 | `ra-6091` |
| 5 | `/workstation/ra-6091/ra-6091/` | 99.658% | 78.01% | 1 | `ra-6091-rpq-6103a` |
| 6 | `/workstation/ra-9091/ra-9091/` | 99.658% | 78.01% | 1 | `ra-9091-rpq-9103a` |
| 7 | `/workstation/ra-9091/ra-9091-rpq-9103a/` | 99.658% | 78.01% | 1 | `ra-9091` |
| 8 | `/workstation/rg-6091/rg-6091-rpq-6103a/` | 99.657% | 78.12% | 0 | `rg-6091` |
| 9 | `/workstation/rg-6091/rg-6091/` | 99.657% | 78.12% | 1 | `rg-6091-rpq-6103a` |
| 10 | `/workstation/rc-6094/rc-6094/` | 99.646% | 77.71% | 0 | `rc-6094-rpq-6103a` |
| 11 | `/workstation/saa-331/saa-331m/` | 99.612% | 81.46% | 1 | `saa-331mspw-3` |
| 12 | `/workstation/saa-331/saa-331mspw-3/` | 99.612% | 81.46% | 1 | `saa-331m` |
| 13 | `/workstation/saa-331/saa-331spw-3/` | 99.605% | 81.84% | 0 | `saa-331spw-3-spq-32a` |
| 14 | `/workstation/saa-331/saa-331spw-3-spq-32a/` | 99.605% | 81.84% | 0 | `saa-331spw-3` |
| 15 | `/workstation/sab-331/sab-331spw-3/` | 99.603% | 81.59% | 0 | `sab-331spw-3-spq-32a` |
| 16 | `/workstation/sab-331/sab-331spw-3-spq-32a/` | 99.603% | 81.59% | 1 | `sab-331spw-3` |
| 17 | `/workstation/saa-331/saa-331spw-3s/` | 99.594% | 81.53% | 1 | `saa-331spw-3s-spq-32a` |
| 18 | `/workstation/sab-331/sab-331spw-3s/` | 99.591% | 81.29% | 0 | `sab-331spw-3s-spq-32a` |
| 19 | `/workstation/sab-331/sab-331spw-3s-spq-32a/` | 99.591% | 81.29% | 0 | `sab-331spw-3s` |
| 20 | `/workstation/rd-6091/rd-6091/` | 99.404% | 75.52% | 1 | `rd-6091-rpq-6102` |
| 21 | `/workstation/ra-9201/ra-9201/` | 99.403% | 74.90% | 1 | `ra-9201-rpb-91` |
| 22 | `/workstation/saa-331/saa-331spw-3s-spq-33a/` | 99.317% | 81.67% | 0 | `saa-331spw-3s-spq-32a` |
| 23 | `/workstation/saa-331/saa-331spw-3s-spq-32a/` | 99.317% | 81.67% | 1 | `saa-331spw-3s-spq-33a` |
| 24 | `/workstation/sab-331/sab-331spw-3s-spq-33a/` | 99.299% | 81.09% | 0 | `sab-331spw-3s-spq-32a` |
| 25 | `/workstation/sab-331/sab-331spw-3-spq-33a/` | 99.296% | 81.05% | 0 | `sab-331spw-3-spq-32a` |
| 26 | `/workstation/saa-331/saa-331spw-3-spq-33a/` | 99.286% | 80.96% | 1 | `saa-331spw-3-spq-32a` |
| 27 | `/workstation/saa-331/saa-331mspw-3s/` | 99.266% | 80.11% | 1 | `saa-331spw-3s` |
| 28 | `/workstation/ra-9201/ra-9201-rpb-91/` | 99.254% | 80.04% | 0 | `ra-9201-rpb-92` |
| 29 | `/workstation/ra-9201/ra-9201-rpb-92/` | 99.254% | 80.04% | 2 | `ra-9201-rpb-91` |
| 30 | `/workstation/sa/saa-361m/` | 99.243% | 79.30% | 1 | `saa-361` |

#### cnc-tool — top 30

| # | page | cosine vs nearest sibling | 5-gram Jaccard | unique word types | nearest sibling |
|--:|---|--:|--:|--:|---|
| 1 | `/cnc-tool/ea-7mn/eb-7031-22mn/` | 99.361% | 81.86% | 0 | `eb-7031-33mn` |
| 2 | `/cnc-tool/ea-7mn/eb-7031-33mn/` | 99.361% | 81.86% | 0 | `eb-7031-22mn` |
| 3 | `/cnc-tool/ea-10mn/eb-10032-666mn/` | 99.361% | 81.86% | 0 | `eb-10032-888mn` |
| 4 | `/cnc-tool/ea-10mn/eb-10032-888mn/` | 99.361% | 81.86% | 0 | `eb-10032-666mn` |
| 5 | `/cnc-tool/ea-10mn/ea-10032-333mn/` | 99.361% | 81.48% | 0 | `ea-10032-888mn` |
| 6 | `/cnc-tool/ea-10mn/ea-10032-888mn/` | 99.361% | 81.48% | 0 | `ea-10032-333mn` |
| 7 | `/cnc-tool/ea-10mn/eb-10031-111mn/` | 99.361% | 81.48% | 0 | `eb-10032-333mn` |
| 8 | `/cnc-tool/ea-10mn/eb-10032-333mn/` | 99.361% | 81.48% | 0 | `eb-10031-111mn` |
| 9 | `/cnc-tool/san-33/san-332/` | 99.359% | 80.83% | 0 | `san-338` |
| 10 | `/cnc-tool/san-33/san-338/` | 99.359% | 80.83% | 0 | `san-332` |
| 11 | `/cnc-tool/san-36k/san-362k/` | 99.359% | 80.83% | 0 | `san-363k` |
| 12 | `/cnc-tool/san-36k/san-363k/` | 99.359% | 80.83% | 0 | `san-362k` |
| 13 | `/cnc-tool/san-36/san-362/` | 99.359% | 80.83% | 0 | `san-363` |
| 14 | `/cnc-tool/san-36/san-363/` | 99.359% | 80.83% | 0 | `san-362` |
| 15 | `/cnc-tool/ea-10n/eb-10032-33n/` | 99.357% | 81.82% | 0 | `eb-10032-66n` |
| 16 | `/cnc-tool/ea-10n/eb-10032-66n/` | 99.357% | 81.82% | 0 | `eb-10032-33n` |
| 17 | `/cnc-tool/ea-10n/eb-10031-11n/` | 99.357% | 80.70% | 0 | `eb-10032-88n` |
| 18 | `/cnc-tool/ea-10n/eb-10032-88n/` | 99.357% | 80.70% | 0 | `eb-10031-11n` |
| 19 | `/cnc-tool/ea-12n/ed-12031-111n/` | 99.357% | 82.16% | 0 | `ed-12031-333n` |
| 20 | `/cnc-tool/ea-12n/ea-12031-333n/` | 99.357% | 81.78% | 0 | `ea-12041-666n` |
| 21 | `/cnc-tool/ea-12n/ea-12041-666n/` | 99.357% | 81.78% | 0 | `ea-12031-333n` |
| 22 | `/cnc-tool/ea-12n/ea-12031-111n/` | 99.357% | 81.40% | 0 | `ea-12031-333n` |
| 23 | `/cnc-tool/ea-12n/eb-12031-111n/` | 99.357% | 81.40% | 0 | `eb-12041-666n` |
| 24 | `/cnc-tool/ea-12n/eb-12041-666n/` | 99.357% | 81.40% | 0 | `eb-12031-111n` |
| 25 | `/cnc-tool/ea-10mn/ea-10031-111mn/` | 99.336% | 79.63% | 0 | `ea-10031-222mn` |
| 26 | `/cnc-tool/ea-10mn/ea-10031-222mn/` | 99.336% | 79.63% | 0 | `ea-10031-111mn` |
| 27 | `/cnc-tool/ea-7mn/ea-7031-22mn/` | 99.336% | 79.63% | 0 | `ea-7031-33mn` |
| 28 | `/cnc-tool/ea-7mn/ea-7031-33mn/` | 99.336% | 79.63% | 1 | `ea-7031-22mn` |
| 29 | `/cnc-tool/ea-7mn/eb-7021-11mn/` | 99.335% | 79.63% | 0 | `eb-7031-22mn` |
| 30 | `/cnc-tool/ea-7mn/eb-7032-66mn/` | 99.335% | 79.63% | 0 | `eb-7031-33mn` |

#### parts-cabinet — top 30

| # | page | cosine vs nearest sibling | 5-gram Jaccard | unique word types | nearest sibling |
|--:|---|--:|--:|--:|---|
| 1 | `/parts-cabinet/tki-83/tki-8302/` | 99.853% | 77.88% | 0 | `tki-8304` |
| 2 | `/parts-cabinet/tki-83/tki-8304/` | 99.853% | 77.88% | 0 | `tki-8302` |
| 3 | `/parts-cabinet/tki-83/tki-8301/` | 99.738% | 79.05% | 0 | `tki-8303` |
| 4 | `/parts-cabinet/tki-83/tki-8303/` | 99.738% | 79.05% | 0 | `tki-8301` |
| 5 | `/parts-cabinet/ta-1/ta-115/` | 99.591% | 81.42% | 0 | `ta-120` |
| 6 | `/parts-cabinet/ta-1/ta-120/` | 99.591% | 81.42% | 0 | `ta-115` |
| 7 | `/parts-cabinet/ta-1/ta-112/` | 99.574% | 78.52% | 1 | `ta-155` |
| 8 | `/parts-cabinet/ta-1/ta-155/` | 99.574% | 78.52% | 1 | `ta-112` |
| 9 | `/parts-cabinet/ta-1/ta-154/` | 99.558% | 78.80% | 1 | `ta-120` |
| 10 | `/parts-cabinet/tki-83/tki-8305/` | 99.492% | 77.41% | 1 | `tki-8301` |
| 11 | `/parts-cabinet/tki-2/tki-2515-1/` | 99.389% | 80.15% | 0 | `tki-2515-3` |
| 12 | `/parts-cabinet/tki-2/tki-2515-3/` | 99.389% | 80.15% | 0 | `tki-2515-1` |
| 13 | `/parts-cabinet/tki-2/tki-2405-1/` | 99.389% | 80.10% | 0 | `tki-2405-3` |
| 14 | `/parts-cabinet/tki-2/tki-2405-3/` | 99.389% | 80.10% | 0 | `tki-2405-1` |
| 15 | `/parts-cabinet/tki-2/tki-2410-1/` | 99.389% | 80.10% | 0 | `tki-2410-3` |
| 16 | `/parts-cabinet/tki-2/tki-2410-3/` | 99.389% | 80.10% | 0 | `tki-2410-1` |
| 17 | `/parts-cabinet/tc-11/tc-112/` | 99.383% | 80.65% | 1 | `tc-113` |
| 18 | `/parts-cabinet/tc-11/tc-113/` | 99.383% | 80.65% | 1 | `tc-112` |
| 19 | `/parts-cabinet/tc-11/tc-111/` | 99.383% | 80.20% | 1 | `tc-112` |
| 20 | `/parts-cabinet/tki-30/tki-302/` | 99.376% | 80.60% | 0 | `tki-304` |
| 21 | `/parts-cabinet/tki-30/tki-304/` | 99.376% | 80.60% | 1 | `tki-302` |
| 22 | `/parts-cabinet/tki-30/tki-301/` | 99.376% | 80.15% | 1 | `tki-302` |
| 23 | `/parts-cabinet/tki-1/tki-1412d-3/` | 99.351% | 77.70% | 0 | `tki-1412d-3m` |
| 24 | `/parts-cabinet/tki-1/tki-1412d-3m/` | 99.351% | 77.70% | 1 | `tki-1412d-3` |
| 25 | `/parts-cabinet/tki-1/tki-1412-3/` | 99.350% | 77.59% | 1 | `tki-1412-3m` |
| 26 | `/parts-cabinet/tki-1/tki-1412-3m/` | 99.350% | 77.59% | 1 | `tki-1412-3` |
| 27 | `/parts-cabinet/tki-1/tki-1412d-2/` | 99.343% | 76.64% | 1 | `tki-1412d-3` |
| 28 | `/parts-cabinet/tki-1/tki-1412-2/` | 99.341% | 76.11% | 0 | `tki-1412-3` |
| 29 | `/parts-cabinet/tki-1/tki-1308-2/` | 99.341% | 77.30% | 0 | `tki-1308-3` |
| 30 | `/parts-cabinet/tki-1/tki-1308-3/` | 99.341% | 77.30% | 1 | `tki-1308-2` |

#### hanger-rack — top 30

| # | page | cosine vs nearest sibling | 5-gram Jaccard | unique word types | nearest sibling |
|--:|---|--:|--:|--:|---|
| 1 | `/hanger-rack/km-23/km-2360/` | 99.565% | 72.64% | 1 | `km-2306` |
| 2 | `/hanger-rack/km-22/km-2240/` | 99.537% | 72.75% | 0 | `km-2222` |
| 3 | `/hanger-rack/da-3/da-32-black/` | 99.382% | 75.06% | 0 | `da-32-white` |
| 4 | `/hanger-rack/da-3/da-32-white/` | 99.382% | 75.06% | 0 | `da-32-black` |
| 5 | `/hanger-rack/km-23/km-2324/` | 99.355% | 76.10% | 0 | `km-2342` |
| 6 | `/hanger-rack/km-23/km-2342/` | 99.355% | 76.10% | 1 | `km-2324` |
| 7 | `/hanger-rack/kr-23/kr-2324/` | 99.348% | 76.47% | 0 | `kr-2342` |
| 8 | `/hanger-rack/kr-23/kl-2324/` | 99.348% | 76.04% | 1 | `kl-2342` |
| 9 | `/hanger-rack/kr-13/kl-1312/` | 99.348% | 76.04% | 0 | `kl-1321` |
| 10 | `/hanger-rack/kr-14/kr-1404/` | 99.331% | 76.53% | 1 | `kr-1440` |
| 11 | `/hanger-rack/kr-13/kr-1303/` | 99.330% | 76.79% | 2 | `kr-1330` |
| 12 | `/hanger-rack/km-23/km-2306/` | 99.320% | 76.04% | 1 | `km-2324` |
| 13 | `/hanger-rack/kr-14/kl-1431/` | 99.316% | 76.64% | 0 | `kl-1440` |
| 14 | `/hanger-rack/kr-14/kl-1440/` | 99.316% | 76.64% | 0 | `kl-1431` |
| 15 | `/hanger-rack/km-22/km-2204/` | 99.315% | 75.49% | 1 | `km-2222` |
| 16 | `/hanger-rack/km-22/km-2222/` | 99.315% | 75.49% | 1 | `km-2204` |
| 17 | `/hanger-rack/kr-24/kl-2408/` | 99.315% | 76.21% | 1 | `kl-2426` |
| 18 | `/hanger-rack/kr-14/kl-1404/` | 99.315% | 76.21% | 0 | `kl-1413` |
| 19 | `/hanger-rack/kr-24/kr-2480/` | 99.314% | 77.45% | 1 | `kr-2462` |
| 20 | `/hanger-rack/kr-24/kr-2462/` | 99.314% | 77.45% | 2 | `kr-2480` |
| 21 | `/hanger-rack/kr-24/kr-2426/` | 99.314% | 76.59% | 0 | `kr-2480` |
| 22 | `/hanger-rack/kr-14/kr-1431/` | 99.314% | 77.45% | 0 | `kr-1440` |
| 23 | `/hanger-rack/kr-14/kr-1440/` | 99.314% | 77.45% | 0 | `kr-1431` |
| 24 | `/hanger-rack/kr-14/kr-1413/` | 99.314% | 76.59% | 1 | `kr-1440` |
| 25 | `/hanger-rack/kr-24/kr-2408/` | 99.314% | 76.10% | 1 | `kr-2480` |
| 26 | `/hanger-rack/kr-23/kl-2342/` | 99.313% | 76.41% | 1 | `kl-2360` |
| 27 | `/hanger-rack/kr-23/kl-2360/` | 99.313% | 76.41% | 1 | `kl-2342` |
| 28 | `/hanger-rack/kr-13/kr-1321/` | 99.313% | 77.28% | 0 | `kr-1330` |
| 29 | `/hanger-rack/kr-13/kr-1330/` | 99.313% | 77.28% | 0 | `kr-1321` |
| 30 | `/hanger-rack/kr-13/kr-1312/` | 99.313% | 76.85% | 0 | `kr-1330` |

#### documents-cabinet — top 30

| # | page | cosine vs nearest sibling | 5-gram Jaccard | unique word types | nearest sibling |
|--:|---|--:|--:|--:|---|
| 1 | `/documents-cabinet/a4l-330d/a4a-345d/` | 99.351% | 78.35% | 1 | `a4m-345d` |
| 2 | `/documents-cabinet/a4l-330d/a4m-345d/` | 99.351% | 78.35% | 1 | `a4a-345d` |
| 3 | `/documents-cabinet/a4l-330/a4m-345/` | 99.341% | 80.05% | 1 | `a4m-354` |
| 4 | `/documents-cabinet/a4l-330/a4m-354/` | 99.341% | 80.05% | 2 | `a4m-345` |
| 5 | `/documents-cabinet/a4l-330/a4lm-32418/` | 99.341% | 79.59% | 0 | `a4m-345` |
| 6 | `/documents-cabinet/a4l-330/a4lm-32015/` | 99.341% | 79.13% | 1 | `a4lm-32418` |
| 7 | `/documents-cabinet/a4l-204/a4m-206p/` | 99.340% | 79.90% | 1 | `a4m-212` |
| 8 | `/documents-cabinet/a4l-204/a4m-212/` | 99.340% | 79.90% | 1 | `a4m-206p` |
| 9 | `/documents-cabinet/a4l-204/a4a-206p/` | 99.340% | 78.97% | 2 | `a4a-212` |
| 10 | `/documents-cabinet/a4l-204/a4a-212/` | 99.340% | 78.97% | 2 | `a4a-206p` |
| 11 | `/documents-cabinet/a4l-220/a4a-230/` | 99.339% | 78.29% | 1 | `a4m-230` |
| 12 | `/documents-cabinet/a4l-220/a4m-230/` | 99.339% | 78.29% | 1 | `a4a-230` |
| 13 | `/documents-cabinet/a4l-104/a4m-106/` | 99.338% | 79.69% | 1 | `a4lm-10203` |
| 14 | `/documents-cabinet/a4l-104/a4lm-10203/` | 99.338% | 79.69% | 2 | `a4m-106` |
| 15 | `/documents-cabinet/a4l-104/a4a-106/` | 99.338% | 77.84% | 1 | `a4lm-10203` |
| 16 | `/documents-cabinet/a4l-110/a4a-115/` | 99.338% | 78.24% | 1 | `a4m-115` |
| 17 | `/documents-cabinet/a4l-110/a4m-115/` | 99.338% | 78.24% | 1 | `a4a-115` |
| 18 | `/documents-cabinet/a4l-204/a4l-204p/` | 99.335% | 78.46% | 1 | `a4l-208` |
| 19 | `/documents-cabinet/a4l-204/a4l-208/` | 99.335% | 78.46% | 1 | `a4l-204p` |
| 20 | `/documents-cabinet/a4l-330/a4a-354/` | 99.323% | 78.68% | 1 | `a4a-345` |
| 21 | `/documents-cabinet/a4l-330/a4a-345/` | 99.323% | 78.68% | 2 | `a4a-354` |
| 22 | `/documents-cabinet/a4l-330/a4l-330/` | 99.197% | 73.46% | 1 | `a4l-336` |
| 23 | `/documents-cabinet/a4l-330/a4l-336/` | 99.197% | 73.46% | 1 | `a4l-330` |
| 24 | `/documents-cabinet/a4l-330d/a4l-330d/` | 99.169% | 72.82% | 1 | `a4m-345d` |
| 25 | `/documents-cabinet/a4l-104/a4l-104/` | 99.136% | 71.89% | 1 | `a4lm-10203` |
| 26 | `/documents-cabinet/a4l-110/a4l-110/` | 99.135% | 72.25% | 1 | `a4m-115` |
| 27 | `/documents-cabinet/a4l-220/a4l-220/` | 99.129% | 72.07% | 1 | `a4m-230` |
| 28 | `/documents-cabinet/toa-14/toa-14/` | 97.004% | 63.35% | 7 | `a4l-110` |

#### locker — top 30

| # | page | cosine vs nearest sibling | 5-gram Jaccard | unique word types | nearest sibling |
|--:|---|--:|--:|--:|---|
| 1 | `/locker/locker-white/fba-202aw/` | 99.193% | 77.73% | 0 | `fba-204aw` |
| 2 | `/locker/locker-white/fba-204aw/` | 99.193% | 77.73% | 0 | `fba-202aw` |
| 3 | `/locker/locker-gray/fbb-202a/` | 99.190% | 76.72% | 1 | `fbb-204a` |
| 4 | `/locker/locker-gray/fbb-204a/` | 99.190% | 76.72% | 1 | `fbb-202a` |
| 5 | `/locker/locker-gray/fbb-208a/` | 99.189% | 76.72% | 1 | `fbb-204a` |
| 6 | `/locker/locker-gray/fbb-303a/` | 99.189% | 76.72% | 1 | `fbb-208a` |
| 7 | `/locker/locker-gray/fbb-306a/` | 99.189% | 76.72% | 1 | `fbb-303a` |
| 8 | `/locker/locker-gray/fbb-204/` | 99.169% | 76.62% | 1 | `fbb-202` |
| 9 | `/locker/locker-gray/fbb-202/` | 99.169% | 76.62% | 2 | `fbb-204` |
| 10 | `/locker/locker-gray/fbb-208/` | 99.168% | 76.62% | 1 | `fbb-204` |
| 11 | `/locker/locker-gray/fbb-303/` | 99.168% | 76.62% | 2 | `fbb-208` |
| 12 | `/locker/locker-gray/fbb-306/` | 99.168% | 76.62% | 2 | `fbb-312` |
| 13 | `/locker/locker-white/fba-204w/` | 99.163% | 76.34% | 2 | `fba-202w` |
| 14 | `/locker/locker-white/fba-202w/` | 99.163% | 76.34% | 3 | `fba-204w` |
| 15 | `/locker/locker-gray/fbb-309a/` | 99.044% | 78.21% | 1 | `fbb-312a` |
| 16 | `/locker/locker-gray/fbb-309/` | 99.032% | 76.51% | 4 | `fbb-315` |
| 17 | `/locker/locker-gray/fbb-312a/` | 98.946% | 79.74% | 2 | `fbb-315a` |
| 18 | `/locker/locker-gray/fbb-315a/` | 98.946% | 79.74% | 2 | `fbb-312a` |
| 19 | `/locker/locker-gray/fbb-312/` | 98.928% | 79.34% | 1 | `fbb-315` |
| 20 | `/locker/locker-gray/fbb-315/` | 98.928% | 79.34% | 2 | `fbb-312` |

#### rack — top 30

| # | page | cosine vs nearest sibling | 5-gram Jaccard | unique word types | nearest sibling |
|--:|---|--:|--:|--:|---|
| 1 | `/rack/me/me-321/` | 99.349% | 75.00% | 1 | `me-322` |
| 2 | `/rack/me/me-322/` | 99.349% | 75.00% | 1 | `me-321` |
| 3 | `/rack/mb-2/mb-206/` | 99.178% | 76.35% | 2 | `mb-208` |
| 4 | `/rack/mb-2/mb-208/` | 99.178% | 76.35% | 3 | `mb-206` |
| 5 | `/rack/mb-2/mb-2081/` | 99.178% | 77.08% | 1 | `mb-2061` |
| 6 | `/rack/mb-2/mb-2061/` | 99.178% | 77.08% | 2 | `mb-2081` |
| 7 | `/rack/mb-3/mb-3091/` | 99.178% | 77.08% | 2 | `mb-3121` |
| 8 | `/rack/mb-3/mb-3121/` | 99.178% | 77.08% | 3 | `mb-3091` |
| 9 | `/rack/mb-3/mb-312/` | 99.155% | 75.15% | 2 | `mb-309` |
| 10 | `/rack/mb-3/mb-309/` | 99.155% | 75.15% | 5 | `mb-312` |


### A2 — Full on-page field coverage (count of SKU pages carrying a non-empty value)

| field | workbench | tool-cabinet | perforated-board | workstation | cnc-tool | parts-cabinet | hanger-rack | documents-cabinet | locker | rack | TOTAL |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **SKU pages** | 893 | 219 | 113 | 86 | 90 | 71 | 59 | 28 | 20 | 10 | **1589** |
| Dimensions | 874 | 43 | 79 | 86 | 30 | 31 | 59 | 9 | 20 | 10 | 1241 |
| Material / Top | 870 | 43 | 78 | 86 | 0 | 20 | 59 | 1 | 20 | 10 | 1187 |
| Panel set | 636 | 0 | 0 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 653 |
| Load capacity | 184 | 15 | 2 | 16 | 0 | 9 | 0 | 0 | 1 | 1 | 228 |
| Colour | 56 | 16 | 84 | 0 | 15 | 10 | 15 | 27 | 0 | 0 | 223 |
| Type | 96 | 0 | 33 | 12 | 0 | 20 | 36 | 0 | 0 | 2 | 199 |
| Drawers | 0 | 160 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 161 |
| Cabinet | 0 | 32 | 0 | 0 | 60 | 55 | 0 | 0 | 0 | 0 | 147 |
| Cabinet (slide system) | 0 | 128 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 128 |
| Tool Holders | 0 | 0 | 0 | 0 | 90 | 0 | 0 | 0 | 0 | 0 | 90 |
| Steel Top | 72 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 72 |
| Accessories | 36 | 21 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 67 |
| Panel | 0 | 0 | 0 | 0 | 0 | 0 | 43 | 0 | 0 | 0 | 43 |
| Drawer | 0 | 0 | 0 | 8 | 0 | 35 | 0 | 0 | 0 | 0 | 43 |
| Panel Set | 36 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 43 |
| Quantity | 6 | 0 | 20 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 27 |
| Storage unit | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 20 | 0 | 20 |
| Lock | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 20 | 0 | 20 |
| Combination | 0 | 0 | 0 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 18 |
| Bins | 0 | 0 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 17 |
| Layer A, B | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16 |
| Drawer Qty | 0 | 4 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 12 |
| Layer C | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| NA | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 10 |
| Model No. (color) | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| HEUER Vise | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| Jaw Width | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| Hoist Rail | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 8 |
| Bench Vise | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| Drawer Rack | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| Shelf Qty | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 8 |
| Drawer Qty (Color) | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 8 |
| Shelf depth | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 8 |
| Qty | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 6 |
| Shelf | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| Reference price (RM) | 893 | 219 | 45 | 86 | 90 | 66 | 59 | 27 | 20 | 10 | 1515 |
| >=2 product images | 15 | 150 | 0 | 29 | 75 | 6 | 8 | 0 | 0 | 0 | 283 |


### A3 — Scripts

All analysis scripts are in the session scratchpad (deliberately not committed):

```
C:/Users/User/AppData/Local/Temp/claude/C--Users-User-Documents-GitHub-tanko-website-1-/d997d937-bb41-4fe2-9e31-8609dc417d7b/scratchpad
  extract_text.py        strip 1,779 pages to visible text -> pages.jsonl
  analyze_dupes.py       boilerplate share, unique-token counts, pairwise similarity
  analyze_sections.py    per-section word budget, within-family similarity
  page_fields.py         harvest on-page spec key/values -> page_fields.json
  field_inventory.py     join products.json + merchant feed + catalog csv
  analyze_templates.py   prose-skeleton collapse, worst-30 tables, closest-pair diffs
  consolidation.py       R1-R4 consolidation rules and page counts
  gen_prototype.py       working prototype of the generator in section 3
```
