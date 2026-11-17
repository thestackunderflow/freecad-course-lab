F=hook; echo "== s9 (retry, checkbox at +37,+132) $(date -u +%T) route 2: Reference ticked in the dialog, then Toggle Driving/Reference (K, X) on it" >> $L
read -r MX MY < <(SP $F HookSketch 5 mid); xdotool mousemove $MX $MY; sleep 0.5; xdotool click 1; sleep 1
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key d; sleep 3
g=$(xdotool search --name 'Insert Length' getwindowgeometry 2>/dev/null | tr '\n' ' ')
read -r DX DY < <(echo "$g" | sed -E 's/.*Position: ([0-9]+),([0-9]+).*/\1 \2/')
xdotool mousemove $((DX + 37)) $((DY + 132)); sleep 0.5; xdotool click 1; sleep 1; shot $O/q3b-ref-ticked.png
xdotool mousemove $((DX + 135)) $((DY + 190)); sleep 0.5; xdotool click 1; sleep 4
echo "after ref OK: $(live11 $F)" >> $L
echo "solver: $(solver_text)" >> $L; shot $O/q3b-ref-added.png
n=$(Q "import FreeCAD; print(len(FreeCAD.getDocument('$F').getObject('HookSketch').Constraints) - 1)")
Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); FreeCADGui.Selection.addSelection('$F', 'HookSketch', 'Constraint$((n + 1))'); print(1)" > /dev/null
echo "sel: $(selnames)" >> $L
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key x; sleep 4
echo "dialogs after K X: $(xdotool search --onlyvisible --name '.' getwindowname %@ 2>/dev/null | grep -v -E '^(FreeCAD|openbox)' | tr '\n' '|')" >> $L
shot $O/q3b-toggled-driving.png
echo "after toggle: $(live11 $F)" >> $L
echo "solver: $(solver_text)" >> $L
echo "report: $(report_text | tail -c 500)" >> $L
