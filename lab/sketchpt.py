"""Lab instrument (lesson 2), never filmed as a step: where a sketch's line or corner is drawn on the screen right now,
so the take can click it the way a person would (the Sketcher moves and rescales lines as sizes are pinned).
Points are read from the sketch's own geometry, mapped through its placement into the 3D view, then to screen pixels.

    python3 -m lab.sketchpt DOC SKETCH GEO WHERE [DX DY]
      GEO   the line's index (0 = the first polyline line); -1 with WHERE "origin" for the sketch origin
      WHERE mid | start | end | origin | center (a circle's centre, lesson 4)
      DX DY a screen-pixel offset added to the result (where to drop a dimension beside a line)
    prints "x y" (display pixels)"""
import sys

sys.path.insert(0, '/lab')
from lab import fcrpc  # noqa: E402

CODE = """import FreeCAD, FreeCADGui
from PySide import QtCore, QtWidgets
sk = FreeCAD.getDocument({doc!r}).getObject({sk!r})
pl = sk.getGlobalPlacement()
geo, where = {geo!r}, {where!r}
if where == 'origin':
    p = FreeCAD.Vector(0, 0, 0)
elif where == 'center':
    p = sk.Geometry[geo].Center
else:
    g = sk.Geometry[geo]
    a, b = g.StartPoint, g.EndPoint
    p = {{'start': a, 'end': b, 'mid': (a + b) * 0.5}}[where]
q = pl.multVec(p)
v = FreeCADGui.ActiveDocument.ActiveView
vw = [w for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QWidget)
      if w.metaObject().className() == 'Gui::View3DInventorViewer' and w.isVisible()]
w = max(vw, key=lambda w: w.width() * w.height())
k = w.devicePixelRatioF()
gp = w.mapToGlobal(QtCore.QPoint(0, 0))
x, y = v.getPointOnViewport(q)
print('%d %d' % (round(gp.x() * k + x), round(gp.y() * k + v.getSize()[1] - y)))"""


def where(doc, sk, geo, at, dx=0, dy=0):
    x, y = (int(s) for s in fcrpc.run(CODE.format(doc=doc, sk=sk, geo=int(geo), where=at)).split())
    return x + int(dx), y + int(dy)


if __name__ == '__main__':
    a = sys.argv[1:]
    x, y = where(a[0], a[1], a[2], a[3], *(a[4:6] or []))
    print(f'{x} {y}')
