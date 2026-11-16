"""fc9 lab queries run INSIDE FreeCAD through the add-on's socket, after fc8q.py (FQ execs both), never filmed as a
step. Positions are display pixels (device ratio applied)."""
import json
import FreeCAD
import FreeCADGui
from PySide import QtWidgets


def popup_pos(text):
    """centre of an open combo box popup's row whose text is `text` ("none" if no popup shows it)"""
    QtWidgets.QApplication.processEvents()
    for v in QtWidgets.QApplication.allWidgets():
        if isinstance(v, QtWidgets.QAbstractItemView) and v.isVisible() and 'ComboBox' in v.metaObject().className():
            m = v.model()
            for r in range(m.rowCount()):
                if m.index(r, 0).data() == text:
                    rect = v.visualRect(m.index(r, 0))
                    k = v.devicePixelRatioF()
                    g = v.viewport().mapToGlobal(rect.center())
                    print('%d %d' % (int(g.x() * k), int(g.y() * k)))
                    return
    print('none')


def combo_pos(current):
    """centre of the visible combo box now showing `current`"""
    for c in _mw.findChildren(QtWidgets.QComboBox):
        if c.isVisible() and c.currentText() == current:
            print(' '.join(map(str, _px(c))))
            return
    print('none')


def field_pos(label):
    """centre of the spin box on the task-panel row whose label is `label` (Length, Occurrences)"""
    for lab in _mw.findChildren(QtWidgets.QLabel):
        if lab.isVisible() and lab.text() == label:
            g = lab.mapToGlobal(lab.rect().center())
            best = None
            for w in _mw.findChildren(QtWidgets.QAbstractSpinBox):
                if not w.isVisible():
                    continue
                c = w.mapToGlobal(w.rect().center())
                if abs(c.y() - g.y()) < 12 and (best is None or c.x() < best[0]):
                    best = (c.x(), w)
            if best:
                print(' '.join(map(str, _px(best[1]))))
                return
    print('none')


def notices():
    """the notification area's rows and the Report view's last lines (where a pattern warning shows)"""
    out = []
    for w in QtWidgets.QApplication.allWidgets():
        if w.isVisible() and isinstance(w, QtWidgets.QTreeWidget) and w.headerItem() and \
                w.headerItem().text(2) == 'Message':
            it = QtWidgets.QTreeWidgetItemIterator(w)
            while it.value():
                i = it.value()
                out.append([i.text(1), i.text(2)])
                it += 1
    print(json.dumps(out))


def pattern_state(doc):
    d = FreeCAD.getDocument(doc)
    out = []
    for o in d.Objects:
        if o.TypeId == 'PartDesign::LinearPattern':
            out.append({'name': o.Name, 'mode': o.Mode, 'length': round(o.Length.Value, 4), 'occ': o.Occurrences,
                        'dir': str(o.Direction)[-40:], 'solids': len(o.Shape.Solids), 'state': o.State,
                        'expr': [list(e) for e in o.ExpressionEngine]})
    print(json.dumps(out))


def expr_ok():
    """centre of the Expression Editor's OK button ("none" if it is not open)"""
    for w in QtWidgets.QApplication.topLevelWidgets():
        if w.isVisible() and 'Expression' in w.metaObject().className() + w.windowTitle():
            for b in w.findChildren(QtWidgets.QAbstractButton):
                if b.isVisible() and b.text().replace('&', '') == 'OK':
                    print(' '.join(map(str, _px(b))))
                    return
    print('none')
