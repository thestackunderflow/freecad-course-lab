#!/bin/bash
# Lesson 3 take "hand" (PLAN-L3 by-hand frames; lab L3-Q1, L3-Q2): lesson 2's hook gets a spreadsheet of five named
# sizes, its six sizes and its pad written from them, then one cell at a time changes the part. FreeCAD 1.1.4 with
# the add-on in Mod and its socket on (Auto-Start Server), in Part Design, as a viewer leaves lesson 2; lesson 2's
# saved hook is in the home folder as hook-lesson2.FCStd (the course's start file).
# Filmed: File, Open, the start file; the volume line (8500.0); the workbench list, Spreadsheet; Create spreadsheet;
# rows 1-5 (name in A, value with mm in B, B's alias); the finished sheet held; the hook's tab; the sketch opened
# (double-click), zoomed out one notch; each size lit, then double-clicked: "=", Spreadsheet.<name>, Enter (the
# list), Enter (the editor's OK), Enter (Insert Length's OK); "Fully constrained"; Close; Pad double-clicked, Length
# "=" Spreadsheet.width, OK; the volume line again (8500.0); Windows, Tile; hook_depth's cell 40 mm; the volume and X
# lines; thickness's cell 8 mm; the volume line; thickness back to 5 mm.
# Not filmed (logged "lab query" events): a copy saved and measured after binding, after 40, after 8, after 5.
#   tools/run.sh lab/take_hand3.sh
set -u
. /lab/lab/common.sh
O=/lab/out/l3/hand; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
cp /lab/out/l2/hand/hand.FCStd ~/hook-lesson2.FCStd
sl_display $W $H
fc_start "$O/app.log" 1.8; sleep 8
cd /lab
python3 - > "$O/setup-rpc.txt" 2>&1 <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run("""import FreeCADGui
from PySide import QtWidgets
FreeCADGui.activateWorkbench('PartDesignWorkbench')
for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
    if w.objectName() in ('Python console',):
        w.show()
print(1)"""))
PY
sleep 2
DOC=hook_lesson2
xdotool mousemove 1500 700
console() {   # console "line" LABEL
  sl_click 900 1722 "console: click"
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
snap() {
  sl_mark "lab query: save $1"
  python3 -m lab.fcrpc save "$DOC" "/tmp/$1.FCStd" > "$O/save-$1.txt" 2>&1 && cp "/tmp/$1.FCStd" "$O/$1.FCStd"
  FC_DOC="/tmp/$1.FCStd" FC_OUT="$O/measure-$1.json" freecadcmd /lab/checker/measure.py > "$O/measure-$1.log" 2>&1
}
sl_record "$O"
sl_mark "recording started: FreeCAD, Part Design, Start page"
sl_nap 1.5
# F2: File, Open, the start file
sl_click 45 36 "File menu"
sl_glide 160 110 15; sl_nap 0.4
sl_click 160 110 "File: Open"
sl_nap 2.0
sl_shot "$O/s0-open-dialog.png"
sl_type "~/hook-lesson2.FCStd" "open: typed the file name" 90
sl_nap 0.6
sl_key Return "open: Enter"
sl_nap 3.0
xdotool mousemove 1500 1200; sl_key 0 "key 0: isometric"; sl_nap 1.5
open_to Pad
read -r PX PY < <(row Pad); echo "pad $PX $PY" > "$O/rows.txt"
sl_click "$PX" "$PY" "tree: Pad"
sl_nap 1.0
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line (lesson 2's hook)"
sl_shot "$O/s1-opened.png"
# F4: the workbench list, Spreadsheet; Create spreadsheet
sl_click 700 88 "workbench list"
sl_nap 1.2
sl_glide 636 536 20; sl_mark "hover: Spreadsheet"; sl_nap 0.8
sl_click 636 536 "workbench: Spreadsheet"
sl_nap 2.0
sl_glide 48 228 20; sl_mark "hover: Create spreadsheet"; sl_nap 1.5
sl_click 48 228 "Create spreadsheet"
sl_nap 2.5
sl_shot "$O/s2-sheet.png"
# F5-F7: rows 1-5: a name in A, a value with mm in B, B's alias
n=0
for r in "hook_depth 25" "thickness 5" "lip_height 10" "plate_height 60" "width 20"; do
  set -- $r; n=$((n + 1)); y=$((410 + (n - 1) * 54))
  sl_click 676 $y "cell A$n"
  sl_type "$1" "A$n: typed $1" 110
  sl_key Return "A$n: Enter"
  sl_nap 0.6
  sl_click 856 $y "cell B$n"
  sl_type "$2 mm" "B$n: typed $2 mm" 130
  sl_key Return "B$n: Enter"
  sl_nap 0.6
  sl_click 856 $y "cell B$n again"
  sl_glide 2590 300 20; sl_nap 0.4
  sl_click 2590 300 "Alias box"
  sl_type "$1" "alias B$n: typed $1" 110
  sl_key Return "alias B$n: Enter"
  sl_nap 1.2
  [ $n -eq 1 ] && sl_shot "$O/s3-row1.png"
done
sl_click 1300 1200 "an empty cell"
sl_mark "the finished sheet"; sl_nap 4.5
sl_shot "$O/s4-sheet-done.png"
# F8: the hook's tab; the sketch opened; one notch out
sl_click 580 1734 "tab: the hook"
sl_nap 1.5
open_to Sketch
read -r KX KY < <(row Sketch)
sl_glide "$KX" "$KY" 20; sl_nap 0.5
sl_mark "tree: double-click the sketch"; xdotool click --repeat 2 --delay 120 1
sl_nap 3.5
xdotool mousemove 1300 900; sl_nap 0.3; xdotool click 5; sl_mark "zoom: one notch out"
sl_nap 1.5
sl_shot "$O/s5-sketch.png"
# each size lit (hover) in the order the narration says them, then bound
python3 -m lab.dimpt "$DOC" Sketch list > "$O/dims.txt" 2>&1
read -r -a P < <(python3 -m lab.dimpt "$DOC" Sketch 17 18 19 20 21 22 | tr '\n' ' ')
echo "${P[*]}" > "$O/dim-points.txt"
LABELS=("25 bottom" "10 lip height" "5 lip width" "5 drop inside the lip" "60 back plate" "5 back plate thickness")
for i in 0 1 2 3 4 5; do
  sl_glide "${P[$((i * 2))]}" "${P[$((i * 2 + 1))]}" 18; sl_mark "hover size: ${LABELS[$i]}"; sl_nap 1.2
done
EXPR=("Spreadsheet.hook_depth" "Spreadsheet.lip_height" "Spreadsheet.thickness" "Spreadsheet.lip_height - Spreadsheet.thickness" "Spreadsheet.plate_height" "Spreadsheet.thickness")
for i in 0 1 2 3 4 5; do
  x=${P[$((i * 2))]}; y=${P[$((i * 2 + 1))]}
  sl_glide "$x" "$y" 20; sl_mark "hover size: ${LABELS[$i]}"; sl_nap 0.8
  sl_mark "double-click size: ${LABELS[$i]}"; xdotool click --repeat 2 --delay 120 1
  sl_nap 1.6
  [ $i -eq 0 ] && sl_shot "$O/s6-insert-length.png"
  sl_type "=" "Insert Length: typed =" 150
  sl_nap 1.4
  [ $i -eq 0 ] && sl_shot "$O/s7-editor.png"
  sl_type "${EXPR[$i]}" "editor: typed ${EXPR[$i]}" 105
  sl_nap 1.2
  [ $i -eq 0 ] && sl_shot "$O/s8-completion.png"
  sl_key Return "editor: Enter (pick from the list)"
  sl_nap 1.0
  [ $i -eq 0 ] && sl_shot "$O/s9-result.png"
  sl_key Return "editor: Enter (OK)"
  sl_nap 1.0
  sl_key Return "Insert Length: Enter (OK)"
  sl_nap 1.8
  [ $i -eq 0 ] && sl_shot "$O/s10-bound.png"
done
sl_glide 2440 754 25; sl_mark "hover: Fully constrained"; sl_nap 3.0
sl_shot "$O/s11-all-bound.png"
sl_click 2528 616 "Close"
sl_nap 2.5
# F14: Pad's Length from width
read -r PX PY < <(row Pad)
sl_glide "$PX" "$PY" 20; sl_nap 0.5
sl_mark "tree: double-click Pad"; xdotool click --repeat 2 --delay 120 1
sl_nap 3.0
sl_click 2660 882 "Pad: Length box"
xdotool key ctrl+a
sl_type "=" "Pad Length: typed =" 150
sl_nap 1.4
sl_type "Spreadsheet.width" "editor: typed Spreadsheet.width" 105
sl_nap 1.2
sl_key Return "editor: Enter (pick from the list)"
sl_nap 1.0
sl_key Return "editor: Enter (OK)"
sl_nap 1.2
sl_shot "$O/s12-pad-width.png"
sl_click 2428 616 "Pad: OK"
sl_nap 2.5
xdotool mousemove 1500 1200; sl_key 0 "key 0: isometric"; sl_nap 1.5
read -r PX PY < <(row Pad)
sl_click "$PX" "$PY" "tree: Pad"
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line (still 8,500)"
sl_shot "$O/s13-still-8500.png"
snap named
# F16: Windows, Tile; hook_depth's cell 40 mm
sl_click 700 36 "Windows menu"
sl_glide 706 165 15; sl_nap 0.5
sl_click 706 165 "Windows: Tile"
sl_nap 2.5
sl_shot "$O/s14-tiled.png"
sl_click 2060 460 "cell B1 (hook_depth)"
sl_nap 0.8
sl_type "40 mm" "B1: typed 40 mm" 160
sl_key Return "B1: Enter (40 mm)"
sl_nap 3.5
sl_shot "$O/s15-depth40.png"
read -r PX PY < <(row Pad)
sl_click "$PX" "$PY" "tree: Pad"
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line (40 deep)"
console "b = Gui.Selection.getSelection()[0].Shape.BoundBox; round(b.XMin, 3), round(b.XMax, 3)" "the X line"
sl_shot "$O/s16-depth40-console.png"
snap depth40
# F19: thickness 8 mm; then back to 5 mm
sl_click 2060 514 "cell B2 (thickness)"
sl_nap 0.8
sl_type "8 mm" "B2: typed 8 mm" 160
sl_key Return "B2: Enter (8 mm)"
sl_nap 3.5
sl_shot "$O/s17-thick8.png"
read -r PX PY < <(row Pad)
sl_click "$PX" "$PY" "tree: Pad"
console "Gui.Selection.getSelection()[0].Shape.Volume" "the volume line (8 thick)"
sl_shot "$O/s18-thick8-console.png"
snap thick8
sl_click 2060 514 "cell B2 (thickness) again"
sl_nap 0.8
sl_type "5 mm" "B2: typed 5 mm" 160
sl_key Return "B2: Enter (5 mm)"
sl_nap 3.0
sl_shot "$O/s19-thick5.png"
sl_mark "recording stopped"
sl_stop
snap back5
python3 -m lab.fcrpc docs > "$O/docs.json" 2>&1
fc_quit; sl_display_stop
echo "hand take done"; ls "$O"/measure-*.json
