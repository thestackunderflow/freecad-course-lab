#!/bin/bash
# Lesson 7, run R1 (paid; pre-registered in out/l7/prereg.json before the run). Started by claude-run/run.sh with
# LESSON=l7. FreeCAD open on the right with lesson 3's hook, the add-on in Mod, the MCP Addon workbench showing and
# the RPC server STOPPED (Auto-Start off), set up through the socket before filming, then the console cleared. Filmed:
# `claude` (no flags), message 1; then, as the viewer, Start RPC Server clicked in FreeCAD; message 2.
set -u
RUN=${1:-R1}
O=/lab/out/l7/runs/$RUN; mkdir -p "$O"
. /lab/lab/common.sh
M1=${M1:-"What documents are open in FreeCAD?"}
M2=${M2:-"I clicked Start RPC Server in FreeCAD. Try again."}
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true; mkdir -p ~/hook; claude_home /home/maker/hook
cp /lab/out/l3/hand/back5.FCStd ~/hook.FCStd
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
FreeCAD.openDocument('/home/maker/hook.FCStd')
FreeCADGui.activeDocument().activeView().viewIsometric()
FreeCADGui.SendMsgToActiveView('ViewFit')
FreeCADGui.activateWorkbench('FreeCADMCPAddonWorkbench')
FreeCADGui.runCommand('Toggle_Auto_Start', 0)
print('ok')"""))
print(fcrpc.run("import FreeCADGui\nFreeCADGui.runCommand('Stop_RPC_Server', 0)\nprint('stop sent')"))
PY
sleep 3
python3 -m lab.fcrpc ping > "$O/socket-ping-before.txt" 2>&1; echo "exit $?" >> "$O/socket-ping-before.txt"
cat "$FC_DATA/freecad_mcp_settings.json" > "$O/settings-before.json"
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
d['mcpServers']['freecad'] = dict(e, command='python3', args=['/lab/proxy/mcp_log_proxy.py', '--log', o + '/transcript.jsonl',
                                   '--png-dir', o, '--', e['command']] + list(e.get('args') or []))
json.dump(d, open(p, 'w'), indent=1)
EOF
xdotool mousemove 2000 700
sl_record "$O"
sl_mark "recording started: a terminal (left), FreeCAD with the hook open and the socket off (right)"
sl_nap 1.5
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
sl_nap 5
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
