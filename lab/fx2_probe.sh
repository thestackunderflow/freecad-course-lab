#!/bin/bash
# fx2 probe (not a take): the Export dialog's type list and its positions.
set -u
. /lab/lab/common.sh
O=/lab/out/scratch/fx2probe; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
sl_display $W $H
fc_start "$O/app.log" 1.8; sleep 8
python3 - > "$O/setup-rpc.txt" 2>&1 <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCADGui
from PySide import QtCore, QtWidgets
mw = FreeCADGui.getMainWindow()
for w in mw.findChildren(QtWidgets.QMdiArea)[0].subWindowList():
    if w.windowTitle().startswith('Start'):
        w.close()
for w in mw.findChildren(QtWidgets.QDockWidget):
    if w.objectName() in ('Python console',):
        w.show()
        mw.resizeDocks([w], [190], QtCore.Qt.Vertical)
        w.widget().clear()
print(1)"""))
PY
w=$(xdotool search --name "FreeCAD" | head -1); wmctrl -i -r "$w" -b add,maximized_vert,maximized_horz; sleep 2
python3 - >> "$O/setup-rpc.txt" 2>&1 <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCAD as App, Part, FreeCADGui as Gui
doc = App.newDocument("washer")
obj = doc.addObject("Part::Feature", "washer")
obj.Shape = Part.makeCylinder(2.5, 0.3).cut(Part.makeCylinder(1.1, 0.3))
doc.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.Selection.addSelection(obj)
print(obj.Shape.Volume)"""))
PY
sl_shot "$O/a-washer.png"
xdotool mousemove 1500 700
sl_click 45 36 "File"; sl_nap 1; sl_glide 105 554 15; sl_nap 0.5; sl_shot "$O/b-menu.png"
sl_click 105 554 "Export"; sl_nap 3; sl_shot "$O/c-dialog.png"
sl_click 1404 1225 "type list"; sl_nap 2.5; sl_shot "$O/d-types.png"
fc_quit
