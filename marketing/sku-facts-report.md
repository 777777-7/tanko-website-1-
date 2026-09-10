# Tanko SKU Fact Base — Coverage Report

**Generated:** 2026-09-10
**Sources:** `TANKO Catalogue NO.E147.pdf` (52pp, primary), `TANKO_Catalogue_NO.E327.pdf` (4pp, Hexagonal Workbench supplement, printed 2025/11 — newer than E147), `tanko_catalog_extracted.csv` (cross-check only), `marketing/google-merchant-feed.tsv` (cross-check only), `docs/**/index.html` picker-data JSON (cross-check only).
**Output:** `marketing/sku-facts.json` — 661 records (619 real catalogue entries + 42 explicitly-flagged "not in catalogue" placeholders), every non-null field carries a `(source_pdf, page)` citation.

**Method note:** every page was rendered to an image (PyMuPDF `get_pixmap`, 2.0–2.5×) and read visually; wherever a page laid out several SKU cards side by side (tool-cabinet drawer stacks, CNC holder matrix), the visual read was cross-checked against `page.get_text("words")` word coordinates clustered by column x-range and sorted by y, because naive `page.get_text()` scrambles column order on this catalogue's multi-column pages. Every SKU code asserted to exist in the catalogue was additionally confirmed with a full-text regex search across both PDFs.

---

## 1. Coverage by category

| Category | Real records | Have dimensions | Have load rating | Have drawer stack | Have material/colour |
|---|---:|---:|---:|---:|---:|
| workbench | 164 | 156 (95%) | 63 (38%) | — (n/a, see §5) | 100 (61%) |
| tool-cabinet | 113 | 105 (93%) | 92 (81%) | 69 (61%) | 4 (4%) |
| cnc-tool | 64 | 58 (91%) | 26 (41%) | 6 (9%) | 0 |
| workstation | 66 | 66 (100%) | 26 (39%) | — | 11 (17%) |
| perforated-board | 62 | 21 (34%)¹ | 2 (3%) | — | 12 (19%) |
| hanger-rack | 55 | 54 (98%) | 55 (100%) | — | 0 |
| parts-cabinet | 32 | 32 (100%) | 9 (28%) | — | 9 (28%) |
| documents-cabinet | 14 | 14 (100%) | 0 | — | 3 (21%) |
| household-items | 16 | 16 (100%) | 0 | — | 5 (31%) |
| trolley | 15 | 15 (100%) | 12 (80%) | — | 10 (67%) |
| locker | 10 | 10 (100%) | 0 | — | 2 (20%) |
| rack | 8 | 8 (100%) | 8 (100%) | — | 0 |
| **Total** | **619** | **555 (90%)** | **293 (47%)** | **75** | **147 (24%)** |

¹ Perforated-board "no dimensions" rows are almost all hooks/holders/trays specified by length, hole diameter, or holder-count rather than W×D×H — the figure is present, just carried in the `note` field, not `dims_mm`.

"Load rating" coverage looks low in several categories (documents-cabinet, locker, rack-adjacent) because those product lines genuinely carry no printed load figure on their catalogue page — that absence is recorded honestly rather than backfilled.

Materials/colour coverage is concentrated in workbench (workbench-top letter codes N/F/W/S/T/TG/TH are fully decoded — see §4) and trolley/perforated-board (explicit colour swatches). Most tool-cabinet, cnc-tool, hanger-rack and workstation products are steel-cabinet items where the catalogue prints no distinct "material" field beyond "steel" implicitly — colour is shown only as a swatch dot with no printed name, so it was left `null` rather than guessed.

---

## 2. The 403-page "None" problem — what this fact base actually fixes

Live-site grep found 74 family-index pages still emitting the literal string `None` in their `picker-data` JSON (`dims`/`material`/`color`/`load` fields): 47 in workbench, 12 in tool-cabinet, 11 in workstation, 3 in cnc-tool, 1 in a guide page. This fact base directly supplies replacement values for:

