#!/bin/bash
# fx4 take D (LAB-fx4 section 3.D): Firefox on the python-sdk v2.0.0 release page, the old plug's PyPI JSON, the 0.1.28 project page.
#   tools/run_fx4.sh d lab/fx4_D.sh
set -u
. /lab/lab/common.sh
X=/lab/out/fx4; O=$X/D; mkdir -p "$O" /tmp/ffp
cp /lab/lab/firefox-user.js /tmp/ffp/user.js
echo 'user_pref("devtools.jsonview.enabled", true);' >> /tmp/ffp/user.js
sl_display $W $H
firefox --no-remote -profile /tmp/ffp about:blank > "$O/firefox.log" 2>&1 &
w=$(sl_wait_window "Mozilla Firefox" 90); sleep 4
wmctrl -i -r "$w" -b add,maximized_vert,maximized_horz; sleep 2
xdotool mousemove 1440 900
go() { xdotool key ctrl+l; sleep 0.5; sl_type "$1" "" 60; sl_key Return "${2:-go}"; }
sl_record "$O"; sl_mark "recording started: Firefox"; sl_nap 1
go "github.com/modelcontextprotocol/python-sdk/releases/tag/v2.0.0" "typed: release page"
sl_nap 9; sl_mark "firefox: release v2.0.0 opened"
SL_SHOT_WAKE=0 sl_shot "$O/s-release-top.png"
for i in 1 2 3; do xdotool key ctrl+minus; sleep 0.4; done; sleep 1; xdotool key ctrl+Home; sleep 1
xdotool key ctrl+f; sleep 0.6; xdotool type --delay 60 "FastMCP is now"; xdotool key Return; sleep 1.5; xdotool key Escape; sleep 1.5
SL_SHOT_WAKE=0 sl_shot "$O/release-v2.0.0.png"
sl_nap 28
go "pypi.org/pypi/freecad-mcp/0.1.19/json" "typed: pypi json"
sl_nap 6; sl_mark "firefox: pypi 0.1.19 json opened"
SL_SHOT_WAKE=0 sl_shot "$O/s-json-first.png"
sl_click 554 271 "JSON filter box"; sl_type "mcp[cli]" "typed: filter mcp" 80; sl_nap 3
SL_SHOT_WAKE=0 sl_shot "$O/pypi-0.1.19-json.png"; sl_mark "json: requires_dist shown"
sl_nap 8
xdotool key ctrl+a; sl_type "2026-07-05" "typed: filter upload_time" 80; sl_nap 3
SL_SHOT_WAKE=0 sl_shot "$O/pypi-0.1.19-json-upload.png"; sl_mark "json: upload_time shown"
sl_nap 6
go "pypi.org/project/freecad-mcp/0.1.28/" "typed: pypi project page"
sl_nap 7; sl_mark "firefox: pypi 0.1.28"
SL_SHOT_WAKE=0 sl_shot "$O/pypi-0.1.28.png"
sl_nap 4
for i in 1 2 3; do xdotool key ctrl+minus; sleep 0.4; done
xdotool key ctrl+f; sleep 0.6; xdotool type --delay 60 "Requires: Python"; xdotool key Return; sleep 1.5; xdotool key Escape; sleep 1.5
sl_mark "firefox: pypi 0.1.28 Requires Python"
SL_SHOT_WAKE=0 sl_shot "$O/pypi-0.1.28-requires.png"
sl_nap 10
sl_mark "recording stopped"; sl_stop
python3 - "$O" <<'PY'
import json, os, sys
d = sys.argv[1]
rows = [json.loads(l) for l in open(os.path.join(d, 'events.jsonl')) if l.strip()]
open(os.path.join(d, 'events.tsv'), 'w').write(''.join('%s\t%.2f\n' % (r['event'], r['t']) for r in rows))
PY
curl -s https://pypi.org/pypi/freecad-mcp/0.1.19/json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['info']['requires_dist']); print([u['upload_time'] for u in d['urls']])" | tee "$O/pypi-0.1.19-json.txt"
pkill firefox; sl_display_stop
echo "D done"
