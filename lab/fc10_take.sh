#!/bin/bash
# fc10 takes (PLAN 4.2), FreeCAD 1.1.4 by hand, no AI. Recipes from G0 (out/fc10/G0/VERDICT.txt).
#   FCC_PREFIX=fc10 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fc10_take.sh A|B|P|C|D
#   A  trap: unpinned @60; full window; Params plate_height 60 -> 80; Recompute; front view (fixed camera); Measure the
#      top back corner and the bottom back corner (Position, signed z); right view on the screw hole           F0 F7 S0
#   B  pinned demo: pinned @60; the same change, the same Measures; right view; HookSketch opened, message held  F1 S2
#   P  pickup: unpinned @60; Params rows; HookSketch opened, rule marks, message held, its link clicked
#      (every corner selected), origin held                                                                F3 F4 F5 F6
#   C  fix: unpinned @60; HookSketch; a small box dragged around the bottom back corner (selects the corner AND the
#      origin, G0 Q4: a Ctrl-click on the same spot deselects); Coincident Constraint (tooltip held); "Fully
#      constrained"; Close; Params 80; Recompute; front view; Measure top + bottom; right view          F9 F10 F11 S2
#   D  proof: C's end file (pinned @80); HookSketch; drag the back line (nothing moves); Close; Params 100;
#      Recompute; front view; Measure top + bottom; right view                                                 F13
#   T  T2 nudge with the stake (PLAN 2.4 branch "T1 >= 1 mm but the stake not visible", take A: 1.32 mm): unpinned
#      @60; HookSketch; one drag on the back line, mostly down (a slip); Close; front view; Measure top + bottom;
#      right view on the hole                                                                       F0 S0 (fallback)
#   TB the same drag on the pinned copy @60: nothing moves                                             F1 S2 (fallback)
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh
T=$1; O=$X/$T; mkdir -p $O; L=$O/take.log; : > $L
case $T in A|P|C|T) SRC=$X/P/hook-unpinned.FCStd;; B|TB) SRC=$X/P/hook-pinned.FCStd;; D) SRC=$X/C/end.FCStd;;
  *) echo "A|B|P|C|D|T|TB"; exit 2;; esac
F=hook
fx_start $O
mkdir -p /tmp/fc10; cp "$SRC" /tmp/fc10/$F.FCStd
open_doc /tmp/fc10/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1
Q "import FreeCADGui
FreeCADGui.getDocument('$F').activeView().setAnimationEnabled(False)
print(1)" >> $L 2>&1
report_hide; sleep 2; xdotool mousemove 1500 1500; rv_clear
echo "start: $(live $F)" >> $L

