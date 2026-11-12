"""Directed narration for a faceless-shorts project (Piper, offline, free): deliberate pauses, emphasis on the
important words, and a broadcast polish, so it sounds like a presenter and not a text reader.
(owner's requests, Nov 11: "pauses at the right time, effort on the important word, like a real professional";
 "no ah / uh sounds")

  python3 pro_voice.py <project> [--model PATH] [--pace 0.88]

script.json lines: { "text": "...", "caps": "...", "say": "<directed text>", "gap": 0.26 }
"say" is the same words as "text" plus direction marks (if "say" is missing, the line is directed automatically
from its punctuation):
    /        a short pause (0.18 s): between two thoughts
    //       a beat (0.36 s): before a reveal, after a question, before the END QUESTION's choice
    *...*    the important words: a touch slower and louder (put them right AFTER a pause mark)
Rules of thumb: one *...* per line (the number or the decision), placed right after a pause mark; a // before every
reveal; two pieces per line, three at most; and the words of "say" must be exactly the words of "text".

v3 (Nov 11): every LINE is spoken by Piper in ONE pass (natural intonation, no half-sentence endings: speaking
fragments on their own made Piper drag the last sound into an "uh"/"um"). The pauses are then made by widening the
natural gaps Piper leaves at those points, the important phrase is slowed (ffmpeg atempo, pitch kept) and lifted,
and the dragged tail at the end of each line is trimmed.
Writes data/narration.wav, data/lines.json AND data/words.json + words.txt (do NOT run words.py after this).
"""
import argparse, json, re, subprocess, tempfile, wave
from pathlib import Path
import numpy as np

PIPER = "/home/claude/piper/piper/piper"
ap = argparse.ArgumentParser()
ap.add_argument("project")
ap.add_argument("--model", default="/home/claude/piper/voices/en-us-ryan-high.onnx")
ap.add_argument("--pace", type=float, default=0.88, help="Piper length scale (<1 = brisker)")
ap.add_argument("--emph", type=float, default=0.92, help="tempo of the *important* words (<1 = slower)")
a = ap.parse_args()
P = Path(a.project); S = json.loads((P / "script.json").read_text())
SHORT, BEAT, EMPH_DB = 0.18, 0.36, 1.8
norm = lambda w: re.sub(r"[^a-z0-9']+", "", w.lower())


def piper(text, scale):
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        subprocess.run([PIPER, "--model", a.model, "--length_scale", f"{scale:.3f}", "--noise_scale", "0.6", "--noise_w", "0.75",
                        "--sentence_silence", "0.0", "--output_file", f.name], input=text.encode(), check=True, capture_output=True)
        with wave.open(f.name) as w:
            sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return sr, x


def frames_db(x, sr, step=0.01):
    f = int(step * sr); n = len(x) // f
    return 20 * np.log10(np.sqrt((x[:n * f].reshape(n, f) ** 2).mean(1)) + 1e-9), f


def trim(x, sr):
    """cut leading silence, and the dragged tail: keep 60 ms after the last frame within 24 dB of the loudest, then fade"""
    db, f = frames_db(x, sr); pk = db.max()
    loud = np.where(db > pk - 24)[0]
    if not len(loud): return x
    s = max(0, loud[0] * f - int(0.02 * sr)); e = min(len(x), (loud[-1] + 1) * f + int(0.06 * sr))
    y = x[s:e].copy(); n = min(len(y) // 4, int(0.04 * sr))
    if n > 0: y[-n:] *= np.linspace(1, 0, n) ** 1.5; y[:int(0.008 * sr)] *= np.linspace(0, 1, int(0.008 * sr))
    return y


def gaps(x, sr):
    """quiet stretches inside the speech: [(start, end)] in samples"""
    db, f = frames_db(x, sr); pk = db.max(); q = db < pk - 30; out, i = [], 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if j - i >= 4 and i > 0 and j < len(q): out.append((i * f, j * f))
            i = j
        else: i += 1
    return out


def stretch(x, sr, tempo):
    with tempfile.TemporaryDirectory() as d:
        with wave.open(f"{d}/i.wav", "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/i.wav", "-af", f"atempo={tempo:.3f}", f"{d}/o.wav"], check=True)
        with wave.open(f"{d}/o.wav") as w:
            return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


def parse(say):
    """-> words [{w, em, pause}] from the directed text"""
    words, em = [], False
    for tok in re.findall(r"//|/|\S+", say):
        if tok in ("/", "//"):
            if words: words[-1]["pause"] = max(words[-1]["pause"], BEAT if tok == "//" else SHORT)
            continue
        st = tok.startswith("*"); en = tok.rstrip(".,:;?!").endswith("*") or tok.endswith("*")
        w = tok.replace("*", "")
        if st: em = True
        if norm(w): words.append({"w": w, "em": em, "pause": 0.0})
        if en: em = False
    return words


def auto_direct(text):
    t = re.sub(r"([:;])\s+", r"\1 // ", text)
    t = re.sub(r"([.?!])\s+(?=\S)", r"\1 // ", t)
    return re.sub(r",\s+(?=(and|but|so|or|before|which|where|then)\b)", ", / ", t)


