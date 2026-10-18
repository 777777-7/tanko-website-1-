# -*- coding: utf-8 -*-
# Research 18 Oct 2026. GSC (90 days): "esd storage" 103 impressions at position 78.9 and
# "esd box" 33 at 68.0, both landing on the ESD *workbench* guide or the electronics industry page,
# neither of which answers a storage question. The workbench guide's real ranking ("esd workbench
# malaysia", position 8.2) is a different intent, so a storage page does not cannibalise it.
# Product facts from the Tanko pages (18 Oct 2026):
#  - TKI-2 "-9" cabinets: black PP anti-static drawers, surface resistance 10^4-10^6 ohm, drawer
#    outer W100xD220xH52mm, inner W90xD192xH47mm, 10kg. TKI-2405-9 (20 drawers, W460xD230xH310)
#    RM325.35; TKI-2410-9 (40, W475xD230xH650) RM650.70; TKI-2515-9 (75, W580xD230xH940)
#    RM1,156.80; TKI-2515-9M (mobile, 2" PU castors, 210kg) RM1,337.55; TKI-2515D-9 (75, lock,
#    W645xD295xH1000) RM2,578.70; TKI-2515D-9M (lock, 3" castors, 900kg) RM2,916.10.
#  - TKI-83 hanging cases: black PP (anti-static) option in five sizes, 3-10kg; hang on louvred
#    boards, bin hanger optional for perforated boards. No resistance figure is published.
#  - KPQ-4302 / KPQ-4304 (BLACK)(ANTI-STATIC): 420mm steel rail with 4 x TKI-8302 or 3 x TKI-8304,
#    for perforated panels. Price on request.
# Resistance classes follow ANSI/ESD S541 / IEC 61340-5-3 (conductive < 1x10^4 ohm, dissipative
# 1x10^4 to < 1x10^11 ohm, insulative >= 1x10^11 ohm).

ESDA = 'https://www.esda.org/standards/'

