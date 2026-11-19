"""Timeline + renderer. Usage:
  python3 render.py frames out_dir t1 t2 ...      # stills at global times
  python3 render.py segment N out.mp4             # render section N's segment
  python3 render.py range T0 T1 out.mp4           # render an arbitrary time range
  python3 render.py timeline                      # print timeline json
"""
import json, os, re, sys, subprocess, time
import numpy as np
from PIL import Image, ImageDraw
import engine as E
import scenes as S
from beats import SECTIONS, GAPS, CHAPTERS, TAIL

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
TEXTS = [s["text"] for s in json.load(open(os.path.join(WORK, "narration_sections.json")))]
RATE = 557 / 44.81  # chars per second measured on the hook take

def durations():
    p = os.path.join(WORK, "durations.json")
    if os.path.exists(p): return json.load(open(p))
    return [44.81] + [len(t) / RATE for t in TEXTS[1:]]

def weights(txt):
    w = np.zeros(len(txt) + 1); acc = 0.0
    for i, ch in enumerate(txt):
        w[i] = acc
        acc += 1.0
        if ch in ".?!": acc += 3.0
        elif ch in ",:;": acc += 1.5
        elif ch == "\n": acc += 3.0
    w[len(txt)] = acc
    return w

class Timeline:
    def __init__(self):
        self.durs = durations()
        self.beats = []  # dicts: start, end, fn, kw, sec, anchor_pos
        self.sec_start = []; self.narr = []
        cur = 0.0
        for s, beats in enumerate(SECTIONS):
            seg0 = cur; n0 = cur + GAPS[s]; n1 = n0 + self.durs[s]
            self.sec_start.append(seg0); self.narr.append((n0, n1))
            txt = TEXTS[s]; w = weights(txt); scale = self.durs[s] / w[-1]
            def tpos(pos, w=w, scale=scale, n0=n0): return n0 + w[pos] * scale
            if s in CHAPTERS:
                num, title = CHAPTERS[s]
                self.beats.append(dict(start=seg0, end=n0 + 0.25, fn="chapter", kw=dict(num=num, title=title), sec=s, pos=0, tpos=tpos, txt=txt))
            for i, (anchor, fn, kw) in enumerate(beats):
                if anchor is None:
                    pos = 0; st = n0 + 0.25 if s in CHAPTERS else seg0
                else:
                    pos = txt.find(anchor)
                    if pos < 0: raise SystemExit(f"anchor not found: s{s} {anchor!r}")
                    st = tpos(pos) - 0.15
                self.beats.append(dict(start=st, end=None, fn=fn, kw=kw, sec=s, pos=pos, tpos=tpos, txt=txt))
            cur = n1
        self.total = cur + TAIL
        for i, b in enumerate(self.beats):
            b["end"] = self.beats[i + 1]["start"] if i + 1 < len(self.beats) else self.total
        for s in range(len(SECTIONS)): pass

    def beat_at(self, T):
        for i, b in enumerate(self.beats):
            if b["start"] <= T < b["end"]: return i
        return len(self.beats) - 1

class Ctx:
    def __init__(self, b): self.b = b; self.fi = 0
    def at(self, phrase):
        txt = self.b["txt"]; p = txt.find(phrase, self.b["pos"])
        if p < 0: p = txt.find(phrase)
        if p < 0: return None
        return self.b["tpos"](p) - self.b["start"]

def draw_beat(tl, i, T, fi):
    b = tl.beats[i]
    t = T - b["start"]; dur = b["end"] - b["start"]
    dark = b["fn"] in ("chapter", "reveal_numbers")
    img = E.background(fi, dark=dark)
    d = ImageDraw.Draw(img)
    c = Ctx(b); c.fi = fi
    getattr(S, b["fn"])(img, d, t, dur, c, **b["kw"])
    if b["fn"] not in ("chapter",):
        img = E.kenburns(img, min(1.0, t / max(dur, 1)), 1.0, 1.025)
    return img

def frame(tl, T, fi, cache):
    i = tl.beat_at(T)
    img = draw_beat(tl, i, T, fi)
    b = tl.beats[i]; XF = 0.4
    if i > 0 and T - b["start"] < XF:
        key = i - 1
        if key not in cache:
            pb = tl.beats[key]
            cache[key] = draw_beat(tl, key, pb["end"] - 1 / E.FPS, fi)
        a = (T - b["start"]) / XF
        img = Image.blend(cache[key], img, E.ease_io(a))
    return img

def encode(tl, T0, T1, out):
    E.init()
    n = int(round((T1 - T0) * E.FPS))
    tmp = out[:-4] + ".part.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{E.W}x{E.H}", "-r", str(E.FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-tune", "animation", "-pix_fmt", "yuv420p", "-g", "60", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    cache = {}; t0 = time.time()
    for k in range(n):
        T = T0 + k / E.FPS
        fi = int(T * E.FPS)
        p.stdin.write(frame(tl, T, fi, cache).tobytes())
    p.stdin.close(); rc = p.wait()
    if rc == 0: os.replace(tmp, out)
    print(f"{out}: {n} frames in {time.time() - t0:.1f}s", flush=True)

if __name__ == "__main__":
    tl = Timeline(); mode = sys.argv[1]
    if mode == "timeline":
        print(json.dumps(dict(total=tl.total, durs=tl.durs, sec_start=tl.sec_start, narr=tl.narr,
                              beats=[(round(b["start"], 2), round(b["end"], 2), b["sec"], b["fn"]) for b in tl.beats]), indent=0))
    elif mode == "frames":
        E.init(); od = sys.argv[2]; os.makedirs(od, exist_ok=True)
        for Ts in sys.argv[3:]:
            T = float(Ts); frame(tl, T, int(T * 30), {}).save(os.path.join(od, f"f_{T:07.2f}.jpg"), quality=88)
    elif mode == "segment":
        s = int(sys.argv[2]); T0 = tl.sec_start[s]
        T1 = tl.sec_start[s + 1] if s + 1 < len(SECTIONS) else tl.total
        encode(tl, T0, T1, sys.argv[3])
    elif mode == "range":
        encode(tl, float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
