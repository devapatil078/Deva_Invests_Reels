"""deva invests sound pack: 15 original sound effects made in code (no samples, no downloads, no licence needed).

  python3 make_sfx.py [out_dir=./sfx]

Writes 3 variants each of: whoosh (scene cuts), pop (cards appearing), click (UI), impact (big reveal), chime (notification),
as 48 kHz stereo 16-bit WAV, every file under 2 s, peak -3 dBFS, plus credits.json. Same seed = same files every run.
"""
import json, sys, wave
from pathlib import Path
import numpy as np
from scipy import signal

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else 'sfx'); OUT.mkdir(parents=True, exist_ok=True)
SR = 48000
rng = np.random.default_rng(2026)


def tt(d): return np.arange(int(d * SR)) / SR
def noise(d): return rng.standard_normal(int(d * SR))
def lp(x, f, o=2): b, a = signal.butter(o, min(f, SR / 2 - 100) / (SR / 2), 'low'); return signal.lfilter(b, a, x)
def hp(x, f, o=2): b, a = signal.butter(o, f / (SR / 2), 'high'); return signal.lfilter(b, a, x)
def bp(x, f0, f1, o=2): b, a = signal.butter(o, [f0 / (SR / 2), f1 / (SR / 2)], 'band'); return signal.lfilter(b, a, x)
def dec(n, a, r):
    """attack a seconds, then exponential decay; r = decay rate (bigger = shorter)"""
    t = np.arange(n) / SR; e = np.exp(-r * np.maximum(0, t - a)); na = max(1, int(a * SR)); e[:na] *= np.linspace(0, 1, na); return e
def chirp(f0, f1, d, k=1.0):
    t = tt(d); f = f0 * (f1 / f0) ** ((t / d) ** k); return np.sin(2 * np.pi * np.cumsum(f) / SR)
def tail(x, ms=8):
    n = int(ms / 1000 * SR); x = x.copy(); x[-n:] *= np.linspace(1, 0, n); return x


def sweep_filter(x, f_lo, f_hi, q=0.3, shape=None):
    """resonant band-pass whose centre glides f_lo -> f_hi -> f_lo (state-variable filter)"""
    n = len(x); k = np.linspace(0, 1, n); s = np.sin(np.pi * k) ** 2 if shape is None else shape(k)
    fc = f_lo + (f_hi - f_lo) * s; y = np.zeros(n); low = band = 0.0
    for i in range(n):
        f = 2 * np.sin(np.pi * fc[i] / SR); high = x[i] - low - q * band; band += f * high; low += f * band; y[i] = band
    return y


# ---------- whoosh: air moving past, panned left -> right ----------
def whoosh(d, lo, hi, q, skew):
    x = noise(d); k = np.linspace(0, 1, len(x))
    y = sweep_filter(x, lo, hi, q, lambda k: np.sin(np.pi * k ** skew) ** 2)
    e = np.sin(np.pi * k ** skew) ** 2.2; y = lp(y * e, 6500)
    pan = np.clip(k * 1.1 - 0.05, 0, 1)
    return np.stack([y * np.cos(pan * np.pi / 2), y * np.sin(pan * np.pi / 2)], 1)

# ---------- pop: soft bubble / card pop ----------
def pop(f0, f1, d, body):
    t = tt(d); x = chirp(f0, f1, d, 0.6) * dec(len(t), 0.0015, 1 / (d * 0.22))
    click = hp(noise(0.006), 1500) * dec(int(0.006 * SR), 0.0002, 900) * 0.25; x[:len(click)] += click
    x += np.sin(2 * np.pi * f1 * 0.5 * t) * dec(len(t), 0.002, 1 / (d * 0.3)) * body
    return lp(x, 5000)

# ---------- click: small UI tap ----------
def click(f, d, bright):
    t = tt(d); tone = (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.03 * t)) * dec(len(t), 0.0003, 1 / (d * 0.18))
    tick = bp(noise(d), 1200, 6000) * dec(len(t), 0.0001, 1 / (d * 0.06)) * bright
    return lp(tone * 0.6 + tick, 8000)

