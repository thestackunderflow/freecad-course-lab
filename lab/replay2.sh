#!/bin/bash
# Lesson 2, lab L2-Q6 (no AI, free): a fresh FreeCAD 1.1.4 with the socket on; Claude's logged tools/call requests from
# runs/claude-1 replayed in order over the same plug (`uvx freecad-mcp@0.1.28`, our own client), with no mouse or key
# input; the window screenshotted before and after; the part the replay made saved and measured with the same
# freecadcmd line; compared with the by-hand part and with Claude's own. Writes out/l2/replay/.
#   tools/run.sh lab/replay2.sh [RUN]
set -u
. /lab/lab/common.sh
RUN=${1:-claude-1}
O=/lab/out/l2/replay; rm -rf "$O"; mkdir -p "$O"
R=/lab/out/l2/runs/$RUN
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 8
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 2
xdotool mousemove 300 900; sleep 1
SL_SHOT_WAKE=0 sl_shot "$O/before.png"
cd /lab
python3 -m client.replay "$R/transcript.jsonl" "$O/replay.json" -- uvx freecad-mcp@0.1.28 > "$O/replay.log" 2>&1
sleep 3
SL_SHOT_WAKE=0 sl_shot "$O/after.png"
read -r DOC OBJ SK < <(python3 -c "
import json, sys; sys.path.insert(0, '/lab')
from lab import fcrpc, newpart
st = json.loads(fcrpc.run(newpart.CODE)); p = newpart.pick(st, hand_doc='-none-')
print(' '.join(p) if p else '')")
echo "$DOC $OBJ $SK" > "$O/replay-part.txt"
python3 -m lab.fcrpc save "$DOC" /tmp/replay.FCStd > "$O/save.txt" 2>&1
FC_DOC=/tmp/replay.FCStd FC_OUT="$O/measure.json" freecadcmd /lab/checker/measure.py > "$O/measure.log" 2>&1
python3 -m checker.compare /lab/out/l2/hand/measure.json "$O/measure.json" "$O/compare-hand.json" 8500 > /dev/null 2>&1
python3 -m checker.compare "$R/measure.json" "$O/measure.json" "$O/compare-claude.json" 8500 > /dev/null 2>&1
fc_quit; sl_display_stop
echo "replay done: $DOC $OBJ"; head -c 400 "$O/replay.log"
