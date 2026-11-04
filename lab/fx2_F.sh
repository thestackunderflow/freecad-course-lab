#!/bin/bash
# fx2 take F, PrusaSlicer half (LAB-fx2): the 27 mm3 cube opens with no dialog; Import STL (Imperial Units) converts it anyway;
# the Export menu entry; tiny.stl (8 mm3) asks.
set -u
. /lab/lab/fx2_head_ps.sh
O=/lab/out/fx2/F; mkdir -p "$O"
cp /lab/out/fx2/F/fc/cube3.stl ~/fx2/
ps_start
sl_record "$O"; sl_mark "recording started: PrusaSlicer 2.9.2"; sl_nap 2
ps_open /home/maker/fx2/cube3.stl cube3
sl_nap 3; sl_shot "$O/s-plain-open.png"
sl_mark "cube3.stl: opened, no dialog"; sl_nap 2
ps_select; sl_shot "$O/s-size-plain.png"; sl_nap 6
sl_key Delete "Delete: the object"; sl_nap 2
menu_file() { sl_click 36 49 "File menu"; sl_nap 0.8; sl_glide "$1" "$2" 12; sl_nap 1.2; }
menu_file 96 374
sl_mark "Import menu: shown"; sl_shot "$O/s-import-menu.png"; sl_nap 8
sl_glide 792 428 15; sl_nap 0.8; sl_mark "Import STL (Imperial Units): clicked"; sl_click 792 428 "Import STL (Imperial Units)"; sl_nap 3
sl_type "/home/maker/fx2/cube3.stl" "Import: typed cube3.stl" 80; sl_nap 0.8; sl_key Return "Import: Enter"; sl_nap 4
sl_shot "$O/s-after-imperial.png"
ps_select; sl_mark "size boxes: shown (imperial import)"; sl_shot "$O/s-size-imperial.png"; sl_nap 8
menu_file 95 428
sl_mark "Export menu: shown"; sl_shot "$O/s-export-menu.png"; sl_nap 8
sl_key Escape "close menu"; sl_nap 0.5; sl_key Escape "close menu"; sl_nap 1
# scale to 2.6316 percent (lock on: one field sets all three)
sl_click 2249 939 "Scale factor X"; xdotool key ctrl+a; sl_type "2.6316" "Scale: typed 2.6316" 120; sl_key Tab "Tab"; sl_nap 2
sl_shot "$O/s-size-scaled.png"
menu_file 95 428
sl_glide 782 592 15; sl_nap 0.8; sl_click 782 592 "Export Plate as STL/OBJ"; sl_nap 3
sl_shot "$O/s-export-dialog.png"
sl_type "/home/maker/fx2/tiny.stl" "Export: typed tiny.stl" 80; sl_nap 0.8; sl_key Return "Export: Enter"; sl_nap 4
sl_shot "$O/s-export-done.png"
sl_mark "Export Plate as STL/OBJ: done"
sl_click 300 1500 "the 3D view"; sl_key ctrl+a "Ctrl+A"; sl_key Delete "Delete: the object"; sl_nap 2
ps_open /home/maker/fx2/tiny.stl tiny
sl_mark "tiny.stl: opened"; sl_nap 4; sl_shot "$O/s-tiny-open.png"; sl_nap 4
cp ~/fx2/tiny.stl "$O/" 2>/dev/null
sl_stop; kill "$SL_APP" 2>/dev/null; sl_display_stop; echo "take F ps done"
