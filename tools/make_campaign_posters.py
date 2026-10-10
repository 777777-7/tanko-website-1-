# -*- coding: utf-8 -*-
"""Social posters for the week of 12 Oct 2026 (1080x1350, 4:5 feed format).

Run:  python tools/make_campaign_posters.py
Writes marketing/posters/pegboard-steel-vs-hardboard-en.jpg and fit-out-checklist-en.jpg.
Every price and rule comes from the model pages, the metal pegboard guide or the
fit-out checklist guide.
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
WHITE = (255, 255, 255)


def F(s):
    return ImageFont.truetype(os.path.join(FONTS, 'arialbd.ttf'), s)


def R(s):
    return ImageFont.truetype(os.path.join(FONTS, 'arial.ttf'), s)


def product(fname, box):
    im = Image.open(os.path.join(A3, fname)).convert('RGB')
    im.thumbnail(box, Image.LANCZOS)
    return im


def centre(d, text, f, y, fill, x0=0, x1=W):
    w = d.textlength(text, font=f)
    d.text((x0 + (x1 - x0 - w) / 2, y), text, font=f, fill=fill)


def offer_band(d, url):
    d.rectangle([0, H - 150, W, H], fill=INK)
    centre(d, 'FREE delivery + installation, Selangor & KL', F(32), H - 132, WHITE)
    centre(d, '1-year warranty, handled locally   |   ' + url, R(28), H - 82, (210, 214, 220))


def card(im, d, x, y, cw, ch, img, name, sub, badge=None, badge_fill=GREEN):
    d.rounded_rectangle([x, y, x + cw, y + ch], 18, fill=WHITE, outline=(222, 218, 210), width=2)
    p = product(img, (cw - 60, ch - 170))
    im.paste(p, (int(x + (cw - p.width) / 2), y + 30))
    if badge:
        bw = d.textlength(badge, font=F(26)) + 44
        d.rounded_rectangle([x + cw - bw - 18, y + 18, x + cw - 18, y + 68], 25, fill=badge_fill)
        centre(d, badge, F(26), y + 28, WHITE, x + cw - bw - 18, x + cw - 18)
    centre(d, name, F(32), y + ch - 112, INK, x, x + cw)
    centre(d, sub, R(25), y + ch - 72, GREY, x, x + cw)


def pegboard():
    im = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=RED)
    y = 58
    centre(d, 'WORKSHOP TOOL BOARDS', F(34), y, RED)
    y += 62
    centre(d, 'Hooks falling out?', F(76), y, INK)
    y += 90
    centre(d, 'Holes worn oval?', F(76), y, INK)
    y += 116
    centre(d, 'Hardboard pegboard swells in humid workshops,', R(31), y, GREY)
    y += 44
    centre(d, 'and its holes wear under daily hook loads.', R(31), y, GREY)
    y += 66
    centre(d, 'Steel boards from RM168.70', F(62), y, RED)
    y += 96
    cw, ch = 470, 470
    card(im, d, 50, y, cw, ch, 'KQ-306A (Gray).webp', 'KQ-3 steel boards',
         '9 sizes, 5 colours, one hole pitch', 'STEEL')
    card(im, d, 50 + cw + 40, y, cw, ch, 'KQ-306AS (Stainless Steel).webp', 'KQ-306AS #304 stainless',
         'wash-down areas, RM397.65', '#304', (60, 90, 140))
    y += ch + 28
    centre(d, 'Hooks move between every board size. Shadow-board them for 5S.', R(28), y, INK)
    offer_band(d, 'storagesystem.com.my')
    out = os.path.join(OUT, 'pegboard-steel-vs-hardboard-en.jpg')
    im.save(out, quality=90, optimize=True)
    print('wrote', out)


def fit_out():
    im = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=RED)
    y = 58
    centre(d, 'NEW FACTORY FIT-OUT', F(34), y, RED)
    y += 62
    centre(d, 'Storage is usually', F(74), y, INK)
    y += 88
    centre(d, 'the last order.', F(74), y, INK)
    y += 110
    centre(d, 'Confirm your counts 6 to 8 weeks before start-up', R(31), y, GREY)
    y += 44
    centre(d, 'so everything is installed before production.', R(31), y, GREY)
    y += 70
    # checklist on the left, bench photo on the right
    box_y = y
    d.rounded_rectangle([50, box_y, W - 50, box_y + 560], 18, fill=WHITE, outline=(222, 218, 210), width=2)
    items = ['Line workbenches and workstations',
             'Maintenance benches, tool cabinets',
             'Shadow boards for tool control',
             'Spares cabinets and bins',
             'Mould racks',
             'Changing-room lockers',
             'Act 446 hostel lockers']
    ty = box_y + 40
    for it in items:
        d.ellipse([86, ty + 4, 122, ty + 40], fill=GREEN)
        d.line([(95, ty + 22), (102, ty + 31), (115, ty + 13)], fill=WHITE, width=5)
        d.text((140, ty + 2), it, font=F(30), fill=INK)
        ty += 66
    d.text((140, ty + 4), '1 per resident, 350 x 350 x 900 mm inside', font=R(25), fill=GREY)
    p = product('WAT-5203N.webp', (330, 330))
    im.paste(p, (W - 50 - 20 - p.width, box_y + 200))
    y = box_y + 590
    centre(d, 'Free area-by-area checklist on our website (Guides)', F(30), y, RED)
    offer_band(d, 'storagesystem.com.my')
    out = os.path.join(OUT, 'fit-out-checklist-en.jpg')
    im.save(out, quality=90, optimize=True)
    print('wrote', out)


if __name__ == '__main__':
    pegboard()
    fit_out()
