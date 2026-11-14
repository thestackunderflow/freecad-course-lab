"""fc8 lab queries run INSIDE FreeCAD through the add-on's socket (Q "exec(open('/lab/lab/fc8q.py').read()); f()"),
never filmed as a step. Positions are display pixels (device ratio applied)."""
import json
import FreeCAD
import FreeCADGui
from PySide import QtWidgets, QtCore

QtWidgets.QApplication.processEvents()
_mw = FreeCADGui.getMainWindow()


def _px(w, p=None):
    k = w.devicePixelRatioF()
    g = w.mapToGlobal(p if p is not None else w.rect().center())
    return [int(g.x() * k), int(g.y() * k)]


def toolbars(match=''):
    """visible toolbars: name, then each button's command, text and centre"""
    out = []
    for tb in _mw.findChildren(QtWidgets.QToolBar):
        if not tb.isVisible() or match not in tb.objectName():
            continue
        row = [tb.objectName()]
        for a in tb.actions():
            w = tb.widgetForAction(a)
            if w is None or not w.isVisible() or a.isSeparator():
                continue
            row.append([a.objectName() or a.data(), a.text().replace('&', ''), _px(w)])
        out.append(row)
    print(json.dumps(out))


def task_texts():
    """every visible label / button / check box / list row in the task panel (Combo view), with centres"""
    out = []
    for d in _mw.findChildren(QtWidgets.QWidget):
        if d.metaObject().className() == 'Gui::TaskView::TaskView' and d.isVisible():
            for w in d.findChildren(QtWidgets.QWidget):
                if not w.isVisible():
                    continue
                t = ''
                if isinstance(w, (QtWidgets.QLabel, QtWidgets.QAbstractButton)):
                    t = w.text()
                elif isinstance(w, QtWidgets.QComboBox):
                    t = 'combo:' + w.currentText()
                elif isinstance(w, (QtWidgets.QAbstractSpinBox, QtWidgets.QLineEdit)):
                    t = 'field:' + (w.text() if hasattr(w, 'text') else '')
                if t:
                    out.append([w.metaObject().className(), t[:60], _px(w)])
                if isinstance(w, QtWidgets.QTreeWidget):
                    it = QtWidgets.QTreeWidgetItemIterator(w)
                    while it.value():
                        i = it.value()
                        r = w.visualItemRect(i)
                        out.append(['row', i.text(0)[:60], _px(w.viewport(), r.center()) if r.isValid() else None])
                        it += 1
                if isinstance(w, QtWidgets.QListWidget):
                    for n in range(w.count()):
                        i = w.item(n)
                        out.append(['list', i.text()[:60], _px(w.viewport(), w.visualItemRect(i).center())])
    print(json.dumps(out))


def placements(doc):
    d = FreeCAD.getDocument(doc)
    print(json.dumps({o.Name: [o.Label, o.TypeId, [round(v, 4) for v in o.Placement.Base],
                               [round(v, 6) for v in o.Placement.Rotation.Q]]
                      for o in d.Objects if hasattr(o, 'Placement') and o.TypeId in
                      ('App::Link', 'PartDesign::Body', 'Assembly::AssemblyObject', 'Part::MultiCommon')}))


def objects(doc):
    d = FreeCAD.getDocument(doc)
    print(json.dumps([[o.Name, o.Label, o.TypeId] for o in d.Objects]))


def common_of(doc, a, b):
    """shared volume of two objects' shapes as placed now (a, b: object names)"""
    d = FreeCAD.getDocument(doc)
    s = d.getObject(a).Shape.common(d.getObject(b).Shape)
    print(json.dumps({'common_mm3': round(s.Volume, 4), 'solids': len(s.Solids)}))


def view_point(doc, *pts):
    v = FreeCADGui.getDocument(doc).activeView()
    k = _mw.devicePixelRatioF()
    out = []
    for i in range(0, len(pts), 3):
        p = v.getPointOnViewport(FreeCAD.Vector(pts[i], pts[i + 1], pts[i + 2]))
        gl = v.graphicsView() if hasattr(v, 'graphicsView') else None
        out.append([p[0], p[1]])
    print(json.dumps(out))


def report_tail(n=12):
    out = []
    for d in _mw.findChildren(QtWidgets.QDockWidget):
        if 'Report' in d.objectName():
            for t in d.findChildren(QtWidgets.QPlainTextEdit) + d.findChildren(QtWidgets.QTextEdit):
                out += t.toPlainText().splitlines()[-n:]
    print(json.dumps(out))


def prep(doc, iso=True):
    """a file saved headless: each body and its tip shown, other features hidden; hook orange, rail blue-grey; iso, fit"""
    d = FreeCAD.getDocument(doc)
    g = FreeCADGui.getDocument(doc)
    cols = {'Hook': (0.93, 0.55, 0.20), 'Rail': (0.55, 0.62, 0.72)}
    for b in [o for o in d.Objects if o.TypeId == 'PartDesign::Body']:
        for f in b.Group:
            if hasattr(g.getObject(f.Name), 'Visibility'):
                g.getObject(f.Name).Visibility = (f == b.Tip)
        g.getObject(b.Name).Visibility = True
        for k, c in cols.items():
            if k in b.Label:
                g.getObject(b.Name).ShapeAppearance = [FreeCAD.Material(DiffuseColor=c)]
    v = g.activeView()
    v.viewIsometric() if iso else None
    FreeCADGui.SendMsgToActiveView('ViewFit')
    print('prepped', doc)


def look(doc, view, cx, cy, cz, height):
    """not filmed: a standard view, then the orthographic camera centred on (cx, cy, cz) showing `height` mm"""
    v = FreeCADGui.getDocument(doc).activeView()
    v.setAnimationEnabled(False)
    getattr(v, 'view' + view)()
    cam = v.getCameraNode()
    d = cam.orientation.getValue().multVec(__import__('pivy').coin.SbVec3f(0, 0, -1))
    p = FreeCAD.Vector(cx, cy, cz) - FreeCAD.Vector(d[0], d[1], d[2]) * 200
    cam.position.setValue(p.x, p.y, p.z)
    if hasattr(cam, 'height'):
        cam.height.setValue(height)
    print('look', view, cx, cy, cz, height)
