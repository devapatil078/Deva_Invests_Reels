"""Scenes for video 3: the bank inside GE (GE Capital). Built on video 2 scenes. Base library + this video's own scenes.
Every figure drawn here is passed in from beats.py, which takes them from facts.md."""
from scenes_base import *
from scenes_base import _at
import math, random

PANEL = (18, 24, 38); EDGE = (50, 60, 82)

def fmt(v, dec=1): return f"{v:,.{dec}f}"

# ---------- Louisiana map ----------
LA = [(-94.04, 33.02), (-91.17, 33.0), (-91.08, 32.65), (-91.16, 32.2), (-90.91, 31.84), (-91.38, 31.3), (-91.63, 31.0),
      (-89.73, 31.0), (-89.85, 30.68), (-89.6, 30.4), (-89.4, 30.05), (-89.2, 29.6), (-89.4, 29.2), (-89.95, 29.25),
      (-90.4, 29.1), (-90.9, 29.05), (-91.4, 29.3), (-91.9, 29.65), (-92.4, 29.55), (-93.2, 29.78), (-93.85, 29.71),
      (-93.7, 30.3), (-93.55, 31.0), (-93.82, 31.6), (-94.04, 31.99)]
def la_proj(lon, lat):
    return 560 + (lon + 94.6) / 6.0 * 900, 960 - (lat - 28.7) / 4.6 * 860
LA_PL = {"RICHLAND PARISH": (-91.75, 32.42), "NEW ORLEANS": (-90.07, 29.95), "BATON ROUGE": (-91.15, 30.45)}

def la_map(img, d, t, dur, c, show_site=True, caption=None, sub=None, src=None):
    a = A(t, 0, 0.8)
    pts = [la_proj(*p) for p in LA]
    if a > 0:
        d.polygon(pts, fill=mix(BG, (24, 32, 50), ease(a)), outline=mix(BG, (90, 104, 132), ease(a)))
    for k, (nm, ll) in enumerate(LA_PL.items()):
        x, y = la_proj(*ll); big = nm == "RICHLAND PARISH"
        if big and not show_site: continue
        aa = A(t, 0.6 + k * 0.3)
        dot(d, x, y, 12 if big else 7, RED if big else MUTED, aa, ring=big, t=t)
        text(d, nm, x + 22, y - 16, 30 if big else 22, "semi", INK if big else MUTED, a=aa, rise=0)
    text(d, "LOUISIANA", 250, 160, 30, "semi", GOLD, a=A(t, 0.2), track=3)
    if caption: text(d, caption, 250, 210, 64, "black", INK, a=A(t, 0.4), maxw=340)
    if sub: text(d, sub, 250, 400, 34, "med", MUTED, a=A(t, 1.0), maxw=380)
    if src: source(d, src, A(t, 0.5))

# ---------- pastry name card ----------
def pastry_name(img, d, t, dur, c, name, line2, sub=None, src=None):
    rect(d, 360, 300, 1200, 300, fill=PANEL, outline=GOLD, width=3, r=18, a=A(t, 0, 0.5))
    text(d, "ISSUER", 420, 330, 26, "semi", GOLD, a=A(t, 0.1), track=3)
    text(d, name, W / 2, 380, 110, "black", INK, "c", a=A(t, 0.2))
    text(d, line2, W / 2, 520, 40, "med", MUTED, "c", a=A(t, _at(c, "fried pastry", 1.0)))
    if sub: text(d, sub, W / 2, 700, 56, "black", RED, "c", a=A(t, _at(c, sub[1], 1.5)), maxw=1600) if isinstance(sub, tuple) else None
    if src: source(d, src, A(t, 0.5))

def pastry_name2(img, d, t, dur, c, name, line2, big, big_at, src=None):
    rect(d, 360, 200, 1200, 260, fill=PANEL, outline=GOLD, width=3, r=18, a=A(t, 0, 0.5))
    text(d, "ISSUER", 420, 230, 26, "semi", GOLD, a=A(t, 0.1), track=3)
    text(d, name, W / 2, 270, 100, "black", INK, "c", a=A(t, 0.2))
    text(d, line2, W / 2, 395, 34, "med", MUTED, "c", a=A(t, _at(c, "fried pastry", 1.0)))
    text(d, big, W / 2, 560, 170, "black", RED, "c", a=A(t, _at(c, big_at, 2.0)))
    if src: source(d, src, A(t, 0.5))

# ---------- bond certificate (recreation) ----------
def bond_cert(img, d, t, dur, c, rows, title="SENIOR SECURED NOTES", issuer="BEIGNET INVESTOR LLC", caption=None, src=None, stamp_s=None, stamp_at=None):
    x, w = 240, 900
    yy = paper(d, x, 150, w, 780, a=A(t, 0, 0.6))
    if yy is None: return
    d.rectangle([x + 24, yy + 24, x + w - 24, yy + 756], outline=mix(PAPER, (150, 130, 90), ease(A(t, 0.2))), width=3)
    d.rectangle([x + 36, yy + 36, x + w - 36, yy + 744], outline=mix(PAPER, (180, 160, 120), ease(A(t, 0.2))), width=1)
    ptext(d, issuer, x + w / 2, yy + 70, 44, "serifb", a=A(t, 0.3), align="c")
    ptext(d, title, x + w / 2, yy + 130, 28, "serif", (90, 90, 96), a=A(t, 0.3), align="c")
    for i, (k, v, hl) in enumerate(rows):
        ry = yy + 230 + i * 92
        h = A(t, _at(c, hl, 99), 0.6) if hl else 0
        if h > 0: d.rectangle([x + 60, ry - 10, x + 60 + (w - 120) * ease(h), ry + 52], fill=mix(PAPER, (250, 215, 90), ease(h)))
        ptext(d, k, x + 80, ry, 30, "serif", a=A(t, 0.5 + i * 0.15))
        ptext(d, v, x + 470, ry, 34, "serifb", a=A(t, 0.5 + i * 0.15))
    recreation(d, x + 50, yy + 710, A(t, 0.4))
    if caption: text(d, caption, 1240, 420, 64, "black", INK, a=A(t, 1.0), maxw=600)
    if stamp_s: stamp(img, stamp_s, 900, 760, RED, -10, 60, A(t, _at(c, stamp_at, 2.0), 0.4))
    if src: source(d, src, A(t, 0.5))

