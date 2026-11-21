#!/bin/bash
# fc17 takes (PLAN 2026-11-21-cad-lesson-17 4.2 rev 2, start files without the rim), FreeCAD 1.1.4 by hand, no AI.
# Copied from lab/fc16_take.sh (keeps wb_pd: the workbench list back to Part Design after Params, lesson 15's fix).
#   FCC_PREFIX=fc17 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fc17_take.sh R|T|F|P|Y
#   R  peg-moved: full window, orbit; Params rows (wall, peg_x 15); front view; Q5 a 3D click on the peg      F3
#   T  peg-moved: Pad001 picked in the tree; Part Design > Transformation Features > Mirror; the panel's first
#      plane + preview held (Q3); Plane list -> Base XZ-plane; OK; back view; Measure 13 (copy tip to back wall)
#      and 70 (front tip to back tip) (Q7)                                                                     F4 F5
#   F  T's end: right-click Mirrored (menu words, Q8), its Edit item; Plane list -> Base YZ-plane; OK; front view;
#      Measure 20 (inner edges) and 57 (front tip to back wall); back view clear                               F7 F8
#   P  F's end reopened (films into out/fc17/K: out/fc17/P holds the start files): peg_x 20, peg_size 12, wall 3
#   Y  F's end orbiting slowly (think pause)
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh; . /lab/lab/fc12_lib.sh; . /lab/lab/fc13_lib.sh; . /lab/lab/fc14_lib.sh; . /lab/lab/fc15_lib.sh; . /lab/lab/fc16_lib.sh; . /lab/lab/fc17_lib.sh
T=$1; TD=$T; [ "$T" = P ] && TD=K   # take P films into out/fc17/K: out/fc17/P holds the start files
O=$X/$TD; mkdir -p $O; L=$O/take.log; : > $L
case $T in R|T) SRC=$X/P/peg-moved.FCStd;; F) SRC=$X/T/end.FCStd;; P|Y) SRC=$X/F/end.FCStd;; *) echo "R|T|F|P|Y"; exit 2;; esac
[ -f "$SRC" ] || { echo "no $SRC"; exit 2; }
F=cup
W14=/tmp/fc17-ui.json
fx_start $O
mkdir -p /tmp/fc17; cp "$SRC" /tmp/fc17/$F.FCStd   # the take works on a copy in /tmp: never on a start file

prepdoc() {
  FQ "prep('$F')" >> $L 2>&1
  Q "import FreeCAD, FreeCADGui
g = FreeCADGui.getDocument('$F'); g.activeView().setAnimationEnabled(False)
g.getObject('Body').ShapeAppearance = [FreeCAD.Material(DiffuseColor=(0.93, 0.55, 0.20))]
print(1)" >> $L 2>&1
}
if [ "$T" != P ]; then
  open_doc /tmp/fc17/$F.FCStd >> $L 2>&1; prepdoc
  report_hide; sl_nap 2; xdotool mousemove 1500 1500; rv_clear
fi
echo "notices at open: $(FQ "notices()")" >> $L

mstate() {     # the Body as FreeCAD holds it now (not filmed): mirrors, states, volume, y extent, peg runs along x
  Q "import FreeCAD, json
d = FreeCAD.getDocument('$F'); b = d.getObject('Body'); s = b.Shape; bb = s.BoundBox; P = d.getObject('Params')
w = float(P.get('wall')); ins = lambda x, y, z: s.isInside(FreeCAD.Vector(x, y, z), 1e-6, True)
def runs(y, z):
    r = []; a = None
    for i in range(-900, 901):
        x = i * 0.05; t = ins(x, y, z)
        if t and a is None: a = x
        if not t and a is not None: r.append([round(a, 2), round(x - 0.05, 2)]); a = None
    return r
ms = [[o.Name, o.Label, o.MirrorPlane[0].Name if o.MirrorPlane and o.MirrorPlane[0] else None,
       list(o.MirrorPlane[1]) if o.MirrorPlane else None, [x.Name for x in o.Originals], list(o.State)]
      for o in b.Group if o.TypeId == 'PartDesign::Mirrored']
st = {o.Name: [list(o.State), o.getStatusString()] for o in b.Group if o.TypeId.startswith('PartDesign::') and list(o.State) != ['Up-to-date']}
print(json.dumps({'peg_x': float(P.get('peg_x')), 'peg_size': float(P.get('peg_size')), 'wall': w, 'tip': b.Tip.Name,
  'mirrors': ms, 'state': st, 'volume': round(s.Volume, 3), 'solids': len(s.Solids),
  'y': [round(bb.YMin, 3), round(bb.YMax, 3), round(bb.YLength, 3)], 'behind_back': round(bb.YMax - (20 + w), 3),
  'front_x': runs(-28, 40), 'back_x': runs(28, 40), 'hole_open': not ins(0, 20 + w / 2, 30)}))"
}
orbit() {      # orbit SECONDS DEG: the camera turns round the world Z axis, smoothly
  Q "import FreeCAD, FreeCADGui, time
from PySide import QtWidgets
v = FreeCADGui.getDocument('$F').activeView(); n = int($1 * 30); st = $2 / float(n)
for i in range(n):
    v.setCameraOrientation(FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), st).multiply(v.getCameraOrientation()))
    QtWidgets.QApplication.processEvents(); time.sleep(1 / 30.0)
