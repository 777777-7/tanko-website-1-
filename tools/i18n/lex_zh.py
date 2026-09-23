# -*- coding: utf-8 -*-
"""Simplified-Chinese lexicon + composition rules for storagesystem.com.my.

Terminology follows Tanko's own Chinese catalogue, converted to Simplified and
adjusted for a Malaysian buyer (Ringgit, local warranty, Selangor stock).

Run:  python tools/i18n/lex_zh.py   ->  tools/i18n/glossary_zh.json
"""
import re, json, io, os

# ---------------------------------------------------------------- atomic terms
T = {
    # --- structural chrome
    "Home": "首页",
    "&mdash;": "&mdash;",
    "&rsquo;": "&rsquo;",
    "Details &rarr;": "详情 →",
    "Add to Basket": "加入询价单",
    "Full Specs &amp; Details": "完整规格与详情",
    "Variant Comparison": "型号比较",
    "Features": "产品特色",
    "Specification": "规格",
    "Product Specification": "产品规格",
    "How to choose": "选购指南",
    "Accessories": "配件",
    "Notes": "备注",
    "Note": "备注",
    "Related guides": "相关指南",
    "Product Ranges in this Category": "本类别产品系列",
    "Model lines, sizes and prices": "型号系列、尺寸与价格",
    "Model line": "型号系列",
    "Size (WxDxH)": "尺寸（宽x深x高）",
    "Top / material": "桌面 / 材质",
    "Variants": "款式",
    "Guide price": "参考价",
    "Request a quote": "索取报价",
    "talk to our team": "联系我们的团队",
    "or": "或",
    "All": "全部",
    "/unit": "/台",
    "POA": "价格面议",
    "mm": "mm",
    "Baca halaman ini dalam Bahasa Malaysia →": "Baca halaman ini dalam Bahasa Malaysia →",

    # --- measurement labels
    "Model": "型号",
    "Model No.": "型号",
    "Model&nbsp;No.": "型号",
    "Dimensions": "尺寸",
    "Dimensions (WxDxH)": "尺寸（宽x深x高）",
    "Inner Dimensions": "内部尺寸",
    "Inner dimensions": "内部尺寸",
    "Outer Dimensions": "外部尺寸",
    "Material": "材质",
    "Material : Steel": "材质：钢制",
    "Load": "承重",
    "Loading": "承重",
    "Color": "颜色",
    "Colour": "颜色",
    "Qty": "数量",
    "Type": "类型",
    "Top": "桌面",
    "Panel": "面板",
    "Panel set": "面板组",
    "Panel Set": "面板组",
    "Items included": "内含配件",
    "Items Included": "内含配件",
    "Unit of measurement": "单位",
    "Unit of measurement：mm": "单位：mm",
    "Drawer Height": "抽屉高度",
    "Holders Qty": "支架数量",
    "Shelf Qty": "层板数量",
    "Workbench Loading": "工作桌承重",
    "Drawer Loading": "抽屉承重",
    "Top option": "桌面选配",
    "Desktop": "桌面",
    "Drawer/Cabinet": "抽屉/柜体",
    "(holders specification)": "（支架规格）",

    # --- materials
    "Steel": "钢制",
    "steel": "钢制",
    "Steel Top": "钢制桌面",
    "Steel top": "钢制桌面",
    "Stainless steel": "不锈钢",
    "Stainless Steel": "不锈钢",
    "304 stainless steel": "304 不锈钢",
    "Wood": "木质",
    "Rubber mat": "橡胶垫",
    "PVC mat": "PVC 垫",
    "ABS": "ABS",
    "PP": "PP",
    "PS": "PS",
    "PS (transparent)": "PS（透明）",
    "ABS (gray)": "ABS（灰色）",
    "Rubber wood": "橡胶木",
    "Plywood": "合板",
    "White": "白色",
    "Gray": "灰色",
    "Black": "黑色",

    # --- tops
    "Workbench-top": "工作桌桌面",
    "Workbench-Top": "工作桌桌面",
    "Ｗorkbench-Top": "工作桌桌面",
    "Rubber top(N)": "橡胶桌面(N)",
    "Laminate top(F)": "美耐板桌面(F)",
    "Wood top(W)": "木质桌面(W)",
    "Stainless steel top(S)": "不锈钢桌面(S)",
    "Rubber wood top(W)": "橡胶木桌面(W)",
    "Rubber(N)": "橡胶(N)",
    "Laminate(F)": "美耐板(F)",
    "Wood(W)": "木质(W)",
    "Stainless steel(S)": "不锈钢(S)",
    "Laminate top": "美耐板桌面",
    "Rubber top": "橡胶桌面",
    "Wood top": "木质桌面",
    "Tanko-top(TG)": "Tanko 桌面(TG)",
    "Tanko-top(TH)": "Tanko 桌面(TH)",
    "Tanko top(TG)&amp;(TH)": "Tanko 桌面 (TG) 及 (TH)",
    "Tanko (Malaysia distributor: Primaxs) top(T)":
        "Tanko（马来西亚总代理：Primaxs）桌面(T)",

    # --- product families
    "Workbenches": "工作桌",
    "Workbench": "工作桌",
    "Workbench Accessories": "工作桌配件",
    "Tool Cabinet": "工具柜",
    "Tool Cabinets": "工具柜",
    "Tool cabinet": "工具柜",
    "Perforated Board": "洞洞板",
    "Perforated board": "洞洞板",
    "Perforated Boards": "洞洞板",
    "Perforated boards": "洞洞板",
    "Hooks": "挂钩",
    "Hangers": "吊挂架",
    "Holders": "支架",
    "Tool Holders": "工具支架",
    "Modular Workstations": "模组式工作站",
    "Workstation": "工作站",
    "CNC Tool Storage": "CNC 刀具存放",
    "CNC Trolley": "CNC 刀具推车",
    "CNC Tool Cabinet with Door": "带门 CNC 刀具柜",
    "Parts Cabinet": "零件柜",
    "Parts Cabinets": "零件柜",
    "Parts cabinet": "零件柜",
    "Hanger Racks": "挂架",
    "Documents Cabinets": "文件柜",
    "Display Stand": "展示架",
    "Trolley": "推车",
    "Tilt Out Bins Cart": "斜口料盒推车",
    "Packing Station": "包装工作站",
    "Storage cabinet": "储物柜",
    "Cabinet": "柜体",
    "Cabinet ▸ Steel": "柜体 ▸ 钢制",
    "Hanging Cabinet": "吊柜",
    "Hanging cabinet": "吊柜",
    "Wall cabinet": "壁柜",
    "Top chest": "上置工具箱",
    "Drawer": "抽屉",
    "Drawers": "抽屉",
    "Drawer set": "抽屉组",
    "Standard drawer": "标准抽屉",
    "Shelf": "层板",
    "Undershelf": "下层板",
    "Socket": "插座",
    "Light": "照明灯",
    "LED Light": "LED 灯",
    "Shelf &amp; LED Light": "层板与 LED 灯",
    "Universal socket": "万用插座",
    "Power tower": "电源柱",
    "Division boxes": "分隔盒",
    "Adjustable dividers": "可调分隔片",
    "Bottom tray": "底盘",
    "Anti-static mat": "防静电垫",
    "Hooks Set": "挂钩组",
    "Bin Hanger": "料盒挂架",
    "Hanging bin": "挂式料盒",
    "Hanging Bin Set": "挂式料盒组",
    "Monitor Arm": "屏幕支臂",
    "Bottle Holder": "瓶架",
    "Louvred Board": "百叶板",
    "Stainless Steel Perforated Board": "不锈钢洞洞板",
    "Metal Hook": "金属挂钩",
    "Plastic Hook": "塑胶挂钩",
    "Stainless Steel Hook": "不锈钢挂钩",
    "L hook": "L 型挂钩",
    "V hook": "V 型挂钩",
    "Closed end hook - L": "闭口挂钩 - L",
    "Closed end hook - S": "闭口挂钩 - S",
    "Loop hook-S": "环形挂钩 - S",
    "Loop hook-M": "环形挂钩 - M",
    "Loop hook-L": "环形挂钩 - L",
    "T Handle Holder": "T 型把手支架",
    "Clip Holder": "夹具支架",
    "Screwdriver Holder": "螺丝起子支架",
    "Drill Holder": "钻头支架",
    "Wrench Holder": "扳手支架",
    "Tray": "托盘",

    # --- grades / variants
    "Standard": "标准型",
    "Professional": "专业型",
    "Heavy Duty": "重型",
    "Performance": "高效型",
    "Hexagonal": "六角型",
    "Mobile": "移动式",
    "Stand-alone": "独立式",
    "Independent": "独立式",
    "Linkable": "可连接式",
    "Linkable type": "连接型",
    "Independent type": "独立型",

    # --- features
    "With lock": "附锁",
    "With leveler screws": "附调整脚",
    "Combination lock": "密码锁",
    "Drawer latch": "抽屉卡扣",
    "Drawer stop design": "抽屉止挡设计",
    "Colored label": "彩色标签",
    "Transparent front window": "透明前窗",
    "Made in Taiwan": "台湾制造",
    "DIY product, Made in Taiwan": "DIY 组装产品，台湾制造",
    "Full length aluminum handles and labels": "全长铝制把手与标签",
    "Hooks can be applied to perforated boards.":
        "挂钩可搭配洞洞板使用。",
    "Power plugs not included": "不含插头",
    "※ Power plugs not included": "※ 不含插头",
    "Made for 304 stainless steel. Durable and easy to clean.":
        "采用 304 不锈钢制造，耐用且易于清洁。",
    "Universal socket 110V~220V x 2": "万用插座 110V~220V x 2",
    "20W LED Light": "20W LED 灯",
    "10mm Rubber mat (P)": "10mm 橡胶垫 (P)",
    "12mm PVC mat (Q)": "12mm PVC 垫 (Q)",
    "Covered with P : 10mm Rubber mat Q : 12mm PVC mat":
        "覆面 P：10mm 橡胶垫　Q：12mm PVC 垫",
    "Rubber wood / 304 Stainless steel": "橡胶木 / 304 不锈钢",
    "White / Black": "白色 / 黑色",
    "■gray □white ■red": "■灰 □白 ■红",
    "■blue ■black": "■蓝 ■黑",
    "4&#34; PU castors": "4寸 PU 脚轮",

    # --- drawer codes
    "EA": "EA", "EB": "EB", "ED": "ED",
    "EA drawer": "EA 抽屉",
    "EB drawer": "EB 抽屉",
    "ED drawer": "ED 抽屉",
    "EA (standard drawer)": "EA（标准抽屉）",
    "EB (standard drawer)": "EB（标准抽屉）",
    "ED (standard drawer)": "ED（标准抽屉）",
    "EA (T drawer)": "EA（T 型抽屉）",
    "EB (T drawer)": "EB（T 型抽屉）",
    "ED (T drawer)": "ED（T 型抽屉）",
    "EA (panel set)": "EA（面板组）",
    "EB (panel set)": "EB（面板组）",
    "Pole x 1 (2 pcs)": "立柱 x 1（2 件）",

    # --- long prose
    "Manufactured in Taiwan by Tanko &middot; Malaysia stock &middot; nationwide delivery. "
    "Not all combinations are stocked — request a quote to confirm lead time.":
        "由 Tanko 天钢台湾原厂制造 &middot; 马来西亚现货 "
        "&middot; 全国配送。并非所有组合都备有库存"
        "——请索取报价以确认交期。",
    "Primaxs Marketing (M) Sdn Bhd is the exclusive Malaysia distributor for Tanko. "
    "Nationwide delivery from our Selangor warehouse, Ringgit pricing and local warranty.":
        "Primaxs Marketing (M) Sdn Bhd 是 Tanko 天钢在马来西亚的"
        "独家总代理，由雪兰莪仓库发货至全国，以马币报价并提供本地保固。",
    "Anti-static mat is optional, includes 2 snaps and 1 grounding wire. "
    "RoHS 2.0 compliant Surface resistance: 10⁷ – 10⁹ Ω":
        "防静电垫为选配，附 2 个接地扣及 1 条接地线。"
        "符合 RoHS 2.0，表面电阻：10⁷ – 10⁹ Ω",
    "High density fiberboard(HDF) covered with green rubber mat on top and PVC protection "
    "on four edges. Machine maintenance, normal factories, production line and garages.":
        "高密度纤维板（HDF）表面覆绿色橡胶垫，"
        "四边 PVC 包边。适用于机械保养、一般工厂、"
        "生产线与汽修厂。",
    "Plywood top covered with gray laminate and PVC protective edges, great performance in "
    "high temperature environment. All electronics companies, research labs, hospitals, "
    "workshop and metrology department.":
        "合板桌面覆灰色美耐板，四边 PVC 包边，"
        "耐高温表现优异。适用于电子厂、研发"
        "实验室、医院、工作坊与计量部门。",
    "High density material covered with 1.2mm stainless steel sheet. Tool makers, workshops, "
    "research labs.":
        "高密度板材表面覆 1.2mm 不锈钢板。适用于"
        "模具厂、工作坊与研发实验室。",
    "Finger-jointed rubber wood to ensure high durability. Tool makers, equipment maintenance.":
        "指接橡胶木制造，耐用度高。适用于模具"
        "厂与设备保养。",
    "Multi-layer laminate and PVC protection on four edges. Research labs, schools.":
        "多层美耐板，四边 PVC 包边。适用于研发"
        "实验室与学校。",
    "Rubber, laminate, wood, stainless steel and Tanko (Malaysia distributor: Primaxs) top.":
        "橡胶、美耐板、木质、不锈钢及 Tanko"
        "（马来西亚总代理：Primaxs）桌面。",
    "Wood top, laminate top and rubber top.":
        "木质桌面、美耐板桌面与橡胶桌面。",
    "Laminate top, Rubber top, Wood top":
        "美耐板桌面、橡胶桌面、木质桌面",
    "Laminate, Rubber, Wood": "美耐板、橡胶、木质",
    "Laminate, Rubber, Stainless steel": "美耐板、橡胶、不锈钢",
    "Rubber top(N), Laminate top(F)": "橡胶桌面(N)、美耐板桌面(F)",
    "Rubber wood top(W), Stainless steel top(S)":
        "橡胶木桌面(W)、不锈钢桌面(S)",
    "Ｗorkbench-Top Tanko (Malaysia distributor: Primaxs) top : (H)36mm,43mm Others : (H)50mm":
        "工作桌桌面　Tanko（马来西亚总代理：Primaxs）"
        "桌面：(H)36mm、43mm　其他：(H)50mm",
    "Stocked in Seri Kembangan, Selangor, with free delivery and installation in Selangor and "
    "Kuala Lumpur; nationwide delivery arranged on request. 1-year warranty against "
    "manufacturing defects, administered locally.":
        "现货存放于雪兰莪Seri Kembangan，"
        "雪兰莪及吉隆坡免费配送与安装；全国"
        "配送可依需求安排。产品提供一年制造"
        "瑕疵保固，由本地直接受理。",
}

