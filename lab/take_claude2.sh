#!/bin/bash
# Lesson 2 take "claude-N" (PLAN-L2 F22-F26, F28-F29; lab L2-Q3, L2-Q4, L2-Q7, L2-Q8), paid. Started by
#   LESSON=l2 BUDGET_MARK="# --- GO 29 Oct 2026 FreeCAD L2" bash claude-run/run.sh claude-N CAP lab/take_claude2.sh
# The state a viewer has after lesson 1 and the by-hand part: Claude Code + uv installed, the plug added with
# --scope user (wrapped in the logging proxy), FreeCAD on the right with its socket on, the by-hand hook document
# open and the Python console showing; Claude Code already started in the terminal on the left (46 columns).
# Filmed, nobody touching FreeCAD except where a viewer would: File, New Document (an empty document); message 1 (the
# SolidCraft lesson's message with one word changed) typed into Claude Code; its reply; Ctrl+O (what it did);
# message 2; then, as the viewer: the 3D view clicked, key 0 and V, F (isometric, fit all); Claude's part clicked in
# the tree; the two console lines; Claude's sketch opened (double-click), its Sketcher message; Close.
# Afterwards (not filmed): /cost, Claude's document saved and measured.
set -u
RUN=${1:-claude-1}
O=/lab/out/l2/runs/$RUN; mkdir -p "$O"
. /lab/lab/common.sh
M1=${M1:-"In FreeCAD, sketch this outline on the XZ plane, starting at 0,0: right 25, up 10, left 5, down 5, left 15, up 55, left 5, then back to the start. Extrude it 20 mm."}
M2=${M2:-"Measure it, and list the steps in its model tree."}
printf '%s\n' "$M1" > "$O/message-1.txt"; printf '%s\n' "$M2" > "$O/message-2.txt"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true; mkdir -p ~/hook; claude_home /home/maker/hook
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
json.dump({'mcpServers': {'freecad': d['mcpServers']['freecad']}}, open(os.path.join(o, 'entry-as-run.json'), 'w'), indent=1)
EOF
claude --version > "$O/claude-version.txt" 2>&1
cp /lab/out/l2/hand/hand.FCStd /tmp/hand.FCStd
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 6
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 1
cd /lab && python3 - > "$O/setup-rpc.txt" 2>&1 <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCAD, FreeCADGui
from PySide import QtWidgets
FreeCAD.openDocument('/tmp/hand.FCStd')
FreeCADGui.activateWorkbench('PartDesignWorkbench')
FreeCADGui.activeDocument().activeView().viewIsometric()
FreeCADGui.SendMsgToActiveView('ViewFit')
for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
    if w.objectName() in ('Python console',):
        w.show()
print('ok')"""))
PY
sleep 2
cd ~/hook
term_open cc 0 0 46 36 30 claude
wait_pane cc 'auto mode|❯' 40; sleep 4
pane cc > "$O/pane-start.txt"
xdotool mousemove 2000 700
sl_record "$O"
sl_mark "recording started: Claude Code (left), FreeCAD with the by-hand hook (right)"
sl_nap 2
sl_click 1188 33 "FreeCAD: File menu"
sl_click 1267 68 "File: New Document"
sl_nap 1.5
sl_glide 700 1500 20; sl_mark "to the terminal"
sl_nap 0.5
cd /lab && python3 -m lab.drive "$O" cc "$M1"
sl_nap 2
tmux send-keys -t cc C-o; sl_mark "Ctrl+O: expanded view"
sl_nap 8; pane cc 600 > "$O/pane-expanded.txt"
tmux send-keys -t cc C-o; sl_mark "Ctrl+O: back"
sl_nap 2
python3 -m lab.drive "$O" cc "$M2"
sl_nap 2
# the viewer: the 3D view clicked, isometric, fit all
sl_click 2650 1250 "viewer: click the 3D view"
sl_key 0 "viewer: key 0 isometric"
sl_nap 1.0
sl_key v "viewer: key V"; sl_key f "viewer: key F (fit all)"
sl_nap 3.0
sl_shot "$O/s1-part.png"
sl_mark "lab query: where is Claude's part"
read -r DOC OBJ SK < <(python3 -m lab.newpart "$O/newpart.json" 2>>"$O/lab-query.err")
echo "$DOC $OBJ $SK" > "$O/claude-part.txt"
read -r RX RY < <(python3 -m lab.fcrpc row "$DOC" "$OBJ" 2>>"$O/lab-query.err")
sl_nap 1.0
sl_click "$RX" "$RY" "tree: Claude's part"
sl_nap 1.5
sl_click 2016 1722 "console: click"
sl_type "Gui.Selection.getSelection()[0].Shape.Volume" "console: typed the volume line" 85
sl_key Return "console: Enter"
sl_nap 3.5
sl_type "b = Gui.Selection.getSelection()[0].Shape.BoundBox; round(b.ZMin, 3), round(b.ZMax, 3)" "console: typed the height line" 70
sl_key Return "console: Enter 2"
sl_nap 4.0
sl_shot "$O/s2-console.png"
if [ "$SK" != "-" ] && [ -n "$SK" ]; then
  for i in 1 2 3; do
    read -r AX AY < <(python3 -m lab.fcrpc arrow "$DOC" "$SK" 2>>"$O/lab-query.err")
    [ "$AX" = open ] || [ "$AX" = none ] || [ -z "${AY:-}" ] && break
    sl_click "$AX" "$AY" "tree: open a row to reach the sketch"; sl_nap 0.8
  done
  read -r KX KY < <(python3 -m lab.fcrpc row "$DOC" "$SK" 2>>"$O/lab-query.err")
  if [ -n "${KX:-}" ]; then
    sl_glide "$KX" "$KY" 20; sl_nap 0.5
    sl_mark "tree: double-click Claude's sketch"; xdotool click --repeat 2 --delay 120 1
    sl_nap 4.0
    sl_shot "$O/s3-sketch.png"
    sl_mark "Claude's sketch open"
    sl_nap 3.0
  fi
fi
sl_mark "recording stopped"
sl_stop
cp ~/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
pane cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
cd /lab
python3 -m lab.fcrpc docs > "$O/docs.json" 2>&1
python3 -c "
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run('import FreeCADGui\nd = FreeCADGui.ActiveDocument\nd.resetEdit() if d and d.getInEdit() else None\nprint(1)'))" > /dev/null 2>&1
python3 -m lab.fcrpc save "$DOC" /tmp/claude.FCStd > "$O/save.txt" 2>&1 && cp /tmp/claude.FCStd "$O/claude.FCStd"
FC_DOC=/tmp/claude.FCStd FC_OUT="$O/measure.json" freecadcmd /lab/checker/measure.py > "$O/measure.log" 2>&1
python3 -c "
import sys, json; sys.path.insert(0, '/lab')
from client import replay
json.dump(replay.call_pairs('$O/transcript.jsonl'), open('$O/calls.json', 'w'), indent=1)
"
fc_quit; tmux kill-server 2>/dev/null; sl_display_stop
echo "claude take done: $DOC $OBJ $SK"
