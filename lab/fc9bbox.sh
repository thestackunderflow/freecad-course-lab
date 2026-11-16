#!/bin/sh
# fc9: where the plan name sits (full-size pixels) in a recording's frame at T s, or in a PNG: tesseract word boxes.
#   docker run --rm -v "<lab>:/lab" fc8-ocr:1 sh /lab/lab/fc9bbox.sh FILE [T]
f=$1; t=${2:-0}; d=$(mktemp -d)
case $f in *.mp4) ffmpeg -v error -ss $t -i "$f" -frames:v 1 "$d/x.png";; *) cp "$f" "$d/x.png";; esac
tesseract "$d/x.png" - tsv 2>/dev/null | awk -F'\t' 'tolower($12) ~ /ultra|sonnet|claude/ {print $12, "x="$7, "y="$8, "w="$9, "h="$10}'
rm -rf "$d"
