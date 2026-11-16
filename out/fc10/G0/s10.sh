read -r RX RY < <(row_open rect Sketch); xdotool mousemove $RX $RY; sleep 0.5; xdotool click --repeat 2 --delay 120 1; sleep 4
echo "q5 in edit: $(Q 'import FreeCADGui; print(FreeCADGui.ActiveDocument.getInEdit())')" >> $L
FQ "look('rect', 'Top', 40, 30, 0, 160)" > /dev/null; sleep 1
read -r AX AY < <(vp 30 20 0); read -r BX BY < <(vp 75 55 0); echo "q5 rect corners at $AX $AY / $BX $BY" >> $L
xdotool mousemove 1500 300; sleep 0.3; xdotool key g; sleep 0.2; xdotool key r; sleep 1
xdotool mousemove $AX $AY; sleep 0.8; xdotool click 1; sleep 0.8
for i in $(seq 1 10); do xdotool mousemove $((AX + (BX - AX) * i / 10)) $((AY + (BY - AY) * i / 10)); sleep 0.05; done
sleep 0.5; xdotool click 1; sleep 1.5; xdotool key Escape; sleep 1; xdotool mousemove 1500 300; sleep 0.5
shot $O/q5-rect.png
echo "q5 solver_text: $(solver_text)" >> $L
Q "import FreeCAD
s = FreeCAD.getDocument('rect').getObject('Sketch')
print('q5 drawn', len(s.Geometry), 'cons', [c.Type for c in s.Constraints], 'DoF', s.DoF, [(round(g.StartPoint.x,2), round(g.StartPoint.y,2)) for g in s.Geometry if 'Line' in g.TypeId])" >> $L
