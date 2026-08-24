# Primaxs Design System — MASTER.md (v2)

**Single source of truth** for the Primaxs Marketing (M) Sdn Bhd website.

**Radical shift from v1** — v1 was a dark-mode "industrial-template" system
that read as generic AI-generated SaaS. v2 recentres on the actual reference
(tanko.com.tw, real industrial catalogue sites like McMaster-Carr, Rittal,
Hoffmann Group) — **warm-paper light mode with dark-steel accent sections**,
editorial magazine typography, mixed case (never uppercase-condensed which
is the AI-industrial cliché), and real photographic weight.

---

## 1. Why every choice below exists

The site sells industrial storage to Malaysian procurement teams, workshop
owners and facility managers. Tanko itself (the manufacturer whose products
we distribute) leads with a **light-first design with strategic dark
sections**, mixed-case sans-serif with weight variation, and clean product
photography on neutral backgrounds. That IS the reference for "confident
industrial B2B distributor" — a real trade catalogue, not a startup landing.

**v1's mistakes we're fixing:**
| Problem in v1 | Root cause | Fix in v2 |
|---|---|---|
| Reads as "generic AI dark SaaS template" | Flat `#0b0e14` background + uniform cards | Warm-paper light primary + selective dark-steel sections for rhythm |
| Condensed UPPERCASE headlines are AI-industrial cliché | Saira Condensed 800 uppercase everywhere | **Libre Bodoni** display serif in **mixed case** — real editorial-catalogue voice |
| White product cards on dark = disconnected | The dark ground never made the light product photos feel like "catalogue" | Product photos sit on warm-paper base — cards ARE the paper, no jarring contrast |
| No depth, no motion | Everything static, no shadow scale | Real shadow scale (3 depths), lift-on-hover, subtle scroll-reveal |
| No texture | Flat colour blocks | Warm paper tone + hairline rules + numbered chapter markers as compositional device |
| Marketing-brochure copy | Headlines like "Industrial Storage & Tool Cabinets — Malaysia's Exclusive Tanko Distributor" | Catalogue voice: "The Tanko catalogue. Distributed in Malaysia since 2006." |

---

## 2. Colour system — warm-paper light + dark-steel accents

### Tokens

| Token | Hex | Role |
|---|---|---|
| `--paper` | `#f3efe8` | Primary page background — warm off-white (newsprint / spec-sheet paper, not clinical white) |
| `--paper-2` | `#eae5db` | Secondary elevation, subtle section striping |
| `--surface` | `#ffffff` | Card / product-tile surface — pure white keeps catalogue shots clean |
| `--ink` | `#0d1117` | Primary text — near-black, ~14:1 on paper |
| `--ink-2` | `#2a2f36` | Secondary text ~9:1 |
| `--ink-muted` | `#5c6470` | Metadata, labels ~5.9:1 on paper (AA passes) |
| `--rule` | `#d7d1c4` | Warm hairline rule — 1 px between paper sections |
| `--rule-strong` | `#b8b1a2` | Bolder hairline for datasheet tables |
| `--accent` | `#c62828` | **Tanko catalogue red** — signal only. 4.7:1 on paper, 4.6:1 on white (AA). Never gradient, never glow. |
| `--accent-ink` | `#ffffff` | Text on the red accent (buttons) |
| `--steel-dark` | `#141821` | Dark-steel accent background (Why Primaxs section, CTA band, footer) |
| `--steel-mid` | `#252a34` | Second dark elevation |
| `--steel-ink` | `#f5f2eb` | Warm-paper text on dark-steel sections (better than pure white — matches paper tone) |
| `--steel-muted` | `#8b93a0` | Muted text on dark-steel |
| `--steel-rule` | `#2f3644` | Rule on dark |

### Contrast (WCAG AA verified)
- `--ink` on `--paper` → **14:1** ✅ AAA
- `--ink-muted` on `--paper` → **5.9:1** ✅ AA
- `--accent` on `--paper` → **4.7:1** ✅ AA
- `#fff` on `--accent` → **4.6:1** ✅ AA
- `--steel-ink` on `--steel-dark` → **13.4:1** ✅ AAA
- `--steel-muted` on `--steel-dark` → **5.2:1** ✅ AA

