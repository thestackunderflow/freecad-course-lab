#!/bin/bash
# fx19 takes A and B (LAB-fx19 3.A, 3.B; PLAN rev 3 lab fills: A ends with the box's OK then Cancel, the Pad removed;
# B = Validate, rejoin the gap, close, Validate again, Pad again, the volume line). One container, two recordings.
#   FCC_PREFIX=fx19 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fx19_AB.sh
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh
mkdir -p $X/A $X/B; L=$X/A/take.log; : > $L
fx_start $X/A
mkdir -p /tmp/fx19; cp $X/P/hook-gap.FCStd /tmp/fx19/hook-gap.FCStd
open_doc /tmp/fx19/hook-gap.FCStd >> $L 2>&1
sleep 2

read -r SKX SKY < <(row_open hook_gap Sketch); echo "Sketch row $SKX $SKY" >> $L
BASE=$(nwin); echo "windows $BASE" >> $L
rv_clear
xdotool mousemove 1500 700
SL_SHOT_WAKE=0 sl_shot $X/A/before.png

# ================= take A: the refusal
O=$X/A
sl_record "$O"; sl_mark "recording started: FreeCAD, hook-gap open, Part Design, front view"
sl_nap 3
sl_glide 1300 900 20; sl_key 0 "key 0: isometric"; sl_nap 3.5
sl_key 1 "key 1: front"; sl_nap 2.5
clk "$SKX $SKY" "tree: Sketch"; sl_nap 1.5
sl_glide 50 228 20; sl_mark "hover: Pad"; sl_nap 1.2
sl_click 50 228 "Pad"; sl_nap 2.5
sl_type "20" "Pad: typed 20" 250; sl_nap 2
clk "$TASK_OK" "Pad: OK"; sl_nap 1
sl_mark "Input error box: Wire is not closed."
sl_nap 8
SL_SHOT_WAKE=0 sl_shot $O/refusal.png
echo "windows with the box $(nwin)" >> $L
clk "$BOX_OK" "box: OK"; sl_nap 2.5
SL_SHOT_WAKE=0 sl_shot $O/panel-still-open.png
clk "$TASK_CANCEL" "task: Cancel (the Pad is removed)"; sl_nap 3
SL_SHOT_WAKE=0 sl_shot $O/after-cancel.png
sl_mark "recording stopped"; sl_stop
Q "import FreeCAD
d = FreeCAD.getDocument('hook_gap'); print([o.Name for o in d.Objects if not o.Name.startswith(('X_','Y_','Z_','XY','XZ','YZ'))])" >> $L 2>&1

# ================= take B: the fix
O=$X/B; L=$X/B/take.log; : > $L
rv_clear
sl_record "$O"; sl_mark "recording started: the state take A left (sketch only, the Pad removed)"
sl_nap 2
clk "$SKX $SKY" "tree: Sketch"; sl_nap 1
clk "$SKETCH_MENU" "Sketch menu"; sl_nap 1.2
sl_glide 595 249 15; sl_mark "hover: Validate Sketch"; sl_nap 0.8
sl_click 595 249 "Validate Sketch"; sl_nap 3
clk "$HIGHLIGHT_BTN" "Highlight Troublesome Vertices"; sl_nap 4
SL_SHOT_WAKE=0 sl_shot $O/validate.png
clk "$VALID_CLOSE" "validation: Close"; sl_nap 2
# into the sketch
sl_glide "$SKX" "$SKY" 20; sl_nap 0.4
xdotool click --repeat 2 --delay 120 1; sl_mark "tree: double-click Sketch"; sl_nap 3.5
SL_SHOT_WAKE=0 sl_shot $O/sketch-open.png
read -r CX CY < <(SP hook_gap Sketch 7 end); read -r FX FY < <(SP hook_gap Sketch 0 start)
echo "corner before zoom: closing end $CX $CY, first start $FX $FY" >> $L
sl_glide "$FX" "$FY" 20; sl_mark "zoom in on the corner"
DIR=4; n=0; prev=$(( (FY - CY) < 0 ? CY - FY : FY - CY ))
while [ $n -lt 24 ]; do
  xdotool click $DIR; sleep 0.35; n=$((n + 1))
  if [ $((n % 3)) -eq 0 ]; then
    read -r CX CY < <(SP hook_gap Sketch 7 end); read -r FX FY < <(SP hook_gap Sketch 0 start)
    d=$(( (FY - CY) < 0 ? CY - FY : FY - CY )); echo "scroll $n button $DIR: apart $d px" >> $L
    [ "$d" -lt "$prev" ] && [ $n -eq 3 ] && DIR=5
    prev=$d; [ "$d" -ge 60 ] && break
    xdotool mousemove "$FX" "$FY"
  fi
