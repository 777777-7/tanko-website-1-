# -*- coding: utf-8 -*-
"""Per-category FAQ + related-guide mappings for SEO enrichment of category pages.

These are original, Malaysia-focused Q&As written for this site (not copied from
tanko.tw) so Google won't treat them as duplicate content. Each category gets a
short FAQ rendered as <details> + FAQPage schema, plus links to the most relevant
guides to strengthen internal linking.
"""

CATEGORY_FAQ = {
    "workbench": [
        {"q": "What size workbench do I need for a Malaysian workshop?",
         "a": "Standard Tanko workbench depths are 750 mm and widths run from 1200 mm up to 2100 mm. Start with the widest item that must sit on the bench, add working space around it, and confirm the aisle behind operators stays clear. A 1500 mm or 1800 mm bench covers most single-operator stations."},
        {"q": "Rubber, laminate, stainless steel or wood top — which is best?",
         "a": "Rubber (impact) tops suit hammering and mechanical work; laminate tops are clean and quiet for assembly and inspection; stainless-steel tops are for wet, food, chemical or cleanroom areas; solid wood tops are for lighter packing and display work. Tell us the task and we can match the top."},
        {"q": "Can I get a workbench with drawers, power sockets and a pegboard?",
         "a": "Yes. Most Tanko workbench lines accept bolt-on upper racks, drawers, power socket bars, LED lights and perforated boards. Because they are modular, you can add them now or later. Ask for a configured quote including accessories."},
        {"q": "How long does delivery take for workbenches in Malaysia?",
         "a": "Stocked configurations can ship from our Selangor warehouse within a few business days. Non-stocked or fully configured units are quoted with a confirmed lead time before you order. Nationwide delivery (including Peninsular Malaysia) is available."},
        {"q": "Do you sell to companies outside Selangor and KL?",
         "a": "Yes — we deliver across Malaysia. We regularly supply factories and workshops in Johor Bahru, Penang, Ipoh, Melaka and the East Coast, and can arrange freight to East Malaysia on request."},
    ],
    "tool-cabinet": [
        {"q": "What is the difference between a tool cabinet and a tool trolley?",
         "a": "A tool cabinet is a stationary chest (often with full-extension drawers) for high-density storage at one point. A trolley or mobile chest adds casters so the same tools travel bay to bay. Many Malaysian workshops buy one fixed cabinet plus one mobile trolley."},
        {"q": "How much weight can Tanko tool cabinet drawers hold?",
         "a": "Drawer ratings vary by model, but Tanko industrial cabinets use full-extension ball-bearing slides rated for daily industrial use, typically 30-50 kg per drawer depending on the line. Confirm the exact rating for the model you are looking at."},
        {"q": "Do the drawers lock securely?",
         "a": "Yes — Tanko tool cabinets include a central locking system that locks all drawers with one key turn, with an optional padlock hasp. This is standard on industrial chests used in shared workshops."},
        {"q": "Can a tool cabinet be used outdoors or in a humid factory?",
         "a": "Standard powder-coated steel cabinets suit dry indoor workshops. For humid or outdoor areas (common in parts of Malaysia), specify the corrosion-protected option or keep the cabinet in a sheltered bay."},
        {"q": "What sizes of tool cabinets do you keep in stock in Malaysia?",
         "a": "We keep the popular chest sizes (e.g. 7-12 drawer rolling cabinets and 2-3 bay drawer chests) in local stock at Selangor. Larger or custom drawer configurations are ordered to your specification with a confirmed lead time."},
    ],
    "cnc-tool": [
        {"q": "What is a CNC tool cabinet for?",
         "a": "A CNC tool cabinet stores tool holders (BT-30, BT-40, BT-50, HSK, ISO) in fitted drawers so the precision taper stays free of chips, coolant and moisture — protecting both the holder and the machine spindle."},
        {"q": "Which tool holder sizes do you support?",
         "a": "Tanko CNC tool storage covers BT-30, BT-40, BT-50, HSK and ISO holders, with drawer inserts and tool discs matched to each taper. Tell us your holder mix and we will configure the drawers."},
        {"q": "Do you supply CNC tool trolleys for moving tools to the machine?",
         "a": "Yes. Tanko offers CNC tool trolleys (open and drawer types) on casters so holders can travel from the tool room to the machine and back, reducing downtime on machining lines."},
        {"q": "How many tools can a CNC cabinet hold?",
         "a": "It depends on the model and drawer layout. A tall drawer-type cabinet can hold 40-100+ holders depending on tool length and diameter. We can calculate capacity from your tool inventory."},
        {"q": "Do you install CNC tool cabinets in Malaysia?",
         "a": "We deliver nationwide and can arrange on-site placement and configuration. Most clients do the final layout themselves with our drawing support, since drawer inserts are tool-specific."},
    ],
    "workstation": [
        {"q": "What is a modular workstation?",
         "a": "A modular workstation is a configurable assembly or production bench built on a common frame, to which drawer units, pegboards, overhead shelving, lighting and power can be added to match one specific job or line position."},
        {"q": "Can workstations be reconfigured later?",
         "a": "Yes — that is the point of a modular system. You can add, move or remove drawers, shelves, lights and power bars as the process changes, instead of replacing the whole bench."},
        {"q": "Are workstations suitable for electronics assembly in Malaysia?",
         "a": "Very. Modular workstations support ESD grounding, anti-static mats, clean laminate tops and task lighting — common requirements for electronics assembly and inspection lines. Ask about ESD options."},
        {"q": "What lead time for a full workstation line?",
         "a": "Standard modular parts are kept in stock. For a complete multi-station line we will confirm layout, quantities and lead time in a written quote — typically a few weeks including freight."},
        {"q": "Can you help design the workstation layout?",
         "a": "Yes — send us your process description, line length and the items each operator needs, and we will propose a workstation layout with a bill of materials for your approval."},
    ],
    "rack": [
        {"q": "What are mould racks used for?",
         "a": "Mould racks are heavy-duty steel racks that store injection moulds and die sets vertically, using support arms so each mould slides in and out on its own level — protecting mould faces and saving floor space."},
        {"q": "How much weight can a mould rack hold?",
         "a": "Load ratings depend on the rack configuration and mould width. Two- and three-column Tanko mould racks are sized for production moulds; tell us your heaviest mould and we will spec the frame and arm spacing."},
        {"q": "Do you provide pull-out racks for heavy tooling?",
         "a": "Yes — pull-out racks let heavy moulds or fixtures be drawn out for crane or hoist access. They suit tool rooms where moulds are too heavy for manual handling."},
        {"q": "Can mould racks be customised to my mould sizes?",
         "a": "Within the Tanko modular range, arm height and shelf spacing are adjustable to match your mould dimensions. Provide your mould list and we will confirm a fitting layout."},
    ],
    "hanger-rack": [
        {"q": "What is a hanger rack?",
         "a": "A hanger rack is a frame with perforated panels and shelves used for tool control, workshop layout and technical display — commonly seen in 5S workshops for storing long tools and materials."},
        {"q": "Can hanger racks be moved around the workshop?",
         "a": "Some models are mobile with casters, others are fixed. Mobile versions are useful when tools must follow the work area; fixed versions suit permanent 5S shadow-board stations."},
        {"q": "What accessories fit on a hanger rack?",
         "a": "Perforated boards, hooks, hangers, shelves and small bins snap onto the frame, so you can tailor each station to the tools actually used there."},
    ],
    "locker": [
        {"q": "What are Tanko steel lockers used for?",
         "a": "Multi-compartment steel lockers provide secure personal storage for factory workers, gym members, students and facility staff — with key or combination locks depending on the model."},
        {"q": "Combination or key lock — which is better for a factory?",
         "a": "Combination locks remove the cost and hassle of key management and lost keys, so they are popular in factories and gyms. Key locks suit situations where only one person should ever open a specific locker."},
        {"q": "How many compartments can a locker have?",
         "a": "Configurations range from single full-height lockers up to multi-compartment units. Choose based on how many staff you need to cover per locker bay and how much each person stores."},
        {"q": "Do lockers ship fully assembled?",
         "a": "Most arrive with minimal assembly (bolt-together legs and doors). We can arrange assembly on site for larger installations if needed."},
    ],
    "parts-cabinet": [
        {"q": "What are parts cabinets used for?",
         "a": "Parts cabinets keep fasteners, spares, and small components visible and countable at service benches and spares rooms — combining transparent drawers or bins with labelled storage."},
        {"q": "Parts cabinet or bins — what is the difference?",
         "a": "Cabinets are framed units with drawers for heavier or bulkier stock; bins (tilt-out, hanging or floor) are lighter modular systems for smaller quantities. Many spares rooms use a mix of both."},
        {"q": "Can parts bins be wall mounted?",
         "a": "Yes — hanging and back-mounted bins attach to perforated boards or rails, keeping frequently used small parts at eye level without occupying bench or floor space."},
    ],
    "documents-cabinet": [
        {"q": "What are document cabinets used for in a factory?",
         "a": "A4 document cabinets keep QA records, job cards, drawings and manuals at the point of use — desktop or floor-standing — so paperwork stays organised and retrievable on the shop floor."},
        {"q": "Desktop or floor-standing document cabinet?",
         "a": "Desktop units suit small volumes kept at a work position; floor-standing units suit larger filing needs in offices and QA stations. Choose by the volume you need within reach."},
    ],
    "perforated-board": [
        {"q": "What is a perforated board / pegboard used for?",
         "a": "Perforated boards (pegboards) hold hooks, hangers and small bins for visible tool storage — the basis of shadow-board tool control in 5S workshops."},
        {"q": "What is shadow-board tool control?",
         "a": "Shadow boarding is marking the outline of each tool on the board so every tool has a marked home. It makes missing tools obvious at a glance and is a core 5S practice."},
        {"q": "Do you supply hooks for Tanko perforated boards?",
         "a": "Yes — Tanko supplies a full range of steel, plastic and stainless hooks, hangers and specialist holders that fit the perforated-board pattern. Tell us the tools and we will recommend the hooks."},
    ],
    "household-items": [
        {"q": "Are Tanko household storage items the same quality as the industrial range?",
         "a": "Tanko household chests and storage units use the same steel fabrication and powder-coating quality as the industrial range, sized for home and light-commercial use."},
        {"q": "Do you sell household storage in Malaysia?",
         "a": "Yes — household items are part of the Tanko catalogue we distribute. Delivery and ordering follow the same nationwide process as our industrial range."},
    ],
}

