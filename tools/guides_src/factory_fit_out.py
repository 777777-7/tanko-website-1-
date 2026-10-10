# -*- coding: utf-8 -*-
# Research 10 Oct 2026. Why this page: MIDA approved 973 manufacturing projects in 1H 2026
# (+88% y/y, The Edge) and Penang alone RM17.3bil (The Star); named projects being fitted out
# now include E&R Engineering (Melaka FTZ, opening 13 Oct), PEN SJ Electronics (Batu Kawan
# BKIP3), SkyGate NHJ (Perai) and MKS Instruments (Bandar Cassia). Nobody in Malaysia publishes
# a storage-and-workstation fit-out checklist for a new plant; the facilities and project
# managers doing it are the buyers we want. Doubles as the outreach asset in
# marketing/target-accounts-oct-2026.md.
# Facts: prices are the lowest published guide price per range in docs/ on 10 Oct 2026
# (workbench seating excluded); lead times are the ones printed on every product page;
# Act 446 locker size from the steel locker guide (Skrine alert, Sep 2020).

MIDA = ('https://www.mida.gov.my/media-release/malaysia-secures-rm218-5-billion-in-approved-'
        'investments-in-1h-2026-with-domestic-investment-in-manufacturing-up-23/')
EDGE = 'https://theedgemalaysia.com/node/816173'
STAR = ('https://www.thestar.com.my/news/nation/2026/09/03/'
        'penang-manufacturing-investments-jump-38-to-rm173bil-in-1h2026')
SKRINE = ('https://www.skrine.com/insights/alerts/september-2020/'
          'workers%E2%80%99-accommodation-standards-updated')
DOSH = ('https://dosh.gov.my/wp-content/uploads/2025/01/GUIDELINES-ON-OCCUPATIONAL-SAFETY-AND-'
        'HEALTH-FOR-STANDING-AT-WORK-2024.pdf')

