"""One-command final build once the 10 narration files are in vo/01.wav ... vo/10.wav (relative to /tmp/ytw).
python3 finalize.py   ->  deliver/final_video.mp4   (then re-encode to <= 90 MB for upload, see README)"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
W = "/tmp/ytw"; E = os.path.join(W, "engine")

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())

vo = [os.path.join(W, "vo", f"{i:02d}.wav") for i in range(1, 11)]
missing = [p for p in vo if not os.path.exists(p)]
if missing: sys.exit(f"missing narration: {missing}")
json.dump([dur(p) for p in vo], open(os.path.join(W, "durations.json"), "w"))
subprocess.check_call([sys.executable, "audio.py", os.path.join(W, "audio")], cwd=E)
sys.path.insert(0, E); import render as R
tl = R.Timeline()
os.makedirs(os.path.join(W, "seg"), exist_ok=True)
os.makedirs(os.path.join(W, "deliver"), exist_ok=True)
segs = [os.path.join(W, "seg", f"s{i:02d}.mp4") for i in range(10)]
ONLY = [int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")] if "--only" in sys.argv else list(range(10))
def run(i): subprocess.check_call([sys.executable, "render.py", "segment", str(i), segs[i]], cwd=E)
with ThreadPoolExecutor(3) as ex: list(ex.map(run, ONLY))
lst = os.path.join(W, "seg", "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
silent = os.path.join(W, "seg", "video.mp4")
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent])
# narration bus: each section placed at its start time
inputs, filt = [], []
for i, p in enumerate(vo):
    inputs += ["-i", p]; ms = int(tl.narr[i][0] * 1000)
    filt.append(f"[{i + 1}:a]aresample=44100,adelay={ms}|{ms}[v{i}]")
filt.append("".join(f"[v{i}]" for i in range(10)) + "amix=inputs=10:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[vo]")
filt.append(f"[11:a]volume=0.30[m];[12:a]volume=0.55[s]")
filt.append("[vo][m][s]amix=inputs=3:normalize=0,alimiter=limit=0.95[a]")
out = os.path.join(W, "deliver", "final_video.mp4")
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", silent] + inputs +
                      ["-i", os.path.join(W, "audio", "music.wav"), "-i", os.path.join(W, "audio", "sfx.wav"),
                       "-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                       "-shortest", "-movflags", "+faststart", out])
print("done", out, round(tl.total / 60, 2), "min")
