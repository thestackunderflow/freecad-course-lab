#!/bin/bash
# fx20 take E (LAB-fx20 3.E, your turn, by hand; recipe from fx19_E.sh): New document, Part Design, New Body, sketch
# on XY; Rectangle (G, R) from the origin; sizes 40 and 20 (D); DoF read; the top side sized 41 (the refusal popup);
# again with Reference ticked (reads "(40 mm)"); Close; Pad 10; View, Panels, Python console; volume (expected 8000.0).
#   FCC_PREFIX=fx20 FCC_DOCKER_ARGS="--network none -e ZOOM_BTN=4" tools/run.sh lab/fx19_E.sh
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh
O=$X/E; mkdir -p $O; L=$O/take.log; : > $L
fx_start $O
Q "import FreeCADGui
FreeCADGui.activateWorkbench('PartWorkbench')
print(1)" >> $L 2>&1
sleep 2
ZB=${ZOOM_BTN:-4}; K=17.86
SPU() { SP Unnamed Sketch "$@"; }
IDX() { Q "import FreeCAD
s = FreeCAD.getDocument('Unnamed').getObject('Sketch')
g = [(i, x) for i, x in enumerate(s.Geometry)]
def side(pred): return [i for i, x in g if pred(x.StartPoint, x.EndPoint)][0]
b = side(lambda a, e: abs(a.y - e.y) < 1e-6 and min(a.y, e.y) < 1e-6)
t = side(lambda a, e: abs(a.y - e.y) < 1e-6 and min(a.y, e.y) > 1e-6)
r = side(lambda a, e: abs(a.x - e.x) < 1e-6 and min(a.x, e.x) > 1e-6)
l = side(lambda a, e: abs(a.x - e.x) < 1e-6 and min(a.x, e.x) < 1e-6)
print(b, r, t, l)"; }
CON() { Q "import FreeCAD
s = FreeCAD.getDocument('Unnamed').getObject('Sketch')
print('$1', len(s.Constraints), [(c.Type, c.First, c.FirstPos, c.Second, c.SecondPos, round(c.Value, 3)) for c in s.Constraints], 'DoF', s.solve(), s.DoF)" >> $L 2>&1; }
report_hide
xdotool mousemove 1500 700
sl_record "$O"; sl_mark "recording started: FreeCAD, start page, Part workbench"
sl_nap 3
sl_click 45 36 "File menu"; sl_click 143 76 "File: New Document"; sl_nap 1.5
sl_click 700 88 "workbench list"; sl_nap 1.2
sl_glide 630 338 20; sl_nap 0.6; sl_click 630 338 "workbench: Part Design"; sl_nap 2
sl_glide 510 158 20; sl_nap 0.8; sl_click 510 158 "New Body"; sl_nap 1.5
sl_glide 570 158 20; sl_nap 0.8; sl_click 570 158 "New Sketch"; sl_nap 2
sl_glide 2340 750 20; sl_nap 0.8; sl_click 2340 750 "attachment: XY-plane"; sl_nap 1.5
sl_click 2430 616 "attachment: OK"; sl_nap 3
sl_drag 1500 900 1100 1470 "pan: middle drag" 2; sl_nap 1.2
read -r OX OY < <(SP Unnamed Sketch -1 origin); echo "origin $OX $OY" >> $L
xdotool mousemove 1400 1100; sl_nap 0.4
sl_key g "key G"; sl_key r "key R: Rectangle"; sl_nap 1
x2=$(awk -v o="$OX" -v k=$K 'BEGIN{printf "%d", o + 42 * k}'); y2=$(awk -v o="$OY" -v k=$K 'BEGIN{printf "%d", o - 22 * k}')
sl_glide "$OX" "$OY" 25; sl_nap 0.5; SL_HOLD=0.9 sl_click "$OX" "$OY" "rectangle: first corner on the origin"
sl_glide "$x2" "$y2" 30; sl_nap 0.5; SL_HOLD=0.9 sl_click "$x2" "$y2" "rectangle: opposite corner"
sl_nap 1; sl_key Escape "Esc: tool off"; sl_nap 1.5
read -r GB GR GT GL < <(IDX); echo "bottom $GB right $GR top $GT left $GL" >> $L
CON "after rectangle"
xdotool mousemove 1400 1200; sl_nap 0.4
sl_key d "key D: Dimension"; sl_nap 1
dim() {   # dim GEO DX DY VALUE LABEL [ref]: VALUE typed, or (ref) the Reference box ticked and nothing typed
  local x y px py
  read -r x y < <(SPU "$1" mid); sl_glide "$x" "$y" 25; sl_nap 0.4; sl_click "$x" "$y" "dimension $5: pick"
  read -r px py < <(SPU "$1" mid "$2" "$3"); sl_glide "$px" "$py" 20; sl_nap 0.3; sl_click "$px" "$py" "dimension $5: place"
  sl_nap 1.2
  if [ "${6:-}" = ref ]; then clk "$((px + 36)) $((py + 150))" "dimension $5: tick Reference"; sl_nap 1.2
  else sl_type "$4" "dimension $5: typed $4" 220; fi
  sl_key Return "dimension $5: Enter"; sl_nap 2.2
}
dim "$GB" 0 80 40 "bottom 40"
dim "$GR" -90 0 20 "right 20"
CON "after sizes"
dim "$GT" 0 -80 41 "top 41"
sl_mark "popup: the refusal"; sl_nap 5
SL_SHOT_WAKE=0 sl_shot $O/refusal.png
CON "after 41"
dim "$GT" 0 -80 "" "top, Reference" ref
sl_nap 2
SL_SHOT_WAKE=0 sl_shot $O/ref.png
CON "after Reference"
xdotool key Escape; sl_mark "Esc: Dimension off"; sl_nap 1.5
read -r ZX ZY < <(B text Close); clk "$ZX $ZY" "sketch: Close"; sl_nap 2.5
read -r SKX SKY < <(row_open Unnamed Sketch); echo "Sketch row $SKX $SKY" >> $L
clk "$SKX $SKY" "tree: Sketch"; sl_nap 1
sl_glide 50 228 20; sl_nap 0.8; sl_click 50 228 "Pad"; sl_nap 2.5
sl_type "10" "Pad: typed 10" 250; sl_nap 2
clk "$TASK_OK" "Pad: OK"; sl_nap 2
sl_glide 1500 900 20; sl_key 0 "key 0: isometric"; sl_nap 3
read -r PX PY < <(ROW Unnamed Pad); echo "Pad row $PX $PY" >> $L
clk "$PX $PY" "tree: Pad"; sl_nap 1.2
console_line $O "Gui.Selection.getSelection()[0].Shape.Volume"
SL_SHOT_WAKE=0 sl_shot $O/volume.png
sl_mark "recording stopped"; sl_stop
Q "import FreeCAD
d = FreeCAD.getDocument('Unnamed'); p = d.getObject('Pad')
print('READ pad', p.isValid() if p else None, p.Shape.Volume if p and not p.Shape.isNull() else None)" >> $L 2>&1
fc_quit; sl_display_stop
echo "E done (fx20)"
