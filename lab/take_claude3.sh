#!/bin/bash
# Lesson 3 take "B1" / "A1" / "B2" (PLAN-L3 F21-F28; lab L3-Q4), paid. Started by
#   LESSON=l3 BUDGET_MARK="# --- GO 29 Oct 2026 FreeCAD L3" bash claude-run/run.sh B1 CAP lab/take_claude3.sh
# The state a viewer has after lessons 1-2: Claude Code + uv installed, the plug added with --scope user (wrapped in
# the logging proxy), FreeCAD on the right with its socket on and an empty document; Claude Code started in the
# terminal on the left (46 columns). The messages are the committed files out/l3/messages/<A|B>-1.txt, 2.txt, 3.txt
# (B = one sentence in front of lesson 2's message; A = lesson 2's message alone), typed one character at a time.
# Filmed, nobody touching FreeCAD except where a viewer would: message 1; then, as the viewer: the 3D view clicked,
# key 0, Fit all; Claude's part clicked in the tree; the volume line. Message 2; the volume line and the X line.
# Message 3; the volume line. Claude's spreadsheet (if any) double-clicked open. Not filmed (logged "lab query"
# events): a saved copy after each message, measured with freecadcmd. Afterwards: Ctrl+O view, /cost, scoring.
set -u
RUN=${1:-B1}
O=/lab/out/l3/runs/$RUN; mkdir -p "$O"
. /lab/lab/common.sh
K=${RUN:0:1}
M1=$(cat /lab/out/l3/messages/$K-1.txt); M2=$(cat /lab/out/l3/messages/$K-2.txt); M3=$(cat /lab/out/l3/messages/$K-3.txt)
printf '%s\n' "$M1" > "$O/message-1.txt"; printf '%s\n' "$M2" > "$O/message-2.txt"; printf '%s\n' "$M3" > "$O/message-3.txt"
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
FreeCAD.newDocument('Unnamed')
FreeCADGui.activateWorkbench('PartDesignWorkbench')
mdi = FreeCADGui.getMainWindow().findChild(QtWidgets.QMdiArea)
for w in mdi.subWindowList():
    if w.windowTitle().startswith('Start'):
        w.close()
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
lines() { wc -l < "$O/transcript.jsonl" 2>/dev/null || echo 0; }
snap() {   # snap STAGE: (not filmed) Claude's part's document saved and measured
  sl_mark "lab query: save after $1"
  read -r DOC OBJ SK < <(cd /lab && python3 -m lab.newpart "$O/newpart-$1.json" 2>>"$O/lab-query.err")
  echo "$DOC $OBJ $SK" > "$O/part-$1.txt"
  echo "$1 $(lines)" >> "$O/stages.txt"
  if [ -n "${DOC:-}" ]; then
    (cd /lab && python3 -m lab.fcrpc save "$DOC" "/tmp/$1.FCStd" > "$O/save-$1.txt" 2>&1) && cp "/tmp/$1.FCStd" "$O/$1.FCStd"
    FC_DOC="/tmp/$1.FCStd" FC_OUT="$O/measure-$1.json" freecadcmd /lab/checker/measure.py > "$O/measure-$1.log" 2>&1
  fi
}
console() {   # console "line" LABEL: typed into FreeCAD's Python console as a viewer
  sl_click 2016 1722 "console: click"
  sl_type "$1" "console: typed $2" 70
  sl_key Return "console: Enter ($2)"
  sl_nap 3.0
}
pick_part() {   # the viewer clicks Claude's part in the tree (opens the rows above it first; model-index lookup)
  local rx ry ax ay i
  for i in 1 2 3; do
    read -r ax ay < <(cd /lab && python3 -m lab.fcrpc arrow "$DOC" "$OBJ" 2>>"$O/lab-query.err")
    { [ "${ax:-}" = open ] || [ "${ax:-}" = none ] || [ -z "${ay:-}" ]; } && break
    sl_click "$ax" "$ay" "tree: open a row"; sl_nap 0.6
  done
  read -r rx ry < <(cd /lab && python3 -m lab.fcrpc row "$DOC" "$OBJ" 2>>"$O/lab-query.err")
  if [ -n "${ry:-}" ]; then sl_click "$rx" "$ry" "tree: Claude's part"; else sl_mark "tree: Claude's part row not found"; fi
  sl_nap 1.2
}
sl_record "$O"
sl_mark "recording started: Claude Code (left), FreeCAD with an empty document (right)"
sl_nap 2
cd /lab && python3 -m lab.drive "$O" cc "$M1"
sl_nap 2
snap first
sl_click 2650 1250 "viewer: click the 3D view"
sl_key 0 "viewer: key 0 isometric"
sl_nap 1.0
sl_key v "viewer: key V"; sl_key f "viewer: key F (fit all)"
sl_nap 3.0
sl_shot "$O/s1-first.png"
pick_part
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line"
sl_shot "$O/s2-first-console.png"
cd /lab && python3 -m lab.drive "$O" cc "$M2"
sl_nap 2
snap after2
sl_click 2650 1250 "viewer: click the 3D view"; sl_key v "viewer: key V"; sl_key f "viewer: key F (fit all)"
sl_nap 2.5
sl_shot "$O/s3-after2.png"
pick_part
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line"
console "b = Gui.Selection.getSelection()[0].Shape.BoundBox; round(b.XMin, 3), round(b.XMax, 3)" "the X line"
sl_shot "$O/s4-after2-console.png"
cd /lab && python3 -m lab.drive "$O" cc "$M3"
sl_nap 2
snap after3
sl_click 2650 1250 "viewer: click the 3D view"; sl_key v "viewer: key V"; sl_key f "viewer: key F (fit all)"
sl_nap 2.5
sl_shot "$O/s5-after3.png"
pick_part
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line"
sl_shot "$O/s6-after3-console.png"
# Claude's spreadsheet, if it made one: opened from the tree as a viewer would
SHEET=$(cd /lab && python3 -c "
import json
d = json.load(open('$O/measure-after3.json')) if __import__('os').path.exists('$O/measure-after3.json') else {}
s = d.get('sheets') or []
print(s[0]['name'] if s else '')" 2>/dev/null)
if [ -n "$SHEET" ]; then
  for i in 1 2 3; do
    read -r AX AY < <(cd /lab && python3 -m lab.fcrpc arrow "$DOC" "$SHEET" 2>>"$O/lab-query.err")
    { [ "${AX:-}" = open ] || [ "${AX:-}" = none ] || [ -z "${AY:-}" ]; } && break
    sl_click "$AX" "$AY" "tree: open a row to reach the spreadsheet"; sl_nap 0.8
  done
  read -r SX SY < <(cd /lab && python3 -m lab.fcrpc row "$DOC" "$SHEET" 2>>"$O/lab-query.err")
  if [ -n "${SY:-}" ]; then
    sl_glide "$SX" "$SY" 20; sl_nap 0.5
    sl_mark "tree: double-click Claude's spreadsheet"; xdotool click --repeat 2 --delay 120 1
    sl_nap 4.0
    sl_shot "$O/s7-sheet.png"
    sl_mark "Claude's spreadsheet open"
    sl_nap 3.0
  fi
fi
sl_mark "recording stopped"
sl_stop
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
python3 -m checker.score_l3 "$O" > "$O/score.log" 2>&1
fc_quit; tmux kill-server 2>/dev/null; sl_display_stop
echo "claude take done: $(cat "$O/part-first.txt" 2>/dev/null)"
