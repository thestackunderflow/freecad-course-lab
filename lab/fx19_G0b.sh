#!/bin/bash
# fx19 G0b (LAB-fx19 section 1, GUI probe): stills only, no recording, no AI. FreeCAD 1.1.4 on Xvfb opens
# P/hook-gap.FCStd; the sketch selected; Part Design, Pad; 20; OK; stills + every visible text (g0bdump.py); then the
# Sketch menu, Validate sketch, Highlight Troublesome Vertices; stills + texts.
#   FCC_PREFIX=fx19 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fx19_G0b.sh
set -u
. /lab/lab/common.sh
O=/lab/out/fx19/G0; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
cp /lab/out/fx19/P/hook-gap.FCStd /tmp/hook-gap.FCStd
sl_display $W $H
fc_start "$O/g0b-app.log" 1.8; sleep 8
cd /lab
Q() { timeout 20 python3 -c "import sys; sys.path.insert(0,'/lab'); from lab import fcrpc; print(fcrpc.run(sys.argv[1]))" "$1"; }
B() { timeout 20 python3 -m lab.button "$@"; }
D() { timeout 25 python3 /lab/out/fx19/G0/g0bdump.py "$O/$1.json" > "$O/$1.txt" 2>&1 || echo "dump $1 failed/blocked" >> "$O/g0b-log.txt"; }
{
echo "env: display ${W}x${H} QT_SCALE 1.8"
Q "import FreeCAD, FreeCADGui
d = FreeCAD.openDocument('/tmp/hook-gap.FCStd')
for o in d.Objects:
    if o.TypeId in ('Sketcher::SketchObject', 'PartDesign::Body'):
        FreeCADGui.getDocument(d.Name).getObject(o.Name).Visibility = True
FreeCADGui.activateWorkbench('PartDesignWorkbench')
v = FreeCADGui.activeDocument().activeView(); v.viewFront(); FreeCADGui.SendMsgToActiveView('ViewFit')
from PySide import QtWidgets
for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
    if 'Report' in w.objectName(): w.show()
print(d.Name, [o.Name for o in d.Objects])"
} >> "$O/g0b-log.txt" 2>&1
sleep 2
sl_shot "$O/g0b-0-open.png"
Q "import FreeCADGui
FreeCADGui.Selection.clearSelection(); FreeCADGui.Selection.addSelection('hook_gap', 'Sketch')
print(FreeCADGui.Selection.getSelection())" >> "$O/g0b-log.txt" 2>&1
sleep 1
read -r PX PY < <(B PartDesign_Pad); echo "Pad button $PX $PY" >> "$O/g0b-log.txt"
sl_click "$PX" "$PY" "Pad"
sleep 3
sl_shot "$O/g0b-1-taskpanel.png"
D g0b-1-taskpanel
sl_type "20" "typed 20" 250
sleep 2
sl_shot "$O/g0b-2-length20.png"
D g0b-2-length20
read -r KX KY < <(B text OK); echo "OK button $KX $KY" >> "$O/g0b-log.txt"
sl_click "$KX" "$KY" "Pad: OK"
sleep 3
sl_shot "$O/g0b-3-after-ok.png"
D g0b-3-after-ok
echo "=== after OK" >> "$O/g0b-log.txt"; cat "$O/g0b-3-after-ok.txt" >> "$O/g0b-log.txt"
echo "G0B-PHASE1-DONE" >> "$O/g0b-log.txt"
# phase 2 (the dialog, if any, is closed with its own button by the next script run after the stills are read)
if [ -n "${PHASE2:-}" ]; then . /lab/lab/fx19_G0b2.sh; fi
sleep 1
tmux kill-server 2>/dev/null; fc_quit; sl_display_stop
echo "G0b done"
