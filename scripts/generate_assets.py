#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / 'icons'
BRAND = ROOT / 'assets' / 'brand'
STORE = ROOT / 'store-assets'

ICONS.mkdir(parents=True, exist_ok=True)
BRAND.mkdir(parents=True, exist_ok=True)
STORE.mkdir(parents=True, exist_ok=True)


def lerp(a, b, t):
    return int(a + (b - a) * t)


def gradient(size, top=(10, 18, 42, 255), bottom=(34, 14, 68, 255)):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    px = img.load()
    for y in range(size):
        t = y / max(1, size - 1)
        c = tuple(lerp(top[i], bottom[i], t) for i in range(4))
        for x in range(size):
            px[x, y] = c
    return img


def make_icon(size=1024):
    # Chrome recommends transparent padding around the 128x128 store icon.
    pad = int(size * 0.125)
    inner = size - 2 * pad

    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    base = gradient(inner)
    mask = Image.new('L', (inner, inner), 0)
    md = ImageDraw.Draw(mask)
    radius = int(inner * 0.23)
    md.rounded_rectangle((0, 0, inner - 1, inner - 1), radius=radius, fill=255)
    canvas.alpha_composite(Image.composite(base, Image.new('RGBA', base.size), mask), (pad, pad))

    # Soft cyan/violet glow, intentionally not YouTube-red branding.
    glow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.arc((pad + inner*.08, pad + inner*.06, pad + inner*.92, pad + inner*.92),
           start=205, end=350, width=max(4, int(size*.028)), fill=(74, 222, 255, 230))
    gd.arc((pad + inner*.07, pad + inner*.05, pad + inner*.93, pad + inner*.93),
           start=20, end=185, width=max(4, int(size*.028)), fill=(156, 92, 255, 220))
    blur = glow.filter(ImageFilter.GaussianBlur(max(2, int(size*.018))))
    canvas.alpha_composite(blur)
    canvas.alpha_composite(glow)

    d = ImageDraw.Draw(canvas)
    # Rear card / new-tab layer.
    card_w = inner * 0.60
    card_h = inner * 0.38
    x1 = pad + inner * 0.22
    y1 = pad + inner * 0.25
    x2 = x1 + card_w
    y2 = y1 + card_h
    stroke = max(3, int(size * 0.032))
    d.rounded_rectangle((x1, y1, x2, y2), radius=int(inner*.07), outline=(170, 117, 255, 230), width=stroke)

    # Foreground card slightly offset down-left.
    fx1 = pad + inner * 0.14
    fy1 = pad + inner * 0.40
    fx2 = pad + inner * 0.73
    fy2 = pad + inner * 0.72
    d.rounded_rectangle((fx1, fy1, fx2, fy2), radius=int(inner*.07), outline=(226, 240, 255, 255), width=stroke)

    # Generic play triangle, small enough not to resemble YouTube branding.
    cx = (fx1 + fx2) / 2
    cy = (fy1 + fy2) / 2
    tri = [
        (cx - inner*.045, cy - inner*.065),
        (cx - inner*.045, cy + inner*.065),
        (cx + inner*.075, cy),
    ]
    d.polygon(tri, fill=(226, 240, 255, 250))

    # Detached tab marker in upper-right + small slash to suggest state release.
    tx1 = pad + inner*.69
    ty1 = pad + inner*.15
    tx2 = pad + inner*.84
    ty2 = pad + inner*.30
    d.rounded_rectangle((tx1, ty1, tx2, ty2), radius=int(inner*.035), fill=(73, 219, 255, 245))
    d.line((pad+inner*.63, pad+inner*.69, pad+inner*.82, pad+inner*.50), fill=(98, 225, 255, 255), width=stroke)

    return canvas


def font(size, bold=False):
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf',
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


def rounded_bg(w, h):
    img = Image.new('RGBA', (w, h), (9, 15, 31, 255))
    # subtle vertical gradient
    px = img.load()
    for y in range(h):
        t = y / max(1, h-1)
        c = (lerp(9, 28, t), lerp(15, 18, t), lerp(31, 56, t), 255)
        for x in range(w):
            px[x, y] = c
    return img


def draw_card(draw, box, active=True):
    x1, y1, x2, y2 = box
    outline = (103, 226, 255, 255) if active else (151, 108, 255, 255)
    draw.rounded_rectangle(box, radius=20, outline=outline, width=5, fill=(18, 25, 46, 255))
    cx, cy = (x1+x2)//2, (y1+y2)//2
    draw.polygon([(cx-10,cy-15),(cx-10,cy+15),(cx+17,cy)], fill=(235,243,255,245))
    # preview bar
    draw.rounded_rectangle((x1+16,y2-30,x2-16,y2-17), radius=6, fill=(53,64,91,255))


def make_promo(w, h, large=False):
    img = rounded_bg(w, h)
    d = ImageDraw.Draw(img)

    if not large:
        icon_size = 150
        icon = make_icon(512).resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        img.alpha_composite(icon, (18, (h-icon_size)//2))

        x = 150
        d.text((x, 56), 'Stuck Preview Fix', font=font(24, True), fill=(244,248,255,255))
        d.text((x, 112), 'Stops stuck previews after', font=font(15), fill=(196,210,235,255))
        d.text((x, 137), 'opening a YouTube video', font=font(15), fill=(196,210,235,255))
        d.text((x, 162), 'in a new tab.', font=font(15), fill=(196,210,235,255))
        d.rounded_rectangle((x, 205, x+185, 238), radius=16, fill=(27,42,73,255))
        d.text((x+14, 212), 'Chrome • Edge • Chromium', font=font(11, True), fill=(115,226,255,255))
        return img

    icon_size = 260
    icon = make_icon(512).resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    img.alpha_composite(icon, (70, (h-icon_size)//2))

    x = 305
    d.text((x, 105), 'Stuck Preview Fix', font=font(52, True), fill=(244,248,255,255))
    d.text((x, 238), 'Stops video-card previews that keep playing', font=font(25), fill=(196,210,235,255))
    d.text((x, 305), 'after opening a YouTube video in a new tab.', font=font(25), fill=(196,210,235,255))

    # simple before -> after diagram on right
    bx = 980; by = 135; bw = 130; bh = 245
    draw_card(d, (bx,by,bx+bw,by+bh), active=False)
    d.text((bx+24, by+bh+18), 'stuck', font=font(20, True), fill=(191,163,255,255))
    ax = 1135
    d.text((ax, by+88), '→', font=font(48, True), fill=(225,235,255,255))
    cx = 1218
    draw_card(d, (cx,by,cx+bw,by+bh), active=True)
    d.text((cx+15, by+bh+18), 'stopped', font=font(20, True), fill=(103,226,255,255))
    return img


source = make_icon(1024)
source.save(BRAND / 'icon-master-1024.png')
for s in (16, 32, 48, 128, 512):
    source.resize((s, s), Image.Resampling.LANCZOS).save(ICONS / f'icon{s}.png')
source.resize((300, 300), Image.Resampling.LANCZOS).save(STORE / 'logo-300.png')
make_promo(440, 280, large=False).save(STORE / 'small-promo-440x280.png')
make_promo(1400, 560, large=True).save(STORE / 'large-promo-1400x560.png')
print('Assets generated.')
