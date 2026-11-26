"""Narration with Piper (LibriTTS high, speaker 720, CC BY 4.0). Reads /tmp/ytw/narration_sections.json -> /tmp/ytw/vo/01.wav ... 10.wav.
Extend REP with this video's acronyms, names and dates (spell them the way they should be SPOKEN).
Usage: python3 tts_piper.py [section numbers to redo, e.g. 2 5]"""
import json, subprocess, os, sys, re
S = json.load(open("/tmp/ytw/narration_sections.json"))
REP = [("In the US,", "In the U.S.,"), ("In the US", "In the U.S."), ("US dollars", "U.S. dollars"), ("US banks", "U.S. banks"),
       ("CEO", "C E O"), ("CFO", "C F O"), ("IT systems", "I T systems"), ("the EU,", "the E U,"), ("AI", "A I"), ("GPU", "G P U"),
       ("1990s", "nineteen-nineties"), ("2000s", "two-thousands"), (" — ", ", "), ("UK", "U.K."), ("UN ", "U.N. "),
       ("%", " percent"), ("Beignet", "Ben-yay"), ("Sopaipilla", "Soapa-peeya")]
RX = [(r"\bGE\b", "G E"), (r"\bFDIC\b", "F D I C"), (r"\bSEC\b", "S E C"), (r"\bIOUs\b", "I O U's"), (r"\bIOU\b", "I O U"), (r"\bHealthCare\b", "Health Care")]
LS = {2: "1.20"}          # section 2 (the intro) is read a little slower
ONLY = {int(x) for x in sys.argv[1:]} or set(range(1, len(S) + 1))
os.makedirs("/tmp/ytw/vo", exist_ok=True)
for i, s in enumerate(S, 1):
    if i not in ONLY: continue
    t = s["text"]
    for a, b in REP: t = t.replace(a, b)
    for a, b in RX: t = re.sub(a, b, t)
    out = f"/tmp/ytw/vo/{i:02d}.wav"
    r = subprocess.run(["/opt/piperx/piper/piper", "--model", "/opt/piperx/lt/en-us-libritts-high.onnx", "--speaker", "720",
                        "--length_scale", LS.get(i, "1.12"), "--sentence_silence", "0.42", "--output_file", out], input=t.encode(), capture_output=True)
    print(i, r.returncode, r.stderr.decode()[-300:] if r.returncode else "", flush=True)
