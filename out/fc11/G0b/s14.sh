O=$X/G0b; L=$O/g0b-log.txt; F=rect
echo "== s14 (s12+s13 again: one Escape only; s12 left the sketch with the second Escape) $(date -u +%T) G0b 5: your-turn rectangle in the GUI: construction line corner to corner" >> $L
O=$X/G0b; L=$O/g0b-log.txt; F=rect
Q "import FreeCAD; [FreeCAD.closeDocument(n) for n in list(FreeCAD.listDocuments())]; print(1)" >> $L; sleep 2
cp $X/P/rect-pinned.FCStd /tmp/fc11/$F.FCStd
open_doc /tmp/fc11/$F.FCStd >> $L 2>&1; sleep 2
p=$(ROW $F Sketch); echo "row $p" >> $L; xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 4
FQ "look('$F', 'Top', 20, 15, 0, 60)" >> $L 2>&1; sleep 2
echo "solver at open: $(solver_text)" >> $L
shot $O/s14-open.png
p=$(B Sketcher_ToggleConstruction); echo "toggle btn $p" >> $L; xdotool mousemove ${p% *} ${p#* }; sleep 0.5; xdotool click 1; sleep 1
p=$(B Sketcher_CreateLine); echo "line btn $p" >> $L; xdotool mousemove ${p% *} ${p#* }; sleep 0.5; xdotool click 1; sleep 1
read -r AX AY < <(SP $F Sketch 0 start); read -r BX BY < <(SP $F Sketch 2 start); echo "corners $AX $AY / $BX $BY" >> $L
xdotool mousemove $AX $AY; sleep 0.8; xdotool click 1; sleep 0.8; xdotool mousemove $BX $BY; sleep 0.8; xdotool click 1; sleep 1
xdotool key Escape; sleep 1.5
shot $O/s14-line.png
echo "geo: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('Sketch'); print(len(sk.Geometry), [sk.getConstruction(i) for i in range(len(sk.Geometry))], round(sk.Geometry[-1].length(), 4), sk.DoF, len(sk.Constraints))")" >> $L
echo "solver: $(solver_text)" >> $L
read -r MX MY < <(SP $F Sketch 4 mid 0 0); echo "diag mid $MX $MY" >> $L; xdotool mousemove $MX $MY; sleep 0.5; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key d; sleep 3
g=$(xdotool search --onlyvisible --name 'Insert Length' getwindowgeometry 2>/dev/null | tr '\n' ' '); echo "dialog: $g" >> $L
shot $O/s14-dialog-driving.png
read -r DX DY < <(echo "$g" | sed -E 's/.*Position: ([0-9]+),([0-9]+).*/\1 \2/')
xdotool mousemove $((DX + 135)) $((DY + 190)); sleep 0.8; xdotool click 1; sleep 4
shot $O/s14-after-driving.png
echo "solver: $(solver_text)" >> $L
echo "cons: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('Sketch'); print(len(sk.Constraints), [(c.Type, c.First, round(c.Value,3), c.Driving) for c in sk.Constraints][-1], list(sk.RedundantConstraints))")" >> $L
echo "report: $(report_text | grep -v 'executed successfully' | tail -c 300)" >> $L
read -r MX MY < <(SP $F Sketch 4 mid 0 0); echo "diag mid $MX $MY" >> $L; xdotool mousemove $MX $MY; sleep 0.5; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key d; sleep 3
g=$(xdotool search --onlyvisible --name 'Insert Length' getwindowgeometry 2>/dev/null | tr '\n' ' '); echo "dialog: $g" >> $L
read -r DX DY < <(echo "$g" | sed -E 's/.*Position: ([0-9]+),([0-9]+).*/\1 \2/')
xdotool mousemove $((DX + 37)) $((DY + 132)); sleep 0.5; xdotool click 1; sleep 1; shot $O/s14-ref-ticked.png
xdotool mousemove $((DX + 135)) $((DY + 190)); sleep 0.5; xdotool click 1; sleep 4
shot $O/s14-after-ref.png
echo "solver: $(solver_text)" >> $L
echo "cons: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('Sketch'); print(len(sk.Constraints), [(c.Type, c.First, round(c.Value,4), c.Driving) for c in sk.Constraints][-1])")" >> $L
Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('Sketch'); sk.setDatum(8, FreeCAD.Units.Quantity('60 mm')); sk.solve(); FreeCAD.getDocument('$F').recompute(); print(1)" >> $L
sleep 2
echo "width 60: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('Sketch'); print(round(sk.Constraints[8].Value,4), round(sk.Geometry[4].length(), 6), round(sk.Constraints[-1].Value, 6), sk.Constraints[-1].Driving)")" >> $L
shot $O/s14-width60.png
