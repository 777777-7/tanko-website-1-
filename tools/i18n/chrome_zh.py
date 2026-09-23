# -*- coding: utf-8 -*-
"""Translate the shared chrome (nav, footer, basket UI) on the Chinese pages.

build_lang.py only translates text inside <main>, so the header, footer and
basket widget stayed English on /zh/ pages. This applies a fixed map to the
markup outside <main>.

Links whose destination is an English-only page keep their English title on
purpose - the label should describe what you actually land on.

Run:  python tools/i18n/chrome_zh.py [--dry]
"""
import re, io, os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ZH = os.path.join(ROOT, 'docs', 'zh')

CHROME = {
    # --- primary nav
    "Skip to main content": "跳至主要内容",
    "Home": "首页",
    "Products": "产品",
    "Download": "下载",
    "Guides": "指南",
    "About Us": "关于我们",
    "Contact Us": "联系我们",
    "Basket &amp; Send List": "询价单",
    "View all product categories &rarr;": "查看所有产品类别 &rarr;",
    "View all &rarr;": "查看全部 &rarr;",
    "All Guides &amp; Resources": "所有指南与资源",
    "Guides &amp; Resources": "指南与资源",
    "By Location": "按地区",
    "By Industry": "按行业",
    "By Location &rarr;": "按地区 &rarr;",
    "By Industry &rarr;": "按行业 &rarr;",

    # --- calls to action
    "Request a Quote": "索取报价",
    "Request a Quote&nbsp;&rarr;": "索取报价&nbsp;&rarr;",
    "Need a custom quote for your workshop or factory?":
        "需要为你的工作坊或工厂定制报价？",
    "Tell us the models and quantities — we'll come back with pricing, lead time and delivery options.":
        "告诉我们型号与数量——我们会附上价格、交期与配送方式回复。",

    # --- basket / enquiry widget
    "Your basket": "你的询价单",
    "Your basket is empty.": "询价单是空的。",
    "Your basket is empty": "询价单是空的",
    "Items in basket": "询价单内品项",
    "Browse products": "浏览产品",
    "Clear basket": "清空询价单",
    "WhatsApp us": "WhatsApp 联系我们",
    "Send your list via WhatsApp": "通过 WhatsApp 发送清单",
    "Contact Us on WhatsApp": "通过 WhatsApp 联系我们",
    "Add products to your basket and we'll include the model codes in your WhatsApp message.":
        "把产品加入询价单，我们会在 WhatsApp 讯息中附上型号。",

    # --- search
    "Search products": "搜索产品",
    "Search in product catalogue →": "在产品目录中搜索 →",
    "to open ·": "开启 ·",
    "to navigate ·": "切换 ·",
    "to close": "关闭",

    # --- footer
    "Company": "公司",
    "About Primaxs": "关于 Primaxs",
    "Contact": "联系方式",
    "Get in Touch": "联系我们",
    "Follow us on Facebook": "在 Facebook 关注我们",
    "Privacy Policy": "隐私政策",
    "Terms of Service": "服务条款",
    "Returns &amp; Warranty": "退换货与保固",
    "Returns &amp; Refund": "退货与退款",
    "Editorial Policy": "编辑政策",
    "Exclusive Malaysia retail distributor for Tanko industrial storage — tool cabinets, workbenches, lockers and racking.":
        "Tanko 工业储存在马来西亚的独家零售总代理 — 工具柜、工作桌、置物柜与货架。",

    # --- footer product links (these already point at the /zh/ twins)
    "Workbenches": "工作桌",
    "Tool Cabinets": "工具柜",
    "CNC Tool Storage": "CNC 刀具存放",
    "Modular Workstations": "模组式工作站",
    "Hanger Racks": "挂架",
    "Lockers": "置物柜",
}


def process(path, write=True):
    with io.open(path, encoding='utf-8') as fh:
        html = fh.read()

    m = re.search(r'<main\b', html)
    if not m:
        return 'no-main'
    end = html.rindex('</main>') + len('</main>')
    head, body, tail = html[:m.start()], html[m.start():end], html[end:]

    n = 0
    for src, dst in CHROME.items():
        pat = '>' + src + '<'
        rep = '>' + dst + '<'
        for seg_name in ('head', 'tail'):
            pass
        if pat in head:
            n += head.count(pat); head = head.replace(pat, rep)
        if pat in tail:
            n += tail.count(pat); tail = tail.replace(pat, rep)

    if not n:
        return 'nothing'
    if write:
        with io.open(path, 'w', encoding='utf-8', newline='') as fh:
            fh.write(head + body + tail)
    return 'translated %d' % n


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    tot = 0
    files = sorted(glob.glob(os.path.join(ZH, '**', '*.html'), recursive=True))
    for f in files:
        r = process(f, write=not dry)
        if r.startswith('translated'):
            tot += int(r.split()[1])
    print('%s%d Chinese pages, %d chrome strings replaced'
          % ('[dry] ' if dry else '', len(files), tot))
