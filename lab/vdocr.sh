#!/bin/sh
# video D probes: OCR every 2 s of each recording and every still under DIR for an account detail, before the commit.
#   MSYS_NO_PATHCONV=1 docker run --rm --network none -v "<lab>:/lab" fc8-ocr:1 sh /lab/lab/vdocr.sh /lab/out/... -> DIR/OCR.txt
D=$1; OUT=$D/OCR.txt; : > $OUT
PAT="ultra|@gmail|sk-ant"
for v in $(find $D -name screen.mp4 | sort); do
  t=$(mktemp -d); ffmpeg -v error -i "$v" -vf "fps=1/2,scale=1440:-1" "$t/f%04d.png"
  n=0; hits=0
  for f in "$t"/f*.png; do n=$((n + 1)); x=$(tesseract "$f" - 2>/dev/null | grep -i -E "$PAT")
    [ -n "$x" ] && { hits=$((hits + 1)); echo "$v t=$(( (n - 1) * 2 ))s: $x" >> $OUT; }; done
  echo "SCANNED $v frames=$n hits=$hits" >> $OUT; rm -rf "$t"
done
n=0; hits=0
for f in $(find $D -name "*.png" | sort); do n=$((n + 1)); x=$(tesseract "$f" - 2>/dev/null | grep -i -E "$PAT")
  [ -n "$x" ] && { hits=$((hits + 1)); echo "$f: $x" >> $OUT; }; done
echo "SCANNED stills=$n hits=$hits" >> $OUT
grep SCANNED $OUT | sed 's#/lab/##'
