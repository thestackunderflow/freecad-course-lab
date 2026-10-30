"""Lab instrument (lesson 4), never filmed as a step: where a toolbar button is drawn on screen, found by the FreeCAD
command it runs (for example PartDesign_Hole, PartDesign_Fillet, PartDesign_CompSketches), so the take clicks it the
way a person would, wherever the toolbars wrapped on this screen size.

    python3 -m lab.button COMMAND        prints "x y" (display pixels) of the visible button, or "none\""""
import sys

sys.path.insert(0, '/lab')
from lab import fcrpc  # noqa: E402

CODE = """import FreeCADGui
from PySide import QtWidgets
QtWidgets.QApplication.processEvents()
mw = FreeCADGui.getMainWindow()
out = 'none'
for tb in mw.findChildren(QtWidgets.QToolBar):
    if out != 'none' or not tb.isVisible():
        continue
    for a in tb.actions():
        if a.objectName() == {cmd!r} or a.data() == {cmd!r}:
            w = tb.widgetForAction(a)
            if w is not None and w.isVisible():
                k = w.devicePixelRatioF()
                g = w.mapToGlobal(w.rect().center())
                out = '%d %d' % (int(g.x() * k), int(g.y() * k))
                break
print(out)"""


def where(cmd):
    return fcrpc.run(CODE.format(cmd=cmd))


if __name__ == '__main__':
    print(where(sys.argv[1]))