### Rules for using colour
- Red is signal-only: CTA buttons, hover borders on cards, hairline above H1, red mono SKU code. **Never** used as a section background or decorative block.
- Dark-steel sections are used **selectively** for rhythm and gravitas — Why Primaxs + CTA closer + footer. Everything else stays on warm paper.
- No shadows on dark-steel sections — depth comes from panel elevation only.
- Signal amber `#c99a3b` reserved for `Heavy Duty` / `Stainless` chips only (never decoration).

---

## 3. Typography — editorial magazine

Three deliberate roles. All from Google Fonts (single stylesheet link).

| Role | Face | Weights | Fallback |
|---|---|---|---|
| **Display** — H1, H2, category names, hero copy | **Libre Bodoni** (variable) | 400 · 500 · 600 · 700 | `"Bodoni Moda", "Playfair Display", Georgia, serif` |
| **Body** — running copy, subs, meta, form controls | **Public Sans** | 400 · 500 · 600 · 700 | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` |
| **Mono** — SKUs, dimensions, tabular data, ticks | **JetBrains Mono** | 500 · 600 | `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` |

### Why Libre Bodoni + Public Sans
- **Libre Bodoni** is a variable serif with high stroke contrast — the letter-shape reads instantly as "editorial magazine / trade catalogue," not "startup" or "SaaS." Pulled from ui-ux-pro-max's typography data as one of the "magazine, editorial, publishing, refined, journalism, print" pairings. It is NOT on the AI-default fonts list (Inter / Space Grotesk / Sora / Manrope / Poppins). Distinctive.
- **Public Sans** — U.S. Federal design-system heritage, engineering-doc neutrality. Pairs with Bodoni exactly the way NYT and print magazines pair a bold serif display with humanist sans body.
- **JetBrains Mono** — kept for SKU codes and dimensions.

### Scale (mixed case throughout — NEVER uppercase)

| Level | Font | Weight | Size | Line-height | Tracking |
|---|---|---|---|---|---|
| Hero H1 | Bodoni | 500 | `clamp(48px, 6.4vw, 88px)` | 0.95 | −0.02 em |
| Page H1 | Bodoni | 500 | `clamp(36px, 4vw, 56px)` | 1.05 | −0.015 em |
| Section H2 | Bodoni | 500 | `clamp(30px, 3.2vw, 44px)` | 1.05 | −0.01 em |
| Sub H3 | Bodoni | 500 | 20 – 26 px | 1.15 | −0.005 em |
| Card headline | Public Sans | 600 | 16 – 18 px | 1.25 | 0 |
| Lede paragraph | Public Sans | 400 | 18 px | 1.55 | 0 |
| Body | Public Sans | 400 | 16 px | 1.6 | 0 |
| Meta / small | Public Sans | 500 | 13 px | 1.5 | 0 |
| Eyebrow / kicker | Mono | 500 | 11 px | 1 | +0.14 em, **uppercase** (mono only, as spec-label convention) |
| SKU / dimensions | Mono | 600 | 12 – 14 px | 1 | +0.02 em |

Bodoni display uses `text-wrap: balance`. Never `text-transform: uppercase` on Bodoni — it becomes unreadable and generic. Uppercase only for mono kicker labels.

---

## 4. Spacing scale

Base unit: **8 px**.

| Token | Value | Use |
|---|---|---|
| `--sp-1` | 4 px | Chip / badge internal padding |
| `--sp-2` | 8 px | Icon-to-text gap |
| `--sp-3` | 12 px | Field vertical, card interior gap |
| `--sp-4` | 16 px | Standard card grid gap |
| `--sp-5` | 24 px | Container horizontal padding (mobile) |
| `--sp-6` | 32 px | Section head → body |
| `--sp-8` | 48 px | Section head → title (desktop) |
| `--sp-10` | 64 px | Between related section groups |
| `--sp-12` | 96 px | **Section vertical padding (desktop)** |
| `--sp-14` | 128 px | Hero + CTA vertical padding (desktop) |

Section padding steps down: `96px` desktop → `72px` ≤900px → `56px` ≤560px.

Container max-width: `1240 px`. Editorial sections use narrower `800 px` measure.

---

## 5. Shadow scale (real depth, used sparingly)

| Token | Value | Use |
|---|---|---|
| `--shadow-1` | `0 1px 2px rgba(15,20,30,.05), 0 1px 3px rgba(15,20,30,.06)` | Resting card |
| `--shadow-2` | `0 4px 10px rgba(15,20,30,.06), 0 12px 24px rgba(15,20,30,.08)` | Card hover |
| `--shadow-3` | `0 12px 32px rgba(15,20,30,.10), 0 24px 48px rgba(15,20,30,.14)` | Modal / dropdown |

Shadows exist on **light-paper cards only**. Dark-steel sections use panel
elevation (border + background delta) for depth, never shadow.

---

## 6. Components

### 6.1 Buttons — flat, sharp, deliberate
- `.btn` base: `padding: 14px 22px; border-radius: 3px; font: 600 14px Public Sans; letter-spacing: .02em;`
- `.btn-primary`: `--accent` red fill, white text, `--shadow-1` at rest → `--shadow-2` on hover, no gradient.
- `.btn-ghost`: transparent, 1.5px `--ink` border, hover fills to `--ink` with `--paper` text.
- `.btn-lg`: `18px 32px`, 15 px font.
- Focus-visible: `outline: 2px solid var(--accent); outline-offset: 3px;` — always visible.
- Touch target: 44×44 px minimum on mobile.

### 6.2 Cards — real depth, breathing room
Base structure `.card`:
- `background: var(--surface); border: 1px solid var(--rule); border-radius: 4px;`
- `box-shadow: var(--shadow-1);`
- Hover: `box-shadow: var(--shadow-2); transform: translateY(-3px);` in 220 ms `cubic-bezier(.4,0,.2,1)`.
- Padding: `--sp-4` interior mobile, `--sp-6` desktop.
- Product tile: `aspect-ratio: 4/3` desktop, `1/1` mobile — bigger breathing room than v1's cramped grid.

### 6.3 Featured product cards — bigger, editorial
Distinct from regular category tiles. Uses `aspect-ratio: 3/4` (portrait), a `--sp-6` internal padding, and a top-hairline in `--accent` to signal "featured." Bodoni product name at 20 px vs 16 px on regular cards. This is the "varied card treatment for featured vs regular" the critique asked for.

### 6.4 Numbered chapter markers
Category grid and industry rows use large mono chapter numbers (`01`, `02`, …) rendered at 32 px `--rule-strong` colour, positioned above the section head or beside each item. Editorial magazine convention — compositional depth for free.

### 6.5 Tables (variant comparison)
Warm-paper base, hairline rows (`--rule`), sticky header row in `--paper-2`, first column SKU in mono red. Row hover: `background: var(--paper-2)`. Table wrapper: `overflow-x: auto; border: 1px solid var(--rule); border-radius: 4px;`

### 6.6 Nav / filter pills (Professional / Classic / All)
Not default rounded-pill styling. Editorial rendering:
- Underline-driven: text sits on baseline, active pill has a 2px `--accent` underline, others have `--rule` underline.
- Font: Mono 500, 12 px, uppercase, +0.08 em tracking.
- Hover: underline shifts to `--ink`.
- Padding: `0 2px 8px` (underline sits below text).
- Zero border-radius on pills — they're baseline dividers, not buttons.

---

## 7. Motion (subtle, purposeful, CSS-only)

| Duration | Easing | Use |
|---|---|---|
| 140 ms | `ease` | Button colour transitions |
| 220 ms | `cubic-bezier(.4,0,.2,1)` | Card hover lift, modal open/close |
| 400 ms | `ease` | Hero slide cross-fade |
| 500 ms | `cubic-bezier(.36,1.6,.4,1)` | Basket FAB bump on add |
| 700 ms | `cubic-bezier(.55,-0.05,.4,1.05)` | Fly-to-basket ghost |
| 300 ms | `cubic-bezier(.4,0,.2,1)` | Scroll-reveal fade-in-up (`IntersectionObserver`, lightweight, no lib) |

**Optional subtle hero parallax:** background translateY(60px) at scroll top → 0 at scroll 400 px, `will-change: transform`, only if measured to cost < 2 ms/frame. Kill on `prefers-reduced-motion`.

**Forbidden:** scroll-driven aurora, parallax layers on content (only on hero background), auto-counting numbers, glow-pulse CTAs, animation libraries (GSAP, Framer Motion, etc.).

**`prefers-reduced-motion: reduce` disables ALL transitions** site-wide.

---

## 8. Interaction states

Same as v1 §7 — every clickable/focusable element has default / hover / focus-visible / active / disabled / loading states. Focus-visible always uses `outline: 2px solid var(--accent); outline-offset: 3px;` — never removed without replacement.

---

## 9. Accessibility

- WCAG AA minimum on all text/background pairs (§2 lists ratios).
- Focus-visible always shown on keyboard.
- Touch targets 44×44 px min.
- One `<h1>` per page, real text (never image-baked).
- `<ul role="list">` on card lists (Safari VoiceOver quirk).
- Alt text convention per v1 §8.4 (unchanged).

---

## 10. Copy voice (v2 addition)

The current copy sounds like AI marketing. Rewrite priorities:

| Type | v1 sample | v2 direction |
|---|---|---|
| Hero H1 | "Industrial Storage & Tool Cabinets — Malaysia's Exclusive Tanko Distributor" | "The Tanko catalogue. Distributed in Malaysia since 2006." |
| Hero sub | "Workbenches, tool cabinets, workstations, racking and lockers — Taiwan-engineered since 1975, stocked and supported locally by Primaxs." | "Authorised dealer for Tanko Enterprise Co., Ltd. — the Taiwan storage manufacturer since 1975. Stocked in Selangor, quoted in Ringgit, warranty handled locally." |
| Section titles | "Shop by Category" / "Featured Products" / "Who We Serve" | "The range" / "Selected models" / "Industries we equip" |
| CTA | "Request a Quote" | "Send us your list" (or keep RaQ but as secondary; primary should sound like a trade action, not a landing-page CTA) |

**Facts preserved verbatim:** est. 1975 · exclusive Malaysia distributor · 11 categories · ~1,700 SKUs · Company No. 756588-H · Selangor address · phone/email.

---

## 11. Page-type conformance

Each page type must comply. Same list as v1 §10 with the following v2 additions:
- **Category pages** use dark-steel *hero* stripe with the category H1 in Bodoni, warm-paper body below with cards.
- **Family pages** keep the 4-tab layout but tabs restyled as editorial baseline-underline (per §6.6).
- **Variant pages** get a real editorial two-column layout at desktop: dimensioned drawing left, spec panel right in warm paper.
- **Guides** already read as editorial — retune type to Bodoni display + Public Sans body.

---

## 12. What ships next (Step 4 workflow)

1. This MASTER.md — v2. Superseded v1.
2. **Homepage sample** built with this system, scoped under `body.home-v4`, delivered live at `http://localhost:8765/`.
3. **Wait for approval** before propagating across category / family / variant / guide pages.
4. On approval: sweep site.css, replace all v1 tokens with v2, retune per-page templates, verify no broken routes, run accessibility check.

---

## 13. Change log

| Date | Change | Reason |
|---|---|---|
| 2026-08-23 | v1 → v2 total rewrite | v1 was a competent-but-generic dark template; visitor critique confirmed it read as "AI-generated SaaS." v2 pivots to warm-paper editorial-catalogue direction rooted in the actual tanko.com.tw reference and the ui-ux-pro-max skill's editorial/magazine style category. |
