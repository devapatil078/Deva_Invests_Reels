"""Scene library BASE (from video 1). Copy to scenes.py and add this video's own scene functions below.
Signature of every scene: fn(img, d, t, dur, c, **kw). t = seconds since the beat started, dur = beat length.
c.at(phrase) -> local seconds when the phrase is spoken (relative to beat start); c.fi = frame index.
render.py needs at least: chapter (chapter cards) and whatever names beats.py uses. Video 1 had ~50 scenes; aim for a NEW visual
every 6-12 seconds. filing(), split_view() and endscreen() below still contain video-1 text: edit them for the new topic."""
import math, random
from PIL import Image, ImageDraw
from engine import *

def A(t, t0, dur=0.6): return clamp((t - t0) / dur)

def _at(c, p, default=0.0):
    if p is None: return default
    if isinstance(p, (int, float)): return float(p)
    v = c.at(p)
    return default if v is None else v

def kinetic(img, d, t, dur, c, lines, y0=None, size=84, gap=1.35, align="c", x=None, kicker=None, src=None):
    """lines: list of (text, phrase_or_time, style dict)"""
    n = len(lines)
    total_h = sum(l[2].get("size", size) * gap for l in lines)
    y = y0 if y0 is not None else H / 2 - total_h / 2
    xx = x if x is not None else (W / 2 if align == "c" else 160)
    if kicker:
        text(d, kicker, xx, y - 80, 28, "semi", GOLD, align, a=A(t, 0.1), track=3)
    for k, (s, when, st) in enumerate(lines):
        sz = st.get("size", size)
        tw_ = _at(c, when)
        if k == 0: tw_ = min(tw_, 0.35)
        text(d, s, xx, y, sz, st.get("w", "bold"), st.get("color", INK), align, a=A(t, tw_), maxw=st.get("maxw"))
        y += sz * gap * st.get("lines", 1)
    if src: source(d, src, A(t, 0.5))

def title_card(img, d, t, dur, c, title, sub=None, kicker=None):
    a = A(t, 0.0, 1.0)
    if kicker: text(d, kicker, W / 2, 360, 30, "semi", GOLD, "c", a=a)
    text(d, title, W / 2, 430, 104, "black", INK, "c", a=a, maxw=1600)
    if sub: text(d, sub, W / 2, 680, 38, "med", MUTED, "c", a=A(t, 0.6, 1.0))
    line(d, W / 2 - 160, 650, W / 2 + 160, 650, RED, 4, a=A(t, 0.4, 0.8))

def chapter(img, d, t, dur, c, num, title):
    a = A(t, 0.0, 0.5) * (1 - A(t, dur - 0.5, 0.5))
    text(d, f"CHAPTER {num}" if isinstance(num, int) else num, W / 2, 440, 34, "semi", RED, "c", a=a, rise=0)
    text(d, title, W / 2, 500, 110, "black", INK, "c", a=a, rise=10)
    line(d, W / 2 - 60, 660, W / 2 + 60, 660, RED, 4, a=a)

def building(d, x, y, w, h, a, closed=False, t=0):
    if a <= 0: return
    rect(d, x, y, w, h, fill=(30, 38, 56), outline=(60, 70, 92), r=4, a=a)
    rect(d, x - 20, y - 24, w + 40, 26, fill=(40, 49, 70), a=a)
    cols, rows = 6, 5
    for r_ in range(rows):
        for c_ in range(cols):
            lit = (r_ * 7 + c_ * 3) % 5 == 0 and not closed
            wx = x + 30 + c_ * (w - 60) / cols; wy = y + 30 + r_ * (h - 140) / rows
            rect(d, wx, wy, (w - 60) / cols - 22, (h - 140) / rows - 26, fill=(245, 205, 120) if lit else (22, 28, 42), a=a)
    rect(d, x + w / 2 - 50, y + h - 100, 100, 100, fill=(16, 20, 30), outline=(70, 80, 100), a=a)
    if closed:
        rect(d, x + w / 2 - 150, y + h - 190, 300, 70, fill=RED, r=6, a=A(t, 1.0, 0.4))
        text(d, "CLOSED", x + w / 2, y + h - 182, 44, "black", INK, "c", a=A(t, 1.0, 0.4), rise=0)

def globe(d, cx, cy, r, a, t):
    if a <= 0: return
    col = mix(BG, (60, 80, 110), ease(a))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=3)
    rot = (t * 0.15) % 1.0
    for k in range(6):
        ph = (k / 6 + rot) % 1.0
        ew = abs(math.cos(ph * math.pi)) * r
        d.ellipse([cx - ew, cy - r, cx + ew, cy + r], outline=col, width=2)
    for k in range(1, 5):
        yy = cy - r + k * 2 * r / 5; hw = math.sqrt(max(0, r * r - (yy - cy) ** 2))
        d.line([cx - hw, yy, cx + hw, yy], fill=col, width=2)

# Map: equirectangular box. Video 1 used Europe (lon -8..48, lat 44..64). Change the box for the new region and
# define CITY = {"Name": (lon, lat), ...} in scenes.py before using city().
def proj(lon, lat):
    x = 160 + (lon + 8) / (48 + 8) * 1600
    y = 980 - (lat - 44) / (64 - 44) * 860
    return x, y

