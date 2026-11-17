O=$X/G0b; L=$O/g0b-log.txt; F=hook
echo "== s8 $(date -u +%T) 3b: state after OK" >> $L
echo "solver: $(solver_text)" >> $L
echo "live: $(live11 $F)" >> $L
echo "cons tail: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('HookSketch'); print(len(sk.Constraints), [(i, c.Type, c.First, round(c.Value,3), c.Driving) for i, c in enumerate(sk.Constraints)][-3:], sk.ExpressionEngine[-2:])")" >> $L
echo "report: $(report_text | grep -v 'executed successfully' | tail -c 700)" >> $L
