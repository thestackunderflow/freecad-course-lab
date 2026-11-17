O=$X/G0b; L=$O/g0b-log.txt; F=hook
echo "== s4 $(date -u +%T) 3b: fresh orphan, back line sized =Params.plate_height WHILE the 55 is driving" >> $L
Q "import FreeCAD; FreeCAD.closeDocument('$F'); print(1)" >> $L; sleep 2
cp $O/hook-orphan.FCStd /tmp/fc11/$F.FCStd
open_doc /tmp/fc11/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1; sleep 2
echo "rows open: $(row_open $F HookSketch)" >> $L; xdotool mousemove 1500 1500; sleep 1
p=$(ROW $F HookSketch); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 4
FQ "look('$F', 'Front', 12, 0, 30, 90)" >> $L 2>&1; sleep 2
echo "solver at open: $(solver_text)" >> $L
read -r MX MY < <(SP $F HookSketch 7 mid); xdotool mousemove $MX $MY; sleep 0.5; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key d; sleep 3
shot $O/s4-dialog.png
g=$(xdotool search --name 'Insert Length' getwindowgeometry 2>/dev/null | tr '\n' ' '); echo "dialog: $g" >> $L
read -r DX DY < <(echo "$g" | sed -E 's/.*Position: ([0-9]+),([0-9]+).*/\1 \2/')
xdotool type --delay 150 '='; sleep 1.5; shot $O/s4-eq.png
xdotool type --delay 120 'Params.plate_height'; sleep 1.5; shot $O/s4-expr.png
xdotool key Return; sleep 1.5; shot $O/s4-expr-enter.png
echo "dialog still: $(xdotool search --onlyvisible --name 'Insert Length' 2>/dev/null | wc -l)" >> $L
