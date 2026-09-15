# Why competitors outrank us — measured, not guessed

Until today the backlink story was inference. Bing Webmaster Tools reports real
link data for **any** domain, so on 15 September 2026 I pulled ours and two
competitors' side by side. This is the actual gap.

---

## The numbers

| | Referring domains | Links from NEWPAGES | Everything else |
|---|---|---|---|
| **storagesystem.com.my** | **2** | **90** | aseanbizs.com 5 |
| knightauto.com.my | 11 | **23,900** | newpages.asia 60, newstore.my 45, robuta.com 9, newjobs.com.my 6, alibaba.com 2, mudah.my 1, sourcifychina.com 1, limseonghai.com 1, hardware1000.com 1 |
| jteasia.com | 10 | **1,200** | **onesync.my 440**, newpages.asia 33, jawatankosong.com 8, tendata.com 4, mypages.my 2, robuta.com 2, spmalaysia.com.my 1, glassdoor.at 1, metoree.com 1 |

Two referring domains against their ten and eleven. On the single source we
share, we have 90 links and Knight Auto has **twenty-three thousand nine
hundred**.

This is the whole of the "position 43 on tool cabinets" problem. Our tool
cabinet page is technically better than theirs — the audits say so. Theirs is
better *linked*, by a factor of 265.

---

## How Knight Auto actually got 23,900 links

Read their anchor text and the mechanism is obvious:

| Anchor | Count |
|---|---|
| https://www.knightauto.com.my | 8,700 |
| 在官网查看此产品 (view this product on the official site) | 5,400 |
| Melihat Produk Di Laman Web Rasmi | 5,100 |
| View Product On Official Website | 4,800 |
| Visit Official Site | 24 |
| Knight Auto Sdn Bhd | 14 |

They did not list *the company* on NEWPAGES. They listed **every product**, in
**three languages**, and every one of those listings carries a link back to the
matching product page on their own site.

We have 1,517 product pages. Three languages each is roughly 4,500 listings —
the exact shape of their profile. This is not a trick and it is not paid links:
it is a supplier directory being used the way it was designed to be used.

**Our anchor text, for comparison:** `https://www.storagesystem.com.my` ×90 and
`PRIMAXS MARKETING (M) SDN BHD` ×5. Two anchors, both bare. **Not one link in
existence describes what we sell.** No "industrial workbench", no "tool cabinet
Malaysia", nothing. That is why we rank for the brand and little else.

---

## The other sources, and what each is worth

**onesync.my — 440 links to JTE, 0 to us.** JTE's second-largest source, all
anchored "Official Website". OneSync is a Malaysian web/SEO agency running a
directory network. Worth finding out what a listing costs.

**The NEWPAGES family propagates.** newpages.asia, newstore.my, newjobs.com.my
and mypages.my all appear, and both competitors are on several. One properly
built NEWPAGES presence seeds a small network, which is why their *domain*
count is five times ours off what is substantially one relationship.

**robuta.com appears for both.** A B2B directory neither of us had to pay much
attention to, and both of them are on it and we are not.

**jawatankosong.com 8, newjobs.com.my 6 — job boards.** Posting a genuine
vacancy creates a followed link from a high-authority Malaysian domain. Primaxs
is a real company with real hiring needs; this is the cheapest legitimate link
on the list and nobody has taken it.

**alibaba.com 2, mudah.my 1.** Marketplace presence. Low link value on its own,
but both are places Malaysian buyers actually search.

---

## What this changes about the plan

The honest ranking of effort against return:

1. **NEWPAGES product listings.** One action, correctly done, closes most of a
   265× gap. Everything else on this page is a rounding error next to it.
   Needs Wei Ming's login — I cannot create or sign into accounts.
2. **Descriptive anchor text.** Whatever we build next, the anchor must say
   *industrial workbench Malaysia*, not the bare URL. Zero of our 95 links do.
3. **A job posting.** Real vacancy, real link, no cost.
4. **robuta.com and onesync.my.** Both competitors are there; find the entry
   requirements.

And what it does *not* change: nothing on-page will fix this. The site already
beats all seven competitors on sitemap images, schema types, alt text, AI
crawler access and hreflang. We are not losing on the page. We are losing on
who points at it.

---

*Source: Bing Webmaster Tools → Backlinks → Backlinks To Any Site, 15 Sep 2026.
Bing's index is also what ChatGPT search, Copilot and DuckDuckGo read — and it
currently holds **28** of our 1,847 URLs.*

---

# Addendum — I opened the listings and found the exact gap

The table above says Knight Auto has 23,900 NEWPAGES links and we have 90. That
is the *symptom*. Here is the cause, read off the live pages.

## 1. We have 12 products listed. They have thousands.

Our NEWPAGES company page is **id 93368** (`m.newpages.com.my/en/company/93368/`)
and the copy on it is good — it describes the 11 ranges properly. It lists
**twelve products**.

