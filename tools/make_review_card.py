# -*- coding: utf-8 -*-
"""Printable Google-review request card with a QR code (A6 at 300 dpi, 1240x1748).

Run:  python tools/make_review_card.py
Writes marketing/review-kit/review-card.png and review-qr.png.

The link opens the "write a review" box for the Primaxs Google Business Profile.
It is built from the listing's feature ID (FTID), read from the Google Maps URL of
the listing on 9 Oct 2026. Signed-out visitors are asked to sign in first.
"""
import os
import segno
from PIL import Image, ImageDraw, ImageFont

FTID = '0x31cc366fbae78e4b:0xa4d19568ef7d7535'
REVIEW_URL = ('https://www.google.com/search?q=Primaxs+Marketing+(M)+Sdn+Bhd#lrd=%s,3,,,' % FTID)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'marketing', 'review-kit')
FONTS = r'C:\Windows\Fonts'
W, H = 1240, 1748
RED, INK, GREY, PAPER = (200, 30, 45), (24, 28, 36), (95, 102, 112), (255, 255, 255)


def f(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def centre(d, text, font, y, fill):
    d.text(((W - d.textlength(text, font=font)) / 2, y), text, font=font, fill=fill)


def main():
    os.makedirs(OUT, exist_ok=True)
    qr_path = os.path.join(OUT, 'review-qr.png')
    segno.make(REVIEW_URL, error='m').save(qr_path, scale=20, border=2)

    im = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 22], fill=RED)
    logo = os.path.join(ROOT, 'docs', 'assets', 'primaxs-logo-removebg-preview.png')
    if os.path.exists(logo):
        lg = Image.open(logo).convert('RGBA')
        lg.thumbnail((360, 200))
        im.paste(lg, ((W - lg.width) // 2, 70), lg)
    y = 300
    centre(d, 'Happy with your Tanko order?', f('arialbd.ttf', 66), y, INK)
    y += 100
    centre(d, 'A Google review takes one minute', f('arial.ttf', 46), y, GREY)
    y += 62
    centre(d, 'and helps other factories find us.', f('arial.ttf', 46), y, GREY)
    y += 100
    qr = Image.open(qr_path).convert('RGB')
    qr = qr.resize((700, 700), Image.NEAREST)
    im.paste(qr, ((W - 700) // 2, y))
    y += 730
    centre(d, 'Scan with your phone camera', f('arialbd.ttf', 44), y, RED)
    y += 90
    centre(d, 'Puas hati? Imbas untuk ulasan Google.', f('arial.ttf', 40), y, INK)
    y += 62
    centre(d, '满意吗？扫码在 Google 给我们评价。', f('msyh.ttc', 40), y, INK)
    d.rectangle([0, H - 120, W, H], fill=INK)
    centre(d, 'Primaxs Marketing (M) Sdn Bhd  |  storagesystem.com.my', f('arial.ttf', 36), H - 86, (230, 232, 236))
    out = os.path.join(OUT, 'review-card.png')
    im.save(out, dpi=(300, 300))
    print('wrote', out)
    print('link', REVIEW_URL)


if __name__ == '__main__':
    main()
