#!/bin/bash
# fc11 takes (PLAN 4.2 rev 3.1), FreeCAD 1.1.4 by hand, no AI. Recipes from G0 + G0b (out/fc11/G0*/VERDICT.txt).
#   FCC_PREFIX=fc11 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fc11_take.sh T|F|P|R|D|U|X|Y
#   T  orphan @60 (G0b GUI file): Params 80, Recompute, front Measure top (60.00), sketch "Fully constrained"   F0 F6 S0
#   F  reference @60: Params 80, Recompute, front Measure top (80.00), sketch: blue 75 held                    F1 F15 S3
#   P  pinned @60: Params rows, sketch "Fully constrained"                                                         F3
#   R  pinned @60: K D on the inner face, box 55 held (panel "Redundant constraints: (24)"), OK, the refusal       F4 S1
#   D  pinned @60: click "plate_height = 60 mm (f)", Delete, panel; K D on the inner face, 55, OK, panel           F5 S1
#   U  orphan @80 (G0b GUI file): click the 55, K X (blue), panel; back line K D "=Params.plate_height", OK;
#      Close, Recompute, front Measure top (80.00); sketch: blue 75 held                                    F8 F9 S2
#   X  U's end file reopened: Params 100, Recompute, front Measure top (100.00); sketch: blue 95 held              F11
#   H  (lab finding, 17 Nov) orphan @60: right view on the plate's back, the screw hole; Params 80, Recompute; the same
#      view: the hole is gone (HoleSketch reads plate_height: hole at z 65 above the 60 top, the Pocket cuts nothing)
#   Y  your-turn rectangle 40 x 30 pinned: construction mode, line corner to corner, K D, Reference ticked, OK  F16
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh
T=$1; O=$X/$T; mkdir -p $O; L=$O/take.log; : > $L
F=hook
case $T in T|H) SRC=$X/G0b/hook-orphan.FCStd;; U) SRC=$X/G0b/hook-orphan-80gui.FCStd;; F) SRC=$X/P/hook-reference.FCStd;;
  P|R|D) SRC=$X/P/hook-pinned.FCStd;; X) SRC=$X/U/end.FCStd;; Y) SRC=$X/P/rect-pinned.FCStd; F=rect;;
  *) echo "T|F|P|R|D|U|X|Y|H"; exit 2;; esac
