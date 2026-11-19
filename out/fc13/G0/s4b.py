import FreeCAD, FreeCADGui
from PySide import QtWidgets
v = FreeCADGui.getDocument('trap').activeView()
out = []
for ax in ((0, 1, 0), (1, 0, 0)):
    for a in (-60, -45, -30, 30, 45, 60):
        v.viewTop()
        v.setCameraOrientation(FreeCAD.Rotation(FreeCAD.Vector(*ax), a).multiply(v.getCameraOrientation()))
        FreeCADGui.SendMsgToActiveView('ViewFit')
        QtWidgets.QApplication.processEvents()
        row = []
        for p in ((28, 0, 40), (-28, 0, 40), (28, 0, 30), (-28, 0, 30)):
            sp = v.getPointOnViewport(FreeCAD.Vector(*p))
            i = v.getObjectInfo((int(sp[0]), int(sp[1])))
            row.append((p[0], p[2], i['Component'] if i else None))
        out.append((ax, a, row))
for r in out:
    print(r)
