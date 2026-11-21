#!/bin/bash
# fc14 takes (PLAN 4.2 rev 2.1 + G0 out/fc14/G0/VERDICT.txt: the fix is route (c)), FreeCAD 1.1.4 by hand, no AI.
#   FCC_PREFIX=fc14 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fc14_take.sh R|H|T|M|F|P|Y
#   R  peg-noshell: full window, orbit; Sketch001 selected (Attachment: XZ_Plane, offset); Params rows; orbit       F3
#   H  peg-trap: the tree's features shown one at a time with Space (Pad, Pad001, Thickness)                     F1/F6
#   T  peg-noshell: top face, Thickness, "=" Params.wall, untick inwards, OK; iso; view into the cup (opening)    F0 F4 F5
#   M  T's end: top view, Measure the peg's two side edges (14); view into the cup                              F5
#   F  T's end: route (c): Thickness Delete; Pad > Set Tip; top face, Thickness, = Params.wall, untick, OK;
#      Pad001 > Set Tip; iso; view into the cup (closed); top view, Measure (10)                                 F7 F8
#   P  F's end reopened: Params wall 3, Recompute, Measure (10); peg_size 12, Recompute, Measure (12); orbit       F9
#   Y  peg-trap orbiting slowly (think pause)                                                                    F14
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh; . /lab/lab/fc12_lib.sh; . /lab/lab/fc14_lib.sh
T=$1; O=$X/$T; mkdir -p $O; L=$O/take.log; : > $L
case $T in R|T) SRC=$X/P/peg-noshell.FCStd;; M|F) SRC=$X/T/end.FCStd;; P) SRC=$X/F/end.FCStd;; H|Y) SRC=$X/P/peg-trap.FCStd;;
  *) echo "R|H|T|M|F|P|Y"; exit 2;; esac
F=peg
fx_start $O
mkdir -p /tmp/fc14; cp "$SRC" /tmp/fc14/$F.FCStd

prepdoc() {
  FQ "prep('$F')" >> $L 2>&1
  Q "import FreeCAD, FreeCADGui
g = FreeCADGui.getDocument('$F'); g.activeView().setAnimationEnabled(False)
g.getObject('Body').ShapeAppearance = [FreeCAD.Material(DiffuseColor=(0.93, 0.55, 0.20))]
print(1)" >> $L 2>&1
}
if [ "$T" != P ]; then
  open_doc /tmp/fc14/$F.FCStd >> $L 2>&1; prepdoc
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


