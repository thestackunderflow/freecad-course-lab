# Task R: run inside FreeCAD's GUI (passed to AppRun as a file). Stages, each leaving a flag file the probe waits for
# before its screenshot: 1 the MCP Addon workbench chosen and its "FreeCAD MCP" menu open; 2 Start RPC Server run
# (the same command the toolbar button runs) and the Report view read.
import json
import os
import sys

import FreeCAD
import FreeCADGui
from PySide import QtCore, QtWidgets

OUT = os.environ.get('R031_OUT', '/tmp/r031')
os.makedirs(OUT, exist_ok=True)
EV = {}


def flag(name):
    open(os.path.join(OUT, name), 'w').close()


def report_text():
    for d in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
        if 'Report' in d.objectName():
            d.show()
            for t in d.findChildren(QtWidgets.QPlainTextEdit) + d.findChildren(QtWidgets.QTextEdit):
                return t.toPlainText()
    return ''


def stage1():
    wbs = FreeCADGui.listWorkbenches()
    EV['workbench_menu'] = wbs['FreeCADMCPAddonWorkbench'].MenuText if 'FreeCADMCPAddonWorkbench' in wbs else None
    FreeCADGui.activateWorkbench('FreeCADMCPAddonWorkbench')
    EV['commands'] = {c: FreeCADGui.Command.get(c).getInfo()['menuText']
                      for c in ('Start_RPC_Server', 'Stop_RPC_Server') if FreeCADGui.Command.get(c)}
    EV['freecad_version'] = '.'.join(FreeCAD.Version()[:3])
    EV['freecad_python'] = sys.version.split()[0]
    mb = FreeCADGui.getMainWindow().menuBar()
    for a in mb.actions():
        if a.text().replace('&', '') == 'FreeCAD MCP':
            mb.setActiveAction(a)
    QtCore.QTimer.singleShot(2500, lambda: flag('stage1'))
    QtCore.QTimer.singleShot(6000, stage2)


def stage2():
    for m in QtWidgets.QApplication.instance().topLevelWidgets():
        if isinstance(m, QtWidgets.QMenu) and m.isVisible():
            m.hide()
    FreeCADGui.runCommand('Start_RPC_Server')
    QtCore.QTimer.singleShot(4000, stage2b)


def stage2b():
    EV['report'] = report_text()
    with open(os.path.join(OUT, 'gui.json'), 'w') as f:
        json.dump(EV, f, indent=1)
    flag('stage2')


QtCore.QTimer.singleShot(4000, stage1)