audio, lines, words_out, t, SR = [], [], [], float(S.get("lead", 0.35)), None
for i, ln in enumerate(S["lines"]):
    W = parse(ln.get("say") or auto_direct(ln["text"]))
    script = [w for w in ln["text"].split() if norm(w)]
    if [norm(w["w"]) for w in W] != [norm(w) for w in script]:
        raise SystemExit(f'line {i}: the words of "say" differ from "text"\n  say : {" ".join(w["w"] for w in W)}\n  text: {" ".join(script)}')
    for k, w in enumerate(script): W[k]["w"] = w                            # keep the script's spelling + punctuation
    # one pass, with a comma where a pause is wanted and the text has none (a mid-sentence comma is natural)
    tts = " ".join(w["w"] + ("," if w["pause"] and k < len(W) - 1 and not re.search(r"[,.:;?!]$", w["w"]) else "") for k, w in enumerate(W))
    sr, x = piper(tts, a.pace); SR = SR or sr; x = trim(x, sr)
    # split at the natural gaps nearest each pause mark
    wt = np.array([len(norm(w["w"])) + 2.5 + (3 if re.search(r"[,.:;?!]$", w["w"]) else 0) for w in W], float)
    ends = np.cumsum(wt) / wt.sum() * len(x)                                 # expected end (samples) of each word
    G = gaps(x, sr); cuts = []                                               # (word index, cut sample, pause)
    db, fr = frames_db(x, sr); pk = db.max()
    for k, w in enumerate(W[:-1]):
        if not w["pause"]: continue
        g = min(G, key=lambda g: abs((g[0] + g[1]) / 2 - ends[k])) if G else None
        if g and abs((g[0] + g[1]) / 2 - ends[k]) < 0.45 * sr and (not cuts or (g[0] + g[1]) // 2 > cuts[-1][1]):
            cuts.append((k, (g[0] + g[1]) // 2, w["pause"], g[1] - g[0])); continue
        # no natural gap there (e.g. "it ate eleven..."): cut at the quietest point between words near the boundary
        lo, hi = int((ends[k] - 0.22 * sr) / fr), int((ends[k] + 0.22 * sr) / fr)
        lo, hi = max(1, lo), min(len(db) - 1, hi)
        if hi > lo:
            m = lo + int(np.argmin(db[lo:hi]))
            if db[m] < pk - 16 and (not cuts or m * fr > cuts[-1][1]):
                cuts.append((k, m * fr + fr // 2, w["pause"], 0))
    print(f"  line {i}: {sum(1 for w in W[:-1] if w['pause'])} pause marks, {len(cuts)} placed")
    segs, s0, k0 = [], 0, 0
    for k, c, pz, glen in cuts:
        segs.append((W[k0:k + 1], x[s0:c], max(0.0, pz - glen / sr))); s0, k0 = c, k + 1
    segs.append((W[k0:], x[s0:], 0.0))
    start = t
    for ws, seg, extra in segs:
        seg = seg.copy(); n = min(len(seg) // 4, int(0.012 * sr))              # tiny fades at every cut: no clicks
        if n > 0: seg[:n] *= np.linspace(0, 1, n); seg[-n:] *= np.linspace(1, 0, n)
        if sum(w["em"] for w in ws) * 2 > len(ws):                           # the important phrase: a bit slower + louder
            seg = stretch(seg, sr, a.emph) * 10 ** (EMPH_DB / 20)
        if not audio: audio.append(np.zeros(int(t * sr), np.float32))
        d = len(seg) / sr; ww = [len(norm(w["w"])) + 2.5 for w in ws]; c = t
        for w, q in zip(ws, ww):
            dd = d * q / sum(ww); words_out.append({"w": w["w"], "line": i, "s": round(c, 3), "e": round(c + dd * 0.92, 3)}); c += dd
        audio.append(seg.astype(np.float32)); t += d
        if extra > 0: audio.append(np.zeros(int(extra * sr), np.float32)); t += extra
    lines.append({"i": i, "text": ln["text"], "start": round(start, 3), "end": round(t, 3)})
    g = float(ln.get("gap", S.get("gap", 0.26))) if i < len(S["lines"]) - 1 else float(S.get("outro", 1.0))
    audio.append(np.zeros(int(g * SR), np.float32)); t += g

y = np.concatenate(audio); y = y / max(1e-6, np.abs(y).max()) * 0.85
(P / "data").mkdir(exist_ok=True)
raw = P / "data/narration_raw.wav"
with wave.open(str(raw), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype(np.int16).tobytes())
# broadcast polish: warmth, presence, air, de-ess, gentle compression, limiter (no make-up gain on breaths: gate first)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af",
                "agate=threshold=0.01:ratio=3:attack=2:release=60,highpass=f=75,lowshelf=g=2.5:f=170,equalizer=f=380:t=q:w=1.1:g=-2.5,"
                "equalizer=f=3300:t=q:w=1.0:g=3,highshelf=g=2:f=9000,deesser=i=0.35,"
                "acompressor=threshold=-20dB:ratio=3:attack=6:release=120:makeup=3dB,alimiter=limit=0.89",
                "-ar", str(SR), "-ac", "1", str(P / "data/narration.wav")], check=True)
raw.unlink()
dur = round(len(y) / SR, 3)
(P / "data/lines.json").write_text(json.dumps({"duration": dur, "voice": "piper:" + Path(a.model).stem + " (directed v3)", "lines": lines}, indent=1))
(P / "data/words.json").write_text(json.dumps(words_out, indent=1))
(P / "data/words.txt").write_text("\n".join(f"{w['s']:7.2f} {w['e']:7.2f}  L{w['line']:<2d} {w['w']}" for w in words_out))
print(f"{P.name}: directed narration {dur:.2f} s, {len(lines)} lines, {len(words_out)} words, "
      f"{sum(1 for l in S['lines'] for m in re.findall('//|/', l.get('say', '')))} pause marks (do not run words.py)")
