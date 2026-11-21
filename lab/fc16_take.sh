#!/bin/bash
# fc16 takes (PLAN 4.2 rev 2, Q9 branch: lesson 14's cup + hole_size, no rim), FreeCAD 1.1.4 by hand, no AI.
# Copied from lab/fc15_take.sh (keeps wb_pd: the workbench list back to Part Design after Params, lesson 15's fix).
#   FCC_PREFIX=fc16 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fc16_take.sh R|D|T|A|F|P|Y
#   R  hole-start: full window, orbit; Params rows (wall, hole_size); back face zoom                              F3
#   D  hole-start: rear view, back face, New sketch, circle (typed 5), Diameter "=" Params.hole_size, centre
#      height 30 (I), Close, Pocket, Length 2, OK; inside view: the hole is open at wall 2                          F4
#   T  D's end: Params wall 3, Recompute; back zoom (the circle still there); inside view: hole gone; Measure the
#      skin (pit floor, then Ctrl + the inside back face): 1.00 mm                                                  F0 F5
#   A  T's end: double-click Pocket, Type Through all, OK; inside view: open; front view: the front wall holed      F6
#   F  A's end: double-click Pocket, Type Dimension, Length "=" Params.wall, OK; inside view open; front closed     F7 F8
#   P  F's end reopened: Params wall 4, Recompute; inside open; front closed; hole_size 6, Recompute; back zoom    F9
#   Y  F's end orbiting slowly (think pause)                                                                        F14
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh; . /lab/lab/fc12_lib.sh; . /lab/lab/fc13_lib.sh; . /lab/lab/fc14_lib.sh; . /lab/lab/fc15_lib.sh; . /lab/lab/fc16_lib.sh
T=$1; TD=$T; [ "$T" = P ] && TD=K   # take P films into out/fc16/K: out/fc16/P holds the start files
O=$X/$TD; mkdir -p $O; L=$O/take.log; : > $L
case $T in R|D) SRC=$X/P/hole-start.FCStd;; T) SRC=$X/D/end.FCStd;; A) SRC=$X/T/end.FCStd;; F) SRC=$X/A/end.FCStd;;
  P|Y) SRC=$X/F/end.FCStd;; *) echo "R|D|T|A|F|P|Y"; exit 2;; esac
[ -f "$SRC" ] || { echo "no $SRC"; exit 2; }
F=cup
W14=/tmp/fc16-ui.json
fx_start $O
mkdir -p /tmp/fc16; cp "$SRC" /tmp/fc16/$F.FCStd

prepdoc() {
  FQ "prep('$F')" >> $L 2>&1
  Q "import FreeCAD, FreeCADGui
g = FreeCADGui.getDocument('$F'); g.activeView().setAnimationEnabled(False)
g.getObject('Body').ShapeAppearance = [FreeCAD.Material(DiffuseColor=(0.93, 0.55, 0.20))]
print(1)" >> $L 2>&1
}
if [ "$T" != P ]; then
  open_doc /tmp/fc16/$F.FCStd >> $L 2>&1; prepdoc
  report_hide; sleep 2; xdotool mousemove 1500 1500; rv_clear
fi
echo "notices at open: $(FQ "notices()")" >> $L

orbit() {      # orbit SECONDS DEG: the camera turns round the world Z axis, smoothly
  Q "import FreeCAD, FreeCADGui, time
from PySide import QtWidgets
v = FreeCADGui.getDocument('$F').activeView(); n = int($1 * 30); st = $2 / float(n)
for i in range(n):
    v.setCameraOrientation(FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), st).multiply(v.getCameraOrientation()))
    QtWidgets.QApplication.processEvents(); time.sleep(1 / 30.0)
print(1)" >> $L 2>&1
}
zoomto() {     # zoomto SECONDS VIEW CX CY CZ HEIGHT: the camera glides to look at (CX,CY,CZ), HEIGHT mm high
  # VIEW: a standard view (Rear, Front, Isometric) or Inside (from the front turned 45 deg down: over the front rim
  # into the cup, onto the inside of the back wall)
  Q "import FreeCAD, FreeCADGui, time
from PySide import QtWidgets
from pivy import coin
v = FreeCADGui.getDocument('$F').activeView(); v.setAnimationEnabled(False); cam = v.getCameraNode()
p0 = FreeCAD.Vector(*cam.position.getValue().getValue()); h0 = cam.height.getValue()
r0 = cam.orientation.getValue()
if '$2' == 'Inside':
    v.viewFront(); v.setCameraOrientation(FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -45).multiply(v.getCameraOrientation()))
else:
    getattr(v, 'view$2')()