# --------------------------------------------------- second pass: further terms
T.update({
    "Sink cabinet": "水槽柜",
    "Wastebin cabinet": "垃圾柜",
    "Mobile Tool Cabinet": "移动式工具柜",
    "Classic Workstation": "经典型工作站",
    "Professional Workstation": "专业型工作站",
    "Heavy Duty Workbench": "重型工作桌",
    "Professional Workbench": "专业型工作桌",
    "Performance Workbench": "高效型工作桌",
    "Steel Top Workbench": "钢制桌面工作桌",
    "Stainless Steel Workbench": "不锈钢工作桌",
    "Hexagonal Workbench": "六角型工作桌",
    "Packing Station Workbench": "包装工作站",
    "Benchwork": "钢制面工作桌",
    "Mould Rack": "模具架",
    "Pull-out Rack": "抽拉式货架",
    "Chest of Drawers": "抽屉柜",
    "Household Items": "居家用品",
    "Racks": "货架",
    "Rack": "货架",
    "Handle": "把手",
    "Dimension": "尺寸",
    "Width": "宽度",
    "Height": "高度",
    "Depth": "深度",
    "Ｗith divider": "附分隔片",
    "With divider": "附分隔片",
    "With panel": "附面板",
    "With shelves": "附层板",
    "(T= T drawer)": "（T = T 型抽屉）",
    "Ｗorkbench-Top (H) 50mm": "工作桌桌面（H）50mm",
    "Ｗorkbench-Top (H)50mm": "工作桌桌面（H）50mm",
    "Ｗorkbench-Top Thickness 50mm": "工作桌桌面厚度 50mm",
    "50° tilt out angle": "50° 斜口角度",
    "Universal socket 110V~220V . Power plugs not included.":
        "万用插座 110V~220V。不含插头。",
    "Power Tower Universal socket 110V~220V Air coupling (1 hole) Power plugs not included.":
        "电源柱　万用插座 110V~220V　气动接头"
        "（1 孔）　不含插头。",
    "Total holders = upper tray + 2 tool holder racks":
        "支架总数 = 上层托盘 + 2 组刀具支架",
    "Silde System Standard drawer : 90% extension T drawer : 100% extension":
        "滑轨系统　标准抽屉：90% 拉出　"
        "T 型抽屉：100% 拉出",
    "Steel / Desktop: Steel / 304 Stainless steel":
        "钢制 / 桌面：钢制 / 304 不锈钢",
    "Steel Desktop ： Rubber wood": "钢制　桌面：橡胶木",
    "Covered with P : 10mm black rubber mat Q : 12mm PVC mat":
        "覆面 P：10mm 黑色橡胶垫　Q：12mm PVC 垫",
    "Drawer height 50mm-150mm :": "抽屉高度 50mm-150mm：",
    "Drawer height 50mm-150mm : with 3x3 dividers":
        "抽屉高度 50mm-150mm：附 3x3 分隔片",
    "Drawer height over 200mm : with 2x2 dividers":
        "抽屉高度 200mm 以上：附 2x2 分隔片",
    "1st drawer height (50mm-100mm) : with division boxes":
        "第一层抽屉高度（50mm-100mm）：附分隔盒",
    "▲ Division boxes application": "▲ 分隔盒应用",
    "▲Division Boxes Application": "▲ 分隔盒应用",
    "▲ Partitions application": "▲ 分隔板应用",
    "▲Adjustable Partitions Application": "▲ 可调分隔板应用",
    "Tanko (Malaysia distributor: Primaxs) patented partitions":
        "Tanko（马来西亚总代理：Primaxs）专利分隔板",
})

