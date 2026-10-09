# Products showing a made-up RM1,500 price (found 9 Oct 2026)

`site/build.py` (around line 2127) gives any product with no price data, and no priced siblings, a
default `_pmyr = 1500` "so every product has a price for SEO". That RM1,500 is shown on the page and
sent to Google in Product structured data (and so to Merchant listings) as if it were real.

**Nothing has been changed.** Wei Ming's standing rule is that pricing is not touched unless he asks.
Options, his call:

1. Give these 41 SKUs their real Tanko prices (best: they then rank in Shopping tiles honestly).
2. Treat them like the other unpriced items: drop the price and show "price on request".
3. Leave as is (risk: a buyer quotes RM1,500 back at us, and Google may flag price mismatches).

| Family | Product pages |
|---|---|
| `cnc-tool/ea-12n` | [ea-12031-111n](https://www.storagesystem.com.my/cnc-tool/ea-12n/ea-12031-111n/), [ea-12031-333n](https://www.storagesystem.com.my/cnc-tool/ea-12n/ea-12031-333n/), [ea-12041-666n](https://www.storagesystem.com.my/cnc-tool/ea-12n/ea-12041-666n/), [eb-12031-111n](https://www.storagesystem.com.my/cnc-tool/ea-12n/eb-12031-111n/), [eb-12031-333n](https://www.storagesystem.com.my/cnc-tool/ea-12n/eb-12031-333n/), [eb-12041-666n](https://www.storagesystem.com.my/cnc-tool/ea-12n/eb-12041-666n/), [ed-12031-111n](https://www.storagesystem.com.my/cnc-tool/ea-12n/ed-12031-111n/), [ed-12031-333n](https://www.storagesystem.com.my/cnc-tool/ea-12n/ed-12031-333n/), [ed-12041-666n](https://www.storagesystem.com.my/cnc-tool/ea-12n/ed-12041-666n/) |
| `household-items/haa` | [haa-715w](https://www.storagesystem.com.my/household-items/haa/haa-715w/), [haa-915w](https://www.storagesystem.com.my/household-items/haa/haa-915w/) |
| `locker/locker-white` | [fba-202aw](https://www.storagesystem.com.my/locker/locker-white/fba-202aw/), [fba-204aw](https://www.storagesystem.com.my/locker/locker-white/fba-204aw/) |
| `perforated-board/te_211` | [te-211](https://www.storagesystem.com.my/perforated-board/te_211/te-211/) |
| `rack/me` | [me-321](https://www.storagesystem.com.my/rack/me/me-321/), [me-322](https://www.storagesystem.com.my/rack/me/me-322/) |
| `tool-cabinet/ekk-1m` | [ekk-1m](https://www.storagesystem.com.my/tool-cabinet/ekk-1m/ekk-1m/) |
| `workbench/wd-4ms` | [ws-48ms](https://www.storagesystem.com.my/workbench/wd-4ms/ws-48ms/) |
| `workbench/wkt_5102` | [wkt-5102f1](https://www.storagesystem.com.my/workbench/wkt_5102/wkt-5102f1/), [wkt-5102f1wpk-21](https://www.storagesystem.com.my/workbench/wkt_5102/wkt-5102f1wpk-21/), [wkt-5102f](https://www.storagesystem.com.my/workbench/wkt_5102/wkt-5102f/), [wkt-5102w1](https://www.storagesystem.com.my/workbench/wkt_5102/wkt-5102w1/), [wkt-5102w1wpk-21](https://www.storagesystem.com.my/workbench/wkt_5102/wkt-5102w1wpk-21/), [wkt-5102w](https://www.storagesystem.com.my/workbench/wkt_5102/wkt-5102w/) |
| `workbench/wp-51` | [wp511024](https://www.storagesystem.com.my/workbench/wp-51/wp511024/), [wp511024a](https://www.storagesystem.com.my/workbench/wp-51/wp511024a/), [wp511025](https://www.storagesystem.com.my/workbench/wp-51/wp511025/), [wp511025a](https://www.storagesystem.com.my/workbench/wp-51/wp511025a/), [wp511026](https://www.storagesystem.com.my/workbench/wp-51/wp511026/), [wp511026a](https://www.storagesystem.com.my/workbench/wp-51/wp511026a/), [wp511028](https://www.storagesystem.com.my/workbench/wp-51/wp511028/), [wp511028a](https://www.storagesystem.com.my/workbench/wp-51/wp511028a/) |
| `workbench/wp-53` | [wp53100-100](https://www.storagesystem.com.my/workbench/wp-53/wp53100-100/), [wp53100-120](https://www.storagesystem.com.my/workbench/wp-53/wp53100-120/), [wp53100-140](https://www.storagesystem.com.my/workbench/wp-53/wp53100-140/), [wp53100-160](https://www.storagesystem.com.my/workbench/wp-53/wp53100-160/), [wp53100-180](https://www.storagesystem.com.my/workbench/wp-53/wp53100-180/), [wp53101-120](https://www.storagesystem.com.my/workbench/wp-53/wp53101-120/), [wp53101-140](https://www.storagesystem.com.my/workbench/wp-53/wp53101-140/), [wp53101-160](https://www.storagesystem.com.my/workbench/wp-53/wp53101-160/), [wp53118-001](https://www.storagesystem.com.my/workbench/wp-53/wp53118-001/) |

Total: 41 pages.
