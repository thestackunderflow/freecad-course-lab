F=hook; echo "== s2 $(date -u +%T)" >> $L
Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null
echo "rows open: $(row_open $F HookSketch)" >> $L; xdotool mousemove 1500 1500; sleep 1
p=$(ROW $F HookSketch); echo "row $p" >> $L; xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 4
echo "editing: $(Q "import FreeCADGui; print(FreeCADGui.ActiveDocument.getInEdit())")" >> $L
FQ "look('$F', 'Front', 12, 0, 30, 90)" >> $L 2>&1; sleep 2
echo "solver open: $(solver_text)" >> $L
shot $O/q1-sketch-open.png
read -r MX MY < <(SP $F HookSketch 5 mid); echo "inner mid $MX $MY" >> $L
xdotool mousemove $MX $MY; sleep 0.5; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L
echo "buttons: dist $(B Sketcher_ConstrainDistance) dim $(B Sketcher_Dimension) vdist $(B Sketcher_ConstrainDistanceY)" >> $L