# ---------- deal structure diagram ----------
def node(d, x, y, w, h, title, sub, a, col=INK, edge=EDGE):
    if a <= 0: return
    rect(d, x, y, w, h, fill=PANEL, outline=edge, width=3, r=14, a=a)
    text(d, title, x + w / 2, y + 22, 40, "black", col, "c", a=a, rise=0)
    if sub: text(d, sub, x + w / 2, y + 78, 28, "med", MUTED, "c", a=a, rise=0, maxw=w - 30)

def structure(img, d, t, dur, c, stage=1, src="Meta release, Oct 21, 2025; Bloomberg"):
    """stage 1: owners + JV; 2: + bond + lenders; 3: + lease + guarantee arrows highlighted"""
    a0 = A(t, 0, 0.5)
    node(d, 150, 140, 520, 150, "META", "owns 20%", a0, INK)
    node(d, 1250, 140, 520, 150, "BLUE OWL FUNDS", "own 80%", A(t, 0.2), INK)
    node(d, 660, 430, 600, 160, "THE VENTURE", "owns Hyperion, Richland Parish", A(t, 0.4), GOLD, GOLD)
    arrow(d, 480, 290, 760, 430, MUTED, 4, A(t, 0.6))
    arrow(d, 1440, 290, 1160, 430, MUTED, 4, A(t, 0.6))
    if stage >= 2:
        node(d, 1250, 760, 520, 150, "BEIGNET INVESTOR", "$27.3B of bonds", A(t, 0.3 if stage > 2 else _at(c, "Beignet", 0.8)), RED, RED)
        arrow(d, 1360, 760, 1160, 590, RED, 4, A(t, 0.5 if stage > 2 else _at(c, "Beignet", 0.8) + 0.4))
        node(d, 150, 760, 520, 150, "LENDERS", "Pimco ~$18B + others", A(t, 0.6 if stage > 2 else _at(c, "Pimco", 1.4)), INK)
        arrow(d, 670, 835, 1250, 835, MUTED, 4, A(t, 0.8 if stage > 2 else _at(c, "Pimco", 1.4) + 0.3))
        text(d, "cash", 960, 795, 26, "semi", MUTED, "c", a=A(t, 0.9 if stage > 2 else _at(c, "Pimco", 1.6)), rise=0)
    if stage >= 3:
        la = A(t, _at(c, "the lease", 0.5))
        arrow(d, 420, 290, 700, 560, TEAL, 6, la)
        label_box(d, 760, 330, "RENT · 4-year terms", 28, TEAL, TEAL, la)
        ga = A(t, _at(c, "the guarantee", 3.0))
        line(d, 200, 290, 200, 640, GOLD, 6, ga)
        arrow(d, 200, 640, 660, 560, GOLD, 6, ga)
        label_box(d, 260, 655, "GUARANTEE · first 16 yrs", 28, GOLD, GOLD, ga)
    source(d, src, A(t, 0.5))

# ---------- money flows: $7B in, $3B out ----------
def money_flow(img, d, t, dur, c, src):
    node(d, 160, 400, 480, 160, "BLUE OWL FUNDS", "cash in", A(t, 0), INK)
    node(d, 720, 400, 480, 160, "THE VENTURE", "Hyperion", A(t, 0.1), GOLD, GOLD)
    node(d, 1280, 400, 480, 160, "META", "one-time payment", A(t, 0.2), INK)
    a1 = A(t, _at(c, "seven billion", 0.3)); a2 = A(t, _at(c, "three billion", 1.5))
    arrow(d, 640, 480, 720, 480, TEAL, 6, a1)
    text(d, "~$7B", 400, 260, 110, "black", TEAL, "c", a=a1)
    arrow(d, 1200, 480, 1280, 480, RED, 6, a2)
    text(d, "~$3B", 1520, 260, 110, "black", RED, "c", a=a2)
    text(d, "Meta was paid to bring the project in.", W / 2, 700, 56, "black", INK, "c", a=A(t, _at(c, "Meta was paid", 3.0)))
    source(d, src, A(t, 0.5))

# ---------- bond price chart (only reported prices; straight lines join them) ----------
PRICE_PTS = [("Oct 2025", 0.0, 100.0, "issued at 100"), ("days later", 0.06, 110.0, "~110 within days"),
             ("late Jul 2026", 0.75, 96.0, "~96"), ("Sep 23, 2026", 0.92, 94.4, "94.4 record low"), ("mid-Oct 2026", 1.0, 92.0, "just under 92")]
def price_chart(img, d, t, dur, c, upto=5, anchors=None, src="Bloomberg; Protos; Enterprise (reported prices)", note=None, pts=None):
    pts = pts or PRICE_PTS
    x0, x1, y0, y1 = 260, 1660, 220, 860
    lo, hi = 86.0, 114.0
    def P(f, v): return x0 + f * (x1 - x0), y1 - (v - lo) / (hi - lo) * (y1 - y0)
    text(d, "BEIGNET BOND PRICE  (cents on the dollar)", 260, 140, 30, "semi", GOLD, a=A(t, 0), track=2)
    for v in (90, 100, 110):
        _, yy = P(0, v)
        line(d, x0, yy, x1, yy, (40, 48, 68) if v != 100 else (90, 100, 125), 2 if v != 100 else 3, A(t, 0.1))
        text(d, f"{v}", x0 - 30, yy - 16, 26, "semi", MUTED if v != 100 else INK, "r", a=A(t, 0.1), rise=0)
    text(d, "FACE VALUE", x1 - 10, P(0, 100)[1] - 40, 22, "semi", MUTED, "r", a=A(t, 0.2), rise=0)
    anchors = anchors or [None] * len(pts)
    prev = None
    for i in range(min(upto, len(pts))):
        lab, f, v, tag = pts[i]
        when = _at(c, anchors[i], 0.3 + i * 0.6) if i < len(anchors) else 0.3 + i * 0.6
        if i == 0: when = min(when, 0.3)
        a = A(t, when, 0.8)
        x, y = P(f, v)
        if prev is not None and a > 0:
            px, py = prev; e = ease(a)
            col = TEAL if v >= 100 else RED
            d.line([px, py, px + (x - px) * e, py + (y - py) * e], fill=col, width=6)
        col = TEAL if v >= 100 else RED
        dot(d, x, y, 11, col, a, ring=(i == upto - 1), t=t)
        up = (i % 2 == 1)
        if i == 0:
            text(d, tag, x + 20, y + 22, 32, "black", INK, a=a, rise=0)
        else:
            text(d, tag, x, y - 70 if (v >= 100 or up) else y + 26, 32, "black", col if v < 100 else INK, "c", a=a, rise=0)
        if f > 0.02 and f < 0.2: pass
        else: text(d, lab, x, y1 + 24 + (34 if (i == len(pts) - 1 and len(pts) > 3) else 0), 24, "semi", MUTED, "c", a=a, rise=0)
        prev = (x, y)
    if note: text(d, note, W / 2, 960, 26, "med", MUTED, "c", a=A(t, 0.8))
    source(d, src, A(t, 0.5))

