#!/bin/bash
# Lesson 6 take "hand" (PLAN-L6 by-hand frames F4, F6, F8, F17-F19; lab L6-Q1, L6-Q2): lesson 5's hook (hook-lesson5.FCStd =
# lesson 4's by-hand width30: hook_depth 40, width 30, the opening 30) in FreeCAD 1.1.4, Part Design.
# Filmed: key 0 V F; Tools > Measure, Distance, the plate's inside face, Ctrl + the lip's inside top edge (30.00);
# Close; the Spreadsheet double-clicked; Windows > Tile; the sheet's B1 (hook_depth 40); 45 mm, Enter; Measure again
# (35.00); 55 mm; Measure (45.00); Measure Radius on a hole's rim (2.00) and on the small curve at the lip's end
# (2.00); the Fillet row; the volume line (17098.58).
# Not filmed (logged "lab query" events): a copy saved and read (checker/l6read) at 40, 45 and 55.
#   FCC_PREFIX=fc6 tools/run.sh lab/take_hand6.sh
set -u
. /lab/lab/common.sh
. /lab/lab/l6common.sh
O=/lab/out/l6/hand; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
cp /lab/out/l4/hand/width30.FCStd ~/hook-lesson5.FCStd
md5sum ~/hook-lesson5.FCStd > "$O/start.md5"
sl_display $W $H
fc_start "$O/app.log" 1.8; sleep 8
cd /lab
python3 - > "$O/setup-rpc.txt" 2>&1 <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCAD, FreeCADGui
from PySide import QtCore, QtWidgets
mw = FreeCADGui.getMainWindow()
FreeCAD.openDocument('/home/maker/hook-lesson5.FCStd')
FreeCADGui.activateWorkbench('PartDesignWorkbench')
for w in mw.findChildren(QtWidgets.QMdiArea)[0].subWindowList():
    if w.windowTitle().startswith('Start'):
        w.close()
for w in mw.findChildren(QtWidgets.QDockWidget):
    if w.objectName() in ('Python console',):
        w.show()
        mw.resizeDocks([w], [190], QtCore.Qt.Vertical)
        w.widget().clear()
FreeCADGui.runCommand('Std_Measure')
QtWidgets.QApplication.processEvents()
for c in mw.findChildren(QtWidgets.QCheckBox):
    if c.isVisible() and c.text().replace('&', '').startswith('Show Delta'):
        c.setChecked(False)
FreeCADGui.Control.closeDialog()
FreeCADGui.activeDocument().activeView().viewIsometric()
FreeCADGui.SendMsgToActiveView('ViewFit')
print(1)"""))
PY
sleep 2
DOC=hook_lesson5
B() { python3 -m lab.button "$@" 2>>"$O/lab-query.err"; }
row() { python3 -m lab.fcrpc row "$DOC" "$1" 2>>"$O/lab-query.err"; }
dbl() { sl_glide "$1" "$2" 20; sl_nap 0.5; sl_mark "$3"; xdotool click --repeat 2 --delay 120 1; }
console() {   # console "line" LABEL
  local cx cy; read -r cx cy < <(B console)
  sl_click "$cx" "$cy" "console: click"
  sl_type "$1" "console: typed $2" 70
  sl_key Return "console: Enter ($2)"
  sl_nap 3.5
}
snap() {
  sl_mark "lab query: save and read $1"
  python3 -m lab.fcrpc save "$DOC" "/tmp/$1.FCStd" > "$O/save-$1.txt" 2>&1 && cp "/tmp/$1.FCStd" "$O/$1.FCStd"
  FC_DOC="/tmp/$1.FCStd" FC_OUT="$O/read-$1.json" freecadcmd /lab/checker/l6read.py > "$O/read-$1.log" 2>&1
}
setcell() {   # setcell VALUE: B1 (hook_depth) in the tiled sheet
  local ex ey wx wy
  read -r ex ey < <(B cell 12 3); sl_click "$ex" "$ey" "the sheet: an empty cell (the window takes the keys)"
  sl_nap 0.6
  read -r wx wy < <(B cell 0 1); sl_click "$wx" "$wy" "cell B1 (hook_depth)"
  sl_nap 0.8
  sl_type "$1 mm" "B1: typed $1 mm" 160
  sl_key Return "B1: Enter ($1 mm)"
  sl_nap 3.0
}
xdotool mousemove 1500 700
snap depth40
sl_record "$O"
sl_mark "recording started: lesson 5's hook in FreeCAD 1.1.4"
sl_nap 2.0
# F4: the opening, measured
m6_view
sl_shot "$O/s1-corner.png"
m6_opening "$O/result-40.txt" 5.0
sl_shot "$O/s2-measure30.png"
m6_close
# F6: the sheet, Tile, hook_depth 40 -> 45
read -r PX PY < <(row Spreadsheet)
dbl "$PX" "$PY" "tree: double-click Spreadsheet"
sl_nap 2.5
read -r MX MY < <(B menu Windows)
sl_click "$MX" "$MY" "Windows menu"
sl_glide $((MX + 5)) 165 15; sl_nap 0.5
sl_click $((MX + 5)) 165 "Windows: Tile"
sl_nap 2.5
read -r WX WY < <(B cell 0 1); sl_glide "$WX" "$WY" 20; sl_mark "hover: B1 hook_depth 40 mm"; sl_nap 3.0
sl_shot "$O/s3-tiled.png"
setcell 45
m6_view
m6_opening "$O/result-45.txt" 5.0
sl_shot "$O/s4-measure35.png"
m6_close
snap depth45
# F8: 55
setcell 55
m6_view
m6_opening "$O/result-55.txt" 5.0
sl_shot "$O/s5-measure45.png"
m6_close
snap depth55
# F17-F18: Radius on a hole's rim, on the small curve at the lip's end
m6_radius hole "$O/result-hole.txt" 5.0
sl_shot "$O/s6-hole.png"
m6_close
m6_radius round "$O/result-round.txt" 5.0
sl_shot "$O/s7-round.png"
m6_close
# F19: the Fillet row, the volume line
read -r PX PY < <(row Fillet)
sl_click "$PX" "$PY" "tree: Fillet"
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line (hook_depth 55)"
sl_shot "$O/s8-volume.png"
read -r WX WY < <(B cell 0 1); sl_glide "$WX" "$WY" 20; sl_mark "hover: B1 hook_depth 55 mm"; sl_nap 3.0
sl_shot "$O/s9-sheet55.png"
sl_mark "recording stopped"
sl_stop
fc_quit; sl_display_stop
for s in depth40 depth45 depth55; do
  python3 -m checker.score_l6 "$O/read-$s.json" > "$O/score-$s.json" 2>&1
done
echo "hand take done"; cat "$O"/result-*.txt; python3 -c "
import json
for s in ('depth40', 'depth45', 'depth55'):
    d = json.load(open('$O/score-%s.json' % s)); print(s, d['pass'], d['opening_mm'], d['volume_mm3'], [k for k, v in d['lines'].items() if not v])"