r1 = cam.orientation.getValue(); cam.orientation.setValue(r0)
d = r1.multVec(coin.SbVec3f(0, 0, -1)); c = FreeCAD.Vector($3, $4, $5)
p1 = c - FreeCAD.Vector(d[0], d[1], d[2]) * 200
n = int($1 * 30)
for i in range(1, n + 1):
    t = i / float(n); t = t * t * (3 - 2 * t)
    cam.orientation.setValue(coin.SbRotation.slerp(r0, r1, t))
    p = p0 + (p1 - p0) * t; cam.position.setValue(p.x, p.y, p.z); cam.height.setValue(h0 + ($6 - h0) * t)
    QtWidgets.QApplication.processEvents(); time.sleep(1 / 30.0)
print(1)" >> $L 2>&1
  sl_mark "view: $2 (${6} mm high, at $3 $4 $5)"; sl_nap 1
}
isofit() {
  sl_key 0 "key 0: isometric"; sl_nap 0.5
  Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewIsometric(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L
  sl_mark "(view fitted)"; sl_nap 2
}
wall() { Q "import FreeCAD; print(float(FreeCAD.getDocument('$F').getObject('Params').get('wall')))"; }
inside() { zoomto 3 Inside 0 20 30 64; sl_nap 2; shot $O/inside-$1.png; echo "inside $1: $(hstate $F)" >> $L; }
backzoom() { local w; w=$(wall); zoomto 3 Rear 0 $(python3 -c "print(20 + $w)") 30 24; sl_nap 2; shot $O/back-$1.png; }
frontzoom() { zoomto 3 Front 0 -22 34 30; sl_nap 2; shot $O/front-$1.png; echo "front $1: $(hstate $F)" >> $L; }
clr() { Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null; }
bail() { echo "BAIL: $1" >> $L; sl_stop; fc_quit; sl_display_stop; exit 1; }
dblrow() {     # dblrow OBJ LABEL: double-click a tree row
  local p; p=$(ROW $F "$1"); sl_glide ${p% *} ${p#* } 20; sl_nap 0.5
  sl_mark "$2"; xdotool click --repeat 2 --delay 120 1; sl_nap 3
}
params_set() {   # params_set ROW VALUE NAME: Params tab, cell B(ROW+1) <- VALUE, Enter, Recompute, back to the 3D tab
  dblrow Params "double-click: open Params"
  local c; c=$(B cell $1 1); echo "$3 cell $c" >> $L
  at "$c" "cell B$(( $1 + 1 )): $3"; sl_nap 1
  sl_type "$2" "typed $2" 250; sl_key Return "Enter"; sl_nap 1.5
  shot $O/params-$3-$2.png
  btn Std_Refresh "Recompute"; sl_nap 3
  local t; t=$(B tab "$F"); at "$t" "tab: back to the 3D view"; sl_nap 2
  echo "$3 $2: $(hstate $F)" >> $L
}
wb_pd() {      # the workbench list (Spreadsheet after Params) back to Part Design, by clicks
  local c; c=$(FQ "combo_pos('Spreadsheet')"); echo "wb combo $c" >> $L; [ "$c" != none ] || return 0
  uiwatch 15; at "$c" "workbench list"; sl_nap 1.5
  local p; p=$(ui popup "Part Design")
  case "$p" in ""|none) p=$(ui menu "Part Design");; esac
  echo "wb Part Design at $p" >> $L
  case "$p" in ""|none) xdotool key Escape; bail "workbench Part Design not found";; esac
  at "$p" "workbench: Part Design"; sl_nap 2.5
}
panel_log() { echo "panel $1: $(FQ "task_texts()" | grep -o 'combo:[^"]*\|field:[^"]*\|"QLabel", "[^"]*"\|"QCheckBox", "[^"]*"' | tr '\n' ' ')" >> $L; }
typeset_to() {   # typeset_to FROM TO: the Pocket panel's Type list, FROM -> TO, by clicks (rows from the UI watcher)
  local c p; c=$(FQ "combo_pos('$1')"); [ "$c" != none ] || bail "no Type list showing $1"
  uiwatch 15; at "$c" "Type list"; sl_nap 1.8
  echo "Type list rows: $(ui dump | grep -o '"popup": \[.*\]' | cut -c1-300)" >> $L
  p=$(ui popup "$2"); case "$p" in ""|none) xdotool key Escape; bail "Type $2 not in the list";; esac
  sl_glide ${p% *} ${p#* } 15; sl_nap 0.8; sl_click ${p% *} ${p#* } "Type: $2"; sl_nap 2.5
}
pocket_ok() { panel_log "before OK"; shot $O/panel-$1.png; at "$(taskpos any OK)" "OK"; sl_nap 4; echo "after OK: $(hstate $F)" >> $L; echo "notices: $(FQ "notices()")" >> $L; }
mskin() {      # mskin NAME: Measure; the pit floor (back view), the camera into the cup, Ctrl + the inside back face
  local w p; w=$(wall); clr
  zoomto 3 Rear 0 $(python3 -c "print(20 + $w)") 30 14
  btn Std_Measure "Measure"; sl_nap 2
  p=$(vp 0 $(python3 -c "print(20 + $w - 2)") 30); sl_glide ${p% *} ${p#* } 25; sl_nap 0.8
  sl_click ${p% *} ${p#* } "$1: the pit's floor (the bottom of the 2 mm cut)"; sl_nap 1.5
  zoomto 3 Inside 0 20 32 40
  p=$(vp 0 20 37); sl_glide ${p% *} ${p#* } 25; sl_nap 0.8
  xdotool keydown ctrl; sl_click ${p% *} ${p#* } "$1: Ctrl + the inside face of the back wall"; xdotool keyup ctrl
  sl_nap 3.5
  echo "$1 measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*' | tr '\n' ' ')" >> $L
  echo "$1 selection: $(selnames)" >> $L
  shot $O/measure-$1.png; sl_nap 3
  at "$(taskpos any Close)" "Measure: Close"; sl_nap 1.5
  clr
}

sl_record "$O"; sl_mark "recording started: FreeCAD 1.1.4, cup.FCStd ($T)"
sl_nap 3
case $T in
R)
  orbit 6 60
  dblrow Params "double-click: open Params"; sl_nap 1.5
  for r in 3 6; do c=$(B cell $r 1); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Params row $((r + 1))"; sl_nap 2.5; done
  shot $O/params.png
  t=$(B tab "$F"); at "$t" "tab: back to the 3D view"; sl_nap 1.5
  wb_pd
  isofit; zoomto 4 Rear 0 22 25 70; sl_nap 3; shot $O/back.png
  isofit; orbit 4 40
  ;;
D)
  zoomto 3 Rear 0 22 25 70; clr
  p=$(vp 0 22 38); sl_glide ${p% *} ${p#* } 25; sl_nap 0.7; sl_click ${p% *} ${p#* } "click: the back face"; sl_nap 1.5
  echo "selection: $(selnames)" >> $L
  k=$(B PartDesign_CompSketches); sl_glide ${k% *} ${k#* } 20; sl_mark "hover: New sketch"; sl_nap 1.2
  sl_click ${k% *} ${k#* } "New sketch"; sl_nap 3.5
  echo "sketch: $(Q "import FreeCAD; s = FreeCAD.getDocument('$F').ActiveObject if False else [o for o in FreeCAD.getDocument('$F').Objects if o.TypeId == 'Sketcher::SketchObject'][-1]; print(s.Name, s.AttachmentSupport, s.MapMode)")" >> $L
  shot $O/sketch-open.png
  xdotool mousemove 1400 1300; sl_nap 0.3
  sl_key g "key G"; sl_key c "key C (circle)"; sl_nap 1.0
  p=$(vp 0 22 30); sl_glide ${p% *} ${p#* } 25; sl_nap 0.6
  sl_click ${p% *} ${p#* } "circle: centre (on the vertical axis)"
  sl_glide $(( ${p% *} + 110 )) $(( ${p#* } - 110 )) 12; sl_nap 1.0
  sl_type "5" "circle: typed 5" 250; sl_key Return "circle: Enter (5)"; sl_nap 1.5
  SK=$(Q "import FreeCAD; print([o.Name for o in FreeCAD.getDocument('$F').Objects if o.TypeId == 'Sketcher::SketchObject'][-1])")
  echo "sketch name $SK; geo: $(Q "import FreeCAD; s = FreeCAD.getDocument('$F').getObject('$SK'); print([str(g) for g in s.Geometry], [(c.Type, c.Value) for c in s.Constraints])")" >> $L
  xdotool click 3; sl_mark "right-click: circle tool off"; sl_nap 1.2
  p=$(taskpos list "Constraint1 (5 mm)"); echo "constraint row $p" >> $L
  sl_glide ${p% *} ${p#* } 20; sl_nap 0.6; sl_mark "double-click: Constraint1 (5 mm), the diameter"
  xdotool click --repeat 2 --delay 120 1; sl_nap 2
  sl_type "=" "Diameter: typed = (Expression Editor)" 150; sl_nap 1.4
  sl_type "Params.hole_size" "editor: typed Params.hole_size" 95; sl_nap 1.5
  sl_key Return "editor: Enter (the list)"; sl_nap 1.0
  sl_key Return "editor: Enter (OK)"; sl_nap 1.0
  shot $O/diameter-box.png
  sl_key Return "Insert Diameter: Enter (OK)"; sl_nap 1.8
  p=$(vp 22 22 57); sl_glide ${p% *} ${p#* } 20; sl_nap 0.4; sl_click ${p% *} ${p#* } "click: empty space above the cup (nothing selected)"; sl_nap 0.8
  [ "$(selnames)" = "[]" ] || { echo "SELECTION CLEARED BY CODE: $(selnames)" >> $L; clr; }
  p=$(SP $F $SK 0 center); sl_glide ${p% *} ${p#* } 20; sl_nap 0.5; sl_click ${p% *} ${p#* } "click: the circle's centre"; sl_nap 0.8
  echo "centre selection: $(selnames)" >> $L
  sl_key i "key I (vertical distance)"; sl_nap 1.6
  sl_type "30" "typed 30" 200; sl_key Return "Enter (30)"; sl_nap 2
  echo "sketch: $(Q "import FreeCAD; s = FreeCAD.getDocument('$F').getObject('$SK'); print([(c.Type, c.Value) for c in s.Constraints], s.ExpressionEngine, s.FullyConstrained, [str(g) for g in s.Geometry])")" >> $L
  shot $O/sketch-done.png; sl_nap 2
  at "$(taskpos any Close)" "Close (the sketch)"; sl_nap 2.5
  p=$(ROW $F $SK); sl_glide ${p% *} ${p#* } 20; sl_nap 0.4; sl_click ${p% *} ${p#* } "tree: the hole sketch"; sl_nap 1
  b=$(B PartDesign_Pocket); sl_glide ${b% *} ${b#* } 20; sl_mark "hover: Pocket"; sl_nap 1.2
  sl_click ${b% *} ${b#* } "Pocket"; sl_nap 4
  panel_log open; shot $O/panel-open.png; sl_nap 2
  p=$(FQ "field_pos('Length')"); [ "$p" != none ] || bail "no Length field"
  sl_click $(( ${p% *} - 40 )) ${p#* } "Length: click"; xdotool key ctrl+a; sl_nap 0.4
  sl_type "2" "Length: typed 2" 250; sl_nap 2
  pocket_ok typed2
  isofit; sl_nap 2; shot $O/iso.png
  backzoom w2
  inside w2
  ;;
T)
  isofit
  params_set 3 3 wall
  wb_pd
  isofit; sl_nap 1
  backzoom w3
  inside w3; sl_nap 2
  mskin skin-w3
  inside w3b
  ;;
A)
  inside w3; sl_nap 1
  dblrow Pocket "double-click: Pocket"
  panel_log open
  typeset_to Dimension "Through all"
  pocket_ok through
  inside through; sl_nap 1
  isofit; sl_nap 1
  frontzoom through; sl_nap 3
  ;;
F)
  inside through; sl_nap 1
  dblrow Pocket "double-click: Pocket"
  typeset_to "Through all" Dimension
  p=$(FQ "field_pos('Length')"); [ "$p" != none ] || bail "no Length field"
  sl_click $(( ${p% *} - 40 )) ${p#* } "Length: click"; xdotool key ctrl+a; sl_nap 0.4
  sl_type "=" "Length: typed = (Expression Editor)" 200; sl_nap 2
  shot $O/expr-open.png
  sl_type "Params.wall" "Length: typed Params.wall" 110; sl_nap 1.5
  sl_key Return "Return: name list closed"; sl_nap 2
  shot $O/expr-typed.png
  at "$(FQ "expr_ok()")" "Expression Editor: OK"; sl_nap 3
  pocket_ok wall
  inside fixed; sl_nap 1
  isofit; sl_nap 1
  frontzoom fixed; sl_nap 2
  isofit
  ;;
P)
  sl_nap 1
  open_doc /tmp/fc16/$F.FCStd >> $L 2>&1; sl_mark "file reopened: F's saved end file (Length = Params.wall)"; prepdoc; report_hide; sl_nap 3
  echo "notices at reopen: $(FQ "notices()")" >> $L
  echo "reopened: $(hstate $F)" >> $L
  isofit
  params_set 3 4 wall
  wb_pd
  isofit; sl_nap 1
  inside w4; sl_nap 1
  frontzoom w4; sl_nap 1
  isofit
  params_set 6 6 hole_size
  wb_pd
  isofit; sl_nap 1
  backzoom hole6
  inside hole6
  ;;
Y)
  isofit; orbit 24 120
  ;;
esac
sl_nap 2; sl_stop
lab_save $F $O/end.FCStd >> $L 2>&1
echo "TAKE $T DONE" >> $L
fc_quit; sl_display_stop
check16 $O/end.FCStd $O/check.json >> $L