- **All EA/EB/ED heavy-duty tool-cabinet drawer stacks and dimensions** (tool-cabinet/ea-10, ea-12, ea-7, ea-7m families) — previously the site had `"dims": null, "material": null, "color": null, "load": null` for every one of these 48 variant cards.
- **All EGA/EGM/EGL/ELA/ELS standard tool-cabinet dimensions and drawer stacks** (p21–23).
- **The full CNC holder-capacity matrix** for the ea-10n/ea-10mn/ea-12n/ea-7mn families (60 SKUs) — these had no on-page load or holder-count differentiator at all; the matrix in `sku-facts.json.cnc_holder_capacity_matrix` is the only way to tell those 90 cnc-tool SKUs apart.
- **Workbench top-material letter codes** (N/F/W/S/T/TG/TH) fully decoded with their printed construction description, resolving the "ALL 402 missing material values" gap for every workbench SKU whose material is only encoded as a one-letter suffix on its own model number.

---

## 3. Drawer-code verdict (EA-\<height\>\<drawers\>\<config\>)

**Working hypothesis:** `EA-<height/100><drawer count><config index>`, e.g. `EA-10051` = H1000, 5 drawers, config 1.

**Verdict: the digit-decoding formula is CONFIRMED. The claim that all 8 website dropdown values per family are real, catalogue-backed products is REFUTED — only 3 of 8 are.**

### Evidence

E147 p25 ("Tool Cabinet" / "Heavy Duty") prints a drawer-height stack to the left of each cabinet illustration for a subset of EA/EB/ED codes. Reading those stacks (PyMuPDF word-coordinates clustered by column, cross-checked against a 2.5× page render) and decoding the SKU suffix against the printed row count gives an exact match every time:

| SKU | Decoded as | Printed drawer-height stack (top→bottom) | Rows |
|---|---|---|---|
| EA-7042(T) | H700, 4 drawers, cfg 2 | 100 / 100T / 150T / 250T | 4 ✓ |
| EA-7051(T) | H700, 5 drawers, cfg 1 | 100 / 100T / 100T / 150T / 150T | 5 ✓ |
| EA-7061(T) | H700, 6 drawers, cfg 1 | 100 / 100T ×5 | 6 ✓ |
| EA-10062(T) | H1000, 6 drawers, cfg 2 | 100 / 150T / 150T / 150T / 150T / 200T | 6 ✓ |
| EA-10073(T) | H1000, 7 drawers, cfg 3 | 75 / 75 / 100T / 100T / 150T / 150T / 250T | 7 ✓ |
| EA-10091(T) | H1000, 9 drawers, cfg 1 | 100 / 100T ×8 | 9 ✓ |
| EA-12052(T) | H1200, 5 drawers, cfg 2 | 200T / 200T / 200T / 200T / 300T | 5 ✓ |
| EA-12071(T) | H1200, 7 drawers, cfg 1 | 150T ×6 / 200T | 7 ✓ |
| EA-12074(T) | H1200, 7 drawers, cfg 4 | 100 / 100T ×3 / 200T ×2 / 300T | 7 ✓ |

Every EB/ED sibling at the same height+suffix shares the identical stack, differing only in cabinet width/depth (EA=W566×D607, EB=W718×D607, ED=W718×D759).

**But**: a full-text regex search (`E[ABD]-\d{3,5}[A-Z]{0,2}`) across every page of both `TANKO Catalogue NO.E147.pdf` and `TANKO_Catalogue_NO.E327.pdf` finds that **only these 9 drawer-count/config combinations exist anywhere in either catalogue**: H700 → 042, 051, 061; H1000 → 062, 073, 091; H1200 → 052, 071, 074 (plus 3 mobile-M variants: 7042M, 7051M, 7042MA).

The website's own `Drawers` axis offers **8 values per family**:
- `ea-7` (H700): 7041, 7042, 7051, 7052, 7053, 7054, 7061, 7073 — only **7042, 7051, 7061** are in the catalogue.
- `ea-10` (H1000): 10051, 10052, 10061, 10062, 10071, 10072, 10073, 10091 — only **10062, 10073, 10091** are in the catalogue.
- `ea-12` (H1200): 12051, 12052, 12071, 12072, 12073, 12074, 12081, 12082 — only **12052, 12071, 12074** are in the catalogue.
- `ea-7m` (Mobile): 7041, 7042, 7051, 7052, 7053, 7054, 7061, 7081 — only **7042, 7051** (plus 7042 with a panel-set "MA" variant) are in the catalogue.

