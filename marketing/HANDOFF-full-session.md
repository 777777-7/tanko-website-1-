# Full handoff — everything from this working session

**Purpose:** hand the entire context to a fresh Claude. The raw transcript is
142 MB and unusable; this is the same knowledge in 15 minutes of reading.

**Covers:** 12–17 September 2026, 58 commits.
**Last updated:** 17 September 2026

> Read this file first. Then [HANDOFF-supplier-expansion.md](HANDOFF-supplier-expansion.md)
> if the work is about suppliers, or the linked files in §8 for anything else.

---

## 1. Who and what

**Wong Wei Ming** — Business Development Manager at **Primaxs Marketing (M) Sdn
Bhd**, Seri Kembangan, Selangor. **It is his uncle's company; he is not the
founder.** Solo operator on all of this.

**Primaxs is the exclusive Malaysia distributor for Tanko Enterprise Co., Ltd.
(Taiwan) since 2006** — industrial storage across 11 categories, 1,517 products:
workbenches, tool cabinets, CNC tool storage, lockers, racking, perforated boards,
parts cabinets, document cabinets, hanger racks, workstations, household items.

**storagesystem.com.my** — 1,851 pages, English + full Bahasa Malaysia twins,
ranks **#1 in Malaysia for CNC tool storage**. Google Merchant Center feed, Google
Business Profile, Supabase-backed `/sales/` area. He built all of it. It is both
the main revenue channel and the main argument in every supplier email.

**Contact block used everywhere:** No. 39, Jalan Balakong Jaya 4, Taman Industri
Balakong Jaya, 43300 Seri Kembangan, Selangor · Tel +60 3-4296 4737 · WhatsApp
+60 11-5841 9886 · sales@storagesystem.my

---

## 2. Standing constraints — these cause real damage if got wrong

These are also stored as memory files in
`.claude/projects/C--Users-User-Documents-GitHub-tanko-website-1-/memory/`.

| Rule | Detail |
|---|---|
| **Facebook** | **Primaxs Marketing Page only. NEVER his personal profile.** |
| **LinkedIn** | Posts **do** go from his personal profile |
| **74 unpriced SKUs** | *"unpriced for reason, i did not ask you to change, then dont change"* |
| **Commercial offer** | Free delivery Selangor/KL, free installation, outstation charged — **in every post** |
| **Every post needs an image** | No text-only posts on any channel. Pick the image *before* writing |
| **Cross-posting** | Every FB Page post also goes to the groups |
| **Rankings** | **Always GSC. Never his signed-in Chrome** |
| **He cannot** | Solve CAPTCHAs, create accounts, or enter passwords |
| **NP Points** | A stored balance — spending them is a purchase needing his authorisation |
| **Site freeze** | 16–23 Sep 2026: promotion only, no `docs/` edits unless he asks |
| **Repo model** | `main` deploys `docs/` directly. **Never rebuild `docs/`** — it regresses the pretty spec tables |
| **Warranty** | 1 year against manufacturing defects, administered locally in Selangor |

---

## 3. Platform automation quirks — expensive to learn, cheap to reuse

**These were all discovered by breaking something. Do not rediscover them.**

### Facebook

- **Attach the image BEFORE typing the text.** Attaching rebuilds the Lexical
  editor and orphans anything already typed — the post publishes image-only. This
  happened once and needed 9 posts repaired.
- Verify in **Meta Business Suite → 内容 → 帖子和 Reels**. *"该篇帖子没有文字内容"*
  means the post has no text.
- **Group post editor:** select the dialog that has **both** `编辑帖子` text **and**
  a textbox. Using `.pop()` picks a textbox-less dialog — this caused every
  apparent "scrambled text" bug.
- `execCommand('insertText')` is reliable and untruncated, but strips newlines.
  Between paragraphs dispatch
  `new InputEvent('beforeinput',{inputType:'insertParagraph',bubbles:true,cancelable:true})`.
- Clear with real ctrl+A / Delete. Verify via `document.body.innerText`, **not**
  the textbox — it detaches on save and reads 0.
- **`navigator.clipboard.writeText` freezes the renderer on Facebook** even with
  the tab focused.
