# s1: open the pinned hook, edit HookSketch, click the inner face, the distance tool: what dialog?
F=hook; mkdir -p /tmp/fc11; cp $X/P/hook-pinned.FCStd /tmp/fc11/$F.FCStd
echo "== s1 $(date -u +%T)" >> $L
open_doc /tmp/fc11/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1; sleep 2
echo "cfg: $(grep -o -E '(AutoRemoveRedundants|AutoRecompute|ShowDialogOnDistanceConstraint)[^/]*' ~/.local/share/FreeCAD/v1-1/user.cfg ~/.config/FreeCAD/v1-1/user.cfg 2>/dev/null | tr '\n' ' ')" >> $L
echo "cfgfiles: $(ls ~/.config/FreeCAD* ~/.local/share/FreeCAD 2>/dev/null | tr '\n' ' ')" >> $L
echo "start: $(live11 $F)" >> $L
p=$(ROW $F HookSketch); xdotool mousemove ${p% *} ${p#* } click --repeat 2 --delay 120 1; sleep 4
FQ "look('$F', 'Front', 12, 0, 30, 90)" >> $L; sleep 2
echo "solver open: $(solver_text)" >> $L
shot $O/q1-sketch-open.png
read -r MX MY < <(SP $F HookSketch 5 mid); echo "inner mid $MX $MY" >> $L
xdotool mousemove $MX $MY; sleep 0.5; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L
echo "buttons: dist $(B Sketcher_ConstrainDistance) dim $(B Sketcher_Dimension) vdist $(B Sketcher_ConstrainDistanceY)" >> $L
