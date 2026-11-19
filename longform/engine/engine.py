"""Motion-graphics engine: draws documentary beats frame by frame with PIL and pipes to ffmpeg."""
import math, os, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
BG = (11, 15, 23)
INK = (237, 239, 243)
MUTED = (138, 147, 166)
DIM = (70, 78, 96)
RED = (229, 72, 77)
GOLD = (245, 185, 66)
TEAL = (61, 214, 198)
PAPER = (236, 231, 220)
PAPER_INK = (40, 40, 44)

F = "/usr/share/fonts/opentype/inter/"
FONTS = {
    "black": F + "InterDisplay-Black.otf", "xbold": F + "InterDisplay-ExtraBold.otf",
    "bold": F + "InterDisplay-Bold.otf", "semi": F + "Inter-SemiBold.otf",
    "med": F + "Inter-Medium.otf", "reg": F + "Inter-Regular.otf", "light": F + "InterDisplay-Light.otf",
    "serif": "/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf",
    "serifb": "/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf",
    "seriti": "/usr/share/fonts/truetype/crosextra/Caladea-Italic.ttf",
    "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "monob": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
}
_fc = {}
def font(w, s):
    k = (w, int(s))
    if k not in _fc: _fc[k] = ImageFont.truetype(FONTS[w], int(s))
    return _fc[k]

def clamp(x, a=0.0, b=1.0): return a if x < a else b if x > b else x
def ease(x):
    x = clamp(x); return 1 - (1 - x) ** 3
def ease_io(x):
    x = clamp(x); return 3 * x * x - 2 * x * x * x
def mix(c1, c2, a): return tuple(int(c1[i] + (c2[i] - c1[i]) * a) for i in range(3))

# ---------- background ----------
def make_bg():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W * 0.5, H * 0.45
    d = np.sqrt(((x - cx) / W) ** 2 + ((y - cy) / H) ** 2)
    base = np.array(BG, np.float32)
    top = np.array((20, 27, 43), np.float32)
    g = np.clip(1.0 - d * 1.6, 0, 1)[..., None]
    img = base + (top - base) * g
    vig = np.clip(1.0 - (d - 0.35) * 1.2, 0.55, 1.0)[..., None]
    img = img * vig
    # faint grid
    grid = ((x % 120 < 1.2) | (y % 120 < 1.2)).astype(np.float32)[..., None] * 5
    img = np.clip(img + grid * g, 0, 255)
    return img.astype(np.uint8)
