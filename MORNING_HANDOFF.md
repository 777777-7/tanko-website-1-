# Morning Handoff — 2026-08-24

Everything I did overnight is in [OVERNIGHT_LOG.md](OVERNIGHT_LOG.md) with
timestamps. Deep SEO research is in
[SEO_RESEARCH_NOTES.md](SEO_RESEARCH_NOTES.md) with citations.

This file is the short "read me first with coffee" version.

---

## What's ready to ship

The site under `dist/` has 1,799 pages, all rendered from `python site/build.py`.
Every page:

- Has exactly one H1, a unique meta title (all ≤ 68 chars, most ≤ 60), a
  unique meta description (all ≤ 158 chars).
- Carries the correct JSON-LD schema for its page type (Organization,
  LocalBusiness with real address, WebSite, BreadcrumbList, CollectionPage,
  Product with hasVariant, Article + FAQPage on guides).
- Has real alt text on every image.
- Is reachable from the header nav, footer, or a category page — no
  orphans.

Sitemap: `dist/sitemap.xml` (1,798 URLs, auto-regenerated on every build)
Robots: `dist/robots.txt` (permissive to real-time AI answer engines,
blocks the aggressive scrapers).

---

## Three things I want your call on before touching them

### 1. Image compression (biggest performance lever)

`asset3/` is ~1 GB of product PNGs. About 1,100 files are 500 KB – 1 MB
and 10 are over 1 MB. On Malaysian mobile 4G, a 900 KB LCP image will
fail Google's 2.5 s "good" LCP threshold — and that's the single biggest
CWV risk on the whole site.

I already drafted a script (blocked from running until you approve — it
renames PNG to JPG in place and would also need to rewrite `products.json`
and any hardcoded refs). Expected savings: ~75 % (1 GB → ~250 MB), no
visible quality loss at 82 % JPEG.

**Question for you:** should I run it? It touches ~1,100 files and is
non-trivial to reverse without a git snapshot. If yes, I'll rewrite paths
in `products.json` and rebuild in the same pass.

### 2. Domain verification path for Google Search Console

Three options — the easiest is DNS TXT if you own the domain:

- **DNS TXT (best)** — you add one TXT record to primaxs.com.my's DNS.
  Verifies the whole domain including subdomains and www vs non-www.
- **HTML meta tag** — I add `<meta name="google-site-verification">` to
  `base.html`, you paste the token when you're in Search Console.
- **HTML file upload** — you drop a `googleXXXX.html` file into the root.

**Question for you:** which do you prefer? DNS is the most durable.

### 3. Analytics

Nothing is instrumented. Options:

- **GA4** — free, feature-heavy, some GDPR complexity.
- **Plausible** — paid, tiny script (~1 KB), no cookies, no consent banner
  required. Cleaner for a B2B site.
- **Google Tag Manager** — one shim that can host GA4 plus anything
  else later.

**Question for you:** which one? I can wire any of them in a single edit
to `base.html`.

---

## Google Search Console setup (once you're ready)

1. Go to <https://search.google.com/search-console/>. Sign in with the
   Google account you want to own the property (recommend the workshop
   account, not a personal one — you can add multiple owners after).
2. Click **Add property** → **Domain** → enter `primaxs.com.my`.
3. Copy the TXT record it shows you. Add it to primaxs.com.my's DNS
   (you'll do this at whoever hosts your DNS: MYNIC, Cloudflare,
   GoDaddy — depends on where you registered). Wait ~10 minutes, hit
   **Verify**.
4. Once verified, go to **Sitemaps** in the left nav, paste
   `sitemap.xml`, submit.
5. Under **Enhancements** you'll see Breadcrumbs, Products, FAQ, and
   Sitelinks searchbox reports appear over 1–2 weeks. Under **Experience**
   you'll see Core Web Vitals. Under **Coverage** you'll see how many
   URLs Google has actually indexed.

## Bing Webmaster Tools (do this same day)

ChatGPT Search reads Bing's index — no Bing presence, no ChatGPT
citations. It's 5 minutes:

1. <https://www.bing.com/webmasters/> — sign in.
2. Add site: `https://primaxs.com.my/`.
3. Import from Search Console (Bing lets you do this in one click if you
   verify Google first — saves re-verifying).
4. Submit `https://primaxs.com.my/sitemap.xml`.

## Optional: submit sitemap to IndexNow (near-instant crawling)

IndexNow pushes URL changes to Bing (and via Bing → ChatGPT) in seconds
rather than waiting for the next crawl. It's a POST with a shared key.
Nice-to-have — say the word and I'll wire it into `build.py` so every
rebuild fires the update.

---

## What I did NOT change tonight

- No prices anywhere (standing rule).
- No fake reviews, no fake staff photos, no fake awards (standing rule).
- No pricing, no promo popups, no fake urgency (standing rule).
- No URL changes — every existing link still works.
- No third-party JS added.
- No CSS design changes to any page — the visual design you signed off on
  is untouched. All my changes are in the `<head>` (meta, schema) and in
  a new sitemap.xml + robots.txt.

---

## Files created / modified

New:
- `gen_sitemap.py` — sitemap + robots generator
- `SEO_RESEARCH_NOTES.md` — this session's research with citations
- `MORNING_HANDOFF.md` — this file
- `OVERNIGHT_LOG.md` — detailed timestamped log
- `dist/sitemap.xml` — 1,798 URLs
- `dist/robots.txt` — permissive to AI answer bots

Modified:
- `site/build.py` — added `breadcrumb_ld`, `website_ld`,
  `collection_page_ld`, `graph_ld`, `_org_graph_nodes`; enriched
  LocalBusiness with PostalAddress + phone + email; every page type now
  emits the schema its result surface wants; family/variant titles + descs
  disambiguated; guide meta descriptions trimmed.
- `site/templates/family.html` — how-to-choose image `alt` falls back to
  family name + step number if the step has no title.
- `site/content/guides.py` — 5 guide meta descriptions trimmed to ≤ 155
  chars.

---

## To rebuild

```bash
python site/build.py
```

That produces the full 1,799-page site under `dist/`, regenerates
sitemap.xml and robots.txt in the same run.

## To preview locally

```bash
python -m http.server 8765 -d dist
```

then open <http://localhost:8765/>.
