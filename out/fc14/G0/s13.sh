Q "import FreeCAD, FreeCADGui; d=FreeCAD.getDocument('peg'); d.getObject('Body').Tip=d.getObject('Pad'); g=FreeCADGui.getDocument('peg'); g.getObject('Pad001').Visibility=False; g.getObject('Pad').Visibility=True; g.activeView().setAnimationEnabled(False); g.activeView().viewIsometric(); FreeCADGui.SendMsgToActiveView('ViewFit'); FreeCADGui.Selection.clearSelection(); d.recompute(); print(1)" > /dev/null; sleep 2
p=$(vp 0 0 50); echo "S13 vp $p" >> $L; xdotool mousemove ${p% *} ${p#* }; sleep 0.6; xdotool click 1; sleep 1.5
echo "S13 selection: $(selnames)" >> $L
