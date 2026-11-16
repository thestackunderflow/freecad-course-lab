read -r CX CY < <(SP hook HookSketch 0 start)
xdotool mousemove $((CX - 25)) $((CY - 25)); sleep 0.5; xdotool mousedown 1; sleep 0.2
for i in 1 2 3 4 5 6 7 8 9 10; do xdotool mousemove $((CX - 25 + 5 * i)) $((CY - 25 + 5 * i)); sleep 0.05; done
xdotool mouseup 1; sleep 1
echo "q4e box select: $(selnames)" >> $L
p=$(B Sketcher_ConstrainCoincidentUnified); xdotool mousemove ${p% *} ${p#* }; sleep 1.5
shot $O/q4e-tooltip.png
xdotool click 1; sleep 2; xdotool mousemove 1500 300; sleep 1
echo "q4e solver_text: $(solver_text)" >> $L
Q "import FreeCAD
s = FreeCAD.getDocument('hook').getObject('HookSketch')
print('constraints', len(s.Constraints), [(c.Type, c.First, c.FirstPos, c.Second, c.SecondPos) for c in s.Constraints][22:], 'redundant', list(s.RedundantConstraints))" >> $L
shot $O/q4e-after-coincident.png