- **The "Call Now" upsell appears between 发帖 and publishing. Dismissing it with
  以后再说 switches the 速推 boost toggle ON — that is paid advertising.** This
  fired once and was caught before spend.

### LinkedIn

- **Photo attachment cannot be automated.** No `.click()` or `showPicker()`
  interception, shim invisible behind the inert modal, synthetic drag-drop
  ignored, clipboard image paste fails. **Wei Ming must pick the file himself.**
  Text typing works fine.

### Google Business Profile

- The post dialog lives in a **same-origin iframe** — find it via `/添加帖子/` in
  `contentDocument`.
- Image goes in via a shim input, re-creating the `File` inside the iframe's own
  `window`.
- **The "Learn more" URL field's reported coordinates do not match its screen
  position.** Workaround: put the URL in the body text instead.

### Google Search Console

- Daily indexing quota is about **10 URLs**.
- The URL inspection box needs a **fresh page load** and a `find`-derived ref —
  the autocomplete dropdown swallows Enter.

### General

- **NEVER `delete HTMLElement.prototype.click`** to undo a patch. Native `click`
  is an own property of that prototype and deleting it breaks the page. Recover
  from a fresh same-origin iframe's `contentWindow`.
- **Git commits: use a heredoc with `-F -`.** Unescaped quotes in `-m` broke a
  commit.
- Taiwantrade blocks plain fetches (403) — use a browser tool.
- JS-rendered catalogues return an empty template to a plain fetch. Find the data
  endpoint in the network log instead.

---

## 4. What was done, by workstream

### Site integrity

- **Reverted the cannibalisation retitle** (`5320d55f34`) — it had corrupted two
  guide `<h1>` tags. Restored via `git checkout 5320d55f34~1 -- docs/guides/`.
- **Full-site audit** — `scratchpad/audit.py`, all 1,854 pages, every perspective.
  Final state: **83 findings, all known-intentional** (74 unpriced offers, 5
  false-positive titles, 2 deliberate noindex, `sales/` canonical). The audit
  itself needed three fixes before it was trustworthy: URL-decoding, a literal
  `\x08` byte a bad patch had written into a regex, and stutter detection matching
  single letters in part numbers like "A4A-106".
- **341 dead `/asset3/*.jpg` schema images removed** (`b51adb3d02`) via
  `scratchpad/fix_schema_img.py`. **The first version would have stripped `@id`
  and breadcrumb URLs — caught by a dry run.** Rewritten to parse the JSON and
  only walk `"image"` keys.
- **173 wrong preview images fixed** (`205f204470`, `08912b60e4`) — 164 by subject,
  then 9 more found by a kind-based audit applied to every page after Wei Ming
  spotted one.

### The perforated board investigation

Wei Ming asked why it had "gone from top". Findings:

- Commit `527bb5f40f` (12 Sep) **had** stripped the singular "Perforated Board"
  from the title, og:title and h1 of 12 pages. Restored in `e62cd3069e`.
- **But the ranking drop was a 6-impression blip that had already self-recovered
  two days before I changed anything.** GSC for 14 Sep showed 9 clicks, 47
  impressions, position 7.0 — its best day ever. I had claimed a lasting drop;
  that was wrong and was retracted.

### Promotion

Two full days across Facebook Page + 9 groups + GBP + LinkedIn — perforated boards
(16 Sep) and steel lockers (17 Sep). Logged in
[social-queue.md](social-queue.md). One FB post published text-less and all 8
surviving group copies were repaired; one group had already deleted its copy as
spam.

### Listings and indexing

- **NEWPAGES confirmed complete** — 12/12 listings, 0 points. The wall there is
  commercial, not technical.
- Sitemap typo removed; 9 indexing requests submitted.
- Local inventory feed rebuilt with the store code Google actually assigned.
- `robots.txt` now names every AI crawler explicitly and no longer blocks
  Bytespider.
- Four location pages added for the free-delivery belt.

### Supplier expansion

The largest workstream. **See [HANDOFF-supplier-expansion.md](HANDOFF-supplier-expansion.md)
— it is complete on its own.** One-line summary: **Tai Sam #1 (email ready), Chung
Fu #2 (email ready), Yung Chia #3, castors withdrawn.**

---

## 5. Things I got wrong and retracted — do not reintroduce them

