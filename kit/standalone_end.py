"""Standalone ending (Nov 12, 2026 content strategy): no PART badge, no "NEXT · PART" card. The reel ends on its payoff,
then ONE short end card with ONE ask, spoken by the same narrator with the same polish and the one soft chime.
(Nov 12 FLIPPING run: this copy = the repo's kit/standalone_end.py at local commit d97ab6a, which could not be pushed: copy it into kit/.)

usage: python3 standalone_end.py <in.mp4> <out.mp4> "<spoken ask>" "<line 1>" "<line 2>" ["<line 3>"] [--pill 2]
  the lines are drawn top to bottom; the line number given with --pill (default 2) is drawn as a yellow pill, the others as
  big white text. Examples:
    send ask:     "Send this to someone about to redo their kitchen." "SEND THIS TO" "SOMEONE REDOING" "THEIR KITCHEN"
    keyword ask:  "Comment FLIP for my free flip starter toolkit." "COMMENT" "FLIP" "FOR THE FREE TOOLKIT"
    question ask: "Kitchen or door: which would you pick?" "KITCHEN OR DOOR?" "COMMENT ONE WORD"
Style, voice and sound match series_end_sfx.py (Piper ryan-high, 'ah' cleanup, broadcast polish, chime_1 at -9 dB).
"""
import argparse, math, os, subprocess, tempfile, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('out'); ap.add_argument('spoken'); ap.add_argument('lines', nargs='+'); ap.add_argument('--pill', type=int, default=2)
a = ap.parse_args()
FONT = os.path.expanduser('~/faceless-shorts/bank-money/fonts/Inter-Black.otf'); FONT2 = os.path.expanduser('~/faceless-shorts/bank-money/fonts/Inter-ExtraBold.otf')
PIPER, MODEL = '/home/claude/piper/piper/piper', '/home/claude/piper/voices/en-us-ryan-high.onnx'
W, H, FPS = 1080, 1920, 24
tmp = tempfile.mkdtemp()
run = lambda *x: subprocess.run(list(x), check=True, capture_output=True)
probe = lambda f: float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).decode())


