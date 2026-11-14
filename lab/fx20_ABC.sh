#!/bin/bash
# fx20 takes A, B, C (LAB-fx20 3.A-C). One container, three recordings. Places on the sketch come from a pre-pass
# (not filmed: into the sketch, the sketch-to-screen map read, out again) so no lab query writes into the Report view
# during A. Labels as found in G0 (DEVIATIONS 3).
#   FCC_PREFIX=fx20 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fx20_ABC.sh
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh
mkdir -p $X/A $X/B $X/C; L=$X/A/take.log; : > $L
fx_start $X/A
mkdir -p /tmp/fx20; cp $X/P/hook.FCStd /tmp/fx20/hook.FCStd
open_doc /tmp/fx20/hook.FCStd >> $L 2>&1; sleep 2
read -r SKX SKY < <(row_open hook Sketch); echo "Sketch row $SKX $SKY" >> $L
NOTE=$(Q "import FreeCADGui
from PySide import QtWidgets
w = FreeCADGui.getMainWindow().statusBar().findChild(QtWidgets.QPushButton, 'notificationArea')
k = w.devicePixelRatioF(); g = w.mapToGlobal(w.rect().center()); print('%d %d' % (g.x() * k, g.y() * k))")
echo "notification button $NOTE" >> $L
# ---- pre-pass (not filmed): the map, the bottom size's label
xdotool mousemove "$SKX" "$SKY"; sleep 0.5; xdotool click --repeat 2 --delay 120 1; sleep 4
read -r OX OY < <(SP hook Sketch -1 origin); read -r EX EY < <(SP hook Sketch 0 end)
K=$(awk "BEGIN{print ($EX-$OX)/25}")
LD=$(Q "import FreeCAD; c = FreeCAD.getDocument('hook').getObject('Sketch').Constraints[17]; print(c.Type, c.Value, c.LabelDistance, c.LabelPosition)")
echo "map origin $OX $OY, bottom end $EX $EY, k $K px/mm; bottom size: $LD" >> $L
LDV=$(echo "$LD" | awk '{print ($3 < 0 ? -$3 : $3)}')
M() { awk "BEGIN{printf \"%d %d\", $OX + $K * ($1), $OY - $K * ($2)}"; }
read -r ZX ZY < <(B text Close); echo "sketch Close $ZX $ZY" >> $L
xdotool mousemove "$ZX" "$ZY"; sleep 0.4; xdotool click 1; sleep 3
BASE=$(nwin); echo "windows $BASE" >> $L
rv_clear; xdotool mousemove 1500 700
SL_SHOT_WAKE=0 sl_shot $X/A/before.png

dim_arm() {  # dim_arm ARMLEN TAG: key D, the arm top's middle, placed 110 px above
  read -r AX AY < <(M "$(awk "BEGIN{print 5 + $1 / 2}")" 5)
  sl_glide 1500 700 15; sl_key d "key D: Dimension"; sl_nap 1.2
  clk "$AX $AY" "$2: pick the arm's top"; sl_nap 1
  sl_glide "$AX" $((AY - 110)) 15; sl_nap 0.8; sl_click "$AX" $((AY - 110)) "$2: place the size"; sl_nap 2.5
  PLX=$AX; PLY=$((AY - 110))
}
bottom_edit() {  # bottom_edit BOTTOM VALUE TAG: double-click the bottom size's label, type, Return
  read -r BX BY < <(M "$(awk "BEGIN{print $1 / 2}")" "-$LDV")
  sl_glide "$BX" "$BY" 20; sl_nap 0.8
  xdotool click --repeat 2 --delay 120 1; sl_mark "$3: double-click the bottom size ($1)"; sl_nap 2.5
  sl_type "$2" "$3: typed $2" 250; sl_nap 1.5
  sl_key Return "$3: Return (OK)"; sl_nap 3
}

# ================= take A: the refusal
O=$X/A
sl_record "$O"; sl_mark "recording started: FreeCAD, hook open, Part Design, front view"
sl_nap 3
sl_glide "$SKX" "$SKY" 20; sl_nap 0.4
xdotool click --repeat 2 --delay 120 1; sl_mark "tree: double-click Sketch"; sl_nap 4
sl_mark "hold: Fully constrained"; sl_nap 4
read -r CX CY < <(M 20 5)
sl_glide "$CX" "$CY" 20; sl_nap 0.8; xdotool mousedown 1; sl_mark "drag the arm's corner"
sl_glide $((CX + 90)) $((CY - 70)) 30; sl_nap 0.5; xdotool mouseup 1; sl_mark "released: nothing moved"; sl_nap 2.5
dim_arm 15 A
sl_type "17" "A: typed 17" 250; sl_nap 1.5
sl_key Return "A: Return (OK)"; sl_mark "popup: Negative datum values ..."; sl_nap 5
SL_SHOT_WAKE=0 sl_shot $O/popup.png
clk "$NOTE" "notification list: open"; sl_nap 8
SL_SHOT_WAKE=0 sl_shot $O/refusal.png
clk "$NOTE" "notification list: close"; sl_nap 1.5
sl_glide 1500 700 15; sl_key Escape "Esc: Dimension tool off"; sl_nap 4
SL_SHOT_WAKE=0 sl_shot $O/unchanged.png
sl_mark "recording stopped"; sl_stop
{ echo "A after:"; sk_state hook; solver_text; } >> $L 2>&1

# ================= take B: the fix
O=$X/B; L=$X/B/take.log; : > $L
rv_clear
sl_record "$O"; sl_mark "recording started: the sketch as take A left it"
sl_nap 2
bottom_edit 25 27 B
SL_SHOT_WAKE=0 sl_shot $O/green.png; sl_nap 2
read -r ZX ZY < <(B text Close); echo "sketch Close $ZX $ZY" >> $L
clk "$ZX $ZY" "sketch: Close"; sl_nap 3
sl_glide 1500 900 20; sl_key 0 "key 0: isometric"; sl_nap 3
SL_SHOT_WAKE=0 sl_shot $O/padded.png
read -r PX PY < <(ROW hook Pad); echo "Pad row $PX $PY" >> $L
clk "$PX $PY" "tree: Pad"; sl_nap 1.2
console_line "$O" "Gui.Selection.getSelection()[0].Shape.Volume"
SL_SHOT_WAKE=0 sl_shot $O/volume.png
sl_mark "recording stopped"; sl_stop
Q "import FreeCAD
d = FreeCAD.getDocument('hook'); p = d.getObject('Pad'); s = d.getObject('Sketch')
print('READ B pad valid', p.isValid(), 'volume', p.Shape.Volume, 'solve', s.solve(), 'DoF', s.DoF, 'bottom', s.Constraints[17].Value, 'arm top', s.Geometry[4].length())
d.saveCopy('/tmp/fx20/B-fixed.FCStd')" >> $L 2>&1
cp /tmp/fx20/B-fixed.FCStd $O/B-fixed.FCStd 2>/dev/null

# ================= take C: a reading, not an order
O=$X/C; L=$X/C/take.log; : > $L
sl_glide 1500 900 20; sl_key 1 "key 1: front (not filmed)"; sl_nap 2
read -r SKX SKY < <(ROW hook Sketch); echo "Sketch row $SKX $SKY" >> $L
report_hide
sl_record "$O"; sl_mark "recording started: B's result (bottom 27, Pad 8700)"
sl_nap 2
sl_glide "$SKX" "$SKY" 20; sl_nap 0.4
xdotool click --repeat 2 --delay 120 1; sl_mark "tree: double-click Sketch"; sl_nap 4
dim_arm 17 C
clk "$((PLX + 36)) $((PLY + 150))" "Insert Length: tick Reference"; sl_nap 1.5
sl_key Return "C: Return (OK), no value typed"; sl_nap 4
SL_SHOT_WAKE=0 sl_shot $O/ref.png
{ echo "C ref:"; sk_state hook; } >> $L 2>&1
sl_glide 1500 700 15; sl_key Escape "Esc: Dimension tool off"; sl_nap 2
bottom_edit 27 30 C
SL_SHOT_WAKE=0 sl_shot $O/ref30.png; sl_nap 2
{ echo "C bottom 30:"; sk_state hook; solver_text; } >> $L 2>&1
sl_key ctrl+z "Ctrl+Z: back to 27"; sl_nap 3
SL_SHOT_WAKE=0 sl_shot $O/undo.png
sl_mark "recording stopped"; sl_stop
{ echo "C after:"; sk_state hook; solver_text; } >> $L 2>&1
fc_quit; sl_display_stop
echo "ABC done"
