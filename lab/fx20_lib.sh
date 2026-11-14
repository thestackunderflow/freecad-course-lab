# fx20 helpers on top of common.sh + fx19_lib.sh (FreeCAD 1.1.4, Qt scale 1.8, 2880x1800).
#   . /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh
X=/lab/out/fx20

WG() {   # WG KIND ARG: centre "x y" of a visible widget: KIND class (className contains ARG) | text (button/label text
         # contains ARG) | link (a label whose text contains ARG: a point inside its link part). "none" if not found.
  Q "import FreeCADGui
from PySide import QtWidgets, QtGui, QtCore
import re
kind, arg = '$1', '''$2'''
def px(w, p):
    k = w.devicePixelRatioF(); g = w.mapToGlobal(p); return '%d %d' % (int(g.x() * k), int(g.y() * k))
out = 'none'
for w in QtWidgets.QApplication.allWidgets():
    if not w.isVisible() or out != 'none':
        continue
    c = w.metaObject().className()
    if kind == 'class' and arg in c:
        out = px(w, w.rect().center())
    elif kind == 'text' and isinstance(w, (QtWidgets.QAbstractButton, QtWidgets.QLabel)) and w.text() and arg in w.text().replace('&', ''):
        out = px(w, w.rect().center())
    elif kind == 'link' and isinstance(w, QtWidgets.QLabel) and arg in w.text() and '<a' in w.text():
        t = w.text(); pre = re.sub('<[^>]+>', '', t[:t.index('<a')])
        link = re.sub('<[^>]+>', '', t[t.index('<a'):])
        fm = QtGui.QFontMetrics(w.font())
        x = fm.horizontalAdvance(pre) + min(fm.horizontalAdvance(link) // 2, 40)
        out = px(w, QtCore.QPoint(x, w.height() // 2))
print(out)"
}

sk_state() {   # sk_state DOC: the sketch's numbers a person cannot see (constraint count, arm-top length, solver)
  Q "import FreeCAD
s = FreeCAD.getDocument('$1').getObject('Sketch')
g = s.Geometry[4]
print('constraints', len(s.Constraints), 'arm-top length', round(g.length(), 4), 'solve', s.solve(), 'DoF', s.DoF,
      'conflicting', list(s.ConflictingConstraints), 'redundant', list(s.RedundantConstraints),
      'last', [(c.Type, c.Value, c.Driving) for c in s.Constraints][-1])"
}

solver_text() {   # every visible label in the task panel (Solver messages included); call only with no modal box up
  Q "import FreeCADGui
from PySide import QtWidgets
out = []
for d in FreeCADGui.getMainWindow().findChildren(QtWidgets.QWidget):
    if d.metaObject().className() == 'Gui::TaskView::TaskView' and d.isVisible():
        out += [l.text() for l in d.findChildren(QtWidgets.QLabel) if l.isVisible() and l.text()]
print(out)"
}
