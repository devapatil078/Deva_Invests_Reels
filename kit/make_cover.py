"""Reel cover (1080x1920 JPG): a clean frame from the reel (no captions) + the series/part badge + the main hook.

  python3 make_cover.py <frame.jpg> <out.jpg> "<SERIES>" <part> "<line 1>" "<line 2>" ["<line 3>"] [--shift 300] [--sub "THE 70% RULE"]

Wrap the word(s) to highlight in [brackets]: "SOLD FOR [21% MORE]". Text sits in the top band so it also survives the
Instagram grid crop (3:4, centre). Get a clean frame with:  QS='&nocap=1&res=1' node tools/capture.mjs frames <dir> "<t>"
(the project's main.js skips captions when the URL has nocap).
"""
import argparse, glob, os, re
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument('frame'); ap.add_argument('out'); ap.add_argument('series'); ap.add_argument('part')
ap.add_argument('lines', nargs='+'); ap.add_argument('--shift', type=int, default=300); ap.add_argument('--sub', default='')
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
# background: the same frame, blurred and darkened, then the sharp frame pushed down to free the top band
bg = fr.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.45))
im = bg.copy(); im.paste(fr, (0, a.shift))
# soft dark band behind the text
band = Image.new('L', (W, H), 0); bd = ImageDraw.Draw(band)
top = 1080 + a.shift * 0.3
for y in range(int(top)):
    bd.line([(0, y), (W, y)], fill=int(215 * max(0.0, min(1.0, (top - y) / (top * 0.55)))))
im = Image.composite(Image.new('RGB', (W, H), (8, 10, 16)), im, band)
d = ImageDraw.Draw(im)

# badge: PART n · SERIES
f1, f2 = BLACK(40), BLACK(34)
p1 = f'PART {a.part}'; w1 = d.textlength(p1, font=f1); w2 = d.textlength(a.series, font=f2)
x0, y0 = (W - (w1 + w2 + 96)) / 2, 250
d.rounded_rectangle([x0, y0, x0 + w1 + 40, y0 + 64], 32, fill=YEL); d.text((x0 + 20, y0 + 32), p1, font=f1, fill=INK, anchor='lm')
d.rounded_rectangle([x0 + w1 + 56, y0, x0 + w1 + w2 + 96, y0 + 64], 32, fill=(40, 42, 48)); d.text((x0 + w1 + 76, y0 + 33), a.series, font=f2, fill=(255, 255, 255), anchor='lm')


# hook: up to 3 lines, auto-sized to fit, [highlight] in yellow, thick dark stroke
def runs(s): return [(t, i % 2 == 1) for i, t in enumerate(re.split(r'[\[\]]', s)) if t]
size = 132
while size > 70 and max(d.textlength(re.sub(r'[\[\]]', '', l), font=BLACK(size)) for l in a.lines) > W - 110: size -= 4
fh = BLACK(size); y = y0 + 110
for l in a.lines:
    rs = runs(l); tw = sum(d.textlength(t, font=fh) for t, _ in rs); x = (W - tw) / 2
    for t, hi in rs:
        d.text((x, y), t, font=fh, fill=YEL if hi else (255, 255, 255), stroke_width=max(6, size // 14), stroke_fill=(0, 0, 0)); x += d.textlength(t, font=fh)
    y += int(size * 1.08)
if a.sub:
    fs = BLACK(46); tw = d.textlength(a.sub, font=fs); y += 14
    d.rounded_rectangle([(W - tw) / 2 - 26, y, (W + tw) / 2 + 26, y + 74], 37, fill=(207, 81, 64)); d.text((W / 2, y + 38), a.sub, font=fs, fill=(255, 255, 255), anchor='mm')

# handle, inside the grid-safe area
fb = BLACK(34); d.text((W / 2, 1625), '@deva_invests', font=fb, fill=(255, 255, 255), anchor='mm', stroke_width=5, stroke_fill=(0, 0, 0))
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
im.save(a.out, quality=92)
print(a.out)