**42 of the resulting EA/EB/ED codes (listed in full in `sku-facts.json.skus`, `family` field starting "NOT IN CATALOGUE") do not occur anywhere in either PDF.** They are marked `dims_mm: null`, `drawer_stack_mm: null` in the fact base — do not invent a stack for them. Cross-checking `marketing/google-merchant-feed.tsv` confirms several of these unconfirmed codes (e.g. `EA-10051`, `EA-10052`, `EA-12051`) are nonetheless live, priced listings on the site today; whether they are genuine unpublished Tanko SKUs or a site-generation artefact could not be settled from the source catalogues and should be checked against Tanko directly before further content is written for them.

**What differs between config 1 and config 2 at the same drawer count:** confirmed to be **the drawer height stack** (and therefore which individual drawer rows are standard vs T-type slide), not the drawer count — e.g. H1200's two 7-drawer configs (071 vs 074) have completely different height sequences (150T×6+200T vs 100+100T×3+200T×2+300T) while the cabinet's own W×D×H is identical for a given letter+height. The outer cabinet dimensions never change with config; only the internal drawer-height layout does.

**T-suffix meaning (confirmed, E147 p24):** "Standard drawer" = 90% extension slide, 100kg load capacity. "T drawer" = 100% extension slide, 200kg load capacity. The SKU-level `(T)` suffix denotes the cabinet variant using T-type slides on the rows marked T in the printed stack; it is orthogonal to drawer count/config.

---

## 4. CNC tool-cabinet holder-capacity matrix (E147 p26)

The 90 cnc-tool SKUs break into two distinct catalogue-documented product lines:

**A. 60 SKUs (ea-10n, ea-10mn, ea-12n, ea-7mn families, 15 variants each)** — axes are `Cabinet (EA/EB/ED)` × `Tool Holders (BT-30/BT-40/BT-50/HSK-40/HSK-63)`. These share only 5 distinct cabinet dimension sets and carry no on-page top material or load rating of their own — **the p26 holder-qty matrix is the only fact that can differentiate them**, reproduced in full in `sku-facts.json.cnc_holder_capacity_matrix`:

| Taper | Drawer Tray — EA | Drawer Tray — EB | Drawer Tray — ED | Upper Tray — EA | Upper Tray — EB | Upper Tray — ED |
|---|---:|---:|---:|---:|---:|---:|
| BT-30 | 25 | 33 | 46 | 36 | 53 | 72 |
| BT-40 | 23 | 28 | 39 | 30 | 39 | 52 |
| BT-50 | 10 | 18 | 23 | 23 | 28 | 33 |
| HSK-40 | 25 | 33 | 46 | 36 | 53 | 72 |
| HSK-63 | 10 | 18 | 23 | 20 | 28 | 33 |

Each cabinet carries one drawer tray + one upper tray, so total holder capacity = the sum of the two cells for its taper+cabinet-letter combination. Load: 100kg/standard drawer, 200kg/T drawer, 1000kg static whole-frame (all confirmed p26).

**B. 30 SKUs (enr-12, ens-1, ens-3, san-33, san-36, san-36k families, 5 variants each)** — a *different* physical product line (CNC Trolley / CNC Tool Cabinet with Door), each with its own literal catalogue model number and its own holder-qty table (pages 27–29): SAN-331…338(M) H900, SAN-361…368(KM) H1780, ENS-1 (ENS-112M…182M), ENS-3 (ENS-312M…382M), ENR (ENR-1218M…1288M). All fully captured in `sku-facts.json`.

---

## 5. Workbench top-material code legend (fixes the "ALL 402 missing material values" gap)

Two overlapping letter systems, both confirmed from the catalogue:

- **N** = Rubber top — HDF covered with green rubber mat + PVC protective edges (Professional/Heavy Duty/Hexagonal workbenches).
- **F** = Laminate top — particle board covered with gray laminate + PVC protective edges.
- **W** = Wood top — finger-jointed rubber wood.
- **S** = Stainless steel top — HD material covered with 1.2mm stainless steel sheet (Heavy Duty only).
- **T** (Tanko top, Heavy Duty only) — multi-layer laminate + PVC protection on 4 edges, split into **TG** (36mm, W1500/1800×D750×H786) and **TH** (43mm, ×H793) sub-variants.
- **A** (Benchwork top, Heavy Duty p13 / E327 hexagonal) = 36mm base material covered with 9mm steel plate.

Every workbench family base code (WA-, WB-, WBT-, WBS-, WD-, WDT-, WAT-, WAS-, WAD-, WHB-, WHA-) takes one of these letters as a suffix; the family's W×D×H is constant across the letter, only the top construction changes (except TG/TH which also shift H by a few mm — captured explicitly).