# ------------------------------------------- third pass: FAQ headings and specs
T.update({
    # workbench FAQ
    "What size workbench do I need for a Malaysian workshop?":
        "马来西亚的工作坊该选多大的工作桌？",
    "Rubber, laminate, stainless steel or wood top — which is best?":
        "橡胶、美耐板、不锈钢还是木质桌面"
        "——哪一种最合适？",
    "Can I get a workbench with drawers, power sockets and a pegboard?":
        "工作桌可以加装抽屉、插座和洞洞板吗？",
    "How long does delivery take for workbenches in Malaysia?":
        "在马来西亚订购工作桌的交期多久？",
    "Do you sell to companies outside Selangor and KL?":
        "雪兰莪和吉隆坡以外的公司也能订购吗？",
    # tool cabinet FAQ
    "What is the difference between a tool cabinet and a tool trolley?":
        "工具柜和工具推车有什么区别？",
    "How much weight can Tanko tool cabinet drawers hold?":
        "Tanko 工具柜的抽屉能承重多少？",
    "Do the drawers lock securely?": "抽屉的锁具牢靠吗？",
    "Can a tool cabinet be used outdoors or in a humid factory?":
        "工具柜能用在户外或潮湿的厂房吗？",
    "What sizes of tool cabinets do you keep in stock in Malaysia?":
        "马来西亚现货备有哪些尺寸的工具柜？",
    # perforated board FAQ
    "What is a perforated board / pegboard used for?":
        "洞洞板（pegboard）用来做什么？",
    "What is shadow-board tool control?":
        "什么是影子板（Shadow Board）工具管理？",
    "Do you supply hooks for Tanko perforated boards?":
        "你们有供应搭配 Tanko 洞洞板的挂钩吗？",
    # workstation FAQ
    "What is a modular workstation?": "什么是模组式工作站？",
    "Can workstations be reconfigured later?":
        "工作站日后可以重新组合吗？",
    "Are workstations suitable for electronics assembly in Malaysia?":
        "工作站适合马来西亚的电子组装线吗？",
    "What lead time for a full workstation line?":
        "整条工作站产线的交期多久？",
    "Can you help design the workstation layout?":
        "你们能协助规划工作站的配置吗？",
    # CNC FAQ
    "What is a CNC tool cabinet for?": "CNC 刀具柜的用途是什么？",
    "Which tool holder sizes do you support?": "支持哪些刀柄规格？",
    "Do you supply CNC tool trolleys for moving tools to the machine?":
        "有供应把刀具送到机台的 CNC 刀具推车吗？",
    "How many tools can a CNC cabinet hold?":
        "一台 CNC 刀具柜能放多少把刀具？",
    "Do you install CNC tool cabinets in Malaysia?":
        "你们在马来西亚提供 CNC 刀具柜的安装服务吗？",
    "Fixed CNC cabinets: H1000, H1200 and mobile options":
        "固定式 CNC 刀具柜：H1000、H1200，另有移动式选项",
    "Total holders = 8 tool holder racks":
        "支架总数 = 8 组刀具支架",
    # parts cabinet FAQ
    "What are parts cabinets used for?": "零件柜有什么用途？",
    "Parts cabinet or bins — what is the difference?":
        "零件柜与料盒有什么区别？",
    "Can parts bins be wall mounted?": "料盒可以壁挂吗？",
    # hanger rack FAQ
    "What is a hanger rack?": "什么是挂架？",
    "Can hanger racks be moved around the workshop?":
        "挂架可以在厂房内移动吗？",
    "What accessories fit on a hanger rack?":
        "挂架可以搭配哪些配件？",
    # documents / locker / rack / household FAQ
    "What are document cabinets used for in a factory?":
        "文件柜在工厂里有什么用途？",
    "Desktop or floor-standing document cabinet?":
        "桌上型还是落地型文件柜？",
    "What are Tanko steel lockers used for?":
        "Tanko 钢制置物柜有什么用途？",
    "Combination or key lock — which is better for a factory?":
        "密码锁还是钥匙锁——工厂该选哪一种？",
    "How many compartments can a locker have?":
        "置物柜最多可以有几格？",
    "Do lockers ship fully assembled?":
        "置物柜出货时是整台组装好的吗？",
    "What are mould racks used for?": "模具架有什么用途？",
    "How much weight can a mould rack hold?": "模具架能承重多少？",
    "Do you provide pull-out racks for heavy tooling?":
        "有供应放重型模具的抽拉式货架吗？",
    "Can mould racks be customised to my mould sizes?":
        "模具架可以依照我的模具尺寸订制吗？",
    "Are Tanko household storage items the same quality as the industrial range?":
        "Tanko 的居家收纳产品和工业系列品质一样吗？",
    "Do you sell household storage in Malaysia?":
        "你们在马来西亚有销售居家收纳产品吗？",
    # spec fragments
    "Taiwan-manufactured, distributed in Malaysia Standard drawer ：100kg load capacity "
    "T drawer ：200kg load capacity":
        "台湾制造，马来西亚代理　标准抽屉："
        "承重 100kg　T 型抽屉：承重 200kg",
    "Taiwan-manufactured, distributed in Malaysia Standard drawer：100kg load capacity "
    "T drawer：200kg load capacity":
        "台湾制造，马来西亚代理　标准抽屉："
        "承重 100kg　T 型抽屉：承重 200kg",
    "Drawer height over than 200mm :": "抽屉高度 200mm 以上：",
    "Drawer height over than 300mm :": "抽屉高度 300mm 以上：",
    "Sensor working distance: 5 cm": "感应距离：5 cm",
    "Can be adjusted at a maximum of 90° angle.":
        "最大可调角度 90°。",
    "Lumen: 1100 lm(max) Rated Power Consumption: 15 W Maximum when connected with WP-9004: 27.5W":
        "流明：1100 lm（最大）　额定功耗：15 W　"
        "与 WP-9004 串接时最大：27.5W",
    "Cart Type Pro : Layer A, B, C with bins Standard : Layer A, B with bins":
        "推车型式　Pro：A、B、C 层附料盒　"
        "标准型：A、B 层附料盒",
    "Accessories Standard (Layer C) : Shelves and hanging bins are optional":
        "配件　标准型（C 层）：层板与挂式"
        "料盒为选配",
    "Unit of measurement：WxDxH mm": "单位：宽x深x高 mm",
    "Unit of measurement ： WxDxH mm": "单位：宽x深x高 mm",
    "Work with perforated boards. Suitable for all Tanko (Malaysia distributor: Primaxs) "
    "hanging bin .":
        "可搭配洞洞板使用，适用于所有 Tanko"
        "（马来西亚总代理：Primaxs）挂式料盒。",
    "Available ≤ 27&#34; LCD/TV": "适用 ≤ 27 寸 LCD/TV",
    "360° rotation": "360° 旋转",
    "Tilted up and down ±30°.": "上下倾斜 ±30°。",
    "s： Aluminum alloy, steel": "材质：铝合金、钢制",
    "Ø20 Ø60 Ø100 Load 5kg": "Ø20 Ø60 Ø100　承重 5kg",
    "Modular Rack【Independent】": "模组货架【独立式】",
    "Modular Rack【Linkable】": "模组货架【连接式】",
    "ABS + PC (transparent) （PC drawers are suitable for oily items.）":
        "ABS + PC（透明）（PC 抽屉适合存放油性"
        "物件。）",
    "TKI-2-9 抽屜75 pcs": "TKI-2-9 抽屉 75 件",
    "TKI-2-3 抽屜75 pcs": "TKI-2-3 抽屉 75 件",
    "Surface resistance：104 ~ 106 ohm": "表面电阻：104 ~ 106 ohm",
    "EGPL-2 Drawer Height 75mm Unit of measurement：mm":
        "EGPL-2　抽屉高度 75mm　单位：mm",
    "EKA Top Cover Dimensions：W709xD452xH68 mm Material：Steel Color：Red / Blue":
        "EKA 顶盖　尺寸：W709xD452xH68 mm　材质：钢制"
        "　颜色：红 / 蓝",
    "26mm C：900mm D：6mm": "26mm　C：900mm　D：6mm",
    "in Malaysia usually want one of two things: a":
        "在马来西亚通常有两种需求：",
})

