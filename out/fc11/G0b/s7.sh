O=$X/G0b; L=$O/g0b-log.txt; F=hook
echo "== s7 $(date -u +%T) 3b: accept the expression, OK the box" >> $L
xdotool key Return; sleep 1.5; shot $O/s7-ret1.png
echo "expr editor open after Return: $(xdotool search --onlyvisible --name 'Expression Editor' 2>/dev/null | wc -l)" >> $L
if [ "$(xdotool search --onlyvisible --name 'Expression Editor' 2>/dev/null | wc -l)" -gt 0 ]; then xdotool key Return; sleep 1.5; shot $O/s7-ret2.png; fi
echo "expr editor open after 2nd: $(xdotool search --onlyvisible --name 'Expression Editor' 2>/dev/null | wc -l)" >> $L
shot $O/s7-box-with-expr.png
g=$(xdotool search --onlyvisible --name 'Insert Length' getwindowgeometry 2>/dev/null | tr '\n' ' '); echo "insert length: $g" >> $L
if [ -n "$g" ]; then
  read -r DX DY < <(echo "$g" | sed -E 's/.*Position: ([0-9]+),([0-9]+).*/\1 \2/')
  xdotool mousemove $((DX + 135)) $((DY + 190)); sleep 0.8; xdotool click 1; sleep 4
fi
echo "dialogs: $(xdotool search --onlyvisible --name '.' getwindowname %@ 2>/dev/null | grep -v -E '^(FreeCAD|openbox)' | tr '\n' '|')" >> $L
shot $O/s7-after-ok.png
