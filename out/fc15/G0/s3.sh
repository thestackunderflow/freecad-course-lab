F=cup
Q "import FreeCADGui; FreeCADGui.getDocument('cup').activeView().viewFront(); FreeCADGui.SendMsgToActiveView('ViewFit'); FreeCADGui.runCommand('Std_ToggleClipPlane',0); print(1)"
sleep 3
echo "dialogs: $(dialogs)"
Q "from PySide import QtWidgets
import FreeCADGui
out=[]
for w in QtWidgets.QApplication.topLevelWidgets():
    if w.isVisible() and w.windowTitle(): out.append((w.metaObject().className(), w.windowTitle()))
dk=[d.windowTitle() for d in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget) if d.isVisible()]
print(out, dk)"
echo "panel: $(FQ "task_texts()" | cut -c1-1500)"
shot $O/g0-clip.png
