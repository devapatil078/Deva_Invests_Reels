import sys, math, random
from PIL import Image, ImageDraw, ImageFilter
import engine as E
from engine import *
from thumbs import base, glow_text, save
img, d = base()
W_, H_ = img.size
# server-hall corridor in perspective (vanishing point right of centre)
vx, vy = 1180, 470
lay = Image.new("RGB", img.size, (0, 0, 0)); ld = ImageDraw.Draw(lay)
rng = random.Random(4)
for side in (-1, 1):
    for k in range(14):
        z0 = 1.0 / (1 + k * 0.32); z1 = 1.0 / (1 + (k + 1) * 0.32)
        def P(z, yy, s=side):
            x = vx + s * 1300 * z; y = vy + (yy - vy) * z
            return x, y
        top0 = P(z0, -900); bot0 = P(z0, 1700); top1 = P(z1, -900); bot1 = P(z1, 1700)
        poly = [(top0[0], vy + (-500) * z0), (top1[0], vy + (-500) * z1), (bot1[0], vy + 1100 * z1), (bot0[0], vy + 1100 * z0)]
        shade = int(44 + 14 * (k % 2))
        ld.polygon(poly, fill=(shade - 8, shade, shade + 18))
        # rack lights
        for j in range(22):
            fy = -480 + j * 72
            x = (top0[0] + top1[0]) / 2; zz = (z0 + z1) / 2
            y = vy + fy * zz
            col = (229, 72, 77) if rng.random() < 0.18 else (60, 160, 255) if rng.random() < 0.5 else (40, 70, 110)
            r = max(1, 5 * zz)
            ld.ellipse([x - r * 3, y - r, x + r * 3, y + r], fill=col)
glow = lay.filter(ImageFilter.GaussianBlur(6))
img = Image.blend(img, Image.composite(glow, lay, Image.new("L", img.size, 120)), 0.85)
# darken left for text
dark = Image.new("RGB", img.size, (5, 7, 12))
mask = Image.linear_gradient("L").rotate(90).resize(img.size)
img = Image.composite(img, dark, mask.point(lambda v: int(min(255, v * 1.25 + 40))))
d = ImageDraw.Draw(img)
# falling price line
pts = [(930, 300), (1050, 210), (1420, 470), (1620, 550), (1850, 660)]
d.line(pts, fill=(229, 72, 77), width=12, joint="curve")
d.ellipse([1850 - 22, 660 - 22, 1850 + 22, 660 + 22], fill=(229, 72, 77))
glow_text(img, "$3B SOLD", 90, 300, 250, RED, align="l")
glow_text(img, "THEN IT FELL", 100, 600, 130, INK, align="l", blur=12)
d = ImageDraw.Draw(img)
d.text((104, 220), "THE AI BOND", font=font("black", 70), fill=GOLD)
save(img, sys.argv[1])
