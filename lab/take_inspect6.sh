#!/bin/bash
# Lesson 6 (no AI, free): a run's saved copy opened again in FreeCAD 1.1.4 (the Claude takes' window size and place)
# and our check filmed on it: key 0 V F; Tools > Measure, Distance, the plate's inside face, Ctrl + the lip's inside
# top edge. Used for run B1, whose in-run check picked the fillet's edge (48.00) before the aim fix; labelled "opened
# again" in the video.
#   FCC_PREFIX=fc6 tools/run.sh lab/take_inspect6.sh B1
set -u
RUN=${1:-B1}
. /lab/lab/common.sh
. /lab/lab/l6common.sh
O=/lab/out/l6/inspect-$RUN; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
cp "/lab/out/l6/runs/$RUN/after-hook_lesson5.FCStd" ~/hook-lesson5.FCStd
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 6
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 1
cd /lab
python3 -m lab.opendoc /home/maker/hook-lesson5.FCStd > "$O/opendoc.txt" 2>&1
python3 - > "$O/setup-rpc.txt" 2>&1 <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCAD, FreeCADGui
from PySide import QtWidgets
mw = FreeCADGui.getMainWindow()
FreeCADGui.activateWorkbench('PartDesignWorkbench')
for w in mw.findChild(QtWidgets.QMdiArea).subWindowList():
    if w.windowTitle().startswith('Start'):
        w.close()
d = FreeCAD.ActiveDocument
for o in d.Objects:
    if o.TypeId == 'PartDesign::Body' or o.Name == 'Fillet':
        o.ViewObject.Visibility = True
FreeCADGui.activeDocument().activeView().viewIsometric()
FreeCADGui.SendMsgToActiveView('ViewFit')
print('ok')"""))
PY
sleep 2
xdotool mousemove 2000 700
sl_record "$O"
sl_mark "recording started: run $RUN's saved hook, opened again"
sl_nap 1.5
m6_view
m6_opening "$O/our-measure.txt" 5.0
sl_shot "$O/s1-ourcheck.png"
m6_close
sl_mark "recording stopped"
sl_stop
fc_quit; sl_display_stop
echo "inspect done ($RUN): $(cat "$O/our-measure.txt")"; grep -c "aim:" "$O/events.jsonl"
