#!/bin/bash
# Lesson 4 take "plain" (PLAN-L4 F0, F18; lab L4-Q3), watch only: the same hook with the hole centres typed as plain
# numbers (lab/build4.py PLAIN=1, built headless before filming, from the same start file). Filmed: File, Open; the sheet
# opened; Windows, Tile; width 30 mm; key 6 in the hook's window; the volume line; the hole sketch opened (its across
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
print(fcrpc.run("""import FreeCADGui
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
print(1)"""))
PY
sleep 2
DOC=hook_plain
B() { python3 -m lab.button "$@" 2>>"$O/lab-query.err"; }
row() { python3 -m lab.fcrpc row "$DOC" "$1" 2>>"$O/lab-query.err"; }
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
sl_click 45 36 "File menu"
sl_glide 160 110 15; sl_nap 0.4
sl_click 160 110 "File: Open"
sl_nap 2.0
sl_type "~/hook-plain.FCStd" "open: typed the file name" 90
sl_key Return "open: Enter"
sl_nap 3.0
xdotool mousemove 1500 1300; sl_key 6 "key 6: the back"; sl_key v "key V"; sl_key f "key F (fit all)"; sl_nap 2.0
sl_shot "$O/s1-back20.png"
read -r SX SY < <(row Spreadsheet)
dbl "$SX" "$SY" "tree: double-click Spreadsheet"
sl_nap 3.0
sl_click 700 36 "Windows menu"
sl_glide 706 165 15; sl_nap 0.5
sl_click 706 165 "Windows: Tile"
sl_nap 2.5
sl_click 2420 838 "the sheet: an empty cell"
sl_nap 0.8
sl_click 2060 676 "cell B5 (width)"
sl_nap 0.8
sl_type "30 mm" "B5: typed 30 mm" 160
sl_key Return "B5: Enter (30 mm)"
sl_nap 3.5
sl_click 1100 1250 "the hook's window: an empty spot"
sl_nap 0.5
sl_key 6 "key 6: the back, 30 wide"; sl_key v "key V"; sl_key f "key F (fit all)"; sl_nap 2.5
sl_shot "$O/s2-back30.png"
read -r PX PY < <(row Fillet)
sl_click "$PX" "$PY" "tree: Fillet"
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line (30 wide)"
sl_mark "lab query: save width30"
python3 -m lab.fcrpc save "$DOC" /tmp/width30.FCStd > "$O/save.txt" 2>&1 && cp /tmp/width30.FCStd "$O/"
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
