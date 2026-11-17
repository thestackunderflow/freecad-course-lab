F=hook; echo "== s7 $(date -u +%T) fresh FreeCAD: clean add, no query while the dialog is up" >> $L
cp $X/P/hook-pinned.FCStd /tmp/fc11/$F.FCStd 2>/dev/null || { mkdir -p /tmp/fc11; cp $X/P/hook-pinned.FCStd /tmp/fc11/$F.FCStd; }
open_doc /tmp/fc11/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1; sleep 2
echo "param AutoRemoveRedundants (default True/False asked): $(Q "import FreeCAD; p = FreeCAD.ParamGet('User parameter:BaseApp/Preferences/Mod/Sketcher'); print(p.GetBool('AutoRemoveRedundants', True), p.GetBool('AutoRemoveRedundants', False), p.GetBool('AutoRecompute', True), p.GetBool('AutoRecompute', False), p.GetBool('ShowDialogOnDistanceConstraint', True))")" >> $L
echo "rows open: $(row_open $F HookSketch)" >> $L; xdotool mousemove 1500 1500; sleep 1
p=$(ROW $F HookSketch); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 4
FQ "look('$F', 'Front', 12, 0, 30, 90)" >> $L 2>&1; sleep 2
read -r MX MY < <(SP $F HookSketch 5 mid); xdotool mousemove $MX $MY; sleep 0.5; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key d; sleep 3
shot $O/q1-dialog.png
g=$(xdotool search --name 'Insert Length' getwindowgeometry 2>/dev/null | tr '\n' ' '); echo "dialog: $g" >> $L
read -r DX DY < <(echo "$g" | sed -E 's/.*Position: ([0-9]+),([0-9]+).*/\1 \2/')
xdotool mousemove $((DX + 135)) $((DY + 190)); sleep 0.8; shot $O/q1-ok-hover.png; xdotool click 1; sleep 4
echo "dialog left: $(xdotool search --name 'Insert Length' 2>/dev/null | wc -l)" >> $L
shot $O/q1-after-ok.png
echo "after OK: $(live11 $F)" >> $L
echo "constraints: $(Q "import FreeCAD; sk = FreeCAD.getDocument('$F').getObject('HookSketch'); print(len(sk.Constraints), [(c.Type, c.First, round(c.Value,3), c.Driving) for c in sk.Constraints][-1])")" >> $L
echo "solver: $(solver_text)" >> $L
echo "report: $(report_text)" >> $L
