"""Apply the Nov 11 owner-requested fixes to the kit copies from the repo (idempotent; run after copying the repo's
kit/ into /root/faceless-shorts/kit/):   python3 apply_kit_patches.py /root/faceless-shorts/kit
  1. Essential sounds only (owner, Nov 11: no whoosh, no pops (they sounded like 'ah'), 'no unnecessary sounds, just essentials, very professional'): mix_sfx.py plays no music bed and keeps only ONE impact (the big reveal) and at most ONE chime; series_end_sfx.py keeps only one soft chime when the ask lands.
  2. series_end_sfx.py: cut the short "ah" Piper adds after a phrase (owner, Nov 11); SPOKEN_FULL env = the whole spoken tease; NUM up to twenty; yt ending says LINK IN THE DESCRIPTION.
"""
import sys
from pathlib import Path

CLEAN = """def _clean_ah(path):
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
"""
K = Path(sys.argv[1] if len(sys.argv) > 1 else '/root/faceless-shorts/kit')

def patch(f, pairs):
    p = K / f; s = p.read_text(); n = 0
    for a, b in pairs:
        if (b and b in s) or (not b and a not in s): continue
        if a not in s: print(f'{f}: pattern not found (skipped): {a[:60]!r}'); continue
        s = s.replace(a, b); n += 1
    p.write_text(s); print(f'{f}: {n} change(s)')

patch('mix_sfx.py', [
    ("cj = json.loads((P / 'data/cues.json').read_text())",
     "cj = json.loads((P / 'data/cues.json').read_text())\ncj['cues'] = [c for c in cj['cues'] if c.get('type') not in ('whoosh', 'slide', 'zip')]   # owner, Nov 11: no whoosh sounds"),
    ("cj['cues'] = [c for c in cj['cues'] if c.get('type') not in ('whoosh', 'slide', 'zip')]   # owner, Nov 11: no whoosh sounds",
     "cj['cues'] = [c for c in cj['cues'] if c.get('type') not in ('whoosh', 'slide', 'zip')]   # owner, Nov 11: no whoosh sounds\n"
     "cj['cues'] = [dict(c, type='click', gain=round(0.45 * float(c.get('gain', 1.0)), 3)) if c.get('type') in ('pop', 'plop', 'boing', 'gulp') else c for c in cj['cues']]   # owner, Nov 11: no 'ah' sounds (the pitched pop sounded like a voice), so pops play as soft clicks"),
    ("cj['cues'] = [dict(c, type='click', gain=round(0.45 * float(c.get('gain', 1.0)), 3)) if c.get('type') in ('pop', 'plop', 'boing', 'gulp') else c for c in cj['cues']]   # owner, Nov 11: no 'ah' sounds (the pitched pop sounded like a voice), so pops play as soft clicks",
     "cj['cues'] = [dict(c, type='click', gain=round(0.45 * float(c.get('gain', 1.0)), 3)) if c.get('type') in ('pop', 'plop', 'boing', 'gulp') else c for c in cj['cues']]   # owner, Nov 11: no 'ah' sounds (the pitched pop sounded like a voice), so pops play as soft clicks\n"
     "_ess, _seen = [], set()   # owner, Nov 11: 'no unnecessary sounds, just essentials, very professional': keep ONE impact (the big reveal) and at most ONE chime; drop every other effect\n"
     "for _c in sorted(cj['cues'], key=lambda c: c['t']):\n"
     "    _k = {'impact': 'impact', 'thud': 'impact', 'slam': 'impact', 'chime': 'chime', 'sparkle': 'chime'}.get(_c.get('type'))\n"
     "    if _k and _k not in _seen: _seen.add(_k); _ess.append(dict(_c, gain=round(0.8 * float(_c.get('gain', 1.0)), 3)))\n"
     "cj['cues'] = _ess"),
    ("mus = script.get('music', 'bed')", "mus = 'none'   # owner, Nov 11: essentials only; the music bed's plucked notes sounded like 'uh uh', so no music"),
])
patch('series_end_sfx.py', [
    ("NUM = {2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight'}",
     "NUM = {2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty'}"),
    ("say(f\"Part {NUM[part + 1]}: {spoken}?\", f'{tmp}/a.wav')",
     "say(os.environ.get(\"SPOKEN_FULL\") or f\"Part {NUM[part + 1]}: {spoken}?\", f'{tmp}/a.wav')"),
    ("from the pinned comment.\"", "from the description.\""),
    ("('whoosh_2', 0.0, -2), ", ""),
    ("('pop_1', 0.05, -6), ('pop_3', 0.32, -6), ('pop_2', ASK - 0.12, -7), ('click_1', ASK + 0.22, -5), ('chime_1', ASK + 0.5, -4)", "('chime_1', ASK + 0.5, -9)"),
    ("('click_2', 0.05, -10), ('click_3', 0.32, -10), ('click_2', ASK - 0.12, -11), ('click_1', ASK + 0.22, -5), ('chime_1', ASK + 0.5, -4)", "('chime_1', ASK + 0.5, -9)"),
    ("def say(text, path): subprocess.run([PIPER, '--model', MODEL, '--length_scale', '0.97', '--noise_scale', '0.72', '--noise_w', '0.9', '--output_file', path], input=text.encode(), check=True, capture_output=True)",
     CLEAN + "def say(text, path): subprocess.run([PIPER, '--model', MODEL, '--length_scale', '0.97', '--noise_scale', '0.72', '--noise_w', '0.9', '--output_file', path], input=text.encode(), check=True, capture_output=True); _clean_ah(path)"),
    ("L.update(a1=text_layer('GET IT IN THE', 76, (255, 255, 255)), a2=pill_layer('PINNED COMMENT', 84, (17, 17, 17), (255, 212, 59)), a3=text_layer('free spreadsheet, no catch', 48, (220, 228, 238), 6, FONT2))",
     "L.update(a1=text_layer('LINK IN THE', 76, (255, 255, 255)), a2=pill_layer('DESCRIPTION', 84, (17, 17, 17), (255, 212, 59)), a3=text_layer('7 free tools, no catch', 48, (220, 228, 238), 6, FONT2))"),
])
