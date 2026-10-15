# -*- coding: utf-8 -*-
# Research 15 Oct 2026. Malaysia's data centre build-out is the largest new B2B fit-out market
# in the country and no page on this site targeted it (no existing page ranks for it, so no
# cannibalisation). Market facts, all read 15 Oct 2026:
#  - Knight Frank Data Centre Atlas 2026 (via EdgeProp): Johor live IT capacity 1,110MW, incoming
#    pipeline 8,542MW, third in Asia-Pacific; Johor co-location vacancy 0.7% (NST, Aug 2026).
#  - BMI (via Business Today, 9 Oct 2026): 125 data centres, 925.6MW live, 2.0GW under construction,
#    3.1GW planned.
#  - TechRepublic: Q1 2026 approvals of RM34.6bn for data centre and cloud projects (33 projects).
# ESD facts mirror the site's ESD guide (10^6-10^9 ohm dissipative top, common point ground, wrist
# strap) and IEC 61340-5-1 as the usual reference standard. Tanko does not list dedicated ESD-top
# models in this catalogue: ESD tops and grounding are quoted per project (same wording as the
# /workstation/ FAQ). The only catalogue item marked anti-static is KPQ-4302 (BLACK)(ANTI-STATIC).
# Prices are guide prices from the model pages on 15 Oct 2026.

KF = 'https://www.edgeprop.my/content/1916967/johor-leads-asia-pacific-data-centre-pipeline-klang-valley-sees-1h2026-investment-rebound-says-knight-frank'
BMI = 'https://www.businesstoday.com.my/2026/10/09/bmis-malaysia-data-centre-overview/'
TR = 'https://techrepublic.com/article/news-data-center-johor-apac-malaysia/'
NST = 'https://www.nst.com.my/amp/business/economy/2026/08/1522642/johor-data-centre-boom-hits-capacity-wall'

