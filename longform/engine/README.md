# deva invests long-form engine (from video 1, Danske Bank, 23:19, Nov 12 2026)

Pure Python: PIL + numpy draw every frame, ffmpeg encodes, scipy synthesizes the original music and SFX, Piper reads the narration. No paid tools, no stock footage, no samples.

## Layout (keep these exact paths; finalize.py and tts_piper.py assume them)
/tmp/ytw/narration_sections.json   10 sections: [{"section": "Hook", "text": "..."}, ...]  (only "text" is read)
/tmp/ytw/tts_piper.py              -> /tmp/ytw/vo/01.wav ... 10.wav
/tmp/ytw/engine/engine.py          primitives: text, rect, line, arrow, dot, label_box, counter, stamp, paper, ptext, fake_lines, source, recreation, kenburns; colours BG INK MUTED DIM RED GOLD TEAL PAPER
/tmp/ytw/engine/scenes.py          = scenes_base.py + this video's own scenes (write new ones; aim for ~50 scene types / ~90 beats over 23 min)
/tmp/ytw/engine/beats.py           the beat sheet (see beats_example.py)
/tmp/ytw/engine/render.py          timeline + per-frame renderer + encoder
/tmp/ytw/engine/audio.py           music.wav + sfx.wav from the timeline
/tmp/ytw/engine/finalize.py        durations -> audio -> 10 segments (2 in parallel) -> concat -> mix -> /tmp/ytw/deliver/final_video.mp4
/tmp/ytw/engine/thumbs.py          thumbnail helpers

## How timing works
beats.py lists, per narration section, (anchor phrase, scene name, kwargs). A beat starts when its anchor phrase is spoken: render.py maps character positions in the section text to time (punctuation adds pause weight) scaled to the real WAV length (durations.json, written by finalize.py). Inside a scene, c.at("phrase") returns the local time a phrase is spoken, so elements can appear on the word. GAPS = silence before each section (chapter cards play there), CHAPTERS = {section_index: (number, "TITLE")}, TAIL = 16 s end screen after the last word. Every anchor must appear verbatim in that section's text or render.py stops with "anchor not found".

## Commands
1. python3 /tmp/ytw/tts_piper.py                     (all 10; or pass section numbers to redo some)
2. cd /tmp/ytw/engine && python3 render.py timeline  (check beats and total length)
3. python3 render.py frames /tmp/ytw/qc 20 95 300 ...  then LOOK at the JPGs (busy moments, every new scene type). Fix empty openings: an element should be visible within ~0.4 s of a beat starting (use min(0.35, _at(...)) for the first element).
4. python3 finalize.py   (about an hour for 23 min on 2 workers; use --only 3,5 to re-render chosen sections, then run it again for the mix)
5. Upload encode (<= 90 MB for GitHub), 2-pass:
   D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/ytw/deliver/final_video.mp4)
   VB=$(python3 -c "print(int(90e6*8/$D) - 140000)")
   ffmpeg -y -i final_video.mp4 -c:v libx264 -preset veryfast -tune animation -b:v $VB -pass 1 -an -f mp4 /dev/null
   ffmpeg -y -i final_video.mp4 -c:v libx264 -preset veryfast -tune animation -b:v $VB -pass 2 -c:a aac -b:a 128k -movflags +faststart upload.mp4
   (tested Nov 12: ~400 kbps video looks clean for this style.)
6. QC: ffprobe; `ffmpeg -v error -i upload.mp4 -f null -` must print nothing; loudness: `ffmpeg -i upload.mp4 -af ebur128 -f null -` about -16 LUFS; look at 8+ frames.

## Style rules that made video 1 work
- Dark navy gradient + faint grid + light grain; Inter Display Black for big words; red = danger/the key number, gold = labels, teal = "normal" comparisons.
- A new visual every 6-12 s; numbers count up on the word they are spoken; every on-screen figure has a small "Source: ..." line.
- Any document, letter, filing or email shown is a RECREATION and labelled so (recreation()). Never fake a headline, quote or record.
- No real logos, no real people's faces, no copyrighted footage or music. Synthesized music only (audio.py).
- Music sits under the voice (0.30), SFX at 0.55, narration normalised to -16 LUFS. No whooshes louder than the voice.
- Voice: Piper LibriTTS-high speaker 720 (CC BY 4.0, credit it in the description). Never the ryan voices (non-commercial).
