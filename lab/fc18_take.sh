#!/bin/bash
# fc18 takes (PLAN 2026-11-21-cad-lesson-18 4.2 rev 2, HANDOVER-L18-film.md), FreeCAD 1.1.4 by hand, no AI.
# Copied from lab/fc17_take.sh (keeps wb_pd: the workbench list back to Part Design after Params, lesson 15's fix).
#   FCC_PREFIX=fc18 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fc18_take.sh R|D|T|S|F|P|Y|Q7
#   R  the lesson 16 wall cup orbiting, then round-start: full window, Params rows (cup_diameter, cup_height, wall) F3
#   D  round-start: Create sketch, XZ_Plane, the vertical sketch axis lit; the 6 lines from the origin (polyline);
#      height =Params.cup_height (outside line), rim and floor =Params.wall: 1 DoF left (the width)              F4
#   T  D's end: floor line K D "=Params.cup_diameter"; Close; Revolve (panel words, Axis / Type rows, Q2 Q5 Q8);
#      OK; Measure the outer rim edge (Q3)                                                                    F0 F5
#   S  round-name + round-fixed, Window > Tile, the same view and zoom (Q11)                                  F0 F7
#   F  T's end: sketch opened, the width size double-clicked, "=" , Params.cup_diameter / 2 (Q4); Close; Measure F1 F8
#   P  F's end reopened (films into out/fc18/K: out/fc18/P holds the start files): cup_diameter 80; Measure   F9
#   Y  F's end orbiting slowly (think pause)                                                                   F14
#   Q7 round-fixed: in the sketch, outside line + vertical axis, Diameter tool, then Dimension (K D); not saved
#   C  Claude's two saved files (runs/A1, runs/B1 after-cup), each: full window 3 s, cup_diameter 80, Recompute,
#      Measure the outer rim edge (Radius 40.00 expected), hold 4 s; copies in /tmp, nothing saved          F13
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh; . /lab/lab/fc12_lib.sh; . /lab/lab/fc13_lib.sh; . /lab/lab/fc14_lib.sh; . /lab/lab/fc15_lib.sh; . /lab/lab/fc16_lib.sh; . /lab/lab/fc17_lib.sh; . /lab/lab/fc18_lib.sh
T=$1; TD=$T; [ "$T" = P ] && TD=K   # take P films into out/fc18/K: out/fc18/P holds the start files
X=$X18; O=$X/$TD; mkdir -p $O; L=$O/take.log; : > $L
case $T in R|D|S) SRC=$X/P/round-start.FCStd;; T) SRC=$X/D/end.FCStd;; F) SRC=$X/T/end.FCStd;; P|Y) SRC=$X/F/end.FCStd;;
  Q7) SRC=$X/P/round-fixed.FCStd;; C) SRC=$X/runs/A1/after-cup.FCStd;; *) echo "R|D|T|S|F|P|Y|Q7|C"; exit 2;; esac
[ -f "$SRC" ] || { echo "no $SRC"; exit 2; }
F=cup; [ "$T" = C ] && { F=a1; [ -f $X/runs/B1/after-cup.FCStd ] || { echo "no B1 file"; exit 2; }; }
W14=/tmp/fc18-ui.json
fx_start $O
mkdir -p /tmp/fc18; cp "$SRC" /tmp/fc18/$F.FCStd   # the take works on a copy in /tmp: never on a start file
[ "$T" = C ] && cp $X/runs/B1/after-cup.FCStd /tmp/fc18/b1.FCStd

prepdoc() {    # prepdoc DOC: tip shown, orange, no animation
  FQ "prep('$1')" >> $L 2>&1
  Q "import FreeCAD, FreeCADGui
g = FreeCADGui.getDocument('$1'); g.activeView().setAnimationEnabled(False)
for b in [o for o in FreeCAD.getDocument('$1').Objects if o.TypeId == 'PartDesign::Body']:
    g.getObject(b.Name).ShapeAppearance = [FreeCAD.Material(DiffuseColor=(0.93, 0.55, 0.20))]
print(1)" >> $L 2>&1
}
cst() { FQ18 "cstate('${1:-$F}')"; }
ski() { FQ18 "skinfo('${1:-$F}')"; }
orbit() {      # orbit SECONDS DEG [DOC]: the camera turns round the world Z axis, smoothly
  Q "import FreeCAD, FreeCADGui, time
from PySide import QtWidgets
v = FreeCADGui.getDocument('${3:-$F}').activeView(); n = int($1 * 30); st = $2 / float(n)
for i in range(n):
    v.setCameraOrientation(FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), st).multiply(v.getCameraOrientation()))
    QtWidgets.QApplication.processEvents(); time.sleep(1 / 30.0)
