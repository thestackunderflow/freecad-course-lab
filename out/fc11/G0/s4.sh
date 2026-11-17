F=hook; echo "== s4 $(date -u +%T)" >> $L
xdotool key Return; sleep 3
echo "after OK: $(live11 $F)" >> $L
echo "solver: $(solver_text)" >> $L
shot $O/q1-after-ok.png
rv_clear
at "$(B text Close)" "close" > /dev/null 2>&1; sleep 4
echo "editing after close: $(Q "import FreeCADGui; print(FreeCADGui.ActiveDocument.getInEdit())")" >> $L
echo "after close: $(live11 $F)" >> $L
echo "report: $(report_text)" >> $L
shot $O/q1b-closed-60.png
