#!/bin/bash
# fx2 run R1 (LAB-fx2 section 4, pre-registered; one run): Claude Code with the freecad plug (0.1.28, RPC server auto-started),
# FreeCAD open with washer.FCStd (take A) selected, one prompt. Started by claude-run/run.sh with LESSON=fx2.
set -u
RUN=${1:-R1}
O=/lab/out/fx2/runs/$RUN; mkdir -p "$O"
. /lab/lab/common.sh
M1="Export the washer for 3D printing and tell me what the slicer will say about its size"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true; mkdir -p ~/fx2 ~/run-fx2; claude_home /home/maker/run-fx2
cp /lab/out/fx2/A/washer.FCStd ~/fx2/washer.FCStd
claude mcp add --scope user freecad -- uvx freecad-mcp@0.1.28 > "$O/mcp-add.txt" 2>&1
uvx freecad-mcp@0.1.28 --help > /dev/null 2>&1
claude --version > "$O/claude-version.txt" 2>&1
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 8
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 1
cd /lab
python3 - > "$O/setup-rpc.txt" 2>&1 <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCAD, FreeCADGui
d = FreeCAD.openDocument('/home/maker/fx2/washer.FCStd')
FreeCADGui.activeDocument().activeView().viewIsometric()
FreeCADGui.SendMsgToActiveView('ViewFit')
FreeCADGui.Selection.addSelection(d.getObject('washer'))
FreeCADGui.activateWorkbench('FreeCADMCPAddonWorkbench')
print('ok')"""))
PY
sleep 3
python3 -m lab.fcrpc ping > "$O/socket-ping-before.txt" 2>&1; echo "exit $?" >> "$O/socket-ping-before.txt"
cat "$FC_DATA/freecad_mcp_settings.json" > "$O/settings-before.json"
SL_SHOT_WAKE=0 sl_shot "$O/before-recording.png"
cd ~/run-fx2
term_open cc 0 0 46 36 30 bash
python3 - "$O" <<'EOF'
import json, os, sys
o = sys.argv[1]
p = os.path.expanduser('~/.claude.json')
d = json.load(open(p))
e = d['mcpServers']['freecad']
json.dump({'mcpServers': {'freecad': e}}, open(os.path.join(o, 'entry-as-added.json'), 'w'), indent=1)
d['mcpServers']['freecad'] = dict(e, command='python3', args=['/lab/proxy/mcp_log_proxy.py', '--log', o + '/transcript.jsonl',
                                   '--png-dir', o, '--', e['command']] + list(e.get('args') or []))
json.dump(d, open(p, 'w'), indent=1)
EOF
claude --version > "$O/claude-version.txt" 2>&1; claude mcp list > "$O/mcp-list-before.txt" 2>&1
xdotool mousemove 2000 700
sl_record "$O"
sl_mark "recording started: a terminal (left), FreeCAD with the washer open (right)"
sl_nap 1.5
say_cmd cc 'claude' "claude: typed"
wait_pane cc 'auto mode|❯' 40 && sl_mark "claude: start screen"
sl_nap 3
cd /lab && python3 -m lab.drive "$O" cc "$M1"
sl_nap 3
pane cc 400 > "$O/pane-after-m1.txt"
sl_nap 3
ls -l /home/maker/fx2 /home/maker/run-fx2 > "$O/ls-after.txt" 2>&1; cp /home/maker/fx2/*.stl /home/maker/fx2/*.3mf /home/maker/run-fx2/* "$O/" 2>/dev/null
sl_mark "recording stopped"
sl_stop
pane cc 3000 > "$O/pane-full.txt"
cp ~/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
( find ~/.cache -path '*mcp-logs*' -type f 2>/dev/null; find ~/.claude -name '*.txt' -path '*mcp*' 2>/dev/null ) > "$O/mcp-log-files.txt"
for f in $(find ~/.cache -path '*mcp-logs*' -type f 2>/dev/null | head -5); do echo "=== $f"; tail -c 4000 "$f"; done > "$O/mcp-log-tail.txt" 2>&1
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
pane cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
fc_quit; tmux kill-server 2>/dev/null; sl_display_stop
echo "R1 take done"
