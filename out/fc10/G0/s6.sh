xdotool key ctrl+z; sleep 2
echo "q4g after undo: $(solver_text)" >> $L
Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null; sleep 1
read -r CX CY < <(SP hook HookSketch 0 start)
p=$(B Sketcher_ConstrainCoincidentUnified); xdotool mousemove ${p% *} ${p#* }; sleep 0.5; xdotool click 1; sleep 1
xdotool mousemove $CX $CY; sleep 0.8; xdotool click 1; sleep 1.5
shot $O/q4g-tool-first-click.png
xdotool click 1; sleep 2
echo "q4g tool-first two clicks: $(solver_text)" >> $L
Q "import FreeCAD
s = FreeCAD.getDocument('hook').getObject('HookSketch')
print('constraints', len(s.Constraints), [(c.Type, c.First, c.FirstPos, c.Second, c.SecondPos) for c in s.Constraints][22:])" >> $L
xdotool key Escape; sleep 1; xdotool mousemove 1500 300
echo "q4g after Esc: $(solver_text)" >> $L
