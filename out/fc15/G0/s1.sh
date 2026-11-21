F=cup; mkdir -p /tmp/fc15; cp /lab/out/fc15/P/rim-start.FCStd /tmp/fc15/cup.FCStd
open_doc /tmp/fc15/cup.FCStd; FQ "prep('cup')"; report_hide
Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); FreeCADGui.Selection.addSelection('cup','Pad001','Edge16'); FreeCADGui.runCommand('PartDesign_Fillet',0); print(1)"
sleep 4
Q "import FreeCAD; d=FreeCAD.getDocument('cup'); f=d.getObject('Fillet'); f.setExpression('Radius','Params.rim_out'); d.recompute(); print(f.State, f.getStatusString())"
uiwatch 30
at "$(taskpos any OK)" "OK"; sleep 4
echo "UI: $(ui dump)"
b=$(ui button OK); xdotool mousemove ${b% *} ${b#* } click 1; sleep 3
echo "dialogs: $(dialogs)"; echo "panel: $(FQ "task_texts()" | cut -c1-300)"; echo "state: $(fstate cup)"
echo "report: $(report_text)"
