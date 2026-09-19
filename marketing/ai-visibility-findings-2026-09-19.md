# Why ChatGPT ranks you but shows no map — 19 September 2026

You rank top in ChatGPT for *"where to buy industrial workbench in Malaysia"* but
the location does not show. **I found the cause, and it is not on your website.**

---

## Your site is not the problem

I checked a product page (`/workbench/wa-67a/`) end to end:

| Check | Result |
|---|---|
| `LocalBusiness` schema | **Present** |
| `PostalAddress` with street, locality, postcode, region | **Present** |
| `GeoCoordinates` (3.01217, 101.75234) | **Present** |
| `OpeningHoursSpecification` | **Present** |
| Address in **visible HTML text**, not just JSON-LD | **Present** — full NAP in the footer |
| `robots.txt` | Explicitly allows OAI-SearchBot, ChatGPT-User, GPTBot, PerplexityBot, ClaudeBot, Applebot, Google-Extended and a dozen more |
| `llms.txt` | Present, 8 KB, with company block, address and specification guidance |

**There is nothing meaningful left to fix on the site for AI crawling.** That work
was already done properly. Adding more schema will not make a map appear.

---

## The actual cause

**ChatGPT does not draw location cards from your website.** It draws them from a
places database. ChatGPT's search is built on Bing's index, so the place record
that matters is **Bing Places**, not your JSON-LD.

So I looked you up on Bing Maps. You are listed — **with the wrong address.**

| | Bing has | Your site says |
|---|---|---|
| Street number | **37** Jalan Balakong Jaya 4 | **No. 39**, Jalan Balakong Jaya 4 |
| Locality | **Kampung Malaysia Raya** | **Seri Kembangan** |
| Postcode | 43300 | 43300 |
| Phone | 03-4296 4737 | +60 3-4296 4737 |

**The street number is wrong and the locality is wrong.**

That mismatch is very likely why no clean location card appears. When a places
record disagrees with the authoritative website, the confidence score drops and the
card is suppressed or shown without the map. It also means **anyone using Bing,
Copilot or ChatGPT to navigate to you is being sent to the wrong door.**

---

## What to do, in order of return

### 1. Claim and correct the Bing Places listing — biggest single win

Go to **`www.bingplaces.com`**, claim the listing, fix the street number to **39**
and the locality to **Seri Kembangan**.

**This is the fix for the ChatGPT map problem.** It costs nothing and it is the
only item on this page that directly addresses what you asked.

### 2. Apple Business Connect

**`businessconnect.apple.com`** — free. Feeds Apple Maps and Siri. Your robots.txt
already welcomes Applebot, so the crawl side is ready and the places side is not.

### 3. Check your Google Business Profile address matches exactly

Google is the largest places database and feeds Gemini and Google's AI Overviews.
Confirm it reads **No. 39** and **Seri Kembangan**, character for character.

### 4. Decide on the second phone number

Two numbers appear across the site in roughly equal measure:

- `+60-3-4296-4737` on 235 pages
- `+60-12-616-3088` on 234 pages

Having a mobile alongside a landline is normal and fine. **But every places
listing should carry the same primary number**, and that primary should be the one
that appears first in your schema. Inconsistent phone data across Google, Bing and
Apple weakens all three records.

---

## What I would not bother doing

**Do not add more schema to product pages.** They already carry Product, Offer,
ProductGroup, LocalBusiness, PostalAddress, GeoCoordinates, OpeningHours,
BreadcrumbList and Organization. That is more structured data than almost any
Malaysian competitor, and it is already working — which is exactly why you rank in
ChatGPT in the first place.

**The ranking proves the content side is done. The missing map is a places-data
problem, and places data lives outside your site.**

---

## Honest limits

- I cannot see what ChatGPT shows you — I have no way to query it. This diagnosis
  is from the Bing places record being wrong, which is a sufficient explanation,
  but you should confirm the card appears correctly once the listing is fixed.
- I have not verified the Google Business Profile address today; that needs your
  login.
- Whether the Bing listing can be claimed depends on whether it was auto-generated
  or someone else created it. You will find out at claim time.
