ctx() { uiwatch 20; local p m; p=$(ROW peg $1); xdotool mousemove ${p% *} ${p#* }; sleep 0.3; xdotool click 1; sleep 0.4; xdotool click 3; sleep 1; m=$(ui menu "$2"); xdotool mousemove ${m% *} ${m#* }; sleep 0.4; xdotool click 1; sleep 2.5; echo "S14 ui after $1 $2: $(ui dump | cut -c1-300)" >> $L; }
p=$(B PartDesign_Thickness); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click 1; sleep 4
p=$(FQ "field_pos('Thickness')"); xdotool mousemove $(( ${p% *} - 40 )) ${p#* }; xdotool click 1; xdotool key ctrl+a; sleep 0.3
xdotool type --delay 150 "="; sleep 1.5; xdotool type --delay 100 "Params.wall"; sleep 1; xdotool key Return; sleep 1.5
e=$(FQ "expr_ok()"); xdotool mousemove ${e% *} ${e#* }; xdotool click 1; sleep 2
c=$(taskpos any "Make thickness inwards"); xdotool mousemove $(( ${c% *} - 238 )) ${c#* }; sleep 0.4; xdotool click 1; sleep 3
echo "S14 panel before OK: $(FQ "task_texts()" | grep -o '"Make thickness inwards"' | head -1) $(Q "import FreeCADGui
from PySide import QtWidgets
print([c.isChecked() for c in FreeCADGui.getMainWindow().findChildren(QtWidgets.QCheckBox) if c.isVisible() and 'inwards' in c.text()])")" >> $L
shot $O/q3c-panel.png
o=$(taskpos any OK); xdotool mousemove ${o% *} ${o#* }; sleep 0.4; xdotool click 1; sleep 3
echo "S14 after new Thickness: $(bstate peg)" >> $L
ctx Pad001 "Set Tip"
echo "S14 after Set Tip Pad001: $(bstate peg)" >> $L
btn Std_Refresh R > /dev/null 2>&1; sleep 3
echo "S14 final: $(bstate peg)" >> $L
echo "S14 rep: $(report_text | grep -v executed | tail -c 300)" >> $L
shot $O/q3c-final.png
lab_save peg $O/q3c-fixed-gui.FCStd > /dev/null 2>&1
