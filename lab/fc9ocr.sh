#!/bin/sh
# fc9: OCR every 2 s of each recording under out/fc9 for a plan name (Claude Code's header), before the commit.
#   MSYS_NO_PATHCONV=1 docker run --rm -v "<lab>:/lab" fc8-ocr:1 sh /lab/lab/fc9ocr.sh  -> out/fc9/OCR-plan.txt
OUT=/lab/out/fc9/OCR-plan.txt; : > $OUT
for v in $(find /lab/out/fc9 -name screen.mp4 | sort); do
  d=$(mktemp -d)
  ffmpeg -v error -i "$v" -vf "fps=1/2,scale=1440:-1" "$d/f%04d.png"
  n=0; hits=0
  for f in "$d"/f*.png; do
    n=$((n + 1))
    t=$(tesseract "$f" - 2>/dev/null | grep -i -E "ultra|max plan|pro plan|claude max|claude pro|team plan|enterprise")
    if [ -n "$t" ]; then hits=$((hits + 1)); echo "$v t=$(( (n - 1) * 2 ))s: $t" >> $OUT; fi
  done
  echo "SCANNED $v frames=$n hits=$hits" >> $OUT
  rm -rf "$d"
done
cat $OUT | grep SCANNED
