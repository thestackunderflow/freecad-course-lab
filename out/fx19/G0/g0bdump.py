"""G0b reader (not filmed): every visible text a person could read right now, over the add-on socket, as JSON.
    python3 /lab/out/fx19/G0/g0bdump.py OUT.json
Dialogs (title + labels + buttons), the task panel's labels/buttons, the Report view's text, the Model tree rows with
their tooltips, the status bar. Wrapped by lab.fcrpc.guard, so it cannot raise inside FreeCAD."""
import json
import sys

sys.path.insert(0, '/lab')
from lab import fcrpc  # noqa: E402

CODE = r"""import FreeCADGui, json
from PySide import QtWidgets, QtCore
QtWidgets.QApplication.processEvents()
mw = FreeCADGui.getMainWindow()
R = {'dialogs': [], 'report': '', 'tree': [], 'status': '', 'task': {'labels': [], 'buttons': [], 'groups': []}}
for w in QtWidgets.QApplication.topLevelWidgets():
    if w is mw or not w.isVisible():
        continue
    R['dialogs'].append({'class': w.metaObject().className(), 'title': w.windowTitle(),
        'labels': [l.text() for l in w.findChildren(QtWidgets.QLabel) if l.isVisible() and l.text()],
        'buttons': [b.text() for b in w.findChildren(QtWidgets.QAbstractButton) if b.isVisible() and b.text()]})
for d in mw.findChildren(QtWidgets.QDockWidget):
    if not d.isVisible():
        continue
    if 'Report' in d.objectName() or 'Report' in d.windowTitle():
        for t in d.findChildren(QtWidgets.QPlainTextEdit) + d.findChildren(QtWidgets.QTextEdit):
            R['report'] += t.toPlainText()
for d in mw.findChildren(QtWidgets.QWidget):
    if d.metaObject().className() in ('Gui::TaskView::TaskView',) and d.isVisible():
        R['task']['labels'] += [l.text() for l in d.findChildren(QtWidgets.QLabel) if l.isVisible() and l.text()]
        R['task']['buttons'] += [b.text() for b in d.findChildren(QtWidgets.QAbstractButton) if b.isVisible() and b.text()]
        R['task']['groups'] += [g.title() for g in d.findChildren(QtWidgets.QGroupBox) if g.isVisible() and g.title()]
        for w in d.findChildren(QtWidgets.QWidget):
            if w.isVisible() and w.metaObject().className() in ('Gui::TaskView::TaskBox', 'QSint::ActionGroup'):
                R['task']['groups'].append('box:' + (w.windowTitle() or ''))
for tv in mw.findChildren(QtWidgets.QTreeView):
    if not tv.isVisible():
        continue
    m = tv.model()
    if m is None:
        continue
    def walk(p, depth):
        for r in range(m.rowCount(p)):
            i = m.index(r, 0, p)
            R['tree'].append({'text': m.data(i), 'tip': m.data(i, QtCore.Qt.ToolTipRole), 'depth': depth})
            if depth < 4:
                walk(i, depth + 1)
    walk(QtCore.QModelIndex(), 0)
R['status'] = mw.statusBar().currentMessage()
print(json.dumps(R))"""

if __name__ == '__main__':
    out = fcrpc.run(CODE)
    d = json.loads(out)
    json.dump(d, open(sys.argv[1], 'w'), indent=1)
    print('dialogs', [(x['title'], x['labels']) for x in d['dialogs']])
    print('task', d['task'])
    print('tree tips', [(t['text'], t['tip']) for t in d['tree'] if t['tip']])
    print('report tail', d['report'][-400:])
    print('status', d['status'])
