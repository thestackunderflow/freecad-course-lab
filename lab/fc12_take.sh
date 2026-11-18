#!/bin/bash
# fc12 takes (PLAN 4.2 rev 2.1), FreeCAD 1.1.4 by hand, no AI. Recipes from G0 (out/fc12/G0/VERDICT.txt).
#   FCC_PREFIX=fc12 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fc12_take.sh R|O|T|M|F|P|Y|K
#   R  ring: full window, the stand orbits; Params tab, cursor down the 8 rows, hold on hooks + hook_gap        F3
#   O  ring: double-click PolarPattern; the task panel: Axis, Mode Extent, Length 360°, Occurrences 6 (fx); Cancel  F4
#   T  ring: Params hooks 6 -> 4, Recompute; PolarPattern, Length 240, Tab, OK; iso, top view                  F0 F5 S0
#   M  T's end: top view, Measure the lip edges of hooks 1 and 2 (80)                                           F5
#   F  T's end: PolarPattern, Mode -> Spacing (120 preview held), "=" Params.hook_gap, OK; top; Measure (60)      F1 F7 S2
#   P  F's end opened (reopened file): Params hooks 4 -> 3, Recompute, top, Measure (60); hooks 6, Recompute, top  F9 S2
#   Y  ring orbiting, slow (think-pause footage; never 8 hooks)                                                 F13
#   K  trap (stand-trap): click PolarPattern, Data tab, hover Angle: FreeCAD's description held                F6 S0
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh; . /lab/lab/fc12_lib.sh
T=$1; O=$X/$T; mkdir -p $O; L=$O/take.log; : > $L
case $T in R|O|T|Y) SRC=$X/P/stand-ring.FCStd;; M|F) SRC=$X/T/end.FCStd;; P) SRC=$X/F/end.FCStd;; K) SRC=$X/P/stand-trap.FCStd;;
  *) echo "R|O|T|M|F|P|Y|K"; exit 2;; esac
F=stand
fx_start $O
mkdir -p /tmp/fc12; cp "$SRC" /tmp/fc12/$F.FCStd

prepdoc() {
  FQ "prep('$F')" >> $L 2>&1
  Q "import FreeCAD, FreeCADGui
g = FreeCADGui.getDocument('$F'); g.activeView().setAnimationEnabled(False)
g.getObject('Body').ShapeAppearance = [FreeCAD.Material(DiffuseColor=(0.93, 0.55, 0.20))]
print(1)" >> $L 2>&1
}
if [ "$T" != P ]; then
  open_doc /tmp/fc12/$F.FCStd >> $L 2>&1; prepdoc
  report_hide; sleep 2; xdotool mousemove 1500 1500; rv_clear
fi

orbit() {      # orbit SECONDS DEG: the camera turns round the world Z axis (the post), smoothly
  Q "import FreeCAD, FreeCADGui, time
from PySide import QtWidgets
v = FreeCADGui.getDocument('$F').activeView(); n = int($1 * 30); st = $2 / float(n)
for i in range(n):
    v.setCameraOrientation(FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), st).multiply(v.getCameraOrientation()))
    QtWidgets.QApplication.processEvents(); time.sleep(1 / 30.0)