| Claim | Reality |
|---|---|
| "The perforated board product page title never changed" | **False.** `527bb5f40f` changed title, og:title and h1 across 12 pages |
| "The 12 Sep title change caused a lasting ranking drop" | **False.** It had recovered on its own by 14 Sep, before any fix |
| "Contact Bright Jing Chin first" | They are an Exporter only, no brand to be exclusive for, covering all Asia |
| "Malaysia is empty for GISON" | **Hup Sheng Hardware carries 127 GISON SKUs across 34 categories** |
| "Castors are the #1 opening" | JEIN YI's *territory* being open ≠ the *market* being open. KSW: 12 branches since 1992. UKAI: 9 imported brands since 1989 |
| "Yung Chia is a school furniture company" | Education is 32 of 253 products — **13%**. It is a contract furniture maker with 23 office task chairs |
| Audit reported 1,028 bugs | All false positives from three bugs in my own scanner |

**The pattern worth carrying forward: verify against the repo or GSC before
asserting a cause.** Most of these came from reasoning ahead of the evidence.

---

## 6. Open items

### Supplier work
- **Send the Tai Sam email** — `sales@tai-sam.com.tw`, cc `info@yoeshin.com.tw`
- **Send the Chung Fu email** — **no verified address yet**, only a Taiwantrade
  enquiry form. Finding one is an open task
- Yung Chia — one email; the deciding question is whether their Singapore office
  (2019) already covers Malaysia
- Confirm the Tanko agreement has no clause restricting other suppliers
- Decide what stock commitment is realistic before Tai Sam asks

### Site work, after the freeze lifts (23 Sep)
- **4 pages still need GSC indexing:** `/perforated-board/hangers/`,
  `/workbench/wa-57a/`, `/workbench/wa-67a/`, `/perforated-board/kp-47/kp-4701/`
- **~100 thin category pages** under 250 words
- **Missing pages:** privacy, terms, shipping, warranty
- Add a skip-link
- Resolve the cannibalisation question — the first attempt was reverted, so it is
  still open
- Check the GBP primary phone matches schema `+60-3-4296-4737`
- Facebook Page CTA button

---

## 7. How he works

- Solo developer. Deploys from `main` / `docs/`. Small edits direct to main, big
  changes on a branch.
- Wants **commits and pushes done for him**, with real commit messages.
- **Writes terse, often with typos** — *"cjheck perforatedf board website, why
  gone from top"*. Read past them; the intent is usually precise.
- **Pushes back when something is wrong, and is usually right.** *"what i sent you
  was the perforated board one"* and *"but yungchia got also company chairs"* both
  corrected real errors. Take the pushback seriously and re-check rather than
  defending.
- Prefers research written to a committed markdown file, not just chat.

---

## 8. Where everything lives

**Supplier work:** [HANDOFF-supplier-expansion.md](HANDOFF-supplier-expansion.md)
and the 10 files it lists.

**Marketing and SEO:** [README.md](README.md) indexes the folder. Key files —
[social-queue.md](social-queue.md) (post log),
[site-audit-2026-09-16.md](site-audit-2026-09-16.md),
[content-calendar.md](content-calendar.md), [rank1-research.md](rank1-research.md),
[icp-and-pains.md](icp-and-pains.md), [dedup-plan.md](dedup-plan.md),
[backlink-targets.md](backlink-targets.md).

**Cross-session memory:** 16 files in
`.claude/projects/C--Users-User-Documents-GitHub-tanko-website-1-/memory/`,
indexed by `MEMORY.md`. These encode the standing constraints in §2 and the
platform quirks in §3.

**Scripts:** `scratchpad/audit.py`, `fix_schema_img.py`, `fix_og_subject.py`,
`og_kind_audit.py`, `fix_og_kind.py`.

**History:** `git log --since="2026-09-12"` — 58 commits, messages written to
explain the reasoning rather than the diff.

---

## 9. Standing caution

Company facts, founding years, certifications and export markets in the supplier
research come from the companies' own records and are cited per file. **Prices,
MOQ, margins, freight costs and market sizes are not verified anywhere** — each
document says so in its final section. Rankings and scores are judgement, not
measurement. Site metrics come from GSC and from the repo itself.
