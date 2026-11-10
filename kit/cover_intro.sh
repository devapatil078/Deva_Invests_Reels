#!/bin/sh
# Put the reel's cover on screen for the first 0.8 s (fading into the video over the last 0.25 s). Audio is untouched,
# so the voice and captions keep their timing.   usage: sh cover_intro.sh <in.mp4> <cover.jpg> <out.mp4>
set -e
ffmpeg -v error -y -i "$1" -loop 1 -t 0.8 -framerate 30 -i "$2" -filter_complex \
  "[1:v]scale=1080:1920,format=yuva420p,fade=t=out:st=0.55:d=0.25:alpha=1[c];[0:v][c]overlay=0:0:eof_action=pass:enable='lte(t,0.8)'[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a copy -movflags +faststart "$3"
echo "$3"