# ---------- price / yield seesaw ----------
def seesaw(img, d, t, dur, c):
    cx, cy = W / 2, 640
    ph = A(t, _at(c, "they pay less", 3.0), 1.2) - A(t, _at(c, "pay more", 1.5), 1.0) * 0.0
    tilt0 = -0.18 * ease(A(t, _at(c, "pay more", 1.5), 0.8))
    tilt = tilt0 + 0.36 * ease(A(t, _at(c, "they pay less", 3.0), 0.8))
    L = 560
    xa, ya = cx - L * math.cos(tilt), cy - L * math.sin(tilt)
    xb, yb = cx + L * math.cos(tilt), cy + L * math.sin(tilt)
    d.polygon([(cx, cy + 10), (cx - 60, cy + 120), (cx + 60, cy + 120)], fill=mix(BG, (60, 70, 92), ease(A(t, 0))))
    d.line([xa, ya, xb, yb], fill=mix(BG, (150, 160, 180), ease(A(t, 0))), width=10)
    node(d, xa - 170, ya - 170, 340, 150, "PRICE", "what you pay", A(t, 0.1), INK)
    yc = A(t, _at(c, "the yield", 4.5))
    node(d, xb - 170, yb - 170, 340, 150, "YIELD", "what you earn", A(t, 0.1), GOLD if yc <= 0 else RED, GOLD)
    text(d, "Price down = yield up", W / 2, 880, 64, "black", RED, "c", a=yc)
    text(d, "Face value = 100", W / 2, 170, 40, "semi", MUTED, "c", a=A(t, 0.3))

# ---------- horizontal bars ----------
def hbars(img, d, t, dur, c, title, bars, unit="", prefix="", maxv=None, src=None, dec=0, y0=300, gap=170, note=None):
    """bars: (label, value, phrase, color)"""
    maxv = maxv or max(b[1] for b in bars)
    text(d, title, 200, 170, 34, "semi", GOLD, a=A(t, 0), track=2, maxw=1500)
    for i, (lab, v, when, col) in enumerate(bars):
        y = y0 + i * gap
        tw_ = _at(c, when, 0.4 + i * 0.8)
        if i == 0: tw_ = min(tw_, 0.35)
        p = ease(A(t, tw_, 1.0))
        text(d, lab, 200, y, 34, "semi", INK, a=A(t, tw_ - 0.2 if tw_ > 0.2 else 0), rise=0)
        bw = 1150 * v / maxv * p
        if bw > 1: d.rectangle([200, y + 52, 200 + bw, y + 52 + 64], fill=col)
        if p > 0: text(d, f"{prefix}{v * p:,.{dec}f}{unit}", 200 + bw + 24, y + 52, 56, "black", INK, a=p, rise=0)
    if note: text(d, note, 200, 960, 28, "med", MUTED, a=A(t, 0.8))
    if src: source(d, src, A(t, 0.5))

# ---------- gas plants ----------
def plants(img, d, t, dur, c, src):
    text(d, "POWER FOR HYPERION", W / 2, 150, 30, "semi", GOLD, "c", a=A(t, 0), track=3)
    a1 = _at(c, "Three were approved", 0.3); a2 = _at(c, "seven more", 2.0)
    for i in range(10):
        x = 260 + i * 145; y = 420
        when = min(0.35, a1) + i * 0.15 if i < 3 else a2 + (i - 3) * 0.12
        a = A(t, when, 0.5)
        col = TEAL if i < 3 else RED
        rect(d, x, y + 120, 110, 160, fill=(30, 38, 56), outline=col, width=3, r=6, a=a)
        rect(d, x + 20, y, 30, 140, fill=(40, 49, 70), outline=col, width=2, a=a)
        rect(d, x + 62, y + 40, 26, 100, fill=(40, 49, 70), outline=col, width=2, a=a)
    text(d, "3 approved, 2025", 260 + 145, 740, 34, "semi", TEAL, "c", a=A(t, a1 + 0.3))
    text(d, "+7 Meta agreed to fund, Mar 2026", 260 + 145 * 6.5, 740, 34, "semi", RED, "c", a=A(t, a2 + 0.6))
    text(d, "10 plants · more than 7 GW", W / 2, 830, 64, "black", INK, "c", a=A(t, _at(c, "Ten plants", 4.0)))
    source(d, src, A(t, 0.5))

# ---------- vote card ----------
def votes(img, d, t, dur, c, rows, src):
    text(d, "LOUISIANA PUBLIC SERVICE COMMISSION", W / 2, 160, 30, "semi", GOLD, "c", a=A(t, 0), track=3)
    for i, (when_s, what, tally, p) in enumerate(rows):
        y = 280 + i * 210
        tw_ = _at(c, p, 0.4 + i * 1.5)
        if i == 0: tw_ = min(tw_, 0.35)
        a = A(t, tw_)
        rect(d, 220, y, 1480, 170, fill=PANEL, outline=EDGE, r=14, a=a)
        text(d, when_s, 270, y + 30, 32, "semi", MUTED, a=a, rise=0)
        text(d, what, 270, y + 82, 44, "bold", INK, a=a, rise=0, maxw=1050)
        text(d, tally, 1650, y + 46, 72, "black", RED, "r", a=a, rise=0)
    source(d, src, A(t, 0.5))