done
sl_nap 2
SL_SHOT_WAKE=0 sl_shot $O/gap-zoomed.png
Q "import FreeCAD; print('constraints before', len(FreeCAD.getDocument('hook_gap').getObject('Sketch').Constraints))" >> $L 2>&1
clk "$CX $CY" "pick: the closing line's end"; sl_nap 1
clk "$FX $FY" "pick: the first line's start"; sl_nap 1.2
xdotool mousemove $((FX + 120)) $((FY - 120)); sl_nap 0.4
sl_key c "key C: coincident"; sl_nap 3
SL_SHOT_WAKE=0 sl_shot $O/joined.png
Q "import FreeCAD
s = FreeCAD.getDocument('hook_gap').getObject('Sketch')
print('constraints after', len(s.Constraints), [c.Type for c in s.Constraints][-2:], 'DoF', s.solve(), s.DoF, 'closing end', s.Geometry[7].EndPoint)" >> $L 2>&1
sl_glide 1500 900 20; sl_key Escape "Esc: selection cleared"; sl_nap 1
read -r ZX ZY < <(B text Close); echo "sketch Close $ZX $ZY" >> $L
clk "$ZX $ZY" "sketch: Close"; sl_nap 3
# validate again
clk "$SKX $SKY" "tree: Sketch"; sl_nap 1
clk "$SKETCH_MENU" "Sketch menu"; sl_nap 1.2
sl_glide 595 249 15; sl_nap 0.6; sl_click 595 249 "Validate Sketch (again)"; sl_nap 3
clk "$HIGHLIGHT_BTN" "Highlight Troublesome Vertices (again)"; sl_nap 3
close_box_if_any "$BASE" "box after the second highlight: Return" >> $L
SL_SHOT_WAKE=0 sl_shot $O/validate-again.png
sl_nap 2
clk "$VALID_CLOSE" "validation: Close"; sl_nap 2
# Pad again
clk "$SKX $SKY" "tree: Sketch"; sl_nap 1
sl_glide 50 228 20; sl_mark "hover: Pad"; sl_nap 1
sl_click 50 228 "Pad (again)"; sl_nap 2.5
sl_type "20" "Pad: typed 20" 250; sl_nap 2
clk "$TASK_OK" "Pad: OK"; sl_nap 2
echo "windows after Pad OK $(nwin) (baseline $BASE)" >> $L
sl_glide 1500 900 20; sl_key 0 "key 0: isometric"; sl_nap 3
SL_SHOT_WAKE=0 sl_shot $O/padded.png
read -r PX PY < <(ROW hook_gap Pad); echo "Pad row $PX $PY" >> $L
# View, Panels, Python console; the Pad clicked; the lesson-1 line
sl_click 211 36 "View menu"
sl_glide 255 1043 25; sl_mark "View: Panels"; sl_nap 0.6
sl_glide 700 1043 25; sl_nap 0.3
sl_click 800 1124 "Panels: Python console"; sl_nap 2
clk "$PX $PY" "tree: Pad"; sl_nap 1.2
read -r KX KY < <(B console); echo "console $KX $KY" >> $L
clk "$KX $KY" "console: click"
sl_type "Gui.Selection.getSelection()[0].Shape.Volume" "console: typed the volume line" 85
sl_key Return "console: Enter"; sl_nap 4
SL_SHOT_WAKE=0 sl_shot $O/volume.png
sl_mark "recording stopped"; sl_stop
Q "import FreeCAD
d = FreeCAD.getDocument('hook_gap'); p = d.getObject('Pad'); s = d.getObject('Sketch')
print('READ pad valid', p.isValid(), 'volume', p.Shape.Volume, 'wire closed', [w.isClosed() for w in s.Shape.Wires], 'DoF', s.DoF)
d.saveCopy('/tmp/fx19/B-fixed.FCStd')" >> $L 2>&1
cp /tmp/fx19/B-fixed.FCStd $O/B-fixed.FCStd 2>/dev/null
fc_quit; sl_display_stop
echo "AB done"