fx_start $O
mkdir -p /tmp/fc11; cp "$SRC" /tmp/fc11/$F.FCStd
open_doc /tmp/fc11/$F.FCStd >> $L 2>&1
[ $F = hook ] && FQ "prep('$F')" >> $L 2>&1
Q "import FreeCADGui
FreeCADGui.getDocument('$F').activeView().setAnimationEnabled(False)
print(1)" >> $L 2>&1
report_hide; sleep 2; xdotool mousemove 1500 1500; rv_clear
[ $F = hook ] && echo "start: $(live11 $F)" >> $L

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
  echo "after $1: $(live11 $F)" >> $L
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
okbox() {      # okbox: where the "Insert Length" box is (OK at +135 +190, Reference at +37 +132, G0); no lab query while up
  local g; g=$(xdotool search --onlyvisible --name 'Insert Length' getwindowgeometry 2>/dev/null | tr '\n' ' ')
  echo "box: $g" >> $L; [ -n "$g" ] || bail "no Insert Length box"
  read -r BOXX BOXY < <(echo "$g" | sed -E 's/.*Position: ([0-9]+),([0-9]+).*/\1 \2/')
}
kd() {         # kd LABEL: K then D (Distance) with the mouse off the sketch, then the box is up
  sl_glide 1800 1300 15; sl_key k "key K"; sleep 0.3; sl_key d "key D: $1"; sl_nap 3; okbox
}
boxok() { sl_glide $((BOXX + 135)) $((BOXY + 190)) 20; sl_nap 0.8; sl_click $((BOXX + 135)) $((BOXY + 190)) "box: OK${1:-}"; }
lineclick() {  # lineclick SKETCH GEO WHERE DX DY LABEL
  local p; p=$(SP $F $1 $2 $3 $4 $5); sl_glide ${p% *} ${p#* } 20; sl_nap 0.6; sl_click ${p% *} ${p#* } "$6"; sl_nap 1.5
  echo "sel: $(selnames)" >> $L
}
labelclick() { # labelclick INDEX LABEL: a size's label in the view
  local p; p=$(cd /lab && timeout 20 python3 -m lab.dimpt $F HookSketch $1); sl_glide ${p% *} ${p#* } 20; sl_nap 0.8
  sl_click ${p% *} ${p#* } "$2"; sl_nap 1.5; echo "sel: $(selnames)" >> $L
}
holdsketch() { # holdsketch LABEL SECONDS SHOT
  sl_mark "hold: $1"; xdotool mousemove 1500 1500; sl_nap ${2:-4}; shot $O/$3.png; echo "solver ($1): $(solver_text)" >> $L
}

xdotool mousemove 1500 1500
if [ $F = hook ]; then echo "rows open: $(row_open $F HookSketch)" >> $L; xdotool mousemove 1500 1500; sleep 1; isofit; fi
sl_record "$O"; sl_mark "recording started: FreeCAD 1.1.4, $F.FCStd open ($T)"
sl_nap 3
case $T in
T|F|X)
  H=80; [ $T = X ] && H=100
  setheight $H
  isofit; sl_nap 2; shot $O/iso.png
  front_measures $H
  isofit; sl_nap 1
  skedit $((H / 2)) $((H + 50)); holdsketch "sketch message" 5 sketch-message
  skclose; isofit; sl_nap 2
  ;;
H)
  hole_view 60; sl_mark "hold: the screw hole at 60"; sl_nap 4; shot $O/hole-60.png
  isofit; sl_nap 1
  setheight 80
  hole_view 60; sl_mark "hold: no hole after 80"; sl_nap 5; shot $O/hole-80.png
  isofit; sl_nap 2
  ;;
P)
  dblrow Params "double-click: open Params"
  for r in 0 1 2 3 4; do
    c=$(B cell $r 1); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Params row $((r + 1))"; sl_nap 1.8
  done
  xdotool mousemove 1500 1500; sl_nap 2; shot $O/params.png
  t=$(B tab "$F"); at "$t" "tab: back to the 3D view"; sl_nap 2
  skedit; holdsketch "Fully constrained" 6 sketch-full
  skclose
  ;;
R)
  skedit; sl_nap 2
  lineclick HookSketch 5 mid 0 0 "click: the inside face"
  kd "Insert Length box"
  shot $O/box.png; sl_mark "hold: box 55.00, Reference unticked, panel Redundant constraints (24)"; sl_nap 5
  boxok; sl_nap 1.5
  shot $O/refused.png; sl_mark "hold: notification Datum 55.00 mm ... invalid"; xdotool mousemove 1500 1500; sl_nap 5
  holdsketch "panel after OK" 3 after-ok
  echo "after OK: $(live11 $F)" >> $L
  skclose
  ;;
D)
  skedit; sl_nap 2
  labelclick 20 "click: plate_height = 60 mm (f)"; sl_mark "hold: the plate_height size selected"; sl_nap 2.5
  shot $O/selected.png
  sl_key Delete "key Delete"; sl_nap 2
  holdsketch "panel after Delete" 4 after-delete
  lineclick HookSketch 5 mid 0 0 "click: the inside face"
  kd "Insert Length box"
  shot $O/box.png; sl_mark "hold: box 55.00"; sl_nap 3
  boxok; sl_nap 2
  holdsketch "Fully constrained again" 5 after-55
  echo "after 55: $(live11 $F)" >> $L
  skclose
  ;;
