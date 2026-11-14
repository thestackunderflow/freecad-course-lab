# fx19 helpers on top of common.sh (FreeCAD 1.1.4, Qt scale 1.8, 2880x1800). Fixed places are from G0b's stills
# (out/fx19/G0/g0b-*.png); everything else is asked of FreeCAD BEFORE a recording where possible.
#   . /lab/lab/common.sh; . /lab/lab/fx19_lib.sh
X=/lab/out/fx19
PAD_BTN="50 228"; TASK_OK="2430 615"; TASK_CANCEL="2631 615"; BOX_OK="1503 945"
SKETCH_MENU="514 36"; VALIDATE_ITEM="595 249"; HIGHLIGHT_BTN="2518 799"; VALID_CLOSE="2530 616"

Q() { (cd /lab && timeout 20 python3 -c "import sys; sys.path.insert(0,'/lab'); from lab import fcrpc; print(fcrpc.run(sys.argv[1]))" "$1"); }
B() { (cd /lab && timeout 20 python3 -m lab.button "$@"); }
ROW() { (cd /lab && timeout 20 python3 -m lab.fcrpc row "$@"); }
SP() { (cd /lab && timeout 20 python3 -m lab.sketchpt "$@"); }

fx_start() {      # fx_start LOGDIR: a fresh profile, the add-on with its socket on, FreeCAD on the virtual screen
  cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
  addon_install; autostart_on true
  sl_display $W $H
  fc_start "$1/app.log" 1.8; sleep 8
}

open_doc() {      # open_doc PATH: open, sketch + body shown (a file saved headless opens hidden), Part Design, front, fit
  Q "import FreeCAD, FreeCADGui
d = FreeCAD.openDocument('$1')
for o in d.Objects:
    if o.TypeId in ('Sketcher::SketchObject', 'PartDesign::Body', 'PartDesign::Pad'):
        FreeCADGui.getDocument(d.Name).getObject(o.Name).Visibility = True
FreeCADGui.activateWorkbench('PartDesignWorkbench')
FreeCADGui.activeDocument().activeView().viewFront(); FreeCADGui.SendMsgToActiveView('ViewFit')
from PySide import QtWidgets
for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
    if 'Report' in w.objectName(): w.show()
print(d.Name)"
}

rv_clear() {      # the Report view emptied 0.4 s after this query (so the query's own "executed" line goes too)
  Q "from PySide import QtCore, QtWidgets
import FreeCADGui
def _lab_clear():
    for d in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
        if 'Report' in d.objectName():
            for t in d.findChildren(QtWidgets.QPlainTextEdit) + d.findChildren(QtWidgets.QTextEdit):
                t.clear()
QtCore.QTimer.singleShot(400, _lab_clear)
print('ok')" > /dev/null; sleep 1
}

nwin() { xdotool search --onlyvisible --name ".*" 2>/dev/null | wc -l; }

close_box_if_any() {   # close_box_if_any BASELINE LABEL: a modal box closed with its own default button (Return), no query
  if [ "$(nwin)" -gt "$1" ]; then sl_key Return "$2"; sleep 1.5; echo "box closed: $2"; else echo "no box: $2"; fi
}

clk() { set -- $1 "$2"; [ $# -eq 3 ] || { echo "clk: no place for $*" >&2; return 1; }; sl_glide "$1" "$2" 20; sl_nap 0.5; sl_click "$1" "$2" "$3"; }

row_open() {      # row_open DOC OBJ: "x y" of OBJ's tree row, its closed parents opened first by clicks (not filmed)
  local a i
  for i in 1 2 3 4; do
    a=$(cd /lab && timeout 20 python3 -m lab.fcrpc arrow "$1" "$2")
    [ "$a" = open ] && break
    set -- "$1" "$2"; xdotool mousemove ${a% *} ${a#* } click 1; sleep 1
  done
  ROW "$1" "$2"
}

report_hide() {   # not filmed: the Report view dock closed (lab queries write a line there each)
  Q "import FreeCADGui
from PySide import QtWidgets
for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
    if 'Report' in w.objectName(): w.hide()
print('ok')" > /dev/null
}

console_line() {  # console_line OUTDIR LINE: View, Panels, Python console (its tab if docked as a tab); click; type; Enter
  sl_click 211 36 "View menu"
  sl_glide 255 1043 25; sl_mark "View: Panels"; sl_nap 0.6
  sl_glide 700 1043 25; sl_nap 0.3
  sl_click 800 1124 "Panels: Python console"; sl_nap 2
  local t k
  t=$(B tab "Python Console"); [ -n "$t" ] && [ "$t" != none ] && { clk "$t" "tab: Python Console"; sl_nap 1; }
  k=$(B console); echo "console at $k" >> "$1/take.log"
  clk "$k" "console: click" || return 1
  sl_type "$2" "console: typed the volume line" 85
  sl_key Return "console: Enter"; sl_nap 4
}
