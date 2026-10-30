"""Lab instrument (lesson 4), never filmed as a step: where something a person would click is drawn on screen right now,
so the take clicks it the way a person would, wherever this screen size put it.

    python3 -m lab.button COMMAND            a toolbar button, by the FreeCAD command it runs (PartDesign_Hole,
                                             PartDesign_Fillet, PartDesign_CompSketches ...)
    python3 -m lab.button menu TITLE         a menu-bar title (Windows, File ...)
    python3 -m lab.button tab TEXT           a document tab under the 3D view, by the start of its text
    python3 -m lab.button console            the Python console's input line (its bottom row)
    python3 -m lab.button cell ROW COL       a cell of the visible spreadsheet (0-based: B5 = 4 1)
    python3 -m lab.button view               an empty spot (bottom-left corner) of the biggest visible 3D view
prints "x y" (display pixels), or "none". (An open menu blocks the add-on's socket until it closes, so menu items are
clicked at fixed offsets in the takes.)"""
import sys

sys.path.insert(0, '/lab')
from lab import fcrpc  # noqa: E402

HEAD = """import FreeCADGui
from PySide import QtWidgets
QtWidgets.QApplication.processEvents()
mw = FreeCADGui.getMainWindow()
def px(w, p):
    k = w.devicePixelRatioF()
    g = w.mapToGlobal(p)
    return '%d %d' % (int(g.x() * k), int(g.y() * k))
out = 'none'
"""

CODE = HEAD + """for tb in mw.findChildren(QtWidgets.QToolBar):
    if out != 'none' or not tb.isVisible():
        continue
    for a in tb.actions():
        if a.objectName() == {cmd!r} or a.data() == {cmd!r}:
            w = tb.widgetForAction(a)
            if w is not None and w.isVisible():
                out = px(w, w.rect().center())
                break
print(out)"""

MENU = HEAD + """bar = mw.menuBar()
for a in bar.actions():
    if a.text().replace('&', '') == {title!r}:
        out = px(bar, bar.actionGeometry(a).center())
print(out)"""


TAB = HEAD + """for bar in mw.findChildren(QtWidgets.QTabBar):
    if out != 'none' or not bar.isVisible():
        continue
    for i in range(bar.count()):
        if bar.tabText(i).startswith({text!r}):
            out = px(bar, bar.tabRect(i).center())
            break
print(out)"""

CONSOLE = HEAD + """for w in mw.findChildren(QtWidgets.QDockWidget):
    if w.objectName() == 'Python console' and w.isVisible():
        c = w.widget()
        r = c.rect()
        out = px(c, r.center() + r.center().__class__(0, r.height() // 2 - 30))
print(out)"""


CELL = HEAD + """import shiboken6
for w in QtWidgets.QApplication.allWidgets():
    if out != 'none' or w.metaObject().className() != 'SpreadsheetGui::SheetTableView' or not w.isVisible():
        continue
    v = shiboken6.wrapInstance(shiboken6.getCppPointer(w)[0], QtWidgets.QTableView)
    r = v.visualRect(v.model().index({row}, {col}))
    if r.height() > 0:
        out = px(v.viewport(), r.center())
print(out)"""


VIEW = HEAD + """vw = [w for w in mw.findChildren(QtWidgets.QWidget)
      if w.metaObject().className() == 'Gui::View3DInventorViewer' and w.isVisible()]
if vw:
    w = max(vw, key=lambda w: w.width() * w.height())
    out = px(w, w.rect().topLeft() + w.rect().topLeft().__class__(90, w.height() - 90))
print(out)"""


def where(cmd):
    return fcrpc.run(CODE.format(cmd=cmd))


def main(a):
    if a[0] == 'menu':
        return fcrpc.run(MENU.format(title=a[1]))
    if a[0] == 'tab':
        return fcrpc.run(TAB.format(text=a[1]))
    if a[0] == 'cell':
        return fcrpc.run(CELL.format(row=int(a[1]), col=int(a[2])))
    if a[0] == 'view':
        return fcrpc.run(VIEW)
    if a[0] == 'console':
        return fcrpc.run(CONSOLE)
    return where(a[0])


if __name__ == '__main__':
    print(main(sys.argv[1:]))
