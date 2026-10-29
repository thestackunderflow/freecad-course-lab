#!/bin/bash
# Lesson 2 take "hand" (PLAN-L2 F3, F5, F6, F8-F14, F16-F18, F20; lab L2-Q1, L2-Q2): the wall hook by hand in Part
# Design at a person's pace. FreeCAD 1.1.4 with the add-on in Mod and its socket on (Auto-Start Server), in the Part
# workbench as a viewer leaves lesson 1. Filmed: File, New Document; the workbench list, Part Design; New Body; New
# Sketch, the attachment list (each plane in turn), XZ-plane, OK; the view slid down (middle drag); Polyline, the
# origin, each corner clicked roughly in place, the close; a free corner dragged (it stretches) and back; Dimension
# (D) six times with typed sizes; "Fully constrained"; the same corner dragged (it stays); Close; the sketch in the
# tree, Pad, 20, OK; key 0; the navigation cube; the tree; View, Panels, Python console; the pad clicked; the volume
# line and the height line. After the recording (not filmed): a copy saved and measured with freecadcmd.
#   tools/run.sh lab/take_hand2.sh
set -u
. /lab/lab/common.sh
O=/lab/out/l2/hand; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
sl_display $W $H
fc_start "$O/app.log" 1.8; sleep 8
cd /lab
python3 -c "
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc; print(fcrpc.run('import FreeCADGui\nFreeCADGui.activateWorkbench(\"PartWorkbench\")\nprint(1)'))" > "$O/setup-rpc.txt" 2>&1
sleep 2
xdotool mousemove 1500 700
SP() { python3 -m lab.sketchpt Unnamed Sketch "$@"; }
sl_record "$O"
sl_mark "recording started: FreeCAD, start page, Part workbench"
sl_nap 1.5
# F3: a new document; the workbench list; Part Design
sl_click 45 36 "File menu"
sl_click 143 76 "File: New Document"
sl_nap 1.5
sl_click 700 88 "workbench list"
sl_nap 1.2
sl_glide 630 338 20; sl_mark "hover: Part Design"; sl_nap 0.8
sl_click 630 338 "workbench: Part Design"
sl_nap 2.0
# F5: New Body; the tree
sl_glide 510 158 20; sl_mark "hover: New Body"; sl_nap 1.5
sl_click 510 158 "New Body"
sl_nap 1.5
sl_glide 160 342 20; sl_mark "hover: tree Body"; sl_nap 1.5
sl_click 54 374 "tree: open Origin"
sl_nap 2.5
sl_click 54 374 "tree: close Origin"
sl_nap 1.0
# F6: New Sketch; the attachment list, each plane; XZ; OK
sl_glide 570 158 20; sl_mark "hover: New Sketch"; sl_nap 1.2
sl_click 570 158 "New Sketch"
sl_nap 2.0
sl_shot "$O/s1-attach.png"
sl_glide 2340 750 20; sl_mark "hover: XY-plane"; sl_nap 2.2
sl_glide 2340 774 12; sl_mark "hover: XZ-plane"; sl_nap 2.2
sl_glide 2340 800 12; sl_mark "hover: YZ-plane"; sl_nap 2.2
sl_click 2340 774 "attachment: XZ-plane"
sl_nap 1.5
sl_click 2430 616 "attachment: OK"
sl_nap 3.0
sl_shot "$O/s2-front.png"
# slide the drawing area down to make room (middle-button drag)
sl_drag 1500 900 1350 1470 "pan: middle drag" 2
sl_nap 1.2
read -r OX OY < <(SP -1 origin)
echo "origin $OX $OY" > "$O/origin.txt"
# F8: Polyline; the origin
sl_glide 316 228 20; sl_mark "hover: Polyline"; sl_nap 1.2
sl_click 316 228 "Polyline"
sl_nap 1.0
SL_HOLD=0.9 sl_click "$OX" "$OY" "polyline: origin"
# F9: each corner roughly in place, then the close on the first point (rough mm at 17.86 px)
K=17.86
n=0
for p in "28 0 right" "28 12 up" "22 12 left" "22 6 down" "6 6 left" "6 55 up" "0 55 left"; do
  set -- $p; n=$((n + 1))
  x=$(awk -v o="$OX" -v a="$1" -v k=$K 'BEGIN{printf "%d", o + a * k}')
  y=$(awk -v o="$OY" -v a="$2" -v k=$K 'BEGIN{printf "%d", o - a * k}')
  sl_glide "$x" "$y" 30; sl_nap 0.5
  SL_HOLD=0.9 sl_click "$x" "$y" "polyline: corner $n ($3)"
