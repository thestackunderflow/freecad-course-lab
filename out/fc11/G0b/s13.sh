O=$X/G0b; L=$O/g0b-log.txt; F=rect
echo "== s13 $(date -u +%T) G0b 5: driving diagonal (Reference unticked), then Reference ticked" >> $L
read -r MX MY < <(SP $F Sketch 4 mid 0 0); xdotool mousemove $MX $MY; sleep 0.5; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key d; sleep 3
g=$(xdotool search --onlyvisible --name 'Insert Length' getwindowgeometry 2>/dev/null | tr '\n' ' '); echo "dialog: $g" >> $L
shot $O/s13-dialog-driving.png
read -r DX DY < <(echo "$g" | sed -E 's/.*Position: ([0-9]+),([0-9]+).*/\1 \2/')
xdotool mousemove $((DX + 135)) $((DY + 190)); sleep 0.8; xdotool click 1; sleep 4
shot $O/s13-after-driving.png
echo "solver: $(solver_text)" >> $L
echo "cons: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('Sketch'); print(len(sk.Constraints), [(c.Type, c.First, round(c.Value,3), c.Driving) for c in sk.Constraints][-1], list(sk.RedundantConstraints))")" >> $L
echo "report: $(report_text | grep -v 'executed successfully' | tail -c 300)" >> $L
read -r MX MY < <(SP $F Sketch 4 mid 0 0); xdotool mousemove $MX $MY; sleep 0.5; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key d; sleep 3
g=$(xdotool search --onlyvisible --name 'Insert Length' getwindowgeometry 2>/dev/null | tr '\n' ' '); echo "dialog: $g" >> $L
read -r DX DY < <(echo "$g" | sed -E 's/.*Position: ([0-9]+),([0-9]+).*/\1 \2/')
xdotool mousemove $((DX + 37)) $((DY + 132)); sleep 0.5; xdotool click 1; sleep 1; shot $O/s13-ref-ticked.png
xdotool mousemove $((DX + 135)) $((DY + 190)); sleep 0.5; xdotool click 1; sleep 4
shot $O/s13-after-ref.png
echo "solver: $(solver_text)" >> $L
echo "cons: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('Sketch'); print(len(sk.Constraints), [(c.Type, c.First, round(c.Value,4), c.Driving) for c in sk.Constraints][-1])")" >> $L
Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('Sketch'); sk.setDatum(8, FreeCAD.Units.Quantity('60 mm')); sk.solve(); FreeCAD.getDocument('$F').recompute(); print(1)" >> $L
sleep 2
echo "width 60: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('Sketch'); print(round(sk.Constraints[8].Value,4), round(sk.Geometry[4].length(), 6), round(sk.Constraints[-1].Value, 6), sk.Constraints[-1].Driving)")" >> $L
shot $O/s13-width60.png