GUIDE = dict(
    slug='data-centre-fit-out-workbenches-spares-storage-malaysia',
    title='Data Centre Fit-Out Malaysia: Benches, Spares & Lockers',
    description=('What a Malaysian data centre needs beyond the racks: build-room benches with ESD '
                 'options, spares cabinets, tool control and staff lockers, with sizes and prices.'),
    h1='Data Centre Fit-Out in Malaysia: Build Benches, Spares Storage and Lockers',
    crumb='Data Centre Fit-Out',
    tag='Buyer\'s Guide',
    about='Storage and workbenches for data centre support rooms in Malaysia',
    published='2026-10-15',
    image='/asset_content/workshop/tanko-display-lockers-parts-cabinets.webp',
    og_image='/feed-img/workshop__lockers-parts-cabinets.jpg',
    image_alt='Tanko steel lockers, black parts cabinets and coloured bins on display',
    caption='Tanko lockers and multi-drawer parts cabinets: the two items every data centre support area ends up needing.',
    lead=('A data centre budget goes on power, cooling and racks. The rooms around the data hall '
          'are furnished last: the build room where servers are staged, the spares store, the '
          'loading bay and the security entrance. They often end up with office furniture that is not '
          'ESD-safe, cannot take a loaded server chassis, and gives no way to count tools in and out '
          'of the data hall. This guide goes room by room through what those spaces need, with sizes '
          'and guide prices.'),
    faqs=[
        ('What workbench does a data centre build room need?',
         'A steel-frame bench sized for the heaviest kit you open on it, with an ESD-safe top and a '
         'common-point ground for anything with exposed boards, power at the bench and good task '
         'lighting. Tanko heavy-duty frames are rated to 2,000kg and modular workstations add shelves, '
         'power rails and lights. ESD tops and grounding are specified per quotation.'),
        ('Are Tanko workbenches ESD-safe?',
         'They can be configured for ESD work: a dissipative top (typically 10^6 to 10^9 ohms surface '
         'resistance), a common-point ground and wrist-strap points are quoted per project, so the bench '
         'matches your ESD control plan. The KPQ-4302 hanging bins come in an anti-static black version '
         'for small parts.'),
        ('How should a data centre store spare parts?',
         'Keep fast-moving small spares such as optics, screws, cable ties and fuses in labelled '
         'multi-drawer parts cabinets, keep drives and boards in their original anti-static packaging '
         'inside lockable cabinets, and keep a separate, labelled shelf for parts awaiting return to '
         'the vendor. Tanko parts cabinets start at RM289.20.'),
        ('Do data centres need lockers?',
         'Usually, yes. Many sites restrict bags and personal devices beyond the security point, so '
         'staff, contractors and vendor engineers need somewhere to leave them. Steel lockers with '
         'per-door locks and name-card holders suit a security entrance. Tanko lockers start at RM1,614.70.'),
        ('Do you deliver to data centre sites in Johor and Cyberjaya?',
         'Yes. Primaxs delivers across Malaysia. Delivery and installation are free in Selangor and Kuala '
         'Lumpur (which includes Cyberjaya); outstation delivery, including Johor and Kulai, is quoted '
         'separately on the quotation.'),
    ],
    ranges=[
        ('/workstation/', 'Modular workstations', 'build and test stations with shelves, power rails and lights, RM927.85 to RM14,954'),
        ('/workbench/heavy-duty/', 'Heavy duty workbenches', 'frames rated to 2,000kg, from RM2,386'),
        ('/parts-cabinet/', 'Parts cabinets and bins', 'multi-drawer cabinets for small spares, from RM289.20'),
        ('/perforated-board/', 'Steel perforated boards', 'shadow boards for tool control, from RM168.70'),
        ('/tool-cabinet/eka-3m/', 'Tool trolleys', 'EKA-3M W900 x D485 x H850mm, from RM1,024.25'),
        ('/locker/', 'Steel lockers', 'staff and vendor lockers, from RM1,614.70'),
        ('/documents-cabinet/', 'Document cabinets', 'for method statements and site files, from RM216.90'),
    ],
    sources=[
        'Knight Frank Data Centre Atlas 2026, reported by EdgeProp: <a href="%s" rel="noopener" target="_blank">Johor leads Asia-Pacific data centre pipeline</a>' % KF,
        'BMI, reported by Business Today (9 October 2026): <a href="%s" rel="noopener" target="_blank">Malaysia data centre overview</a>' % BMI,
        'TechRepublic: <a href="%s" rel="noopener" target="_blank">Malaysia data center growth as Johor capacity tightens</a>' % TR,
        'New Straits Times (August 2026): <a href="%s" rel="noopener" target="_blank">Johor data centre boom hits capacity wall</a>' % NST,
        'Related: <a href="/guides/esd-anti-static-workbench-malaysia/">ESD and anti-static workbenches</a> and the <a href="/guides/new-factory-storage-fit-out-checklist-malaysia/">new factory fit-out checklist</a>',
    ],
    body='''
<div class="callout"><p><strong>Direct answer:</strong> Beyond the racks, a Malaysian data centre needs five kinds of support furniture: steel build-room benches with ESD tops and grounding, multi-drawer cabinets for small spares, shadow boards and trolleys so tools are counted in and out of the data hall, lockers at the security entrance, and document cabinets for method statements. Tanko covers all five, with guide prices from RM168.70 (pegboard) to RM2,386 (heavy-duty bench), delivered across Malaysia.</p></div>

<h2>Why this matters now</h2>
<p>Malaysia is one of the fastest-growing data centre markets in Asia. Knight Frank's 2026 atlas puts Johor's live IT capacity at 1,110MW with a pipeline of 8,542MW, third in Asia-Pacific, and vacancy in Johor's co-location space has been reported at 0.7%. BMI counts 125 Malaysian data centres with 925.6MW live and around 2GW under construction. Every one of those buildings has a build room, a spares store, a loading bay and a security entrance, and those rooms are usually specified late in the project.</p>

<h2>Room by room: what each support space needs</h2>
<table>
  <thead><tr><th>Space</th><th>What goes wrong</th><th>What to specify</th></tr></thead>
  <tbody>
    <tr><td>Build and staging room</td><td>Servers opened on office desks with no ESD control; desks that flex under a loaded chassis</td><td>Steel-frame benches rated well above the heaviest kit, ESD top and common-point ground, power at the bench, task lighting</td></tr>
    <tr><td>Spares store</td><td>Optics, screws and fuses mixed in cardboard boxes; nobody knows what is in stock</td><td>Labelled multi-drawer parts cabinets, lockable cabinets for drives and boards, a separate shelf for parts awaiting return</td></tr>
    <tr><td>Data hall tool control</td><td>Tools left inside racks or under raised floors after maintenance</td><td>A shadow board at the data hall entrance and a fitted trolley for the shift's tool kit, checked out and back</td></tr>
    <tr><td>Loading bay and receiving</td><td>Unboxing on the floor; packaging and labels everywhere</td><td>A heavy-duty receiving bench and racking for incoming stock</td></tr>
    <tr><td>Security entrance</td><td>Bags and phones carried into restricted areas, or piled at the guard post</td><td>Steel lockers with per-door locks for staff, contractors and vendor engineers</td></tr>
    <tr><td>Operations office</td><td>Method statements and permits scattered across desks</td><td>A4 document cabinets and trays, labelled by system</td></tr>
  </tbody>
</table>

<h2>The build room bench: load, ESD and power</h2>
<p>The bench in a build room has three jobs. It has to carry the heaviest thing you will open on it, so specify the frame for the kit, not for a monitor; Tanko heavy-duty frames are rated to 2,000kg. It has to be part of your ESD control: a dissipative top (typically 10<sup>6</sup> to 10<sup>9</sup> ohms surface resistance), a common-point ground and a wrist-strap point, so that charge drains away instead of reaching exposed boards. IEC 61340-5-1 is the standard most ESD control plans are written against. And it needs power and light where the work is, which is what a <a href="/workstation/">modular workstation</a> adds: shelves, power rails and lighting that can be moved when the room is rearranged.</p>
<p>Tanko does not sell a single "ESD model": the ESD top and grounding are specified on the quotation, so they match your site's ESD control plan. Tell us the plan's requirements and we will configure the bench to them. See the <a href="/guides/esd-anti-static-workbench-malaysia/">ESD workbench guide</a> for the five elements of an ESD workstation.</p>

<h2>Spares storage that tells you what is in stock</h2>
<p>A spares store works when every part has one labelled place. Multi-drawer <a href="/parts-cabinet/">parts cabinets</a> suit small, fast-moving items: optics, screws, cable ties, fuses, rail kits. Drives and boards are best kept in their original anti-static packaging inside a lockable cabinet. The <a href="/perforated-board/kpq-4301/">KPQ-4302 hanging bins</a> come in an anti-static black version for loose small parts at the bench. Keep a separate, clearly marked shelf for faulty parts waiting to go back to the vendor, so they never return to stock by mistake.</p>

<h2>Tool control at the data hall door</h2>
<p>A tool left inside a rack or under a raised floor is a hazard nobody sees until something goes wrong. The simplest control is a <a href="/guides/perforated-board-shadow-board-tool-control-malaysia/">shadow board</a> at the data hall entrance: every tool has an outlined place, so an empty outline shows at a glance what has not come back. Pair it with a fitted <a href="/tool-cabinet/eka-3m/">tool trolley</a> for the shift's kit, checked out and back with the permit.</p>

<h2>Lockers at the security entrance</h2>
<p>Many sites restrict bags and personal devices beyond the security point. Staff, contractors and vendor engineers need somewhere to leave them that is not the guard's desk. <a href="/locker/">Steel lockers</a> with a lock on every door and a name-card holder are the usual answer; plan for the peak number of people on site during a migration or a major maintenance window, not the normal headcount.</p>

<h2>What to send for a quotation</h2>
<ol>
  <li>The rooms you are fitting out and their sizes (a floor plan is ideal).</li>
  <li>The heaviest item that will be opened on a bench, and how many build positions you need.</li>
  <li>Your ESD control plan requirements, if the build room is an ESD protected area.</li>
  <li>The spares you hold (types and rough quantities) and the peak number of people who will need a locker.</li>
  <li>The site address and the delivery window.</li>
</ol>
<p>We reply with a layout and a written Ringgit quotation. Delivery and installation are free in Selangor and Kuala Lumpur, including Cyberjaya; outstation delivery, including Johor and Kulai, is itemised on the quotation. A 1-year warranty against manufacturing defects is handled from our Selangor office.</p>

<div class="callout"><p><strong>Pricing note:</strong> Prices are Ringgit guide prices from the model pages. ESD tops, grounding and configured workstations are quoted per project. <a href="/enquiry/">Send us your room list</a> for a quotation.</p></div>
''',
)
