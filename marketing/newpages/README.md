# NEWPAGES listing — saved, waiting on the SSM certificate

**Status: everything filled, blocked only on the SSM certificate PDF.**

NEWPAGES has no draft-save, so the live form state will be lost as soon as that
browser tab is closed or reloaded. Everything is recorded here instead. When the
SSM certificate exists, the whole form can be re-filled in about a minute.

---

## Why this listing matters

NEWPAGES-built sites dominate Malaysian industrial search results — the ones with
`index.php?ws=ourproducts&cid=` in the URL. Knight Auto (**Seri Kembangan, the
same town**), Alliance Supplies, SP Tools, Sui U Machinery and Mr. Mark Tools all
rank through it.

Primaxs already has a listing at **`newpages.com.my/company/93368`** and it is
unclaimed, has **the wrong address**, and no website link:

> BL 10, Jalan Maju 2/1, Taman Lembah Maju, Kuala Lumpur, Wilayah Persekutuan

A wrong Name-Address-Phone citation is worse than no citation. Google reads
mismatches across directories as a signal it cannot verify the business, and that
directly weakens local ranking. **This is a fix, not just an addition.**

---

## The URL — this part is fiddly

```
https://m.newpages.com.my/en/93368/business-listing.html
```

- The `www` version of that path **404s**. The claim form only exists on the `m.` subdomain.
- Logged out, it redirects to login. Logged out on `m.`, it silently bounces to the homepage.
- **Must be logged in, and must be the `m.` URL.**

Reach it from the listing page (`m.newpages.com.my/en/company/93368/...`) via
either **"Claim this Business"** or **"[Claim & Update]"** — both go to the same
form.

---

## Every field, paste-ready

| Field | Value |
|---|---|
| Company Name | `Primaxs Marketing (M) Sdn Bhd` |
| Company Registered No. | `200601036829 (756588-H)` |
| Company Address | `No. 39, Jalan Balakong Jaya 4, Taman Industri Balakong Jaya, 43300 Seri Kembangan, Selangor` |
| Location | `Selangor` |
| Latitude | `3.01217` |
| Longitude | `101.75234` |
| Email | `sales@storagesystem.my` |
| Tel | `+60 3-4296 4737` |
| Phone Number | `+60 12-616 3088` |
| Fax | *(leave blank)* |
| Website | `https://www.storagesystem.com.my` |
| Facebook Page Url | `https://www.facebook.com/primaxsmarketing` |
| Company Logo | `marketing/newpages/logo-800x800.png` |
| Company Banner | `marketing/newpages/banner-860x360.png` |
| **SSM Document (.pdf)** | **MISSING — the only blocker** |

### Business Type (160-character cap — this is 154)

```
Industrial Storage Equipment Distributor - Workbenches, Tool Cabinets, CNC Tool Storage, Steel Lockers, Warehouse Racking, Workstations, Perforated Boards
```

### Products/Services

```
Primaxs Marketing (M) Sdn Bhd is the exclusive Malaysia distributor for Tanko Enterprise Co., Ltd. (Taiwan, established 1975). We supply approximately 1,700 SKUs across 11 ranges: industrial workbenches in medium and heavy duty specifications; tool cabinets and roller trolleys; CNC tool storage fitted for BT-30, BT-40, BT-50, HSK-40, HSK-63 and ISO holders; modular workstations; steel lockers; parts and document cabinets; warehouse racking; mould racks; and perforated boards with hooks and hangers.

Stock is held in Selangor for popular configurations, with 3 to 7 working day delivery in the Klang Valley and nationwide delivery across Peninsular Malaysia, Sabah and Sarawak. All quotations are issued in Malaysian Ringgit with unit pricing, project pricing and delivery costs itemised separately. Delivery and installation are free within Selangor and the Klang Valley; outstation delivery is quoted separately. The manufacturer warranty against manufacturing defects runs 1 year and is administered locally from our Selangor office.

We supply manufacturing plants, automotive workshops, CNC machining shops, laboratories and cleanrooms, electronics and EMS facilities, food and pharmaceutical production, warehouses, schools, campuses and technical training centres across Malaysia.
```

---

## Business Classified — the free tier caps at 4

The counter reads **"Business Classified 4/4"** and a fifth tick is silently
refused. These four were chosen deliberately:

| ID | Category | Existing listings | Why |
|---|---|---|---|
| **1827** | Storage System (存储系统) | 16 | Exact fit, and a tiny category — the easiest #1 on the whole platform |
| **608** | Hardware (五金) | 357 | Biggest hardware category; where hardware shops browse |
| **1860** | Industrial Equipment (工业设备) | 175 | The main industrial category |
| **1226** | Material Handling Equipment (物料搬运设备) | 57 | Reaches the warehouse and racking buyer — a segment the other three miss |

**Dropped:** `640` Industrial Equipment & Supplies (duplicated 1860).
**Next best if the mix should change later:** `256` Office Furniture (161) and
`1679` Cabinet (227) — worth swapping in if lockers and document cabinets grow as
a share of sales.

---

## The blocker, and where to get it

**SSM Document (.pdf)** is marked required with a red asterisk. It wants the
registration certificate itself, not the number.

Where to get it:

- **MyData SSM** — `mydata-ssm.com.my`. A company profile / e-Info printout is a
  few Ringgit and downloads as a PDF immediately. This is the fastest route.
- Or the **Section 17 certificate** (formerly Form 9) from incorporation, if
  there's a copy in the company files.

There is also a **reCAPTCHA** directly above Submit. That always has to be a
person.

---

## When the certificate is ready

1. Log in to NEWPAGES.
2. Open `https://m.newpages.com.my/en/93368/business-listing.html`.
3. Say the word and the whole form gets re-filled from this file in about a minute
   — text fields, location, GPS, logo, banner and all four categories.
4. Attach the PDF, tick the CAPTCHA, Submit.

---

## Notes for next time

- **Business Hours are a paid feature.** The entire block (`chkday1..7`,
  `from1-N`, `to1-N`) has `disabled: true` on the free tier — the listing is
  badged "Advanced" at the top. Not worth paying for.
- The logo field demands **1:1**; the stock Primaxs logo is 660×378, so
  `logo-800x800.png` here is a padded square build of it.
- The banner wants **860×360**; `banner-860x360.png` is a centre crop of the
  site's OG image.
- The listing already had the correct phone (`03-4296 4737`). It is only the
  address, website, description and categories that were wrong or missing.
