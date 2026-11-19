"""Original score + SFX, all synthesized here (no samples). Writes music.wav and sfx.wav for the timeline.
Usage: python3 audio.py out_dir"""
import sys, os, math, json
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter, butter
import render as R

SR = 44100
def midi(n): return 440.0 * 2 ** ((n - 69) / 12)

def lowpass(x, fc):
    b, a = butter(2, fc / (SR / 2)); return lfilter(b, a, x)

def pad_chunk(notes, dur, seed, bright=0.0):
    n = int(dur * SR); t = np.arange(n) / SR
    rng = np.random.default_rng(seed); out = np.zeros(n)
    for m in notes:
        f = midi(m)
        for det in (-0.12, 0.0, 0.11):
            ff = f * 2 ** (det / 12)
            ph = rng.uniform(0, 2 * np.pi)
            # soft saw: few harmonics
            s = sum(np.sin(2 * np.pi * ff * k * t + ph * k) / k for k in range(1, 6))
            out += s
    out /= (len(notes) * 3 * 2.0)
    out = lowpass(out, 700 + 900 * bright)
    env = np.minimum(1, t / 2.0) * np.minimum(1, (dur - t) / 2.0)
    return out * env

def sub(note, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    env = np.minimum(1, t / 1.5) * np.minimum(1, (dur - t) / 1.5)
    return np.sin(2 * np.pi * midi(note) * t) * env * 0.35

CHORDS = [([57, 60, 64, 69], 45), ([53, 57, 60, 65], 41), ([48, 52, 55, 60], 36), ([55, 59, 62, 67], 43)]  # Am F C G (+bass)

def music(total, beats, narr):
    n = int(total * SR) + SR
    mix = np.zeros(n, np.float32)
    L = 8.0; k = 0; t0 = 0.0
    while t0 < total:
        notes, bass = CHORDS[k % 4]
        c = pad_chunk(notes, L + 2.0, k, bright=0.3 * (k % 8 == 7)) + sub(bass - 12, L + 2.0)
        i0 = int(t0 * SR); i1 = min(n, i0 + len(c)); mix[i0:i1] += c[: i1 - i0]
        t0 += L; k += 1
    # pulse: soft low heartbeat every 2 s
    tt = np.arange(int(0.25 * SR)) / SR
    thump = np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 18) * 0.5
    for s in np.arange(4.0, total, 2.0):
        i0 = int(s * SR); mix[i0:i0 + len(thump)] += thump[: max(0, min(len(thump), n - i0))]
    # automation: gentle overall level, swell on chapter cards, near-silence for the 0.1% reveal
    env = np.full(n, 0.55, np.float32)
    for b in beats:
        if b["fn"] == "chapter":
            i0, i1 = int(b["start"] * SR), int(b["end"] * SR)
            env[i0:i1] = np.maximum(env[i0:i1], 0.9)
        if b["fn"] == "reveal_numbers" and b["kw"].get("stage") == 3:
            i0, i1 = int(b["start"] * SR), int(b["end"] * SR)
            env[i0:i1] = 0.12
        if b["fn"] == "endscreen":
            i0 = int(b["start"] * SR); env[i0:] = 0.85
    env = lowpass(env.astype(np.float64), 1.5).astype(np.float32)  # smooth
    mix *= env
    fade = int(3 * SR); mix[-fade:] *= np.linspace(1, 0, fade)
    mix /= max(1e-6, np.abs(mix).max()); mix *= 0.5
    return mix

def noise_sweep(dur=0.7, f0=300, f1=4000, seed=1):
    n = int(dur * SR); rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, n); out = np.zeros(n); y = 0.0
    fc = np.geomspace(f0, f1, n) if f1 > f0 else np.geomspace(f0, f1, n)
    a = np.exp(-2 * np.pi * fc / SR)
    for i in range(n):
        y = a[i] * y + (1 - a[i]) * x[i]; out[i] = y
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    return out * env / (np.abs(out).max() + 1e-9)

def impact():
    n = int(1.2 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (60 * np.exp(-t * 3) + 35) * t) * np.exp(-t * 4)
    rng = np.random.default_rng(3)
    click = lowpass(rng.normal(0, 1, n), 2500) * np.exp(-t * 40) * 0.6
    x = body + click; return x / np.abs(x).max()

def tick():
    n = int(0.03 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 300)

def key_click(seed):
    n = int(0.04 * SR); rng = np.random.default_rng(seed); t = np.arange(n) / SR
    return lowpass(rng.normal(0, 1, n), 3500) * np.exp(-t * 180)

def sfx(total, beats):
    n = int(total * SR) + SR; out = np.zeros(n, np.float32)
    def put(x, T, g):
        i0 = int(T * SR); i1 = min(n, i0 + len(x))
        if i0 < n: out[i0:i1] += (x[: i1 - i0] * g).astype(np.float32)
    wh = [noise_sweep(0.6, 400, 3000, s) for s in range(4)]
    imp = impact(); tk = tick()
    for i, b in enumerate(beats):
        if i == 0: continue
        fn = b["fn"]
        if fn == "chapter": put(imp, b["start"] + 0.05, 0.55); put(wh[i % 4], b["start"] - 0.2, 0.25)
        elif fn in ("big_number", "compare_402", "endscreen"): put(wh[i % 4], b["start"] - 0.3, 0.18); put(imp, b["start"] + 0.3, 0.28)
        else: put(wh[i % 4], b["start"] - 0.3, 0.12)
    return out

if __name__ == "__main__":
    od = sys.argv[1]; os.makedirs(od, exist_ok=True)
    tl = R.Timeline()
    m = music(tl.total, tl.beats, tl.narr)
    wavfile.write(os.path.join(od, "music.wav"), SR, (np.clip(m, -1, 1) * 32767).astype(np.int16))
    s = sfx(tl.total, tl.beats)
    s = s / max(1e-6, np.abs(s).max()) * 0.6
    wavfile.write(os.path.join(od, "sfx.wav"), SR, (np.clip(s, -1, 1) * 32767).astype(np.int16))
    print("total", tl.total)