GUIDE = dict(
    slug='new-factory-storage-fit-out-checklist-malaysia',
    title='New Factory Fit-Out Checklist Malaysia: Storage & Benches',
    description=('Fitting out a new plant in Malaysia? Which workbenches, tool storage, spares '
                 'cabinets and lockers to order, in what order, with lead times and the Act 446 rule.'),
    h1='Fitting Out a New Factory in Malaysia: The Storage and Workstation Checklist',
    crumb='New Factory Fit-Out Checklist',
    tag='Buyer\'s Guide',
    about='Fitting out a new factory or plant in Malaysia',
    published='2026-10-10',
    image='/asset3/WAT-5203N.webp',
    og_image='/feed-img/asset3__WAT-5203N.jpg',
    image_alt='Tanko WAT-5203N heavy duty workbench with three locking drawers, W1500 x D750 x H800mm',
    caption='The maintenance bench is usually the first thing a new plant needs and the last thing anyone orders.',
    lead=('A new plant is planned around its machines. The workbenches, tool storage, spares cabinets and '
          'lockers around them usually go on the last purchase order of the project, and it shows on '
          'handover day: technicians keep tools in cartons, spares sit in boxes on the floor, and the '
          'hostel has no lockers when the first workers move in. In the first half of 2026 MIDA approved '
          '973 manufacturing projects, 88% more than a year earlier, so a lot of facilities teams are '
          'doing this right now. This checklist covers what to order for each area, how to count it, and '
          'when to order so it is installed before production starts.'),
    faqs=[
        ('What storage and furniture does a new factory need?',
         'Plan it area by area: workbenches or modular workstations for the production lines; heavy duty '
         'benches, tool cabinets, trolleys and shadow boards for maintenance and the tool room; parts '
         'cabinets and bins for the spares store; mould racks if you run moulds or dies; stainless or ESD '
         'benches for the QC lab; document cabinets for the production office; multi-door lockers for '
         'changing rooms; and, if you house workers, one compliant locked cupboard per resident under Act 446.'),
        ('How early should we order storage for a new plant?',
         'Work back from the day the first operators start. Popular Tanko models are delivered in 3 to 7 '
         'working days from Selangor stock; configured or bulk orders take 2 to 4 weeks. Add your own '
         'purchase-order approval time and installation, and the counts need to be confirmed about six to '
         'eight weeks before start-up. Hostel lockers have to be in before the workers move in.'),
        ('How many lockers does a factory need?',
         'For changing rooms, count compartments against peak headcount on the largest shift, plus spares '
         'for contractors and new hires. Multi-door banks are the economical choice there. For employer-'
         'provided housing, the Act 446 accommodation regulations require one locked cupboard per worker of '
         'at least 350 x 350 x 900mm inside, which in the Tanko range means the two-door FBA-202W or FBB-202.'),
        ('Do you deliver and install in Penang, Kulim, Johor and Melaka?',
         'Yes. Primaxs delivers across Malaysia, including East Malaysia, and to Singapore. Delivery and '
         'installation are free in Selangor and Kuala Lumpur; outstation delivery is quoted separately and '
         'itemised on the quotation.'),
        ('Can one supplier quote the whole fit-out?',
         'For storage and workstations, yes. Send the floor plan or a list of areas with headcounts, '
         'technician numbers and spares counts, and Primaxs will return one Ringgit quotation covering '
         'benches, tool storage, parts cabinets, racks and lockers, with lead times per item.'),
        ('Where are Tanko products made?',
         'In Taiwan, by Tanko Enterprise Co., Ltd., which has manufactured industrial storage since 1975. '
         'Primaxs Marketing (M) Sdn Bhd has been the exclusive Malaysia distributor since 2006, holds stock '
         'in Selangor and handles the 1-year warranty against manufacturing defects locally.'),
    ],
    ranges=[
        ('/workbench/', 'Industrial workbenches', 'Performance from RM903.75, heavy duty (2,000kg frames) from RM2,385.90'),
        ('/workstation/', 'Modular workstations', 'line-side and assembly stations from RM927.85'),
        ('/tool-cabinet/', 'Tool cabinets, chests and trolleys', 'from RM1,024.25'),
        ('/perforated-board/', 'Steel perforated boards', 'for shadow boards and tool display, from RM168.70'),
        ('/parts-cabinet/', 'Parts cabinets and bins', 'for the spares store, from RM289.20'),
        ('/rack/', 'Mould racks', 'pull-out levels, from RM9,471.30'),
        ('/documents-cabinet/', 'Document cabinets', 'A4 filing for the production office, from RM216.90'),
        ('/locker/', 'Steel lockers', 'changing-room banks and Act 446 hostel lockers, from RM1,614.70'),
    ],
    sources=[
        'MIDA: <a href="%s" rel="noopener" target="_blank">Malaysia secures RM218.5 billion in approved investments in 1H 2026</a>' % MIDA,
        'The Edge Malaysia: <a href="%s" rel="noopener" target="_blank">data centres and cloud projects make up nearly half of 1H2026 approvals</a> (973 manufacturing projects)' % EDGE,
        'The Star: <a href="%s" rel="noopener" target="_blank">Penang manufacturing investments jump 38%% to RM17.3bil in 1H2026</a>' % STAR,
        'Skrine: <a href="%s" rel="noopener" target="_blank">Workers&rsquo; accommodation standards updated</a> (Act 446 regulations, in force 1 September 2020)' % SKRINE,
        'DOSH Malaysia: <a href="%s" rel="noopener" target="_blank">Guidelines on Occupational Safety and Health for Standing at Work 2024</a> (PDF)' % DOSH,
        'Related: <a href="/guides/industrial-storage-solutions-malaysia/">Industrial storage solutions</a>, <a href="/guides/esd-anti-static-workbench-malaysia/">ESD workbenches</a> and <a href="/guides/steel-locker-buying-guide-malaysia/">steel locker buying guide</a>',
    ],
    body='''
<div class="callout"><p><strong>Direct answer:</strong> List every area of the plant, count what each one needs (stations, technicians, spare-part lines, moulds, staff per shift, hostel residents), and confirm the storage order six to eight weeks before start-up. Configured and bulk orders take 2 to 4 weeks, stocked models 3 to 7 working days, and installation comes after that. Order hostel lockers first: the Act 446 rule requires one locked cupboard per resident, at least 350 x 350 x 900mm inside, before workers move in.</p></div>

<h2>Why storage gets ordered last, and what that costs</h2>
<p>On a plant project the machines have long lead times and a vendor chasing the order, so they get planned first. Storage has no vendor chasing it and looks easy, so it waits. The cost shows up in the first months of production:</p>
<ul>
  <li><strong>Maintenance starts slow.</strong> Without a bench, a tool cabinet and a shadow board, technicians spend the first breakdowns looking for tools rather than fixing machines.</li>
  <li><strong>Spares go missing.</strong> Commissioning spares arrive in cartons. If there is no parts cabinet to receive them into, they are hard to find when the line stops.</li>
  <li><strong>The hostel certificate is at risk.</strong> Employer-provided housing needs a certificate of accommodation from the Labour Department, and the 2020 regulations include a per-worker locker size. Lockers that arrive after the workers do, or the wrong lockers, are a compliance problem.</li>
  <li><strong>Mixed suppliers, mixed standards.</strong> Buying a few benches here and a few cabinets there leaves you with drawers that don&rsquo;t match, colours that don&rsquo;t match, and four warranties to chase.</li>
</ul>

<h2>The checklist, area by area</h2>
<p>Count what each area needs before asking anyone for a price. Prices below are the lowest Ringgit guide price we publish for each range; the quotation is based on the exact models and quantities.</p>
<table>
  <thead><tr><th>Area</th><th>What to order</th><th>Count it by</th><th>Range and guide price</th></tr></thead>
  <tbody>
    <tr><td>Production lines and assembly cells</td><td>Workbenches or modular workstations; seating sized to the bench</td><td>One per station, from the line layout</td><td><a href="/workbench/">Workbenches</a> from RM903.75; <a href="/workstation/">modular workstations</a> from RM927.85</td></tr>
    <tr><td>Maintenance workshop and tool room</td><td>Heavy duty benches, tool cabinets or trolleys, shadow boards</td><td>Technicians per shift and shared bays</td><td>Heavy duty benches from RM2,385.90; <a href="/tool-cabinet/">tool cabinets and trolleys</a> from RM1,024.25; <a href="/perforated-board/">steel perforated boards</a> from RM168.70</td></tr>
    <tr><td>CNC and machining</td><td>Tool holder cabinets and carts</td><td>Holders per machine, by taper (BT or HSK)</td><td><a href="/cnc-tool/">CNC tool storage</a> from RM1,349.60</td></tr>
    <tr><td>Spares store</td><td>Parts cabinets with drawers, bins, louvre panels</td><td>Spare-part lines and their size</td><td><a href="/parts-cabinet/">Parts cabinets</a> from RM289.20; <a href="/hanger-rack/">hanger racks and louvre panels</a> from RM1,012.20</td></tr>
    <tr><td>Mould and die storage</td><td>Pull-out mould racks</td><td>Number of moulds and the heaviest one</td><td><a href="/rack/">Mould racks</a> from RM9,471.30</td></tr>
    <tr><td>QC lab, cleanroom, food areas</td><td>304 stainless or ESD workbenches</td><td>One per test or prep position</td><td>See the <a href="/guides/stainless-steel-workbench-food-pharma-malaysia/">stainless</a> and <a href="/guides/esd-anti-static-workbench-malaysia/">ESD</a> guides</td></tr>
    <tr><td>Production office</td><td>A4 document cabinets and trays</td><td>Files kept on site (batch records, drawings, audits)</td><td><a href="/documents-cabinet/">Document cabinets</a> from RM216.90</td></tr>
    <tr><td>Changing rooms</td><td>Multi-door locker banks</td><td>Peak headcount on the largest shift, plus contractors</td><td>8 to 15-door banks from about RM262 per door</td></tr>
    <tr><td>Worker hostel</td><td>Two-door lockers that meet Act 446</td><td>One per resident at full occupancy</td><td>FBA-202W RM1,614.70; FBB-202 RM2,120.80 (<a href="/locker/#locker-sizes">size table</a>)</td></tr>
  </tbody>
</table>

<h2>Count before you ask for a quote</h2>
<p>A supplier can only quote what you can count. These are the numbers that decide the order, and most of them are already in the project documents:</p>
<ol>
  <li><strong>Stations per line</strong>, from the line layout, and which ones are seated, standing or sit-stand. The <a href="/guides/workbench-height-ergonomics-malaysia/">workbench height guide</a> turns DOSH&rsquo;s 2024 standing-at-work guideline into bench heights.</li>
  <li><strong>Technicians per shift</strong> in maintenance, and whether they share tools. Shared tools need a central lock or a shadow board; personal tools need one cabinet or trolley each. The <a href="/guides/tool-trolley-vs-tool-chest-vs-tool-cabinet-malaysia/">trolley, chest or cabinet guide</a> compares the options.</li>
  <li><strong>Spare-part lines</strong> on the commissioning and critical-spares lists, split into small parts (drawers and bins) and bulky parts (shelves).</li>
  <li><strong>Moulds or dies</strong>: how many, the heaviest, and the largest footprint. Mould racks are rated per level, so the heaviest mould sets the rack.</li>
  <li><strong>Headcount per shift</strong> for the changing rooms, and <strong>hostel residents at full occupancy</strong> for the accommodation.</li>
  <li><strong>ESD-protected areas</strong> on the floor plan, if you assemble or test electronics.</li>
</ol>

<h2>Order sequence and lead times</h2>
<p>Every Tanko product page states the same lead times: 3 to 7 working days for popular models from Selangor stock, and 2 to 4 weeks for configured or bulk orders. Work back from the first day of production:</p>
<table>
  <thead><tr><th>When</th><th>What</th><th>Why then</th></tr></thead>
  <tbody>
    <tr><td>8 to 6 weeks before start-up</td><td>Confirm counts and layout; get one quotation for the whole fit-out</td><td>Leaves room for your PO approval and a 2 to 4 week configured order</td></tr>
    <tr><td>6 to 4 weeks before</td><td>Order hostel lockers, mould racks, large locker banks and any configured benches</td><td>These are the bulk and configured items; hostel lockers must be in before residents arrive</td></tr>
    <tr><td>3 to 2 weeks before</td><td>Order stocked benches, tool cabinets, parts cabinets and boards</td><td>3 to 7 working days from stock, then installation</td></tr>
    <tr><td>Last week</td><td>Installation, shadow-board layout, labelling the spares store</td><td>Shadow boards are laid out with the actual tool set, so they go last</td></tr>
  </tbody>
</table>
<p>If the start-up date moves, the stocked items can move with it. The configured items are the ones to lock in early.</p>

<h2>Worker hostels: the Act 446 locker rule</h2>
<p>Employer-provided accommodation needs a certificate of accommodation from the Labour Department (JTKSM). The Employees&rsquo; Minimum Standards of Housing, Accommodations and Amenities (Accommodation and Centralised Accommodation) Regulations 2020, in force since 1 September 2020, also require each worker to have their own locked cupboard of at least 0.35 m &times; 0.35 m &times; 0.9 m for valuables, passport included. It is one per worker, not one per room.</p>
<p>Most multi-tier lockers fail that size: a three-column bank is about 272mm wide inside each door, and a four-door bank is under 800mm high per compartment. In the Tanko range the two-door FBA-202W (inside 420 x 388 x 987mm) and FBB-202 (inside 415 x 450 x 1653mm) pass. Changing rooms are not covered by the hostel rule, so the cheaper multi-door banks are the right buy there. The <a href="/guides/steel-locker-buying-guide-malaysia/">steel locker guide</a> has the full table.</p>

<h2>Electronics and semiconductor lines: plan the ESD areas first</h2>
<p>Many of the new projects in Penang, Kulim and Johor are semiconductor packaging, test and electronics plants. In an ESD-protected area the bench is part of the grounding chain: a dissipative top, a grounding cord to a common point ground, and a wrist-strap point at every position. Mark the ESD areas on the floor plan before ordering, so the benches, bins and drawer liners for those positions are specified together. The <a href="/guides/esd-anti-static-workbench-malaysia/">ESD workbench guide</a> lists the five elements an auditor checks.</p>

<h2>Outside the Klang Valley: Penang, Kulim, Johor and Melaka</h2>
<p>Primaxs delivers across Malaysia, including East Malaysia, and to Singapore. Delivery and installation are free in Selangor and Kuala Lumpur. For plants in Penang, Kulim, Johor, Melaka and elsewhere, outstation delivery is quoted separately and itemised on the quotation, so you can compare it line by line. One consolidated delivery for the whole fit-out usually costs less than several small ones.</p>

<h2>One quotation for the whole fit-out</h2>
<p>Send us the floor plan, or just a list of areas with the counts above, and the start-up date. We will come back with one Ringgit quotation covering every area, with the lead time for each line, so the configured items can be ordered first. All of it is Tanko, made in Taiwan, with one 1-year warranty against manufacturing defects handled from our Selangor office.</p>

<div class="callout"><p><strong>Pricing note:</strong> Prices are Ringgit guide prices from the model pages. The quotation is based on your exact models and quantities. <a href="/enquiry/">Send us your fit-out list</a> for a quotation.</p></div>
''',
)
