# fc11 helpers (FreeCAD course lesson 11, reference constraints) on top of common.sh + fx19_lib.sh + fx20_lib.sh
# + fc9_lib.sh + fc10_lib.sh.
#   . /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh
X=/lab/out/fc11
check11() {    # check11 FCSTD OUT.json [H]: lab/fc11parts.py check (or resize to H), headless, its own process
  if [ -n "${3:-}" ]; then
    FC11_DOC=$1 FC11_OUT=$2 FC11_MODE=resize FC11_H=$3 timeout 180 /opt/freecad/AppRun freecadcmd /lab/lab/fc11parts.py 2>&1 | tr '\r\t' '\n\n' | grep '^FC11' | tail -1
  else
    FC11_DOC=$1 FC11_OUT=$2 FC11_MODE=check timeout 180 /opt/freecad/AppRun freecadcmd /lab/lab/fc11parts.py 2>&1 | tr '\r\t' '\n\n' | grep '^FC11' | tail -1
  fi
}
live11() {     # live11 DOC: the numbers a person cannot see (not filmed): solver lists, top, inner size, tree states
  Q "import FreeCAD, json
d = FreeCAD.getDocument('$1'); sk = d.getObject('HookSketch'); bb = d.getObject('Body').Shape.BoundBox
inn = [(i, c.Type, round(c.Value, 4), c.Driving) for i, c in enumerate(sk.Constraints) if c.First == 5 and c.Type in ('Distance', 'DistanceY')]
print(json.dumps({'redundant': list(sk.RedundantConstraints), 'conflicting': list(sk.ConflictingConstraints), 'dof': sk.DoF,
  'zmax': round(bb.ZMax, 4), 'xmax': round(bb.XMax, 4), 'inner': inn, 'len5': round(sk.Geometry[5].length(), 4),
  'states': {o.Name: list(o.State) for o in d.Objects if o.TypeId.startswith(('Sketcher::', 'PartDesign::'))},
  'sheet': d.getObject('Params').get('plate_height')}))"
}
report_text() {   # the Report view's text (all of it, last 1500 chars)
  Q "import FreeCADGui
from PySide import QtWidgets
t = ''
for d in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
    if 'Report' in d.objectName():
        for w in d.findChildren(QtWidgets.QPlainTextEdit) + d.findChildren(QtWidgets.QTextEdit):
            t += w.toPlainText()
print(repr(t[-1500:]))"
}
dialogs() {    # visible top-level dialogs: title, labels, check boxes, buttons
  Q "from PySide import QtWidgets
out = []
for w in QtWidgets.QApplication.topLevelWidgets():
    if w.isVisible() and isinstance(w, QtWidgets.QDialog):
        out.append([w.windowTitle(), [l.text() for l in w.findChildren(QtWidgets.QLabel) if l.isVisible() and l.text()],
          [(c.text(), c.isChecked()) for c in w.findChildren(QtWidgets.QCheckBox) if c.isVisible()],
          [b.text() for b in w.findChildren(QtWidgets.QPushButton) if b.isVisible()]])
print(out)"
}
treestate() {  # tree rows' text + icon state as a person sees it is filmed; here the objects' State lists
  Q "import FreeCAD, json
d = FreeCAD.getDocument('$1'); print(json.dumps({o.Name: list(o.State) for o in d.Objects}))"
}
