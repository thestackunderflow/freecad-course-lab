F=cup; echo "== s3b (untick retry: the box itself, plain click) $(date -u +%T)" >> $L
cb() { Q "import FreeCADGui
from PySide import QtWidgets
print([(c.text(), c.isChecked()) for c in FreeCADGui.getMainWindow().findChildren(QtWidgets.QCheckBox) if c.isVisible() and 'inwards' in c.text()])"; }
p=$(ROW $F Thickness); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 5
c=$(taskpos any "Make thickness inwards"); echo "checkbox at $c: $(cb)" >> $L
x=$(( ${c% *} - 238 )); y=${c#* }
xdotool mousemove $x $y; sleep 0.6; xdotool click 1; sleep 3
echo "after plain click on the box ($x $y): $(cb) $(tstate $F)" >> $L
shot $O/q3-unticked-b.png