# ---------- impact: deep boom for the big reveal ----------
def impact(d, f_hi, f_lo, grit, sub):
    t = tt(d)
    boom = np.sin(2 * np.pi * np.cumsum(f_lo + (f_hi - f_lo) * np.exp(-t * 18)) / SR) * dec(len(t), 0.002, 3.2)
    subw = np.sin(2 * np.pi * (f_lo * 0.5) * t) * dec(len(t), 0.01, 2.2) * sub
    hit = lp(noise(d), 900) * dec(len(t), 0.0005, 22) * grit
    rumble = lp(noise(d), 160) * dec(len(t), 0.02, 2.5) * 0.35
    x = np.tanh(1.8 * (boom + subw + hit + rumble)); return lp(x, 3000)

# ---------- chime: short notification bell ----------
def bell(f, d):
    t = tt(d); parts = [(1.0, 1.0, 1.0), (2.0, 0.35, 1.6), (2.76, 0.18, 2.4), (5.4, 0.06, 4.0)]
    return sum(np.sin(2 * np.pi * f * r * t) * g * dec(len(t), 0.002, 3.0 * dr / d) for r, g, dr in parts)
def chime(notes, step, d):
    n = int(d * SR); x = np.zeros(n)
    for k, f in enumerate(notes):
        i = int(k * step * SR); b = bell(f, d - k * step); x[i:i + len(b)] += b[:n - i] * (0.85 ** k)
    return lp(x, 7000)


SPEC = [
    ('whoosh_1', 'whoosh', 'quick swish, scene cuts', lambda: whoosh(0.45, 350, 3200, 0.35, 0.8)),
    ('whoosh_2', 'whoosh', 'medium swoosh, scene cuts', lambda: whoosh(0.65, 250, 2400, 0.30, 1.0)),
    ('whoosh_3', 'whoosh', 'long airy whoosh, big scene change', lambda: whoosh(0.95, 180, 1800, 0.28, 1.3)),
    ('pop_1', 'pop', 'soft bubble pop, cards appearing', lambda: pop(620, 260, 0.12, 0.25)),
    ('pop_2', 'pop', 'higher light pop, small labels', lambda: pop(900, 380, 0.09, 0.15)),
    ('pop_3', 'pop', 'round low pop, big cards', lambda: pop(440, 170, 0.16, 0.35)),
    ('click_1', 'click', 'crisp UI tap', lambda: click(2200, 0.05, 0.5)),
    ('click_2', 'click', 'soft muted click', lambda: click(1500, 0.06, 0.25)),
    ('click_3', 'click', 'bright tick, counters / toggles', lambda: click(3000, 0.04, 0.7)),
    ('impact_1', 'impact', 'deep boom, big reveal', lambda: impact(1.6, 120, 48, 0.5, 0.5)),
    ('impact_2', 'impact', 'punchy hit, reveal', lambda: impact(1.1, 160, 60, 0.8, 0.3)),
    ('impact_3', 'impact', 'heavy cinematic boom', lambda: impact(1.9, 100, 40, 0.4, 0.7)),
    ('chime_1', 'chime', 'two-note notification (up)', lambda: chime([1046.5, 1318.5], 0.11, 0.9)),
    ('chime_2', 'chime', 'three-note bright chime', lambda: chime([784.0, 1046.5, 1568.0], 0.09, 1.2)),
    ('chime_3', 'chime', 'single soft bell ding', lambda: chime([1174.7], 0.0, 1.0)),
]

credits = []
for name, kind, desc, make in SPEC:
    x = make()
    if x.ndim == 1: x = np.stack([x, x], 1)
    x = np.stack([tail(x[:, 0]), tail(x[:, 1])], 1)
    x *= 10 ** (-3 / 20) / (np.abs(x).max() + 1e-9)
    assert len(x) / SR < 2.0, name
    with wave.open(str(OUT / f'{name}.wav'), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes())
    credits.append(dict(file=f'{name}.wav', type=kind, use=desc, title=f'deva invests {name.replace("_", " ")}', creator='deva invests (generated in code by make_sfx.py)',
                        licence='Original work, no third-party material. Free to use; no attribution required.', source_url=None,
                        duration_s=round(len(x) / SR, 3), sample_rate=SR, channels=2))
(OUT / 'credits.json').write_text(json.dumps(dict(pack='deva invests SFX v1', made_with='make_sfx.py (numpy + scipy), seed 2026',
                                                  note='All 15 sounds are synthesized from scratch; none are downloaded or sampled.', files=credits), indent=2))
print(f'{len(credits)} sounds -> {OUT}/  ' + ', '.join(f"{c['file']} {c['duration_s']}s" for c in credits))
