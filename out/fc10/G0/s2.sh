p=$(WG text "Degrees"); echo "q1 link label at $p" >> $L
Q "import FreeCADGui
from PySide import QtWidgets
for l in FreeCADGui.getMainWindow().findChildren(QtWidgets.QLabel):
    if l.isVisible() and 'Degrees' in l.text(): print(repr(l.text()), l.styleSheet()[:100], l.palette().color(l.foregroundRole()).name())" >> $L
xdotool mousemove $(( ${p% *} - 30 )) ${p#* }; sleep 0.5; xdotool click 1; sleep 2
echo "q1 selection after link click: $(selnames)" >> $L
Q "import FreeCADGui; FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" > /dev/null; sleep 1; xdotool mousemove 1500 300; sleep 1
shot $O/q1-link-clicked.png
