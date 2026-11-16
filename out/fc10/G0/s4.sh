read -r CX CY < <(SP hook HookSketch 0 start)
Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null; sleep 1
# (d) box select: drag from up-left of the corner to down-right, empty space start
xdotool mousemove $((CX - 25)) $((CY - 25)); sleep 0.5; xdotool mousedown 1; sleep 0.2
for i in 1 2 3 4 5 6 7 8 9 10; do xdotool mousemove $((CX - 25 + 5 * i)) $((CY - 25 + 5 * i)); sleep 0.05; done
xdotool mouseup 1; sleep 1
echo "q4d box select: $(selnames)" >> $L
shot $O/q4d-box.png
Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null; sleep 1
xdotool mousemove 1500 300; sleep 0.5
