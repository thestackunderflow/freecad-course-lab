#!/bin/bash
# Lesson 5, lab L5-Q9 (no AI, free): a fresh FreeCAD 1.1.4 window (same image, the default Maximum mesh deviation) with
# lesson 4's hook open; a Claude run's message-1 tools/call requests replayed in order over the same plug
# (`uvx freecad-mcp@0.1.28`, our own client). Then the replay's ~/hook-claude.stl is measured by checker/mesh5 and
# compared with the run's file: pass = same triangle count, volume within 0.01 mm3, same verdicts (right part, clean).
#   FCC_PREFIX=fc5 tools/run.sh lab/replay5.sh B1
set -u
. /lab/lab/common.sh
RUN=${1:-B1}
R=/lab/out/l5/runs/$RUN
O=/lab/out/l5/replay-$RUN; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 8
cd /lab
cp /lab/out/l4/hand/width30.FCStd ~/hook-lesson4.FCStd
python3 -m lab.opendoc /home/maker/hook-lesson4.FCStd > "$O/opendoc.txt" 2>&1
n=$(awk '$1 == "first" {print $2}' "$R/stages.txt")
sed -n "1,${n}p" "$R/transcript.jsonl" > "$O/transcript-first.jsonl"
python3 -m client.replay "$O/transcript-first.jsonl" "$O/replay-first.json" -- uvx freecad-mcp@0.1.28 > "$O/replay-first.log" 2>&1
sleep 2
cp ~/hook-claude.stl "$O/hook-claude.stl" 2>/dev/null
python3 - "$R/hook-claude.stl" "$O/hook-claude.stl" > "$O/compare.json" <<'PY'
import json, os, sys
sys.path.insert(0, '/lab')
from checker import mesh5, score_l5
out = {}
for k, p in (('run', sys.argv[1]), ('replay', sys.argv[2])):
    m = mesh5.measure_any(p) if os.path.exists(p) else None
    out[k] = None if m is None else {'triangles': m['triangles'], 'volume_mm3': m['volume_mm3'],
                                     'right_part': score_l5.right_part(m)['ok'], 'clean': score_l5.clean(m)['ok']}
a, b = out['run'], out['replay']
out['pass'] = bool(a and b and a['triangles'] == b['triangles'] and abs(a['volume_mm3'] - b['volume_mm3']) <= 0.01
                   and a['right_part'] == b['right_part'] and a['clean'] == b['clean'])
print(json.dumps(out, indent=1))
PY
fc_quit; sl_display_stop
echo "replay done ($RUN)"; cat "$O/compare.json"