try:
    from terms_zh import TERMS2
    from terms_pb_zh import TERMS_PB
    from terms_tc_zh import TERMS_TC
    from boiler_zh import BOILER
    from pb_prose_zh import PB_PROSE
    from tc_prose_zh import TC_PROSE
    from prose_zh import PROSE
except ImportError:
    from .terms_zh import TERMS2
    from .terms_pb_zh import TERMS_PB
    from .terms_tc_zh import TERMS_TC
    from .boiler_zh import BOILER
    from .pb_prose_zh import PB_PROSE
    from .tc_prose_zh import TC_PROSE
    from .prose_zh import PROSE
T.update(TERMS2)
T.update(TERMS_PB)
T.update(TERMS_TC)
T.update(BOILER)
T.update(PB_PROSE)
T.update(TC_PROSE)
T.update(PROSE)

# ------------------------------------------------------------ composition rules

def _n(m, fmt):
    return fmt % m.group(1)

NUM_RULES = [
    (r'^(\d+)\s*variants?$', "%s 款"),
    (r'^&middot;\s*(\d+)\s*variants?$', "&middot; %s 款"),
    (r'^(\d+)\s*sizes?$', "%s 种尺寸"),
    (r'^(\d+)\s*pcs\.?$', "%s 件"),
    (r'^(\d+)pcs$', "%s 件"),
    (r'^(\d+)\s*pcs\s*/\s*CTN$', "%s 件/箱"),
    (r'^(\d+)\s*configurations?\. Every variant below has its own detail page\.$',
     "共 %s 种组合，以下每一款都有独立的"
     "详情页面。"),
    (r'^(\d+)kg load capacity$', "承重 %skg"),
    (r'^(\d+)kg load capacity per drawer\.$', "每屉承重 %skg。"),
    (r'^Step&nbsp;(\d+)$', "步骤&nbsp;%s"),
    (r'^Step\.(\d+)$', "步骤 %s"),
]
NUM_RULES = [(re.compile(p), f) for p, f in NUM_RULES]