print(1)" >> $L 2>&1
}
isofit() {
  sl_key 0 "key 0: isometric"; sl_nap 0.5
  Q "import FreeCADGui; FreeCADGui.ActiveDocument.ActiveView.viewIsometric(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L
  sl_mark "(view fitted)"; sl_nap 2
}
clr() { Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null; }
bail() { echo "BAIL: $1" >> $L; shot $O/bail.png; sl_stop; fc_quit; sl_display_stop; exit 1; }
wins() { echo "windows: $(xdotool search --onlyvisible --name '.' getwindowname %@ 2>/dev/null | grep -v -E '^(FreeCAD 1.1.4|)$' | sort -u | tr '\n' '|')" >> $L; }
dblrow() {     # dblrow OBJ LABEL: double-click a tree row
  local p; p=$(ROW $F "$1"); sl_glide ${p% *} ${p#* } 20; sl_nap 0.5
  sl_mark "$2"; xdotool click --repeat 2 --delay 120 1; sl_nap 3
}
wb_pd() {      # the workbench list (Spreadsheet after Params) back to Part Design, by clicks
  local c; c=$(FQ "combo_pos('Spreadsheet')"); echo "wb combo $c" >> $L; [ "$c" != none ] || return 0
  uiwatch 15; at "$c" "workbench list"; sl_nap 1.5
  local p; p=$(ui popup "Part Design")
  case "$p" in ""|none) p=$(ui menu "Part Design");; esac
  case "$p" in ""|none) xdotool key Escape; bail "workbench Part Design not found";; esac
  at "$p" "workbench: Part Design"; sl_nap 2.5
}
params_rows() {   # Params opened, rows 1-3 hovered, back to the 3D view, workbench back to Part Design
  dblrow Params "double-click: open Params"; sl_nap 1.5
  for r in 0 1 2; do c=$(B cell $r 1); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Params row $((r + 1))"; sl_nap 2.2; done
  shot $O/params.png
  t=$(B tab "$F"); at "$t" "tab: back to the 3D view"; sl_nap 1.5
  wb_pd
}
params_set() {   # params_set ROW VALUE NAME: Params tab, cell B(ROW+1) <- VALUE, Enter, Recompute, back to the 3D tab
  dblrow Params "double-click: open Params"
  local c; c=$(B cell $1 1)
  at "$c" "cell B$(( $1 + 1 )): $3"; sl_nap 1
  sl_type "$2" "typed $2" 250; sl_key Return "Enter"; sl_nap 1.5
  shot $O/params-$3-$2.png
  btn Std_Refresh "Recompute"; sl_nap 3
  local t; t=$(B tab "$F"); at "$t" "tab: back to the 3D view"; sl_nap 2
  echo "$3 $2: $(cst)" >> $L
}
# --- sketch helpers (positions read from the sketch each time: the Sketcher moves lines as sizes are pinned)
skpt() { FQ18 "skp('$F', 'Sketch', $1, $2)"; }
skv() { FQ18 "skview('$F', 'Sketch', $1, $2, $3)" >> $L; sl_mark "(sketch view set)"; sl_nap 1.5; }
skclose() { at "$(B text Close)" "sketch: Close"; sl_nap 3; }
okbox() {      # okbox: where the "Insert Length" box is (OK at +135 +190, G0 of lesson 11); no lab query while up
  local g; g=$(xdotool search --onlyvisible --name 'Insert Length' getwindowgeometry 2>/dev/null | tr '\n' ' ')
  echo "box: $g" >> $L; [ -n "$g" ] || bail "no Insert Length box"
  read -r BOXX BOXY < <(echo "$g" | sed -E 's/.*Position: ([0-9]+),([0-9]+).*/\1 \2/')
}
kd() {         # kd LABEL [KEY]: K D (Dimension, a length), or KEY alone: L Horizontal Dimension, I Vertical Dimension (1.1.4 shortcuts; signed: K D lengths let the rim fold outward, probe-flip)
  sl_glide 1800 1300 15; if [ -n "${2:-}" ]; then sl_key $2 "key ${2^^}: $1"; else sl_key k "key K"; sleep 0.3; sl_key d "key D: $1"; fi; sl_nap 3; okbox; }
