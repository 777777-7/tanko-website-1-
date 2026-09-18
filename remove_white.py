import os
from PIL import Image

src_dir = r"C:\Users\User\Documents\GitHub\tanko-website-1-\docs\asset3"
files = [
    "SAN-368K.webp",
    "KPQ-4306.webp",
    "KPQ-4301 (Blue).webp",
    "RY-04SA.webp",
    "WB-67W7A.webp",
    "EGL-187M(EGL-187M (black)).webp",
    "MB-206.webp",
    "KM-2240(Blue).webp",
    "RFA-091.webp",
    "A4L-104.webp",
    "EKB-3M(Gray).webp",
]

def white_to_transparent(img):
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            # near-white -> transparent; soft edge by luminance
            if r > 235 and g > 235 and b > 235:
                px[x, y] = (r, g, b, 0)
            elif r > 215 and g > 215 and b > 215:
                # partial fade
                alpha = int(255 * (255 - max(r, g, b)) / 40.0)
                alpha = max(0, min(255, alpha))
                px[x, y] = (r, g, b, alpha)
    return img

for f in files:
    p = os.path.join(src_dir, f)
    if not os.path.exists(p):
        print("MISS", f); continue
    out_name = os.path.splitext(f)[0] + "-cut.png"
    out_p = os.path.join(src_dir, out_name)
    im = Image.open(p)
    im = white_to_transparent(im)
    im.save(out_p, "PNG")
    print("OK", out_name)
