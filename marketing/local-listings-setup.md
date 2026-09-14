# Free local listings — setup steps

The feed is built and live at:

```
https://www.storagesystem.com.my/local-inventory.xml
```

1,517 items, valid XML, every id matched against the primary feed. **It does
nothing until the steps below are done** — all seven are UI work in Google that
I cannot do for you.

---

## ⚠ Read this first — two things that could make the whole thing wrong

### 1. Does your Balakong Jaya premises admit walk-in customers?

Google's policy is unambiguous:

> "You must have a local brick and mortar business location where customers can
> physically visit, view, and purchase the desired item."

If a member of the public can walk in, look at a workbench and buy it, you
qualify. **If it is a warehouse and office that people only visit by
appointment, you do not**, and this whole programme is the wrong tool — don't
set it up.

This is a fact about your business, not a setting. Only you can answer it.

### 2. Is everything really in stock at that address?

The feed declares `in_stock` on all 1,517 items, because that is what your
existing product feed already declares. But a *local* listing makes a stronger
claim than a normal one — it says "this item is available at this building right
now."

Your own site says *"3–7 working days for popular models · 2–4 weeks for
configured or bulk orders"*, which is not the same as 1,517 items sitting in
Balakong.

Google's policy requires accurate inventory data. Two honest options:

- **Trim the feed** to the SKUs you genuinely hold. Tell me which ranges and I
  will filter it.
- **Leave it** if "in stock" fairly describes your normal supply position.

I have deliberately **not** included quantities. The spec makes them optional,
and inventing 1,517 stock counts would be a policy breach. If Google errors on
missing quantity, the fix is real numbers from you, not a guess from me.

---

## The seven steps

**1. Set the store code in Google Business Profile**
More Business Profile settings → Advanced settings → **Store code** → pencil icon

```
PRIMAXS-BALAKONG
```

Type it exactly — it is case-sensitive and must match the feed. Once chosen,
never change it.

⚠️ Set it in that field, **not** via a bulk-upload spreadsheet — uploading a
store code to an existing location creates a duplicate location.

**2. Link Business Profile to Merchant Center**
Merchant Center → Settings → Access and services → Apps and services →
Add service → **Google Business Profile** → select the Balakong store.

Needs **super admin** on the Merchant Center account.

**3. Wait 24 hours.** Location sync is not instant. Uploading before it
completes produces "Invalid store code" even when the code is right.

**4. Opt the primary feed into local**
Settings → Data sources → your `merchant-feed.xml` source → settings →
change usage to **"Use product data for local and online stores"**, and confirm
**free local listings** is enabled as a destination.

Without this the inventory file is ignored.

**5. Add the local inventory source**
Settings → Data sources → Product sources → Supplemental sources →
**Add local inventory** → enter:

```
https://www.storagesystem.com.my/local-inventory.xml
```

Fetch schedule: every 24 hours. **Feed label and content language must match the
primary source.**

**6. Check the error report after the first fetch.** One thing is genuinely
ambiguous in Google's own documentation: the spec page writes availability as
`in_stock` while their example file writes `in stock` with a space. The feed
uses `in_stock`. If the first fetch complains, tell me and I will switch it —
it is a one-line change.

**7. Check for an existing disapproval.** The account may already carry a
*"No online purchasing means"* disapproval from the standard Shopping
destination. That policy does not apply to local listings, but confirm the local
destination is approved rather than assuming it inherited the block.

---

## What NOT to do

**Do not enable the "show your 333 products on the Shopping tab" suggestion in
Search Console.** Standard free listings require a working online checkout, and
Google names *"websites offering only quote requests instead of direct
purchases"* as a disapproval reason. Your feed descriptions literally end
"Request a quote." Enabling it invites a suspension, not traffic.

Local listings are the route that is actually open to you.

---

## What this gets you

Free local listings surface on Search, Maps, Images, Lens and the Shopping tab
— as **"In stock at Primaxs, Seri Kembangan"**. For a supplier whose buyers are
in Selangor and KL, that is the most relevant placement Google offers, and it
costs nothing.

Rebuild the feed any time with:

```bash
python marketing/build_local_inventory.py --apply
```
