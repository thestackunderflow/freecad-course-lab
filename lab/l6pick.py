"""Lab instrument (lesson 6), never filmed as a step: where the things a person clicks for Tools > Measure are drawn on
screen right now, worked out from the part's live shape (whatever a run named it or wherever it moved it), so the take
clicks them the way a person would.

    python3 -m lab.l6pick opening        "x y x y": a spot on the back plate's inner face (between the holes' heights,
                                         a quarter of the width in), then the middle of the lip's inner top edge
    python3 -m lab.l6pick hole           "x y": the top of the upper hole's circle on the plate's inner face
    python3 -m lab.l6pick round          "x y": the middle of the lip's round edge's arc on the front side face
    python3 -m lab.l6pick combo          "x y": the Measurement panel's Mode list
    python3 -m lab.l6pick hit WHAT       "yes ..." when the thing under the cursor (preselected) is WHAT (plate, lipedge,
                                         hole, round), worked out from the part's live shape; else "no ..."
    python3 -m lab.l6pick sel            the current selection (object, sub-elements)
    python3 -m lab.l6pick close          "x y": the Measurement panel's Close button
    python3 -m lab.l6pick result         the text in the Measurement panel's Result field ("30.00 mm"), or "none"
    python3 -m lab.l6pick resultbox      "x y w h" of the Result field (display pixels), for the zoom
The part = the last PartDesign Body with a solid in the active document (else the last root solid)."""
import sys

sys.path.insert(0, '/lab')
from lab import fcrpc  # noqa: E402

PART = """import FreeCAD, FreeCADGui
d = FreeCAD.ActiveDocument
bs = [o for o in d.Objects if o.TypeId == 'PartDesign::Body' and not o.Shape.isNull() and o.Shape.Solids]
if not bs:
    bs = [o for o in d.Objects if getattr(o, 'Shape', None) is not None and not o.Shape.isNull() and o.Shape.Solids]
b = bs[-1].Shape.BoundBox
x0, x1, y0, y1, z0, z1 = b.XMin, b.XMax, b.YMin, b.YMax, b.ZMin, b.ZMax
W = y1 - y0
"""

POINTS = {
    'opening': '[(x0 + 5, y0 + 0.25 * W, z0 + 30), (x1 - 5, y0 + 0.5 * W, z0 + 10)]',
    'hole': '[(x0 + 5, y0 + 0.5 * W - 1.41421356, z0 + 45 + 1.41421356)]',
    'round': '[(x1 - 2 + 1.41421356, y0, z0 + 8 + 1.41421356)]',
}

PANEL = """import FreeCADGui
from PySide import QtWidgets
QtWidgets.QApplication.processEvents()
mw = FreeCADGui.getMainWindow()
out = 'none'
"""

COMBO = PANEL + """for cb in mw.findChildren(QtWidgets.QComboBox):
    if cb.isVisible() and cb.findText('Distance') >= 0 and cb.findText('Radius') >= 0:
        k = cb.devicePixelRatioF(); g = cb.mapToGlobal(cb.rect().center())
        out = '%d %d' % (int(g.x() * k), int(g.y() * k))
print(out)"""

CLOSE = PANEL + """for b in mw.findChildren(QtWidgets.QPushButton):
    if b.isVisible() and b.text().replace('&', '') == 'Close':
        k = b.devicePixelRatioF(); g = b.mapToGlobal(b.rect().center())
        out = '%d %d' % (int(g.x() * k), int(g.y() * k))
print(out)"""

RESULT = PANEL + """labs = [w for w in mw.findChildren(QtWidgets.QLabel) if w.isVisible() and w.text().startswith('Result')]
if labs:
    ly = labs[0].mapToGlobal(labs[0].rect().center()).y()
    eds = [e for e in mw.findChildren(QtWidgets.QLineEdit) if e.isVisible()
           and abs(e.mapToGlobal(e.rect().center()).y() - ly) < 12]
    lx = labs[0].mapToGlobal(labs[0].rect().center()).x()
    eds = sorted([e for e in eds if e.mapToGlobal(e.rect().center()).x() > lx],
                 key=lambda e: e.mapToGlobal(e.rect().topLeft()).x())
    if eds:
        e = eds[0]
        if {box}:
            k = e.devicePixelRatioF(); g = e.mapToGlobal(e.rect().topLeft())
            out = '%d %d %d %d' % (int(g.x() * k), int(g.y() * k), int(e.width() * k), int(e.height() * k))
        else:
            out = e.text()
print(out)"""


HIT = PART + """import Part
pre = FreeCADGui.Selection.getPreselection()
ok = 'no'
names = list(pre.SubElementNames) if pre and pre.Object else []
sh = bs[-1].Shape
for n in names:
    try:
        sub = sh.getElement(n.split('.')[-1])
    except Exception:
        continue
    c = sub.CenterOfMass
    want = {what!r}
    if want == 'plate' and n.split('.')[-1].startswith('Face') and abs(c.x - (x0 + 5)) < 0.01 and sub.Area > 200:
        ok = 'yes'
    if want == 'lipedge' and n.split('.')[-1].startswith('Edge') and abs(c.x - (x1 - 5)) < 0.01 and abs(c.z - (z0 + 10)) < 0.01:
        ok = 'yes'
    if want in ('hole', 'round') and n.split('.')[-1].startswith('Edge') and hasattr(sub.Curve, 'Radius') and abs(sub.Curve.Radius - 2) < 0.01:
        ok = 'yes' if (want == 'hole') == (abs(c.x - (x0 + 5)) < 0.01) else 'no'
print(ok + ' ' + ','.join(names))"""


def pts_code(name):
    vp = fcrpc.VP.split('out = []')[0]
    return (PART + 'PTS = ' + POINTS[name] + '\n' + vp.split('import FreeCAD, FreeCADGui', 1)[1] +
            "out = []\nfor p in PTS:\n    x, y = v.getPointOnViewport(FreeCAD.Vector(*p))\n"
            "    out.append('%d %d' % (round(g.x() * k + x), round(g.y() * k + h - y)))\nprint(' '.join(out))")


def main(a):
    if a[0] in POINTS:
        return fcrpc.run('import FreeCAD, FreeCADGui\n' + pts_code(a[0]))
    if a[0] == 'hit':
        return fcrpc.run(HIT.format(what=a[1]))
    if a[0] == 'sel':
        return fcrpc.run('import FreeCADGui' + chr(10) + 'print([(x.ObjectName, x.SubElementNames) for x in FreeCADGui.Selection.getSelectionEx()])')
    if a[0] == 'close':
        return fcrpc.run(CLOSE)
    if a[0] == 'combo':
        return fcrpc.run(COMBO)
    if a[0] == 'result':
        return fcrpc.run(RESULT.format(box=False))
    if a[0] == 'resultbox':
        return fcrpc.run(RESULT.format(box=True))
    raise SystemExit(__doc__)


if __name__ == '__main__':
    print(main(sys.argv[1:]))
