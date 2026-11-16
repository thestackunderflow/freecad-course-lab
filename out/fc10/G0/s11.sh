xdotool key Escape; sleep 0.5
read -r ZX ZY < <(B text Close); [ "$ZX" != none ] && { xdotool mousemove $ZX $ZY; sleep 0.5; xdotool click 1; sleep 2; }
Q "import FreeCAD
for n in list(FreeCAD.listDocuments()): FreeCAD.closeDocument(n)
print(1)" > /dev/null; sleep 1
cp $X/P/hook-pinned.FCStd /tmp/fc10/hook.FCStd; open_doc /tmp/fc10/hook.FCStd > /dev/null; sleep 2
read -r SKX SKY < <(row_open hook HookSketch); xdotool mousemove $SKX $SKY; sleep 0.5; xdotool click --repeat 2 --delay 120 1; sleep 4
FQ "look('hook', 'Front', 12, 0, 30, 90)" > /dev/null; sleep 1
Q "import FreeCADGui
from PySide import QtWidgets
for l in FreeCADGui.getMainWindow().findChildren(QtWidgets.QLabel):
    if l.isVisible() and 'constrained' in l.text(): print('q1 pinned label', repr(l.text()), l.styleSheet()[:120])" >> $L
read -r MX MY < <(SP hook HookSketch 7 mid)
xdotool mousemove $MX $MY; sleep 0.8; xdotool mousedown 1; sleep 0.2
for i in $(seq 1 15); do xdotool mousemove $((MX + 4 * i)) $((MY - 3 * i)); sleep 0.04; done
sleep 0.3; xdotool mouseup 1; sleep 1.5
shot $O/q3-pinned-after-drag.png
read -r ZX ZY < <(B text Close); xdotool mousemove $ZX $ZY; sleep 0.5; xdotool click 1; sleep 3
echo "q3 pinned live after drag + close: $(live hook)" >> $L
