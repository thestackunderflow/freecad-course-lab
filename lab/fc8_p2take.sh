#!/bin/bash
# video D probe P2 takes (FreeCAD 1.1.4 by hand, no AI), take D's recipe (lab/fc8_take.sh):
#   FCC_PREFIX=fc8 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fc8_p2take.sh P2F|P2T
#   P2F  gap01: Params gap 0.1 -> 0.2, Recompute, Measure left + right; gap 0.3, Recompute, Measure left + right; then
#        Measure on the two whole bodies picked in the tree (Hook, Ctrl + Rail): what the panel shows       F3 F14 (S2)
#   P2T  typo: Measure left + right with the same picks (the sign check)
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc8_lib.sh
T=$1; O=$X/P2/$T; mkdir -p $O; L=$O/take.log; : > $L
case $T in P2F) F=gap01;; P2T) F=typo;; *) echo "take P2F|P2T"; exit 2;; esac
fx_start $O
mkdir -p /tmp/fc8; cp /lab/out/fc8/P/fc8-$F.FCStd /tmp/fc8/$F.FCStd
open_doc /tmp/fc8/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1
Q "import FreeCADGui
FreeCADGui.activateWorkbench('PartDesignWorkbench')
FreeCADGui.getDocument('$F').activeView().setAnimationEnabled(False)
print(1)" >> $L 2>&1
report_hide; sleep 2; xdotool mousemove 1500 1500; rv_clear
m() {   # m SIDE RIB_Y SLOT_Y TAG: take D's Measure (bottom view, zoom, slot edge, Ctrl + rib edge), then Close
  local p i
  sl_glide 1500 1200 15; sl_key 5 "key 5: bottom view"; sl_nap 1
  Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewBottom(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L
  sl_mark "(view fitted)"; sl_nap 2
  p=$(vp -5.5 "$2" 0); sl_glide ${p% *} ${p#* } 25; sl_nap 0.6
  for i in $(seq 1 ${ZOOMS:-14}); do xdotool click ${ZOOMB:-4}; sleep 0.18; done; sl_mark "wheel: zoom on the $1 wall"; sl_nap 1.5
  p=$(vp -5.5 "$3" 0 -5.5 "$2" 0); echo "$4 $1 edges $p" >> $L; local tag=$4; set -- "$1" $p
  btn Std_Measure "Measure"; sl_nap 2
  sl_glide $2 $3 25; sl_nap 0.8; sl_click $2 $3 "$1: the slot's wall edge"; sl_nap 1.5
  sl_glide $4 $5 25; sl_nap 0.8; xdotool keydown ctrl; sl_click $4 $5 "$1: Ctrl + the rib's wall edge"; xdotool keyup ctrl
  sl_nap 3.5
  echo "$tag $1 measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*' | tr '\n' ' ')" >> $L
  shot $O/measure-$tag-$1.png; sl_nap 2
  at "$(taskpos any Close)" "Measure: Close"; sl_nap 1.5
}
setgap() {  # setgap VALUE: double-click Params, cell B3, type, Enter, Recompute, back to the 3D tab
  local p c t
  p=$(ROW $F Params); sl_glide ${p% *} ${p#* } 20; sl_nap 0.5
  sl_mark "double-click: open Params"; xdotool click --repeat 2 --delay 120 1; sl_nap 3
  c=$(B cell 2 1); echo "gap cell $c" >> $L
  at "$c" "cell B3: gap"; sl_nap 1
  sl_type "$1" "typed $1" 250; sl_key Return "Enter"; sl_nap 1.5
  btn Std_Refresh "Recompute"; sl_nap 3
  t=$(B tab "$F"); echo "3D tab $t" >> $L; at "$t" "tab: back to the 3D view"; sl_nap 2
  echo "gap $1: $(FQ "common_of('$F', 'Hook', 'Rail')")" >> $L
}
xdotool mousemove 1500 1500
sl_record "$O"; sl_mark "recording started: FreeCAD 1.1.4, $F.FCStd open"
sl_nap 3
if [ $T = P2F ]; then
  setgap 0.2; m left -16 -16.2 g02; m right -4 -3.8 g02
  setgap 0.3; m left -16 -16.3 g03; m right -4 -3.7 g03
  Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewIsometric(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L
  sl_mark "(iso view)"; sl_nap 1.5
  sl_click 1500 1500 "empty space: nothing selected"; sl_nap 1
  rowclk $F Hook "tree: Hook (the whole body)"; rowclk $F Rail "tree: Ctrl + Rail (the whole body)" ctrl; sl_nap 1
  btn Std_Measure "Measure (two whole bodies selected)"; sl_nap 3.5
  echo "whole measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*' | tr '\n' ' ')" >> $L
  FQ "task_texts()" > $O/whole-task-texts.json 2>&1
  shot $O/measure-whole.png; sl_nap 3
else
  m left -16 -15.8 typo; m right -4 -4.2 typo
fi
sl_nap 2; sl_stop
lab_save $F $O/end.FCStd >> $L 2>&1
echo "TAKE $T DONE" >> $L
fc_quit; sl_display_stop
check_doc $O/end.FCStd $O/check.json >> $L