---

## 6. Families the catalogue does NOT cover

- **The 42 EA/EB/ED drawer-count/config codes listed in §3** — not found in either PDF.
- **Individual per-taper CNC cabinet SKU codes** (e.g. a literal "EA-10031-BT30" code) — the catalogue prints one base cabinet code per height/mobility combination with a holder-count table alongside, not 15 separately-numbered SKUs; the per-taper differentiation must be applied via the matrix, not read off a printed per-SKU code.
- **Colour names for tool-cabinet/workstation/hanger-rack steel bodies** — shown only as unlabelled swatch dots (●) with no printed colour word, so left `null` rather than guessed from the dot's rendered hue.
- **Documents-cabinet, locker, and most rack products carry no printed whole-frame or per-shelf load rating** at all — genuinely absent from the catalogue, not an extraction gap.
- **E327's Hexagonal Workbench section is a near-duplicate of E147 p16–17** with one naming difference (see §7) — no new product line, just corroboration/contradiction data.

---

## 7. Contradictions found

1. **Hexagonal Workbench "Power Tower" SKUs are live on the site with the WRONG height (systematic, 8 SKUs / 16 site pages).** `docs/workbench/whb-88`, `whb-881`, `whb-882`, `wha-882` all list their `*N1A`/`*F1A` (Power Tower) variants at **W2500×D2165×H850mm** — identical to the plain "no accessory" base model. But E147 p17 (and E327 p3) print the Power-Tower variant's height as **H1100mm**: the power tower housing sits on top of the tabletop and visibly adds ~250mm. Confirmed via the catalogue's own printed dimension label next to each illustration on both pages. Affects: WHB-88N1A, WHB-88F1A, WHB-881N1A, WHB-881F1A, WHB-882N1A, WHB-882F1A, WHA-882N1A, WHA-882F1A.

2. **E147 vs E327 naming of the same Power-Tower SKUs.** E147 p17 names them with a trailing "A" (`WHB-88N1A`, `WHB-88F1A`, …). E327 p3 (dated 2025/11 on its own back cover — newer than E147, which carries no print date) shows the *same* products, same dimensions/accessories, named **without** the trailing A (`WHB-88N1`, `WHB-88F1`, …). The live site follows the older E147 naming. Not necessarily wrong, but worth flagging as Tanko's own most recent catalogue disagrees with the SKU string currently used.

3. **42 EA/EB/ED "drawer" dropdown values have no catalogue backing at all** (§3) yet several (e.g. EA-10051, EA-10052, EA-12051) are live, priced SKUs in `marketing/google-merchant-feed.tsv` today. Either they are genuine Tanko products not shown in these two catalogue editions, or they were generated by permutating the axis values without verifying against a real product line. Recommend confirming with Tanko directly before writing differentiated content for them — the safest interim copy is to describe them at the family level (shared dimensions with the confirmed E147 sibling) without inventing a specific drawer-height stack.

4. **No contradiction** was found between this extraction and `tanko_catalog_extracted.csv` on the ~140 SKUs both sources cover with a parsed W×D×H — full agreement, which corroborates the earlier partial extraction's dimension column (though it has no EA/EB/ED rows and is otherwise far less complete than this fact base).

---

## 8. Deliverable

`marketing/sku-facts.json` — top-level keys:
- `_meta` — extraction date, source list, method note, total record count, per-category counts.
- `drawer_code_verdict` — the §3 verdict, evidence table, and T-suffix meaning, machine-readable.
- `cnc_holder_capacity_matrix` — the §4 table, machine-readable (`drawer_tray_qty[taper][cabinet]`, `upper_tray_qty[taper][cabinet]`).
- `skus` — 661 records keyed by SKU (or by a bracket-notation family key, e.g. `WA-57[N/F/S/W]`, where the catalogue tabulates several sibling SKUs against one shared dimension row — each such key's `note` field spells out the literal suffixes it stands for). Every record carries `category`, `family`, `dims_mm` (or `null`), `load`, `drawer_stack_mm`/`drawer_count` where applicable, `material`/`color`, `accessories`, free-text `note`, and `sources: [{source_pdf, page}]`. 42 records are explicit "NOT IN CATALOGUE" placeholders (see §3) so downstream content generation cannot silently invent facts for them.
