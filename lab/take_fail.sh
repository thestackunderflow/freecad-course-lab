#!/bin/bash
# Take "fail-N" (F28, the Short S0-S3; lab Q10a), paid. Started by claude-run/run.sh.
# The socket OFF: FreeCAD on the right with the MCP Addon workbench showing, its RPC server stopped and Auto-Start
# off (done through the socket itself before filming, then the console cleared). Filmed: `claude mcp list` typed in
# the terminal (does it still say Connected?); `claude`; the block request; whatever happens; then, as the viewer,
# Start RPC Server clicked in FreeCAD; "Try again."; the block; its row clicked in the tree and the console line typed.
set -u
RUN=${1:-fail-1}
O=/lab/out/l1/runs/$RUN; mkdir -p "$O"
. /lab/lab/common.sh
M1=${M1:-"Make a block 5 by 20 by 60 millimetres in FreeCAD, then tell me its volume."}
M2=${M2:-"Try again."}
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true; mkdir -p ~/hook; claude_home /home/maker/hook
claude mcp add --scope user freecad -- uvx freecad-mcp@0.1.28 > "$O/mcp-add.txt" 2>&1
uvx freecad-mcp@0.1.28 --help > /dev/null 2>&1
claude --version > "$O/claude-version.txt" 2>&1
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 6
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 1
cd /lab
python3 - > "$O/setup-rpc.txt" 2>&1 <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCAD, FreeCADGui
from PySide import QtWidgets
FreeCAD.newDocument('Unnamed')
FreeCADGui.activeDocument().activeView().viewIsometric()
for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
    if w.objectName() == 'Python console':
        w.show()
FreeCADGui.activateWorkbench('FreeCADMCPAddonWorkbench')
FreeCADGui.runCommand('Toggle_Auto_Start', 0)
print('ok')"""))
print(fcrpc.run("import FreeCADGui\nFreeCADGui.runCommand('Stop_RPC_Server', 0)\nprint('stop sent')"))
PY
sleep 3
python3 -m lab.fcrpc ping > "$O/socket-ping-before.txt" 2>&1; echo "exit $?" >> "$O/socket-ping-before.txt"
cat "$FC_DATA/freecad_mcp_settings.json" > "$O/settings-before.json"
# the console cleared (its own Clear console action) so the setup lines are not on screen
xdotool mousemove 2000 1650 click 3; sleep 1; xdotool mousemove 2094 1563 click 1; sleep 1
SL_SHOT_WAKE=0 sl_shot "$O/before-recording.png"
cd ~/hook
term_open cc 0 0 46 36 30 bash
python3 - "$O" <<'EOF'
import json, os, sys
o = sys.argv[1]
p = os.path.expanduser('~/.claude.json')
d = json.load(open(p))
e = d['mcpServers']['freecad']
json.dump({'mcpServers': {'freecad': e}}, open(os.path.join(o, 'entry-as-added.json'), 'w'), indent=1)
EOF
xdotool mousemove 2000 700
sl_record "$O"
sl_mark "recording started: a terminal (left), FreeCAD with the socket off (right)"
sl_nap 1.5
say_cmd cc 'claude mcp list' "mcp list: typed"
wait_pane cc 'Connected|Failed|failed' 60 && sl_mark "mcp list: result shown"
sl_nap 4
pane cc > "$O/pane-mcp-list.txt"
python3 - "$O" <<'EOF'
import json, os, sys
o = sys.argv[1]
p = os.path.expanduser('~/.claude.json')
d = json.load(open(p))
e = d['mcpServers']['freecad']
d['mcpServers']['freecad'] = dict(e, command='python3', args=['/lab/proxy/mcp_log_proxy.py', '--log', o + '/transcript.jsonl',
                                   '--png-dir', o, '--', e['command']] + list(e.get('args') or []))
json.dump(d, open(p, 'w'), indent=1)
json.dump({'mcpServers': {'freecad': d['mcpServers']['freecad']}}, open(os.path.join(o, 'entry-as-run.json'), 'w'), indent=1)
EOF
say_cmd cc 'claude' "claude: typed"
wait_pane cc 'auto mode|❯' 40 && sl_mark "claude: start screen"
sl_nap 3
cd /lab && python3 -m lab.drive "$O" cc "$M1"
sl_nap 3
pane cc 400 > "$O/pane-after-m1.txt"
sl_click 1254 186 "FreeCAD: Start RPC Server"
sl_nap 3
SL_SHOT_WAKE=0 sl_shot "$O/started.png"
sl_glide 700 1500 20; sl_mark "to the terminal"
python3 -m lab.drive "$O" cc "$M2"
sl_nap 2
sl_mark "lab query: where is Claude's block"
read -r DOC OBJ < <(python3 -m lab.newblock "$O/newblock.json" 2>>"$O/lab-query.err")
echo "$DOC $OBJ" > "$O/claude-block.txt"
read -r RX RY < <(python3 -m lab.fcrpc row "$DOC" "$OBJ" 2>>"$O/lab-query.err")
sl_nap 1.5
[ -n "${RX:-}" ] && sl_click "$RX" "$RY" "tree: Claude's block"
sl_nap 1.5
sl_click 2016 1722 "console: click"
sl_type "Gui.Selection.getSelection()[0].Shape.Volume" "console: typed the volume line" 85
sl_key Return "console: Enter"
sl_nap 5
sl_mark "recording stopped"
sl_stop
cp ~/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
pane cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
python3 -m lab.fcrpc save "$DOC" /tmp/fail.FCStd > "$O/save.txt" 2>&1 && \
  FC_DOC=/tmp/fail.FCStd FC_OUT="$O/measure.json" freecadcmd /lab/checker/measure.py > "$O/measure.log" 2>&1
python3 -c "
import sys, json; sys.path.insert(0, '/lab')
from client import replay
json.dump(replay.call_pairs('$O/transcript.jsonl'), open('$O/calls.json', 'w'), indent=1)
"
fc_quit; tmux kill-server 2>/dev/null; sl_display_stop
echo "fail take done: $DOC $OBJ"
