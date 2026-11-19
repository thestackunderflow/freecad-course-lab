F=cup; echo "== s1 (Q1/Q2/Q6 trap on cup-box) $(date -u +%T)" >> $L
mkdir -p /tmp/fc13; cp $X/P/cup-box.FCStd /tmp/fc13/$F.FCStd
open_doc /tmp/fc13/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1; report_hide; sleep 2; rv_clear
shot $O/q1-box-iso.png
echo "notices at open: $(FQ "notices()")" >> $L
p=$(vp 0 0 50); echo "top face centre on screen $p" >> $L
xdotool mousemove $p; sleep 0.5; xdotool click 1; sleep 1.5
echo "selection: $(selnames)" >> $L
btn PartDesign_Thickness "Thickness"; sleep 5
echo "panel: $(FQ "task_texts()")" >> $L
echo "checkbox: $(Q "import FreeCADGui
from PySide import QtWidgets
print([(c.text(), c.isChecked()) for c in FreeCADGui.getMainWindow().findChildren(QtWidgets.QCheckBox) if c.isVisible()])")" >> $L
echo "state in panel: $(tstate $F)" >> $L
shot $O/q6-panel-open.png
