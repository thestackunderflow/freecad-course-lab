F=hook; echo "== s10 $(date -u +%T) Q1b on the toggled (driving, redundant) 55: Close at 60, then Params 60 -> 80 + Recompute" >> $L
rv_clear; at "$(B text Close)" "close" > /dev/null 2>&1; sleep 4
echo "after close: $(live11 $F)" >> $L
echo "report: $(report_text)" >> $L; shot $O/q1b-closed.png
Q "import FreeCAD; d = FreeCAD.getDocument('$F'); d.getObject('Params').set('plate_height', '80'); d.recompute(); print(1)" >> $L 2>&1; sleep 3
echo "after 80: $(live11 $F)" >> $L
echo "report: $(report_text | tail -c 600)" >> $L; shot $O/q2-at-80.png
lab_save $F $O/q2-redundant-80.FCStd >> $L 2>&1
echo "check saved 80: $(check11 $O/q2-redundant-80.FCStd $O/q2-redundant-80.check.json)" >> $L
