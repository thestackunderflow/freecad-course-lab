O=$X/G0b; L=$O/g0b-log.txt; F=hook
echo "== s11 $(date -u +%T) G0b 3: back line K D =Params.plate_height, OK, Close, Recompute" >> $L
read -r MX MY < <(SP $F HookSketch 7 start 0 60); xdotool mousemove $MX $MY; sleep 0.5; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key d; sleep 3
shot $O/s11-dialog.png
g=$(xdotool search --onlyvisible --name 'Insert Length' getwindowgeometry 2>/dev/null | tr '\n' ' '); echo "dialog: $g" >> $L
[ -n "$g" ] || { echo "NO DIALOG" >> $L; exit 0; }
read -r DX DY < <(echo "$g" | sed -E 's/.*Position: ([0-9]+),([0-9]+).*/\1 \2/')
xdotool type --delay 150 '='; sleep 1.5
xdotool type --delay 120 'Params.plate_height'; sleep 2; shot $O/s11-expr.png
xdotool key Return; sleep 1.5
[ "$(xdotool search --onlyvisible --name 'Expression Editor' 2>/dev/null | wc -l)" -gt 0 ] && { xdotool key Return; sleep 1.5; }
shot $O/s11-box-with-expr.png
xdotool mousemove $((DX + 135)) $((DY + 190)); sleep 0.8; xdotool click 1; sleep 4
echo "dialogs: $(xdotool search --onlyvisible --name '.' getwindowname %@ 2>/dev/null | grep -v -E '^(FreeCAD|openbox)' | tr '\n' '|')" >> $L
shot $O/s11-after-ok.png
echo "solver: $(solver_text)" >> $L
echo "live: $(live11 $F)" >> $L
p=$(B text Close); xdotool mousemove ${p% *} ${p#* }; sleep 0.5; xdotool click 1; sleep 3
p=$(B Std_Refresh); xdotool mousemove ${p% *} ${p#* }; sleep 0.5; xdotool click 1; sleep 3
echo "after close + recompute: $(live11 $F)" >> $L
echo "report: $(report_text | grep -v 'executed successfully' | tail -c 500)" >> $L
FQ "look('$F', 'Front', 12, 0, 40, 110)" >> $L 2>&1; sleep 2; shot $O/s11-fixed-80.png
lab_save $F $O/hook-fixed.FCStd >> $L 2>&1