into() {       # into: the camera turned to look down into the cup at the front wall from behind (the peg's opening)
  sl_mark "view: into the cup"
  Q "import FreeCADGui; v = FreeCADGui.getDocument('$F').activeView(); v.setViewDirection((0.25, -0.7, -1)); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L
  sl_nap 3
}
pm() {         # pm NAME X Z Y: Measure between the peg's side edges at (+-X, Y, Z) in top view
  Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null
  local p; p=$(vp $2 $4 $3 -$2 $4 $3); echo "$1 edges $p" >> $L; set -- "$1" $p
  sl_glide 1500 1650 15; sl_click 1500 1650 "click: empty space (selection cleared)"; sl_nap 1
  btn Std_Measure "Measure"; sl_nap 2
  sl_glide $2 $3 25; sl_nap 0.8; sl_click $2 $3 "$1: first peg side edge"; sl_nap 1.5
  sl_glide $4 $5 25; sl_nap 0.8; xdotool keydown ctrl; sl_click $4 $5 "$1: Ctrl + opposite peg side edge"; xdotool keyup ctrl
  sl_nap 3.5
  echo "$1 measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*\|"QLabel", "[^"]*"' | tr '\n' ' ')" >> $L
  echo "$1 selection: $(selnames)" >> $L
  shot $O/measure-$1.png; sl_nap 3
  at "$(taskpos any Close)" "Measure: Close"; sl_nap 1.5
  Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null
}
ctx() {        # ctx OBJ ITEM: right-click a tree row, click a menu item (positions from the UI watcher; the socket is blocked)
  uiwatch 20; local p m; p=$(ROW $F $1); sl_glide ${p% *} ${p#* } 20; sl_nap 0.5; sl_click ${p% *} ${p#* } "tree: $1"; sl_nap 0.8
  sl_mark "right-click: $1"; xdotool click 3; sl_nap 1.5
  m=$(ui menu "$2"); echo "ctx $1 $2 at $m" >> $L; [ "$m" != none ] || bail "no menu item $2"
  sl_glide ${m% *} ${m#* } 25; sl_nap 0.8; sl_click ${m% *} ${m#* } "menu: $2"; sl_nap 2.5
  echo "after $1 $2: $(bstate $F) ui $(ui dump | cut -c1-200)" >> $L
}
desel() { sl_glide 1500 1650 15; sl_nap 0.3; sl_click 1500 1650 "click: empty space (nothing selected)"; sl_nap 1; }
spacerow() {   # spacerow OBJ LABEL: click a tree row, Space (visibility toggled), click empty space
  local p; p=$(ROW $F $1); sl_glide ${p% *} ${p#* } 20; sl_nap 0.5; sl_click ${p% *} ${p#* } "tree: $1"; sl_nap 0.8
  sl_key space "$2"; sl_nap 1; desel; sl_nap 1.5
}
thick() {      # thick: top face picked, Thickness, "=" Params.wall, "Make thickness inwards" unticked, OK
  Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().setAnimationEnabled(False); print(1)" > /dev/null
  isofit
  Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null
  p=$(vp 0 0 50); sl_glide ${p% *} ${p#* } 25; sl_nap 0.8; sl_click ${p% *} ${p#* } "top face picked"; sl_nap 2
  echo "selection: $(selnames)" >> $L
  if ! selnames | grep -q Face; then
    Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null; sl_nap 1
    sl_click ${p% *} ${p#* } "top face picked (again)"; sl_nap 2; echo "selection 2: $(selnames)" >> $L
  fi
  btn PartDesign_Thickness "Thickness"; sl_nap 4
  echo "panel: $(FQ "task_texts()" | grep -o '"Q[A-Za-z:]*", "[^"]*"\|"list", "[^"]*"' | tr '\n' ' ')" >> $L
  p=$(FQ "field_pos('Thickness')"); [ "$p" != none ] || bail "no Thickness field"
  sl_click $(( ${p% *} - 40 )) ${p#* } "Thickness: click"; xdotool key ctrl+a; sl_nap 0.4
  sl_type "=" "Thickness: typed = (Expression Editor)" 200; sl_nap 2
  sl_type "Params.wall" "Thickness: typed Params.wall" 110; sl_nap 1.5
  sl_key Return "Return: name list closed"; sl_nap 2
  at "$(FQ "expr_ok()")" "Expression Editor: OK"; sl_nap 3
  b=$(cbox) || bail "no checkbox"
  sl_glide ${b% *} ${b#* } 20; sl_nap 1; sl_click ${b% *} ${b#* } "Make thickness inwards: unticked (walls outward, lesson 13)"; sl_nap 3
  echo "box: $(checked)" >> $L
  shot $O/panel.png
  at "$(taskpos any OK)" "OK"; sl_nap 3
  echo "after OK: $(bstate $F)" >> $L
}

if [ "$T" != P ]; then xdotool mousemove 1500 1500; row_open $F Pad001 > /dev/null 2>&1; [ "$T" = R ] && row_open $F Sketch001 > /dev/null 2>&1; xdotool mousemove 1500 1500; sleep 1; fi
sl_record "$O"; sl_mark "recording started: FreeCAD 1.1.4, peg.FCStd ($T)"
sl_nap 3
case $T in
R)
  orbit 6 60
  p=$(ROW $F Sketch001); at "$p" "tree: Sketch001 (the peg's sketch)"; sl_nap 1
  r=$(FQ14 "prop_row('Attachment Offset')"); [ "$r" = none ] && r=$(FQ14 "prop_row('Attachment Support')")
  echo "attach row $r" >> $L; [ "$r" != none ] && { sl_glide ${r% *} ${r#* } 25; sl_mark "hover: the sketch's attachment"; }
  sl_nap 4; shot $O/attach.png; desel
  dblrow Params "double-click: open Params"; sl_nap 1.5
  for r in 0 1 2 3 4 5; do c=$(B cell $r 1); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Params row $((r + 1))"; sl_nap 1.8; done
  shot $O/params.png
  t=$(B tab "$F"); at "$t" "tab: back to the 3D view"; sl_nap 1.5
  orbit 6 60
  ;;
H)
  isofit
  spacerow Thickness "Space: Thickness hidden"
  spacerow Pad "Space: Pad shown (the box)"; sl_nap 2; shot $O/h-pad.png
  spacerow Pad "Space: Pad hidden"
  spacerow Pad001 "Space: Pad001 shown (box + peg)"; sl_nap 2; shot $O/h-pad001.png
  spacerow Pad001 "Space: Pad001 hidden"
  spacerow Thickness "Space: Thickness shown (the last step)"; sl_nap 2; shot $O/h-thickness.png
  echo "H end: $(bstate $F)" >> $L
  ;;
T)
  thick
  isofit; shot $O/trap-iso.png; sl_nap 2
  into; shot $O/trap-into.png; sl_nap 3
  echo "messages: dialogs $(dialogs) notices $(FQ "notices()")" >> $L
  ;;
M)
  topview; sl_nap 1
  pm peg-trap 7 45 -30
  into; shot $O/m-into.png; sl_nap 3
  ;;
F)
  into; sl_nap 2
  p=$(ROW $F Thickness); at "$p" "tree: Thickness"; sl_nap 1; sl_key Delete "Delete: Thickness"; sl_nap 3
  echo "after Delete: $(bstate $F) dialogs $(dialogs)" >> $L
  ctx Pad "Set Tip"
  desel
  thick
  ctx Pad001 "Set Tip"
  desel
  btn Std_Refresh "Recompute"; sl_nap 3
  echo "fixed: $(bstate $F)" >> $L
  isofit; shot $O/fix-iso.png; sl_nap 2
  into; shot $O/fix-into.png; sl_nap 3
  topview; pm peg-fixed 5 45 -30
  echo "messages: dialogs $(dialogs) notices $(FQ "notices()")" >> $L
  ;;
P)
  sl_nap 1
  open_doc /tmp/fc14/$F.FCStd >> $L 2>&1; sl_mark "file reopened: F's saved end file"; prepdoc; report_hide; sl_nap 3
  echo "notices at reopen: $(FQ "notices()")" >> $L
  row_open $F Pad001 >> $L; xdotool mousemove 1500 1500; sl_nap 1
  params_set 3 3 wall
  echo "wall 3: $(bstate $F)" >> $L
  topview; pm peg-w3 5 45 -30
  params_set 4 12 peg_size
  echo "peg 12: $(bstate $F)" >> $L
  topview; pm peg-12 6 46 -30
  isofit; orbit 4 40
  ;;
Y)
  isofit; orbit 24 120
  ;;
esac
sl_nap 2; sl_stop
lab_save $F $O/end.FCStd >> $L 2>&1
echo "TAKE $T DONE" >> $L
fc_quit; sl_display_stop
check14 $O/end.FCStd $O/check.json >> $L
