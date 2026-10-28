#!/bin/bash
# Contact sheet of a take: tools/sheet.sh out/l1/install  -> out/l1/install/sheet.png (frames at events)
export MSYS_NO_PATHCONV=1
LAB=$(cd "$(dirname "$0")/.." && (pwd -W 2>/dev/null || pwd))
docker run --rm -v "$LAB:/lab" -w /lab fcc-app:1.1.4-0.1.28 python3 -m screenlab.sheet "/lab/$1/screen.mp4" "/lab/$1/sheet.png" --events "/lab/$1/events.jsonl" "${@:2}"
