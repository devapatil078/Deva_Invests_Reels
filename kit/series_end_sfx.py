"""Turn a finished Short into a numbered series episode:
  - a 'PART n' badge in the first 2.6 s
  - an end card: NEXT · PART n+1 teaser, then the free Deal Checker ask (ig: comment LINK, yt: pinned comment)
usage: python3 series_end.py <in.mp4> <out.mp4> <ig|yt> <part> "<next line 1>" "<next line 2>" "<spoken next question>" "<tool name>" <KEYWORD>
"""
import sys, subprocess, os, tempfile, math, wave
from PIL import Image, ImageDraw, ImageFilter, ImageFont

src, out, mode, part, n1, n2, spoken, tool, kw = sys.argv[1:10]; part = int(part); SERIES = os.environ.get("SERIES", "FLIPPING SERIES")
FONT = os.path.expanduser('~/faceless-shorts/bank-money/fonts/Inter-Black.otf'); FONT2 = os.path.expanduser('~/faceless-shorts/bank-money/fonts/Inter-ExtraBold.otf')
PIPER, MODEL = '/home/claude/piper/piper/piper', '/home/claude/piper/voices/en-us-ryan-high.onnx'
W, H, FPS = 1080, 1920, 24
NUM = {2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty'}
tmp = tempfile.mkdtemp()
run = lambda *a: subprocess.run(list(a), check=True, capture_output=True)
probe = lambda f: float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).decode())

