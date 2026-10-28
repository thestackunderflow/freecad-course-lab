#!/bin/bash
# Lab Q9 + Q11 (no AI, free): (1) a fresh FreeCAD 1.1.4 with the socket on; the window screenshotted, then Claude's
# logged tools/call requests from runs/claude-1 replayed in order over the same plug (`uvx freecad-mcp@0.1.28`, our
# own client), with no mouse or key input; the window screenshotted again (repaint probe); the result saved and
# measured with the same freecadcmd line. (2) Claude's saved document opened in a fresh FreeCAD and read over the plug
# with get_object + a read-only execute_code (the "no-AI read"). Writes out/l1/replay/.
#   tools/run.sh lab/replay.sh
set -u
. /lab/lab/common.sh
O=/lab/out/l1/replay; rm -rf "$O"; mkdir -p "$O"
R=/lab/out/l1/runs/claude-1
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
python3 - "$O" <<'EOF'
import json, sys
import numpy as np
import subprocess
o = sys.argv[1]
def load(p):
    raw = subprocess.run(['convert', p, '-crop', '1730x1800+1150+0', 'gray:-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8)
a, b = load(o + '/before.png'), load(o + '/after.png')
ch = float((np.abs(a.astype(int) - b.astype(int)) > 16).mean())
json.dump({'window_pixels_changed_fraction': round(ch, 4), 'input_between_shots': 'none (no mouse move, no key, no wake)',
           'repainted_without_input': ch > 0.01}, open(o + '/repaint.json', 'w'), indent=1)
print('repaint', ch)
EOF
python3 -m lab.fcrpc save Block /tmp/replay.FCStd > "$O/save.txt" 2>&1
FC_DOC=/tmp/replay.FCStd FC_OUT="$O/measure.json" freecadcmd /lab/checker/measure.py > "$O/measure.log" 2>&1
fc_quit; sleep 2
# (2) the no-AI read of Claude's own saved document, over the plug
cp "$R/claude.FCStd" /tmp/claude.FCStd
fc_start "$O/app2.log" 1.5; sleep 8
python3 - "$O" <<'EOF'
import json, sys
sys.path.insert(0, '/lab')
from lab import fcrpc
fcrpc.run("import FreeCAD\nFreeCAD.openDocument('/tmp/claude.FCStd')\nprint('ok')")
from client.mcp import McpClient
o = sys.argv[1]
c = McpClient(['uvx', 'freecad-mcp@0.1.28'], timeout_s=120, log_path=o + '/read-transcript.jsonl')
c.start()
obj = McpClient.text(c.call_tool('get_object', {'doc_name': 'claude', 'obj_name': 'Box', 'include_screenshot': False}))
code = ("import FreeCAD\ns = FreeCAD.getDocument('claude').getObject('Box').Shape\nb = s.BoundBox\n"
        "print(round(s.Volume, 4), [round(b.XLength, 4), round(b.YLength, 4), round(b.ZLength, 4)], [b.XMin, b.YMin, b.ZMin, b.ZMax])")
vol = McpClient.text(c.call_tool('execute_code', {'code': code, 'include_screenshot': False}))
c.close()
json.dump({'get_object': obj, 'execute_code_read': vol}, open(o + '/read.json', 'w'), indent=1)
print(vol)
EOF
fc_quit; sl_display_stop
echo "replay done"; cat "$O/replay.log" | head -20
