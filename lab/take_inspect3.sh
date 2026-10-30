#!/bin/bash
# Lesson 3 take "inspect" (PLAN-L3 F24, F26, F28; no AI, free): a Claude run's own saved documents opened again, as a
# viewer checks them. (In run B1 the filmed viewer steps could not click Claude's part: the lab's tree lookup missed
# rows of a second document; fixed in lab/fcrpc.py with model indexes. The run's own copies are re-opened here and
# labelled "opened again".) FreeCAD 1.1.4 at 1.5 scale on the right of the screen as in the run, Python console shown.
# Filmed: File > Open the copy saved after message 1; the part clicked in the tree; the volume line. The copy after
# message 2: the volume line and the X line. The copy after message 3: the volume line; the spreadsheet opened.
#   tools/run.sh lab/take_inspect3.sh B1
set -u
. /lab/lab/common.sh
RUN=${1:-B1}
R=/lab/out/l3/runs/$RUN
O=/lab/out/l3/inspect-$RUN; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
for st in first after2 after3; do cp "$R/$st.FCStd" ~/"$RUN-$st.FCStd"; done
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 8
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 1
cd /lab
python3 - > "$O/setup-rpc.txt" 2>&1 <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCADGui
from PySide import QtCore, QtWidgets
mw = FreeCADGui.getMainWindow()
FreeCADGui.activateWorkbench('PartDesignWorkbench')
for w in mw.findChildren(QtWidgets.QMdiArea)[0].subWindowList():
    if w.windowTitle().startswith('Start'):
        w.close()
for w in mw.findChildren(QtWidgets.QDockWidget):
    if w.objectName() in ('Python console',):
        w.show()
        mw.resizeDocks([w], [260], QtCore.Qt.Vertical)
print(1)"""))
PY
sleep 2
xdotool mousemove 2000 700
console() {
  sl_click 2016 1722 "console: click"
  sl_type "$1" "console: typed $2" 70
  sl_key Return "console: Enter ($2)"
  sl_nap 3.0
}
open_doc() {   # open_doc FILE: File > Open, the name typed, Enter
  sl_click 2400 900 "FreeCAD: click the 3D view"
  sl_key ctrl+o "File > Open (Ctrl+O)"
  sl_nap 2.0
  sl_type "~/$1" "open: typed $1" 90
  sl_key Return "open: Enter"
  sl_nap 3.0
  xdotool mousemove 2400 900; sl_key 0 "key 0: isometric"; sl_key v "key V"; sl_key f "key F (fit all)"; sl_nap 1.5
}
pick() {   # pick DOC OBJ: open the rows above it, then click it
  local ax ay i x y
  for i in 1 2 3; do
    read -r ax ay < <(python3 -m lab.fcrpc arrow "$1" "$2" 2>>"$O/lab-query.err")
    { [ "${ax:-}" = open ] || [ "${ax:-}" = none ] || [ -z "${ay:-}" ]; } && break
    sl_click "$ax" "$ay" "tree: open a row"; sl_nap 0.6
  done
  read -r x y < <(python3 -m lab.fcrpc row "$1" "$2" 2>>"$O/lab-query.err")
  if [ -n "${y:-}" ]; then sl_click "$x" "$y" "tree: $2"; else sl_mark "tree: $2 row not found"; fi
  sl_nap 1.0
}
docname() { python3 -c "
import json; d = json.load(open('$R/newpart-$1.json'))['claude']; print(d[0], d[1])"; }
sl_record "$O"
sl_mark "recording started: run $RUN's saved copies, opened again (no AI)"
sl_nap 1.5
for st in first after2 after3; do
  open_doc "$RUN-$st.FCStd"
  read -r DOC OBJ < <(python3 -m lab.fcrpc docs 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
name = [k for k, v in d.items() if v['label'].startswith('$RUN-$st') or k.startswith('$RUN')]
k = name[-1] if name else list(d)[-1]
objs = [o for o in d[k]['objects'] if o[0] == 'Body'] or d[k]['objects']
print(k, objs[0][0])")
  echo "$st $DOC $OBJ" >> "$O/docs.txt"
  pick "$DOC" "$OBJ"
  sl_mark "check: $st"
  console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line ($st)"
  [ "$st" = after2 ] && console "b = Gui.Selection.getSelection()[0].Shape.BoundBox; round(b.XMin, 3), round(b.XMax, 3)" "the X line"
  sl_shot "$O/s-$st.png"
done
SHEET=$(python3 -c "
import json; m = json.load(open('$R/measure-after3.json')); s = m.get('sheets') or []; print(s[0]['name'] if s else '')")
if [ -n "$SHEET" ]; then
  pick "$DOC" "$SHEET"
  read -r x y < <(python3 -m lab.fcrpc row "$DOC" "$SHEET" 2>>"$O/lab-query.err")
  if [ -n "${y:-}" ]; then
    sl_glide "$x" "$y" 15; sl_mark "tree: double-click the spreadsheet"; xdotool click --repeat 2 --delay 120 1
    sl_nap 4.0; sl_shot "$O/s-sheet.png"; sl_mark "the spreadsheet open"; sl_nap 3.0
  fi
fi
sl_mark "recording stopped"
sl_stop
fc_quit; sl_display_stop
echo "inspect done ($RUN)"; cat "$O/docs.txt"