# Category slug -> guide slugs most relevant to that category (for internal
# linking on category pages). Only existing guide slugs are used.
CATEGORY_GUIDES = {
    "workbench": [
        "how-to-choose-a-workbench-malaysia",
        "workbench-top-material-guide-malaysia",
        "tanko-workbench-pricing-quote-guide-malaysia",
        "meja-kerja-industri-malaysia",
        "esd-anti-static-workbench-malaysia",
        "stainless-steel-workbench-food-pharma-malaysia",
        "heavy-duty-workbench-fabrication-welding-malaysia",
        "buying-tanko-malaysia-vs-importing-directly",
    ],
    "tool-cabinet": [
        "tool-cabinet-buying-guide-automotive-workshop-malaysia",
        "tool-cabinet-maintenance-longevity-malaysia",
        "kabinet-alat-penyimpanan-bengkel-malaysia",
        "industrial-storage-solutions-malaysia",
    ],
    "cnc-tool": [
        "cnc-tool-storage-management-malaysia",
        "industrial-storage-solutions-malaysia",
    ],
    "workstation": [
        "modular-workstations-5s-workplace-organisation-malaysia",
        "5s-workplace-organisation-modular-storage-malaysia",
        "how-to-choose-a-workbench-malaysia",
    ],
    "rack": [
        "warehouse-racking-mould-rack-shelving-malaysia",
        "industrial-storage-solutions-malaysia",
    ],
    "hanger-rack": [
        "industrial-storage-solutions-malaysia",
    ],
    "locker": [
        "steel-locker-buying-guide-malaysia",
    ],
    "parts-cabinet": [
        "parts-bin-document-storage-spares-room-malaysia",
        "industrial-storage-solutions-malaysia",
    ],
    "documents-cabinet": [
        "parts-bin-document-storage-spares-room-malaysia",
    ],
    "perforated-board": [
        "perforated-board-shadow-board-tool-control-malaysia",
        "5s-workplace-organisation-modular-storage-malaysia",
        "modular-workstations-5s-workplace-organisation-malaysia",
    ],
    "household-items": [
        "industrial-storage-solutions-malaysia",
    ],
}