# ---------- pimco sells ----------
def sell_blocks(img, d, t, dur, c, src):
    text(d, "PIMCO'S BEIGNET POSITION", 200, 160, 30, "semi", GOLD, a=A(t, 0), track=3)
    text(d, "~$18B anchored", 200, 210, 64, "black", INK, a=A(t, 0.2))
    sold = A(t, _at(c, "sold about three billion", 1.5), 1.2)
    for i in range(18):
        r_, k = divmod(i, 6)
        x = 220 + k * 150; y = 360 + r_ * 150
        moving = i >= 15
        dx = 330 * ease(sold) if moving else 0
        col = RED if moving and sold > 0 else (70, 90, 130)
        rect(d, x + dx, y, 130, 120, fill=mix((30, 38, 56), col, 0.6), outline=col, width=3, r=8, a=A(t, 0.3 + i * 0.03))
    text(d, "each block ≈ $1B (illustration)", 220, 840, 24, "med", MUTED, a=A(t, 0.6))
    text(d, "~$3B SOLD", 1480, 440, 72, "black", RED, a=A(t, _at(c, "sold about three billion", 1.5) + 0.8))
    text(d, "while the price was above 100", 1480, 550, 34, "semi", INK, a=A(t, _at(c, "above a hundred", 2.5)), maxw=340)
    text(d, "~half as much of each position now", 1480, 680, 34, "semi", MUTED, a=A(t, _at(c, "half as much", 4.0)), maxw=340)
    source(d, src, A(t, 0.5))

# ---------- two-panel compare ----------
def compare(img, d, t, dur, c, lt, lv, rt, rv, lcol=TEAL, rcol=RED, rat=1.5, lsub=None, rsub=None, src=None, title=None):
    if title: text(d, title, W / 2, 120, 30, "semi", GOLD, "c", a=A(t, 0), track=3)
    rect(d, 120, 200, 800, 640, fill=PANEL, outline=EDGE, r=16, a=A(t, 0))
    rect(d, 1000, 200, 800, 640, fill=PANEL, outline=EDGE, r=16, a=A(t, _at(c, rat, 1.5) - 0.3))
    text(d, lt, 520, 260, 36, "semi", MUTED, "c", a=A(t, 0.1), maxw=720)
    text(d, lv, 520, 420, 130, "black", lcol, "c", a=A(t, 0.3))
    if lsub: text(d, lsub, 520, 620, 34, "med", INK, "c", a=A(t, 0.6), maxw=700)
    ra = _at(c, rat, 1.5)
    text(d, rt, 1400, 260, 36, "semi", MUTED, "c", a=A(t, ra), maxw=720)
    text(d, rv, 1400, 420, 130, "black", rcol, "c", a=A(t, ra + 0.2))
    if rsub: text(d, rsub, 1400, 620, 34, "med", INK, "c", a=A(t, ra + 0.5), maxw=700)
    if src: source(d, src, A(t, 0.5))

# ---------- stock up / bond down ----------
def stock_vs_bond(img, d, t, dur, c, src):
    rect(d, 120, 200, 800, 640, fill=PANEL, outline=EDGE, r=16, a=A(t, 0))
    rect(d, 1000, 200, 800, 640, fill=PANEL, outline=EDGE, r=16, a=A(t, 0.2))
    text(d, "META STOCK", 520, 250, 36, "semi", MUTED, "c", a=A(t, 0.1))
    text(d, "BEIGNET BOND", 1400, 250, 36, "semi", MUTED, "c", a=A(t, 0.3))
    p = ease(A(t, 0.4, 1.6))
    arrow(d, 300, 720, 300 + 440 * p, 720 - 360 * p, TEAL, 10, 1.0 if p > 0 else 0, 40)
    arrow(d, 1180, 380, 1180 + 440 * p, 380 + 320 * p, RED, 10, 1.0 if p > 0 else 0, 40)
    text(d, "soaring", 520, 760, 48, "black", TEAL, "c", a=A(t, 1.2))
    text(d, "94.4 · record low", 1400, 760, 48, "black", RED, "c", a=A(t, 1.4))
    text(d, "SEPTEMBER 23, 2026", W / 2, 900, 34, "semi", GOLD, "c", a=A(t, 0.6), track=3)
    source(d, src, A(t, 0.5))

# ---------- exposure counters ----------
def exposure(img, d, t, dur, c, src):
    text(d, "META'S MAXIMUM EXPOSURE TO LOSS · DATA CENTER VENTURES", W / 2, 150, 30, "semi", GOLD, "c", a=A(t, 0), track=2)
    a1 = min(0.35, _at(c, "forty-six billion", 0.3)); a2 = _at(c, "sixty-eight point four", 3.0)
    text(d, "Dec 31, 2025", 520, 300, 36, "semi", MUTED, "c", a=A(t, a1))
    counter(d, 520, 380, 0, 45.952, A(t, a1, 1.4), 150, "$", "B", INK, a=A(t, a1), decimals=1)
    text(d, "Sep 30, 2026", 1400, 300, 36, "semi", MUTED, "c", a=A(t, a2))
    counter(d, 1400, 380, 45.952, 68.404, A(t, a2, 1.6), 150, "$", "B", RED, a=A(t, a2), decimals=1)
    arrow(d, 860, 470, 1060, 470, MUTED, 5, A(t, a2))
    g = _at(c, "residual value guarantees", 6.0)
    text(d, "of which residual value guarantees", W / 2, 640, 34, "semi", GOLD, "c", a=A(t, g))
    text(d, "$28.1B  →  $41.5B", W / 2, 700, 96, "black", INK, "c", a=A(t, g + 0.4))
    text(d, "Meta's stake in the ventures: 20%", W / 2, 880, 40, "bold", MUTED, "c", a=A(t, _at(c, "Meta owns twenty percent", 12.0)))
    source(d, src, A(t, 0.5))