# ── voice: teaser, then the ask (two clips so we know exactly when the ask starts)
def _clean_ah(path):
    # owner, Nov 11: no 'ah' sounds. Piper adds a short breathy voiced blip after the last word; cut it.
    import numpy as _np, wave as _w
    with _w.open(path) as f: sr = f.getframerate(); ch = f.getnchannels(); x = _np.frombuffer(f.readframes(f.getnframes()), _np.int16).astype(float) / 32768
    fr = int(0.01 * sr); n = len(x) // fr
    on = 20 * _np.log10(_np.sqrt((x[:n * fr].reshape(n, fr) ** 2).mean(1)) + 1e-9) > -42; r = []; i = 0
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]: j += 1
            r.append((i * fr, j * fr)); i = j
        else: i += 1
    for _ in range(2):
        if len(r) < 2: break
        a, b = r[-1]; seg = x[a:b]; zcr = _np.mean(_np.abs(_np.diff(_np.sign(seg)))) / 2 * sr if len(seg) > 2 else 0
        if (b - a) / sr < 0.22 and (a - r[-2][1]) / sr >= 0.02 and zcr < 1800: x = x[:r[-2][1] + int(0.03 * sr)]; r = r[:-1]
        else: break
    db = 20 * _np.log10(_np.sqrt((x[:(len(x) // fr) * fr].reshape(-1, fr) ** 2).mean(1)) + 1e-9); loud = _np.where(db > db.max() - 24)[0]
    if len(loud):   # trim the dragged last sound (heard as 'uh'): keep 60 ms after the last loud frame, then fade
        e = min(len(x), (loud[-1] + 1) * fr + int(0.06 * sr)); x = x[:e].copy(); m = min(len(x) // 4, int(0.04 * sr))
        if m > 0: x[-m:] *= _np.linspace(1, 0, m) ** 1.5
    with _w.open(path, 'wb') as f: f.setnchannels(ch); f.setsampwidth(2); f.setframerate(sr); f.writeframes((_np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())
def say(text, path): subprocess.run([PIPER, '--model', MODEL, '--length_scale', '0.97', '--noise_scale', '0.72', '--noise_w', '0.9', '--output_file', path], input=text.encode(), check=True, capture_output=True); _clean_ah(path)
say(os.environ.get("SPOKEN_FULL") or f"Part {NUM[part + 1]}: {spoken}?", f'{tmp}/a.wav')   # "follow" stays on screen only: a shorter end card keeps completion rate up
say(f"And comment {kw} for my free {tool.lower()}." if mode == 'ig' else f"And grab my free {tool.lower()} from the description.", f'{tmp}/b.wav')
ta = probe(f'{tmp}/a.wav'); tb = probe(f'{tmp}/b.wav'); GAP = 0.25; ASK = 0.15 + ta + GAP
run('ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/a.wav', '-i', f'{tmp}/b.wav', '-filter_complex', f'[0]adelay=150|150[x];[1]adelay={int(ASK * 1000)}|{int(ASK * 1000)}[y];[x][y]amix=inputs=2:normalize=0,apad', '-t', f'{ASK + tb + 0.55:.3f}', f'{tmp}/voice.wav')
dur = ASK + tb + 0.55
# same broadcast polish as pro_voice.py, so the end card sounds like the same narrator
run('ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/voice.wav', '-af', 'highpass=f=75,lowshelf=g=2.5:f=170,equalizer=f=380:t=q:w=1.1:g=-2.5,equalizer=f=3300:t=q:w=1.0:g=3,highshelf=g=2:f=9000,deesser=i=0.35,acompressor=threshold=-20dB:ratio=3:attack=6:release=120:makeup=3dB,alimiter=limit=0.89', f'{tmp}/voice_pro.wav')
os.replace(f'{tmp}/voice_pro.wav', f'{tmp}/voice.wav')

# ── end-card sound effects from the kit's sound pack (kit/sfx, made by make_sfx.py); skipped if the pack is missing
SFX = os.environ.get('SFX_DIR', os.path.expanduser('~/faceless-shorts/kit/sfx'))
if os.path.exists(f'{SFX}/chime_1.wav'):
    import numpy as np
    def rd(f):
        b = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-f', 'f32le', '-ac', '2', '-ar', '48000', '-'], capture_output=True, check=True).stdout
        return np.frombuffer(b, dtype=np.float32).reshape(-1, 2).astype(np.float64)
    v = rd(f'{tmp}/voice.wav'); vr = np.sqrt(np.mean(v[np.abs(v).max(1) > 0.01] ** 2) + 1e-12)
    for name, t, lvl in [('chime_1', ASK + 0.5, -9)]:
        x = rd(f'{SFX}/{name}.wav'); x *= vr * 10 ** (lvl / 20) / (np.sqrt(np.mean(x ** 2)) + 1e-12)
        x = np.clip(x, -0.5, 0.5); i = int(max(0, t) * 48000); n = min(len(x), len(v) - i)
        if n > 0: v[i:i + n] += x[:n]
    v *= min(1.0, 0.89 / (np.abs(v).max() + 1e-9))
    with wave.open(f'{tmp}/voice.wav', 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000); w.writeframes((v * 32767).astype('<i2').tobytes())

# ── drawing helpers
def eob(t):
    t = max(0.0, min(1.0, t)); c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def seg(t, a, b): return max(0.0, min(1.0, (t - a) / (b - a)))
def text_layer(txt, size, fill, stroke=10, font=FONT, maxw=980):
    while True:
        f = ImageFont.truetype(font, size); box = f.getbbox(txt, stroke_width=stroke)
        if box[2] - box[0] <= maxw or size < 40: break
        size -= 4
    im = Image.new('RGBA', (box[2] - box[0] + 20, box[3] - box[1] + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - box[0], 10 - box[1]), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=(17, 17, 17)); return im
def pill_layer(txt, size, fg, bg_):
    f = ImageFont.truetype(FONT, size); box = f.getbbox(txt); w, h = box[2] - box[0] + size * 1.2, size * 1.7
    im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h / 2, fill=bg_); d.text((w / 2, h / 2), txt, font=f, fill=fg, anchor='mm'); return im
def paste(base, layer, cx, cy, sc):
    if sc <= 0.01: return
    l = layer.resize((max(1, int(layer.width * sc)), max(1, int(layer.height * sc))), Image.LANCZOS); base.alpha_composite(l, (int(cx - l.width / 2), int(cy - l.height / 2)))

# ── opening badge (overlay PNG for the first seconds)
badge = Image.new('RGBA', (W, H), (0, 0, 0, 0)); b1 = pill_layer(f'PART {part}', 46, (17, 17, 17), (255, 212, 59)); b2 = pill_layer(SERIES, 34, (255, 255, 255), (12, 14, 20, 200))
badge.alpha_composite(b1, (60, 110)); badge.alpha_composite(b2, (60 + b1.width + 16, 110 + (b1.height - b2.height) // 2)); badge.save(f'{tmp}/badge.png')

# ── end card frames
vd = probe(src); run('ffmpeg', '-v', 'error', '-y', '-ss', str(vd - 0.1), '-i', src, '-frames:v', '1', f'{tmp}/last.png')
bg = Image.open(f'{tmp}/last.png').convert('RGB').resize((W, H)).filter(ImageFilter.GaussianBlur(28)); bg = Image.blend(bg, Image.new('RGB', (W, H), (6, 9, 16)), 0.65)
L = dict(next=pill_layer(f'NEXT · PART {part + 1}', 56, (17, 17, 17), (255, 212, 59)), t1=text_layer(n1, 104, (255, 255, 255)), t2=text_layer(n2, 116, (255, 212, 59)),
         fol=text_layer("follow so you don't miss it", 50, (220, 228, 238), 6, FONT2), free=text_layer('FREE ' + tool.upper(), 64, (255, 255, 255), 8))
if mode == 'ig': L.update(a1=text_layer('COMMENT', 92, (255, 255, 255)), a2=pill_layer(kw.upper(), 130, (17, 17, 17), (255, 212, 59)), a3=text_layer("and I'll DM it to you", 48, (220, 228, 238), 6, FONT2))
else: L.update(a1=text_layer('LINK IN THE', 76, (255, 255, 255)), a2=pill_layer('DESCRIPTION', 84, (17, 17, 17), (255, 212, 59)), a3=text_layer('7 free tools, no catch', 48, (220, 228, 238), 6, FONT2))
for i in range(int(dur * FPS)):
    t = i / FPS; f = bg.convert('RGBA')
    paste(f, L['next'], 540, 330, eob(seg(t, 0.0, 0.3))); paste(f, L['t1'], 540, 500, eob(seg(t, 0.15, 0.45))); paste(f, L['t2'], 540, 640, eob(seg(t, 0.3, 0.6)) * (1 + 0.03 * math.sin(t * 6)))
    paste(f, L['fol'], 540, 790, eob(seg(t, ta - 0.9, ta - 0.6)))
    k = seg(t, ASK - 0.15, ASK + 0.1)
    if k > 0:
        d = ImageDraw.Draw(f); d.line([(200, 930), (880, 930)], fill=(255, 255, 255, int(70 * k)), width=3)
    paste(f, L['free'], 540, 1060, eob(seg(t, ASK - 0.15, ASK + 0.15))); paste(f, L['a1'], 540, 1210, eob(seg(t, ASK, ASK + 0.3)))
    paste(f, L['a2'], 540, 1390, eob(seg(t, ASK + 0.2, ASK + 0.5)) * (1 + 0.04 * math.sin((t - ASK) * 9) if t > ASK + 0.6 else eob(seg(t, ASK + 0.2, ASK + 0.5))))
    paste(f, L['a3'], 540, 1575, eob(seg(t, ASK + 0.6, ASK + 0.9)))
    f.convert('RGB').save(f'{tmp}/c{i:04d}.jpg', quality=92)
run('ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{tmp}/c%04d.jpg', '-i', f'{tmp}/voice.wav', '-t', f'{dur:.3f}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', f'{tmp}/card.mp4')
run('ffmpeg', '-v', 'error', '-y', '-i', src, '-loop', '1', '-i', f'{tmp}/badge.png', '-i', f'{tmp}/card.mp4', '-filter_complex',
    "[1:v]format=rgba,fade=t=out:st=2.3:d=0.3:alpha=1[bd];[0:v][bd]overlay=0:0:enable='lt(t,2.6)':shortest=1,fps=24,setsar=1[v0];[0:a]aresample=44100,aformat=channel_layouts=stereo[a0];"
    "[2:v]setsar=1[v1];[2:a]aresample=44100,aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]",
    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out)
print(out, f'{probe(out):.1f}s')
