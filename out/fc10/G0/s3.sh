FQ "look('hook', 'Front', 12, 0, 30, 90)" >> $L
Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null; sleep 1
read -r CX CY < <(SP hook HookSketch 0 start); read -r OX OY < <(SP hook HookSketch -1 origin)
echo "q4 corner $CX $CY origin $OX $OY" >> $L
xdotool mousemove $CX $CY; sleep 0.8; xdotool click 1; sleep 1
echo "q4 after click: $(selnames)" >> $L
xdotool keydown ctrl; xdotool click 1; xdotool keyup ctrl; sleep 1
echo "q4 after ctrl-click same spot: $(selnames)" >> $L
shot $O/q4-corner-select.png
