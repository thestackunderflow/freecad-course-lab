#!/bin/bash
# Lesson 5 take "B1" / "A1" (PLAN-L5 F18-F22; lab L5-Q7), paid. Started by
#   FCC_PREFIX=fc5 LESSON=l5 BUDGET_MARK="# --- GO 31 Oct 2026 FreeCAD L5" bash claude-run/run.sh B1 0.30 lab/take_claude5.sh
# The state a viewer has after lessons 1-4: Claude Code + uv installed, the plug added with --scope user (wrapped in
# the logging proxy), FreeCAD on the right with its socket on and lesson 4's hook open (hook-lesson4.FCStd = lesson
# 4's by-hand width30); Claude Code started in the terminal on the left (46 columns). The messages are the committed
# files out/l5/messages/<A|B>-1.txt, 2.txt, typed one character at a time. The live cost guard (lab/costguard.py)
# interrupts the turn if its estimate passes the run's cap ($0.30). Not filmed (logged "lab query" events): the STL
# copied after message 1. Afterwards: Ctrl+O view, /cost, scoring (checker/score_l5).
set -u
RUN=${1:-B1}
CAP=${COST_CAP:-0.30}
O=/lab/out/l5/runs/$RUN; mkdir -p "$O"
. /lab/lab/common.sh
K=${RUN:0:1}
M1=$(cat /lab/out/l5/messages/$K-1.txt); M2=$(cat /lab/out/l5/messages/$K-2.txt)
printf '%s\n' "$M1" > "$O/message-1.txt"; printf '%s\n' "$M2" > "$O/message-2.txt"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true; mkdir -p ~/hook; claude_home /home/maker/hook
cp /lab/out/l4/hand/width30.FCStd ~/hook-lesson4.FCStd
printf 'set -g focus-events on\n' >> ~/.tmux.conf
claude mcp add --scope user freecad -- uvx freecad-mcp@0.1.28 > "$O/mcp-add.txt" 2>&1
uvx freecad-mcp@0.1.28 --help > /dev/null 2>&1   # the uv cache warm, as after lesson 1's connect step
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
claude --version > "$O/claude-version.txt" 2>&1
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 6
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 1
cd /lab && python3 - > "$O/setup-rpc.txt" 2>&1 <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCAD, FreeCADGui
from PySide import QtWidgets
FreeCAD.openDocument('/home/maker/hook-lesson4.FCStd')
FreeCADGui.activateWorkbench('PartDesignWorkbench')
mdi = FreeCADGui.getMainWindow().findChild(QtWidgets.QMdiArea)
for w in mdi.subWindowList():
    if w.windowTitle().startswith('Start'):
        w.close()
for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
    if w.objectName() in ('Python console',):
        w.show()
        w.widget().clear()
FreeCADGui.activeDocument().activeView().viewIsometric()
FreeCADGui.SendMsgToActiveView('ViewFit')
print('ok')"""))
PY
sleep 2
cd ~/hook
term_open cc 0 0 46 36 30 claude
wait_pane cc 'auto mode|❯' 40; sleep 4
pane cc > "$O/pane-start.txt"
xdotool mousemove 2000 700
lines() { wc -l < "$O/transcript.jsonl" 2>/dev/null || echo 0; }
(cd /lab && python3 -m lab.costguard "$O" cc "$CAP") > "$O/costguard.log" 2>&1 &
GUARD=$!
sl_record "$O"
sl_mark "recording started: Claude Code (left), FreeCAD with lesson 4's hook (right)"
sl_nap 2
cd /lab && python3 -m lab.drive "$O" cc "$M1"
sl_nap 2
sl_mark "lab query: copy the STL after message 1"
echo "first $(lines)" >> "$O/stages.txt"
ls -la ~ > "$O/home-after-1.txt" 2>&1
cp ~/hook-claude.stl "$O/hook-claude.stl" 2>/dev/null || find ~ -name '*.stl' -newer ~/hook-lesson4.FCStd > "$O/stl-found.txt" 2>/dev/null
sl_click 2650 1250 "viewer: click the 3D view"
sl_key 0 "viewer: key 0 isometric"; sl_key v "viewer: key V"; sl_key f "viewer: key F (fit all)"
sl_nap 3.0
sl_shot "$O/s1-after1.png"
if [ ! -e "$O/.guard-tripped" ]; then
  cd /lab && python3 -m lab.drive "$O" cc "$M2"
  sl_nap 3
fi
echo "after2 $(lines)" >> "$O/stages.txt"
sl_shot "$O/s2-after2.png"
sl_mark "recording stopped"
sl_stop
touch "$O/.guard-stop"; wait "$GUARD" 2>/dev/null
tmux send-keys -t cc C-o; sleep 6; pane cc 3000 > "$O/pane-expanded.txt"; tmux send-keys -t cc C-o; sleep 1
pane cc 3000 > "$O/pane-full.txt"
cp ~/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
pane cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
cd /lab
python3 -m lab.fcrpc docs > "$O/docs.json" 2>&1
python3 -c "
import sys, json; sys.path.insert(0, '/lab')
from client import replay
json.dump(replay.call_pairs('$O/transcript.jsonl'), open('$O/calls.json', 'w'), indent=1)
"
python3 -m checker.score_l5 "$O" > "$O/score.log" 2>&1
fc_quit; tmux kill-server 2>/dev/null; sl_display_stop
echo "claude take done ($RUN): $(ls -la "$O/hook-claude.stl" 2>&1)"