_PASS_CHARS = re.compile(
    r'^[\s\dA-Za-z×x\*/\.,\-\+\(\)\[\]–—▸\|&;#※■□'
    r'Ø≤≥°±_~"’\'：　]*$')


_UNITS = ('mm', 'cm', 'kg', 'pcs', 'ctn', 'max', 'min', 'pcs')
_DIM = re.compile(r'[WDHL]\d+(?:\.\d+)?(?:mm|cm)?', re.I)
_CODE = re.compile(r'\b(?:TG|TH|EA|EB|ED|PU|LED|PVC|ABS|PP|PS|HDF|CNC|BT|HSK|ISO|RM)\b')


def PASSTHRU_match(s):
    """True only for code-like strings: SKUs, dimensions, symbols.

    Deliberately strict. An earlier, looser version let whole English
    sentences through untranslated because they happened to be pure ASCII,
    which is exactly how a 'translated' page ends up still in English.
    """
    if not _PASS_CHARS.match(s):
        return False
    # strip the things that legitimately stay as-is, then see what prose is left
    rest = _DIM.sub(' ', s)
    rest = _CODE.sub(' ', rest)
    rest = re.sub(r'\b[A-Z]{1,5}[-_]?\d[A-Z0-9\-_]*\b', ' ', rest)   # SKUs
    words = [w for w in re.findall(r'[A-Za-z]{3,}', rest)
             if w.lower() not in _UNITS]
    if words:
        return False
    return len(s) <= 120


