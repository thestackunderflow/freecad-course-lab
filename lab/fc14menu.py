# fc14: a popup menu's items and their screen centres written to a file by a timer (the add-on's socket is blocked while a
# menu is open). Q "exec(open('/lab/lab/fc14menu.py').read()); arm('/tmp/menu.json', 2500)" then right-click within 2.5 s.
import json as _j
from PySide import QtCore as _QC, QtWidgets as _QWm


def _dump(path):
    out = []
    for m in _QWm.QApplication.topLevelWidgets():
        if isinstance(m, _QWm.QMenu) and m.isVisible():
            k = m.devicePixelRatioF()
            for a in m.actions():
                if a.isSeparator():
                    continue
                c = m.mapToGlobal(m.actionGeometry(a).center())
                out.append([a.text().replace('&', ''), a.isEnabled(), int(c.x() * k), int(c.y() * k)])
    with open(path, 'w') as f:
        _j.dump(out, f)


def arm(path, ms):
    _QC.QTimer.singleShot(ms, lambda: _dump(path))
    print('armed')


def _dump_dialog(path):
    out = []
    for w in _QWm.QApplication.topLevelWidgets():
        if w.isVisible() and isinstance(w, _QWm.QDialog):
            k = w.devicePixelRatioF()
            g = lambda wid, pt: (int(wid.mapToGlobal(pt).x() * k), int(wid.mapToGlobal(pt).y() * k))
            items = []
            for lw in w.findChildren(_QWm.QListWidget):
                for i in range(lw.count()):
                    it = lw.item(i)
                    items.append([it.text(), it.isSelected()] + list(g(lw.viewport(), lw.visualItemRect(it).center())))
            out.append({'title': w.windowTitle(), 'labels': [l.text() for l in w.findChildren(_QWm.QLabel) if l.isVisible() and l.text()],
                        'items': items, 'checks': [(c.text(), c.isChecked()) for c in w.findChildren(_QWm.QCheckBox) if c.isVisible()],
                        'buttons': [[b.text().replace('&', ''), b.isDefault()] + list(g(b, b.rect().center()))
                                    for b in w.findChildren(_QWm.QPushButton) if b.isVisible()]})
    with open(path, 'w') as f:
        _j.dump(out, f)


def arm_dialog(path, ms):
    _QC.QTimer.singleShot(ms, lambda: _dump_dialog(path))
    print('armed')


def _dump_all(path):
    st = {'menu': [], 'dialogs': [], 'popup': []}
    for m in _QWm.QApplication.topLevelWidgets():
        if isinstance(m, _QWm.QMenu) and m.isVisible():
            k = m.devicePixelRatioF()
            for a in m.actions():
                if not a.isSeparator():
                    c = m.mapToGlobal(m.actionGeometry(a).center())
                    st['menu'].append([a.text().replace('&', ''), a.isEnabled(), int(c.x() * k), int(c.y() * k)])
    for v in _QWm.QApplication.allWidgets():
        if isinstance(v, _QWm.QAbstractItemView) and v.isVisible() and 'ComboBox' in v.metaObject().className():
            k = v.devicePixelRatioF(); md = v.model()
            for r in range(md.rowCount()):
                c = v.viewport().mapToGlobal(v.visualRect(md.index(r, 0)).center())
                st['popup'].append([md.index(r, 0).data(), int(c.x() * k), int(c.y() * k)])
    for w in _QWm.QApplication.topLevelWidgets():
        if w.isVisible() and isinstance(w, (_QWm.QDialog, _QWm.QMessageBox)):
            k = w.devicePixelRatioF()
            g = lambda wid: (int(wid.mapToGlobal(wid.rect().center()).x() * k), int(wid.mapToGlobal(wid.rect().center()).y() * k))
            st['dialogs'].append({'title': w.windowTitle(),
                'labels': [l.text() for l in w.findChildren(_QWm.QLabel) if l.isVisible() and l.text()],
                'combos': [[c.currentText(), [c.itemText(i) for i in range(c.count())]] + list(g(c)) for c in w.findChildren(_QWm.QComboBox) if c.isVisible()],
                'checks': [(c.text(), c.isChecked()) for c in w.findChildren(_QWm.QCheckBox) if c.isVisible()],
                'buttons': [[b.text().replace('&', ''), b.isDefault()] + list(g(b)) for b in w.findChildren(_QWm.QPushButton) if b.isVisible()]})
    with open(path + '.tmp', 'w') as f:
        _j.dump(st, f)
    import os as _os
    _os.replace(path + '.tmp', path)


def watch(path, seconds, every=300):
    for i in range(int(seconds * 1000 / every)):
        _QC.QTimer.singleShot(every * (i + 1), lambda: _dump_all(path))
    print('watching')
