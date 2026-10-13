# -*- coding: utf-8 -*-
# Research 14 Oct 2026. Budget 2027 (tabled 9 Oct 2026) puts RM8 billion into TVET across
# ministries (Malay Mail). JPK counted 1,608 accredited skills centres (Pusat Bertauliah) in
# March 2025: 1,138 public and 470 private (JPK statistics report). Public institutes buy through
# MOF-registered suppliers, so this page speaks to private skills centres, corporate training
# workshops, universities and colleges first, without saying anything about MOF.
# HRD Corp ALAT: verified in the HRD Corp Allowable Cost Matrix guidebook (Jan 2026 version),
# pages 9-10: funds "training aids" to set up or enhance training rooms, max 50% of the 1 January
# levy balance, approval before purchase, purchase within 6 months; and it lists "Items that are
# not required for training such as signage and cabinets" as NOT eligible. So this page must NOT
# say our storage is HRD Corp claimable. It says what the guidebook says and tells the reader to
# confirm with HRD Corp.
# Hero photo: real Tanko workbenches with pegboard uprights and power (workshop-2026-08).

ACM = 'https://hrdcorp.gov.my/wp-content/uploads/2025/12/Jan-2026-Version_Allowable-Cost-Matrix-2025.pdf'
MM = ('https://www.malaymail.com/news/malaysia/2026/10/09/'
      'budget-2027-rm8b-for-tvet-30000-new-job-opportunities-via-bakat-madani/238487')
JPK = ('https://www.dsd.gov.my/images/04-sumber/statistik/pencapaian/2025/'
       'LAPORAN%20STATISK%20JPK%20MAC%202025.pdf')