class _PassThru(object):
    match = staticmethod(PASSTHRU_match)


PASSTHRU = _PassThru()


def _rules(s):
    for rx, fmt in NUM_RULES:
        m = rx.match(s)
        if m:
            return fmt % m.group(1)
    # --- "X &mdash; Malaysia" (entity form of the em-dash)
    m = re.match(r'^(.+?) &mdash; Malaysia$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return "%s &mdash; 马来西亚" % sub

    # --- "The EGA-1 standard tool cabinet" style headings
    m = re.match(r'^The (.+)$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return sub

    # --- "Tool Cabinet - H1000"
    m = re.match(r'^(.+?) - (H\d+)$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return "%s - %s" % (sub, m.group(2))

    # --- "Something SKU-1234" : translate the prose, keep the model number
    m = re.match(r'^(.+?) ([A-Z]{2,4}-[\dA-Z][\dA-Z\-]*)$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return "%s %s" % (sub, m.group(2))

    # --- "Drawer height 50 mm"
    m = re.match(r'^Drawer height (\d+) ?mm$', s)
    if m:
        return "抽屉高度 %s mm" % m.group(1)

    # --- "EGL-185M (black)" : lowercase colour in parentheses
    LC = {'black': '黑色', 'red': '红色', 'blue': '蓝色',
          'gray': '灰色', 'grey': '灰色', 'white': '白色',
          'green': '绿色', 'yellow': '黄色'}
    m = re.match(r'^([A-Z][A-Z0-9\-]*) \(([a-z]+)\)$', s)
    if m and m.group(2) in LC:
        return "%s（%s）" % (m.group(1), LC[m.group(2)])

    # --- bare letter codes: KPQ-C, KPQ-B, TKI-8302x4
    if re.match(r'^[A-Z]{1,5}-[A-Z0-9]+(x\d+)?$', s):
        return s

    # --- meta description template:
    #     "NAME — N Tanko <category> variants with side-by-side specs, ..."
    m = re.match(r'^(.+?) — (\d+) Tanko (.+?) variants with side-by-side specs, '
                 r'dimensions and finishes\.', s)
    if m:
        name, n, cat = tr(m.group(1).strip()), m.group(2), tr(m.group(3).strip())
        if name and cat:
            return ("%s — %s 款%s，附规格、尺寸与"
                    "表面处理对照。由 Tanko 自 2006 年"
                    "起的马来西亚独家总代理 Primaxs "
                    "供应。" % (name, n, cat))

    # --- "X range within our Y — N model lines from Tanko, ..."
    m = re.match(r'^(.+?) range within our (.+?) — (\d+) model lines from Tanko, '
                 r'distributed in Malaysia by Primaxs\. Compare options and request a quo', s)
    if m:
        name, cat, n = tr(m.group(1).strip()), tr(m.group(2).strip()), m.group(3)
        if name and cat:
            return ("%s系列，隶属%s — 共 %s 个 Tanko 型号"
                    "系列，由 Primaxs 在马来西亚供应。"
                    "欢迎比较选配并索取报价。"
                    % (name, cat, n))

    # --- "from RM12.05"
    m = re.match(r'^from (RM[\d,.]+)$', s)
    if m:
        return "%s 起" % m.group(1)

    # --- "KQ-306A (BLACK)" / "KPQ-4302 (BLACK)(ANTI-STATIC)"
    COLOURS = {'RED': '红色', 'BLUE': '蓝色', 'YELLOW': '黄色',
               'BLACK': '黑色', 'GRAY': '灰色', 'GREY': '灰色',
               'WHITE': '白色', 'GREEN': '绿色', 'ORANGE': '橙色',
               'PINK': '粉色', 'STAINLESS STEEL': '不锈钢'}
    m = re.match(r'^([A-Z]{1,4}-[\dA-Z]+)\s*\(([A-Z ]+)\)(\(ANTI-STATIC\))?$', s)
    if m and m.group(2) in COLOURS:
        tail = '（防静电）' if m.group(3) else ''
        return "%s（%s）%s" % (m.group(1), COLOURS[m.group(2)], tail)

    # --- "About the X" / "About X"
    m = re.match(r'^About (?:the )?(.+)$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return "关于%s" % sub

    # --- "KP-4802 drawing" / "KPQ-C view 2"
    m = re.match(r'^([A-Z][A-Z0-9\-]*) drawing$', s)
    if m:
        return "%s 图面" % m.group(1)
    m = re.match(r'^([A-Z][A-Z0-9\-]*) view (\d+)$', s)
    if m:
        return "%s 视图 %s" % (m.group(1), m.group(2))

    # --- hooks: "Single hook (L80)", "U hook (6pcs)", "Hooks Set (12pcs)"
    m = re.match(r'^(.+?) \((L\d+)\)$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return "%s（%s）" % (sub, m.group(2))
    m = re.match(r'^(.+?) \((\d+)pcs\)$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return "%s（%s 件）" % (sub, m.group(2))

    # --- "7 types" / "8 colors" / "18 clips"
    m = re.match(r'^(\d+) (types|colors|colours|clips)$', s)
    if m:
        unit = {'types': '种类型', 'colors': '种颜色',
                'colours': '种颜色', 'clips': '个夹'}[m.group(2)]
        return "%s %s" % (m.group(1), unit)

    # --- "3-6kg load capacity"
    m = re.match(r'^([\d\-]+)kg load capacity$', s)
    if m:
        return "承重 %skg" % m.group(1)

    # --- page <title>: "X Malaysia [— from RM9,999] | Primaxs"
    m = re.match(r'^(.+?) Malaysia(?: — from (RM[\d,]+))? \| Primaxs$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            if m.group(2):
                return "马来西亚%s — %s 起 | Primaxs" % (sub, m.group(2))
            return "马来西亚%s | Primaxs" % sub

    # --- "X — Malaysia | Primaxs"
    m = re.match(r'^(.+?) — Malaysia \| Primaxs$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return "%s — 马来西亚 | Primaxs" % sub

    # --- generic "X | Primaxs" (after the more specific title rules above)
    m = re.match(r'^(.+?) \| Primaxs$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return "%s | Primaxs" % sub

    # --- plural family names: "Heavy Duty Workbenches" -> singular lookup
    m = re.match(r'^(.+?)(Workbenches|Cabinets|Racks|Stations|Boards|Lockers|Trolleys)$', s)
    if m:
        singular = {'Workbenches': 'Workbench', 'Cabinets': 'Cabinet', 'Racks': 'Rack',
                    'Stations': 'Station', 'Boards': 'Board', 'Lockers': 'Locker',
                    'Trolleys': 'Trolley'}[m.group(2)]
        sub = tr((m.group(1) + singular).strip())
        if sub:
            return sub

    # --- "... ※ Power plugs not included"
    m = re.match(r'^(.+?)\s*※ Power plugs not included$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return "%s ※ 不含插头" % sub

    # --- "Name ❘ SKU"  (light vertical bar used in hanger rack titles)
    m = re.match(r'^(.+?)\s*❘\s*([A-Z][A-Z0-9\-]*)$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return "%s｜%s" % (sub, m.group(2))

    # --- "Name (TKI-8305)"
    m = re.match(r'^(.+?)\s*\(([A-Z]{1,4}-?\d[A-Z0-9\-]*(?: [A-Z ]+)?)\)$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return "%s（%s）" % (sub, m.group(2))

    # --- "Name — 5 sizes" / "— 3 drawer sizes" / "— 4 styles" / "— 2 columns"
    m = re.match(r'^(.+?) — (\d+) (drawer sizes|sizes|styles|columns?|Drawer types)$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            unit = {'drawer sizes': '种抽屉尺寸',
                    'sizes': '种尺寸', 'styles': '种款式',
                    'column': '排', 'columns': '排',
                    'Drawer types': '种抽屉形式'}[m.group(3)]
            return "%s — %s %s" % (sub, m.group(2), unit)

    # --- "Documents cabinet (Desktop) — 2 columns"
    m = re.match(r'^(.+?) \((Desktop|Floor-standing|With doors)\) — (\d+) columns?$', s)
    if m:
        sub = tr(m.group(1).strip())
        place = {'Desktop': '桌上型', 'Floor-standing': '落地型',
                 'With doors': '附门'}[m.group(2)]
        if sub:
            return "%s（%s）— %s 排" % (sub, place, m.group(3))

    # --- "Tool Cabinet - H700 — Heavy Duty"
    m = re.match(r'^(.+?) - (H\d+) — (.+)$', s)
    if m:
        a, b = tr(m.group(1).strip()), tr(m.group(3).strip())
        if a and b:
            return "%s - %s — %s" % (a, m.group(2), b)

    # --- "Tanko-top(TG)D650"
    m = re.match(r'^Tanko-top\((T[GH])\)(D\d+)$', s)
    if m:
        return "Tanko 桌面(%s)%s" % (m.group(1), m.group(2))

    # --- "X is optional" / "X are optional"
    m = re.match(r'^(.+?) (?:is|are) optional\.?$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return "%s为选配%s" % (sub, '。' if s.endswith('.') else '')

    # --- "NNNkg load capacity." with trailing stop
    m = re.match(r'^(\d+)kg load capacity\.$', s)
    if m:
        return "承重 %skg。" % m.group(1)
    m = re.match(r'^(\d+)kg load capacity per drawer$', s)
    if m:
        return "每屉承重 %skg" % m.group(1)

    # "Workbench loading capacity: NNNkg"
    m = re.match(r'^Workbench loading capacity: (\d+kg)$', s)
    if m:
        return "工作桌承重：%s" % m.group(1)
    # "EA Heavy Duty Tool Cabinet (T= T drawer)"
    m = re.match(r'^(E[ABD]) (.+) \(T= T drawer\)$', s)
    if m:
        sub = tr(m.group(2))
        if sub:
            return "%s %s（T = T 型抽屉）" % (m.group(1), sub)
    # "-> SKU  <top list>"
    m = re.match(r'^→ ([A-Z][A-Z0-9\-]*)\s+(.+)$', s)
    if m:
        sub = tr(m.group(2))
        if sub:
            return "→ %s %s" % (m.group(1), sub)
    # "Rubber top( N ), Laminate top( F )" - spaced code variant
    m = re.match(r'^(.+?)\(\s*([A-Z])\s*\)(.*)$', s)
    if m and m.group(3).strip() in ('', ','):
        base = tr(m.group(1).strip())
        if base:
            return "%s(%s)%s" % (base, m.group(2), m.group(3))
    # "Loop hook-S (Ø20)" style: name + parenthesised dimension
    m = re.match(r'^(.+?)\s*\((Ø[\dA-Za-z×x]+(?:mm)?)\)$', s)
    if m:
        sub = tr(m.group(1).strip())
        if sub:
            return "%s（%s）" % (sub, m.group(2))
    # "Sourcing X in Malaysia?"
    m = re.match(r'^Sourcing (.+) in Malaysia\?$', s)
    if m:
        sub = tr(m.group(1))
        if sub:
            return "在马来西亚采购%s？" % sub
    # "A: B — Malaysia" page titles
    m = re.match(r'^(.+?): (.+?) — Malaysia$', s)
    if m:
        a, b = tr(m.group(1)), tr(m.group(2))
        if a and b:
            return "%s：%s — 马来西亚" % (a, b)
    m = re.match(r'^(.+?) — Malaysia$', s)
    if m:
        a = tr(m.group(1))
        if a:
            return "%s — 马来西亚" % a
    # "SKU｜Name" / "SKU❘Name"
    m = re.match(r'^([A-Z][A-Z0-9\-_]*)\s*[｜❘]\s*(.+)$', s)
    if m:
        sub = tr(m.group(2))
        if sub:
            return "%s｜%s" % (m.group(1), sub)
    # "Name — Variant ❘ SKU"
    m = re.match(r'^(.+?)\s*[｜❘]\s*([A-Z][A-Z0-9\-_]*)$', s)
    if m:
        sub = tr(m.group(1))
        if sub:
            return "%s｜%s" % (sub, m.group(2))
    # "□ : Workbench-Top → SKU"
    m = re.match(r'^□ : (.+?) → (.+)$', s)
    if m:
        sub = tr(m.group(1))
        if sub:
            return "□：%s → %s" % (sub, m.group(2))
    # "Dimensions : W..mmxD..mmxH..mm"
    m = re.match(r'^Dimensions? ?: ?(W[\dA-Za-z×x]+)$', s)
    if m:
        return "尺寸：%s" % m.group(1)
    # "NN% extension/extention [with NNkg load capacity]"
    m = re.match(r'^(\d+)% ext[a-z]+(?: with (\d+)kg load capacity)?$', s)
    if m:
        if m.group(2):
            return "%s%% 拉出，承重 %skg" % (m.group(1), m.group(2))
        return "%s%% 拉出" % m.group(1)
    # "loading：NNkg" and "X loading：NNkg"
    m = re.match(r'^(.*?)\s*[Ll]oading：(\d+kg)$', s)
    if m:
        pre = m.group(1).strip()
        if not pre:
            return "承重：%s" % m.group(2)
        sub = tr(pre)
        if sub:
            return "%s承重：%s" % (sub, m.group(2))
    # "Universal socket 110V~220V x N ..."
    m = re.match(r'^Universal socket 110V~220V x (\d+)(.*)$', s)
    if m:
        tail = m.group(2)
        tail = tail.replace('※ Power plugs not included', '※ 不含插头')
        tail = tail.replace('20W LED Light', '20W LED 灯')
        return "万用插座 110V~220V x %s%s" % (m.group(1), tail)
    # field blocks: "Dimensions：X Material：Y Color：Z Loading：W"
    if re.search(r'：', s) and re.search(
            r'^(Dimensions?|Material|Color|Colour|Handle|Loading|Shelf|Drawer|Desktop|Steel)', s):
        FIELD = {'Dimensions': '尺寸', 'Dimension': '尺寸', 'Material': '材质',
                 'Color': '颜色', 'Colour': '颜色', 'Handle': '把手',
                 'Loading': '承重', 'Shelf': '层板', 'Drawer': '抽屉',
                 'Desktop': '桌面', 'Items Included': '内含配件'}
        VAL = {'Steel': '钢制', 'Gray': '灰色', 'Black': '黑色',
               'White': '白色', 'Red': '红色', 'ABS': 'ABS', 'PP': 'PP',
               'Rubber wood': '橡胶木', 'per drawer': '/屉',
               'per shelf': '/层板', 'load capacity': '承重'}
        out = s
        for k in sorted(FIELD, key=len, reverse=True):
            out = re.sub(r'\b%s\b(?=\s*：)' % re.escape(k), FIELD[k], out)
        for k in sorted(VAL, key=len, reverse=True):
            out = re.sub(r'\b%s\b' % re.escape(k), VAL[k], out)
        if out != s:
            return out
    m = re.match(r'^Step\.(\d+)\s+(.+)$', s)
    if m:
        sub = tr(m.group(2))
        if sub:
            return "步骤 %s %s" % (m.group(1), sub)
    m = re.match(r'^(\d+)\s*variants? &middot; (.+)$', s)
    if m:
        sub = tr(m.group(2))
        if sub:
            return "%s 款 &middot; %s" % (m.group(1), sub)
    m = re.match(r'^(.*?)\((H\d+)\)$', s)
    if m:
        base = T.get(m.group(1).strip())
        if base:
            return "%s(%s)" % (base, m.group(2))
    if "—" in s:
        a, _, b = s.partition("—")
        ta, tb = tr(a.strip()), tr(b.strip())
        if ta and tb:
            return "%s — %s" % (ta, tb)
    return None


def _compose(s):
    """Translate X+Y+Z and X / Y part by part."""
    for sep, join in (("+", "+"), (" / ", " / ")):
        if sep in s:
            outs = []
            for p in s.split(sep):
                t = tr(p.strip())
                if t is None:
                    return None
                outs.append(t)
            return join.join(outs)
    return None


_CI = None


def _ci_lookup(s):
    """Case-insensitive fallback: 'perforated boards' finds 'Perforated Boards'."""
    global _CI
    if _CI is None:
        _CI = {}
        for k, v in T.items():
            _CI.setdefault(k.lower(), v)
    return _CI.get(s.lower())


def tr(s):
    if s in T:
        return T[s]
    ci = _ci_lookup(s)
    if ci is not None:
        return ci
    r = _rules(s)
    if r is not None:
        return r
    r = _compose(s)
    if r is not None:
        return r
    if PASSTHRU.match(s):
        return s
    return None


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, 'strings_zh.json')
    if not os.path.exists(src):
        src = os.path.join(here, 'missing_zh.json')
    miss = json.load(io.open(src, encoding='utf-8'))
    out, still = {}, []
    for s, c in miss:
        t = tr(s)
        if t is not None:
            out[s] = t
        else:
            still.append((s, c))
    json.dump(out, io.open(os.path.join(here, 'glossary_zh.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0, sort_keys=True)
    json.dump(still, io.open(os.path.join(here, 'todo_zh.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0)
    total = sum(c for s, c in miss)
    covered = sum(c for s, c in miss if s in out)
    print('glossary entries : %d of %d distinct strings' % (len(out), len(miss)))
    print('occurrence cover : %.1f%%' % (100.0 * covered / total))
    print('still to do      : %d distinct (%d occurrences)'
          % (len(still), sum(c for s, c in still)))
    for s, c in still[:20]:
        print('   %4d  %s' % (c, s[:86]))
