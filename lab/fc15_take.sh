#!/bin/bash
# fc15 takes (PLAN 4.2 rev 2 + G0 out/fc15/G0/VERDICT.txt), FreeCAD 1.1.4 by hand, no AI.
#   FCC_PREFIX=fc15 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fc15_take.sh R|T|F|I|P|S|Y
#   R  rim-start: full window, orbit; Params rows (rim_out, rim_in, wall); zoom to the rim                         F3
#   T  rim-start: one click on the outer rim edge, Fillet, Radius "=" Params.rim_out (3), OK: "Input error" box
#      (G0: "BRep_API: command not done"), its OK; View > Panels > Report view; Cancel (the Fillet is not kept)      F0 F4
#   F  rim-start: Params rim_out 1.5, Recompute; one click, Fillet, "=" Params.rim_out, OK: builds; Measure the flat F7
#   I  F's end: the four inner rim edges, Fillet, "=" Params.rim_in (1), OK: "Input error" box, OK, Cancel           F8
#   P  F's end reopened: Params wall 3, Recompute; inner edges, Fillet, "=" Params.rim_in, OK: builds; Measure the
#      flat; Params wall 2, Recompute: Fillet001 marked (G0 Q4)                                                     F10
#   Y  F's end orbiting slowly (think pause)                                                                       F14
#   (S, the clipping plane, not filmed: G0 Q9, FreeCAD's cut is not filled; the rim zooms stand in)
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh; . /lab/lab/fc12_lib.sh; . /lab/lab/fc13_lib.sh; . /lab/lab/fc14_lib.sh; . /lab/lab/fc15_lib.sh
T=$1; O=$X/$T; mkdir -p $O; L=$O/take.log; : > $L
case $T in R|T|F) SRC=$X/P/rim-start.FCStd;; I|Y|P) SRC=$X/F/end.FCStd;;
  *) echo "R|T|F|I|P|Y"; exit 2;; esac
F=cup
W14=/tmp/fc15-ui.json
fx_start $O
mkdir -p /tmp/fc15; cp "$SRC" /tmp/fc15/$F.FCStd

