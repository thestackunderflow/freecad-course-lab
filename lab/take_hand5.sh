#!/bin/bash
# Lesson 5 take "hand" (PLAN-L5 by-hand frames; lab L5-Q1..Q4): lesson 4's hook as lesson 4 left it (hook-lesson4.FCStd
# = lesson 4's by-hand width30: 30 wide, two 4 mm holes, the 2 mm fillet). Filmed, at a person's pace: File, Open; the
# Fillet row and the volume line; the tree's rows lit (Body, Pad, Hole, Fillet); the Body clicked; File, Export; the
# type list, STL Mesh; hook.stl; Save. The Mesh workbench; File, Import hook.stl; the Body hidden; the mesh row (Mesh
# Info: facets); Evaluate and repair mesh: All above tests together, Analyze; Close; Check solid mesh (its box). Watch
# only: the Pad row, File, Export hook-pad.stl; imported; its Mesh Info; Check solid mesh. The volume line of each mesh.
# Flat lines, the back view, a hole zoomed. Edit, Preferences, Import-Export, Mesh Formats: Maximum mesh deviation 0.01;
# OK; the Body, File, Export hook-fine.stl; imported; its Mesh Info; its hole zoomed.
# Not filmed (logged "lab query" events): object names and screen places read through the add-on's socket; the
# parameter read back after OK (the take stops if it is not 0.01); every STL measured by checker/mesh5.
#   FCC_PREFIX=fc5 tools/run.sh lab/take_hand5.sh
set -u
. /lab/lab/common.sh
O=/lab/out/l5/hand; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
cp /lab/out/l4/hand/width30.FCStd ~/hook-lesson4.FCStd
sl_display $W $H
fc_start "$O/app.log" 1.8; sleep 8
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
        mw.resizeDocks([w], [190], QtCore.Qt.Vertical)
        w.widget().clear()
