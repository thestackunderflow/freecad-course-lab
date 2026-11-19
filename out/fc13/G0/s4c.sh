F=trap; echo "== s4c (faces route: Face8 in one view, Ctrl + Face10 in the mirrored view) $(date -u +%T)" >> $L
cam() { Q "import FreeCAD, FreeCADGui
v = FreeCADGui.getDocument('$F').activeView(); v.viewTop()
v.setCameraOrientation(FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), $1).multiply(v.getCameraOrientation()))
FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" > /dev/null; sleep 2.5; }
Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null
btn Std_Measure "Measure"; sleep 2
cam -30; p=$(vp 28 0 40); xdotool mousemove $p; sleep 0.6; xdotool click 1; sleep 1.5
echo "pick 1 at $p: $(selnames)" >> $L
cam 30; p=$(vp -28 0 40); xdotool mousemove $p; sleep 0.6; xdotool keydown ctrl; xdotool click 1; xdotool keyup ctrl; sleep 3
echo "pick 2 at $p: $(selnames)" >> $L
echo "faces measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*' | tr '\n' ' ')" >> $L
shot $O/q6-measure-faces.png
at "$(taskpos any Close)" "Close"; sleep 1.5