prepdoc() {
  FQ "prep('$F')" >> $L 2>&1
  Q "import FreeCAD, FreeCADGui
g = FreeCADGui.getDocument('$F'); g.activeView().setAnimationEnabled(False)
g.getObject('Body').ShapeAppearance = [FreeCAD.Material(DiffuseColor=(0.93, 0.55, 0.20))]
print(1)" >> $L 2>&1
}
if [ "$T" != P ]; then
  open_doc /tmp/fc15/$F.FCStd >> $L 2>&1; prepdoc
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
zoomto() {     # zoomto SECONDS VIEW CX CY CZ HEIGHT: the camera glides from where it is to look() at (CX,CY,CZ), HEIGHT mm
  Q "import FreeCAD, FreeCADGui, time
from PySide import QtWidgets
from pivy import coin
v = FreeCADGui.getDocument('$F').activeView(); v.setAnimationEnabled(False); cam = v.getCameraNode()
p0 = FreeCAD.Vector(*cam.position.getValue().getValue()); h0 = cam.height.getValue()
r0 = cam.orientation.getValue()
getattr(v, 'view$2')(); r1 = cam.orientation.getValue(); cam.orientation.setValue(r0)
d = r1.multVec(coin.SbVec3f(0, 0, -1)); c = FreeCAD.Vector($3, $4, $5)
p1 = c - FreeCAD.Vector(d[0], d[1], d[2]) * 200
n = int($1 * 30)
for i in range(1, n + 1):
    t = i / float(n); t = t * t * (3 - 2 * t)
    cam.orientation.setValue(coin.SbRotation.slerp(r0, r1, t))
    p = p0 + (p1 - p0) * t; cam.position.setValue(p.x, p.y, p.z); cam.height.setValue(h0 + ($6 - h0) * t)
    QtWidgets.QApplication.processEvents(); time.sleep(1 / 30.0)
print(1)" >> $L 2>&1
  sl_mark "view: zoomed ($2, ${6} mm high, at $3 $4 $5)"; sl_nap 1
}
isofit() {
  sl_key 0 "key 0: isometric"; sl_nap 0.5
  Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewIsometric(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L
  sl_mark "(view fitted)"; sl_nap 2
}
clr() { Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null; }
bail() { echo "BAIL: $1" >> $L; sl_stop; fc_quit; sl_display_stop; exit 1; }
desel() { sl_glide 1500 1650 15; sl_nap 0.3; sl_click 1500 1650 "click: empty space (nothing selected)"; sl_nap 1; }
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
  echo "$3 $2: $(fstate $F)" >> $L
}
edge_click() {   # edge_click X Y Z LABEL [ctrl]: click the edge through (X,Y,Z) in the current view
  local p; p=$(vp $1 $2 $3); sl_glide ${p% *} ${p#* } 25; sl_nap 0.7
  if [ -n "${5:-}" ]; then xdotool keydown ctrl; sl_click ${p% *} ${p#* } "$4"; xdotool keyup ctrl; else sl_click ${p% *} ${p#* } "$4"; fi
  sl_nap 1.5
}
fillet() {     # fillet NAME: Fillet on the selection, Radius "=" Params.NAME, OK (UI watcher on for a box after OK)
  btn PartDesign_Fillet "Fillet"; sl_nap 4
  echo "panel: $(FQ "task_texts()" | cut -c1-900)" >> $L
  echo "panel list: $(FQ14 "task_list_items()")" >> $L
  shot $O/panel-open.png
  local p; p=$(FQ "field_pos('Radius:')"); [ "$p" = none ] && p=$(FQ "field_pos('Radius')"); [ "$p" != none ] || bail "no Radius field"
  sl_click $(( ${p% *} - 40 )) ${p#* } "Radius: click"; xdotool key ctrl+a; sl_nap 0.4
  sl_type "=" "Radius: typed = (Expression Editor)" 200; sl_nap 2
  sl_type "Params.$1" "Radius: typed Params.$1" 110; sl_nap 1.5
  sl_key Return "Return: name list closed"; sl_nap 2
  at "$(FQ "expr_ok()")" "Expression Editor: OK"; sl_nap 4
  echo "panel after radius: $(FQ "task_texts()" | cut -c1-900)" >> $L
  echo "dialogs before OK: $(dialogs)" >> $L
  shot $O/panel-radius.png
  uiwatch 25
  at "$(taskpos any OK)" "OK"; sl_nap 4
  local u b; u=$(ui dump); echo "ui after OK: $(echo "$u" | cut -c1-900)" >> $L
  FAILED=0
  if echo "$u" | grep -q '"title": "Input error"'; then
    FAILED=1; sl_mark "the box: Input error"; sl_nap 4; shot $O/error-box.png
    b=$(ui button OK); echo "box OK at $b" >> $L
    sl_glide ${b% *} ${b#* } 20; sl_nap 0.8; sl_click ${b% *} ${b#* } "the box: OK"; sl_nap 3
  fi
  echo "dialogs after OK: $(dialogs)" >> $L
  echo "after OK: $(fstate $F)" >> $L
  echo "panel now: $(FQ "task_texts()" | cut -c1-300)" >> $L
}
wb_pd() {      # the workbench list (Spreadsheet after Params) back to Part Design, by clicks
  local c; c=$(FQ "combo_pos('Spreadsheet')"); echo "wb combo $c" >> $L; [ "$c" != none ] || return 0
  uiwatch 15; at "$c" "workbench list"; sl_nap 1.5
  local p; p=$(FQ "popup_pos('Part Design')")
  case "$p" in ""|none) p=$(ui popup "Part Design");; esac
  case "$p" in ""|none) p=$(ui menu "Part Design");; esac
  echo "wb Part Design at $p; ui: $(ui dump | cut -c1-400)" >> $L
  case "$p" in ""|none) xdotool key Escape; bail "workbench Part Design not found";; esac
  at "$p" "workbench: Part Design"; sl_nap 2.5
}
inner4() {     # the four inner rim edges clicked (Ctrl from the second); by-code selection only if a click missed (logged)
  edge_click 30 5 50 "click: inner rim edge 1"
  edge_click 5 20 50 "Ctrl + click: inner rim edge 2" ctrl
  edge_click -30 5 50 "Ctrl + click: inner rim edge 3" ctrl
  edge_click 5 -20 50 "Ctrl + click: inner rim edge 4" ctrl
  local sel; sel=$(selnames); echo "selection: $sel" >> $L
  local want; want=$(Q "import FreeCAD
s = FreeCAD.getDocument('$F').getObject('Body').Tip.Shape
print(sorted('Edge%d' % i for i, e in enumerate(s.Edges, 1) if all(abs(v.Point.z - 50) < 1e-6 for v in e.Vertexes) and e.Curve.__class__.__name__ == 'Line' and all(abs(v.Point.x) <= 30.0001 and abs(v.Point.y) <= 20.0001 for v in e.Vertexes)))")
  echo "inner edges by code: $want" >> $L
  python3 - "$sel" "$want" <<'PY' || { echo "SELECTION FIXED BY CODE (a click missed)" >> $L; Q "import FreeCADGui, FreeCAD
FreeCADGui.Selection.clearSelection(); tip = FreeCAD.getDocument('$F').getObject('Body').Tip.Name
for n in $want: FreeCADGui.Selection.addSelection('$F', tip, n)
print(1)" >> $L; }
import ast, sys
sel = ast.literal_eval(sys.argv[1]); want = ast.literal_eval(sys.argv[2])
got = sorted(x for _, subs in sel for x in subs)
sys.exit(0 if got == want else 1)
PY
}
report_open() {  # View > Panels > Report view, by clicks (menu rows from the UI watcher)
  local p m
  p=$(menubar_pos View); echo "menubar View $p" >> $L; [ "$p" != none ] || return 1
  uiwatch 20; sl_glide ${p% *} ${p#* } 20; sl_nap 0.5; sl_click ${p% *} ${p#* } "menu: View"; sl_nap 1.5
  m=$(ui menu Panels); echo "Panels at $m" >> $L; [ "$m" != none ] || { xdotool key Escape; return 1; }
  sl_glide ${m% *} ${m#* } 20; sl_nap 1.5
  m=$(ui menu "Report view"); echo "Report view at $m" >> $L; [ "$m" != none ] || { xdotool key Escape; xdotool key Escape; return 1; }
  sl_glide $(( ${m% *} - 60 )) ${m#* } 10; sl_glide ${m% *} ${m#* } 15; sl_nap 0.6; sl_click ${m% *} ${m#* } "menu: Report view"; sl_nap 3
}
mflat() {      # mflat NAME X1 X2: top view zoomed on the rim at y 0, Measure between the edges at (X1, 0, 50) and (X2, 0, 50)
  clr; zoomto 3 Top $(python3 -c "print(($2 + $3) / 2)") 0 50 3
  local p; p=$(vp $2 0 50 $3 0 50); echo "$1 edges $p" >> $L; set -- "$1" $p
  btn Std_Measure "Measure"; sl_nap 2
  sl_glide $2 $3 25; sl_nap 0.8; sl_click $2 $3 "$1: the flat's inner edge"; sl_nap 1.5
  sl_glide $4 $5 25; sl_nap 0.8; xdotool keydown ctrl; sl_click $4 $5 "$1: Ctrl + the flat's outer edge (where the round starts)"; xdotool keyup ctrl
  sl_nap 3.5
  echo "$1 measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*\|"QLabel", "[^"]*"' | tr '\n' ' ')" >> $L
  echo "$1 selection: $(selnames)" >> $L
  shot $O/measure-$1.png; sl_nap 3
  at "$(taskpos any Close)" "Measure: Close"; sl_nap 1.5
  clr
}

[ "$T" != P ] && { xdotool mousemove 1500 1500; row_open $F Fillet > /dev/null 2>&1; row_open $F Pad001 > /dev/null 2>&1; xdotool mousemove 1500 1500; sleep 1; }
sl_record "$O"; sl_mark "recording started: FreeCAD 1.1.4, cup.FCStd ($T)"
sl_nap 3
case $T in
R)
  orbit 6 60
  dblrow Params "double-click: open Params"; sl_nap 1.5
  for r in 3 6 7; do c=$(B cell $r 1); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Params row $((r + 1))"; sl_nap 2; done
  shot $O/params.png
  t=$(B tab "$F"); at "$t" "tab: back to the 3D view"; sl_nap 1.5
  isofit; zoomto 4 Isometric 31 0 50 12; sl_nap 3; shot $O/rim-zoom.png
  isofit; orbit 4 40
  ;;
T)
  isofit; clr
  edge_click 32 5 50 "click: the outer rim edge (one click)"
  echo "selection: $(selnames)" >> $L
  selnames | grep -q Edge || { clr; edge_click 32 5 50 "click: the outer rim edge (again)"; echo "selection 2: $(selnames)" >> $L; }
  fillet rim_out
  [ $FAILED = 1 ] || echo "T: NO ERROR BOX" >> $L
  shot $O/after-box.png; sl_nap 2
  report_open || echo "report_open failed" >> $L
  sl_nap 2; echo "report: $(report_text)" >> $L; shot $O/trap-report.png; sl_nap 4
  at "$(taskpos any Cancel)" "Cancel"; sl_nap 3
  echo "after Cancel: $(fstate $F)" >> $L
  isofit; sl_nap 2; shot $O/trap-end.png
  ;;
F)
  isofit
  params_set 6 1.5 rim_out
  wb_pd
  isofit; clr
  edge_click 32 5 50 "click: the outer rim edge (one click)"
  echo "selection: $(selnames)" >> $L
  fillet rim_out
  [ $FAILED = 0 ] || echo "F: ERROR BOX" >> $L
  isofit; sl_nap 2; shot $O/fix-iso.png
  zoomto 4 Isometric 31 0 50 12; sl_nap 3; shot $O/fix-rim.png
  mflat flat-w2 30 30.5
  isofit; sl_nap 1
  ;;
I)
  isofit; zoomto 3 Isometric 0 0 45 52; clr
  inner4
  fillet rim_in
  [ $FAILED = 1 ] || echo "I: NO ERROR BOX" >> $L
  sl_nap 2
  at "$(taskpos any Cancel)" "Cancel"; sl_nap 3
  echo "after Cancel: $(fstate $F)" >> $L
  isofit; sl_nap 2
  ;;
P)
  sl_nap 1
  open_doc /tmp/fc15/$F.FCStd >> $L 2>&1; sl_mark "file reopened: F's saved end file (rim_out 1.5)"; prepdoc; report_hide; sl_nap 3
  echo "notices at reopen: $(FQ "notices()")" >> $L
  row_open $F Fillet >> $L; xdotool mousemove 1500 1500; sl_nap 1
  echo "reopened: $(fstate $F)" >> $L
  params_set 3 3 wall
  wb_pd
  isofit; zoomto 3 Isometric 0 0 45 54; clr
  inner4
  fillet rim_in
  [ $FAILED = 0 ] || echo "P: ERROR BOX at wall 3" >> $L
  isofit; zoomto 4 Isometric 32 0 50 12; sl_nap 3; shot $O/w3-rim.png
  mflat flat-w3 31 31.5
  isofit; sl_nap 1
  row_open $F Fillet001 >> $L; xdotool mousemove 1500 1500
  params_set 3 2 wall
  isofit; sl_nap 2; shot $O/w2-iso.png
  p=$(ROW $F Fillet001); sl_glide ${p% *} ${p#* } 20; sl_mark "hover: the Fillet001 row (its mark)"; sl_nap 3; shot $O/w2-tree.png
  echo "tooltip: $(FQ12 "tooltip_text()" 2>/dev/null)" >> $L
  zoomto 4 Isometric 31 0 50 12; sl_nap 3; shot $O/w2-rim.png
  ;;
Y)
  isofit; orbit 24 120
  ;;
esac
sl_nap 2; sl_stop
lab_save $F $O/end.FCStd >> $L 2>&1
echo "TAKE $T DONE" >> $L
fc_quit; sl_display_stop
check15 $O/end.FCStd $O/check.json >> $L