done
sl_glide "$OX" "$OY" 30; sl_nap 0.5
SL_HOLD=1.2 sl_click "$OX" "$OY" "polyline: close on the first point"
sl_key Escape "Esc: tool off"
sl_nap 1.5
sl_shot "$O/s3-outline.png"
# F10-F11: the marks; the count; a free corner dragged (it stretches) and back
sl_glide 2440 754 25; sl_mark "hover: degrees of freedom"; sl_nap 3.0
read -r CX CY < <(SP 5 end)
sl_glide "$CX" "$CY" 25; sl_nap 0.6
sl_mark "drag free corner: down"; xdotool mousedown 1; sleep 0.2
for i in $(seq 1 30); do xdotool mousemove $((CX + i * 4)) $((CY - i * 2)); sleep 0.04; done
sl_mark "drag free corner: stretched"; sl_nap 1.5
sl_shot "$O/s4-stretched.png"
for i in $(seq 30 -1 0); do xdotool mousemove $((CX + i * 4)) $((CY - i * 2)); sleep 0.04; done
xdotool mouseup 1; sl_mark "drag free corner: released"
sl_nap 1.5
# F12-F13: Dimension (D), six sizes typed
xdotool mousemove 1400 1200; sl_nap 0.5
sl_key d "key D: Dimension"
sl_nap 1.0
dim() {   # dim GEO WHERE DX DY VALUE LABEL [GEO2 WHERE2]
  local x y px py
  read -r x y < <(SP "$1" "$2")
  sl_glide "$x" "$y" 25; sl_nap 0.4
  sl_click "$x" "$y" "dimension $6: pick"
  if [ -n "${7:-}" ]; then read -r x y < <(SP "$7" "$8"); sl_glide "$x" "$y" 25; sl_click "$x" "$y" "dimension $6: pick 2"; fi
  read -r px py < <(SP "$1" "$2" "$3" "$4")
  sl_glide "$px" "$py" 20; sl_nap 0.3
  sl_click "$px" "$py" "dimension $6: place"
  sl_nap 1.2
  sl_type "$5" "dimension $6: typed $5" 220
  sl_key Return "dimension $6: Enter"
  sl_nap 2.2
}
dim 0 mid 0 80 25 "bottom 25"
sl_shot "$O/s5-first-size.png"
dim 1 mid 90 0 10 "lip height 10"
dim 2 mid 0 -70 5 "lip width 5"
dim 3 mid -80 0 5 "lip inside 5"
dim 6 end -110 260 60 "back plate 60" -1 origin
dim 6 mid 0 70 5 "back plate thickness 5"
xdotool key Escape; sl_mark "Esc: Dimension off"
sl_nap 1.0
# F14: Fully constrained; the same corner dragged: it stays
sl_glide 2440 754 25; sl_mark "hover: Fully constrained"; sl_nap 3.0
sl_shot "$O/s6-fully.png"
read -r CX CY < <(SP 5 end)
sl_glide "$CX" "$CY" 25; sl_nap 0.6
sl_mark "drag pinned corner: down"; xdotool mousedown 1; sleep 0.2
for i in $(seq 1 30); do xdotool mousemove $((CX + i * 4)) $((CY - i * 2)); sleep 0.04; done
sl_mark "drag pinned corner: pulled"; sl_nap 1.5
sl_shot "$O/s7-pinned.png"
xdotool mouseup 1; sl_mark "drag pinned corner: released"
sl_nap 1.0
sl_click 2528 616 "Close"
sl_nap 2.5
# F16: the sketch in the tree; Pad; 20; OK
sl_click 180 406 "tree: Sketch"
sl_nap 1.0
sl_glide 48 228 20; sl_mark "hover: Pad"; sl_nap 1.2
sl_click 48 228 "Pad"
sl_nap 2.5
sl_shot "$O/s8-pad10.png"
sl_type "20" "Pad: typed 20" 250
sl_nap 2.0
sl_shot "$O/s9-pad20.png"
sl_click 2428 616 "Pad: OK"
sl_nap 2.0
# F17: key 0; the navigation cube
xdotool mousemove 1500 1200; sl_nap 0.4
sl_key 0 "key 0: isometric"
sl_nap 2.5
sl_shot "$O/s10-iso.png"
sl_click 2794 418 "navigation cube: RIGHT"
sl_nap 3.0
sl_glide 1500 1200 20; sl_key 0 "key 0: isometric again"
sl_nap 2.5
# F18: the tree, the recipe
sl_click 54 406 "tree: open Pad"
sl_nap 1.0
sl_glide 150 342 20; sl_mark "hover: tree Body"; sl_nap 1.5
sl_glide 176 374 15; sl_mark "hover: tree Origin"; sl_nap 1.5
sl_glide 164 406 15; sl_mark "hover: tree Pad"; sl_nap 1.5
sl_glide 200 438 15; sl_mark "hover: tree Sketch"; sl_nap 2.0
sl_shot "$O/s11-tree.png"
# F20: View, Panels, Python console; the pad clicked; the two lines
sl_click 211 36 "View menu"
sl_glide 255 1043 25; sl_mark "View: Panels"; sl_nap 0.6
sl_glide 700 1043 25; sl_nap 0.3
sl_click 800 1124 "Panels: Python console"
sl_nap 2.0
sl_click 164 406 "tree: Pad"
sl_nap 1.2
sl_click 900 1722 "console: click"
sl_type "Gui.Selection.getSelection()[0].Shape.Volume" "console: typed the volume line" 85
sl_key Return "console: Enter"
sl_nap 3.5
sl_type "b = Gui.Selection.getSelection()[0].Shape.BoundBox; round(b.ZMin, 3), round(b.ZMax, 3)" "console: typed the height line" 70
sl_key Return "console: Enter 2"
sl_nap 4.0
sl_shot "$O/s12-console.png"
sl_mark "recording stopped"
sl_stop
# not filmed: save a copy and measure it
python3 -m lab.fcrpc docs > "$O/docs.json" 2>&1
python3 -m lab.fcrpc save Unnamed /tmp/hand.FCStd > "$O/save.txt" 2>&1
cp /tmp/hand.FCStd "$O/hand.FCStd"
FC_DOC=/tmp/hand.FCStd FC_OUT="$O/measure.json" freecadcmd /lab/checker/measure.py > "$O/measure.log" 2>&1
fc_quit; sl_display_stop
echo "hand take done"; cat "$O/measure.json" | head -c 600
