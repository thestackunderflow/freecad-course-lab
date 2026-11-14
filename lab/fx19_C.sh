#!/bin/bash
# fx19 take C (LAB-fx19 3.C): how the gap happens. New document, Part Design, Body, sketch on XZ; Polyline the hook's
# eight corners by clicks (lesson 2's rough corners), the last click 2 mm above the first point: Esc; zoom on the
# corner (C/apart.png). Then that sketch hidden (Space), a second sketch on XZ, the same corners with the last click ON
# the first point: the hover still (Q5 cue), the constraint list before/after the closing click (Q5). Then Q4:
# hook-touch.FCStd opened, Pad 20 (C/touch.png).
#   FCC_PREFIX=fx19 FCC_DOCKER_ARGS="--network none -e ZOOM_BTN=4" tools/run.sh lab/fx19_C.sh
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh
O=$X/C; mkdir -p $O; L=$O/take.log; : > $L
fx_start $O
Q "import FreeCADGui
FreeCADGui.activateWorkbench('PartWorkbench')
print(1)" >> $L 2>&1
sleep 2
ZB=${ZOOM_BTN:-4}
K=17.86
SPU() { SP Unnamed "$@"; }
CONS() { Q "import FreeCAD
s = FreeCAD.getDocument('Unnamed').getObject('$1')
print('$2', len(s.Constraints), [(c.Type, c.First, c.FirstPos, c.Second, c.SecondPos) for c in s.Constraints if c.Type == 'Coincident'])" >> $L 2>&1; }
outline() {   # outline LAST_DY_MM LABEL: Polyline, origin, 7 rough corners, last click at origin + LAST_DY_MM up
  read -r OX OY < <(SPU "$1" -1 origin); echo "origin $OX $OY ($1)" >> $L
  sl_glide 316 228 20; sl_mark "hover: Polyline"; sl_nap 1.2
  sl_click 316 228 "Polyline"; sl_nap 1
  SL_HOLD=0.9 sl_click "$OX" "$OY" "polyline: origin"
  local n=0 p x y
  for p in "28 0 right" "28 12 up" "22 12 left" "22 6 down" "6 6 left" "6 55 up" "0 55 left"; do
    set -- $p; n=$((n + 1))
    x=$(awk -v o="$OX" -v a="$1" -v k=$K 'BEGIN{printf "%d", o + a * k}')
    y=$(awk -v o="$OY" -v a="$2" -v k=$K 'BEGIN{printf "%d", o - a * k}')
    sl_glide "$x" "$y" 30; sl_nap 0.5
    SL_HOLD=0.9 sl_click "$x" "$y" "polyline: corner $n ($3)"
  done
}
new_sketch() {
  sl_glide 570 158 20; sl_mark "hover: New Sketch"; sl_nap 1.2
  sl_click 570 158 "New Sketch"; sl_nap 2
  sl_click 2340 774 "attachment: XZ-plane"; sl_nap 1.5
  sl_click 2430 616 "attachment: OK"; sl_nap 3
  sl_drag 1500 900 1350 1470 "pan: middle drag" 2; sl_nap 1.2
}
report_hide
xdotool mousemove 1500 700
sl_record "$O"; sl_mark "recording started: FreeCAD, start page, Part workbench"
sl_nap 3
sl_click 45 36 "File menu"; sl_click 143 76 "File: New Document"; sl_nap 1.5
sl_click 700 88 "workbench list"; sl_nap 1.2
sl_glide 630 338 20; sl_nap 0.6; sl_click 630 338 "workbench: Part Design"; sl_nap 2
sl_glide 510 158 20; sl_nap 0.8; sl_click 510 158 "New Body"; sl_nap 1.5
new_sketch
# --- C1: the last click 2 mm above the first point
outline Sketch "C1"
read -r OX OY < <(SPU Sketch -1 origin)
LX=$OX; LY=$(awk -v o="$OY" -v k=$K 'BEGIN{printf "%d", o - 2 * k}')
sl_glide "$LX" "$LY" 30; sl_nap 0.8
SL_HOLD=0.9 sl_click "$LX" "$LY" "polyline: last click 2 mm above the first point"
sl_nap 1
sl_key Escape "Esc: polyline ended"; sl_nap 2
CONS Sketch "C1 after Esc"
Q "import FreeCADGui; print('in edit', FreeCADGui.ActiveDocument.getInEdit())" >> $L 2>&1
SL_SHOT_WAKE=0 sl_shot $O/c1-outline.png
sl_glide "$OX" "$OY" 20; sl_mark "zoom in on the corner"
for i in $(seq 1 9); do xdotool click $ZB; sleep 0.35; done
read -r AX AY < <(SPU Sketch 7 end); read -r BX BY < <(SPU Sketch 0 start)
echo "C1 zoomed: last end $AX $AY, first start $BX $BY" >> $L
sl_nap 4
SL_SHOT_WAKE=0 sl_shot $O/apart.png
Q "import FreeCAD
s = FreeCAD.getDocument('Unnamed').getObject('Sketch')
g = s.Geometry
print('C1 geometry', len(g), 'last end', g[-1].EndPoint, 'first start', g[0].StartPoint, 'wires', [w.isClosed() for w in s.Shape.Wires])" >> $L 2>&1
read -r ZX ZY < <(B text Close); echo "sketch Close $ZX $ZY" >> $L
clk "$ZX $ZY" "sketch: Close"; sl_nap 2.5
# --- C2: the first sketch hidden (Space), a second sketch, the last click ON the first point
read -r RX RY < <(ROW Unnamed Sketch); echo "Sketch row $RX $RY" >> $L
clk "$RX $RY" "tree: Sketch"; sl_nap 0.8
sl_glide 1500 900 20; sl_key space "Space: Sketch hidden"; sl_nap 1.5
new_sketch
outline Sketch001 "C2"
read -r OX OY < <(SPU Sketch001 -1 origin)
sl_glide "$OX" "$OY" 30; sl_mark "hover: the first point (highlight cue?)"; sl_nap 2
SL_SHOT_WAKE=0 sl_shot $O/close-hover.png
CONS Sketch001 "C2 before the closing click"
SL_HOLD=1.2 sl_click "$OX" "$OY" "polyline: close on the first point"; sl_nap 1.5
CONS Sketch001 "C2 after the closing click"
sl_key Escape "Esc: tool off"; sl_nap 2
SL_SHOT_WAKE=0 sl_shot $O/closed.png
Q "import FreeCAD
s = FreeCAD.getDocument('Unnamed').getObject('Sketch001')
print('C2 geometry', len(s.Geometry), 'wires', [w.isClosed() for w in s.Shape.Wires], 'in edit', __import__('FreeCADGui').ActiveDocument.getInEdit())" >> $L 2>&1
read -r ZX ZY < <(B text Close); echo "sketch Close $ZX $ZY" >> $L
[ -n "$ZX" ] && [ "$ZX" != none ] && clk "$ZX $ZY" "sketch: Close"; sl_nap 2.5
sl_mark "recording paused: hook-touch opened (not filmed)"
# --- Q4: touching ends, no Coincident
cp $X/P/hook-touch.FCStd /tmp/hook-touch.FCStd
open_doc /tmp/hook-touch.FCStd >> $L 2>&1; sleep 2

read -r TX TY < <(row_open hook_touch Sketch); echo "touch Sketch row $TX $TY" >> $L
BASE=$(nwin)
sl_mark "hook-touch open"; sl_nap 3
clk "$TX $TY" "tree: Sketch (hook-touch)"; sl_nap 1
sl_glide 50 228 20; sl_nap 0.8; sl_click 50 228 "Pad"; sl_nap 2.5
sl_type "20" "Pad: typed 20" 250; sl_nap 2
clk "$TASK_OK" "Pad: OK"; sl_nap 3
echo "windows after OK $(nwin) (baseline $BASE)" >> $L
SL_SHOT_WAKE=0 sl_shot $O/touch.png
sl_nap 2
close_box_if_any "$BASE" "box after the touch Pad: Return" >> $L
sl_glide 1500 900 20; sl_key 0 "key 0: isometric"; sl_nap 3
sl_mark "recording stopped"; sl_stop
Q "import FreeCAD
d = FreeCAD.getDocument('hook_touch'); p = d.getObject('Pad')
print('READ touch pad', p.isValid(), p.getStatusString(), p.Shape.Volume if not p.Shape.isNull() else None)" >> $L 2>&1
fc_quit; sl_display_stop
echo "C done"