# ---------- leverage chart with threshold ----------
def leverage(img, d, t, dur, c, src):
    text(d, "S&P: META'S ADJUSTED LEVERAGE (expected)", W / 2, 150, 32, "semi", GOLD, "c", a=A(t, 0), track=2)
    vals = [("2025", 0.1), ("2026", 0.3), ("2027", 1.1), ("2028", 1.3)]
    y0, h = 860, 520; maxv = 1.5
    _, thy = 0, y0 - h * 1.0 / maxv
    for i, (yr, v) in enumerate(vals):
        x = 380 + i * 320
        p = ease(A(t, 0.3 + i * 0.5, 0.8))
        bh = h * v / maxv * p
        col = RED if v >= 1.0 else TEAL
        if bh > 1: d.rectangle([x, y0 - bh, x + 200, y0], fill=col)
        if p > 0: text(d, f"{v * p:.1f}x", x + 100, y0 - bh - 76, 56, "black", INK, "c", a=p, rise=0)
        text(d, yr, x + 100, y0 + 20, 36, "semi", MUTED, "c", a=A(t, 0.2))
    ta = A(t, _at(c, "Above one times", 4.0))
    for xx in range(300, 1660, 40): d.line([xx, thy, xx + 22, thy], fill=mix(BG, GOLD, ease(ta)), width=4)
    text(d, "1.0x · downgrade line", 1660, thy - 50, 30, "bold", GOLD, "r", a=ta, rise=0)
    source(d, src, A(t, 0.5))

# ---------- the mismatch: duration bars ----------
def mismatch(img, d, t, dur, c, src, rows):
    """rows: (label, years, phrase, color)"""
    text(d, "HOW LONG EACH PIECE LASTS", 200, 140, 32, "semi", GOLD, a=A(t, 0), track=3)
    x0 = 520; scale = 1120 / 24.0
    for yv in (0, 4, 8, 12, 16, 20, 24):
        xx = x0 + yv * scale
        d.line([xx, 230, xx, 900], fill=mix(BG, (34, 42, 60), ease(A(t, 0.1))), width=2)
        text(d, f"{yv} yrs", xx, 910, 22, "semi", MUTED, "c", a=A(t, 0.1), rise=0)
    for i, (lab, yrs, when, col) in enumerate(rows):
        y = 260 + i * 160
        tw_ = _at(c, when, 0.5 + i)
        if i == 0: tw_ = min(tw_, 0.35)
        p = ease(A(t, tw_, 1.0))
        text(d, lab, 200, y + 24, 36, "bold", INK, a=A(t, tw_), rise=0, maxw=300)
        bw = yrs * scale * p
        if bw > 1: d.rounded_rectangle([x0, y + 10, x0 + bw, y + 90], radius=8, fill=col)
        if p > 0.05: text(d, f"{yrs:g} yrs", x0 + bw + 18, y + 22, 48, "black", col, a=p, rise=0)
    source(d, src, A(t, 0.5))

# ---------- coupon compare ----------
def coupons(img, d, t, dur, c, src):
    compare(img, d, t, dur, c, "Meta 30-year bond · Oct 2025", "5.625%", "Meta 30-year notes · Nov 2026", "7.5%",
            TEAL, RED, "Its newest thirty-year", "coupon", "coupon", src, "THE PRICE OF BORROWING")

# ---------- watch list ----------
def watch(img, d, t, dur, c, items, src=None):
    text(d, "WHAT TO WATCH", 260, 200, 30, "semi", GOLD, a=A(t, 0), track=3)
    for i, (num, s, p) in enumerate(items):
        y = 300 + i * 190
        tw_ = _at(c, p, 0.4 + i)
        if i == 0: tw_ = min(tw_, 0.35)
        a = A(t, tw_)
        text(d, num, 260, y, 110, "black", RED, a=a)
        text(d, s, 420, y + 30, 54, "bold", INK, a=a, maxw=1300)
    if src: source(d, src, A(t, 0.5))

# ---------- risk moved ----------
def risk_moved(img, d, t, dur, c):
    node(d, 180, 420, 560, 170, "META'S BALANCE SHEET", None, A(t, 0), INK)
    node(d, 1180, 420, 560, 170, "THE LENDERS", "funds · pensions · insurers · savers", A(t, 0.2), GOLD, GOLD)
    p = ease(A(t, _at(c, "the risk moved", 0.5), 1.6))
    x = 460 + (1460 - 460) * p
    d.ellipse([x - 60, 300 - 60, x + 60, 300 + 60], fill=mix(BG, RED, ease(A(t, 0.3))))
    text(d, "RISK", x, 280, 34, "black", INK, "c", a=A(t, 0.3), rise=0)
    text(d, "Not investment advice.", W / 2, 820, 34, "med", MUTED, "c", a=A(t, _at(c, "This isn't investment advice", 5.0)))

def headline(img, d, t, dur, c, kicker, big, sub=None, color=RED, src=None, sub_at=1.0):
    text(d, kicker, W / 2, 300, 32, "semi", GOLD, "c", a=A(t, 0), track=3)
    sz = 130
    while d.textlength(big, font=font("black", sz)) > 1700 and sz > 60: sz -= 6
    text(d, big, W / 2, 380 + (130 - sz) * 0.5, sz, "black", color, "c", a=A(t, 0.15))
    if sub: text(d, sub, W / 2, 620, 44, "semi", INK, "c", a=A(t, _at(c, sub_at, 1.0)), maxw=1500)
    if src: source(d, src, A(t, 0.5))

# ======================= video 3: GE Capital =======================
DARKP = (14, 19, 30)

