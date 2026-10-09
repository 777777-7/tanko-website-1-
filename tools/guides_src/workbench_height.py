# -*- coding: utf-8 -*-
# Research 9 Oct 2026 (live Google MY, gl=my pws=0): the site already ranks first for
# "workbench height malaysia" on one sentence in the how-to-choose guide; the rest of that
# page is a 55-word makerspace post, Facebook/Reddit threads and foreign blogs. "how high
# should a workbench be" and "standard workbench height mm" are all foreign. No Malaysian
# page turns DOSH's 2024 standing-at-work guideline into buying advice.
# Facts verified this session: DOSH Guidelines on OSH for Standing at Work 2024 (PDF text
# extracted) and CCOHS "Working in a Standing Position". Bench heights and prices are read
# from docs/workbench/. WKT-5102 price deliberately not quoted (RM1,500 on every variant
# looks like a placeholder).

DOSH = 'https://dosh.gov.my/wp-content/uploads/2025/01/GUIDELINES-ON-OCCUPATIONAL-SAFETY-AND-HEALTH-FOR-STANDING-AT-WORK-2024.pdf'
CCOHS = 'https://www.ccohs.ca/oshanswers/ergonomics/standing/standing_basic.html'

GUIDE = dict(
    slug='workbench-height-ergonomics-malaysia',
    title='Workbench Height Guide Malaysia: Sit, Stand & DOSH | Primaxs',
    description=('The right workbench height for precision, assembly and heavy work: the elbow rule, '
                 'DOSH 2024 standing guidance, footrests, mats, and Tanko benches from H750 to H1165mm.'),
    h1='Workbench Height and Ergonomics: How High Should a Workbench Be?',
    crumb='Workbench Height Guide',
    tag='Buyer\'s Guide',
    published='2026-10-09',
    image='/asset3/WA-57F.webp',
    og_image='/feed-img/asset3__WA-57F.jpg',
    image_alt='Tanko WA-57F heavy duty workbench, W1500 x D650 x H786mm, for a Malaysian workshop',
    caption='Most fixed industrial benches sit between 750 and 850mm. Whether that is right depends on the task and the person.',
    lead=('There is no single correct workbench height. The right height is set by two things: what the '
          'operator is doing, and how tall that operator is. Get it wrong and the bench still works, but '
          'the person at it bends, reaches or shrugs all shift, and the back and shoulder complaints arrive '
          'a few months later. This guide turns the Department of Occupational Safety and Health (DOSH) 2024 '
          'standing-at-work guideline into numbers you can use when ordering a bench.'),
    faqs=[
        ('What is the standard height of a workbench?',
         'There is no single standard. Fixed industrial benches are usually 750 to 900mm high. In the Tanko '
         'range they are 750mm (Performance WE 1200), 786 to 800mm (Heavy Duty WA and Professional WB), 810mm '
         '(Steel Top WD) and 836 to 850mm on castors (WA mobile). The right height depends on the task and '
         'the operator, measured from the operator\'s standing elbow height.'),
        ('How high should a workbench be in mm?',
         'Measure the operator\'s standing elbow height, then adjust for the task. Canada\'s CCOHS gives '
         'about 5cm above elbow height for precision work with elbow support, 5 to 10cm below for light '
         'assembly, and 20 to 40cm below for heavy work that needs downward force. For an operator with a '
         '1,000mm elbow height that means about 1,050mm, 900 to 950mm, and 600 to 800mm.'),
        ('What workbench height suits my height?',
         'Use elbow height, not overall body height, because arm and trunk proportions vary. Stand upright '
         'in work shoes with the upper arm hanging and the forearm level, and measure from the floor to the '
         'underside of the elbow. Then apply the task offsets. If several people share one bench, size it '
         'for the shorter operators and give taller ones a raised fixture, as DOSH recommends.'),
        ('Should workers sit or stand at a workbench?',
         'It depends on the task. DOSH says precision work may be done standing only for short periods, '
         'preferably under 10 minutes, and that longer precision or light work should be done seated. '
         'Heavy work that needs force should be done standing. Tasks needing continuous foot control '
         'should be done seated.'),
        ('Do anti-fatigue mats really help?',
         'Yes, when chosen correctly. DOSH cites mats 11 to 11.5mm thick with medium to high stiffness as '
         'giving a significant reduction in lower-leg muscle activity. DOSH also warns that mats can cause '
         'tripping and suit stations where workers move little. Where mats do not fit, it suggests '
         'cushioning poured level with the floor, or cushioned insoles for mobile staff.'),
        ('Is an adjustable-height workbench worth it?',
         'When different people use the same bench, usually yes. A fixed bench is a compromise for everyone '
         'except the person it was sized for. The Tanko WKT-5102 packing station adjusts from 965 to '
         '1,165mm. For fixed benches, platforms for shorter operators and raised fixtures for precision work '
         'are cheaper fixes.'),
    ],
    ranges=[
        ('/workbench/performance/', 'Performance workbenches', 'WE and WET, 750mm (1,200mm wide) and 800mm (1,500mm wide), from RM903.75'),
        ('/workbench/professional/', 'Professional workbenches', 'WB, 800mm, 600kg frames, from RM1,277.30'),
        ('/workbench/heavy-duty/', 'Heavy duty workbenches', 'WA, WAT and WAS, 786 to 800mm, 2,000kg frames, from RM2,385.90'),
        ('/workbench/packing-station/', 'Packing station', 'WKT-5102, adjustable from 965 to 1,165mm'),
        ('/workbench/wp-6/', 'Workbench seating', 'four stool styles sized for Tanko benches, from RM216.90'),
    ],
    sources=[
        'DOSH Malaysia: <a href="%s" rel="noopener" target="_blank">Guidelines on Occupational Safety and Health for Standing at Work 2024</a> (PDF)' % DOSH,
        'Canadian Centre for Occupational Health and Safety: <a href="%s" rel="noopener" target="_blank">Working in a Standing Position, basic information</a>' % CCOHS,
        'DOSH Malaysia: <a href="https://dosh.gov.my/en/perundangan/garis-panduan/ergonomik/" rel="noopener" target="_blank">ergonomics guidelines index</a> (sitting, manual handling, risk assessment)',
        'Related: <a href="/guides/how-to-choose-a-workbench-malaysia/">How to choose a workbench</a> and <a href="/guides/workbench-top-material-guide-malaysia/">Workbench top materials</a>',
    ],
    body='''
<div class="callout"><p><strong>Direct answer:</strong> Set the work surface from the operator&rsquo;s standing elbow height: about 5cm <em>above</em> it for precision work with elbow support, 5 to 10cm <em>below</em> it for light assembly, and 20 to 40cm <em>below</em> it for heavy work that needs downward force. Most fixed industrial benches are 750 to 850mm high, which suits heavy work standing or most work seated. Light standing assembly usually needs the work raised.</p></div>

<h2>Why bench height shows up as back pain</h2>
<p>A bench that is too low makes people bend at the waist and neck. One that is too high makes them lift their shoulders and wing their elbows out. Neither is dramatic on day one. Over a shift, and over months, the static load adds up. DOSH&rsquo;s 2024 guideline points to the national figures for 2022: of 7,143 confirmed cases of occupational disease, occupational musculoskeletal disorders were the second largest group, with 678 cases.</p>
<p>The guideline&rsquo;s first rules are the ones a bench height controls: keep the neck aligned, keep the elbows in and the shoulders relaxed, keep the wrists neutral, and keep everything within easy reach.</p>

<h2>The elbow-height rule</h2>
<p>Elbow height is the reference because it is where the forearms naturally work. DOSH puts the optimal working height of the hands &ldquo;around elbow level&rdquo; and says heavier work should be lower and precision or inspection work higher. CCOHS gives the numbers:</p>
<table>
  <thead><tr><th>Type of work</th><th>Work surface vs standing elbow height</th><th>Example at a 1,000mm elbow height</th></tr></thead>
  <tbody>
    <tr><td>Precision: electronics assembly, inspection, writing</td><td>About 5cm above, with elbow support</td><td>About 1,050mm</td></tr>
    <tr><td>Light: assembly line, mechanical fitting</td><td>5 to 10cm below</td><td>900 to 950mm</td></tr>
    <tr><td>Heavy: work that needs downward force</td><td>20 to 40cm below</td><td>600 to 800mm</td></tr>
  </tbody>
</table>
<p>The 1,000mm column is a worked example, not an average. Measure your own people: stand upright in work shoes, upper arm hanging, forearm level, and measure from the floor to the underside of the elbow.</p>
<p>&ldquo;Work surface&rdquo; means where the hands are, not the bench top. A 150mm fixture or a part in a jig raises the working height by that much. For heavy work, a vice adds its own height on top of the bench.</p>

<h2>Sit or stand? Match the posture to the task</h2>
<p>DOSH ties posture to the type of work:</p>
<ul>
  <li><strong>Precision work</strong> may be done standing only for short periods, &ldquo;preferably less than 10 minutes&rdquo;. Longer precision and light work should be done seated, for visual and body stability.</li>
  <li><strong>Light work</strong> can be seated or standing. The table height is recommended near standing elbow height.</li>
  <li><strong>Heavy work</strong> should be done standing, because the force comes from the larger muscles of the shoulders, back and thighs. DOSH suggests a table height below the waistline.</li>
  <li><strong>Tasks with continuous foot control</strong>, such as a pedal-operated press, should be done seated.</li>
</ul>
<p>DOSH&rsquo;s checklist asks a blunt question: is static standing kept under 10 minutes, with leg movement or rest? If the answer is no for a whole line, the fix is a seat or a sit-stand arrangement, not a better mat.</p>

<h2>Sizing a bench for several people</h2>
<p>Most benches are shared across shifts. DOSH&rsquo;s rule of thumb for reach is to design for smaller-statured people: if shorter operators can reach comfortably, everyone can. For height, it lists five ways to accommodate differences:</p>
<ol>
  <li>Adjust the height of the work surface.</li>
  <li>Stand shorter operators on platforms.</li>
  <li>Set up a work area for tall people, and give short people a bench to stand on.</li>
  <li>Tilt the work surface.</li>
  <li>Use tool extenders.</li>
</ol>
<p>In practice: buy fixed benches at the height that suits your shorter operators for the main task, raise the work for taller operators with a fixture or riser, and save adjustable benches for stations where operators change every shift.</p>

<h2>Fixed, adjustable or on castors: Tanko bench heights</h2>
<p>Every height below is read from the model pages. Load ratings are for the frame.</p>
<table>
  <thead><tr><th>Bench</th><th>Work-top height</th><th>Frame load</th><th>Guide price from</th><th>Suits</th></tr></thead>
  <tbody>
    <tr><td><a href="/workbench/we1200/">Performance WE, 1,200mm wide</a></td><td>750mm</td><td>&mdash;</td><td>RM903.75</td><td>Seated light assembly, QC, packing desks</td></tr>
    <tr><td><a href="/workbench/heavy-duty/">Heavy Duty WA-57, 1,500mm</a></td><td>786mm</td><td>2,000kg</td><td>RM2,385.90</td><td>Heavy standing work, fitting with a vice</td></tr>
    <tr><td><a href="/workbench/we/">Performance WE, 1,500mm</a></td><td>800mm</td><td>&mdash;</td><td>RM1,211.00</td><td>Seated work, light standing work with a fixture</td></tr>
    <tr><td><a href="/workbench/professional/">Professional WB, 1,500mm</a></td><td>800mm</td><td>600kg</td><td>RM1,277.30</td><td>General workshop and assembly</td></tr>
    <tr><td><a href="/workbench/wd-48/">Steel Top WD, 1,224mm</a></td><td>810mm</td><td>2,000kg</td><td>RM1,674.95</td><td>Heavy work, oily parts, welding prep</td></tr>
    <tr><td><a href="/workbench/wa-57m/">Heavy Duty WA, mobile</a></td><td>836 to 850mm</td><td>1,000kg</td><td>RM3,048.65</td><td>Work that moves to the machine</td></tr>
    <tr><td><a href="/workbench/wkt_5102/">Packing station WKT-5102</a></td><td>965 to 1,165mm, adjustable</td><td>100kg top</td><td>See model page</td><td>Shared standing stations, packing, despatch</td></tr>
  </tbody>
</table>
<p>The pattern is worth knowing before you order: <strong>fixed industrial benches sit at 750 to 850mm</strong>. That is right for heavy standing work and for seated work, and low for light standing assembly unless the work is raised. If a line does light assembly standing all shift, plan the fixture height, a riser, or an adjustable station from the start.</p>

<h2>Reach and bench depth</h2>
<p>Height and reach go together. DOSH asks that items be placed around elbow height and within the reach of the forearm, about 50cm. Things in almost constant use belong inside that zone. Frequently used materials should stay within full-arm reach. Anything further forces a lean, and leaning over a bench loads the lower back as badly as bending to a low one.</p>
<ul>
  <li><strong>Depth:</strong> 600 to 750mm deep benches keep the working zone within forearm reach. Deeper tops collect clutter at the back.</li>
  <li><strong>Back panels and shelves:</strong> put the tools used every cycle on a <a href="/perforated-board/">perforated board</a> at the back of the bench, between elbow and shoulder height, not on a top shelf.</li>
  <li><strong>Parts:</strong> DOSH suggests smaller containers to shorten reaches. Tilted bins at the front edge beat a deep tote at the back.</li>
</ul>

<h2>Footrests, mats and stools</h2>
<p>When the bench height cannot change, these three change the posture instead.</p>
<ul>
  <li><strong>Footrests:</strong> DOSH says footrest heights between 10 and 30cm can improve muscle activity and posture, because they let a standing worker shift weight from leg to leg. A rail along the base of the bench does the same job.</li>
  <li><strong>Anti-fatigue mats:</strong> DOSH cites 11 to 11.5mm mats of medium to high stiffness as giving a significant reduction in lower-leg muscle activity. Softer is not better. DOSH also warns that mats can cause tripping, so they suit stations where people move little.</li>
  <li><strong>Sit-stand stools and bench seats:</strong> a stool sized for the bench height lets precision and light work go seated, which is what DOSH recommends for anything longer than about 10 minutes. Tanko&rsquo;s <a href="/workbench/wp-6/">workbench seating</a> comes in four styles from RM216.90, fixed or gas-lift, with or without a backrest.</li>
</ul>
<p>DOSH&rsquo;s clearance figures for standing work are worth checking on any bench with a closed front or drawers: at least 10cm knee clearance and a toe space at least 13cm high and 13cm deep, so the worker can stand close without leaning.</p>

<h2>Heights by job</h2>
<table>
  <thead><tr><th>Job</th><th>Posture</th><th>Where to start</th></tr></thead>
  <tbody>
    <tr><td>Electronics assembly, rework, QC inspection</td><td>Seated, elbow support</td><td>750 to 800mm bench with a matched stool; raise the work, not the operator&rsquo;s shoulders. See <a href="/guides/esd-anti-static-workbench-malaysia/">ESD workbenches</a>.</td></tr>
    <tr><td>Light mechanical assembly</td><td>Standing or sit-stand</td><td>Bench 5 to 10cm below elbow height: a fixed 800mm bench plus a fixture, or an adjustable station</td></tr>
    <tr><td>Packing and despatch</td><td>Standing, mixed operators</td><td>Adjustable 965 to 1,165mm <a href="/workbench/packing-station/">packing station</a></td></tr>
    <tr><td>Fabrication, fitting, vice work</td><td>Standing</td><td>Heavy duty 786 to 810mm bench; the vice brings the jaws up. See <a href="/guides/heavy-duty-workbench-fabrication-welding-malaysia/">heavy duty workbenches</a>.</td></tr>
    <tr><td>Automotive and maintenance bays</td><td>Standing, moving</td><td>Mobile heavy duty bench at 836 to 850mm, or a fixed bench plus a <a href="/guides/tool-trolley-vs-tool-chest-vs-tool-cabinet-malaysia/">tool trolley</a></td></tr>
  </tbody>
</table>

<h2>Measure before you order: a checklist</h2>
<ol>
  <li><strong>List the tasks</strong> at the bench and mark each one precision, light or heavy.</li>
  <li><strong>Decide sit or stand</strong> for each, using the DOSH rules above. Anything precise and longer than 10 minutes goes seated.</li>
  <li><strong>Measure standing elbow height</strong> for the shortest and tallest regular operators, in work shoes.</li>
  <li><strong>Work out the target</strong> working height for the main task, then take off any fixture or part height to get the bench-top height.</li>
  <li><strong>Choose fixed or adjustable.</strong> One operator or a narrow height range: fixed. Rotating operators: adjustable, or fixed plus platforms and risers.</li>
  <li><strong>Check reach and depth</strong>: everything used every cycle within about 50cm.</li>
  <li><strong>Add the extras</strong> the posture needs: stool, footrest or mat.</li>
</ol>

<div class="callout"><p><strong>Pricing note:</strong> Prices are Ringgit guide prices from the model pages. Send us the task, the bench size and your operators&rsquo; elbow heights, and we will <a href="/enquiry/">quote the bench and seating together</a>. Delivery and installation are free in Selangor and Kuala Lumpur; outstation delivery is itemised on the quote.</p></div>
''',
)
