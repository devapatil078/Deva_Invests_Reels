"""Reel cover (1080x1920 JPG): a clean frame from the reel (no captions) + the series/part badge + the main hook.

  python3 make_cover.py <frame.jpg> <out.jpg> "<SERIES>" <part> "<line 1>" "<line 2>" ["<line 3>"] [--shift 0] [--ypos 0] [--sub "THE 70% RULE"]

Wrap the word(s) to highlight in [brackets]: "SOLD FOR [21% MORE]". The text block sits in the vertical middle (move it with --ypos),
inside the Instagram grid crop (3:4, centre). Get a clean frame with:  QS='&nocap=1&res=1' node tools/capture.mjs frames <dir> "<t>"
(the project's main.js skips captions when the URL has nocap).
"""
import argparse, glob, os, re
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument('frame'); ap.add_argument('out'); ap.add_argument('series'); ap.add_argument('part')
ap.add_argument('lines', nargs='+'); ap.add_argument('--shift', type=int, default=0); ap.add_argument('--ypos', type=int, default=0, help='move the text block up (-) or down (+) from the centre'); ap.add_argument('--sub', default='')
a = ap.parse_args()
W, H = 1080, 1920


def font(name, size):
    for pat in [f'/root/faceless-shorts/*/fonts/{name}', f'/usr/share/fonts/**/{name}']:
        fs = glob.glob(pat, recursive=True)
        if fs: return ImageFont.truetype(fs[0], size)
    raise SystemExit(f'font {name} not found')


BLACK = lambda s: font('Inter-Black.otf', s)
YEL, INK = (255, 212, 59), (17, 17, 17)

fr = Image.open(a.frame).convert('RGB').resize((W, H))
# the frame, nudged by --shift (default 0), over a blurred copy so nothing is left empty
bg = fr.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.45))
im = bg.copy(); im.paste(fr, (0, a.shift))
probe = ImageDraw.Draw(Image.new('RGB', (W, H)))


# measure the text block: badge + hook lines (+ sub), then centre it vertically
def runs(s): return [(t, i % 2 == 1) for i, t in enumerate(re.split(r'[\[\]]', s)) if t]
size = 132
while size > 70 and max(probe.textlength(re.sub(r'[\[\]]', '', l), font=BLACK(size)) for l in a.lines) > W - 110: size -= 4
fh = BLACK(size); lh = int(size * 1.08)
block = 64 + 46 + lh * len(a.lines) + (88 if a.sub else 0)
y0 = int(H / 2 - block / 2) + a.ypos

# soft dark band behind the text, fading out above and below
band = Image.new('L', (W, H), 0); bd = ImageDraw.Draw(band)
c0, c1, fade = y0 - 40, y0 + block + 40, 260
for y in range(H):
    k = 1.0 if c0 <= y <= c1 else max(0.0, 1 - (c0 - y) / fade) if y < c0 else max(0.0, 1 - (y - c1) / fade)
    if k > 0: bd.line([(0, y), (W, y)], fill=int(200 * k ** 1.5))
im = Image.composite(Image.new('RGB', (W, H), (8, 10, 16)), im, band)
d = ImageDraw.Draw(im)

# badge: PART n · SERIES
f1, f2 = BLACK(40), BLACK(34)
p1 = f'PART {a.part}'; w1 = d.textlength(p1, font=f1); w2 = d.textlength(a.series, font=f2)
x0 = (W - (w1 + w2 + 96)) / 2
d.rounded_rectangle([x0, y0, x0 + w1 + 40, y0 + 64], 32, fill=YEL); d.text((x0 + 20, y0 + 32), p1, font=f1, fill=INK, anchor='lm')
d.rounded_rectangle([x0 + w1 + 56, y0, x0 + w1 + w2 + 96, y0 + 64], 32, fill=(40, 42, 48)); d.text((x0 + w1 + 76, y0 + 33), a.series, font=f2, fill=(255, 255, 255), anchor='lm')

# hook: [highlight] in yellow, thick dark stroke
y = y0 + 64 + 34
for l in a.lines:
    rs = runs(l); tw = sum(d.textlength(t, font=fh) for t, _ in rs); x = (W - tw) / 2
    for t, hi in rs:
        d.text((x, y), t, font=fh, fill=YEL if hi else (255, 255, 255), stroke_width=max(6, size // 14), stroke_fill=(0, 0, 0)); x += d.textlength(t, font=fh)
    y += lh
if a.sub:
    fs = BLACK(46); tw = d.textlength(a.sub, font=fs); y += 14
    d.rounded_rectangle([(W - tw) / 2 - 26, y, (W + tw) / 2 + 26, y + 74], 37, fill=(207, 81, 64)); d.text((W / 2, y + 38), a.sub, font=fs, fill=(255, 255, 255), anchor='mm')

# handle, inside the grid-safe area
fb = BLACK(34); d.text((W / 2, 1625), '@deva_invests', font=fb, fill=(255, 255, 255), anchor='mm', stroke_width=5, stroke_fill=(0, 0, 0))
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
im.save(a.out, quality=92)
print(a.out)
