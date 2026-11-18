#!/bin/sh
# fc12: OCR every 2 s of each recording under out/fc10 for a plan name (Claude Code's header), before the commit.
#   MSYS_NO_PATHCONV=1 docker run --rm -v "<lab>:/lab" fc8-ocr:1 sh /lab/lab/fc12ocr.sh  -> out/fc12/OCR-runs.txt
OUT=/lab/out/fc12/OCR-runs.txt; : > $OUT
for v in $(find /lab/out/fc12 -name screen.mp4 | sort); do
  d=$(mktemp -d)
  ffmpeg -v error -i "$v" -vf "fps=1/2,scale=1440:-1" "$d/f%04d.png"
  n=0; hits=0
  for f in "$d"/f*.png; do
    n=$((n + 1))
    t=$(tesseract "$f" - 2>/dev/null | grep -i -E "claude_ai_|google drive|claude docs|drivemcp|ultra|max plan|pro plan|claude max|claude pro|team plan|enterprise|sk[-]ant|@gm[a]il|api key")
    if [ -n "$t" ]; then hits=$((hits + 1)); echo "$v t=$(( (n - 1) * 2 ))s: $t" >> $OUT; fi
  done
  echo "SCANNED $v frames=$n hits=$hits" >> $OUT
  rm -rf "$d"
done
cat $OUT | grep SCANNED
