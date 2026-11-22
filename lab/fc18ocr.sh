#!/bin/sh
# fc18: OCR every 2 s of each recording under out/fc18 (GUI takes + Claude runs), and every run still, for a plan name,
# a connector name or an email / key, before the commit (lab/fc14ocr.sh pattern, email regex added).
#   MSYS_NO_PATHCONV=1 docker run --rm --network none -v "<lab>:/lab" fc8-ocr:1 sh /lab/lab/fc18ocr.sh  -> out/fc18/OCR-scan.txt
#   one take only: ... sh /lab/lab/fc18ocr.sh /lab/out/fc18/C  -> out/fc18/C/OCR-scan.txt (no run stills)
R=${1:-/lab/out/fc18}; OUT=$R/OCR-scan.txt; : > $OUT
PAT="claude_ai_|google drive|claude docs|drivemcp|ultra|max plan|pro plan|claude max|claude pro|team plan|enterprise|figma|datum|handoff|sk[-]ant|api key|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}"
for v in $(find $R -name screen.mp4 | sort); do
  d=$(mktemp -d)
  ffmpeg -v error -i "$v" -vf "fps=1/2,scale=1440:-1" "$d/f%04d.png"
  n=0; hits=0
  for f in "$d"/f*.png; do
    n=$((n + 1))
    t=$(tesseract "$f" - 2>/dev/null | grep -i -E "$PAT")
    if [ -n "$t" ]; then hits=$((hits + 1)); echo "$v t=$(( (n - 1) * 2 ))s: $t" >> $OUT; fi
  done
  echo "SCANNED $v frames=$n hits=$hits" >> $OUT
  rm -rf "$d"
done
n=0; hits=0
for f in $(find $R/runs -name "*.png" 2>/dev/null | sort); do
  n=$((n + 1))
  t=$(tesseract "$f" - 2>/dev/null | grep -i -E "$PAT")
  if [ -n "$t" ]; then hits=$((hits + 1)); echo "$f: $t" >> $OUT; fi
done
echo "SCANNED run stills=$n hits=$hits" >> $OUT
grep SCANNED $OUT