def map_base(d, a, t):
    if a <= 0: return
    col = mix(BG, (34, 42, 60), ease(a))
    for lon in range(-5, 50, 5):
        x, _ = proj(lon, 50); d.line([x, 90, x, 990], fill=col, width=1)
    for lat in range(45, 65, 5):
        _, y = proj(0, lat); d.line([140, y, 1780, y], fill=col, width=1)

def city(d, name, a, t, color=INK, big=False, label=True, dx=18, dy=-20):
    x, y = proj(*CITY[name])
    dot(d, x, y, 10 if big else 7, RED if big else color, a, ring=big, t=t)
    if label: text(d, name.upper(), x + dx, y + dy, 26 if big else 22, "semi", INK if big else MUTED, a=a, rise=0)
    return x, y

def timeline(d, t, items, y=540, x0=200, x1=1720, start=0.0):
    line(d, x0, y, x1, y, (70, 80, 104), 4, A(t, start, 0.8))
    n = len(items)
    for i, (lab, desc, when, col) in enumerate(items):
        x = x0 + (i + 0.5) * (x1 - x0) / n
        a = A(t, when)
        dot(d, x, y, 12, col, a, ring=False)
        up = i % 2 == 0
        text(d, lab, x, y - 170 if up else y + 50, 56, "black", col, "c", a=a)
        text(d, desc, x, y - 100 if up else y + 120, 36, "semi", INK, "c", a=a, maxw=(x1 - x0) / n * 1.1)

def bullets(img, d, t, dur, c, items, title=None, src=None, x=260, y=320, size=56):
    if title: text(d, title, x, y - 110, 30, "semi", GOLD, a=A(t, 0), track=3)
    for i, (s, p) in enumerate(items):
        a = A(t, _at(c, p, 0.4 + i))
        dot(d, x + 10, y + i * 130 + size * 0.62, 9, RED, a, ring=False)
        text(d, s, x + 50, y + i * 130, size, "bold", INK, a=a, maxw=1500)
    if src: source(d, src, A(t, 0.5))

def split_view(img, d, t, dur, c, left_t, right_t, left_v, right_v, right_color=RED, mode="text", right_at=1.5):
    rect(d, 120, 200, 800, 640, fill=(18, 24, 38), outline=(50, 60, 82), r=16, a=A(t, 0))
    rect(d, 1000, 200, 800, 640, fill=(18, 24, 38), outline=(50, 60, 82), r=16, a=A(t, 0.3))
    text(d, left_t, 520, 250, 34, "semi", MUTED, "c", a=A(t, 0.2))
    text(d, right_t, 1400, 250, 34, "semi", MUTED, "c", a=A(t, 0.5), maxw=740)
    if mode == "chart":
        pts = [(220 + i * 60, 600 - 40 * math.sin(i * 0.5) - i * 8) for i in range(11)]
        k = int(len(pts) * ease(A(t, 0.5, 1.5)))
        if k > 1: d.line(pts[:k], fill=TEAL, width=5)
        rng = random.Random(int(t * 12))
        if A(t, 1.0) > 0:
            for _ in range(160):
                x = rng.uniform(1060, 1740); y = rng.uniform(340, 780)
                d.line([x, y, x + rng.uniform(-60, 60), y + rng.uniform(-60, 60)], fill=mix(BG, (90, 100, 125), 0.6 * ease(A(t, 1.0))), width=2)
            text(d, "?", 1400, 450, 160, "black", RED, "c", a=A(t, 1.4))
    else:
        text(d, left_v, 520, 450, 96, "black", INK, "c", a=A(t, 0.6))
        text(d, right_v, 1400, 450, 96, "black", right_color, "c", a=A(t, _at(c, right_at, 1.5)))

def bar_chart(img, d, t, dur, c, title, bars, unit="%", maxv=100, src=None, y0=860, h=520):
    """bars: list of (label, value, phrase_or_time, color). Values ONLY from the fact table."""
    text(d, title, W / 2, 140, 36, "semi", INK, "c", a=A(t, 0), maxw=1500)
    n = len(bars); bw = 220; gap = (1500 - n * bw) / (n - 1) if n > 1 else 0
    line(d, 180, y0, 1740, y0, (70, 80, 104), 3, A(t, 0.1))
    for i, (lab, v, when, col) in enumerate(bars):
        x = 210 + i * (bw + gap)
        p = ease(A(t, _at(c, when, 0.5 + i * 0.5), 1.0))
        bh = h * v / maxv * p
        if bh > 1: d.rectangle([x, y0 - bh, x + bw, y0], fill=col)
        text(d, f"{v * p:.0f}{unit}" if p > 0 else "", x + bw / 2, y0 - bh - 80, 60, "black", INK, "c", a=p, rise=0)
        text(d, lab, x + bw / 2, y0 + 24, 36, "semi", MUTED, "c", a=A(t, 0.2))
    if src: source(d, src, A(t, 0.5))

