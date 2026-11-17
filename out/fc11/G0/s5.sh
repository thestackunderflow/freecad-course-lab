F=hook; echo "== s5 $(date -u +%T) retry: OK clicked with the mouse" >> $L
p=$(ROW $F HookSketch); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 4
FQ "look('$F', 'Front', 12, 0, 30, 90)" >> $L 2>&1; sleep 2
read -r MX MY < <(SP $F HookSketch 5 mid); xdotool mousemove $MX $MY; sleep 0.5; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key d; sleep 3
echo "constraints while dialog: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('HookSketch'); print(len(sk.Constraints), [(c.Type, c.First, round(c.Value,3), c.Driving) for c in sk.Constraints][-1])")" >> $L
ok=$(WG text "OK"); echo "ok at $ok" >> $L
xdotool mousemove ${ok% *} ${ok#* }; sleep 0.5; xdotool click 1; sleep 3
echo "after OK click: $(live11 $F)" >> $L
echo "constraints: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('HookSketch'); print(len(sk.Constraints), [(c.Type, c.First, round(c.Value,3), c.Driving) for c in sk.Constraints][-1])")" >> $L
echo "solver: $(solver_text)" >> $L
shot $O/q1-after-okclick.png
