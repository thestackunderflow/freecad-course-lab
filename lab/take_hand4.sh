#!/bin/bash
# Lesson 4 take "hand" (PLAN-L4 by-hand frames; lab L4-Q1, L4-Q2, L4-Q7): lesson 3's hook as lesson 3 left it
# (hook-lesson3.FCStd = lesson 3's by-hand back5: hook_depth 40, thickness 5) gets two names (hole_d, hole_spacing), a
# sketch on the back face with two circles placed by rules from the names, a Hole through all with Diameter = hole_d,
# and a 2 mm fillet on the lip's top outer edge; then width 20 -> 30 in the sheet, and the hole sketch opened to read
# its across distance. FreeCAD 1.1.4 with the add-on in Mod and its socket on (Auto-Start Server), Part Design.
# Filmed: File, Open; the volume line (10000.0); the sheet (double-click); rows 6-7 with aliases; the hook's tab; Part
# Design from the workbench list; key 6; the back face clicked; Create sketch; G C, two circles, 4; L / I with "="
# rules; Fully constrained; Close; Hole, Diameter = hole_d, Through all, OK; key 0; the lip edge; Fillet, 2, OK; the
# volume line (9857.17); Windows, Tile; width 30 mm; key 6 in the hook; the volume line; the hole sketch opened (its
# across distance, 15 mm); Close.
# Not filmed (logged "lab query" events): a copy saved and measured after the holes, after the fillet, after width 30.
#   FCC_PREFIX=fc4 tools/run.sh lab/take_hand4.sh
set -u
. /lab/lab/common.sh
O=/lab/out/l4/hand; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
cp /lab/out/l3/hand/back5.FCStd ~/hook-lesson3.FCStd
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
sleep 2
DOC=hook_lesson3
xdotool mousemove 1500 700
B() { python3 -m lab.button "$@" 2>>"$O/lab-query.err"; }
console() {   # console "line" LABEL
  local cx cy; read -r cx cy < <(B console)
  sl_click "$cx" "$cy" "console: click"
  sl_type "$1" "console: typed $2" 70
  sl_key Return "console: Enter ($2)"
  sl_nap 3.5
}
row() { python3 -m lab.fcrpc row "$DOC" "$1" 2>>"$O/lab-query.err"; }
open_to() {   # open the tree's closed rows above OBJ (clicks, as a person)
  local ax ay i
  for i in 1 2 3; do
    read -r ax ay < <(python3 -m lab.fcrpc arrow "$DOC" "$1" 2>>"$O/lab-query.err")
    { [ "${ax:-}" = open ] || [ "${ax:-}" = none ] || [ -z "${ay:-}" ]; } && return 0
    sl_click "$ax" "$ay" "tree: open a row"; sl_nap 0.6
  done
}
dbl() { sl_glide "$1" "$2" 20; sl_nap 0.5; sl_mark "$3"; xdotool click --repeat 2 --delay 120 1; }
SP() { python3 -m lab.sketchpt "$DOC" Sketch001 "$@" 2>>"$O/lab-query.err"; }
VP() { python3 -m lab.fcrpc vp "$@" 2>>"$O/lab-query.err"; }
snap() {
  sl_mark "lab query: save $1"
  python3 -m lab.fcrpc save "$DOC" "/tmp/$1.FCStd" > "$O/save-$1.txt" 2>&1 && cp "/tmp/$1.FCStd" "$O/$1.FCStd"
  FC_DOC="/tmp/$1.FCStd" FC_OUT="$O/measure-$1.json" freecadcmd /lab/checker/measure.py > "$O/measure-$1.log" 2>&1
}
expr_enter() {   # expr_enter "expression" LABEL: "=", the expression, Enter (list), Enter (editor OK), Enter (dialog OK)
  sl_type "=" "$2: typed =" 150
  sl_nap 1.4
  sl_type "$1" "editor: typed $1" 95
  sl_nap 1.5
  sl_key Return "editor: Enter (the list)"
  sl_nap 1.0
  sl_key Return "editor: Enter (OK)"
  sl_nap 1.0
  sl_key Return "$2: Enter (OK)"
  sl_nap 1.8
}
sl_record "$O"
sl_mark "recording started: FreeCAD, Part Design"
sl_nap 1.5
# F4: File, Open, the start file; the volume line
sl_click 45 36 "File menu"
sl_glide 160 110 15; sl_nap 0.4
sl_click 160 110 "File: Open"
sl_nap 2.0
sl_type "~/hook-lesson3.FCStd" "open: typed the file name" 90
sl_nap 0.6
sl_key Return "open: Enter"
sl_nap 3.0
xdotool mousemove 1500 1200; sl_key 0 "key 0: isometric"; sl_nap 1.5
open_to Pad
read -r PX PY < <(row Pad)
sl_click "$PX" "$PY" "tree: Pad"
sl_nap 1.0
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line (lesson 3's hook)"
sl_shot "$O/s1-opened.png"
# F5: the sheet; rows 6-7
read -r SX SY < <(row Spreadsheet)
dbl "$SX" "$SY" "tree: double-click Spreadsheet"
sl_nap 3.0
sl_shot "$O/s2-sheet.png"
n=5
for r in "hole_d 4" "hole_spacing 30"; do
  set -- $r; n=$((n + 1)); y=$((410 + (n - 1) * 54))
  read -r AX AY < <(B cell $((n - 1)) 0); read -r BX BY < <(B cell $((n - 1)) 1)
  sl_click "$AX" "$AY" "cell A$n"
  sl_type "$1" "A$n: typed $1" 110
  sl_key Return "A$n: Enter"
  sl_nap 0.6
  sl_click "$BX" "$BY" "cell B$n"
  sl_type "$2 mm" "B$n: typed $2 mm" 130
  sl_key Return "B$n: Enter"
  sl_nap 0.6
  sl_click "$BX" "$BY" "cell B$n again"
  sl_glide 2590 300 20; sl_nap 0.4
  sl_click 2590 300 "Alias box"
  sl_type "$1" "alias B$n: typed $1" 110
  sl_key Return "alias B$n: Enter"
  sl_nap 1.2
done
read -r EX2 EY2 < <(B cell 12 3); sl_click "$EX2" "$EY2" "an empty cell"
sl_mark "the sheet with seven names"; sl_nap 3.5
sl_shot "$O/s3-sheet7.png"
# F6: the hook's tab; Part Design; key 6; the back face
read -r TX TY < <(B tab hook)
sl_click "$TX" "$TY" "tab: the hook"
sl_nap 1.5
sl_click 700 88 "workbench list"
sl_nap 1.2
sl_glide 629 337 20; sl_mark "hover: Part Design"; sl_nap 0.6
sl_click 629 337 "workbench: Part Design"
sl_nap 2.0
xdotool mousemove 1500 1300; sl_key 6 "key 6: view from the left (the back)"; sl_nap 0.8
sl_key v "key V"; sl_key f "key F (fit all)"; sl_nap 2.0
read -r FX FY < <(VP 0 -10 30)
sl_glide "$FX" "$FY" 25; sl_nap 0.6
sl_click "$FX" "$FY" "the back face"
sl_nap 1.5
sl_shot "$O/s4-back-face.png"
# F7: Create sketch
read -r KX KY < <(B PartDesign_CompSketches)
sl_glide "$KX" "$KY" 20; sl_mark "hover: Create sketch"; sl_nap 1.5
sl_click "$KX" "$KY" "Create sketch"
sl_nap 3.0
read -r OX OY < <(VP 0 0 0)
sl_glide "$OX" "$OY" 25; sl_mark "hover: the sketch's origin corner"; sl_nap 2.0
sl_shot "$O/s5-sketch.png"
# F8: two circles
xdotool mousemove 1400 1300; sl_nap 0.3
sl_key g "key G"; sl_key c "key C (circle)"
sl_nap 1.0
n=0
for p in "9.2 14.1" "10.7 45.8"; do
  set -- $p; n=$((n + 1))
  read -r CX CY < <(VP 0 -$1 $2)
  sl_glide "$CX" "$CY" 25; sl_nap 0.5
  sl_click "$CX" "$CY" "circle $n: centre"
  sl_glide $((CX + 110)) $((CY - 110)) 12; sl_nap 1.0   # the size label lands here, away from the centre (it would take the centre click)
  sl_type "4" "circle $n: typed 4" 250
  sl_key Return "circle $n: Enter (4)"
  sl_nap 1.5
done
sl_key Escape "Esc: circle tool off"
sl_nap 1.2
sl_shot "$O/s6-circles.png"
# F10-F12: the rules
rule() {   # rule GEO KEY "expression" LABEL
  local x y
  read -r x y < <(SP "$1" center)
  sl_glide "$x" "$y" 20; sl_nap 0.5
  sl_click "$x" "$y" "$4: the centre point"
  sl_nap 0.8
  sl_key "$2" "key ${2^^}: $4"
  sl_nap 1.6
  expr_enter "$3" "$4"
  python3 -c "import sys; sys.path.insert(0, '/lab'); from lab import fcrpc; print('$4:', fcrpc.run('import FreeCAD\nsk = FreeCAD.getDocument(\'hook_lesson3\').getObject(\'Sketch001\')\nprint([(c.Type, round(c.Value, 3)) for c in sk.Constraints])'))" >> "$O/rules.txt" 2>&1
}
rule 0 l "Spreadsheet.width / 2" "lower across"
sl_shot "$O/s7-across.png"
rule 0 i "(Spreadsheet.plate_height - Spreadsheet.hole_spacing) / 2" "lower up"
sl_shot "$O/s8-up.png"
rule 1 l "Spreadsheet.width / 2" "upper across"
rule 1 i "(Spreadsheet.plate_height + Spreadsheet.hole_spacing) / 2" "upper up"
sl_glide 2440 754 25; sl_mark "hover: Fully constrained"; sl_nap 3.0
sl_shot "$O/s9-fully.png"
python3 - > "$O/sketch-check.txt" 2>&1 <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCAD
sk = FreeCAD.getDocument('hook_lesson3').getObject('Sketch001')
print([(c.Type, round(c.Value, 4)) for c in sk.Constraints], dict(sk.ExpressionEngine), sk.FullyConstrained)"""))
PY
sl_mark "lab query: the sketch's sizes read back"
sl_click 2528 616 "Close"
sl_nap 2.5
# F13: Hole
read -r RX RY < <(row Sketch001)
sl_click "$RX" "$RY" "tree: the hole sketch"
sl_nap 1.0
read -r HX HY < <(B PartDesign_Hole)
sl_glide "$HX" "$HY" 20; sl_mark "hover: Hole"; sl_nap 1.8
sl_click "$HX" "$HY" "Hole"
sl_nap 3.0
sl_shot "$O/s10-hole-panel.png"
sl_click 2671 1135 "Hole: Diameter box"
xdotool key ctrl+a
sl_type "=" "Diameter: typed =" 150
sl_nap 1.4
sl_type "Spreadsheet.hole_d" "editor: typed Spreadsheet.hole_d" 105
sl_nap 1.2
sl_key Return "editor: Enter (the list)"
sl_nap 1.0
sl_key Return "editor: Enter (OK)"
sl_nap 1.5
sl_click 2650 933 "Hole: Depth type list"
sl_nap 1.2
sl_glide 2592 972 15; sl_nap 0.4
sl_click 2592 972 "Depth type: Through all"
sl_nap 1.5
sl_shot "$O/s11-hole-set.png"
sl_click 2426 616 "Hole: OK"
sl_nap 3.0
xdotool mousemove 1500 1300; sl_key 0 "key 0: isometric"; sl_nap 0.6
sl_key v "key V"; sl_key f "key F (fit all)"; sl_nap 2.5
sl_shot "$O/s12-holes.png"
snap holes
# F15: the fillet
read -r EX EY < <(VP 40 -10 10)
sl_glide "$EX" "$EY" 25; sl_mark "hover: the lip's top outer edge"; sl_nap 1.2
sl_click "$EX" "$EY" "the lip's top outer edge"
sl_nap 1.2
read -r LX LY < <(B PartDesign_Fillet)
sl_glide "$LX" "$LY" 20; sl_mark "hover: Fillet"; sl_nap 1.5
sl_click "$LX" "$LY" "Fillet"
sl_nap 3.0
sl_shot "$O/s13-fillet-panel.png"
sl_type "2" "Radius: typed 2" 250
sl_nap 1.5
sl_click 2426 616 "Fillet: OK"
sl_nap 3.0
sl_glide "$EX" "$EY" 25; sl_mark "hover: the rounded lip"; sl_nap 2.0
sl_shot "$O/s14-fillet.png"
# F16: the volume line
open_to Fillet
read -r PX PY < <(row Fillet)
sl_click "$PX" "$PY" "tree: Fillet"
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line (holes and fillet)"
sl_shot "$O/s15-volume.png"
snap fillet
# F17: Windows, Tile; width 30
read -r MX MY < <(B menu Windows)   # its place depends on the workbench's menus
sl_click "$MX" "$MY" "Windows menu"
sl_glide $((MX + 5)) 165 15; sl_nap 0.5
sl_click $((MX + 5)) 165 "Windows: Tile"
sl_nap 2.5
sl_shot "$O/s16-tiled.png"
read -r EX2 EY2 < <(B cell 12 3); sl_click "$EX2" "$EY2" "the sheet: an empty cell (the window takes the keys)"
sl_nap 0.8
read -r WX WY < <(B cell 4 1); sl_click "$WX" "$WY" "cell B5 (width)"
sl_nap 0.8
sl_type "30 mm" "B5: typed 30 mm" 160
sl_key Return "B5: Enter (30 mm)"
sl_nap 3.5
sl_shot "$O/s17-width30.png"
read -r VX VY < <(B view); sl_click "$VX" "$VY" "the hook's window: an empty spot"
sl_nap 0.5
sl_key 6 "key 6: the back, 30 wide"; sl_nap 0.6
sl_key v "key V"; sl_key f "key F (fit all)"; sl_nap 2.5
sl_shot "$O/s18-back30.png"
read -r PX PY < <(row Fillet)
sl_click "$PX" "$PY" "tree: Fillet"
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line (30 wide)"
sl_shot "$O/s19-volume30.png"
snap width30
# the hole sketch opened: its across distance reads 15
open_to Sketch001
read -r RX RY < <(row Sketch001)
dbl "$RX" "$RY" "tree: double-click the hole sketch"
sl_nap 3.5
read -r X0 Y0 < <(SP 0 center); sl_glide "$X0" "$Y0" 20; sl_mark "hover: the lower hole's centre"; sl_nap 3.0
sl_shot "$O/s20-sketch30.png"
sl_click 2528 616 "Close (the hole sketch)"
sl_nap 2.0
sl_mark "recording stopped"
sl_stop
python3 -m lab.fcrpc docs > "$O/docs.json" 2>&1
fc_quit; sl_display_stop
for s in holes fillet width30; do
  python3 -c "
import json, sys; sys.path.insert(0, '/lab')
from checker import holes, score_l4
m = json.load(open('$O/measure-$s.json'))
w = 30 if '$s' == 'width30' else 20
print(json.dumps(holes.check(score_l4._part(m), dict(holes.NAMES, width=w)), indent=1))" > "$O/check-$s.json" 2>&1
done
echo "hand take done"; cat "$O/check-width30.json"
