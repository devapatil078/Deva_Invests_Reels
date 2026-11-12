"""Piper (offline, free) narration for a faceless-shorts project.
script.json -> data/narration.wav + data/lines.json with exact per-line times (one Piper call per line).
usage: python3 piper_voice.py <project> [--model PATH] [--length-scale 1.0]
"""
import argparse, json, subprocess, tempfile, wave
from pathlib import Path
import numpy as np

PIPER = "/home/claude/piper/piper/piper"
ap = argparse.ArgumentParser()
ap.add_argument("project")
ap.add_argument("--model", default="/home/claude/piper/voices/en-us-ryan-high.onnx")
ap.add_argument("--length-scale", type=float, default=1.0, help=">1 slower, <1 faster")
a = ap.parse_args()
P = Path(a.project); S = json.loads((P / "script.json").read_text())

def synth(text):
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        subprocess.run([PIPER, "--model", a.model, "--length_scale", str(a.length_scale), "--sentence_silence", "0.12",
                        "--output_file", f.name], input=text.encode(), check=True, capture_output=True)
        with wave.open(f.name) as w:
            sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    env = np.abs(x) > 0.012                      # trim leading/trailing silence
    idx = np.where(env)[0]
    if len(idx): x = x[max(0, idx[0] - int(0.02 * sr)): idx[-1] + int(0.06 * sr)]
    return sr, x

out, t, lines, SR = [], float(S.get("lead", 0.35)), [], None
for i, ln in enumerate(S["lines"]):
    sr, x = synth(ln["text"]); SR = SR or sr
    if not out: out.append(np.zeros(int(t * sr), np.float32))
    start = t; out.append(x); t += len(x) / sr
    lines.append({"i": i, "text": ln["text"], "start": round(start, 3), "end": round(t, 3)})
    g = float(ln.get("gap", S.get("gap", 0.26))) if i < len(S["lines"]) - 1 else float(S.get("outro", 1.0))
    out.append(np.zeros(int(g * sr), np.float32)); t += g
y = np.concatenate(out); y = y / max(1e-6, np.abs(y).max()) * 0.89
(P / "data").mkdir(exist_ok=True)
with wave.open(str(P / "data/narration.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype(np.int16).tobytes())
(P / "data/lines.json").write_text(json.dumps({"duration": round(len(y) / SR, 3), "voice": "piper:" + Path(a.model).stem,
                                               "lines": lines}, indent=1))
print(f"{P.name}: narration {len(y)/SR:.2f} s, {len(lines)} lines")