def factory(d, x, y, s, a, lit=0.0, vault=0.0, t=0):
    """Generic factory silhouette (no logo). vault>0 reveals a glowing bank vault inside."""
    if a <= 0: return
    e = ease(a)
    col = mix(BG, (34, 42, 62), e); edge = mix(BG, (70, 80, 104), e)
    # chimneys
    for k, (cx, ch) in enumerate([(0.12, 0.55), (0.24, 0.7), (0.36, 0.5)]):
        d.rectangle([x + cx * s, y - ch * s * 0.35, x + cx * s + 0.06 * s, y], fill=col, outline=edge)
        # smoke puffs
        for j in range(3):
            ph = ((t * 0.25 + j / 3 + k * 0.2) % 1.0)
            r = 0.014 * s * (1 + ph * 1.5)
            sx = x + cx * s + 0.03 * s + ph * 0.05 * s; sy = y - ch * s * 0.35 - ph * 0.12 * s
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=mix(BG, (60, 68, 88), e * (1 - ph) * 0.7))
    # saw-tooth roof hall
    pts = [(x, y + 0.45 * s)]
    n = 6
    for k in range(n):
        x0 = x + k * s / n
        pts += [(x0, y), (x0 + s / n, y - 0.12 * s), (x0 + s / n, y)]
    pts += [(x + s, y + 0.45 * s)]
    d.polygon(pts, fill=col, outline=edge)
    # windows
    for r_ in range(2):
        for c_ in range(10):
            on = (c_ * 3 + r_ * 5) % 4 == 0
            wx = x + 0.05 * s + c_ * 0.092 * s; wy = y + 0.07 * s + r_ * 0.15 * s
            fc = mix((22, 28, 42), (245, 205, 120), lit * e) if on else (22, 28, 42)
            d.rectangle([wx, wy, wx + 0.05 * s, wy + 0.08 * s], fill=mix(BG, fc, e))
    if vault > 0:
        v = ease(vault); cx, cy, R = x + 0.62 * s, y + 0.24 * s, 0.17 * s * (0.6 + 0.4 * v)
        for g in range(4, 0, -1):
            rr = R * (1 + g * 0.08)
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=mix(col, (120, 90, 30), v * 0.12 * (7 - g) / 6))
        d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=mix(col, (60, 52, 34), v), outline=mix(col, GOLD, v), width=6)
        d.ellipse([cx - R * 0.72, cy - R * 0.72, cx + R * 0.72, cy + R * 0.72], outline=mix(col, GOLD, v), width=3)
        ang = t * 0.6
        for k in range(6):
            aa = ang + k * math.pi / 3
            d.line([cx, cy, cx + math.cos(aa) * R * 0.62, cy + math.sin(aa) * R * 0.62], fill=mix(col, GOLD, v), width=6)
        d.ellipse([cx - R * 0.16, cy - R * 0.16, cx + R * 0.16, cy + R * 0.16], fill=mix(col, GOLD, v))

def factory_bank(img, d, t, dur, c, line1, line2=None, vault_at=None, l2_at=None, src=None):
    va = A(t, _at(c, vault_at, 1.0), 1.2) if vault_at is not None else 0
    factory(d, 410, 500, 1100, A(t, 0, 0.5), lit=1.0, vault=va, t=t)
    line(d, 120, 500 + 0.45 * 1100, 1800, 500 + 0.45 * 1100, (60, 70, 92), 3, A(t, 0))
    text(d, line1, W / 2, 70, 76, "black", INK, "c", a=A(t, 0.1), maxw=1700)
    if line2: text(d, line2, W / 2, 175, 60, "black", GOLD, "c", a=A(t, _at(c, l2_at, 1.2)), maxw=1700)
    if src: source(d, src, A(t, 0.5))

def deal_stack(img, d, t, dur, c, items, title, total=None, total_at=None, src=None):
    """Stacked cards: (date, label, value, phrase, color). Used for the hook's rescue list."""
    text(d, title, 200, 130, 32, "semi", GOLD, a=A(t, 0), track=3)
    for i, (dt, lab, val, p, col) in enumerate(items):
        tw_ = _at(c, p, 0.4 + i * 1.2)
        if i == 0: tw_ = min(tw_, 0.3)
        a = A(t, tw_, 0.5)
        y = 220 + i * 175
        x = 200 + (1 - ease(a)) * 80
        rect(d, x, y, 1520, 150, fill=PANEL, outline=col if a > 0 else EDGE, width=3, r=14, a=a)
        text(d, dt, x + 40, y + 24, 28, "semi", MUTED, a=a, rise=0)
        text(d, lab, x + 40, y + 66, 44, "bold", INK, a=a, rise=0, maxw=1000)
        text(d, val, x + 1480, y + 30, 92, "black", col, "r", a=a, rise=0)
    if total: text(d, total, W / 2, 940, 40, "black", RED, "c", a=A(t, _at(c, total_at, 5.0)))
    if src: source(d, src, A(t, 0.5))

def line_chart(img, d, t, dur, c, title, pts, lo, hi, ticks, prefix="$", dec=2, src=None, unit=""):
    """pts: (xlabel, frac 0..1, value, tag, phrase, color)"""
    x0, x1, y0, y1 = 280, 1640, 240, 840
    def P(f, v): return x0 + f * (x1 - x0), y1 - (v - lo) / (hi - lo) * (y1 - y0)
    text(d, title, 280, 140, 30, "semi", GOLD, a=A(t, 0), track=2)
    for v in ticks:
        _, yy = P(0, v)
        line(d, x0, yy, x1, yy, (40, 48, 68), 2, A(t, 0.1))
        text(d, f"{prefix}{v:g}{unit}", x0 - 24, yy - 16, 26, "semi", MUTED, "r", a=A(t, 0.1), rise=0)
    prev = None
    for i, (lab, f, v, tag, p, col) in enumerate(pts):
        tw_ = _at(c, p, 0.3 + i * 0.8)
        if i == 0: tw_ = min(tw_, 0.3)
        a = A(t, tw_, 0.9); x, y = P(f, v)
        if prev is not None and a > 0:
            e = ease(a); d.line([prev[0], prev[1], prev[0] + (x - prev[0]) * e, prev[1] + (y - prev[1]) * e], fill=col, width=7)
        dot(d, x, y, 12, col, a, ring=(i == len(pts) - 1), t=t)
        text(d, tag, x + (24 if f < 0.8 else -24), y - 76 if v > (lo + hi) / 2 else y + 26, 46, "black", col, "l" if f < 0.8 else "r", a=a, rise=0)
        text(d, lab, x, y1 + 24, 26, "semi", MUTED, "c", a=a, rise=0)
        prev = (x, y)
    if src: source(d, src, A(t, 0.5))

