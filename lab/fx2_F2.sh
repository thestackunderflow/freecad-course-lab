#!/bin/bash
# fx2 take F part 2: scale the imperial-imported cube to 2 x 2 x 2, Export Plate as STL/OBJ (tiny.stl), open it: does it ask?
set -u
. /lab/lab/fx2_head_ps.sh
O=/lab/out/fx2/F/tiny; mkdir -p "$O"
cp /lab/out/fx2/F/fc/cube3.stl ~/fx2/
ps_start
sl_record "$O"; sl_mark "recording started: PrusaSlicer 2.9.2"; sl_nap 2
sl_click 36 49 "File menu"; sl_nap 0.8; sl_glide 96 374 12; sl_nap 1.2
sl_glide 792 428 15; sl_nap 0.8; sl_click 792 428 "Import STL (Imperial Units)"; sl_nap 3
sl_type "/home/maker/fx2/cube3.stl" "Import: typed cube3.stl" 80; sl_nap 0.8; sl_key Return "Import: Enter"; sl_nap 4
ps_select; sl_nap 1
sl_shot "$O/s-before-scale.png"
sl_glide 2249 939 15; sl_nap 0.4; xdotool click --repeat 3 --delay 80 1; sl_nap 0.8
sl_type "2.6316" "Scale: typed 2.6316" 120; sl_nap 0.5; sl_key Return "Scale: Enter"; sl_nap 2.5
sl_shot "$O/s-size-scaled.png"; sl_mark "size boxes: shown (scaled)"; sl_nap 5
sl_click 36 49 "File menu"; sl_nap 0.8; sl_glide 95 428 12; sl_nap 1.2
sl_glide 782 592 15; sl_nap 0.8; sl_mark "Export Plate as STL/OBJ: clicked"; sl_click 782 592 "Export Plate as STL/OBJ"; sl_nap 3
sl_shot "$O/s-export-dialog.png"
sl_type "/home/maker/fx2/tiny.stl" "Export: typed tiny.stl" 80; sl_nap 0.8; sl_key Return "Export: Enter"; sl_nap 4
sl_shot "$O/s-export-done.png"; sl_mark "Export Plate as STL/OBJ: done"
ls -l ~/fx2 | tee "$O/ls-fx2.txt"
sl_click 300 1500 "the 3D view"; sl_key ctrl+a "Ctrl+A"; sl_key Delete "Delete: the object"; sl_nap 2
ps_open /home/maker/fx2/tiny.stl tiny
sl_mark "tiny.stl: opened"; sl_nap 4; sl_shot "$O/s-tiny-open.png"; sl_nap 4
cp ~/fx2/tiny.stl* "$O/" 2>/dev/null
sl_stop; kill "$SL_APP" 2>/dev/null; sl_display_stop; echo "take F2 done"
