F=hook; echo "== s6 $(date -u +%T) OK clicked at 1936 1510 (dialog 1801,1320 456x252)" >> $L
xdotool mousemove 1936 1510; sleep 0.5; xdotool click 1; sleep 4
echo "dialog left: $(xdotool search --name 'Insert Length' 2>/dev/null | wc -l)" >> $L
echo "after OK click: $(live11 $F)" >> $L
echo "constraints: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('HookSketch'); print(len(sk.Constraints), [(c.Type, c.First, round(c.Value,3), c.Driving) for c in sk.Constraints][-1])")" >> $L
echo "solver: $(solver_text)" >> $L
shot $O/q1-after-okclick.png
