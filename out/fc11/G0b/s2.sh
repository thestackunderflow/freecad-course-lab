O=$X/G0b; L=$O/g0b-log.txt; F=hook
echo "== s2 $(date -u +%T) click the plate_height label, Delete; then K D on the inner face, OK" >> $L
read -r DXp DYp < <(cd /lab && timeout 20 python3 -m lab.dimpt $F HookSketch 20); echo "label 20 px $DXp $DYp" >> $L
xdotool mousemove $DXp $DYp; sleep 0.6; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L; shot $O/s2-selected.png
xdotool key Delete; sleep 3
echo "dialogs after Delete: $(xdotool search --onlyvisible --name '.' getwindowname %@ 2>/dev/null | grep -v -E '^(FreeCAD|openbox)' | tr '\n' '|')" >> $L
shot $O/s2-deleted.png
echo "solver after delete: $(solver_text)" >> $L
echo "after delete: $(live11 $F)" >> $L
echo "expr after delete: $(Q "import FreeCAD; print(FreeCAD.getDocument('$F').getObject('HookSketch').ExpressionEngine)")" >> $L
echo "report after delete: $(report_text | tail -c 400)" >> $L
read -r MX MY < <(SP $F HookSketch 5 mid); xdotool mousemove $MX $MY; sleep 0.5; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key d; sleep 3
shot $O/s2-dialog.png
g=$(xdotool search --name 'Insert Length' getwindowgeometry 2>/dev/null | tr '\n' ' '); echo "dialog: $g" >> $L
read -r DX DY < <(echo "$g" | sed -E 's/.*Position: ([0-9]+),([0-9]+).*/\1 \2/')
xdotool mousemove $((DX + 135)) $((DY + 190)); sleep 0.8; xdotool click 1; sleep 4
echo "dialog left: $(xdotool search --name 'Insert Length' 2>/dev/null | wc -l)" >> $L
shot $O/s2-after-ok.png
echo "solver after 55: $(solver_text)" >> $L
echo "after 55: $(live11 $F)" >> $L
echo "report: $(report_text | tail -c 600)" >> $L
