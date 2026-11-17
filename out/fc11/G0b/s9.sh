O=$X/G0b; L=$O/g0b-log.txt; F=hook
echo "== s9 $(date -u +%T) 3b: Close at 60, then Params 80 + recompute" >> $L
p=$(B text Close); xdotool mousemove ${p% *} ${p#* }; sleep 0.5; xdotool click 1; sleep 3
echo "after close: $(live11 $F)" >> $L
echo "report after close: $(report_text | grep -v 'executed successfully' | tail -c 500)" >> $L
shot $O/s9-closed-60.png
lab_save $F $O/hook-3b.FCStd >> $L 2>&1
Q "import FreeCAD; d = FreeCAD.getDocument('$F'); d.getObject('Params').set('plate_height', '80'); d.recompute(); print(1)" >> $L
sleep 2
echo "at 80: $(live11 $F)" >> $L
echo "report at 80: $(report_text | grep -v 'executed successfully' | tail -c 500)" >> $L
shot $O/s9-at-80.png
