#!/bin/bash
# fc13 takes (PLAN 4.2 rev 2.1), FreeCAD 1.1.4 by hand, no AI. Recipes from G0 (out/fc13/G0/VERDICT.txt).
#   FCC_PREFIX=fc13 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fc13_take.sh R|T|M|F|P|Y|K
#   R  cup-box: full window, the cup orbits; Params tab, cursor down the 4 rows, holds; back, orbit          F3
#   T  cup-box: top face picked, Thickness; panel (O = this part, cut before OK): rows hovered, "=" Params.wall,
#      "Make thickness inwards" hovered (ticked); OK; iso, top view                                            F0 F4 F5 S0
#   M  T's end: top view, Measure the two inner rim edges across (56), then front-back (36)                    F5
#   F  T's end: double-click Thickness, click the "Make thickness inwards" box (unticked), OK; iso; top; Measure 60  F1 F8 S2
#   P  F's end opened (reopened file): Params wall 2 -> 3, Recompute, top, Measure (60); cup_width 70, Recompute,
#      top, Measure (70); iso, orbit                                                                            F9 S2
#   Y  cup-trap orbiting, slow (think-pause footage)                                                            F14
#   K  cup-trap: click Thickness, Data tab, hover Reversed: FreeCAD's description held                          F6
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh; . /lab/lab/fc12_lib.sh; . /lab/lab/fc13_lib.sh
T=$1; O=$X/$T; mkdir -p $O; L=$O/take.log; : > $L
case $T in R|T) SRC=$X/P/cup-box.FCStd;; M|F) SRC=$X/T/end.FCStd;; P) SRC=$X/F/end.FCStd;; Y|K) SRC=$X/P/cup-trap.FCStd;;
  *) echo "R|T|M|F|P|Y|K"; exit 2;; esac
F=cup
fx_start $O
mkdir -p /tmp/fc13; cp "$SRC" /tmp/fc13/$F.FCStd

