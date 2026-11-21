F=cup
Q "import FreeCAD; d=FreeCAD.getDocument('cup'); d.getObject('Params').set('rim_out','1.5'); d.recompute()
b=d.getObject('Body'); f=b.newObject('PartDesign::Fillet','Fillet'); f.Base=(d.getObject('Pad001'),['Edge16']); f.setExpression('Radius','Params.rim_out'); d.recompute(); print(f.State)"
Q "from PySide import QtWidgets
import FreeCADGui
mw=FreeCADGui.getMainWindow()
for d in mw.findChildren(QtWidgets.QDockWidget):
    if d.windowTitle()=='Clipping':
        g=d.findChild(QtWidgets.QGroupBox,'groupBoxY'); k=d.devicePixelRatioF(); r=g.rect(); c=g.mapToGlobal(r.topLeft())
        print('gb', int(c.x()*k), int(c.y()*k), int(r.width()*k), int(r.height()*k))
        g.setChecked(True); d.findChild(QtWidgets.QDoubleSpinBox,'clipY').setValue(0)"
FQ "look('cup','Front',31,0,49,8)"
sleep 2; shot $O/g0-clip-front.png
FQ "look('cup','Rear',31,0,49,8)"
sleep 2; shot $O/g0-clip-rear.png
