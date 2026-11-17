O=$X/G0b; L=$O/g0b-log.txt; F=hook
echo "== s5 $(date -u +%T) 3b retry (s4 clicked the 55's label on the back line): back line clicked near its top" >> $L
Q "import FreeCAD; FreeCAD.closeDocument('$F'); print(1)" >> $L; sleep 2
cp $O/hook-orphan.FCStd /tmp/fc11/$F.FCStd
open_doc /tmp/fc11/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1; sleep 2
echo "rows open: $(row_open $F HookSketch)" >> $L; xdotool mousemove 1500 1500; sleep 1
p=$(ROW $F HookSketch); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 4
FQ "look('$F', 'Front', 12, 0, 30, 90)" >> $L 2>&1; sleep 2
echo "geo7: $(Q "import FreeCAD; g = FreeCAD.getDocument('$F').getObject('HookSketch').Geometry[7]; print(g.StartPoint, g.EndPoint)")" >> $L
read -r MX MY < <(SP $F HookSketch 7 start 0 60); echo "click $MX $MY" >> $L
xdotool mousemove $MX $MY; sleep 0.5; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L
