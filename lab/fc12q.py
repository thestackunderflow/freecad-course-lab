"""fc12 lab queries run INSIDE FreeCAD (after fc8q.py + fc9q.py; FQ12 execs all three), never filmed as a step."""
from PySide import QtWidgets as _QW


def prop_row(name):
    """centre of the Property view row whose first column reads `name` ("none" if not shown)"""
    for v in _mw.findChildren(_QW.QTreeView):
        if not v.isVisible() or 'PropertyEditor' not in v.metaObject().className():
            continue
        m = v.model()

        def walk(parent):
            for r in range(m.rowCount(parent)):
                i = m.index(r, 0, parent)
                if i.data() == name:
                    return i
                f = walk(i)
                if f is not None:
                    return f
            return None
        i = walk(v.rootIndex())
        if i is not None:
            v.scrollTo(i)
            rect = v.visualRect(i)
            k = v.devicePixelRatioF()
            g = v.viewport().mapToGlobal(rect.center())
            print('%d %d' % (int(g.x() * k), int(g.y() * k)))
            return
    print('none')


def tooltip_text():
    t = _QW.QToolTip.text() if _QW.QToolTip.isVisible() else ''
    print(repr(t))
