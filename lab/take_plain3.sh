#!/bin/bash
# Lesson 3 take "plain" (PLAN-L3 F18, watch only; lab L3-Q3): lesson 2's hook with plain typed sizes (no spreadsheet),
# its bottom 25 changed to 40 directly. FreeCAD 1.1.4, Part Design, the start file already open (lesson 3's own take
# films File > Open). Filmed: the sketch double-clicked; one notch out; the arm's top line (no size of its own)
# pointed at; the 25 double-clicked, 40 typed, Enter; the arm's top line pointed at again (now 30); Close; key 0; the
# Pad clicked; the volume line and the X line. Not filmed: a copy saved and measured.
#   tools/run.sh lab/take_plain3.sh
set -u
. /lab/lab/common.sh
O=/lab/out/l3/plain; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
cp /lab/out/l2/hand/hand.FCStd ~/hook-lesson2.FCStd
sl_display $W $H
fc_start "$O/app.log" 1.8; sleep 8
cd /lab
python3 - > "$O/setup-rpc.txt" 2>&1 <<'PY'
import sys, os; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCAD, FreeCADGui
from PySide import QtWidgets
FreeCAD.openDocument(%r)
FreeCADGui.activateWorkbench('PartDesignWorkbench')
FreeCADGui.activeDocument().activeView().viewIsometric()
FreeCADGui.SendMsgToActiveView('ViewFit')
mdi = FreeCADGui.getMainWindow().findChild(QtWidgets.QMdiArea)
for w in mdi.subWindowList():
    if w.windowTitle().startswith('Start'):
        w.close()
for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
    if w.objectName() in ('Python console',):
        w.show()
print(1)""" % os.path.expanduser('~/hook-lesson2.FCStd')))
PY
sleep 2
DOC=hook_lesson2
xdotool mousemove 1500 700
row() { python3 -m lab.fcrpc row "$DOC" "$1" 2>>"$O/lab-query.err"; }
for i in 1 2 3; do
  read -r AX AY < <(python3 -m lab.fcrpc arrow "$DOC" Sketch 2>>"$O/lab-query.err")
  { [ "${AX:-}" = open ] || [ "${AX:-}" = none ] || [ -z "${AY:-}" ]; } && break
  xdotool mousemove "$AX" "$AY" click 1; sleep 0.6
done
sl_record "$O"
sl_mark "recording started: lesson 2's plain hook (no spreadsheet)"
sl_nap 1.5
read -r KX KY < <(row Sketch)
sl_glide "$KX" "$KY" 20; sl_nap 0.5
sl_mark "tree: double-click the sketch"; xdotool click --repeat 2 --delay 120 1
sl_nap 3.5
sl_click 940 88 "Fit all (toolbar)"
sl_nap 1.2
read -r X0 Y0 < <(python3 -m lab.sketchpt "$DOC" Sketch 0 start); read -r X1 Y1 < <(python3 -m lab.sketchpt "$DOC" Sketch 0 end)
read -r X6 Y6 < <(python3 -m lab.sketchpt "$DOC" Sketch 6 end)
CX=$(( (X0 + X1) / 2 )); CY=$(( (Y0 + Y6) / 2 ))
sl_glide "$CX" "$CY" 15; sl_mark "pan: middle drag (the hook to the middle)"; xdotool mousedown 2
for i in $(seq 1 20); do xdotool mousemove $(( CX + (1330 - CX) * i / 20 )) $(( CY + (810 - CY) * i / 20 )); sleep 0.03; done
xdotool mouseup 2; sl_nap 0.5
for n in 1 2 3; do xdotool click 4; sleep 0.4; done; sl_mark "zoom: three notches in (the wheel)"
sl_nap 1.5
read -r LX LY < <(python3 -m lab.sketchpt "$DOC" Sketch 4 mid)
sl_glide "$LX" "$LY" 20; sl_mark "hover: the arm's top line (no size)"; sl_nap 2.5
sl_shot "$O/s1-arm-top.png"
read -r DX DY < <(python3 -m lab.dimpt "$DOC" Sketch 17)
sl_glide "$DX" "$DY" 20; sl_mark "hover size: 25 bottom"; sl_nap 0.8
sl_mark "double-click size: 25 bottom"; xdotool click --repeat 2 --delay 120 1
sl_nap 1.6
sl_type "40" "Insert Length: typed 40" 220
sl_nap 0.8
sl_key Return "Insert Length: Enter (OK)"
sl_nap 2.5
read -r LX LY < <(python3 -m lab.sketchpt "$DOC" Sketch 4 mid)
sl_glide "$LX" "$LY" 20; sl_mark "hover: the arm's top line (now 30)"; sl_nap 2.5
sl_shot "$O/s2-forty.png"
sl_glide 2440 754 25; sl_mark "hover: Fully constrained"; sl_nap 2.0
sl_click 2528 616 "Close"
sl_nap 2.5
xdotool mousemove 1500 1200; sl_key 0 "key 0: isometric"; sl_nap 1.0
sl_key v "key V"; sl_key f "key F (fit all)"; sl_nap 1.5
read -r PX PY < <(row Pad)
sl_click "$PX" "$PY" "tree: Pad"
sl_click 900 1722 "console: click"
sl_type "Gui.Selection.getSelection()[0].Shape.Volume" "console: typed the volume line" 70
sl_key Return "console: Enter (volume)"
sl_nap 3.0
sl_type "b = Gui.Selection.getSelection()[0].Shape.BoundBox; round(b.XMin, 3), round(b.XMax, 3)" "console: typed the X line" 70
sl_key Return "console: Enter (X)"
sl_nap 3.5
sl_shot "$O/s3-console.png"
sl_mark "recording stopped"
sl_stop
python3 -m lab.fcrpc save "$DOC" /tmp/plain40.FCStd > "$O/save.txt" 2>&1 && cp /tmp/plain40.FCStd "$O/plain40.FCStd"
FC_DOC=/tmp/plain40.FCStd FC_OUT="$O/measure-plain40.json" freecadcmd /lab/checker/measure.py > "$O/measure.log" 2>&1
fc_quit; sl_display_stop
echo "plain take done"; head -c 300 "$O/measure-plain40.json"
