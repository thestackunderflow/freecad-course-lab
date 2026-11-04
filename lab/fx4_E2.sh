#!/bin/bash
# fx4 take E2 (LAB-fx4 section 3.E2): sys.version in FreeCAD 1.1.4's Python console; Start RPC Server with the 0.1.28 add-on, status bar.
# FreeCAD is set up through the add-on socket (not filmed: Start page closed, console shown, coordinates read, server stopped),
# then the filmed part uses real clicks and keys only.
#   tools/run_fx4.sh e2 lab/fx4_E2.sh          (PROBE=1 in FCC_DOCKER_ARGS="-e PROBE=1": stop before recording)
set -u
O=/lab/out/fx4/E; mkdir -p "$O"
. /lab/lab/fx2_head.sh
. /lab/lab/fx4_lib.sh
autostart_on true
fx2_open_fc
{ Q "import FreeCADGui
FreeCADGui.activateWorkbench('FreeCADMCPAddonWorkbench')
print('ok')"; sleep 2; B Start_RPC_Server; B Stop_RPC_Server; } > $O/E2-coords-mcp.txt 2>&1
Q "import sys; print(sys.version)" | tee $O/E2-sys-version.txt
Q "import FreeCADGui
FreeCADGui.activateWorkbench('PartDesignWorkbench')
from PySide import QtWidgets
mw = FreeCADGui.getMainWindow()
for tb in mw.findChildren(QtWidgets.QToolBar):
    if tb.isVisible() and ('orkbench' in tb.objectName() or 'orkbench' in tb.windowTitle()):
        for w in tb.findChildren(QtWidgets.QWidget):
            if w.isVisible() and w.width() > 40:
                k = w.devicePixelRatioF(); g = w.mapToGlobal(w.rect().center())
                print(tb.objectName(), w.metaObject().className(), int(g.x()*k), int(g.y()*k), w.width(), w.height())" > $O/E2-workbench-widgets.txt
read -r CX CY < <(B console)
sleep 1
read -r SX SY < <( { Q "import FreeCADGui
FreeCADGui.activateWorkbench('FreeCADMCPAddonWorkbench')
print('ok')" > /dev/null; sleep 2; B Start_RPC_Server; } )
Q "import FreeCADGui
FreeCADGui.activateWorkbench('PartDesignWorkbench')
print('ok')" > /dev/null
echo "console $CX $CY  start $SX $SY" | tee $O/E2-xy.txt
SL_SHOT_WAKE=0 sl_shot "$O/E2-probe-before-stop.png"
[ -n "${PROBE:-}" ] && { cat $O/E2-workbench-widgets.txt; fc_quit; sl_display_stop; exit 0; }
sed -i 's/$//' /dev/null
Q "import FreeCADGui
FreeCADGui.runCommand('Stop_RPC_Server')
print('stopped')" > $O/E2-stop.txt 2>&1
sleep 2
python3 -m lab.fcrpc ping > $O/E2-socket-after-stop.txt 2>&1; echo "exit $?" >> $O/E2-socket-after-stop.txt
cat $O/E2-socket-after-stop.txt
R=$O/E2rec
sl_record "$R"; sl_mark "recording started: FreeCAD 1.1.4, Python console open"; sl_nap 1.5
sl_click $CX $CY "console: click"
sl_type 'import sys; print(sys.version)' "console: typed sys.version" 60
sl_key Return "console: Enter (sys.version)"; sl_nap 1.0
sl_mark "console: sys.version"
SL_SHOT_WAKE=0 sl_shot "$O/E2-console-sys-version.png"
sl_nap 11
sl_type 'print(sys.version_info[:3])' "console: typed version_info" 55; sl_key Return "console: Enter (version_info)"; sl_nap 1.5
sl_type 'import platform; print(platform.python_implementation())' "console: typed implementation" 55; sl_key Return "console: Enter (implementation)"; sl_nap 2
SL_SHOT_WAKE=0 sl_shot "$O/E2-freecad-window.png"
sl_click 703 86 "workbench list: opened"; sl_nap 2
xdotool type --delay 150 "MCP"; sl_nap 0.8; sl_key Return "workbench list: MCP Addon chosen"; sl_nap 2.5
sl_click $SX $SY "FreeCAD: Start RPC Server"; sl_nap 1
sl_mark "status: rpc started"; sl_nap 3
SL_SHOT_WAKE=0 sl_shot "$O/E2-status-bar.png"
sl_nap 4
sl_mark "recording stopped"; sl_stop; tsv "$R" events-E2.tsv; cp "$R/events-E2.tsv" "$O/events-E2.tsv"
cp "$O/app.log" "$O/E2-freecad-stdout.txt" 2>/dev/null
fc_quit; sl_display_stop
echo "E2 done"