print(1)"""))
PY
w=$(xdotool search --name "FreeCAD" | head -1); wmctrl -i -r "$w" -b add,maximized_vert,maximized_horz; sleep 2
DOC=hook_lesson4
xdotool mousemove 1500 700
B() { python3 -m lab.button "$@" 2>>"$O/lab-query.err"; }
Q() { python3 -c "import sys; sys.path.insert(0, '/lab'); from lab import fcrpc; print(fcrpc.run(sys.argv[1]))" "$1" 2>>"$O/lab-query.err"; }
row() { python3 -m lab.fcrpc row "$DOC" "$1" 2>>"$O/lab-query.err"; }
objname() { Q "import FreeCAD
d = FreeCAD.getDocument('$DOC')
print(([o.Name for o in d.Objects if o.Label == '$1'] or [''])[-1])"; }
console() {   # console "line" LABEL
  local cx cy; read -r cx cy < <(B console)
  sl_click "$cx" "$cy" "console: click"
  sl_type "$1" "console: typed $2" 70
  sl_key Return "console: Enter ($2)"
  sl_nap 3.5
}
pick() {      # pick OBJ LABEL: click a tree row
  local x y; read -r x y < <(row "$1"); sl_click "$x" "$y" "tree: $2"; sl_nap 1.0
}
hover() { local x y; read -r x y < <(row "$1"); sl_glide "$x" "$y" 18; sl_mark "tree: hover $2"; sl_nap 1.8; }
export_as() {  # export_as NAME LABEL [pick-type]: File, Export, (the type list, STL Mesh), the name, Enter
  sl_click 45 36 "File menu ($2)"
  sl_glide 105 554 15; sl_nap 0.5
  sl_click 105 554 "File: Export ($2)"
  sl_nap 3.0
  if [ "${3:-}" = type ]; then
    sl_click 1404 1225 "Export: the type list"
    sl_nap 2.5
    sl_glide 1212 1421 25; sl_mark "Export: hover STL Mesh"; sl_nap 1.2
    sl_click 1212 1421 "Export: STL Mesh"
    sl_nap 1.2
  fi
  sl_click 1400 1171 "Export: the file name box ($2)"
  xdotool key ctrl+a
  sl_type "$1" "Export: typed $1" 90
  sl_nap 0.8
  sl_key Return "Export: Enter ($2)"
  sl_nap 4.0
}
import_file() {  # import_file NAME LABEL
  sl_click 45 36 "File menu ($2)"
  sl_glide 105 511 15; sl_nap 0.5
  sl_click 105 511 "File: Import ($2)"
  sl_nap 3.0
  sl_type "$1" "Import: typed $1" 90
  sl_nap 0.6
  sl_key Return "Import: Enter ($2)"
  sl_nap 4.0
}
hide() { pick "$1" "$2 (to hide it)"; sl_key space "key Space: hide $2"; sl_nap 1.0; }
measure() { python3 -m checker.mesh5 "$HOME/$1" "$O/mesh-${1%.stl}.json" > /dev/null 2>&1; cp "$HOME/$1" "$O/$1" 2>/dev/null; }
sl_record "$O"
sl_mark "recording started: FreeCAD, Part Design"
sl_nap 1.5
# F5: File, Open; the Fillet row; the volume line
sl_click 45 36 "File menu"
sl_glide 160 110 15; sl_nap 0.4
sl_click 160 110 "File: Open"
sl_nap 2.0
sl_type "~/hook-lesson4.FCStd" "open: typed the file name" 90
sl_nap 0.6
sl_key Return "open: Enter"
sl_nap 3.5
xdotool mousemove 1500 1200; sl_key 0 "key 0: isometric"; sl_nap 0.6; sl_key v "key V"; sl_key f "key F (fit all)"; sl_nap 1.5
pick Fillet "Fillet (the last row)"
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line (lesson 4's hook)"
sl_shot "$O/s1-opened.png"
# F6: the rows
hover Body "Body"; hover Pad "Pad"; hover Hole "Hole"; hover Fillet "Fillet"
sl_shot "$O/s2-rows.png"
# F7: the Body; File, Export; STL Mesh; hook.stl
pick Body "Body"
export_as hook.stl "the Body" type
sl_shot "$O/s3-exported.png"
measure hook.stl
# F8: the Mesh workbench; File, Import; the Body hidden; the mesh row; Mesh Info
sl_click 700 88 "workbench list"
sl_nap 1.2
sl_glide 596 298 20; sl_mark "hover: Mesh"; sl_nap 0.6
sl_click 596 298 "workbench: Mesh"
sl_nap 2.5
import_file hook.stl "the Body's STL"
M1=$(objname hook); echo "mesh1 $M1" >> "$O/objects.txt"
hide Body "Body"
pick "$M1" "the mesh hook"
sl_mark "Mesh Info: hook"; sl_nap 3.0
sl_shot "$O/s4-meshinfo.png"
# F9: Evaluate and repair mesh: All above tests together, Analyze; Close; Check solid mesh
read -r EX EY < <(B Mesh_Evaluation)
sl_glide "$EX" "$EY" 20; sl_mark "hover: Evaluate and repair mesh"; sl_nap 1.5
sl_click "$EX" "$EY" "Evaluate and repair mesh"
sl_nap 2.5
sl_mark "lab query: the panel's buttons"
read -r AX AY CX CY < <(Q "import FreeCADGui
from PySide import QtWidgets, QtCore
mw = FreeCADGui.getMainWindow()
out = 'none'
for d in mw.findChildren(QtWidgets.QDockWidget):
    if d.isVisible() and 'valuat' in d.windowTitle():
        mw.resizeDocks([d], [900], QtCore.Qt.Horizontal)
        QtWidgets.QApplication.processEvents()
        def c(b):
            g = b.mapToGlobal(b.rect().center()); k = b.devicePixelRatioF()
            return '%d %d' % (int(g.x() * k), int(g.y() * k))
        a = [b for b in d.findChildren(QtWidgets.QAbstractButton) if b.objectName() == 'analyzeAllTogether'][0]
        cl = [b for b in d.findChildren(QtWidgets.QAbstractButton) if b.text().endswith('Close')][0]
        out = c(a) + ' ' + c(cl)
print(out)")
echo "evaluate $AX $AY $CX $CY" >> "$O/objects.txt"
sl_nap 1.5
sl_glide "$AX" "$AY" 25; sl_mark "hover: Analyze (all above tests together)"; sl_nap 1.2
sl_click "$AX" "$AY" "Analyze: all above tests together"
sl_nap 6.0
sl_mark "Evaluate: the rows read"
sl_shot "$O/s5-evaluate.png"
Q "import FreeCADGui
from PySide import QtWidgets
mw = FreeCADGui.getMainWindow()
print([b.text() for d in mw.findChildren(QtWidgets.QDockWidget) if d.isVisible() and 'valuat' in d.windowTitle() for b in d.findChildren(QtWidgets.QCheckBox)])" > "$O/evaluate-rows.txt"
sl_nap 2.0
sl_click "$CX" "$CY" "Evaluate: Close"
sl_nap 2.0
pick "$M1" "the mesh hook"
read -r SX SY < <(B Mesh_EvaluateSolid)
sl_glide "$SX" "$SY" 20; sl_mark "hover: Check solid mesh"; sl_nap 1.5
sl_click "$SX" "$SY" "Check solid mesh"
sl_nap 3.0
sl_mark "Check solid mesh: the box (hook)"
sl_shot "$O/s6-solid.png"
sl_nap 2.0
sl_key Return "Check solid mesh: OK"
sl_nap 1.5
# F10: watch only: the Pad row; File, Export hook-pad.stl; imported; Mesh Info; Check solid mesh
sl_mark "watch only: the Pad"
pick Pad "Pad (the wrong row)"
export_as hook-pad.stl "the Pad"
measure hook-pad.stl
import_file hook-pad.stl "the Pad's STL"
M2=$(objname hook-pad); echo "mesh2 $M2" >> "$O/objects.txt"
hide "$M1" "the mesh hook"
pick "$M2" "the mesh hook-pad"
sl_mark "Mesh Info: hook-pad"; sl_nap 3.0
sl_shot "$O/s7-padinfo.png"
read -r SX SY < <(B Mesh_EvaluateSolid)
sl_click "$SX" "$SY" "Check solid mesh (hook-pad)"
sl_nap 3.0
sl_mark "Check solid mesh: the box (hook-pad)"
sl_shot "$O/s8-padsolid.png"
sl_nap 2.0
sl_key Return "Check solid mesh: OK (hook-pad)"
sl_nap 1.5
# F11: the volume line of each mesh
pick "$M1" "the mesh hook"
console "Gui.Selection.getSelection()[0].Mesh.Volume" "the mesh volume (hook)"
pick "$M2" "the mesh hook-pad"
console "Gui.Selection.getSelection()[0].Mesh.Volume" "the mesh volume (hook-pad)"
sl_shot "$O/s9-volumes.png"
# F12: flat lines, the back view, a hole zoomed
hide "$M2" "the mesh hook-pad"
pick "$M1" "the mesh hook (show it)"; sl_key space "key Space: show the mesh hook"; sl_nap 1.0
xdotool mousemove 1500 1300
sl_key v "key V"; sl_key 7 "key 7: flat lines"; sl_nap 1.0
sl_key 6 "key 6: the back"; sl_nap 0.6; sl_key v "key V"; sl_key f "key F (fit all)"; sl_nap 2.0
read -r HX HY < <(python3 -m lab.fcrpc vp 0 -15 15 2>>"$O/lab-query.err")
sl_glide "$HX" "$HY" 25; sl_nap 0.5
for i in $(seq 1 16); do xdotool click 4; sleep 0.3; done
sl_glide $((HX + 700)) $((HY + 500)) 20
sl_mark "the hole zoomed (hook, 26 sides)"; sl_nap 4.0
sl_shot "$O/s10-hole26.png"
# F13: Edit, Preferences, Import-Export, Mesh Formats; 0.01; OK
sl_click 124 36 "Edit menu"
sl_glide 200 860 20; sl_nap 0.5
sl_click 200 860 "Edit: Preferences"
sl_nap 3.0
sl_click 783 675 "Preferences: Import-Export"
sl_nap 1.5
sl_click 752 968 "Preferences: Mesh Formats"
sl_nap 2.5
sl_shot "$O/s11-meshformats.png"
sl_glide 1973 265 20; sl_mark "hover: Maximum mesh deviation"; sl_nap 1.5
sl_click 1973 265 "Maximum mesh deviation: the box"
sleep 0.4; xdotool key ctrl+a
sl_type "0.01" "Maximum mesh deviation: typed 0.01" 200
sl_nap 1.5
sl_shot "$O/s12-deviation.png"
sl_click 1793 1656 "Preferences: OK"
sl_nap 2.0
sl_mark "lab query: the deviation read back"
DEV=$(Q "import FreeCAD
print(FreeCAD.ParamGet('User parameter:BaseApp/Preferences/Mod/Mesh').GetFloat('MaxDeviationExport', -1))")
echo "deviation $DEV" >> "$O/objects.txt"
if [ "$DEV" != "0.01" ]; then sl_mark "STOP: deviation is $DEV"; sl_stop; fc_quit; sl_display_stop; echo "deviation $DEV, stopped"; exit 3; fi
pick Body "Body"
export_as hook-fine.stl "the Body, 0.01"
measure hook-fine.stl
import_file hook-fine.stl "the fine STL"
M3=$(objname hook-fine); echo "mesh3 $M3" >> "$O/objects.txt"
hide "$M1" "the mesh hook"
pick "$M3" "the mesh hook-fine"
sl_mark "Mesh Info: hook-fine"; sl_nap 3.0
sl_shot "$O/s13-fineinfo.png"
xdotool mousemove 1500 1300; sl_key v "key V"; sl_key 7 "key 7: flat lines (fine)"; sl_nap 1.0
sl_key 6 "key 6: the back (fine)"; sl_nap 0.6; sl_key v "key V"; sl_key f "key F (fit all, fine)"; sl_nap 2.0
read -r HX HY < <(python3 -m lab.fcrpc vp 0 -15 15 2>>"$O/lab-query.err")
sl_glide "$HX" "$HY" 25; sl_nap 0.5
for i in $(seq 1 16); do xdotool click 4; sleep 0.3; done
sl_glide $((HX + 700)) $((HY + 500)) 20
sl_mark "the hole zoomed (hook-fine, 229 sides)"; sl_nap 4.0
sl_shot "$O/s14-hole229.png"
sl_mark "recording stopped"
sl_stop
python3 -m lab.fcrpc docs > "$O/docs.json" 2>&1
fc_quit; sl_display_stop
for f in "$O"/mesh-*.json; do python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d['file'], d['triangles'], d['volume_mm3'], d['closed'], d['parts'], [(h['sides'], h['flat_d']) for h in d['holes']])" "$f"; done
cat "$O/objects.txt" "$O/evaluate-rows.txt"
echo "hand take done"
