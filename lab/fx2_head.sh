# fx2 shared head: FreeCAD set up through the add-on socket (not filmed), console + export helpers.
. /lab/lab/common.sh
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
mkdir -p ~/fx2
Q() { python3 -c "import sys; sys.path.insert(0, '/lab'); from lab import fcrpc; print(fcrpc.run(sys.argv[1]))" "$1" 2>>"$O/lab-query.err"; }
B() { python3 -m lab.button "$@" 2>>"$O/lab-query.err"; }
fx2_open_fc() {
  sl_display $W $H
  fc_start "$O/app.log" 1.8; sleep 8
  Q "import FreeCADGui
from PySide import QtCore, QtWidgets
mw = FreeCADGui.getMainWindow()
for w in mw.findChildren(QtWidgets.QMdiArea)[0].subWindowList():
    if w.windowTitle().startswith('Start'):
        w.close()
for w in mw.findChildren(QtWidgets.QDockWidget):
    if w.objectName() in ('Python console',):
        w.show()
        mw.resizeDocks([w], [190], QtCore.Qt.Vertical)
        w.widget().clear()
print(1)" > /dev/null
  local w; w=$(xdotool search --name "FreeCAD" | head -1); wmctrl -i -r "$w" -b add,maximized_vert,maximized_horz; sleep 2
  xdotool mousemove 1500 700
}
console() {   # console "line" LABEL
  local cx cy; read -r cx cy < <(B console)
  sl_click "$cx" "$cy" "console: click"
  sl_type "$1" "console: typed $2" 55
  sl_key Return "console: Enter ($2)"
  sl_nap 1.5
}
export_as() {  # export_as PATH LABEL [type]: File, Export, (type list STL Mesh), the name, Enter
  sl_click 45 36 "File menu ($2)"
  sl_glide 105 554 15; sl_nap 0.5
  sl_click 105 554 "File: Export ($2)"
  sl_nap 3.0
  if [ "${3:-}" = type ]; then
    sl_click 1404 1225 "Export: the type list"; sl_nap 2.5
    sl_glide 1253 1421 25; sl_mark "Export: hover STL Mesh"; sl_nap 1.5
    sl_click 1253 1421 "Export: STL Mesh"; sl_nap 1.2
  fi
  sl_click 1400 1171 "Export: the file name box ($2)"
  xdotool key ctrl+a
  sl_type "$1" "Export: typed $1" 80
  sl_nap 0.8
  sl_key Return "Export: Enter ($2)"
  sl_nap 4.0
}
