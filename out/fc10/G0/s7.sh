Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null; sleep 1
read -r MX MY < <(SP hook HookSketch 7 mid); echo "q3 back line mid $MX $MY" >> $L
xdotool mousemove $MX $MY; sleep 0.8; xdotool mousedown 1; sleep 0.2
for i in $(seq 1 15); do xdotool mousemove $((MX + 4 * i)) $((MY - 3 * i)); sleep 0.04; done
sleep 0.3; xdotool mouseup 1; sleep 1.5
shot $O/q3-after-drag.png
Q "import FreeCAD
s = FreeCAD.getDocument('hook').getObject('HookSketch'); g = s.Geometry[0]
print('q3 corner after drag', round(g.StartPoint.x, 3), round(g.StartPoint.y, 3))" >> $L
read -r ZX ZY < <(B text Close); xdotool mousemove $ZX $ZY; sleep 0.5; xdotool click 1; sleep 3
echo "q3 live after close: $(live hook)" >> $L
FQ "prep('hook')" > /dev/null; sleep 1; shot $O/q3-closed-iso.png
