"""Lab instrument, never filmed as a step: talk to the FreeCAD add-on's own XML-RPC socket (127.0.0.1:9875) to save a
copy of a document for measuring, or to find where a tree row is drawn so the script can click it like a person would.
(Each request briefly shows "MCP: processing…" in FreeCAD's status bar; the takes log a "lab query" event around it.)

    python3 -m lab.fcrpc save DOC PATH          save a copy (the open document is not renamed)
    python3 -m lab.fcrpc row DOC OBJ            prints "x y" of the object's row in the Model tree (screen pixels)
    python3 -m lab.fcrpc docs                   prints the open documents and their objects as JSON
    python3 -m lab.fcrpc arrow DOC OBJ          prints "x y" of the expand arrow of the first closed row above OBJ,
                                                "open" if OBJ's row is showing (the take clicks it, as a person)
    python3 -m lab.fcrpc vp X Y Z [X Y Z ...]   prints "x y" screen pixels of each global point in the 3D view
                                                (lesson 2: where a sketch corner or line is drawn, to click it)
    python3 -m lab.fcrpc cell DOC SHEET CELL    prints a spreadsheet cell's value (lesson 3; CELL may be an alias)
    python3 -m lab.fcrpc ping

Every query is sent wrapped in guard(): an error inside FreeCAD (lesson 2: "Internal C++ object (QTreeWidgetItem)
already deleted" while the Model tree was being rebuilt) is caught there and printed as a LABERR line, so nothing
reaches FreeCAD's console as an error and no error shows on the filmed screen. The client retries a LABERR answer
(the tree settles in a moment) and raises on its own side after three tries."""
import json
import sys
import time
import xmlrpc.client

URL = 'http://127.0.0.1:9875'
LABERR = 'LABERR'
TRIES = 4
RETRY_WAIT = 1.0


def guard(code):
    """The query inside try/except, so it can never raise inside FreeCAD."""
    nl = chr(10)
    body = nl.join('    ' + ln if ln.strip() else ln for ln in code.split(nl))
    return ('try:' + nl + body + nl + 'except BaseException as _lab_e:' + nl +
            '    print(%r + " " + type(_lab_e).__name__ + ": " + str(_lab_e))' % LABERR + nl)


def _exec(code):
    r = xmlrpc.client.ServerProxy(URL, allow_none=True).execute_code(code)
    if not r.get('success'):
        raise RuntimeError(r)
    return r['message'].split('Output: ', 1)[-1].strip()


def run(code):
    out = ''
    for i in range(TRIES):
        out = _exec(guard(code))
        if not out.startswith(LABERR):
            return out
        time.sleep(RETRY_WAIT)
    raise RuntimeError('lab query failed %d times (inside FreeCAD it was caught): %s' % (TRIES, out))


SAVE = """import FreeCAD
FreeCAD.getDocument({doc!r}).saveCopy({path!r})
print('saved')"""

DOCS = """import FreeCAD, json
print(json.dumps({{d.Name: {{'label': d.Label, 'objects': [[o.Name, o.Label] for o in d.Objects]}}
                  for d in FreeCAD.listDocuments().values()}}))"""

ROW = """import FreeCAD, FreeCADGui
from PySide import QtCore, QtWidgets
mw = FreeCADGui.getMainWindow()
target = FreeCAD.getDocument({doc!r}).getObject({obj!r}).Label
found, last = None, ''
for attempt in range(6):          # the Model tree may be rebuilding (its rows are new objects): settle, find again
    QtWidgets.QApplication.processEvents()
    try:
        for tree in mw.findChildren(QtWidgets.QTreeWidget):
            if found or not tree.isVisible():
                continue
            items = tree.findItems(target, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, 0)
            items = [i for i in items if i.parent() is not None] or items   # an object row, not the document row
            for item in items:
                r = tree.visualItemRect(item)
                g = tree.viewport().mapToGlobal(r.center())
                x0 = tree.viewport().mapToGlobal(r.topLeft()).x()
                k = tree.devicePixelRatioF()
                found = (int((x0 + 48 + tree.fontMetrics().horizontalAdvance(target) // 2) * k), int(g.y() * k))
                break
        break
    except RuntimeError as e:
        found, last = None, str(e)
        QtCore.QThread.msleep(150)
print('%d %d' % found if found else 'none')"""

CELL = """import FreeCAD
print(FreeCAD.getDocument({doc!r}).getObject({sheet!r}).get({cell!r}))"""


ARROW = """import FreeCAD, FreeCADGui
from PySide import QtCore, QtWidgets
QtWidgets.QApplication.processEvents()
mw = FreeCADGui.getMainWindow()
target = FreeCAD.getDocument({doc!r}).getObject({obj!r}).Label
doclabel = FreeCAD.getDocument({doc!r}).Label
out = ''
for tree in mw.findChildren(QtWidgets.QTreeWidget):
    if out or not tree.isVisible():
        continue
    for item in tree.findItems(target, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, 0):
        chain, p, top = [], item.parent(), None
        while p is not None:
            chain.append(p); top = p; p = p.parent()
        if top is None or top.text(0) != doclabel:
            continue
        closed = [a for a in reversed(chain) if not a.isExpanded()]
        if closed:
            a = closed[0]
            r = tree.visualItemRect(a)
            g = tree.viewport().mapToGlobal(QtCore.QPoint(r.left() - tree.indentation() // 2, r.center().y()))
            k = tree.devicePixelRatioF()
            out = '%d %d' % (int(g.x() * k), int(g.y() * k))
        else:
            out = 'open'
        break
print(out or 'none')"""

VP = """import FreeCAD, FreeCADGui
from PySide import QtCore, QtWidgets
v = FreeCADGui.ActiveDocument.ActiveView
vw = [w for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QWidget)
      if w.metaObject().className() == 'Gui::View3DInventorViewer' and w.isVisible()]
w = max(vw, key=lambda w: w.width() * w.height())
k = w.devicePixelRatioF()
g = w.mapToGlobal(QtCore.QPoint(0, 0))
h = v.getSize()[1]
out = []
for p in {pts!r}:
    x, y = v.getPointOnViewport(FreeCAD.Vector(*p))
    out.append('%d %d' % (round(g.x() * k + x), round(g.y() * k + h - y)))
print(' '.join(out))"""


def main(argv):
    cmd = argv[0]
    if cmd == 'ping':
        print(xmlrpc.client.ServerProxy(URL).ping())
    elif cmd == 'save':
        print(run(SAVE.format(doc=argv[1], path=argv[2])))
    elif cmd == 'docs':
        print(run(DOCS.format()))
    elif cmd == 'arrow':
        print(run(ARROW.format(doc=argv[1], obj=argv[2])))
    elif cmd == 'vp':
        n = [float(a) for a in argv[1:]]
        print(run(VP.format(pts=[tuple(n[i:i + 3]) for i in range(0, len(n), 3)])))
    elif cmd == 'cell':
        print(run(CELL.format(doc=argv[1], sheet=argv[2], cell=argv[3])))
    elif cmd == 'row':
        print(run(ROW.format(doc=argv[1], obj=argv[2])))


if __name__ == '__main__':
    main(sys.argv[1:])