## 2. Our product listings carry no link to our website at all

I opened our own listing for the KQ-308A perforated board and counted the links
pointing at storagesystem.com.my. **Zero.**

Then I opened a Knight Auto product listing and counted theirs. **Five**, and
none of them carry `rel="nofollow"` — they are followed links that pass value:

| Link text on their product page | Points to |
|---|---|
| **View Product On Official Website** | the matching product page on knightauto.com.my |
| https://www.knightauto.com.my | their homepage |
| https://knightauto.newpages.com.my/ | their NEWPAGES subdomain |
| http://knightauto.n.my/ | their .n.my microsite |

That first one is the anchor that appears 4,800 times in their profile, plus
5,100 in Malay and 5,400 in Chinese. It comes from a **product URL field** on
the listing form. On our twelve listings that field was left blank, so we get
the listing and none of the link.

## 3. We have not claimed either microsite

Knight Auto has `knightauto.n.my` and `knightauto.newpages.com.my`, both live,
both serving their own content, both linked from every product page they own.

I checked ours. `primaxs.n.my`, `primaxsmarketing.n.my` and
`primaxs.newpages.com.my` all resolve to **NEWPAGES' generic landing page** —
nothing is claimed. Two separate indexed sites we are entitled to and do not
have.

---

## What Wei Ming needs to do — in order of return

Everything below needs the NEWPAGES login. I cannot create accounts or sign in.

1. **Fill in the product URL on every existing listing.** Twelve listings, five
   minutes, and each one starts carrying "View Product On Official Website"
   straight to the matching page on our site. Do this first — it is the
   smallest action with a real result, and it proves the field is the cause.
2. **Claim `primaxs.n.my` and `primaxs.newpages.com.my`.** Free with the
   account, and both become separate indexed properties linking to us.
3. **Then add products in bulk, in all three languages.** Ask NEWPAGES whether
   they take a spreadsheet or feed import — with 1,517 SKUs, adding them by
   hand is not realistic, and we already generate a complete product feed at
   `/merchant-feed.xml` with titles, descriptions, images and URLs. If they
   accept a feed, this is one conversation rather than months of typing.
4. **When you add them, set a descriptive product title.** Their anchor text is
   generic because the link text is fixed, but the listing *title* is not:
   "Heavy Duty Industrial Workbench Malaysia - Tanko WB-57F" is how our
   existing twelve are named, and that is exactly right. Keep it.

I have emailed NEWPAGES separately. If they confirm a bulk import, I can
produce the file the same day.

---

# Second addendum — I got into the account, and the wall is commercial

You were already signed in to NEWPAGES, so I went in and read the actual limits
rather than guessing. **This corrects the plan above.**

## What the account says

| | |
|---|---|
| Signed in as | Wong Wei Ming |
| Current tier | free Business Listing |
| Product slots | **15** — twelve used, **three free** |
| NP Points balance | **15** |
| Point price | 10 NP Points per RM 2.00 |
| "Post to Timeline" | **10 NP Points per post** (so the balance buys one) |
| Business Listing **Advanced** | **3,500 NP Points ≈ RM 700** → +18 slots, 33 total, lifetime |
| **Premium Listing** | **MYR 1,980.00** → **unlimited products and timeline posts** |

**That last line is the whole thing.** Knight Auto's 23,900 links are not a
trick we are missing, and not a form field we forgot. They are on the
**Premium tier**, which is the only one that allows unlimited products. On our
tier the ceiling is fifteen. We are at twelve.

So the earlier suggestion — "ask whether they take a feed import for all 1,517
SKUs" — was premature. There is no point asking until the tier allows it.

## What that changes

**The RM1,980 is the decision, and the evidence for it is now on the table.**
Not a vague "we should do more SEO" — a measured 265× link gap against the
competitor beating us on our weakest term, with the mechanism identified and
the price of the mechanism printed on the page.

Judge it as a purchase: 1,517 products × 3 languages on a domain that already
sends Knight Auto 23,900 links, versus one year of the ad spend it replaces.

**What I could not find:** there is no add-product control anywhere in the web
member area — only View, Delete and Post to Timeline on each existing listing,
and no Edit. Product upload appears to happen through their app or their staff.
Worth asking them directly, because it also decides whether 1,500 products is a
bulk import or a data-entry job.

## What I deliberately did not touch

- **I did not spend the NP Points.** The balance has money value and buying a
  timeline post with it is a purchase; that is yours to authorise.
- **I did not delete and re-create any listing.** The twelve have no Edit
  option, so adding the website URL to them may mean deleting and re-adding —
  and if the re-add needs points or approval, deleting first risks losing
  listings that are live and approved today.

## Still free, still worth doing

- **Three unused product slots.** Add the three highest-value SKUs when there is
  a way to add them.
- The company listing itself is already complete — website, Facebook page,
  phone, address, business type, 255-character service description and full
  opening hours are all filled in correctly. Nothing to fix there.
