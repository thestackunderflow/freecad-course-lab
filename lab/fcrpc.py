"""Lab instrument, never filmed as a step: talk to the FreeCAD add-on's own XML-RPC socket (127.0.0.1:9875) to save a
copy of a document for measuring, or to find where a tree row is drawn so the script can click it like a person would.
(Each request briefly shows "MCP: processing…" in FreeCAD's status bar; the takes log a "lab query" event around it.)

    python3 -m lab.fcrpc save DOC PATH          save a copy (the open document is not renamed)
    python3 -m lab.fcrpc row DOC OBJ            prints "x y" of the object's row in the Model tree (screen pixels)
    python3 -m lab.fcrpc docs                   prints the open documents and their objects as JSON
    python3 -m lab.fcrpc ping"""
import json
import sys
import xmlrpc.client

URL = 'http://127.0.0.1:9875'


def run(code):
    r = xmlrpc.client.ServerProxy(URL, allow_none=True).execute_code(code)
    if not r.get('success'):
        raise RuntimeError(r)
    return r['message'].split('Output: ', 1)[-1].strip()


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
found = None
for tree in mw.findChildren(QtWidgets.QTreeWidget):
    if found or not tree.isVisible():
        continue
    items = tree.findItems(target, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, 0)
    items = [i for i in items if i.parent() is not None] or items   # an object row, not a document row of the same name
    for item in items:
        r = tree.visualItemRect(item)
        g = tree.viewport().mapToGlobal(r.center())
        x0 = tree.viewport().mapToGlobal(r.topLeft()).x()
        k = tree.devicePixelRatioF()
        found = (int((x0 + 48 + tree.fontMetrics().horizontalAdvance(target) // 2) * k), int(g.y() * k))
        break
print('%d %d' % found)"""


def main(argv):
    cmd = argv[0]
    if cmd == 'ping':
        print(xmlrpc.client.ServerProxy(URL).ping())
    elif cmd == 'save':
        print(run(SAVE.format(doc=argv[1], path=argv[2])))
    elif cmd == 'docs':
        print(run(DOCS.format()))
    elif cmd == 'row':
        print(run(ROW.format(doc=argv[1], obj=argv[2])))


if __name__ == '__main__':
    main(sys.argv[1:])