U)
  skedit 40 130; sl_nap 2
  n=$(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('HookSketch'); print([i for i, c in enumerate(sk.Constraints) if c.Type == 'Distance' and c.First == 5][0])")
  echo "the 55 is index $n" >> $L
  labelclick $n "click: the 55"; sl_nap 1
  sl_glide 1800 1300 15; sl_key k "key K"; sleep 0.3; sl_key x "key X: Toggle Driving/Reference"; sl_nap 2
  holdsketch "blue 55, Under-constrained 1 DoF" 5 toggled
  lineclick HookSketch 7 start 0 60 "click: the back line"
  kd "Insert Length box"
  sl_type "=" "typed = (Expression Editor opens)" 250; sl_nap 1.5
  sl_type "Params.plate_height" "typed Params.plate_height" 160; sl_nap 2.5; shot $O/expr.png
  sl_key Return "Enter: expression"; sl_nap 1.5
  if [ "$(xdotool search --onlyvisible --name 'Expression Editor' 2>/dev/null | wc -l)" -gt 0 ]; then sl_key Return "Enter: expression editor"; sl_nap 1.5; fi
  shot $O/box-expr.png; sl_mark "hold: box with the expression"; sl_nap 2
  boxok; sl_nap 2
  holdsketch "Fully constrained, blue reads 75" 5 fixed
  echo "after fix: $(live11 $F)" >> $L
  skclose
  btn Std_Refresh "Recompute"; sl_nap 3
  isofit; sl_nap 2; shot $O/iso.png
  front_measures 80
  isofit; sl_nap 1
  skedit 40 130; holdsketch "blue 75" 5 blue75
  skclose; isofit; sl_nap 2
  ;;
Y)
  p=$(ROW $F Sketch); sl_glide ${p% *} ${p#* } 20; sl_nap 0.5; sl_mark "double-click: Sketch (edit)"; xdotool click --repeat 2 --delay 120 1; sl_nap 3
  FQ "look('$F', 'Top', 20, 15, 0, 60)" >> $L; sl_mark "(sketch view set)"; sl_nap 2
  holdsketch "Fully constrained" 3 rect
  at "$(B Sketcher_ToggleConstruction)" "Toggle construction geometry"; sl_nap 1.5
  at "$(B Sketcher_CreateLine)" "Line tool"; sl_nap 1.5
  read -r AX AY < <(SP $F Sketch 0 start); read -r BX BY < <(SP $F Sketch 2 start)
  sl_glide $AX $AY 25; sl_nap 0.8; sl_click $AX $AY "line: first corner"; sl_nap 1
  sl_glide $BX $BY 30; sl_nap 0.8; sl_click $BX $BY "line: far corner"; sl_nap 1
  sl_key Escape "Escape: line tool off"; sl_nap 1.5
  echo "geo: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('Sketch'); print(len(sk.Geometry), [sk.getConstruction(i) for i in range(len(sk.Geometry))], round(sk.Geometry[-1].length(), 4))")" >> $L
  lineclick Sketch 4 mid 0 0 "click: the helper line"
  kd "Insert Length box"
  sl_glide $((BOXX + 37)) $((BOXY + 132)) 20; sl_nap 0.6; sl_click $((BOXX + 37)) $((BOXY + 132)) "tick: Reference"; sl_nap 1.5
  shot $O/box-ref.png
  boxok " (answer on screen from here)"; sl_nap 3
  holdsketch "reference diagonal" 4 diag
  echo "diag: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('Sketch'); c = sk.Constraints[-1]; print(c.Type, round(c.Value, 4), c.Driving, round(sk.Geometry[4].length(), 6), sk.getConstruction(4))")" >> $L
  skclose
  ;;
esac
sl_nap 2; sl_stop
lab_save $F $O/end.FCStd >> $L 2>&1
echo "TAKE $T DONE" >> $L
fc_quit; sl_display_stop
if [ $F = hook ]; then echo "check: $(check11 $O/end.FCStd $O/check.json)" >> $L; fi
true
