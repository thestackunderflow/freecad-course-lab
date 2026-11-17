O=$X/G0b; L=$O/g0b-log.txt
F=hook; echo "== s1 $(date -u +%T) pinned hook: delete the plate_height size on the back line, then K D 55 on the inner face" >> $L
mkdir -p /tmp/fc11; cp $X/P/hook-pinned.FCStd /tmp/fc11/$F.FCStd
open_doc /tmp/fc11/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1; sleep 2
echo "rows open: $(row_open $F HookSketch)" >> $L; xdotool mousemove 1500 1500; sleep 1
p=$(ROW $F HookSketch); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 4
FQ "look('$F', 'Front', 12, 0, 30, 90)" >> $L 2>&1; sleep 2
echo "solver at open: $(solver_text)" >> $L
echo "sizes: $(cd /lab && timeout 20 python3 -m lab.dimpt $F HookSketch list)" >> $L
echo "cons: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('HookSketch'); print([(i, c.Type, c.First, c.Second, round(c.Value,3), c.Name) for i, c in enumerate(sk.Constraints) if c.Type.startswith('Dist') or c.Name])")" >> $L
echo "expr: $(Q "import FreeCAD; print(FreeCAD.getDocument('$F').getObject('HookSketch').ExpressionEngine)")" >> $L
shot $O/s1-open.png
