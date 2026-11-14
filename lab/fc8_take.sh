#!/bin/bash
# fc8 takes (LAB-fc8 "Takes"), FreeCAD 1.1.4 by hand, no AI. Recipes from G0 (out/fc8/G0/VERDICT.txt).
#   FCC_PREFIX=fc8 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fc8_take.sh A|B|C|D|E
#   A  typo: Part, select Hook + Rail, Intersection (slivers, red), Check Geometry > Shape Content (Volume)   F0 F9 S0
#   B  typo: New Assembly, Insert Rail (No) + Hook, hide bodies, Toggle Grounded, Slider (two components), drag up,
#      off the top, then down through the rail                                                               F4-F8
#   C  touch (gap 0): the same as A -> nothing shared                                                        F10 S1
#   D  touch: Params gap 0 -> 0.4, Recompute, bottom view, zoom, Measure left side, then right side          F12 F13 S2
#   E  gap04: the assembly steps, drag the hook up the whole rail and back                                   F15
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc8_lib.sh
T=$1; O=$X/$T; mkdir -p $O; L=$O/take.log; : > $L
case $T in A|B) F=typo;; C|D) F=touch;; E) F=gap04;; esac
case $T in A|C) WB=PartWorkbench;; *) WB=PartDesignWorkbench;; esac
fx_start $O
mkdir -p /tmp/fc8; cp /lab/out/fc8/P/fc8-$F.FCStd /tmp/fc8/$F.FCStd
open_doc /tmp/fc8/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1
Q "import FreeCADGui
FreeCADGui.activateWorkbench('$WB')
FreeCADGui.getDocument('$F').activeView().setAnimationEnabled(False)
print(1)" >> $L 2>&1
report_hide; sleep 2; xdotool mousemove 1500 1500; rv_clear

asm_steps() {  # New Assembly, Insert (Rail: No; Hook), OK, hide the bodies, Ground the rail, Slider by the two components
  Q "import FreeCADGui; FreeCADGui.activateWorkbench('AssemblyWorkbench'); print(1)" >> $L; sl_mark "workbench: Assembly"
  sl_nap 2
  btn Assembly_CreateAssembly "New Assembly"; sl_nap 2
  btn Assembly_Insert "Insert Component"; sl_nap 2.5
  at "$(taskpos row Rail)" "Insert: Rail"; sl_nap 2
  shot $O/ground-dialog.png
  sl_glide 1738 928 20; sl_nap 1.2; sl_click 1738 928 "dialog: ground the first part automatically? No"; sl_nap 1.5
  at "$(taskpos row Hook)" "Insert: Hook"; sl_nap 2
  at "2430 615" "Insert: OK"; sl_nap 2
  rowclk $F Hook "tree: Hook (the body)"; rowclk $F Rail "tree: Ctrl + Rail (the body)" ctrl
  sl_key space "Space: hide the two bodies (the components stay)"; sl_nap 1.5
  rowclk $F Rail001 "tree: Rail001"; sl_nap 0.5
  btn Assembly_ToggleGrounded "Toggle Grounded"; sl_nap 2
  sl_click 1500 1500 "empty space: nothing selected"; sl_nap 1
  btn Assembly_CreateJointSlider "Slider Joint"; sl_nap 2.5
  rowclk $F Rail001 "Slider: Rail001 (the whole component)"; sl_nap 1.5
  rowclk $F Hook001 "Slider: Ctrl + Hook001" ctrl; sl_nap 2.5
  shot $O/slider-panel.png
  at "2430 615" "Slider: OK"; sl_nap 2
  echo "hook z after slider $(hookz)" >> $L
  Q "import FreeCADGui; FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L; sl_nap 1
}

dragz() {      # dragz DZ STEPS LABEL: drag the hook by about DZ mm along the rail (grab the arm's top)
  Q "import FreeCADGui; FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L; sl_mark "(view fitted)"; sl_nap 1
  local z p; z=$(hookz); p=$(vp 15 -10 "$(awk -v z=$z 'BEGIN{print z+5}')" 15 -10 "$(awk -v z=$z -v d=$1 'BEGIN{print z+5+d}')")
  set -- $p "$2" "$3"
  drag3d $1 $2 $3 $4 $5 "$6"
  echo "$6: hook z $(hookz) $(FQ "common_of('$F', 'Hook001', 'Rail001')")" >> $L
}