prepdoc() {
  FQ "prep('$F')" >> $L 2>&1
  Q "import FreeCAD, FreeCADGui
g = FreeCADGui.getDocument('$F'); g.activeView().setAnimationEnabled(False)
g.getObject('Body').ShapeAppearance = [FreeCAD.Material(DiffuseColor=(0.93, 0.55, 0.20))]
print(1)" >> $L 2>&1
}
if [ "$T" != P ]; then
  open_doc /tmp/fc13/$F.FCStd >> $L 2>&1; prepdoc
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
topview() {
  sl_glide 1500 1200 15; sl_key 2 "key 2: top view"; sl_nap 0.5
  Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewTop(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L
  sl_mark "(view fitted)"; sl_nap 2
}
isofit() {
  sl_key 0 "key 0: isometric"; sl_nap 0.5
  Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewIsometric(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L
  sl_mark "(view fitted)"; sl_nap 2
}
m() {          # m NAME X1 Y1 X2 Y2: Measure between the inner rim edges through (X1,Y1,50) and (X2,Y2,50) (top view)
  local p; p=$(vp $2 $3 50 $4 $5 50); echo "$1 edges $p" >> $L; set -- "$1" $p
  btn Std_Measure "Measure"; sl_nap 2
  sl_glide $2 $3 25; sl_nap 0.8; sl_click $2 $3 "$1: first inner edge"; sl_nap 1.5
  sl_glide $4 $5 25; sl_nap 0.8; xdotool keydown ctrl; sl_click $4 $5 "$1: Ctrl + opposite inner edge"; xdotool keyup ctrl
  sl_nap 3.5
  echo "$1 measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*\|"QLabel", "[^"]*"' | tr '\n' ' ')" >> $L
  echo "$1 selection: $(selnames)" >> $L
  shot $O/measure-$1.png; sl_nap 3
  at "$(taskpos any Close)" "Measure: Close"; sl_nap 1.5
  Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null
}
ROW() {
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
  echo "$3 $2: $(tstate $F)" >> $L
}
cbox() {       # cbox: the "Make thickness inwards" box itself (G0: a click on the label centre only focused it)
  local c; c=$(taskpos any "Make thickness inwards"); [ "$c" != none ] || return 1
  echo "$(( ${c% *} - 238 )) ${c#* }"
}
checked() { Q "import FreeCADGui
from PySide import QtWidgets
print([c.isChecked() for c in FreeCADGui.getMainWindow().findChildren(QtWidgets.QCheckBox) if c.isVisible() and 'inwards' in c.text()])"; }

if [ "$T" != P ]; then
  xdotool mousemove 1500 1500
  echo "rows open: $(row_open $F Thickness 2>/dev/null)" >> $L; xdotool mousemove 1500 1500; sleep 1
fi
sl_record "$O"; sl_mark "recording started: FreeCAD 1.1.4, cup.FCStd ($T)"
sl_nap 3
case $T in
R)
  orbit 6 60
  dblrow Params "double-click: open Params"; sl_nap 1.5
  for r in 0 1 2 3; do
    c=$(B cell $r 1); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Params row $((r + 1))"; sl_nap 2
  done
  for r in 0 1 2; do c=$(B cell $r 1); sl_glide ${c% *} ${c#* } 15; sl_mark "hold: row $((r + 1))"; sl_nap 2; done
  c=$(B cell 3 1); sl_glide ${c% *} ${c#* } 15; sl_mark "hold: wall 2"; sl_nap 3
  shot $O/params.png
  t=$(B tab "$F"); at "$t" "tab: back to the 3D view"; sl_nap 1.5
  orbit 6 60
  ;;
T)
  p=$(vp 0 0 50); sl_glide ${p% *} ${p#* } 25; sl_nap 0.8; sl_click ${p% *} ${p#* } "top face picked"; sl_nap 2
  echo "selection: $(selnames)" >> $L
  btn PartDesign_Thickness "Thickness"; sl_nap 4
  shot $O/panel-open.png
  echo "panel: $(FQ "task_texts()" | grep -o '"Q[A-Za-z:]*", "[^"]*"\|"list", "[^"]*"' | tr '\n' ' ')" >> $L
  echo "box at open: $(checked)" >> $L
  sl_mark "O starts: panel open"
  p=$(FQ "field_pos('Thickness')"); sl_glide $(( ${p% *} - 40 )) ${p#* } 20; sl_mark "hover: Thickness 1.00 mm"; sl_nap 2.5
  c=$(FQ "combo_pos('Skin')"); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Mode Skin"; sl_nap 2
  c=$(FQ "combo_pos('Arc')"); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Join type Arc"; sl_nap 2
  sl_click $(( ${p% *} - 40 )) ${p#* } "Thickness: click"; xdotool key ctrl+a; sl_nap 0.4
  sl_type "=" "Thickness: typed = (Expression Editor)" 200; sl_nap 2
  sl_type "Params.wall" "Thickness: typed Params.wall" 110; sl_nap 1.5
  sl_key Return "Return: name list closed"; sl_nap 2
  shot $O/expr.png
  at "$(FQ "expr_ok()")" "Expression Editor: OK"; sl_nap 3
  echo "expr: $(tstate $F)" >> $L
  b=$(cbox); sl_glide ${b% *} ${b#* } 20; sl_mark "hover: Make thickness inwards (ticked)"; sl_nap 4
  echo "box before OK: $(checked)" >> $L
  shot $O/trap-panel.png
  sl_mark "O ends: before OK"
  at "$(taskpos any OK)" "OK"; sl_nap 3
  echo "after OK: $(tstate $F)" >> $L
  isofit; shot $O/trap-iso.png; sl_nap 2
  topview; shot $O/trap-top.png; sl_nap 3
  echo "messages: dialogs $(dialogs) notices $(FQ "notices()")" >> $L
  ;;
M)
  topview; sl_nap 1
  m across 28 0 -28 0
  m front-back 0 18 0 -18
  ;;
F)
  dblrow Thickness "double-click: Thickness (edit)"; sl_nap 1.5
  echo "box at open: $(checked)" >> $L
  b=$(cbox) || bail "no checkbox"
  sl_glide ${b% *} ${b#* } 20; sl_nap 1; sl_click ${b% *} ${b#* } "Make thickness inwards: unticked"; sl_nap 4
  echo "box after click: $(checked) $(tstate $F)" >> $L
  shot $O/fix-panel.png
  at "$(taskpos any OK)" "OK"; sl_nap 3
  echo "after OK: $(tstate $F)" >> $L
  isofit; shot $O/fix-iso.png; sl_nap 2
  topview; shot $O/fix-top.png
  m across 30 0 -30 0
  echo "messages: dialogs $(dialogs) notices $(FQ "notices()")" >> $L
  ;;
P)
  sl_nap 1
  open_doc /tmp/fc13/$F.FCStd >> $L 2>&1; sl_mark "file reopened: F's saved end file"; prepdoc; report_hide; sl_nap 3
  echo "notices at reopen: $(FQ "notices()")" >> $L
  row_open $F Thickness >> $L; xdotool mousemove 1500 1500; sl_nap 1
  params_set 3 3 wall
  topview; shot $O/w3-top.png
  m across-w3 30 0 -30 0
  params_set 0 70 cup_width
  topview; shot $O/cw70-top.png
  m across-cw70 35 0 -35 0
  isofit; orbit 4 40
  ;;
Y)
  orbit 24 120
  ;;
K)
  p=$(ROW $F Thickness); at "$p" "tree: Thickness"; sl_nap 2
  r=$(FQ13 "prop_row('Reversed')"); echo "Reversed row $r" >> $L; [ "$r" != none ] || bail "no Reversed row"
  sl_glide $(( ${r% *} - 6 )) $(( ${r#* } + 3 )) 25; sl_nap 0.3; xdotool mousemove ${r% *} ${r#* }; sl_mark "hover: Reversed"
  sl_nap 3; echo "tooltip: $(FQ13 "tooltip_text()")" >> $L; shot $O/reversed-hover.png; sl_nap 5
  ;;
esac
sl_nap 2; sl_stop
lab_save $F $O/end.FCStd >> $L 2>&1
echo "TAKE $T DONE" >> $L
fc_quit; sl_display_stop
check13 $O/end.FCStd $O/check.json >> $L
