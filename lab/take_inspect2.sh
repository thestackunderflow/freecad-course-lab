#!/bin/bash
# Lesson 2 take "inspect" (PLAN-L2 F26, F29; lab L2-Q7), free, no AI: run 1's own saved document (Claude's part,
# runs/claude-1/claude.FCStd, as Claude left it) opened in FreeCAD 1.1.4 at the by-hand take's size, then a viewer's
# checks: the pad clicked, lesson 1's volume line and the height line; Claude's sketch opened (double-click), its
# Sketcher message; a corner dragged (with no size pins, it stretches) and the drag undone. Nothing is saved.
# (Run 1's filmed viewer steps were spoiled by a lab-query error dialog, so they are filmed here instead.)
#   tools/run.sh lab/take_inspect2.sh [RUN]
set -u
. /lab/lab/common.sh
RUN=${1:-claude-1}
O=/lab/out/l2/inspect; rm -rf "$O"; mkdir -p "$O"
cp "/lab/out/l2/runs/$RUN/claude.FCStd" /tmp/claude.FCStd
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
sl_display $W $H
fc_start "$O/app.log" 1.8; sleep 8
cd /lab
python3 - > "$O/setup-rpc.txt" 2>&1 <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCAD, FreeCADGui
from PySide import QtWidgets
FreeCAD.openDocument('/tmp/claude.FCStd')
FreeCADGui.activateWorkbench('PartDesignWorkbench')
FreeCADGui.activeDocument().activeView().viewIsometric()
FreeCADGui.SendMsgToActiveView('ViewFit')
for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
    if w.objectName() in ('Python console',):
        w.show()
def walk(it):
    it.setExpanded(it.text(0) != 'Origin')
    for i in range(it.childCount()):
        walk(it.child(i))
for t in FreeCADGui.getMainWindow().findChildren(QtWidgets.QTreeWidget):
    try:
        if t.isVisible():
            for i in range(t.topLevelItemCount()):
                walk(t.topLevelItem(i))
    except Exception as e:
        print('skip', e)
print('ok')"""))
PY
sleep 2
PX=164; PY=406; KX=200; KY=438   # the rows as in the by-hand take: claude, Body, Origin (closed), Pad, Sketch
echo "pad $PX $PY sketch $KX $KY" > "$O/rows.txt"
xdotool mousemove 1500 700
sl_record "$O"
sl_mark "recording started: run 1's document (Claude's part), opened again, no AI"
sl_nap 2.0
sl_click "$PX" "$PY" "tree: Claude's pad"
sl_nap 1.5
sl_click 900 1722 "console: click"
sl_type "Gui.Selection.getSelection()[0].Shape.Volume" "console: typed the volume line" 85
sl_key Return "console: Enter"
sl_nap 3.5
sl_type "b = Gui.Selection.getSelection()[0].Shape.BoundBox; round(b.ZMin, 3), round(b.ZMax, 3)" "console: typed the height line" 70
sl_key Return "console: Enter 2"
sl_nap 4.0
sl_shot "$O/s1-console.png"
sl_glide "$KX" "$KY" 25; sl_nap 0.5
sl_mark "tree: double-click Claude's sketch"; xdotool click --repeat 2 --delay 120 1
sl_nap 3.0
sl_click 942 88 "Fit all"
sl_nap 2.5
sl_shot "$O/s2-sketch.png"
sl_glide 2440 754 25; sl_mark "hover: Claude's degrees of freedom"; sl_nap 3.0
read -r CX CY < <(python3 -m lab.sketchpt claude Sketch 5 end)
sl_glide "$CX" "$CY" 25; sl_nap 0.6
sl_mark "drag Claude's corner: down"; xdotool mousedown 1; sleep 0.2
for i in $(seq 1 30); do xdotool mousemove $((CX + i * 6)) $((CY + i * 4)); sleep 0.04; done
sl_mark "drag Claude's corner: stretched"; sl_nap 2.0
sl_shot "$O/s3-stretched.png"
xdotool mouseup 1; sl_mark "drag Claude's corner: released"
sl_nap 1.5
sl_key ctrl+z "Ctrl+Z: undo the drag"
sl_nap 2.5
sl_shot "$O/s4-undone.png"
sl_mark "recording stopped"
sl_stop
fc_quit; sl_display_stop
echo "inspect take done"; cat "$O/rows.txt"
