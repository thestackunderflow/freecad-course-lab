F=trap; echo "== s4 (Q6 Measure route on the GUI trap file) $(date -u +%T)" >> $L
mkdir -p /tmp/fc13; cp $O/q2-trap-gui.FCStd /tmp/fc13/$F.FCStd
open_doc /tmp/fc13/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1; report_hide; sleep 2
echo "docs: $(Q "import FreeCAD; print(list(FreeCAD.listDocuments()))")" >> $L
cam() { Q "import FreeCAD, FreeCADGui
v = FreeCADGui.getDocument('$F').activeView(); v.viewTop()
v.setCameraOrientation(FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), $1).multiply(v.getCameraOrientation()))
FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" > /dev/null; sleep 2; }
clr() { Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null; }
for a in 30 -30; do
  cam $a; clr
  for x in 28 -28; do
    p=$(vp $x 0 30); xdotool mousemove $p; sleep 0.5; xdotool click 1; sleep 1
    echo "rot $a: point ($x,0,30) at $p -> $(selnames)" >> $L; clr
  done
  shot $O/q6-cam$a.png
done
# faces route: face at +28 picked in view rot A, Ctrl + face at -28 picked in view rot B (orbit between)
btn Std_Measure "Measure"; sleep 2
cam 30; p=$(vp 28 0 30); xdotool mousemove $p; sleep 0.5; xdotool click 1; sleep 1.5
echo "faces 1: $(selnames)" >> $L
cam -30; p=$(vp -28 0 30); xdotool mousemove $p; sleep 0.5; xdotool keydown ctrl; xdotool click 1; xdotool keyup ctrl; sleep 3
echo "faces 2: $(selnames)" >> $L
echo "faces measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*\|"QLabel", "[^"]*"' | tr '\n' ' ')" >> $L
shot $O/q6-measure-faces.png
at "$(taskpos any Close)" "Close"; sleep 1.5; clr
# edges route: top view, the two inner rim edges (x = +-28 at z 50)
Q "import FreeCADGui; v=FreeCADGui.getDocument('$F').activeView(); v.viewTop(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >/dev/null; sleep 2
btn Std_Measure "Measure"; sleep 2
p=$(vp 28 0 50); xdotool mousemove $p; sleep 0.5; xdotool click 1; sleep 1.5
p=$(vp -28 0 50); xdotool mousemove $p; sleep 0.5; xdotool keydown ctrl; xdotool click 1; xdotool keyup ctrl; sleep 3
echo "edges sel: $(selnames)" >> $L
echo "edges measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*\|"QLabel", "[^"]*"' | tr '\n' ' ')" >> $L
shot $O/q6-measure-edges.png
at "$(taskpos any Close)" "Close"; sleep 1.5; clr
