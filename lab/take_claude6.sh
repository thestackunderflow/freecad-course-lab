#!/bin/bash
# Lesson 6 take "B1".."B3" / "A1" (PLAN-L6 F10-F16; lab L6-Q3), paid. Started by
#   FCC_PREFIX=fc6 LESSON=l6 BUDGET_MARK="# --- GO 31 Oct 2026 FreeCAD L6" bash claude-run/run.sh B1 0.25 lab/take_claude6.sh
# The state a viewer has after lessons 1-5: Claude Code + uv installed, the plug added with --scope user (wrapped in
# the logging proxy), FreeCAD on the right with its socket on and lesson 5's hook open (hook-lesson5.FCStd = lesson
# 4's by-hand width30); Claude Code started in the terminal on the left (46 columns). The message is the committed file
# out/l6/messages/<A|B>-1.txt, typed one character at a time. If after the turn the hook is unchanged (hook_depth still
# 40 mm and the opening still 30), the committed out/l6/messages/trigger.txt ("Your choice.") is sent once. The live
# cost guard (lab/costguard.py) interrupts the turn if its estimate passes the run's cap ($0.25).
# After the turn, not filmed (lab query): every open document saved as a copy, the start file hashed again. Then filmed:
# our no-AI check in the same window (key 0 V F; Tools > Measure, Distance, the plate's inside face, Ctrl + the lip's
# inside top edge). Afterwards: Ctrl+O view, /cost, checker/l6read on every copy, checker/score_l6.
set -u
RUN=${1:-B1}
CAP=${COST_CAP:-0.25}
O=/lab/out/l6/runs/$RUN; mkdir -p "$O"
. /lab/lab/common.sh
. /lab/lab/l6common.sh
K=${RUN:0:1}
M1=$(cat /lab/out/l6/messages/$K-1.txt); M2=$(cat /lab/out/l6/messages/trigger.txt)
printf '%s\n' "$M1" > "$O/message-1.txt"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true; mkdir -p ~/hook; claude_home /home/maker/hook
cp /lab/out/l4/hand/width30.FCStd ~/hook-lesson5.FCStd
md5sum ~/hook-lesson5.FCStd > "$O/start.md5"
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
mw = FreeCADGui.getMainWindow()
FreeCAD.openDocument('/home/maker/hook-lesson5.FCStd')
FreeCADGui.activateWorkbench('PartDesignWorkbench')
mdi = mw.findChild(QtWidgets.QMdiArea)
for w in mdi.subWindowList():
    if w.windowTitle().startswith('Start'):
        w.close()
FreeCADGui.runCommand('Std_Measure')
QtWidgets.QApplication.processEvents()
for c in mw.findChildren(QtWidgets.QCheckBox):
    if c.isVisible() and c.text().replace('&', '').startswith('Show Delta'):
        c.setChecked(False)
FreeCADGui.Control.closeDialog()
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
unchanged() {   # true when hook_depth is still 40 mm and the start document's part still has the 30 opening
  (cd /lab && python3 - <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
out = fcrpc.run("""import FreeCAD
d = FreeCAD.getDocument('hook_lesson5')
s = [o for o in d.Objects if o.TypeId == 'Spreadsheet::Sheet']
v = s[0].get('hook_depth') if s else None
b = [o for o in d.Objects if o.TypeId == 'PartDesign::Body']
print(abs(float(getattr(v, 'Value', v)) - 40) < 1e-6 and b and abs(b[-1].Shape.Volume - 14848.584) < 0.01)""")
sys.exit(0 if out.strip() == 'True' else 1)
PY
  )
}
(cd /lab && python3 -m lab.costguard "$O" cc "$CAP") > "$O/costguard.log" 2>&1 &
GUARD=$!
sl_record "$O"
sl_mark "recording started: Claude Code (left), FreeCAD with lesson 5's hook (right)"
sl_nap 2
cd /lab && python3 -m lab.drive "$O" cc "$M1"
sl_nap 2
echo "first $(lines)" >> "$O/stages.txt"
if [ ! -e "$O/.guard-tripped" ] && unchanged; then
  sl_mark "the hook is unchanged after the turn: the fixed reply"
  echo "trigger sent" > "$O/trigger.json"
  cd /lab && python3 -m lab.drive "$O" cc "$M2"
  sl_nap 2
fi
echo "after $(lines)" >> "$O/stages.txt"
sl_mark "lab query: save every open document, hash the start file"
python3 -m lab.fcrpc docs > "$O/docs.json" 2>&1
python3 - "$O" <<'PY' > "$O/saves.txt" 2>&1
import json, sys
sys.path.insert(0, '/lab')
from lab import fcrpc
o = sys.argv[1]
for name in json.load(open(o + '/docs.json')):
    print(name, fcrpc.run(fcrpc.SAVE.format(doc=name, path='/tmp/after-%s.FCStd' % name)))
PY
md5sum ~/hook-lesson5.FCStd > "$O/start-after.md5"
ls -la ~ > "$O/home-after.txt" 2>&1
# our no-AI check, filmed in the same window
sl_mark "our check, no AI: Tools > Measure on the opening"
m6_view
m6_opening "$O/our-measure.txt" 5.0
sl_shot "$O/s1-ourcheck.png"
m6_close
sl_nap 1.0
sl_mark "recording stopped"
sl_stop
touch "$O/.guard-stop"; wait "$GUARD" 2>/dev/null
tmux send-keys -t cc C-o; sleep 6; pane cc 3000 > "$O/pane-expanded.txt"; tmux send-keys -t cc C-o; sleep 1
pane cc 3000 > "$O/pane-full.txt"
cp ~/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
pane cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
fc_quit; tmux kill-server 2>/dev/null; sl_display_stop
cd /lab
for f in /tmp/after-*.FCStd; do
  n=$(basename "$f" .FCStd); n=${n#after-}
  cp "$f" "$O/after-$n.FCStd"
  FC_DOC="$f" FC_OUT="$O/read-$n.json" freecadcmd /lab/checker/l6read.py > "$O/read-$n.log" 2>&1
done
python3 -m checker.score_l6 "$O" > "$O/score.log" 2>&1
echo "claude take done ($RUN)"; cat "$O/score.log"