def big_number(img, d, t, dur, c, value, label, sub=None, color=INK, kicker=None, src=None, when=0.2, size=200):
    if kicker: text(d, kicker, W / 2, 300, 32, "semi", GOLD, "c", a=A(t, 0), track=3)
    text(d, value, W / 2, 360, size, "black", color, "c", a=A(t, _at(c, when, 0.2)))
    text(d, label, W / 2, 360 + size * 1.25, 48, "semi", INK, "c", a=A(t, min(0.3, _at(c, when, 0.2) + 0.4)), maxw=1500)
    if sub: text(d, sub, W / 2, 360 + size * 1.25 + 90, 36, "med", MUTED, "c", a=A(t, _at(c, when, 0.2) + 0.8), maxw=1500)
    if src: source(d, src, A(t, 0.5))

def filing(img, d, t, dur, c, title, rows, header="FILING", tag=True, x=260, w=820, caption=None):
    """A recreated document (always tagged RECREATION). rows: list of (key, value, highlight_phrase_or_None)."""
    if caption: text(d, caption, 1180, 440, 72, "black", INK, a=A(t, 1.0), maxw=640)
    yy = paper(d, x, 160, w, 760, a=A(t, 0, 0.6))
    if yy is None: return
    ptext(d, header, x + 50, yy + 40, 22, "serifb", (90, 90, 96), a=A(t, 0.3))
    ptext(d, title, x + 50, yy + 80, 40, "serifb", a=A(t, 0.3))
    for i, (k, v, hlp) in enumerate(rows):
        ry = yy + 200 + i * 90
        hl = A(t, _at(c, hlp, 99), 0.6) if hlp else 0
        if hl > 0: d.rectangle([x + 40, ry - 8, x + 40 + (w - 80) * ease(hl), ry + 52], fill=mix(PAPER, (250, 215, 90), ease(hl)))
        ptext(d, k, x + 50, ry, 30, "serif", a=A(t, 0.5 + i * 0.2))
        ptext(d, v, x + w - 300, ry, 30, "serifb", a=A(t, 0.5 + i * 0.2))
    fake_lines(d, x + 50, yy + 200 + len(rows) * 90 + 30, w - 120, 6, a=A(t, 0.6), seed=21)
    if tag: recreation(d, x + 20, yy + 720, A(t, 0.4))

def quote(img, d, t, dur, c, s, attrib=None, size=96, color=INK):
    text(d, s, W / 2, 420, size, "black", color, "c", a=A(t, 0.2), maxw=1600)
    if attrib: text(d, attrib, W / 2, 640, 36, "med", MUTED, "c", a=A(t, 0.8))

def calendar(d, x, y, top, big, a):
    if a <= 0: return
    rect(d, x, y, 360, 380, fill=(236, 231, 220), r=14, a=a)
    rect(d, x, y, 360, 90, fill=RED, r=14, a=a)
    text(d, top, x + 180, y + 22, 40, "black", INK, "c", a=a, rise=0)
    f = font("black", 150)
    d.text((x + 180 - d.textlength(big, font=f) / 2, y + 140), big, font=f, fill=mix(BG, (30, 30, 34), ease(a)))

def cal_scene(img, d, t, dur, c, top, big, line1, line2=None, color=INK):
    calendar(d, 260, 300, top, big, A(t, 0, 0.5))
    text(d, line1, 760, 400, 64, "black", color, a=A(t, 0.5), maxw=1050)
    if line2: text(d, line2, 760, 600, 40, "med", MUTED, a=A(t, 1.0), maxw=1050)

def tl_scene(img, d, t, dur, c, title, items):
    """items: list of (big label, description, phrase, color)"""
    text(d, title, W / 2, 760, 170, "black", (26, 33, 50), "c", a=A(t, 0), rise=0)
    text(d, title, W / 2, 180, 30, "semi", GOLD, "c", a=A(t, 0), track=2)
    timeline(d, t, [(a_, b_, min(0.4, _at(c, p, 0.5)) if i == 0 else _at(c, p, 0.5 + i * 1.5), col) for i, (a_, b_, p, col) in enumerate(items)])

def endscreen(img, d, t, dur, c, next_title="NEXT VIDEO TITLE\nON TWO LINES"):
    """Last 16 s (TAIL). Left box = YouTube end-screen video element, right circle = Subscribe element."""
    text(d, "NEXT", 160, 210, 32, "semi", GOLD, a=A(t, 0.2), track=3)
    rect(d, 160, 270, 960, 540, fill=(20, 26, 40), outline=GOLD, width=4, r=16, a=A(t, 0.3))
    text(d, next_title, 640, 470, 64, "black", INK, "c", a=A(t, 0.5), rise=0)
    d.ellipse([1340, 330, 1740, 730], outline=mix(BG, (90, 100, 125), ease(A(t, 0.6))), width=4)
    text(d, "SUBSCRIBE", 1540, 510, 40, "black", INK, "c", a=A(t, 0.7), rise=0)
    text(d, "Sources and fact-check in the description.", W / 2, 920, 30, "med", MUTED, "c", a=A(t, 1.0))