xdotool mousemove 1500 1500
sl_record "$O"; sl_mark "recording started: FreeCAD 1.1.4, $F.FCStd open"
sl_nap 3
case $T in
A|C)
  rowclk $F Hook "tree: Hook"; rowclk $F Rail "tree: Ctrl + Rail" ctrl; sl_nap 1
  btn Part_Common "Intersection"; sl_nap 3
  Q "import FreeCAD, FreeCADGui
FreeCADGui.getDocument('$F').getObject('Common').ShapeAppearance = [FreeCAD.Material(DiffuseColor=(0.9, 0.1, 0.1))]
print(1)" >> $L
  sl_click 1500 1500 "empty space"; sl_nap 3
  rowclk $F Common "tree: Common"; sl_nap 1
  btn Part_CheckGeometry "Check Geometry"; sl_nap 2.5
  at "$(taskpos any 'Expand shape content')" "tick: Expand shape content"; sl_nap 1
  at "$(taskpos any 'Run check')" "Run check"; sl_nap 3
  at "$(taskpos any 'Check Geometry Results')" "Check Geometry Results: fold"; sl_nap 1.5
  at "$(taskpos any 'Shape Content')" "Shape Content: open"; sl_nap 3
  shot $O/shape-content.png; sl_nap 3
  sl_click 1000 1500 "empty space: the result's own colour"; sl_nap 4
  shot $O/end-colour.png
  Q "import FreeCADGui
from PySide import QtWidgets
print([w.toPlainText() for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QTextEdit) if 'Volume' in w.toPlainText()])" > $O/shape-content.txt 2>&1
  ;;
B|E)
  asm_steps
  if [ $T = B ]; then
    dragz 60 50 "drag the hook up the rail"; dragz 40 30 "drag it off the top"; sl_nap 1.5
    dragz -80 70 "drag it back down onto the rail"; sl_nap 3
  else
    dragz 85 80 "drag the hook up the whole rail"; sl_nap 1.5; dragz -85 80 "and back down"; sl_nap 3
  fi
  ;;
D)
  p=$(ROW $F Params); sl_glide ${p% *} ${p#* } 20; sl_nap 0.5
  sl_mark "double-click: open Params"; xdotool click --repeat 2 --delay 120 1; sl_nap 3
  c=$(B cell 2 1); echo "gap cell $c" >> $L
  at "$c" "cell B3: gap = 0"; sl_nap 1
  sl_type "0.4" "typed 0.4" 250; sl_key Return "Enter"; sl_nap 1.5
  btn Std_Refresh "Recompute"; sl_nap 3
  t=$(B tab "$F"); echo "3D tab $t" >> $L; at "$t" "tab: back to the 3D view"; sl_nap 2
  m() {   # m SIDE RIB_Y SLOT_Y: bottom view, zoom on the head wall with the wheel, Measure, slot edge, Ctrl + rib edge
    local p i
    sl_glide 1500 1200 15; sl_key 5 "key 5: bottom view"; sl_nap 1
    Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewBottom(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L
    sl_mark "(view fitted)"; sl_nap 2
    p=$(vp -5.5 "$2" 0); sl_glide ${p% *} ${p#* } 25; sl_nap 0.6
    for i in $(seq 1 ${ZOOMS:-14}); do xdotool click ${ZOOMB:-4}; sleep 0.18; done; sl_mark "wheel: zoom on the $1 wall"; sl_nap 1.5
    p=$(vp -5.5 "$3" 0 -5.5 "$2" 0); echo "$1 edges $p" >> $L; set -- "$1" $p
    btn Std_Measure "Measure"; sl_nap 2
    sl_glide $2 $3 25; sl_nap 0.8; sl_click $2 $3 "$1: the slot's wall edge"; sl_nap 1.5
    sl_glide $4 $5 25; sl_nap 0.8; xdotool keydown ctrl; sl_click $4 $5 "$1: Ctrl + the rib's wall edge"; xdotool keyup ctrl
    sl_nap 3.5
    echo "$1 measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*' | tr '\n' ' ')" >> $L
    shot $O/measure-$1.png; sl_nap 2
  }
  m left -16 -16.4
  at "$(taskpos any Close)" "Measure: Close"; sl_nap 1.5
  m right -4 -3.6
  ;;
esac
sl_nap 2; sl_stop
lab_save $F $O/end.FCStd >> $L 2>&1
echo "TAKE $T DONE" >> $L
fc_quit; sl_display_stop
check_doc $O/end.FCStd $O/check.json >> $L
