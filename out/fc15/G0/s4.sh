Q "from PySide import QtWidgets
import FreeCADGui
mw=FreeCADGui.getMainWindow()
for d in mw.findChildren(QtWidgets.QDockWidget):
    if d.windowTitle()=='Clipping':
        k=d.devicePixelRatioF()
        for w in d.findChildren(QtWidgets.QWidget):
            if w.isVisible() and isinstance(w,(QtWidgets.QCheckBox,QtWidgets.QAbstractSpinBox,QtWidgets.QLabel,QtWidgets.QPushButton,QtWidgets.QGroupBox)):
                c=w.mapToGlobal(w.rect().center()); t=getattr(w,'text',lambda:'')() if not isinstance(w,QtWidgets.QGroupBox) else w.title()
                print(w.metaObject().className(), repr(t), w.objectName(), int(c.x()*k), int(c.y()*k), getattr(w,'value',lambda:'')())"
