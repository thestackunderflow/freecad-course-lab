#!/bin/bash
# Take "hand" (F16-F18, F25, F27; lab Q7, Q3 Stop): the back plate by hand at a person's pace. FreeCAD 1.1.4 with the
# add-on in Mod and its socket on (Auto-Start Server), the Python console open (F10 filmed opening it).
# File, New Document; the workbench list, Part; Cube; Cube clicked in the tree; Length 5, Width 20, Height 60 typed in
# the Property view; Fit all; the block clicked in the tree; the console line; the navigation cube's FRONT face, then
# its corner; the workbench list, MCP Addon; Stop RPC Server; the status bar. After the recording (not filmed): the
# socket on again, a copy of the document saved and measured with freecadcmd (checker/measure.py).
#   tools/run.sh lab/take_hand.sh
set -u
. /lab/lab/common.sh
O=/lab/out/l1/hand; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
sl_display $W $H
fc_start "$O/app.log" 1.8; sleep 7
# not filmed: open the Python console (View, Panels, Python Console on the start page)
xdotool mousemove 211 36 click 1; sleep 1; xdotool mousemove 255 1043; sleep 1; xdotool mousemove 700 1043; sleep 0.3
xdotool mousemove 800 1162 click 1; sleep 1.5
xdotool mousemove 1500 700
sl_record "$O"
sl_mark "recording started: FreeCAD, start page, console open"
sl_nap 1.5
sl_click 45 36 "File menu"
sl_click 143 76 "File: New Document"
sl_nap 1.5
sl_click 677 88 "workbench list"
sl_nap 0.8
sl_click 590 377 "workbench: Part"
sl_nap 1.5
sl_glide 49 228 24; sl_mark "hover: Cube"; sl_nap 1.2
sl_click 49 228 "Cube button"
sl_nap 2.5
sl_click 144 341 "tree: Cube"
sl_nap 2.5
sl_click 317 1099 "Property: Length"
sl_key ctrl+a; sl_type "5" "Length: typed 5" 200; sl_key Return "Length: Enter"
sl_nap 1.2
sl_click 317 1133 "Property: Width"
sl_key ctrl+a; sl_type "20" "Width: typed 20" 200; sl_key Return "Width: Enter"
sl_nap 1.2
sl_click 317 1167 "Property: Height"
sl_key ctrl+a; sl_type "60" "Height: typed 60" 200; sl_key Return "Height: Enter"
sl_nap 1.5
sl_click 942 88 "Fit all"
sl_nap 2.5
sl_shot "$O/s1-block.png"
sl_click 144 341 "tree: the block"
sl_nap 1.5
sl_click 900 1722 "console: click"
sl_type "Gui.Selection.getSelection()[0].Shape.Volume" "console: typed the volume line" 85
sl_key Return "console: Enter"
sl_nap 4
sl_shot "$O/s2-volume.png"
sl_click 2794 418 "navigation cube: RIGHT"
sl_nap 4
sl_shot "$O/s3-right.png"
sl_glide 1700 900 20; sl_key 0 "key 0: isometric"
sl_nap 3
sl_click 677 88 "workbench list 2"
sl_nap 0.8
sl_click 629 218 "workbench: MCP Addon"
sl_nap 2
SL_HOLD=0 sl_click 338 218 "Stop RPC Server"
sl_shot "$O/s4-stopped.png"
sl_nap 4
sl_mark "recording stopped"
sl_stop
convert "$O/s4-stopped.png" -crop 1600x60+0+1740 "$O/statusbar-stop.png" 2>/dev/null
# not filmed: the socket on again (the toolbar button), then save a copy and measure it
xdotool mousemove 126 218 click 1; sleep 2
python3 -m lab.fcrpc docs > "$O/docs.json" 2>&1
python3 -m lab.fcrpc save Unnamed /tmp/hand.FCStd > "$O/save.txt" 2>&1
cp /tmp/hand.FCStd "$O/hand.FCStd"
FC_DOC=/tmp/hand.FCStd FC_OUT="$O/measure.json" freecadcmd /lab/checker/measure.py > "$O/measure.log" 2>&1
fc_quit; sl_display_stop
echo "hand take done"; cat "$O/measure.json"
