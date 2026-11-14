#!/bin/bash
# fx19 take E (LAB-fx19 3.E, your turn, by hand): New document, Part Design, New Body, sketch on XY; Rectangle (G, R);
# sizes 30 and 20 (D); the top-left corner's Coincident deleted (the corner clicked, Delete) and that end dragged
# about 1 mm apart; Close; Validate Sketch, Highlight (the two marks); into the sketch, the two ends joined (C); Close;
# Pad 10; View, Panels, Python console; the volume line (expected 6000.0).
#   FCC_PREFIX=fx19 FCC_DOCKER_ARGS="--network none -e ZOOM_BTN=4" tools/run.sh lab/fx19_E.sh
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh
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
sl_drag 1500 900 1350 1470 "pan: middle drag" 2; sl_nap 1.2
read -r OX OY < <(SP Unnamed Sketch -1 origin); echo "origin $OX $OY" >> $L
xdotool mousemove 1400 1100; sl_nap 0.4
sl_key g "key G"; sl_key r "key R: Rectangle"; sl_nap 1
x2=$(awk -v o="$OX" -v k=$K 'BEGIN{printf "%d", o + 32 * k}'); y2=$(awk -v o="$OY" -v k=$K 'BEGIN{printf "%d", o - 22 * k}')
sl_glide "$OX" "$OY" 25; sl_nap 0.5; SL_HOLD=0.9 sl_click "$OX" "$OY" "rectangle: first corner on the origin"
sl_glide "$x2" "$y2" 30; sl_nap 0.5; SL_HOLD=0.9 sl_click "$x2" "$y2" "rectangle: opposite corner"
sl_nap 1; sl_key Escape "Esc: tool off"; sl_nap 1.5
read -r GB GR GT GL < <(IDX); echo "bottom $GB right $GR top $GT left $GL" >> $L
CON "after rectangle"
xdotool mousemove 1400 1200; sl_nap 0.4
sl_key d "key D: Dimension"; sl_nap 1
dim() {   # dim GEO DX DY VALUE LABEL
  local x y px py
  read -r x y < <(SPU "$1" mid); sl_glide "$x" "$y" 25; sl_nap 0.4; sl_click "$x" "$y" "dimension $5: pick"
  read -r px py < <(SPU "$1" mid "$2" "$3"); sl_glide "$px" "$py" 20; sl_nap 0.3; sl_click "$px" "$py" "dimension $5: place"
  sl_nap 1.2; sl_type "$4" "dimension $5: typed $4" 220; sl_key Return "dimension $5: Enter"; sl_nap 2.2
}
dim "$GB" 0 80 30 "bottom 30"
dim "$GR" -90 0 20 "right 20"
xdotool key Escape; sl_mark "Esc: Dimension off"; sl_nap 1.5
CON "after sizes"
# the top-left corner: its Coincident deleted, the end dragged about 1 mm (stop if the sketch is not in edit or not 30 x 20)
Q "import FreeCAD, FreeCADGui
s = FreeCAD.getDocument('Unnamed').getObject('Sketch')
print('GUARD', FreeCADGui.ActiveDocument.getInEdit() is not None and len([c for c in s.Constraints if c.Type.startswith('Distance')]) == 2)" > /tmp/guard.txt 2>&1; cat /tmp/guard.txt >> $L
grep -q "GUARD True" /tmp/guard.txt || { sl_mark "STOP: not in the sketch or sizes missing"; sl_stop; echo "E stopped by guard"; fc_quit; sl_display_stop; exit 1; }
read -r CX CY < <(SPU "$GL" start); read -r C2X C2Y < <(SPU "$GT" end); echo "top-left: left start $CX $CY, top end $C2X $C2Y" >> $L
sl_glide "$CX" "$CY" 25; sl_nap 0.6; sl_click "$CX" "$CY" "corner: top-left clicked"; sl_nap 1
sl_key Delete "Delete: the corner's rules"; sl_nap 1.5
CON "after Delete"
xdotool mousemove $((CX + 60)) $((CY + 60)); sl_nap 0.5; sl_glide "$CX" "$CY" 15; sl_nap 0.8   # moved away and back: preselection
sl_mark "drag the end: down"; xdotool mousedown 1; sleep 0.2
for i in $(seq 1 18); do xdotool mousemove $((CX - i)) $((CY - i)); sleep 0.05; done
xdotool mouseup 1; sl_mark "drag the end: released (about 1 mm)"; sl_nap 1.5
CON "after drag"
Q "import FreeCAD
s = FreeCAD.getDocument('Unnamed').getObject('Sketch'); g = s.Geometry
print('ends', g[$GL].StartPoint, g[$GT].EndPoint, 'gap', (g[$GL].StartPoint - g[$GT].EndPoint).Length)" >> $L 2>&1
SL_SHOT_WAKE=0 sl_shot $O/apart.png
read -r ZX ZY < <(B text Close); clk "$ZX $ZY" "sketch: Close"; sl_nap 2.5
read -r SKX SKY < <(row_open Unnamed Sketch); echo "Sketch row $SKX $SKY" >> $L
clk "$SKX $SKY" "tree: Sketch"; sl_nap 1
clk "$SKETCH_MENU" "Sketch menu"; sl_nap 1.2
sl_glide 595 249 15; sl_nap 0.6; sl_click 595 249 "Validate Sketch"; sl_nap 3
clk "$HIGHLIGHT_BTN" "Highlight Troublesome Vertices"; sl_nap 4
SL_SHOT_WAKE=0 sl_shot $O/validate.png
clk "$VALID_CLOSE" "validation: Close"; sl_nap 2
sl_glide "$SKX" "$SKY" 20; sl_nap 0.4
xdotool click --repeat 2 --delay 120 1; sl_mark "tree: double-click Sketch"; sl_nap 3.5
read -r AX AY < <(SPU "$GL" start); read -r BX BY < <(SPU "$GT" end)
sl_glide "$BX" "$BY" 20; sl_mark "zoom in on the corner"
for i in $(seq 1 9); do xdotool click $ZB; sleep 0.35; done
read -r AX AY < <(SPU "$GL" start); read -r BX BY < <(SPU "$GT" end); echo "zoomed: $AX $AY / $BX $BY" >> $L
sl_nap 1.5
clk "$AX $AY" "pick: one end"; sl_nap 1
clk "$BX $BY" "pick: the other end"; sl_nap 1
xdotool mousemove $((BX + 150)) $((BY + 150)); sl_nap 0.4
sl_key c "key C: coincident"; sl_nap 3
CON "after join"
SL_SHOT_WAKE=0 sl_shot $O/joined.png
sl_glide 1500 900 20; sl_key Escape "Esc: selection cleared"; sl_nap 1
read -r ZX ZY < <(B text Close); clk "$ZX $ZY" "sketch: Close"; sl_nap 2.5
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
echo "E done"
