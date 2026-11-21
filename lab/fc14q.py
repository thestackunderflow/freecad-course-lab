"""fc14 lab queries run INSIDE FreeCAD (after fc8q.py + fc9q.py + fc12q.py; FQ14 execs all four), never filmed."""
from PySide import QtWidgets as _QW14


def _gpx(w, pt):
    g = w.mapToGlobal(pt)
    k = w.devicePixelRatioF()
    return '%d %d' % (int(g.x() * k), int(g.y() * k))


def menu_items():
    """[(text, enabled)] of every visible popup menu"""
    _QW14.QApplication.processEvents()
    out = []
    for m in _QW14.QApplication.topLevelWidgets():
        if isinstance(m, _QW14.QMenu) and m.isVisible():
            out.append([(a.text(), a.isEnabled()) for a in m.actions() if not a.isSeparator()])
    print(out)


def menu_pos(text):
    """centre of a visible popup menu's item whose text starts with `text` ("none" if none shows it)"""
    _QW14.QApplication.processEvents()
    for m in _QW14.QApplication.topLevelWidgets():
        if isinstance(m, _QW14.QMenu) and m.isVisible():
            for a in m.actions():
                if a.text().replace('&', '').startswith(text):
                    print(_gpx(m, m.actionGeometry(a).center()))
                    return
    print('none')


def dialog_list():
    """visible dialogs: title, labels, list items, buttons"""
    _QW14.QApplication.processEvents()
    out = []
    for w in _QW14.QApplication.topLevelWidgets():
        if w.isVisible() and isinstance(w, _QW14.QDialog):
            items = []
            for lw in w.findChildren(_QW14.QListWidget):
                items += [lw.item(i).text() for i in range(lw.count())]
            out.append([w.windowTitle(), [l.text() for l in w.findChildren(_QW14.QLabel) if l.isVisible() and l.text()],
                        items, [b.text() for b in w.findChildren(_QW14.QPushButton) if b.isVisible()]])
    print(out)


def dialog_item_pos(text):
    """centre of a list item (in a visible dialog) whose text starts with `text`"""
    _QW14.QApplication.processEvents()
    for w in _QW14.QApplication.topLevelWidgets():
        if w.isVisible() and isinstance(w, _QW14.QDialog):
            for lw in w.findChildren(_QW14.QListWidget):
                for i in range(lw.count()):
                    if lw.item(i).text().startswith(text):
                        r = lw.visualItemRect(lw.item(i))
                        print(_gpx(lw.viewport(), r.center()))
                        return
    print('none')


def dialog_button_pos(text):
    _QW14.QApplication.processEvents()
    for w in _QW14.QApplication.topLevelWidgets():
        if w.isVisible() and isinstance(w, _QW14.QDialog):
            for b in w.findChildren(_QW14.QPushButton):
                if b.isVisible() and b.text().replace('&', '') == text:
                    print(_gpx(b, b.rect().center()))
                    return
    print('none')


def task_list_items():
    """the dress-up panel's face list (text of every item)"""
    out = []
    for lw in _mw.findChildren(_QW14.QListWidget):
        if lw.isVisible():
            out.append([lw.item(i).text() for i in range(lw.count())])
    print(out)


def task_list_item_pos(text):
    for lw in _mw.findChildren(_QW14.QListWidget):
        if lw.isVisible():
            for i in range(lw.count()):
                if lw.item(i).text() == text:
                    print(_gpx(lw.viewport(), lw.visualItemRect(lw.item(i)).center()))
                    return
    print('none')