GUIDE = dict(
    slug='esd-storage-anti-static-bins-drawers-malaysia',
    title='ESD Storage Malaysia: Anti-Static Bins, Drawers & Cabinets',
    description=('Anti-static storage for Malaysian electronics lines: ESD drawer cabinets rated 10^4 to '
                 '10^6 ohm, hanging bins and lockable parts cabinets, with sizes and prices.'),
    h1='ESD Storage in Malaysia: Anti-Static Drawers, Bins and Parts Cabinets',
    crumb='ESD Storage',
    tag='Buyer\'s Guide',
    about='Anti-static storage for electronic components in Malaysia',
    published='2026-10-18',
    image='/asset3/TKI-2515-9.webp',
    og_image='/feed-img/asset3__TKI-2515-9.jpg',
    image_alt='Tanko TKI-2515-9 parts cabinet with 75 black anti-static drawers',
    caption='TKI-2515-9: a steel cabinet with 75 black anti-static drawers, listed by Tanko at 10^4 to 10^6 ohm surface resistance.',
    lead=('An ESD workstation protects a board while someone is working on it. A lot of the damage '
          'happens before and after: in a cardboard box on a shelf, in a coloured plastic bin that '
          'charges up every time it is pulled out, or in a drawer that was never part of the ESD '
          'control plan. Air-conditioned production rooms in Malaysia dry the air, which makes static '
          'worse. This guide explains what anti-static storage is, what the resistance numbers mean, '
          'and which Tanko storage is made for it.'),
    faqs=[
        ('What is ESD storage?',
         'ESD storage is shelving, drawers, bins and containers made from static-dissipative or '
         'conductive material, so they do not build up a charge and can bleed one away safely. It is '
         'used to hold static-sensitive components such as boards, chips and drives inside and between '
         'ESD protected areas.'),
        ('Are black plastic bins automatically anti-static?',
         'No. Colour says nothing on its own: an ordinary black bin can be just as insulative as a blue '
         'one. A bin is anti-static only if it is made from dissipative or conductive material. Tanko '
         'specifies its black TKI-2-9 drawers at 10^4 to 10^6 ohm surface resistance; check any bin '
         'with a surface resistance meter before it goes into an ESD protected area.'),
        ('What surface resistance should ESD storage have?',
         'Under the ESD Association S541 classification, dissipative materials measure from 1 x 10^4 to '
         'below 1 x 10^11 ohm and conductive materials below 1 x 10^4 ohm; anything at 1 x 10^11 ohm or '
         'more is insulative. Your ESD control plan sets the exact limits, so specify storage against it.'),
        ('Can anti-static bins hang on a perforated board?',
         'Yes. Tanko TKI-83 hanging bins come in a black anti-static version in five sizes and hang on '
         'louvred boards, or on perforated boards with the optional bin hanger. The KPQ-4302 and KPQ-4304 '
         'sets put four or three anti-static bins on a 420mm rail for perforated panels.'),
        ('Do you deliver ESD storage across Malaysia?',
         'Yes. Delivery and installation are free in Selangor and Kuala Lumpur; outstation delivery, '
         'including Penang, Kedah and Johor, is quoted separately. A 1-year warranty against manufacturing '
         'defects is handled from our Selangor office.'),
    ],
    ranges=[
        ('/parts-cabinet/tki-2/', 'TKI-2 parts cabinets', 'the "-9" versions have black anti-static drawers, from RM325.35 for 20 drawers'),
        ('/parts-cabinet/tki-83/', 'TKI-83 hanging bins', 'five sizes, black anti-static option, for louvred and perforated boards'),
        ('/perforated-board/kpq-4301/', 'KPQ hanging bin sets', 'KPQ-4302 and KPQ-4304 anti-static sets on a 420mm rail'),
        ('/perforated-board/kh-3/', 'Louvred board', 'KH-306A for hanging bins, RM289.20'),
        ('/workstation/', 'Modular workstations', 'build ESD stations around the storage, RM927.85 to RM14,954'),
    ],
    sources=[
        'Tanko product pages for the <a href="/parts-cabinet/tki-2/">TKI-2 cabinets</a>, <a href="/parts-cabinet/tki-83/">TKI-83 hanging bins</a> and <a href="/perforated-board/kpq-4301/">KPQ hanging bin sets</a> (dimensions, loads, surface resistance and guide prices)',
        'ESD Association: <a href="%s" rel="noopener" target="_blank">standards, including ANSI/ESD S541 for packaging materials</a>' % ESDA,
        'Related: <a href="/guides/esd-anti-static-workbench-malaysia/">ESD and anti-static workbenches</a>, <a href="/industries/electronics-manufacturing/">electronics manufacturing</a> and the <a href="/guides/data-centre-fit-out-workbenches-spares-storage-malaysia/">data centre fit-out guide</a>',
    ],
    body='''
<div class="callout"><p><strong>Direct answer:</strong> ESD storage is storage made from static-dissipative or conductive material, so components do not pick up a charge between workstations. For small parts, the Tanko TKI-2 "-9" cabinets have black anti-static drawers listed at 10<sup>4</sup> to 10<sup>6</sup> ohm, from RM325.35 for 20 drawers to RM1,156.80 for 75. For line-side bins, the TKI-83 hanging bins and KPQ-4302/4304 sets come in a black anti-static version for louvred and perforated boards.</p></div>

<h2>Why storage is part of ESD control</h2>
<p>A static-sensitive part spends far more time in storage and in transit than it does on the bench. Ordinary plastic bins and drawers are insulative: every time one slides out of a cabinet or is set down on another, friction builds a charge on it, and that charge has nowhere to go. A component dropped into it, or a hand reaching in, can discharge through the part. Low humidity makes this worse, which is why air-conditioned assembly and test rooms in Malaysia need storage that is part of the ESD control plan, not left out of it.</p>

<h2>What the resistance numbers mean</h2>
<table>
  <thead><tr><th>Class</th><th>Surface resistance</th><th>What it does</th></tr></thead>
  <tbody>
    <tr><td>Conductive</td><td>below 1 x 10<sup>4</sup> ohm</td><td>Moves charge quickly; suits shielding and grounded surfaces</td></tr>
    <tr><td>Dissipative</td><td>1 x 10<sup>4</sup> to below 1 x 10<sup>11</sup> ohm</td><td>Bleeds charge away slowly and safely; the usual target for bins, drawers and work surfaces</td></tr>
    <tr><td>Insulative</td><td>1 x 10<sup>11</sup> ohm and above</td><td>Holds charge; keep it out of an ESD protected area</td></tr>
  </tbody>
</table>
<p>These classes follow the ESD Association's S541 packaging standard. Tanko lists the black TKI-2-9 drawers at 10<sup>4</sup> to 10<sup>6</sup> ohm, at the low end of the dissipative range. Your own ESD control plan sets the exact limits for your site, so specify against it and check with a surface resistance meter when the storage arrives.</p>

<h2>Tanko anti-static storage at a glance</h2>
<table>
  <thead><tr><th>Model</th><th>What it is</th><th>Size</th><th>Guide price</th></tr></thead>
  <tbody>
    <tr><td>TKI-2405-9</td><td>20 anti-static drawers</td><td>W460 x D230 x H310mm</td><td>RM325.35</td></tr>
    <tr><td>TKI-2410-9</td><td>40 anti-static drawers</td><td>W475 x D230 x H650mm</td><td>RM650.70</td></tr>
    <tr><td>TKI-2515-9</td><td>75 anti-static drawers</td><td>W580 x D230 x H940mm</td><td>RM1,156.80</td></tr>
    <tr><td>TKI-2515-9M</td><td>75 drawers on 2" castors (210kg)</td><td>mobile</td><td>RM1,337.55</td></tr>
    <tr><td>TKI-2515D-9</td><td>75 drawers, lockable door</td><td>W645 x D295 x H1000mm</td><td>RM2,578.70</td></tr>
    <tr><td>TKI-2515D-9M</td><td>75 drawers, lockable, on 3" castors (900kg)</td><td>mobile</td><td>RM2,916.10</td></tr>
    <tr><td>TKI-83 (black)</td><td>Anti-static hanging bin, five sizes, 3 to 10kg</td><td>105 x 110 x 50 to 140 x 270 x 125mm</td><td>on request</td></tr>
    <tr><td>KPQ-4302 / KPQ-4304</td><td>420mm rail with 4 or 3 anti-static bins</td><td>for perforated panels</td><td>on request</td></tr>
  </tbody>
</table>
<p>Each TKI-2-9 drawer is W100 x D220 x H52mm outside (W90 x D192 x H47mm inside) and carries 10kg. Tanko does not publish a resistance figure for the black TKI-83 bins, so test them against your control plan before they go into the protected area.</p>

<h2>Where each one fits</h2>
<ul>
  <li><strong>At the bench:</strong> anti-static hanging bins on a louvred or perforated panel above the workstation keep the parts for that station within reach and inside the ESD protected area.</li>
  <li><strong>In the component store:</strong> a TKI-2515-9 gives 75 labelled anti-static drawers in under 0.6m of wall.</li>
  <li><strong>For kitting and line feeding:</strong> the mobile TKI-2515-9M moves a full set of parts to the line on castors.</li>
  <li><strong>For high-value parts:</strong> the lockable TKI-2515D-9 keeps drives, boards and programmed chips behind a door.</li>
</ul>

<h2>Setting it up so it works</h2>
<ol>
  <li>Keep ESD storage inside the ESD protected area and keep ordinary bins, cardboard and bubble wrap out of it.</li>
  <li>Stand cabinets and hang bins on grounded ESD work surfaces or panels, so charge has a path to ground.</li>
  <li>Label the drawers and bins as ESD storage, so nobody tops them up with ordinary containers.</li>
  <li>Test surface resistance when the storage arrives and at the intervals your control plan sets.</li>
</ol>

<h2>What to send for a quotation</h2>
<p>Tell us the components you store (size and rough quantities), how many workstations need line-side bins, whether parts must be locked away, and the delivery address. We reply with a layout and a written Ringgit quotation. Delivery and installation are free in Selangor and Kuala Lumpur; outstation delivery is itemised on the quotation.</p>

<div class="callout"><p><strong>Pricing note:</strong> Prices are Ringgit guide prices from the model pages; hanging bins and sets are quoted on request. <a href="/enquiry/">Send us your parts list</a> for a quotation.</p></div>
''',
)
