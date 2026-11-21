# Q3b route (c): fresh trap; delete Thickness; Set Tip on Pad; new Thickness (top face, =Params.wall, untick); Set Tip on Pad001
ctx() {  # ctx OBJ ITEM: right-click a tree row, click a menu item (positions from the watcher)
  uiwatch 20; local p m; p=$(ROW peg $1); xdotool mousemove ${p% *} ${p#* }; sleep 0.3; xdotool click 1; sleep 0.4; xdotool click 3; sleep 1
  m=$(ui menu "$2"); echo "S12 ctx $1 $2 at $m" >> $L; xdotool mousemove ${m% *} ${m#* }; sleep 0.4; xdotool click 1; sleep 2.5
  echo "S12 ui after $1 $2: $(ui dump | cut -c1-400)" >> $L
}
Q "import FreeCAD; FreeCAD.closeDocument('peg'); print(1)" > /dev/null
cp $X/P/peg-trap.FCStd /tmp/fc14/peg.FCStd; open_doc /tmp/fc14/peg.FCStd > /dev/null 2>&1; FQ "prep('peg')" > /dev/null 2>&1
row_open peg Thickness > /dev/null 2>&1; sleep 1
uiwatch 20
p=$(ROW peg Thickness); xdotool mousemove ${p% *} ${p#* }; sleep 0.3; xdotool click 1; sleep 0.5; xdotool key Delete; sleep 2.5
echo "S12 ui after Delete: $(ui dump | cut -c1-500)" >> $L
echo "S12 after delete: $(bstate peg)" >> $L
ctx Pad "Set Tip"
echo "S12 after Set Tip Pad: $(bstate peg)" >> $L
shot $O/q3c-tip-pad.png
Q "import FreeCADGui; FreeCADGui.getDocument('peg').activeView().viewIsometric(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" > /dev/null; sleep 1
p=$(vp 0 0 50); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click 1; sleep 1.5
echo "S12 selection: $(selnames)" >> $L
p=$(B PartDesign_Thickness); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click 1; sleep 4
p=$(FQ "field_pos('Thickness')"); xdotool mousemove $(( ${p% *} - 40 )) ${p#* }; xdotool click 1; xdotool key ctrl+a; sleep 0.3
xdotool type --delay 150 "="; sleep 1.5; xdotool type --delay 100 "Params.wall"; sleep 1; xdotool key Return; sleep 1.5
e=$(FQ "expr_ok()"); xdotool mousemove ${e% *} ${e#* }; xdotool click 1; sleep 2
c=$(taskpos any "Make thickness inwards"); xdotool mousemove $(( ${c% *} - 238 )) ${c#* }; sleep 0.4; xdotool click 1; sleep 3
echo "S12 panel before OK: $(FQ "task_texts()" | grep -o '"Make thickness inwards"' | head -1) $(Q "import FreeCADGui
from PySide import QtWidgets
print([c.isChecked() for c in FreeCADGui.getMainWindow().findChildren(QtWidgets.QCheckBox) if c.isVisible() and 'inwards' in c.text()])")" >> $L
shot $O/q3c-panel.png
o=$(taskpos any OK); xdotool mousemove ${o% *} ${o#* }; sleep 0.4; xdotool click 1; sleep 3
echo "S12 after new Thickness: $(bstate peg)" >> $L
ctx Pad001 "Set Tip"
echo "S12 after Set Tip Pad001: $(bstate peg)" >> $L
btn Std_Refresh R > /dev/null 2>&1; sleep 3
echo "S12 final: $(bstate peg)" >> $L
echo "S12 rep: $(report_text | grep -v executed | tail -c 300)" >> $L
shot $O/q3c-final.png
lab_save peg $O/q3c-fixed-gui.FCStd > /dev/null 2>&1