print(1)" >> $L 2>&1
}
zoomto() {     # zoomto SECONDS VIEW CX CY CZ HEIGHT: the camera glides to a standard view of (CX,CY,CZ), HEIGHT mm high
  Q "import FreeCAD, FreeCADGui, time
from PySide import QtWidgets
from pivy import coin
v = FreeCADGui.getDocument('$F').activeView(); v.setAnimationEnabled(False); cam = v.getCameraNode()
p0 = FreeCAD.Vector(*cam.position.getValue().getValue()); h0 = cam.height.getValue()
r0 = cam.orientation.getValue()
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
front() { zoomto 3 Front 0 -28 32 ${2:-80}; sl_nap 2; shot $O/front-$1.png; echo "front $1: $(mstate)" >> $L; }
rear() { zoomto 3 Rear 0 28 32 ${2:-80}; sl_nap 2; shot $O/rear-$1.png; echo "rear $1: $(mstate)" >> $L; }
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
  echo "$3 $2: $(mstate)" >> $L
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
panel_log() { echo "panel $1: $(FQ "task_texts()" | cut -c1-1500)" >> $L; }
plane_to() {   # plane_to FROM TO: the Mirror panel's Plane list, FROM -> TO, by clicks (rows from the UI watcher)
  local c p; c=$(FQ "combo_pos('$1')"); [ "$c" != none ] || bail "no Plane list showing $1"
  uiwatch 15; at "$c" "Plane list"; sl_nap 2.5
  echo "Plane list rows: $(ui dump | grep -o '"popup": \[.*\]' | cut -c1-600)" >> $L
  shot $O/planelist-$2.png
  p=$(ui popup "$2"); case "$p" in ""|none) xdotool key Escape; bail "Plane $2 not in the list";; esac
  sl_glide ${p% *} ${p#* } 15; sl_nap 0.8; sl_click ${p% *} ${p#* } "Plane: $2"; sl_nap 3
  echo "after plane $2 (preview): $(mstate)" >> $L
}
mir_ok() { panel_log "before OK"; shot $O/panel-$1.png; at "$(taskpos any OK)" "OK"; sl_nap 4
  echo "after OK: $(mstate)" >> $L; echo "notices: $(FQ "notices()")" >> $L; echo "tree: $(treestate $F 2>/dev/null | cut -c1-600)" >> $L; }
meas() {       # meas NAME VIEW1 X Y Z LABEL1 VIEW2 X Y Z LABEL2 HEIGHT: Measure, a click in VIEW1, Ctrl + a click in VIEW2
  local n=$1 p; clr
  zoomto 3 $2 $3 $4 $5 ${12}
  btn Std_Measure "Measure"; sl_nap 2
  p=$(vp $3 $4 $5); sl_glide ${p% *} ${p#* } 25; sl_nap 0.8; sl_click ${p% *} ${p#* } "$n: $6"; sl_nap 1.5
  echo "$n first: $(selnames)" >> $L
  [ "$7" = "$2" ] || zoomto 3 $7 $8 $9 ${10} ${12}
  p=$(vp $8 $9 ${10}); sl_glide ${p% *} ${p#* } 25; sl_nap 0.8
  xdotool keydown ctrl; sl_click ${p% *} ${p#* } "$n: Ctrl + ${11}"; xdotool keyup ctrl
  sl_nap 3.5
  echo "$n measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*\|"QLabel", "[^"]*"' | tr '\n' ' ')" >> $L
  echo "$n selection: $(selnames)" >> $L
  shot $O/measure-$n.png; sl_nap 3
  at "$(taskpos any Close)" "Measure: Close"; sl_nap 1.5
  clr
}

if [ "$T" != P ]; then xdotool mousemove 1500 1500; row_open $F Pad001 > /dev/null 2>&1; xdotool mousemove 1500 1500; sleep 1; fi
echo "start: $(mstate)" >> $L
sl_record "$O"; sl_mark "recording started: FreeCAD 1.1.4, cup.FCStd ($T)"
sl_nap 3
case $T in
R)
  orbit 6 60
  dblrow Params "double-click: open Params"; sl_nap 1.5
  for r in 3 7; do c=$(B cell $r 1); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Params row $((r + 1))"; sl_nap 2.5; done
  shot $O/params.png
  t=$(B tab "$F"); at "$t" "tab: back to the 3D view"; sl_nap 1.5
  wb_pd
  isofit; front peg 90; sl_nap 2
  p=$(vp 15 -35 40); sl_glide ${p% *} ${p#* } 25; sl_nap 0.8; sl_click ${p% *} ${p#* } "Q5: click the peg's front face in the 3D view"; sl_nap 2.5
  echo "Q5 3D click selection: $(selnames)" >> $L; shot $O/q5-click.png; sl_nap 1.5
  clr; isofit; orbit 4 40
  ;;
T)
  isofit; sl_nap 1
  p=$(ROW $F Pad001); at "$p" "tree: Pad001 (the peg)"; sl_nap 1.5
  echo "selection: $(selnames)" >> $L
  m=$(menubar_pos "Part Design"); echo "menubar Part Design $m" >> $L; [ "$m" != none ] || bail "no Part Design menu"
  uiwatch 20; at "$m" "menu: Part Design"; sl_nap 1.8
  echo "Part Design menu: $(ui dump | cut -c1-1500)" >> $L
  s=$(ui menu "Transformation Features"); [ "$s" != none ] || { xdotool key Escape; bail "no Transformation Features"; }
  sl_glide $(( ${s% *} - 80 )) ${s#* } 10; sl_glide ${s% *} ${s#* } 15; sl_nap 1.8
  echo "Transformation menu: $(ui dump | cut -c1-1500)" >> $L
  shot $O/menu-transformation.png
  s=$(ui menu "Mirror"); [ "$s" != none ] || { xdotool key Escape; xdotool key Escape; bail "no Mirror item"; }
  sl_glide $(( ${s% *} - 60 )) ${s#* } 10; sl_glide ${s% *} ${s#* } 15; sl_nap 0.8; sl_click ${s% *} ${s#* } "menu: Mirror"; sl_nap 4
  panel_log open; shot $O/panel-open.png
  echo "Q3 panel open (preview): $(mstate)" >> $L
  isofit; sl_nap 4; shot $O/preview-default.png
  plane_to "Vertical sketch axis" "Base XZ-plane"
  isofit; sl_nap 3; shot $O/preview-xz.png
  mir_ok xz
  isofit; sl_nap 1; orbit 5 180; sl_nap 2; shot $O/back-orbit.png
  rear trap 90; sl_nap 2
  meas behind13 Rear 15 35 40 "the copy's end face (the back peg)" Rear -15 22 40 "the cup's back face" 60
  meas depth70 Front 15 -35 40 "the front peg's end face" Rear 15 35 40 "the back peg's end face" 90
  isofit
  ;;
F)
  isofit; sl_nap 1
  uiwatch 20; p=$(ROW $F Mirrored); sl_glide ${p% *} ${p#* } 20; sl_nap 0.5; sl_click ${p% *} ${p#* } "tree: Mirrored"; sl_nap 0.8
  sl_mark "right-click: Mirrored"; xdotool click 3; sl_nap 2
  echo "Q8 context menu: $(ui dump | cut -c1-1500)" >> $L
  shot $O/context-menu.png
  m=$(ui menu "Edit"); echo "edit item at $m" >> $L
  if [ "$m" != none ]; then sl_glide ${m% *} ${m#* } 25; sl_nap 0.8; sl_click ${m% *} ${m#* } "menu: Edit"; sl_nap 4
  else xdotool key Escape; sl_nap 1; dblrow Mirrored "double-click: Mirrored"; fi
  panel_log open; shot $O/panel-edit.png
  plane_to "Base XZ-plane" "Base YZ-plane"
  isofit; sl_nap 3; shot $O/preview-yz.png
  mir_ok yz
  front fixed 90; sl_nap 2
  meas gap20 Front 10 -35 40 "the right peg's inner edge" Front -10 -35 40 "the left peg's inner edge" 40
  meas depth57 Front 15 -35 40 "the peg's end face" Rear 15 22 40 "the cup's back face" 90
  rear fixed 90; sl_nap 2
  isofit
  ;;
P)
  sl_nap 1
  open_doc /tmp/fc17/$F.FCStd >> $L 2>&1; sl_mark "file reopened: F's saved end file (Mirrored across Base YZ)"; prepdoc; report_hide; sl_nap 3
  echo "notices at reopen: $(FQ "notices()")" >> $L
  echo "reopened: $(mstate)" >> $L
  isofit
  params_set 7 20 peg_x; wb_pd; front x20; rear x20; isofit
  params_set 4 12 peg_size; wb_pd; front s12; rear s12; isofit
  params_set 3 3 wall; wb_pd; front w3; rear w3; isofit
  ;;
Y)
  isofit; orbit 24 120
  ;;
esac
sl_nap 2; sl_stop
lab_save $F $O/end.FCStd >> $L 2>&1
echo "TAKE $T DONE" >> $L
fc_quit; sl_display_stop
check17 $O/end.FCStd $O/check.json >> $L