BG_ARR = None
GRAIN = None
def init():
    global BG_ARR, GRAIN
    BG_ARR = make_bg()
    rng = np.random.default_rng(7)
    GRAIN = [rng.normal(0, 1.6, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]

def background(frame_idx, dark=False):
    arr = BG_ARR.astype(np.int16)
    if dark: arr = (arr * 0.45).astype(np.int16)
    gr = GRAIN[(frame_idx // 4) % 6]
    gr = np.repeat(np.repeat(gr, 2, 0), 2, 1)[..., None]
    arr = np.clip(arr + gr.astype(np.int16), 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB")

# ---------- primitives (all take a, the appear progress 0..1) ----------
def text(d, s, x, y, size=48, w="semi", color=INK, align="l", a=1.0, rise=18, maxw=None, spacing=1.18, track=0):
    if a <= 0: return
    f = font(w, size)
    col = mix(BG, color, ease(a))
    yy = y + (1 - ease(a)) * rise
    lines = wrap(d, s, f, maxw) if maxw else s.split("\n")
    lh = size * spacing
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        xx = x - tw / 2 if align == "c" else x - tw if align == "r" else x
        d.text((xx, yy + i * lh), ln, font=f, fill=col)
    return len(lines) * lh

def wrap(d, s, f, maxw):
    out = []
    for para in s.split("\n"):
        words, cur = para.split(" "), ""
        for wd in words:
            t = (cur + " " + wd).strip()
            if d.textlength(t, font=f) <= maxw: cur = t
            else: out.append(cur); cur = wd
        out.append(cur)
    return out

def rect(d, x, y, w, h, fill=None, outline=None, width=2, r=0, a=1.0):
    if a <= 0: return
    e = ease(a)
    fc = mix(BG, fill, e) if fill else None
    oc = mix(BG, outline, e) if outline else None
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fc, outline=oc, width=width)

def line(d, x1, y1, x2, y2, color=MUTED, width=3, a=1.0, grow=True):
    if a <= 0: return
    e = ease(a)
    if grow: x2, y2 = x1 + (x2 - x1) * e, y1 + (y2 - y1) * e
    d.line([x1, y1, x2, y2], fill=mix(BG, color, min(1, e * 1.5)), width=width)

def arrow(d, x1, y1, x2, y2, color=MUTED, width=3, a=1.0, head=16):
    if a <= 0: return
    e = ease(a)
    ex, ey = x1 + (x2 - x1) * e, y1 + (y2 - y1) * e
    col = mix(BG, color, min(1, e * 1.5))
    d.line([x1, y1, ex, ey], fill=col, width=width)
    ang = math.atan2(ey - y1, ex - x1)
    p = [(ex, ey), (ex - head * math.cos(ang - 0.45), ey - head * math.sin(ang - 0.45)),
         (ex - head * math.cos(ang + 0.45), ey - head * math.sin(ang + 0.45))]
    d.polygon(p, fill=col)

def dot(d, x, y, r=8, color=RED, a=1.0, ring=True, t=0.0):
    if a <= 0: return
    e = ease(a)
    rr = r * e
    d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=mix(BG, color, e))
    if ring:
        ph = (t * 0.8) % 1.0
        R = r + 30 * ph
        d.ellipse([x - R, y - R, x + R, y + R], outline=mix(BG, color, e * (1 - ph) * 0.8), width=2)

def label_box(d, x, y, s, size=30, color=INK, box=DIM, a=1.0, w="semi", pad=18, align="c"):
    if a <= 0: return
    f = font(w, size)
    tw = d.textlength(s, font=f)
    bw, bh = tw + pad * 2, size * 1.6
    bx = x - bw / 2 if align == "c" else x
    rect(d, bx, y, bw, bh, fill=(22, 29, 45), outline=box, r=10, a=a)
    text(d, s, bx + pad, y + (bh - size * 1.2) / 2, size, w, color, a=a, rise=0)
    return bw, bh

def counter(d, x, y, v0, v1, p, size=150, prefix="", suffix="", color=INK, w="black", align="c", a=1.0, decimals=0):
    v = v0 + (v1 - v0) * ease_io(p)
    s = f"{prefix}{v:,.{decimals}f}{suffix}"
    text(d, s, x, y, size, w, color, align, a=a, rise=0)

def stamp(img, s, x, y, color=RED, rot=-12, size=56, a=1.0):
    if a <= 0: return
    e = ease(a)
    f = font("black", size)
    tmp = Image.new("RGBA", (int(size * len(s) * 0.8 + 60), int(size * 1.9)), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    tw = td.textlength(s, font=f)
    td.rounded_rectangle([6, 6, tw + 40, size * 1.6], radius=8, outline=color + (int(230 * e),), width=6)
    td.text((23, size * 0.22), s, font=f, fill=color + (int(230 * e),))
    sc = 1.0 + (1 - e) * 0.6
    tmp = tmp.resize((int(tmp.width * sc), int(tmp.height * sc)), Image.BILINEAR).rotate(rot, expand=True, resample=Image.BILINEAR)
    img.paste(tmp, (int(x - tmp.width / 2), int(y - tmp.height / 2)), tmp)

def paper(d, x, y, w, h, a=1.0, color=PAPER):
    if a <= 0: return
    e = ease(a)
    yy = y + (1 - e) * 40
    d.rounded_rectangle([x + 10, yy + 14, x + w + 10, yy + h + 14], radius=6, fill=mix(BG, (5, 7, 11), e))
    d.rounded_rectangle([x, yy, x + w, yy + h], radius=6, fill=mix(BG, color, e))
    return yy

def ptext(d, s, x, y, size=30, w="serif", color=PAPER_INK, a=1.0, align="l", maxw=None):
    # text on paper: fade from paper color
    if a <= 0: return
    f = font(w, size)
    col = mix(PAPER, color, ease(a))
    lines = wrap(d, s, f, maxw) if maxw else s.split("\n")
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        xx = x - tw / 2 if align == "c" else x
        d.text((xx, y + i * size * 1.25), ln, font=f, fill=col)
    return len(lines) * size * 1.25

def fake_lines(d, x, y, w, n, gap=26, a=1.0, color=(190, 184, 172), seed=1):
    if a <= 0: return
    rng = random.Random(seed)
    for i in range(n):
        lw = w * rng.uniform(0.55, 1.0)
        d.rounded_rectangle([x, y + i * gap, x + lw, y + i * gap + 9], radius=4, fill=mix(PAPER, color, ease(a)))

def source(d, s, a=1.0):
    text(d, "Source: " + s, 80, H - 70, 22, "reg", MUTED, a=a, rise=0)

def recreation(d, x, y, a=1.0):
    text(d, "RECREATION", x, y, 18, "semi", (150, 140, 120), a=a, rise=0, track=2)

# ---------- composite helpers ----------
def kenburns(img, p, z0=1.0, z1=1.035):
    z = z0 + (z1 - z0) * p
    if z <= 1.001: return img
    nw, nh = int(W * z), int(H * z)
    big = img.resize((nw, nh), Image.BILINEAR)
    ox, oy = (nw - W) // 2, (nh - H) // 2
    return big.crop((ox, oy, ox + W, oy + H))
