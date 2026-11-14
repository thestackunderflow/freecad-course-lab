#!/bin/bash
# fx20 take D2 (pickup of D's last part): in D the terminal stayed over FreeCAD, so the red sketch never showed.
# FreeCAD alone, full window: hook-red opened, its sketch in edit (lab query), Fit, hold 10 s (F4 left). No AI.
#   FCC_PREFIX=fx20 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fx20_D2.sh
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh
O=$X/D2; mkdir -p $O; L=$O/take.log; : > $L
fx_start $O
mkdir -p /tmp/fx20; cp $X/P/hook-red.FCStd /tmp/fx20/hook_red.FCStd
open_doc /tmp/fx20/hook_red.FCStd >> $L 2>&1; sleep 1
Q "import FreeCADGui
FreeCADGui.getDocument('hook_red').setEdit('Sketch')
print('edit')" >> $L 2>&1; sleep 3
read -r FIT < <(B Std_ViewFitAll); [ "$FIT" = none ] && FIT="942 88"
xdotool mousemove ${FIT% *} ${FIT#* } click 1; sleep 2
report_hide; xdotool mousemove 1500 700; sleep 1
sl_record "$O"; sl_mark "recording started: hook-red's sketch in edit, Over-constrained (red), full window"
sl_nap 10
SL_SHOT_WAKE=0 sl_shot $O/red.png
sl_mark "recording stopped"; sl_stop
solver_text >> $L 2>&1
fc_quit; sl_display_stop
echo "D2 done"