def clean_ah(path):   # same cleanup as series_end_sfx.py: cut Piper's breathy blip after the last word, trim the dragged tail
    with wave.open(path) as f: sr = f.getframerate(); ch = f.getnchannels(); x = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(float) / 32768
    fr = int(0.01 * sr); n = len(x) // fr
    on = 20 * np.log10(np.sqrt((x[:n * fr].reshape(n, fr) ** 2).mean(1)) + 1e-9) > -42; r = []; i = 0
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]: j += 1
            r.append((i * fr, j * fr)); i = j
        else: i += 1
    for _ in range(2):
        if len(r) < 2: break
        s0, e0 = r[-1]; sg = x[s0:e0]; zcr = np.mean(np.abs(np.diff(np.sign(sg)))) / 2 * sr if len(sg) > 2 else 0
        if (e0 - s0) / sr < 0.22 and (s0 - r[-2][1]) / sr >= 0.02 and zcr < 1800: x = x[:r[-2][1] + int(0.03 * sr)]; r = r[:-1]
        else: break
    db = 20 * np.log10(np.sqrt((x[:(len(x) // fr) * fr].reshape(-1, fr) ** 2).mean(1)) + 1e-9); loud = np.where(db > db.max() - 24)[0]
    if len(loud):
        e = min(len(x), (loud[-1] + 1) * fr + int(0.06 * sr)); x = x[:e].copy(); m = min(len(x) // 4, int(0.04 * sr))
        if m > 0: x[-m:] *= np.linspace(1, 0, m) ** 1.5
    with wave.open(path, 'wb') as f: f.setnchannels(ch); f.setsampwidth(2); f.setframerate(sr); f.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())


subprocess.run([PIPER, '--model', MODEL, '--length_scale', '0.97', '--noise_scale', '0.72', '--noise_w', '0.9', '--output_file', f'{tmp}/a.wav'], input=a.spoken.encode(), check=True, capture_output=True); clean_ah(f'{tmp}/a.wav')
ta = probe(f'{tmp}/a.wav'); LEAD = 0.15; dur = LEAD + ta + 0.7
run('ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/a.wav', '-af', f'adelay={int(LEAD * 1000)}|{int(LEAD * 1000)},apad', '-t', f'{dur:.3f}', f'{tmp}/v0.wav')
run('ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/v0.wav', '-af', 'highpass=f=75,lowshelf=g=2.5:f=170,equalizer=f=380:t=q:w=1.1:g=-2.5,equalizer=f=3300:t=q:w=1.0:g=3,highshelf=g=2:f=9000,deesser=i=0.35,acompressor=threshold=-20dB:ratio=3:attack=6:release=120:makeup=3dB,alimiter=limit=0.89', f'{tmp}/voice.wav')

# the one soft chime when the ask lands
SFX = os.environ.get('SFX_DIR', os.path.expanduser('~/faceless-shorts/kit/sfx'))
if os.path.exists(f'{SFX}/chime_1.wav'):
    def rd(f):
        b = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-f', 'f32le', '-ac', '2', '-ar', '48000', '-'], capture_output=True, check=True).stdout
        return np.frombuffer(b, dtype=np.float32).reshape(-1, 2).astype(np.float64)
    v = rd(f'{tmp}/voice.wav'); vr = np.sqrt(np.mean(v[np.abs(v).max(1) > 0.01] ** 2) + 1e-12)
    c = rd(f'{SFX}/chime_1.wav'); c *= vr * 10 ** (-9 / 20) / (np.sqrt(np.mean(c ** 2)) + 1e-12); c = np.clip(c, -0.5, 0.5)
    i = int((LEAD + 0.45) * 48000); k = min(len(c), len(v) - i)
    if k > 0: v[i:i + k] += c[:k]
    v *= min(1.0, 0.89 / (np.abs(v).max() + 1e-9))
    with wave.open(f'{tmp}/voice.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000); w.writeframes((v * 32767).astype('<i2').tobytes())


def eob(t):
    t = max(0.0, min(1.0, t)); c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def seg(t, x, y): return max(0.0, min(1.0, (t - x) / (y - x)))
def text_layer(txt, size, fill, stroke=10, font=FONT, maxw=980):
    while True:
        f = ImageFont.truetype(font, size); box = f.getbbox(txt, stroke_width=stroke)
        if box[2] - box[0] <= maxw or size < 40: break
        size -= 4
    im = Image.new('RGBA', (box[2] - box[0] + 20, box[3] - box[1] + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - box[0], 10 - box[1]), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=(17, 17, 17)); return im
def pill_layer(txt, size, fg, bg_, maxw=980):
    while True:
        f = ImageFont.truetype(FONT, size); box = f.getbbox(txt); w, h = box[2] - box[0] + size * 1.2, size * 1.7
        if w <= maxw or size < 40: break
        size -= 4
    im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h / 2, fill=bg_); d.text((w / 2, h / 2), txt, font=f, fill=fg, anchor='mm'); return im
def paste(base, layer, cx, cy, sc):
    if sc <= 0.01: return
    l = layer.resize((max(1, int(layer.width * sc)), max(1, int(layer.height * sc))), Image.LANCZOS); base.alpha_composite(l, (int(cx - l.width / 2), int(cy - l.height / 2)))


vd = probe(a.src); run('ffmpeg', '-v', 'error', '-y', '-ss', str(max(0, vd - 0.1)), '-i', a.src, '-frames:v', '1', f'{tmp}/last.png')
bg = Image.open(f'{tmp}/last.png').convert('RGB').resize((W, H)).filter(ImageFilter.GaussianBlur(28)); bg = Image.blend(bg, Image.new('RGB', (W, H), (6, 9, 16)), 0.65)
layers = [pill_layer(t, 104, (17, 17, 17), (255, 212, 59)) if i + 1 == a.pill else text_layer(t, 100, (255, 255, 255)) for i, t in enumerate(a.lines)]
handle = text_layer('@deva_invests', 46, (220, 228, 238), 6, FONT2)
gap = 40; tot = sum(l.height for l in layers) + gap * (len(layers) - 1); y = 820 - tot / 2; ys = []
for l in layers: ys.append(y + l.height / 2); y += l.height + gap
for i in range(int(dur * FPS)):
    t = i / FPS; f = bg.convert('RGBA')
    for k, (l, cy) in enumerate(zip(layers, ys)):
        s = eob(seg(t, 0.05 + 0.15 * k, 0.35 + 0.15 * k))
        if k + 1 == a.pill and t > 0.9: s *= 1 + 0.035 * math.sin((t - 0.9) * 8)
        paste(f, l, 540, cy, s)
    paste(f, handle, 540, 1330, eob(seg(t, 0.6, 0.9)))
    f.convert('RGB').save(f'{tmp}/c{i:04d}.jpg', quality=92)
run('ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{tmp}/c%04d.jpg', '-i', f'{tmp}/voice.wav', '-t', f'{dur:.3f}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', f'{tmp}/card.mp4')
run('ffmpeg', '-v', 'error', '-y', '-i', a.src, '-i', f'{tmp}/card.mp4', '-filter_complex',
    "[0:v]fps=24,setsar=1[v0];[0:a]aresample=44100,aformat=channel_layouts=stereo[a0];[1:v]setsar=1[v1];[1:a]aresample=44100,aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]",
    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', a.out)
print(a.out, f'{probe(a.out):.1f}s')
