# Google Merchant Center — free product listings

**File: [`google-merchant-feed.tsv`](google-merchant-feed.tsv) — 1,591 products, ready to upload.**

Free listings put Primaxs products on Google Search, Google Images, the Shopping
tab, Google Maps and Google Lens at no cost. Malaysia is a supported country.
The Shopping Graph passed 60 billion listings in May 2026, and none of those
placements are billed.

This costs nothing and is not Google Ads. Ads can be switched on later off the
same feed if Wei Ming decides to; the keyword and ad CSVs are already in this
folder.

---

## Where the data came from

Nothing was invented. Every row is an export of the `Product` JSON-LD already
published on the product pages, joined against `products.json` for the specs:

| Feed column | Source |
|---|---|
| `id`, `mpn` | SKU |
| `title` | Product name from the page schema |
| `description` | Rebuilt from real dimensions, material, load capacity and colour, plus the standard Primaxs terms |
| `link` | The canonical product URL |
| `image_link`, `additional_image_link` | The product images already on the site |
| `price` | The guide price already published in the page schema, in MYR |
| `brand` | Tanko |
| `google_product_category` | Mapped by category — Work Benches 503739, Tool Cabinets 4207, Lockers 4163, Shelving 5197, File Cabinets 448 |
| `shipping` | `MY::Selangor and Klang Valley:0 MYR` — free delivery in the home region, stated as a real shipping rule |

`identifier_exists` is set to `no` because these are industrial SKUs without
GTINs. That is the correct value, not a workaround — brand plus MPN is what
Google expects for this class of product.

**Coverage:** 1,591 of 1,761 SKUs. The 170 excluded are the ones with no
published price or no image; they are skipped rather than guessed at.

```
Workbenches            893      Perforated Boards      113
Tool Cabinets          219      CNC Tool Storage        90
Modular Workstations    86      Parts Cabinets          71
Hanger Racks            59      Documents Cabinets      28
Lockers                 20      Racks                   10
```

---

## How to upload it

1. Go to **merchantcenter.google.com** and sign in with the account that owns the
   Google Business Profile.
2. Create the account if there is not one: business name **Primaxs Marketing (M)
   Sdn Bhd**, website **https://www.storagesystem.com.my**, country **Malaysia**,
   currency **MYR**.
3. **Verify and claim the website.** The fastest route is Google Search Console
   if the domain is already verified there; otherwise Merchant Center will offer
   an HTML tag or file, which can be added to the site.
4. **Products → Feeds → Add feed.** Country Malaysia, language English,
   destination **Free listings** (add Shopping ads later only if wanted).
5. Choose **Upload** as the method, name it `primaxs-main`, and upload
   `google-merchant-feed.tsv`.
6. Wait for processing. Expect warnings, not errors — the common ones are
   "missing GTIN" (expected here, `identifier_exists: no` covers it) and image
   quality notes.
7. Under **Growth → Manage programmes**, confirm **Free listings** is switched on.

Initial review usually takes 3–5 working days.

---

## Keeping it current

The feed is generated, not hand-maintained. Re-run the generator whenever prices
or the catalogue change, then re-upload. A monthly refresh is enough — Merchant
Center expires items after 30 days without an update, so **do not let it go
stale**, or the listings quietly disappear.

The alternative is to host the file at a stable URL and let Merchant Center fetch
it on a schedule, which removes the manual step entirely. Worth doing once the
first upload is confirmed working.

---

## The one judgement call in here

The published guide prices go into a Google-wide shopping surface, where
competitors can read them as easily as customers can.

That is a genuine trade-off and it is Wei Ming's call, not a technical decision.
The counter-argument is that the prices are **already public on the website**, so
the exposure is not new — and buyers who can see a price qualify themselves
before they call, which raises the quality of enquiries rather than the quantity.
If the preference is to keep pricing off Google entirely, the feed simply does
not get uploaded, and nothing else in the plan changes.