GUIDE = dict(
    slug='training-workshop-benches-tool-storage-malaysia',
    title='Training Workshop Equipment Malaysia: Benches & Tool Storage',
    description=('Setting up a TVET or company training workshop in Malaysia: trainee benches, '
                 'tool control, lockers, ESD stations, prices, and what HRD Corp ALAT does cover.'),
    h1='Setting Up a Training Workshop in Malaysia: Benches, Tool Storage and Lockers',
    crumb='Training Workshop Setup',
    tag='Buyer\'s Guide',
    about='Equipping TVET and company training workshops in Malaysia',
    published='2026-10-14',
    image='/asset_content/workshop/training-workshop-bench-hero.webp',
    og_image='/feed-img/workshop__training-workshop-bench.jpg',
    image_alt='Row of Tanko workbenches with pegboard uprights, power sockets and lockable drawers',
    caption='Tanko workbenches with pegboard uprights and power at every station: the layout a hands-on training bay needs.',
    lead=('A training workshop is harder on furniture than a production floor. Every intake is new, '
          'nobody owns the bench, tools change hands every session, and the room is reset and '
          're-used all week. Budget 2027 puts RM8 billion into TVET, and private skills centres, '
          'colleges and company training academies are equipping workshops to match. This guide '
          'covers what each training station needs, how to stop tools walking out at the end of a '
          'class, and what the HRD Corp ALAT scheme does and does not pay for.'),
    faqs=[
        ('What equipment does a training workshop need?',
         'Plan it per trainee station: a workbench sized to the practical task, a pegboard upright or '
         'shadow board for the station\'s tools, power at the bench where tools need it, lockable '
         'storage for the shared or calibrated tools, parts bins for consumables, and lockers for '
         'trainees\' bags. Electronics training needs ESD stations; automotive and fabrication training '
         'needs heavy duty benches.'),
        ('How do training centres stop tools going missing?',
         'Shadow boards. Each tool has an outlined place on a steel pegboard, so at the end of a session '
         'the instructor can see in seconds which outline is empty. Pair the board with a lockable tool '
         'cabinet for calibrated or expensive tools that are signed out.'),
        ('Can HRD Corp ALAT pay for workbenches and cabinets?',
         'Not reliably. HRD Corp\'s Allowable Cost Matrix (January 2026) says ALAT funds training aids '
         'used solely for training, capped at 50% of the levy balance as at 1 January, and lists items '
         'not required for training, such as signage and cabinets, as not eligible. Check the specific '
         'item with HRD Corp before you order, and apply before buying: purchases made before approval '
         'cannot be claimed.'),
        ('What workbench height suits trainees?',
         'Most fixed industrial benches are 750 to 850mm high. Standing practical work suits the lower '
         'end for heavy tasks and higher working heights for fine work; DOSH\'s 2024 standing-at-work '
         'guideline is the reference. See the workbench height guide for task-by-task heights.'),
        ('Do you supply private colleges and company training centres?',
         'Yes. Primaxs quotes in Ringgit to private skills centres, colleges, universities and company '
         'training academies, delivers across Malaysia, and installs free in Selangor and Kuala Lumpur.'),
        ('How long does it take to equip a training workshop?',
         'Popular Tanko models are delivered in 3 to 7 working days from Selangor stock; configured or '
         'bulk orders take 2 to 4 weeks. Order before the intake date, so benches and lockers are '
         'installed before the first class.'),
    ],
    ranges=[
        ('/workbench/', 'Industrial workbenches', 'Performance from RM903.75, heavy duty (2,000kg frames) from RM2,385.90'),
        ('/perforated-board/', 'Steel perforated boards', 'shadow boards and pegboard uprights, from RM168.70'),
        ('/tool-cabinet/', 'Tool cabinets and trolleys', 'lockable tool storage, from RM1,024.25'),
        ('/parts-cabinet/', 'Parts cabinets and bins', 'consumables and small parts, from RM289.20'),
        ('/locker/', 'Steel lockers', 'multi-door banks for trainees\' bags, from about RM262 per door'),
        ('/workstation/', 'Modular workstations', 'assembly and electronics training stations, from RM927.85'),
    ],
    sources=[
        'HRD Corp: <a href="%s" rel="noopener" target="_blank">Guidebook Allowable Cost Matrix, January 2026 version</a> (ALAT scheme, pages 9 to 10)' % ACM,
        'Malay Mail: <a href="%s" rel="noopener" target="_blank">Budget 2027: RM8b for TVET</a> (9 October 2026)' % MM,
        'Jabatan Pembangunan Kemahiran: <a href="%s" rel="noopener" target="_blank">Laporan Statistik JPK, Mac 2025</a> (Pusat Bertauliah counts)' % JPK,
        'Related: <a href="/guides/workbench-height-ergonomics-malaysia/">Workbench height guide</a>, <a href="/guides/perforated-board-shadow-board-tool-control-malaysia/">shadow boards and 5S tool control</a> and <a href="/guides/esd-anti-static-workbench-malaysia/">ESD workbenches</a>',
    ],
    body='''
<div class="callout"><p><strong>Direct answer:</strong> Equip a training workshop per trainee station: a steel workbench sized to the practical task, a pegboard upright or shadow board for that station's tools, power at the bench, a lockable cabinet for shared and calibrated tools, parts bins for consumables, and a locker bank for trainees' bags. Shadow boards are what stop tools going missing between classes. Do not plan on HRD Corp ALAT paying for storage: its guidebook lists cabinets as an example of items not eligible.</p></div>

<h2>Why training workshops wear out furniture faster</h2>
<ul>
  <li><strong>Nobody owns the bench.</strong> A production bench has one operator who looks after it. A training bench has a new trainee every session, and every trainee clamps, drops and drills differently.</li>
  <li><strong>Tools change hands all day.</strong> Without a fixed place for every tool, the end-of-class count takes longer than the lesson, and losses get noticed weeks later.</li>
  <li><strong>The room is reset constantly.</strong> Stations are rearranged for each module; furniture that cannot be moved or reconfigured becomes the constraint on the timetable.</li>
  <li><strong>Bags and phones need somewhere to go.</strong> Loose bags on the workshop floor are a trip hazard and a theft risk.</li>
</ul>

<h2>The station checklist</h2>
<table>
  <thead><tr><th>At each station</th><th>Why</th><th>Tanko range and guide price</th></tr></thead>
  <tbody>
    <tr><td>Steel workbench</td><td>Takes clamping, impacts and spills; rubber or laminate top to suit the trade</td><td><a href="/workbench/">Workbenches</a> from RM903.75; heavy duty, 2,000kg frames, from RM2,385.90</td></tr>
    <tr><td>Pegboard upright or shadow board</td><td>Every tool in a marked place; instant end-of-class check</td><td><a href="/perforated-board/">Steel perforated boards</a> from RM168.70</td></tr>
    <tr><td>Power at the bench</td><td>No trailing extension leads across the floor</td><td>Bench uprights with sockets on request</td></tr>
    <tr><td>Drawer unit</td><td>The station's own hand tools and consumables, lockable</td><td>Drawer options on most <a href="/workbench/">workbench</a> lines</td></tr>
  </tbody>
</table>
<p>And for the room: a lockable <a href="/tool-cabinet/">tool cabinet</a> for shared, calibrated or expensive tools that are signed out (from RM1,024.25); <a href="/parts-cabinet/">parts cabinets and bins</a> for consumables (from RM289.20); and a <a href="/locker/">multi-door locker bank</a> at the entrance for trainees' bags (8 to 15-door banks from about RM262 per door).</p>

<h2>Tool control: the shadow board is the real saving</h2>
<p>The most expensive part of a training workshop is not the furniture, it is the tools that disappear. A shadow board gives every tool an outlined place on a steel pegboard. At the end of the session the instructor looks at the wall: any empty outline is a missing tool, and it is found before the class leaves rather than at the next stock-take.</p>
<ul>
  <li>One board per station for the tools that station uses, plus one wall board for shared tools.</li>
  <li>Calibrated instruments and expensive power tools go in a lockable cabinet with a sign-out sheet.</li>
  <li>Steel rather than hardboard: holes stay round after years of hooks being moved, and the board wipes clean.</li>
</ul>
<p>The <a href="/guides/perforated-board-shadow-board-tool-control-malaysia/">shadow board guide</a> covers layout and outlining.</p>

<h2>By trade</h2>
<table>
  <thead><tr><th>Training area</th><th>Bench</th><th>Storage</th></tr></thead>
  <tbody>
    <tr><td>Automotive and motorcycle</td><td>Heavy duty bench, rubber or steel top</td><td>Tool trolleys per bay, shadow boards, parts bins</td></tr>
    <tr><td>Fitting, machining, CNC</td><td>Heavy duty bench for vice work</td><td><a href="/cnc-tool/">CNC tool holder storage</a>, tool cabinets</td></tr>
    <tr><td>Electrical and electronics</td><td><a href="/guides/esd-anti-static-workbench-malaysia/">ESD workstation</a> with grounding at every position</td><td>Anti-static bins, parts cabinets</td></tr>
    <tr><td>Welding and fabrication</td><td>Steel-top heavy duty bench</td><td>Steel racks for stock and offcuts</td></tr>
    <tr><td>Assembly and production skills</td><td><a href="/workstation/">Modular workstations</a> (from RM927.85)</td><td>Bins on louvred panels at reach height</td></tr>
  </tbody>
</table>

<h2>What HRD Corp ALAT does and does not pay for</h2>
<p>Many employers assume their HRD Corp levy will cover a training workshop fit-out. The HRD Corp <em>Allowable Cost Matrix</em> guidebook (January 2026 version) is narrower than that:</p>
<ul>
  <li>ALAT funds <strong>training aids</strong> to set up, renovate or enhance training rooms, used solely for training and relevant to the employer's business. It does not fund building a training centre or renting one.</li>
  <li>The grant is capped at <strong>50% of the levy balance as at 1 January</strong> of the application year.</li>
  <li>The application must be <strong>approved before purchase</strong>; anything bought earlier cannot be claimed. Purchases must be made within six months of approval.</li>
  <li>Grant submission needs a supplier quotation or pro forma invoice and a training-room layout; the claim needs official receipts and an itemised invoice.</li>
  <li>Among items listed as <strong>not eligible</strong>: delivery charges, installation services on their own, and "items that are not required for training such as signage and cabinets".</li>
</ul>
<p>So plan the furniture budget without ALAT, and ask HRD Corp about any specific item before ordering. If you do apply for eligible training equipment, we can provide the itemised quotation and a room layout drawing for your submission.</p>

<h2>What to send for a quotation</h2>
<ol>
  <li>The trade or module, and the number of trainee stations per class.</li>
  <li>The room size (a sketch is enough) and where power points are.</li>
  <li>Which tools each station keeps, and which are shared or calibrated.</li>
  <li>Locker count: trainees per intake, plus staff.</li>
  <li>The intake date, so the order lands before the first class.</li>
</ol>
<p>We reply with a station layout and a Ringgit quotation. Delivery and installation are free in Selangor and Kuala Lumpur; outstation delivery is itemised on the quotation.</p>

<div class="callout"><p><strong>Pricing note:</strong> Prices are Ringgit guide prices from the model pages; the quotation is based on your station count and configuration. <a href="/enquiry/">Send us your workshop layout</a> for a quotation.</p></div>
''',
)
