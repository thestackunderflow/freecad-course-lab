O=$X/G0b; L=$O/g0b-log.txt; F=hook
echo "== s6 $(date -u +%T) 3b: K D on the back line, type =Params.plate_height in the box" >> $L
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key d; sleep 3
shot $O/s6-dialog.png
g=$(xdotool search --name 'Insert Length' getwindowgeometry 2>/dev/null | tr '\n' ' '); echo "dialog: $g" >> $L
[ -n "$g" ] || { echo "NO DIALOG" >> $L; exit 0; }
xdotool type --delay 150 '='; sleep 1.5; shot $O/s6-eq.png
xdotool type --delay 120 'Params.plate_height'; sleep 2; shot $O/s6-expr.png