boxok() { sl_glide $((BOXX + 135)) $((BOXY + 190)) 20; sl_nap 0.8; sl_click $((BOXX + 135)) $((BOXY + 190)) "box: OK${1:-}"; }
lineclick() {  # lineclick GEO WHERE LABEL
  local p; p=$(SP $F Sketch $1 $2 0 0); sl_glide ${p% *} ${p#* } 20; sl_nap 0.6; sl_click ${p% *} ${p#* } "$3"; sl_nap 1.5
  echo "sel: $(selnames)" >> $L
}
exprbox() {    # exprbox EXPR LABEL: in the open box, "=" opens the Expression editor; EXPR typed; Enter
  wins; sl_type "=" "typed = (the expression editor opens)" 250; sl_nap 1.5; wins; shot $O/expr-open-$2.png
  if [ "${3:-}" = replace ]; then sl_key ctrl+a "Ctrl+A: select the expression"; sl_nap 0.8; fi
  sl_type "$1" "typed $1" 160; sl_nap 2.5; shot $O/expr-$2.png
  sl_key Return "Enter: expression"; sl_nap 1.5; wins
  if [ "$(xdotool search --onlyvisible --name 'Expression' 2>/dev/null | wc -l)" -gt 0 ]; then sl_key Return "Enter: expression editor"; sl_nap 1.5; fi
  shot $O/box-$2.png; sl_mark "hold: the box with the expression"; sl_nap 2.5
}
dim() {        # dim GEO EXPR NAME KEY: click a line, K + KEY (l horizontal | i vertical distance), the expression, OK
  lineclick $1 mid "click: the $3 line"
  kd "Insert Length box ($3)" $4; exprbox "$2" "$3"; boxok " ($3)"; sl_nap 2.5
  echo "after $3: $(ski)" >> $L
}
meas_r() {     # meas_r NAME R ZTOP: Measure, a click on the outer rim edge (front), Mode / Result read off the panel
  clr; isofit; sl_nap 1
  btn Std_Measure "Measure"; sl_nap 2
  local p; p=$(vp $(python3 -c "print($2 * 0.7071, -$2 * 0.7071, $3)")); sl_glide ${p% *} ${p#* } 25; sl_nap 0.8
  sl_click ${p% *} ${p#* } "$1: the outer rim edge"; sl_nap 3
  echo "$1 selection: $(selnames)" >> $L
  echo "$1 measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*\|"QLabel", "[^"]*"' | tr '\n' ' ')" >> $L
  shot $O/measure-$1.png; sl_mark "hold: the readout"; sl_nap 4
  if [ "${4:-}" = modes ]; then
    local cur; cur=$(FQ "task_texts()" | python3 -c "import json,sys
d = [x[1][6:] for x in json.load(sys.stdin) if x[1].startswith('combo:')]; print(d[0] if d else 'none')")
    echo "mode combo shows $cur" >> $L; [ "$cur" = none ] || combo_rows "$cur" Mode
  fi
  at "$(taskpos any Close)" "Measure: Close"; sl_nap 1.5
  clr
}
combo_rows() { # combo_rows CURRENT NAME: open a task-panel list, log its rows, close it with Escape
  local c; c=$(FQ "combo_pos('$1')"); echo "$2 combo at $c" >> $L; [ "$c" != none ] || return 0
  uiwatch 12; at "$c" "$2 list"; sl_nap 2.5
  echo "$2 rows: $(ui dump | python3 -c "import json,sys; print(json.load(sys.stdin).get('popup'))" | cut -c1-800)" >> $L
  shot $O/list-$2.png
  local r; r=$(ui popup "$1"); case "$r" in ""|none) bail "$2 list: no row $1";; esac
  sl_glide ${r% *} ${r#* } 15; sl_nap 0.6; sl_click ${r% *} ${r#* } "$2 list: $1 kept"; sl_nap 1.5
}

if [ "$T" != P ] && [ "$T" != S ] && [ "$T" != R ]; then
  open_doc /tmp/fc18/$F.FCStd >> $L 2>&1; prepdoc $F
  report_hide; sl_nap 2; xdotool mousemove 1500 1500; rv_clear
  echo "start: $(cst)" >> $L; echo "start sketch: $(ski)" >> $L
  case $T in F|Q7) row_open $F Sketch > /dev/null 2>&1; xdotool mousemove 1500 1500; sleep 1;; esac
fi
if [ "$T" = R ]; then
  cp $(dirname $X)/fc16/P/hole-fixed.FCStd /tmp/fc18/wallcup.FCStd
  open_doc /tmp/fc18/wallcup.FCStd >> $L 2>&1; FQ "prep('wallcup')" >> $L 2>&1
  report_hide; sl_nap 2; xdotool mousemove 1500 1500; rv_clear
fi
if [ "$T" = S ]; then
  cp $X/P/round-name.FCStd /tmp/fc18/name.FCStd; cp $X/P/round-fixed.FCStd /tmp/fc18/fixed.FCStd
  open_doc /tmp/fc18/name.FCStd >> $L 2>&1; prepdoc name; open_doc /tmp/fc18/fixed.FCStd >> $L 2>&1; prepdoc fixed
  report_hide; sl_nap 2; xdotool mousemove 1500 1500; rv_clear
  echo "name: $(cst name)" >> $L; echo "fixed: $(cst fixed)" >> $L
  Q "import FreeCAD, FreeCADGui
from PySide import QtWidgets
for n in ('name', 'fixed'):
    g = FreeCADGui.getDocument(n); b = FreeCAD.getDocument(n).getObject('Body')
    for v in g.mdiViewsOfType('Gui::View3DInventor'): v.setActiveObject('pdbody', b)
for a in FreeCADGui.getMainWindow().findChildren(QtWidgets.QMdiArea):
    for w in a.subWindowList():
        if w.windowTitle().startswith('Start'): w.close()
print(1)" >> $L 2>&1   # not filmed: the Start page closed, each Body active (no "Start Part" panel)
fi
echo "notices at open: $(FQ "notices()")" >> $L
sl_record "$O"; sl_mark "recording started: FreeCAD 1.1.4 ($T)"
sl_nap 3
case $T in
R)
  orbit 6 60 wallcup; sl_nap 1
  open_doc /tmp/fc18/$F.FCStd >> $L 2>&1; sl_mark "file opened: round-start (the new file)"; prepdoc $F; report_hide; sl_nap 2
  echo "start: $(cst)" >> $L
  params_rows
  isofit; sl_nap 3
  ;;
D)
  isofit; sl_nap 1
  echo "NewSketch: $(FQ18 "cmdinfo('PartDesign_NewSketch')")" >> $L
  dblrow Body "double-click: Cup (the active body)"; sl_nap 1
  btn PartDesign_CompSketches "Create sketch" || bail "no Create sketch button"; sl_nap 3
  FQ "task_texts()" | cut -c1-1500 > $O/panel-newsketch.json; shot $O/panel-newsketch.png
  p=$(FQ "task_texts()" | python3 -c "import json,sys
d = [x for x in json.load(sys.stdin) if x[1].startswith('XZ') and x[2]]
print(' '.join(map(str, d[0][2])) if d else 'none')"); [ "$p" != none ] || bail "no XZ row"
  at "$p" "plane list: XZ_Plane"; sl_nap 2
  at "$(taskpos any OK)" "OK"; sl_nap 4
  echo "sketch made: $(ski)" >> $L
  skv 15 40 115; sl_nap 1
  p=$(skpt 0 95); sl_glide ${p% *} ${p#* } 25; sl_mark "hover: the vertical sketch axis (lit)"; sl_nap 3; shot $O/axis-lit.png
  echo "DistanceX: $(FQ18 "cmdinfo('Sketcher_ConstrainDistanceX')") DistanceY: $(FQ18 "cmdinfo('Sketcher_ConstrainDistanceY')")" >> $L
  echo "Polyline: $(FQ18 "cmdinfo('Sketcher_CreatePolyline')")" >> $L
  btn Sketcher_CreatePolyline "Polyline tool" || { sl_key g "key G"; sleep 0.3; sl_key m "key M: Polyline"; }; sl_nap 2
  n=0
  for uv in "0 0 origin" "30 0 floor" "30 80 outside" "24 80 rim" "24 6 inside" "0 6 floor_top" "0 0 centre_line"; do
    set -- $uv; p=$(skpt $1 $2)
    sl_glide ${p% *} ${p#* } 30; sl_nap 1.2; sl_click ${p% *} ${p#* } "polyline: $3 ($1, $2)"; sl_nap 1.2; n=$((n + 1))
  done
  sl_nap 1; sl_key Escape "Escape: polyline tool off"; sl_nap 2; xdotool mousemove 1800 1300
  echo "drawn: $(ski)" >> $L; echo "solver drawn: $(solver_text)" >> $L; shot $O/drawn.png
  sl_mark "hold: the 6 lines drawn"; sl_nap 2.5
  dim 1 "Params.cup_height" height i
  dim 2 "Params.wall" rim l
  dim 5 "Params.wall" floor i
  xdotool mousemove 1800 1300; sl_mark "hold: 1 degree of freedom left (the width)"; sl_nap 4
  echo "solver end: $(solver_text)" >> $L; shot $O/one-dof.png
  ;;
T)
  dblrow Sketch "double-click: Sketch (edit)"; sl_nap 1; skv 30 40 115
  dim 0 "Params.cup_diameter" width l
  xdotool mousemove 1800 1300; sl_mark "hold: fully constrained, width reads 60"; sl_nap 3
  echo "solver: $(solver_text)" >> $L; shot $O/width60.png
  skclose; isofit
  p=$(ROW $F Sketch); at "$p" "tree: Sketch"; sl_nap 1.5; echo "selection: $(selnames)" >> $L
  echo "Revolution cmd: $(FQ18 "cmdinfo('PartDesign_Revolution')")" >> $L
  p=$(B PartDesign_Revolution); sl_glide ${p% *} ${p#* } 25; sl_mark "hover: Revolve (tooltip)"; sl_nap 3; shot $O/revolve-tooltip.png
  btn PartDesign_Revolution "Revolve" || bail "no Revolve button"; sl_nap 4
  FQ "task_texts()" | cut -c1-2500 > $O/panel-revolve.json; shot $O/panel-revolve.png
  echo "preview: $(cst)" >> $L
  Q "import FreeCADGui; FreeCADGui.ActiveDocument.ActiveView.viewIsometric(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L; sl_mark "(view fitted, no key: key 0 would type into the Angle field)"; sl_nap 1; sl_mark "hold: the preview (no click yet)"; sl_nap 3; shot $O/preview.png
  FQ "task_texts()" | cut -c1-2500 > $O/panel-revolve-ok.json
  at "$(taskpos any OK)" "OK"; sl_nap 4
  echo "after OK: $(cst)" >> $L; echo "notices: $(FQ "notices()")" >> $L; echo "tree: $(treestate $F 2>/dev/null | cut -c1-600)" >> $L
  isofit; orbit 4 60; sl_nap 1
  meas_r trap120 60 80 modes
  isofit
  ;;
S)
  m=$(menubar_pos "Windows"); [ "$m" != none ] || bail "no Windows menu"
  uiwatch 15; at "$m" "menu: Windows"; sl_nap 1.8
  echo "Windows menu: $(ui dump | cut -c1-900)" >> $L
  s=$(ui menu "Tile"); [ "$s" != none ] || { xdotool key Escape; bail "no Tile"; }
  sl_glide ${s% *} ${s#* } 15; sl_nap 0.8; sl_click ${s% *} ${s#* } "menu: Tile"; sl_nap 3
  # render 1 (22 Nov): the stale "Start Part" task panel stayed drawn over the 120 cup's rim (right view): make each
  # file's Cup the active body (the Part Design watcher then drops the panel) and close any open task dialog
  # render 2 (22 Nov): setActiveObject raised "No SWIG wrapped library loaded" and the panel stayed; the Cup is already
  # the active body (green), so hide the Tasks dock itself through Qt (the same as its close button)
  Q "import FreeCADGui
from PySide import QtGui
n = 0
for w in FreeCADGui.getMainWindow().findChildren(QtGui.QDockWidget):
    if w.windowTitle() in ('Tasks', 'Combo View') or w.objectName() in ('Tasks', 'TaskView', 'Combo View'):
        w.hide(); n += 1
print('docks hidden', n)" >> $L 2>&1
  for d in name fixed; do FQ "look('$d', 'Isometric', 0, 0, 40, 170)" >> $L; done
  sl_mark "(both views: isometric, 170 mm high)"; sl_nap 6; shot $O/side-by-side.png
  ;;
F)
  dblrow Sketch "double-click: Sketch (edit)"; sl_nap 1; skv 30 40 115
  i=$(Q "import FreeCAD
s = FreeCAD.getDocument('$F').getObject('Sketch'); e = dict(s.ExpressionEngine)
print([int(k.split('[')[1].rstrip(']')) for k, v in e.items() if 'cup_diameter' in v and '[' in k][0])")
  echo "width constraint index $i" >> $L
  p=$(cd /lab && timeout 20 python3 -m lab.dimpt $F Sketch $i); sl_glide ${p% *} ${p#* } 20; sl_nap 0.8
  sl_mark "double-click: the width (60)"; xdotool click --repeat 2 --delay 120 1; sl_nap 3
  okbox; shot $O/box-width-open.png; sl_mark "hold: the box, bound to Params.cup_diameter"; sl_nap 2.5
  exprbox "Params.cup_diameter / 2" half replace
  boxok " (width)"; sl_nap 2.5
  echo "after half: $(ski)" >> $L; xdotool mousemove 1800 1300
  sl_mark "hold: width reads 30"; sl_nap 3; shot $O/width30.png
  skclose; isofit; sl_nap 1
  echo "after close: $(cst)" >> $L
  meas_r fix60 30 80
  isofit
  ;;
P)
  sl_nap 1
  open_doc /tmp/fc18/$F.FCStd >> $L 2>&1; sl_mark "file reopened: F's saved end file"; prepdoc $F; report_hide; sl_nap 3
  echo "notices at reopen: $(FQ "notices()")" >> $L; echo "reopened: $(cst)" >> $L
  isofit
  params_set 0 80 cup_diameter; wb_pd
  meas_r proof80 40 80
  isofit
  ;;
Y)
  isofit; orbit 24 120
  ;;
Q7)
  dblrow Sketch "double-click: Sketch (edit)"; sl_nap 1; skv 30 40 115
  lineclick 1 mid "click: the outside line"
  p=$(skpt 0 95); sl_glide ${p% *} ${p#* } 20; sl_nap 0.6; sl_click ${p% *} ${p#* } "click: the vertical axis"; sl_nap 1.5
  echo "sel: $(selnames)" >> $L
  echo "Diameter cmd: $(FQ18 "cmdinfo('Sketcher_ConstrainDiameter')")" >> $L
  Q "import FreeCADGui; FreeCADGui.runCommand('Sketcher_ConstrainDiameter'); print(1)" >> $L 2>&1 &
  sl_mark "Diameter tool (Q7)"; sl_nap 3; wins; shot $O/q7-diameter.png
  sl_key Return "Return: message closed"; sl_nap 2; wins; echo "after diameter: $(ski)" >> $L
  clr; lineclick 1 mid "click: the outside line"
  sl_glide ${p% *} ${p#* } 20; sl_nap 0.6; sl_click ${p% *} ${p#* } "click: the vertical axis"; sl_nap 1.5
  echo "sel: $(selnames)" >> $L
  sl_glide 1800 1300 15; sl_key k "key K"; sleep 0.3; sl_key d "key D: Dimension (Q7)"; sl_nap 3; wins; shot $O/q7-dimension.png
  sl_key Escape "Escape"; sl_nap 2; wins; echo "after dimension: $(ski)" >> $L
  ;;
C)
  for d in a1 b1; do
    if [ $d = b1 ]; then
      Q "import FreeCAD; FreeCAD.closeDocument('a1'); print(1)" >> $L 2>&1; sl_mark "a1 closed"; sl_nap 1
      F=b1; open_doc /tmp/fc18/b1.FCStd >> $L 2>&1; sl_mark "file opened: b1"; prepdoc b1; report_hide; sl_nap 1
      xdotool mousemove 1500 1500; echo "start b1: $(cst)" >> $L
    fi
    isofit; sl_mark "hold: $d full window"; sl_nap 3
    params_set 0 80 cup_diameter; wb_pd
    meas_r ${d}_80 40 80
    isofit; sl_nap 1
  done
  ;;
esac
sl_nap 2; sl_stop
[ "$T" = Q7 ] || [ "$T" = S ] || [ "$T" = C ] || lab_save $F $O/end.FCStd >> $L 2>&1
echo "end: $(cst 2>/dev/null)" >> $L
echo "TAKE $T DONE" >> $L
fc_quit; sl_display_stop
[ -e $O/end.FCStd ] && check18 $O/end.FCStd $O/check.json >> $L
true
