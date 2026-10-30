"""Lab instrument (lesson 3), never filmed as a step: where a sketch's dimension label is drawn on screen, so the take
can double-click a size like a person would. For DistanceX / DistanceY / Distance constraints between two points (or
on one line), the label sits at the midpoint, moved LabelDistance along the normal and LabelPosition along the line
(FreeCAD's own layout for linear dimensions); the point is mapped to screen pixels with the 3D view's
getPointOnViewport (as lab.fcrpc vp).

    python3 -m lab.dimpt DOC SKETCH INDEX [INDEX ...]     prints "x y" per constraint index (display pixels)
    python3 -m lab.dimpt DOC SKETCH list                   prints each size: index, type, value"""
import sys

sys.path.insert(0, '/lab')
from lab import fcrpc  # noqa: E402

CODE = """import FreeCAD, FreeCADGui
from PySide import QtWidgets
sk = FreeCAD.getDocument({doc!r}).getObject({sk!r})
def pt(geo, pos):
    if geo == -1:
        return FreeCAD.Vector(0, 0, 0)
    g = sk.Geometry[geo]
    return {{1: g.StartPoint, 2: g.EndPoint, 3: getattr(g, 'Center', g.StartPoint)}}.get(pos, (g.StartPoint + g.EndPoint) * 0.5)
v = FreeCADGui.ActiveDocument.ActiveView
vw = [w for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QWidget)
      if w.metaObject().className() == 'Gui::View3DInventorViewer' and w.isVisible()]
w = max(vw, key=lambda w: w.width() * w.height())
k = w.devicePixelRatioF()
g0 = w.mapToGlobal(w.rect().topLeft())
h = v.getSize()[1]
pl = sk.getGlobalPlacement()
out = []
for i in {idx!r}:
    c = sk.Constraints[i]
    if c.Second == -2000 or c.Second is None:
        a, b = pt(c.First, 1), pt(c.First, 2)
    else:
        a, b = pt(c.First, c.FirstPos), pt(c.Second, c.SecondPos)
    if c.Type == 'DistanceX':
        b = FreeCAD.Vector(b.x, a.y, 0)
    elif c.Type == 'DistanceY':
        b = FreeCAD.Vector(a.x, b.y, 0)
    d = b - a
    n = d.Length or 1.0
    u = FreeCAD.Vector(d.x / n, d.y / n, 0)
    norm = FreeCAD.Vector(-u.y, u.x, 0)
    m = (a + b) * 0.5 + norm * c.LabelDistance + u * c.LabelPosition
    x, y = v.getPointOnViewport(pl.multVec(m))
    out.append('%d %d' % (round(g0.x() * k + x), round(g0.y() * k + h - y)))
print(chr(10).join(out))"""

LIST = """import FreeCAD
sk = FreeCAD.getDocument({doc!r}).getObject({sk!r})
for i, c in enumerate(sk.Constraints):
    if c.Type in ('Distance', 'DistanceX', 'DistanceY'):
        print(i, c.Type, round(c.Value, 3))"""


if __name__ == '__main__':
    doc, sk = sys.argv[1], sys.argv[2]
    if sys.argv[3] == 'list':
        print(fcrpc.run(LIST.format(doc=doc, sk=sk)))
    else:
        print(fcrpc.run(CODE.format(doc=doc, sk=sk, idx=[int(a) for a in sys.argv[3:]])))
