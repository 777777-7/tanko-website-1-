# The LinkedIn introduction message — rewritten

Wei Ming's feedback on the first version was right: **it read as a specification
dump, not an introduction.** Nobody reads a wall of load ratings from someone they
have not met.

---

## The image problem solves itself

**Every product and category page on the site carries its own `og:image`.** I
checked all 1,857 pages: only 4 fall back to the generic logo, and the rest point
at that product's own photo.

**So pasting a product link into a LinkedIn message automatically shows that
product's picture as a preview card.** No attachment needed, and it looks less like
spam than a bare image.

**The trick is to link a specific product or category page, not the bare domain.**
`storagesystem.com.my` shows the logo. `storagesystem.com.my/cnc-tool/` shows the
CNC trolley with its fitted BT sockets.

Good links to use, each with a real product photo attached:

| Link | What the preview shows |
|---|---|
| `/cnc-tool/` | CNC trolley, fitted taper sockets |
| `/workbench/` | Industrial workbench |
| `/tool-cabinet/` | Heavy duty tool cabinet |
| `/locker/` | Steel lockers |
| `/perforated-board/` | Tool board panel wall |

---

## The message — introduction first, product second

> Hi [Name], good to be connected.
>
> Quick introduction — I am Wei Ming, Business Development Manager at Primaxs
> Marketing in Seri Kembangan. We are the exclusive Malaysia distributor for Tanko
> Enterprise, a Taiwanese industrial storage maker established in 1975.
>
> We supply Samsung's Malaysian plant, along with machine shops, electronics
> manufacturers and laboratories around the Klang Valley.
>
> What we do: workbenches, tool cabinets, CNC tool storage, steel lockers and
> racking. Made in Taiwan, and we hold stock here in Selangor with our own
> installation crew — so 3 to 7 working days instead of a 6 to 9 week import.
>
> Some examples here: https://www.storagesystem.com.my/cnc-tool/
>
> If storage ever comes up on your side, I would be glad to help — no obligation.
>
> Wei Ming
> +60 11-5841 9886

**Roughly 150 words instead of 300.** One link, which carries a product photo
automatically.

---

## Why this version is better

**It opens with who he is, not what he sells.** "Quick introduction" sets the
expectation that nothing is being demanded.

**Samsung sits in the second line, plainly, without being the whole pitch.**
Permission to name them is confirmed, so it is stated as fact and then left alone.

**Three specification points, not ten.** Made in Taiwan, local stock, own install
crew. The rest belongs on the website, which is one click away.

**It ends with an exit.** *"No obligation"* is what makes a cold message feel like
a person rather than a campaign, and it costs nothing.

**What was cut:** the 2,000 kg UDL figure, 304 stainless, ESD tops, the full
BT/HSK socket list, warranty terms, delivery pricing, the SKU count. **All of it is
true and none of it belongs in a first message.** Save it for the reply.

---

## Attaching real images

LinkedIn does not accept a programmatic image upload — this was already logged from
the post composer and applies to messages too. **Wei Ming has to pick the file
himself** if he wants photos attached rather than a link preview.

Four prepared for that: the EA-10031-111MN CNC trolley, the WA-67A workbench, the
EA-7042T heavy duty cabinet, and the FBB-202 locker.

**In most cases the link preview is enough** and is less effort.

---

## A limit worth knowing

**LinkedIn throttles.** After two messages and one connection invite in quick
succession, the message composer stopped opening on the next profile — three
attempts, no dialog. That is the platform slowing things down.

**The right response is to stop, not to keep clicking.** Persisting is what turns
throttling into a restriction. A handful of messages per session, spread out, is
the sustainable pace.

---

# Confirmed in practice — 20 September 2026

## The link preview is the image. Settled.

Sending to Harvinderpal Singh rendered a card in the thread reading
**"Industrial Workbenches Malaysia — from RM904 | storagesystem.com.my"**, with the
product photo.

**No attachment is needed on LinkedIn, and none is possible.** I checked the DOM
inside an open composer: there are **zero `input[type=file]` elements**. LinkedIn
creates one only at the moment you click the image button, and that click opens a
native Windows file dialog which cannot be seen or controlled, and which freezes
the whole browser until dismissed. Do not click it.

**Facebook is the opposite** — its file input exists in the DOM and accepts a
programmatic upload. Open the composer, find the input, upload to it. Never click
Facebook's 照片/视频 button either, for the same native-dialog reason.

## Wei Ming's correction: no delivery or lead-time claims

He asked for these removed from outreach on 20 Sep. **Cut from all messages:**

- "3 to 7 working days rather than a 6 to 9 week import"
- "free delivery and installation within Selangor and KL"
- "our own installation crew"

**Keep:** who he is, exclusive Tanko distributor since 1975, Samsung, the product
list, made in Taiwan, stock held in Selangor, the link, and the exit line.

The commercial offer still belongs in **promotional posts** — see
[[project-commercial-offer]]. This restriction is for one-to-one outreach only,
where a lead-time promise to a stranger is a commitment he may not want to make
before seeing the requirement.

## LinkedIn throttles at roughly four messages

Tonight: two messages, then an InMail, then one more — and the composer stopped
opening. Same pattern as the previous session, which stalled after two messages
and an invite.

**Four per session, then stop.** Persisting is what converts throttling into a
restriction, and this is the account that carries his professional identity.

## Premium Business is active

Renews 20 October 2026, so the free month runs until then. **15 InMail credits per
month, 14 remaining.** InMail reaches 3rd-degree people directly, which is what
made the BAC plant manager reachable at all.

**Screen out "Open to work" before spending anything.** Three of the first five
prospects found were job-hunting, including a BASF Facilities Manager and a
Nexperia engineer. Someone leaving is not a champion and will not be there when a
fit-out lands.
