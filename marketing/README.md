# marketing/

Campaign assets for Primaxs. Version-controlled so they stay findable and
edits are tracked.

## What's here

| File | What it is | How to use it |
|---|---|---|
| `google-ads-keywords.csv` | 96 keywords, 6 campaigns, 17 ad groups, each mapped to a real landing page | Import into Google Ads Editor |
| `google-ads-ads.csv` | 17 responsive search ads, validated against Google's 30/90/15 character limits | Import into Google Ads Editor |
| `google-ads-negatives.csv` | 49 campaign-level negatives × 6 campaigns | Import into Google Ads Editor |
| `linkedin-pack.md` | Profile copy, company page copy, 24 posts, connection notes | Copy-paste. One blank: your job title |
| `directory-listings.md` | Canonical NAP block, 3 description lengths, 8 submission targets | Copy-paste per directory |

## Google Ads — import order

Google Ads Editor, **Account → Import → From file**, in this order:

1. `google-ads-keywords.csv` — creates campaigns, ad groups and keywords
2. `google-ads-ads.csv` — adds the responsive search ads
3. `google-ads-negatives.csv` — adds campaign negatives

Then, before posting changes:

- Set campaign budgets (RM3,000/month total is the researched starting point;
  industrial supplies benchmarks around **RM240 cost per lead** in Malaysia,
  the cheapest B2B category)
- Set location targeting to **Malaysia**, and set "people in your targeted
  locations" rather than the default which includes people merely interested
- Set language targeting to **English and Malay**
- Add call extensions: office `+60 3-4296 4737`, mobile `+60 12-616 3088`
- Add sitelinks pointing at `/enquiry/`, `/guides/`, `/products/`, `/about/`
- Import conversions from the `/sales/` Supabase dashboard: `email_submit`
  and `whatsapp_send`

### Campaign structure

| Campaign | Ad groups | Targets |
|---|---|---|
| `MY-Search-Workbench` | Generic, Heavy Duty, ESD, Stainless | 955 workbench pages |
| `MY-Search-ToolCabinet` | Generic, Roller Trolley | 238 tool cabinet pages |
| `MY-Search-CNC` | CNC Tool Storage | 103 CNC pages, most differentiated product |
| `MY-Search-Storage` | Lockers, Racking, Parts, Pegboard, Workstations | Remaining ranges |
| `MY-Search-BM` | Meja Kerja, Kabinet Alat, Loker & Rak | Bahasa Malaysia — no competitor bids on these |
| `MY-Search-Geo` | Klang Valley, Johor Penang | Location-qualified intent |

The Bahasa campaign is the one to watch. Malaysian competitors are almost all
bidding English-only, so CPCs there should be meaningfully lower, and the
traffic lands on the ten Bahasa guides now live on the site.

## Not started, and why

- **Directory submissions** — every one needs an account created. I can't
  create accounts, so the copy is staged instead.
- **LinkedIn posting** — the account is a blank student profile with 0
  connections. Posting reaches nobody until the profile is fixed and a network
  exists. See the warning at the top of `linkedin-pack.md` about invite rate
  limits; bulk-inviting from a new account gets it restricted.
- **Google Ads going live** — costs money. CSVs are ready; switching them on
  is your call.
