# -*- coding: utf-8 -*-
"""Build the Act 446 hostel-locker social poster (1080x1350, 4:5 feed format).

Run:  python tools/make_locker_poster.py
Writes marketing/posters/locker-act446-en.jpg and locker-act446-zh.jpg.
Every number on the poster comes from the model pages or the 2020 regulations.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A3 = os.path.join(ROOT, 'docs', 'asset3')
OUT = os.path.join(ROOT, 'marketing', 'posters')
FONTS = r'C:\Windows\Fonts'
W, H = 1080, 1350
RED = (200, 30, 45)
INK = (24, 28, 36)
GREY = (95, 102, 112)
GREEN = (20, 128, 70)
PAPER = (246, 243, 238)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def product(fname, box):
    im = Image.open(os.path.join(A3, fname)).convert('RGB')
    im.thumbnail(box, Image.LANCZOS)
    return im


def centre(d, text, f, y, fill, x0=0, x1=W):
    w = d.textlength(text, font=f)
    d.text((x0 + (x1 - x0 - w) / 2, y), text, font=f, fill=fill)


def build(lang):
    zh = lang == 'zh'
    bold = font('msyhbd.ttc', 1) if zh else None
    F = (lambda s: font('msyhbd.ttc', s)) if zh else (lambda s: font('arialbd.ttf', s))
    R = (lambda s: font('msyh.ttc', s)) if zh else (lambda s: font('arial.ttf', s))
    T = {
        'en': dict(
            kicker='WORKER HOSTEL LOCKERS',
            h1='Does yours pass', h2='the Act 446 size?',
            rule='Each worker needs their own locked cupboard of at least',
            dims='350 x 350 x 900 mm',
            src='Accommodation Regulations 2020, in force since 1 Sep 2020',
            ok='PASSES', a='FBB-202  2-door', a2='inside 415 x 450 x 1653 mm',
            b='FBA-202W  2-door', b2='inside 420 x 388 x 987 mm',
            no='Check the inside size: many multi-tier lockers are too narrow or too short.',
            fine='Fine: up to RM50,000 per offence',
            o1='FREE delivery + installation, Selangor & KL',
            o2='1-year warranty, handled locally',
            url='storagesystem.com.my/locker'),
        'zh': dict(
            kicker='员工宿舍储物柜',
            h1='你的储物柜', h2='符合 Act 446 尺寸吗？',
            rule='每位员工须有独立上锁柜，内部至少',
            dims='350 x 350 x 900 mm',
            src='2020 年员工住宿条例，2020 年 9 月 1 日起生效',
            ok='符合', a='FBB-202  双门', a2='内部 415 x 450 x 1653 mm',
            b='FBA-202W  双门', b2='内部 420 x 388 x 987 mm',
            no='请量内部尺寸：很多多层储物柜太窄或太矮。',
            fine='罚款：每项违规最高 RM50,000',
            o1='雪兰莪及吉隆坡免费送货 + 安装',
            o2='一年保修，本地处理',
            url='storagesystem.com.my/locker'),
    }[lang]

    im = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=RED)
    y = 58
    centre(d, T['kicker'], F(34), y, RED)
    y += 62
    centre(d, T['h1'], F(78 if not zh else 72), y, INK)
    y += 92
    centre(d, T['h2'], F(78 if not zh else 72), y, INK)
    y += 118
    centre(d, T['rule'], R(32), y, GREY)
    y += 50
    centre(d, T['dims'], F(70), y, RED)
    y += 92
    centre(d, T['src'], R(26), y, GREY)
    y += 56

    # two product cards
    cw, ch = 470, 500
    for i, (img, name, inside) in enumerate([('FBB-202.webp', T['a'], T['a2']),
                                            ('FBA-202W.webp', T['b'], T['b2'])]):
        x = 50 + i * (cw + 40)
        d.rounded_rectangle([x, y, x + cw, y + ch], 18, fill=(255, 255, 255), outline=(222, 218, 210), width=2)
        p = product(img, (cw - 60, 330))
        im.paste(p, (int(x + (cw - p.width) / 2), y + 30))
        d.rounded_rectangle([x + cw - 170, y + 18, x + cw - 18, y + 70], 26, fill=GREEN)
        centre(d, T['ok'], F(28), y + 27, (255, 255, 255), x + cw - 170, x + cw - 18)
        centre(d, name, F(34), y + ch - 118, INK, x, x + cw)
        centre(d, inside, R(26), y + ch - 78, GREY, x, x + cw)
    y += ch + 30
    centre(d, T['no'], R(29), y, INK)
    y += 54
    centre(d, T['fine'], F(30), y, RED)

    # offer band
    d.rectangle([0, H - 150, W, H], fill=INK)
    centre(d, T['o1'], F(32), H - 132, (255, 255, 255))
    centre(d, T['o2'] + '   |   ' + T['url'], R(28), H - 82, (210, 214, 220))
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, 'locker-act446-%s.jpg' % lang)
    im.save(out, quality=90, optimize=True)
    print('wrote', out)


if __name__ == '__main__':
    build('en')
    build('zh')
