#!/bin/bash
# Lesson 4 take "plain" (PLAN-L4 F0, F18; lab L4-Q3), watch only: the same hook with the hole centres typed as plain
# numbers (lab/build4.py PLAIN=1, built headless before filming, from the same start file). Not filmed: the file
# opened and shown as the by-hand file shows it (a file saved headless carries no view data: the body's tip visible,
# the rest hidden). Filmed: the hook from the back; the sheet opened; Windows, Tile; width 30 mm; key 6 in the hook's window; the volume line; the hole sketch opened (its across
# distance still 10 mm); Close. Not filmed: a copy saved and measured after width 30.
#   FCC_PREFIX=fc4 tools/run.sh lab/take_plain4.sh
set -u
. /lab/lab/common.sh
O=/lab/out/l4/plain; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
FC_IN=/lab/out/l3/hand/back5.FCStd FC_OUT=$HOME/hook-plain.FCStd PLAIN=1 freecadcmd /lab/lab/build4.py > "$O/build.log" 2>&1
grep "built hook" "$O/build.log"
sl_display $W $H
fc_start "$O/app.log" 1.8; sleep 8
cd /lab
python3 - > "$O/setup-rpc.txt" 2>&1 <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCAD, FreeCADGui
from PySide import QtCore, QtWidgets
mw = FreeCADGui.getMainWindow()
FreeCADGui.activateWorkbench('PartDesignWorkbench')
for w in mw.findChildren(QtWidgets.QMdiArea)[0].subWindowList():
    if w.windowTitle().startswith('Start'):
        w.close()
for w in mw.findChildren(QtWidgets.QDockWidget):
    if w.objectName() in ('Python console',):
        w.show()
        mw.resizeDocks([w], [190], QtCore.Qt.Vertical)
        w.widget().clear()
d = FreeCAD.openDocument('/home/maker/hook-plain.FCStd')
g = FreeCADGui.getDocument(d.Name)
for o in d.Objects:
    if hasattr(g.getObject(o.Name), 'Visibility'):
        g.getObject(o.Name).Visibility = o.Name in ('Body', 'Fillet')
FreeCADGui.activeDocument().activeView().viewLeft()
FreeCADGui.SendMsgToActiveView('ViewFit')
print(1)"""))
PY
sleep 2
DOC=hook_plain
B() { python3 -m lab.button "$@" 2>>"$O/lab-query.err"; }
row() { python3 -m lab.fcrpc row "$DOC" "$1" 2>>"$O/lab-query.err"; }
open_to() {
  local ax ay i
  for i in 1 2 3; do
    read -r ax ay < <(python3 -m lab.fcrpc arrow "$DOC" "$1" 2>>"$O/lab-query.err")
    { [ "${ax:-}" = open ] || [ "${ax:-}" = none ] || [ -z "${ay:-}" ]; } && return 0
    sl_click "$ax" "$ay" "tree: open a row"; sl_nap 0.6
  done
}
SP() { python3 -m lab.sketchpt "$DOC" Sketch001 "$@" 2>>"$O/lab-query.err"; }
dbl() { sl_glide "$1" "$2" 20; sl_nap 0.5; sl_mark "$3"; xdotool click --repeat 2 --delay 120 1; }
console() {
  local cx cy; read -r cx cy < <(B console)
  sl_click "$cx" "$cy" "console: click"
  sl_type "$1" "console: typed $2" 70
  sl_key Return "console: Enter ($2)"
  sl_nap 3.5
}
xdotool mousemove 1500 700
sl_record "$O"
sl_mark "recording started"
sl_nap 1.0
sl_mark "the plain hook from the back, 20 wide"; sl_nap 2.5
sl_shot "$O/s1-back20.png"
read -r SX SY < <(row Spreadsheet)
dbl "$SX" "$SY" "tree: double-click Spreadsheet"
sl_nap 3.0
read -r MX MY < <(B menu Windows)   # its place depends on the workbench's menus
sl_click "$MX" "$MY" "Windows menu"
sl_glide $((MX + 5)) 165 15; sl_nap 0.5
sl_click $((MX + 5)) 165 "Windows: Tile"
sl_nap 2.5
read -r EX2 EY2 < <(B cell 12 3); sl_click "$EX2" "$EY2" "the sheet: an empty cell"
sl_nap 0.8
read -r WX WY < <(B cell 4 1); sl_click "$WX" "$WY" "cell B5 (width)"
sl_nap 0.8
sl_type "30 mm" "B5: typed 30 mm" 160
sl_key Return "B5: Enter (30 mm)"
sl_nap 3.5
read -r VX VY < <(B view); sl_click "$VX" "$VY" "the hook's window: an empty spot"
sl_nap 0.5
sl_key 6 "key 6: the back, 30 wide"; sl_key v "key V"; sl_key f "key F (fit all)"; sl_nap 2.5
sl_shot "$O/s2-back30.png"
open_to Fillet
read -r PX PY < <(row Fillet)
sl_click "$PX" "$PY" "tree: Fillet"
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line (30 wide)"
sl_mark "lab query: save width30"
python3 -m lab.fcrpc save "$DOC" /tmp/width30.FCStd > "$O/save.txt" 2>&1 && cp /tmp/width30.FCStd "$O/"
open_to Sketch001
read -r RX RY < <(row Sketch001)
dbl "$RX" "$RY" "tree: double-click the hole sketch"
sl_nap 3.5
read -r X0 Y0 < <(SP 0 center); sl_glide "$X0" "$Y0" 20; sl_mark "hover: the lower hole's centre"; sl_nap 3.0
sl_shot "$O/s3-sketch30.png"
sl_click 2528 616 "Close (the hole sketch)"
sl_nap 2.0
sl_mark "recording stopped"
sl_stop
FC_DOC=/tmp/width30.FCStd FC_OUT="$O/measure-width30.json" freecadcmd /lab/checker/measure.py > "$O/measure.log" 2>&1
fc_quit; sl_display_stop
python3 -c "
import json, sys; sys.path.insert(0, '/lab')
from checker import holes, score_l4
m = json.load(open('$O/measure-width30.json'))
print(json.dumps(holes.check(score_l4._part(m), dict(holes.NAMES, width=30)), indent=1))" > "$O/check-width30.json" 2>&1
echo "plain take done"; cat "$O/check-width30.json"