print(1)" >> $L 2>&1
}
field() {      # field LABEL TEXT: triple-click the task-panel field on row LABEL, type TEXT, Tab
  local p; p=$(FQ "field_pos('$1')"); [ "$p" != none ] || { echo "no field $1" >> $L; return 1; }
  sl_glide $(( ${p% *} - 40 )) ${p#* } 20; sl_nap 0.6
  xdotool click --repeat 3 --delay 90 1; sl_mark "$1: select"; sl_nap 0.4
  sl_type "$2" "$1: typed $2" 220; sl_nap 0.6; sl_key Tab "Tab"; sl_nap 2.5
  echo "$1 = $2: $(pstate $F)" >> $L
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
m() {          # m NAME A1 A2: Measure the angle between the lip tops' radial side edges of the hooks at A1 and A2 (top view)
  local p a b
  a=$(rot 46.5 10 $2); b=$(rot 46.5 10 $3)   # the lip top's radial side edge (G0 s6: tangent edges read 100)
  p=$(vp $a 10 $b 10); echo "$1 edges $p" >> $L; set -- "$1" $p
  btn Std_Measure "Measure"; sl_nap 2
  sl_glide $2 $3 25; sl_nap 0.8; sl_click $2 $3 "$1: first hook, lip edge"; sl_nap 1.5
  sl_glide $4 $5 25; sl_nap 0.8; xdotool keydown ctrl; sl_click $4 $5 "$1: Ctrl + next hook, lip edge"; xdotool keyup ctrl
  sl_nap 3.5
  echo "$1 measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*\|"QLabel", "[^"]*"' | tr '\n' ' ')" >> $L
  echo "$1 selection: $(selnames)" >> $L
  shot $O/measure-$1.png; sl_nap 3
  at "$(taskpos any Close)" "Measure: Close"; sl_nap 1.5
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
params_hooks() {   # params_hooks N: Params tab, cell B7 (hooks) <- N, Enter, Recompute, back to the 3D tab
  dblrow Params "double-click: open Params"
  local c; c=$(B cell 6 1); echo "hooks cell $c" >> $L
  at "$c" "cell B7: hooks"; sl_nap 1
  sl_type "$1" "typed $1" 250; sl_key Return "Enter"; sl_nap 1.5
  shot $O/params-hooks-$1.png
  btn Std_Refresh "Recompute"; sl_nap 3
  local t; t=$(B tab "$F"); at "$t" "tab: back to the 3D view"; sl_nap 2
  echo "hooks $1: $(pstate $F)" >> $L
}

if [ "$T" != P ]; then
  xdotool mousemove 1500 1500
  echo "rows open: $(row_open $F PolarPattern)" >> $L; xdotool mousemove 1500 1500; sleep 1
fi
sl_record "$O"; sl_mark "recording started: FreeCAD 1.1.4, stand.FCStd ($T)"
sl_nap 3
case $T in
R)
  orbit 6 60
  dblrow Params "double-click: open Params"; sl_nap 1.5
  for r in 0 1 2 3 4 5 6 7; do
    c=$(B cell $r 1); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Params row $((r + 1))"; sl_nap 1.6
  done
  c=$(B cell 6 1); sl_glide ${c% *} ${c#* } 15; sl_mark "hold: hooks 6"; sl_nap 3
  c=$(B cell 7 1); sl_glide ${c% *} ${c#* } 15; sl_mark "hold: hook_gap 60 °"; sl_nap 3
  shot $O/params.png
  t=$(B tab "$F"); at "$t" "tab: back to the 3D view"; sl_nap 1.5
  orbit 6 60
  ;;
O)
  dblrow PolarPattern "double-click: PolarPattern (edit)"; sl_nap 1.5
  shot $O/panel.png
  c=$(FQ "combo_pos('Base Z-axis')"); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Axis Base Z-axis"; sl_nap 2.5
  c=$(FQ "combo_pos('Extent')"); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Mode Extent"; sl_nap 2.5
  p=$(FQ "field_pos('Occurrences')"); sl_glide $(( ${p% *} - 40 )) ${p#* } 20; sl_mark "hover: Occurrences 6 (fx: Params.hooks)"; sl_nap 3
  p=$(FQ "field_pos('Length')"); sl_glide $(( ${p% *} - 40 )) ${p#* } 20; sl_mark "hover: Length 360.00°"; sl_nap 3
  echo "panel: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*' | tr '\n' ' ')" >> $L
  orbit 4 40
  at "$(taskpos any Cancel)" "Cancel"; sl_nap 2
  ;;
T)
  params_hooks 4
  dblrow PolarPattern "double-click: PolarPattern (edit)"; sl_nap 1
  field Length 240
  sl_nap 2; shot $O/trap-panel.png
  at "$(taskpos any OK)" "OK"; sl_nap 3
  isofit; shot $O/trap-iso.png; sl_nap 2
  topview; shot $O/trap-top.png; sl_nap 3
  echo "messages: dialogs $(dialogs) notices $(FQ "notices()")" >> $L
  ;;
M)
  topview; sl_nap 1
  m h1-h2 0 80
  ;;
F)
  dblrow PolarPattern "double-click: PolarPattern (edit)"; sl_nap 1
  c=$(FQ "combo_pos('Extent')"); at "$c" "Mode box"; sl_nap 1.5
  at "${c% *} $(( ${c#* } + 42 ))" "Mode: Spacing"; sl_nap 4
  shot $O/spacing-120.png
  echo "switched: $(pstate $F)" >> $L
  p=$(FQ "field_pos('Spacing')"); [ "$p" != none ] || bail "no Spacing field"
  sl_glide $(( ${p% *} - 40 )) ${p#* } 20; sl_nap 0.6
  sl_click $(( ${p% *} - 40 )) ${p#* } "Spacing: click"; xdotool key ctrl+a; sl_nap 0.4
  sl_type "=" "Spacing: typed = (Expression Editor)" 200; sl_nap 2
  sl_type "Params.hook_gap" "Spacing: typed Params.hook_gap" 110; sl_nap 1.5
  sl_key Return "Return: name list closed"; sl_nap 2
  shot $O/expr.png
  at "$(FQ "expr_ok()")" "Expression Editor: OK"; sl_nap 2.5
  echo "expr: $(pstate $F)" >> $L
  shot $O/fix-panel.png
  at "$(taskpos any OK)" "OK"; sl_nap 3
  isofit; shot $O/fix-iso.png; sl_nap 2
  topview; shot $O/fix-top.png
  m h1-h2 0 60
  ;;
P)
  sl_nap 1
  open_doc /tmp/fc12/$F.FCStd >> $L 2>&1; sl_mark "file reopened: F's saved end file"; prepdoc; report_hide; sl_nap 3
  row_open $F PolarPattern >> $L; xdotool mousemove 1500 1500; sl_nap 1
  params_hooks 3
  topview; shot $O/h3-top.png
  m h1-h2 0 60
  params_hooks 6
  topview; shot $O/h6-top.png; sl_nap 2
  isofit; orbit 4 40
  ;;
Y)
  orbit 24 120
  ;;
K)
  p=$(ROW $F PolarPattern); at "$p" "tree: PolarPattern"; sl_nap 2
  r=$(FQ12 "prop_row('Angle')"); echo "Angle row $r" >> $L; [ "$r" != none ] || bail "no Angle row"
  sl_glide $(( ${r% *} - 6 )) $(( ${r#* } + 3 )) 25; sl_nap 0.3; xdotool mousemove ${r% *} ${r#* }; sl_mark "hover: Angle"
  sl_nap 3; echo "tooltip: $(FQ12 "tooltip_text()")" >> $L; shot $O/angle-hover.png; sl_nap 5
  ;;
esac
sl_nap 2; sl_stop
lab_save $F $O/end.FCStd >> $L 2>&1
echo "TAKE $T DONE" >> $L
fc_quit; sl_display_stop
check12 $O/end.FCStd $O/check.json >> $L
