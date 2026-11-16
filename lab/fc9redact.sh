#!/bin/sh
# fc9: cover the plan name in Claude Code's header (x 600-910, y 118-170 at 2880x1800, found by lab/fc9bbox.sh) with
# "Claude [plan]" in every run recording and still; the originals are replaced (they are never kept).
#   docker run --rm -v "<lab>:/lab" fc8-ocr:1 sh /lab/lab/fc9redact.sh
FONT=$(fc-list : file 2>/dev/null | grep -i -m1 -E "DejaVuSansMono|Mono" | cut -d: -f1)
VF="drawbox=x=600:y=118:w=320:h=52:color=black@1:t=fill,drawtext=fontfile=$FONT:text='Claude [plan]':x=606:y=126:fontsize=34:fontcolor=0xb0b0b0"
for r in /lab/out/fc9/runs/*; do
  v=$r/screen.mp4
  if [ -e "$v" ]; then
    ffmpeg -v error -y -i "$v" -vf "$VF" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -an "$r/screen.red.mp4" \
      && mv "$r/screen.red.mp4" "$v" && echo "redacted $v"
  fi
  for p in "$r"/*.png; do
    ffmpeg -v error -y -i "$p" -vf "$VF" "$p.red.png" && mv "$p.red.png" "$p"
  done
done