def profit_split(img, d, t, dur, c, total, part, total_lab, part_lab, total_at=None, part_at=None, pct_lab=None, pct_at=None, src=None, title=None):
    if title: text(d, title, W / 2, 130, 30, "semi", GOLD, "c", a=A(t, 0), track=3)
    x0, y0, w, h = 260, 330, 1400, 200
    ta = A(t, min(0.3, _at(c, total_at, 0.3)), 0.8)
    rect(d, x0, y0, w, h, fill=(40, 50, 72), r=12, a=ta)
    text(d, total_lab, x0, y0 - 70, 40, "semi", INK, a=ta, rise=0)
    text(d, f"${total:.1f}B", x0 + w, y0 - 86, 64, "black", INK, "r", a=ta, rise=0)
    pa = ease(A(t, _at(c, part_at, 1.5), 1.2))
    pw = w * part / total * pa
    if pw > 2: d.rounded_rectangle([x0, y0, x0 + pw, y0 + h], radius=12, fill=GOLD)
    text(d, part_lab, x0, y0 + h + 40, 40, "semi", GOLD, a=pa, rise=0)
    text(d, f"${part * pa:.1f}B", x0 + 30, y0 + 52, 90, "black", BG, a=pa, rise=0)
    if pct_lab: text(d, pct_lab, W / 2, 780, 72, "black", RED, "c", a=A(t, _at(c, pct_at, 3.0)))
    if src: source(d, src, A(t, 0.5))

def rollover(img, d, t, dur, c, stop_at=None, label=None, src=None):
    """IOU cards rolling: each expires and is replaced by a new one. stop_at: new card fails to arrive (red gap)."""
    text(d, "COMMERCIAL PAPER = SHORT IOUs", W / 2, 130, 34, "semi", GOLD, "c", a=A(t, 0), track=2)
    st = _at(c, stop_at, 1e9) if stop_at is not None else 1e9
    period = 2.2
    # lenders column and borrower
    node(d, 120, 420, 420, 170, "LENDERS", "money market funds · big investors", A(t, 0), INK)
    node(d, 1380, 420, 420, 170, "GE CAPITAL", "pays each IOU with a new one", A(t, 0.2), GOLD, GOLD)
    for k in range(4):
        ph = ((t / period) + k / 4) % 1.0
        born = t - ph * period
        x = 640 + ph * 680; y = 470
        failed = born > st
        if failed:
            a = A(t, st + 0.3, 0.4)
            rect(d, 900, 640, 120, 80, fill=None, outline=RED, width=4, r=10, a=a)
            continue
        a = min(1.0, ph * 6, (1 - ph) * 6) * A(t, 0.3)
        rect(d, x - 60, y - 10, 120, 80, fill=PAPER, r=10, a=a)
        text(d, "IOU", x, y + 8, 34, "black", PAPER_INK, "c", a=a, rise=0)
    if st < 1e8:
        text(d, "What if nobody buys the next one?", W / 2, 780, 64, "black", RED, "c", a=A(t, st + 0.3))
    elif label:
        text(d, label, W / 2, 780, 56, "black", INK, "c", a=A(t, 1.0), maxw=1600)
    if src: source(d, src, A(t, 0.5))

def short_long(img, d, t, dur, c, long_at=None, src=None):
    text(d, "THE MISMATCH", W / 2, 140, 32, "semi", GOLD, "c", a=A(t, 0), track=3)
    a1 = A(t, 0.2); a2 = A(t, _at(c, long_at, 1.5))
    text(d, "BORROWED FOR", 200, 300, 34, "semi", MUTED, a=a1)
    rect(d, 200, 360, 90 * ease(a1), 100, fill=TEAL, r=8, a=a1)
    text(d, "days or weeks", 320, 376, 60, "black", TEAL, a=a1, rise=0)
    text(d, "LENT OUT FOR", 200, 560, 34, "semi", MUTED, a=a2)
    rect(d, 200, 620, 1500 * ease(a2), 100, fill=RED, r=8, a=a2)
    text(d, "years", 230, 636, 60, "black", INK, a=A(t, _at(c, long_at, 1.5) + 0.6), rise=0)
    if src: source(d, src, A(t, 0.5))

def meter(img, d, t, dur, c, title, cap, cap_lab, steps, unit="B", src=None):
    """Horizontal fill vs a cap line. steps: (value, label, phrase)."""
    text(d, title, 200, 170, 32, "semi", GOLD, a=A(t, 0), track=3)
    x0, y0, w, h = 200, 420, 1520, 140
    rect(d, x0, y0, w, h, fill=(26, 33, 50), outline=EDGE, r=12, a=A(t, 0))
    text(d, f"{cap_lab}: ${cap:g}{unit}", x0 + w, y0 - 60, 36, "semi", MUTED, "r", a=A(t, 0.2), rise=0)
    cur = 0.0; lab = None
    for i, (v, l, p) in enumerate(steps):
        tw_ = _at(c, p, 0.5 + i * 2.0)
        if i == 0: tw_ = min(tw_, 0.35)
        e = ease(A(t, tw_, 1.2))
        if e > 0: cur = cur + (v - cur) * e; lab = (l, v, e)
    if cur > 0:
        d.rounded_rectangle([x0, y0, x0 + w * cur / cap, y0 + h], radius=12, fill=RED)
        text(d, f"${cur:,.2f}{unit}", x0 + w * cur / cap + 20 if cur / cap < 0.7 else x0 + 30, y0 + 30, 72, "black", INK, a=1, rise=0)
    if lab: text(d, lab[0], x0, y0 + h + 50, 44, "semi", INK, a=lab[2], rise=0)
    if src: source(d, src, A(t, 0.5))

def breakup(img, d, t, dur, c, names, at=None, src=None):
    """One GE block splits into three companies."""
    sp = ease(A(t, _at(c, at, 1.0), 1.4))
    W3 = 480
    xs = [W / 2 - W3 * 1.5 - 60 * sp, W / 2 - W3 / 2, W / 2 + W3 / 2 + 60 * sp]
    for i, (nm, sub, p) in enumerate(names):
        a = A(t, 0)
        x = xs[i]
        rect(d, x, 380, W3, 260, fill=PANEL, outline=GOLD if sp > 0.5 else EDGE, width=3, r=14 if sp > 0.2 else 2, a=a)
        aa = A(t, _at(c, p, 1.5 + i))
        text(d, nm, x + W3 / 2, 440, 50, "black", INK, "c", a=aa, rise=0, maxw=W3 - 30)
        text(d, sub, x + W3 / 2, 540, 30, "med", MUTED, "c", a=aa, rise=0, maxw=W3 - 40)
    text(d, "ONE COMPANY → THREE", W / 2, 200, 34, "semi", GOLD, "c", a=A(t, 0), track=3)
    if src: source(d, src, A(t, 0.5))

