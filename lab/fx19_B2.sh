#!/bin/bash
# fx19 take B pickup (B2): take B's last step re-filmed on B's own saved document (B/B-fixed.FCStd): the Pad clicked;
# View, Panels, Python console; the lesson-1 volume line. (In take B the console docked as a hidden tab beside the
# Report view, so the click missed: DEVIATIONS.)
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh
O=$X/B2; mkdir -p $O; L=$O/take.log; : > $L
fx_start $O
mkdir -p /tmp/fx19; cp $X/B/B-fixed.FCStd /tmp/fx19/hook-gap.FCStd
open_doc /tmp/fx19/hook-gap.FCStd >> $L 2>&1
Q "import FreeCADGui; FreeCADGui.activeDocument().activeView().viewIsometric(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L 2>&1
report_hide; sleep 1
read -r PX PY < <(row_open hook_gap Pad); echo "Pad row $PX $PY" >> $L
xdotool mousemove 1500 800
sl_record "$O"; sl_mark "recording started: take B's fixed hook (saved at the end of take B), isometric"
sl_nap 3
clk "$PX $PY" "tree: Pad"; sl_nap 1.2
console_line $O "Gui.Selection.getSelection()[0].Shape.Volume"
SL_SHOT_WAKE=0 sl_shot $O/volume.png
sl_mark "recording stopped"; sl_stop
Q "import FreeCAD; p = FreeCAD.getDocument('hook_gap').getObject('Pad'); print('READ', p.isValid(), p.Shape.Volume)" >> $L 2>&1
fc_quit; sl_display_stop; echo "B2 done"
