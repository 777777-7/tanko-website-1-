# -*- coding: utf-8 -*-
"""Web images and a social poster from the October 2026 showroom installation.

Run:  python tools/make_showroom_assets.py
Source: marketing/customer-projects/showroom-2026-10/*.jpg (crops of the customer's
photos with the customer's logos cut out; the customer is not named until they agree).
Writes:
  docs/asset_content/projects/showroom-pegboard-*.webp (+ -w800) for the site,
  docs/feed-img/projects__showroom-pegboard.jpg (1200x1200 Open Graph / hero),
  marketing/posters/showroom-pegboard-en.jpg (1080x1350 feed poster).
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'marketing', 'customer-projects', 'showroom-2026-10')
WEB = os.path.join(ROOT, 'docs', 'asset_content', 'projects')
FEED = os.path.join(ROOT, 'docs', 'feed-img')
POST = os.path.join(ROOT, 'marketing', 'posters')
FONTS = r'C:\Windows\Fonts'
RED, INK, GREY, PAPER, WHITE = (200, 30, 45), (24, 28, 36), (95, 102, 112), (246, 243, 238), (255, 255, 255)


def F(s):
    return ImageFont.truetype(os.path.join(FONTS, 'arialbd.ttf'), s)


def R(s):
    return ImageFont.truetype(os.path.join(FONTS, 'arial.ttf'), s)


def centre(d, text, f, y, fill, x0=0, x1=1080):
    w = d.textlength(text, font=f)
    d.text((x0 + (x1 - x0 - w) / 2, y), text, font=f, fill=fill)


def cover(im, w, h):
    """Scale and centre-crop to exactly w x h."""
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def load(name):
    return Image.open(os.path.join(SRC, name)).convert('RGB')


def web_images():
    os.makedirs(WEB, exist_ok=True)
    for src, out in [('partition-front.jpg', 'showroom-pegboard-partition'),
                     ('counter-backboard.jpg', 'showroom-pegboard-counter'),
                     ('partition-side.jpg', 'showroom-pegboard-side')]:
        im = load(src)
        im.save(os.path.join(WEB, out + '.webp'), quality=82)
        small = im.copy()
        small.thumbnail((800, 800), Image.LANCZOS)
        small.save(os.path.join(WEB, out + '-w800.webp'), quality=80)
        print('wrote', out, im.size)
    # 1200x1200 hero / Open Graph collage
    hero = Image.new('RGB', (1200, 1200), PAPER)
    hero.paste(cover(load('partition-front.jpg'), 790, 1200), (0, 0))
    hero.paste(cover(load('counter-backboard.jpg'), 400, 400), (800, 0))
    hero.paste(cover(load('partition-side.jpg'), 400, 790), (800, 410))
    hero.save(os.path.join(WEB, 'showroom-pegboard-hero.webp'), quality=82)
    small = hero.copy()
    small.thumbnail((800, 800), Image.LANCZOS)
    small.save(os.path.join(WEB, 'showroom-pegboard-hero-w800.webp'), quality=80)
    hero.save(os.path.join(FEED, 'projects__showroom-pegboard.jpg'), quality=86)
    print('wrote hero')


def poster():
    W, H = 1080, 1350
    im = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=RED)
    centre(d, 'REAL INSTALLATION  |  SHOWROOM', F(32), 46, RED)
    centre(d, 'A pegboard wall that', F(66), 96, INK)
    centre(d, 'stands on its own', F(66), 174, INK)
    centre(d, 'Steel pegboard on support poles: a partition and a counter backboard', R(28), 262, GREY)
    y = 318
    im.paste(cover(load('partition-front.jpg'), 600, 820), (40, y))
    im.paste(cover(load('counter-backboard.jpg'), 400, 400), (650, y))
    im.paste(cover(load('partition-side.jpg'), 400, 410), (650, y + 410))
    y += 840
    centre(d, 'Custom sizes up to 8 x 4 ft  |  5 colours  |  hooks, shelves, screen arms', F(28), y, INK)
    d.rectangle([0, H - 150, W, H], fill=INK)
    centre(d, 'FREE delivery + installation, Selangor & KL', F(32), H - 132, WHITE)
    centre(d, '1-year warranty, handled locally   |   storagesystem.com.my', R(28), H - 82, (210, 214, 220))
    os.makedirs(POST, exist_ok=True)
    out = os.path.join(POST, 'showroom-pegboard-en.jpg')
    im.save(out, quality=90, optimize=True)
    print('wrote', out)


if __name__ == '__main__':
    web_images()
    poster()