def turbine(img, d, t, dur, c, counters, src=None):
    """Gas turbine (generic drawing) feeding a data center. counters: (label, value, prefix, suffix, dec, phrase)."""
    a = A(t, 0)
    cx, cy = 520, 470
    # turbine body (cone)
    d.polygon([(cx - 340, cy - 120), (cx + 220, cy - 180), (cx + 220, cy + 180), (cx - 340, cy + 120)], fill=mix(BG, (44, 54, 78), ease(a)), outline=mix(BG, (90, 100, 125), ease(a)))
    for k in range(9):
        xx = cx - 300 + k * 58
        d.line([xx, cy - 110 - k * 7, xx, cy + 110 + k * 7], fill=mix(BG, (70, 80, 104), ease(a)), width=3)
    R = 150; ang = t * 3
    d.ellipse([cx + 220 - 40, cy - R, cx + 220 + 40, cy + R], outline=mix(BG, GOLD, ease(a)), width=4)
    for k in range(8):
        aa = ang + k * math.pi / 4
        d.line([cx + 220, cy, cx + 220 + math.cos(aa) * 30, cy + math.sin(aa) * R * 0.9], fill=mix(BG, GOLD, ease(a)), width=4)
    # power line to data center racks
    pa = A(t, 0.6, 1.0)
    for k in range(5):
        ph = (t * 0.8 + k / 5) % 1
        px = 800 + ph * 260
        dot(d, px, cy, 6, GOLD, pa, ring=False)
    for r_ in range(3):
        rect(d, 1100 + r_ * 110, 330, 90, 280, fill=(22, 28, 42), outline=EDGE, r=6, a=pa)
        for k in range(8):
            on = (int(t * 4) + k + r_) % 3 == 0
            rect(d, 1112 + r_ * 110, 345 + k * 32, 66, 18, fill=TEAL if on else (40, 50, 70), r=3, a=pa)
    text(d, "DATA CENTER", 1255, 630, 28, "semi", MUTED, "c", a=pa, rise=0)
    text(d, "GAS TURBINE (illustration)", cx - 60, 680, 24, "semi", MUTED, "c", a=a, rise=0)
    for i, (lab, v, pre, suf, dec, p) in enumerate(counters):
        tw_ = _at(c, p, 1.0 + i * 2)
        pp = A(t, tw_, 1.2)
        x = 260 + i * 720
        counter(d, x, 760, 0, v, pp, 96, pre, suf, GOLD if i == 0 else INK, "black", "l", A(t, tw_, 0.3), dec)
        text(d, lab, x, 880, 32, "semi", MUTED, a=A(t, tw_, 0.3), rise=0)
    if src: source(d, src, A(t, 0.5))

def dow_board(img, d, t, dur, c, out_at=None, src=None):
    text(d, "DOW JONES INDUSTRIAL AVERAGE", W / 2, 170, 32, "semi", GOLD, "c", a=A(t, 0), track=3)
    oa = A(t, _at(c, out_at, 1.5), 0.6)
    rect(d, 560, 330, 800, 200, fill=PANEL, outline=RED if oa > 0 else EDGE, width=4, r=14, a=A(t, 0.1))
    text(d, "GENERAL ELECTRIC", W / 2, 360, 64, "black", INK, "c", a=A(t, 0.2), rise=0)
    text(d, "continuous member since 1907", W / 2, 450, 34, "med", MUTED, "c", a=A(t, 0.3), rise=0)
    if oa > 0:
        d.line([560, 430, 560 + 800 * ease(oa), 430], fill=RED, width=10)
        stamp(img, "REMOVED · JUNE 2018", W / 2, 700, RED, -6, 64, oa)
    if src: source(d, src, A(t, 0.5))

def insurance_clock(img, d, t, dur, c, src=None):
    """Policy sold in 1989-2006, claims arrive decades later."""
    text(d, "LONG-TERM CARE POLICIES", 200, 160, 32, "semi", GOLD, a=A(t, 0), track=3)
    x0, x1 = 200, 1720
    def X(yr): return x0 + (yr - 1985) / (2030 - 1985) * (x1 - x0)
    line(d, x0, 600, x1, 600, (70, 80, 104), 4, A(t, 0.1))
    for yr in (1990, 2000, 2010, 2020, 2030):
        text(d, str(yr), X(yr), 630, 28, "semi", MUTED, "c", a=A(t, 0.2), rise=0)
    a1 = A(t, 0.3)
    d.rectangle([X(1989), 520, X(1989) + (X(2006) - X(1989)) * ease(a1), 590], fill=mix(BG, TEAL, ease(a1)))
    text(d, "policies written 1989–2006", X(1989), 450, 36, "bold", TEAL, a=a1, rise=0)
    a2 = A(t, _at(c, "often decades after", 2.0), 1.4)
    for k in range(18):
        yr = 1995 + k * 1.9
        hgt = 20 + k * 9
        if yr > 2029: break
        d.rectangle([X(yr), 600 + 10, X(yr) + 20, 610 + hgt * ease(a2)], fill=mix(BG, RED, ease(a2)))
    text(d, "claims keep arriving for decades", X(2012), 820, 36, "bold", RED, "c", a=a2, rise=0)
    a3 = A(t, _at(c, "estimates were too low", 6.0))
    if a3 > 0: stamp(img, "ESTIMATES TOO LOW · 2018", 1300, 330, RED, -8, 52, a3)
    if src: source(d, src, A(t, 0.5))

def endscreen(img, d, t, dur, c, next_title="ENRON: WHO ACTUALLY\nLOST THE MONEY"):
    text(d, "NEXT", 160, 210, 32, "semi", GOLD, a=A(t, 0.2), track=3)
    rect(d, 160, 270, 960, 540, fill=(20, 26, 40), outline=GOLD, width=4, r=16, a=A(t, 0.3))
    text(d, next_title, 640, 460, 64, "black", INK, "c", a=A(t, 0.5), rise=0)
    d.ellipse([1340, 330, 1740, 730], outline=mix(BG, (90, 100, 125), ease(A(t, 0.6))), width=4)
    text(d, "SUBSCRIBE", 1540, 510, 40, "black", INK, "c", a=A(t, 0.7), rise=0)
    text(d, "Sources and fact-check in the description.", W / 2, 920, 30, "med", MUTED, "c", a=A(t, 1.0))
