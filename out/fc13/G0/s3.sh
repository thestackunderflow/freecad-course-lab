F=cup; echo "== s3 (Q3 fix in the GUI, Q6 Reversed hover) $(date -u +%T)" >> $L
Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null
p=$(row_open $F Thickness); echo "row $p" >> $L; xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 5
echo "panel: $(FQ "task_texts()" | grep -o '"Q[A-Za-z:]*", "[^"]*"' | tr '\n' ' ')" >> $L
c=$(taskpos any "Make thickness inwards"); echo "checkbox at $c" >> $L
at "$c" "untick"; sleep 4
echo "checkbox: $(Q "import FreeCADGui
from PySide import QtWidgets
print([(c.text(), c.isChecked()) for c in FreeCADGui.getMainWindow().findChildren(QtWidgets.QCheckBox) if c.isVisible() and 'inwards' in c.text()])")" >> $L
echo "state before OK: $(tstate $F)" >> $L
shot $O/q3-unticked.png
at "$(taskpos any OK)" "OK"; sleep 5
echo "after OK: $(tstate $F)" >> $L
echo "dialogs: $(dialogs) notices: $(FQ "notices()")" >> $L
FQ "prep('$F')" >> $L 2>&1; sleep 1; shot $O/q3-fixed-iso.png
Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewTop(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L; sleep 2
shot $O/q3-fixed-top.png
lab_save $F $O/q3-fixed-gui.FCStd >> $L 2>&1
check13 $O/q3-fixed-gui.FCStd $O/q3-fixed-gui.check.json >> $L
p=$(ROW $F Thickness); at "$p" "tree: Thickness"; sleep 2
r=$(FQ13 "prop_row('Reversed')"); echo "Reversed row $r" >> $L
[ "$r" != none ] && { xdotool mousemove $(( ${r% *} - 5 )) $(( ${r#* } + 3 )); sleep 0.3; xdotool mousemove ${r% *} ${r#* }; sleep 3; echo "tooltip: $(FQ13 "tooltip_text()")" >> $L; shot $O/q6-reversed-hover.png; }
echo "doc string: $(Q "import FreeCAD; o=FreeCAD.getDocument('$F').getObject('Thickness'); print(repr(o.getDocumentationOfProperty('Reversed')))")" >> $L