ROW() {       # the tree row, asked up to 6 times (the tree fills a little after the file opens)
  local p i
  for i in 1 2 3 4 5 6; do
    p=$(cd /lab && timeout 20 python3 -m lab.fcrpc row "$@" 2>/dev/null)
    [ -n "$p" ] && [ "$p" != none ] && { echo "$p"; return 0; }
    sleep 2
  done
  echo none
}
bail() { echo "BAIL: $1" >> $L; sl_stop; fc_quit; sl_display_stop; exit 1; }
dblrow() {     # dblrow OBJ LABEL: double-click a tree row
  local p; p=$(ROW $F "$1"); [ "$p" != none ] || bail "no row $1"
  sl_glide ${p% *} ${p#* } 20; sl_nap 0.5
  sl_mark "$2"; xdotool click --repeat 2 --delay 120 1; sl_nap 3
}
cam() {        # cam VIEW KEY CX CY CZ HEIGHT: the standard view key a person presses, then the lab's fixed camera
  sl_glide 1500 1200 15; sl_key $2 "key $2: $1 view"; sl_nap 0.5
  FQ "look('$F', '$1', $3, $4, $5, $6)" >> $L; sl_mark "(view set: $1 centred $3 $4 $5, $6 mm tall)"; sl_nap 2
}
isofit() {
  sl_key 0 "key 0: isometric"; sl_nap 0.5
  Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewIsometric(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L
  sl_mark "(view fitted)"; sl_nap 2
}
setheight() {  # setheight VALUE: Params cell B1 (plate_height) -> VALUE, Enter, Recompute, back to the 3D tab
  dblrow Params "double-click: open Params"
  local c; c=$(B cell 0 1); echo "plate_height cell $c" >> $L
  sl_glide ${c% *} ${c#* } 20; sl_mark "hover: plate_height"; sl_nap 1.5
  sl_click ${c% *} ${c#* } "cell B1: plate_height"; sl_nap 1
  sl_type "$1" "typed $1" 250; sl_key Return "Enter"; sl_nap 1.5
  shot $O/params-$1.png
  btn Std_Refresh "Recompute"; sl_nap 3
  local t; t=$(B tab "$F"); echo "3D tab $t" >> $L; at "$t" "tab: back to the 3D view"; sl_nap 2
  echo "after $1: $(live $F nosolve)" >> $L
}
mpos() {       # mpos NAME X Y Z: Measure, one click on the body's corner at (X, Y, Z): Position (signed)
  local p; p=$(vp "$2" "$3" "$4"); echo "$1 corner at $p" >> $L
  btn Std_Measure "Measure"; sl_nap 2
  sl_glide ${p% *} ${p#* } 25; sl_nap 0.8; sl_click ${p% *} ${p#* } "$1: corner"; sl_nap 3.5
  echo "$1 measure: $(Q "import FreeCADGui
from PySide import QtWidgets
out = []
for d in FreeCADGui.getMainWindow().findChildren(QtWidgets.QWidget):
    if d.metaObject().className() == 'Gui::TaskView::TaskView' and d.isVisible():
        out += [w.text() for w in d.findChildren(QtWidgets.QLineEdit) if w.isVisible()]
print(' | '.join(out))")" >> $L
  shot $O/measure-$1.png; sl_nap 2
  at "$(taskpos any Close)" "Measure: Close"; sl_nap 1.5
}
front_measures() {   # the front view on the back line, then the top and bottom back corners
  local x0 z0 z1; read -r x0 z0 z1 < <(Q "import FreeCAD
b = FreeCAD.getDocument('$F').getObject('Body').Shape.BoundBox; print(round(b.XMin, 4), round(b.ZMin, 4), round(b.ZMax, 4))")
  echo "front x $x0 z $z0 $z1" >> $L
  cam Front 1 12 0 $(awk -v h=${1:-80} 'BEGIN{print h / 2}') $(awk -v h=${1:-80} 'BEGIN{print h + 50}')
  echo "front px: floor-left $(vp -10 0 0) floor-right $(vp 40 0 0) top-back $(vp $x0 0 $z1) bottom-back $(vp $x0 0 $z0) at60 $(vp 0 0 60) at0 $(vp 0 0 0)" >> $L
  sl_nap 2; shot $O/front.png
  mpos top $x0 0 $z1
  mpos bottom $x0 0 $z0
}
hole_view() {  # right view: the plate's back face with the screw hole
  local z1; z1=$(Q "import FreeCAD; print(round(FreeCAD.getDocument('$F').getObject('Body').Shape.BoundBox.ZMax, 4))")
  cam Right 3 0 -10 $(awk -v h=${1:-80} 'BEGIN{print h / 2}') $(awk -v h=${1:-80} 'BEGIN{print h + 30}')
  echo "right px: top-mid $(vp 0 -10 $z1) hole $(vp 0 -10 $(awk -v h=${1:-80} 'BEGIN{print h - 15}')) floor $(vp 0 -10 0)" >> $L
  sl_nap 3; shot $O/hole.png; sl_nap 1
}
skedit() {     # skedit: double-click HookSketch, the lab's camera on the hook (sketch edit zooms to fit on its own)
  dblrow HookSketch "double-click: HookSketch (edit)"; sl_nap 1
  FQ "look('$F', 'Front', 12, 0, ${1:-30}, ${2:-90})" >> $L; sl_mark "(sketch view set)"; sl_nap 2
  echo "solver: $(solver_text)" >> $L
}
skclose() { at "$(B text Close)" "sketch: Close"; sl_nap 3; }

xdotool mousemove 1500 1500
echo "rows open: $(row_open $F HookSketch)" >> $L; xdotool mousemove 1500 1500; sleep 1
isofit
sl_record "$O"; sl_mark "recording started: FreeCAD 1.1.4, hook.FCStd open ($T)"
sl_nap 3
case $T in
A|B)
  H=80
  setheight $H
  isofit; sl_nap 2; shot $O/iso.png
  front_measures $H
  hole_view $H
  if [ $T = B ]; then
    skedit 40 110; sl_nap 1; shot $O/sketch-message.png; sl_mark "hold: message"; sl_nap 4
    skclose
  fi
  isofit; sl_nap 2
  ;;
P)
  dblrow Params "double-click: open Params"
  for r in 0 1 2 3 4; do
    c=$(B cell $r 1); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Params row $((r + 1))"; sl_nap 1.8
  done
  xdotool mousemove 1500 1500; sl_nap 2; shot $O/params.png
  t=$(B tab "$F"); at "$t" "tab: back to the 3D view"; sl_nap 2
  skedit; sl_mark "hold: rule marks"; sl_nap 5; shot $O/sketch-rules.png
  sl_mark "hold: message"; sl_nap 4
  p=$(WG text "Degrees"); echo "link $p" >> $L
  sl_glide $(( ${p% *} - 40 )) ${p#* } 20; sl_nap 0.8; sl_click $(( ${p% *} - 40 )) ${p#* } "message link: 2 Degrees of Freedom"
  sl_nap 1; xdotool mousemove 1500 1500; sl_nap 4; shot $O/link-selected.png
  echo "selection after link: $(selnames)" >> $L
  read -r OX OY < <(SP $F HookSketch -1 origin); echo "origin px $OX $OY" >> $L
  sl_glide $OX $((OY - 120)) 25; sl_mark "hover: near the origin"; sl_nap 3
  Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" >> $L
  skclose
  ;;
C)
  skedit; sl_nap 2
  read -r CX CY < <(SP $F HookSketch 0 start); echo "corner px $CX $CY" >> $L
  sl_glide $((CX - 30)) $((CY - 30)) 20; sl_nap 0.8
  sl_mark "box select: start up-left of the corner"; xdotool mousedown 1; sleep 0.2
  for i in $(seq 1 12); do xdotool mousemove $((CX - 30 + 5 * i)) $((CY - 30 + 5 * i)); sleep 0.06; done
  sleep 0.3; xdotool mouseup 1; sl_mark "box select: released (corner + origin)"; sl_nap 1.5
  echo "selection: $(selnames)" >> $L
  p=$(B Sketcher_ConstrainCoincidentUnified); sl_glide ${p% *} ${p#* } 25; sl_mark "hover: Coincident Constraint"; sl_nap 2.5
  shot $O/tooltip.png
  sl_click ${p% *} ${p#* } "Coincident Constraint"; sl_nap 1.5; xdotool mousemove 1500 1500
  echo "solver: $(solver_text)" >> $L
  sl_mark "hold: Fully constrained"; sl_nap 5; shot $O/fully.png
  skclose
  H=80
  setheight $H
  isofit; sl_nap 2
  front_measures $H
  hole_view $H
  isofit; sl_nap 2
  ;;
D)
  skedit 40 110; sl_nap 1
  read -r MX MY < <(SP $F HookSketch 7 mid); echo "back line mid $MX $MY" >> $L
  echo "before drag: $(Q "import FreeCAD; g = FreeCAD.getDocument('$F').getObject('HookSketch').Geometry[0]; print(g.StartPoint)")" >> $L
  sl_glide $MX $MY 20; sl_nap 0.8; sl_mark "drag: the back line"; xdotool mousedown 1; sleep 0.2
  for i in $(seq 1 20); do xdotool mousemove $((MX + 4 * i)) $((MY - 3 * i)); sleep 0.05; done
  sleep 0.4; xdotool mouseup 1; sl_mark "drag: released"; sl_nap 3
  echo "after drag: $(Q "import FreeCAD; g = FreeCAD.getDocument('$F').getObject('HookSketch').Geometry[0]; print(g.StartPoint)")" >> $L
  shot $O/after-drag.png
  skclose
  H=100
  setheight $H
  isofit; sl_nap 2
  front_measures $H
  hole_view $H
  isofit; sl_nap 2
  ;;
T|TB)
  skedit; sl_nap 2
  read -r MX MY < <(SP $F HookSketch 7 mid); echo "back line mid $MX $MY" >> $L
  sl_glide $MX $MY 20; sl_nap 0.8; sl_mark "drag: the back line (a slip)"; xdotool mousedown 1; sleep 0.2
  for i in $(seq 1 16); do xdotool mousemove $((MX + 2 * i)) $((MY + 9 * i)); sleep 0.04; done
  sleep 0.3; xdotool mouseup 1; sl_mark "drag: released"; sl_nap 3
  echo "after drag: $(Q "import FreeCAD; g = FreeCAD.getDocument('$F').getObject('HookSketch').Geometry[0]; print(g.StartPoint)")" >> $L
  shot $O/after-drag.png
  skclose
  echo "after close: $(live $F nosolve)" >> $L
  isofit; sl_nap 2
  front_measures 60
  hole_view 60
  isofit; sl_nap 2
  ;;
esac
sl_nap 2; sl_stop
lab_save $F $O/end.FCStd >> $L 2>&1
echo "TAKE $T DONE" >> $L
fc_quit; sl_display_stop
echo "check: $(check10 $O/end.FCStd $O/check.json)" >> $L
