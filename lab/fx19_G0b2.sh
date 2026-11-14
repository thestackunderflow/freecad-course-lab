# fx19 G0b phase 2 v2 (sourced by fx19_G0b.sh with PHASE2=1). No socket query while the modal "Input error" box is up
# (run 2: queued queries printed red code into the Report view). Its own OK at the place run 1's still shows it.
sl_click 1503 945 "dialog: OK (fixed, from run 1's still)"
sleep 2
sl_shot "$O/g0b-4-dialog-closed.png"; D g0b-4-dialog-closed
read -r RX RY < <(timeout 20 python3 -m lab.fcrpc row hook_gap Pad); echo "Pad row $RX $RY" >> "$O/g0b-log.txt"
if [ -n "$RX" ] && [ "$RX" != none ]; then
  xdotool mousemove $((RX - 10)) "$RY"; sleep 0.3; xdotool mousemove "$RX" "$RY"; sleep 3
  SL_SHOT_WAKE=0 sl_shot "$O/g0b-5-tree-tooltip.png"
fi
xdotool mousemove 1400 700; sleep 1
read -r CX CY < <(timeout 20 python3 -m lab.button text Cancel); echo "Cancel $CX $CY" >> "$O/g0b-log.txt"
[ -n "$CX" ] && [ "$CX" != none ] && sl_click "$CX" "$CY" "task: Cancel"
sleep 3
sl_shot "$O/g0b-6-after-cancel.png"; D g0b-6-after-cancel
Q "import FreeCAD
d = FreeCAD.getDocument('hook_gap')
print([(o.Name, o.isValid(), o.getStatusString()) for o in d.Objects if 'Pad' in o.Name or o.Name == 'Sketch'])" >> "$O/g0b-log.txt" 2>&1
Q "import FreeCADGui
FreeCADGui.Selection.clearSelection(); FreeCADGui.Selection.addSelection('hook_gap', 'Sketch'); print('sel')" >> "$O/g0b-log.txt" 2>&1
read -r SX SY < <(timeout 20 python3 -m lab.button menu Sketch); echo "Sketch menu $SX $SY" >> "$O/g0b-log.txt"
sl_click "$SX" "$SY" "Sketch menu"; sleep 1.5
SL_SHOT_WAKE=0 sl_shot "$O/g0b-7-sketch-menu.png"
xdotool key Escape; sleep 1
Q "import FreeCADGui
FreeCADGui.runCommand('Sketcher_ValidateSketch', 0); print('validate')" >> "$O/g0b-log.txt" 2>&1
sleep 3
sl_shot "$O/g0b-8-validate.png"; D g0b-8-validate
read -r HX HY < <(timeout 20 python3 -m lab.button text "Highlight Troublesome Vertices"); echo "Highlight $HX $HY" >> "$O/g0b-log.txt"
[ -n "$HX" ] && [ "$HX" != none ] && sl_click "$HX" "$HY" "Highlight Troublesome Vertices"
sleep 3
sl_shot "$O/g0b-9-highlight.png"; D g0b-9-highlight
echo "G0B-PHASE2-DONE" >> "$O/g0b-log.txt"
