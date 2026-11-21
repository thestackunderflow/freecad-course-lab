# Q2 trap in the GUI on peg-noshell, then route (b) on that GUI-made Thickness
lab_save peg $O/q3c-fixed-gui.FCStd > /dev/null 2>&1
Q "import FreeCAD; FreeCAD.closeDocument('peg'); print(1)" > /dev/null
cp $X/P/peg-noshell.FCStd /tmp/fc14/peg.FCStd; open_doc /tmp/fc14/peg.FCStd > /dev/null 2>&1; FQ "prep('peg')" > /dev/null 2>&1
Q "import FreeCADGui; g=FreeCADGui.getDocument('peg'); g.activeView().setAnimationEnabled(False); g.activeView().viewIsometric(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" > /dev/null; sleep 2
echo "S15 open: $(bstate peg)" >> $L
p=$(vp 0 0 50); xdotool mousemove ${p% *} ${p#* }; sleep 0.6; xdotool click 1; sleep 1.5
echo "S15 selection: $(selnames)" >> $L
p=$(B PartDesign_Thickness); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click 1; sleep 4
p=$(FQ "field_pos('Thickness')"); xdotool mousemove $(( ${p% *} - 40 )) ${p#* }; xdotool click 1; xdotool key ctrl+a; sleep 0.3
xdotool type --delay 150 "="; sleep 1.5; xdotool type --delay 100 "Params.wall"; sleep 1; xdotool key Return; sleep 1.5
e=$(FQ "expr_ok()"); xdotool mousemove ${e% *} ${e#* }; xdotool click 1; sleep 2
c=$(taskpos any "Make thickness inwards"); xdotool mousemove $(( ${c% *} - 238 )) ${c#* }; sleep 0.4; xdotool click 1; sleep 3
echo "S15 panel before OK: $(FQ "task_texts()" | grep -o '"Make thickness inwards"' | head -1) $(Q "import FreeCADGui
from PySide import QtWidgets
print([c.isChecked() for c in FreeCADGui.getMainWindow().findChildren(QtWidgets.QCheckBox) if c.isVisible() and 'inwards' in c.text()])")" >> $L
shot $O/q3c-panel.png
o=$(taskpos any OK); xdotool mousemove ${o% *} ${o#* }; sleep 0.4; xdotool click 1; sleep 3
echo "S15 after new Thickness: $(bstate peg)" >> $L
echo "S15 messages: dialogs $(dialogs) notices $(FQ "notices()") rep $(report_text | grep -v executed | tail -c 200)" >> $L
lab_save peg $O/q2-trap-gui.FCStd > /dev/null 2>&1
shot $O/q2-trap-iso.png
uiwatch 40
p=$(ROW peg Thickness); xdotool mousemove ${p% *} ${p#* }; sleep 0.3; xdotool click 1; sleep 0.4; xdotool click 3; sleep 1
m=$(ui menu "Move Feature After"); xdotool mousemove ${m% *} ${m#* }; sleep 0.4; xdotool click 1; sleep 2
c=$(ui combo "Beginning"); xdotool mousemove ${c% *} ${c#* }; sleep 0.4; xdotool click 1; sleep 1.5
q=$(ui popup "Pad"); xdotool mousemove ${q% *} ${q#* }; sleep 0.4; xdotool click 1; sleep 1
b=$(ui button OK); xdotool mousemove ${b% *} ${b#* }; sleep 0.4; xdotool click 1; sleep 3
echo "S15 route b on GUI trap: $(bstate peg) rep $(report_text | grep -v executed | tail -c 200)" >> $L
