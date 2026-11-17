O=$X/G0b; L=$O/g0b-log.txt; F=rect
echo "== s12 $(date -u +%T) G0b 5: your-turn rectangle in the GUI: construction line corner to corner" >> $L
Q "import FreeCAD; [FreeCAD.closeDocument(n) for n in list(FreeCAD.listDocuments())]; print(1)" >> $L; sleep 2
cp $X/P/rect-pinned.FCStd /tmp/fc11/$F.FCStd
open_doc /tmp/fc11/$F.FCStd >> $L 2>&1; sleep 2
p=$(ROW $F Sketch); echo "row $p" >> $L; xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 4
FQ "look('$F', 'Top', 20, 15, 0, 60)" >> $L 2>&1; sleep 2
echo "solver at open: $(solver_text)" >> $L
shot $O/s12-open.png
p=$(B Sketcher_ToggleConstruction); echo "toggle btn $p" >> $L; xdotool mousemove ${p% *} ${p#* }; sleep 0.5; xdotool click 1; sleep 1
p=$(B Sketcher_CreateLine); echo "line btn $p" >> $L; xdotool mousemove ${p% *} ${p#* }; sleep 0.5; xdotool click 1; sleep 1
read -r AX AY < <(SP $F Sketch 0 start); read -r BX BY < <(SP $F Sketch 2 start); echo "corners $AX $AY / $BX $BY" >> $L
xdotool mousemove $AX $AY; sleep 0.8; xdotool click 1; sleep 0.8; xdotool mousemove $BX $BY; sleep 0.8; xdotool click 1; sleep 1
xdotool key Escape; sleep 1; xdotool key Escape; sleep 1
shot $O/s12-line.png
echo "geo: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('Sketch'); print(len(sk.Geometry), [sk.getConstruction(i) for i in range(len(sk.Geometry))], round(sk.Geometry[-1].length(), 4), sk.DoF, len(sk.Constraints))")" >> $L
echo "solver: $(solver_text)" >> $L
