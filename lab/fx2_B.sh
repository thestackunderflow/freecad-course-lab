#!/bin/bash
# fx2 take B (LAB-fx2 section 3): PrusaSlicer 2.9.2 opens the washer STL: the dialog, No, Yes, Reload from disk.
#   MSYS_NO_PATHCONV=1 docker run --rm --name fx2-B --network none --shm-size 1g --memory 4g -v <lab>:/lab fcc-slicer:2.9.2 bash /lab/lab/fx2_B.sh
set -u
O=/lab/out/fx2/B; rm -rf "$O"; mkdir -p "$O"
. /lab/lab/fx2_head_ps.sh
cp /lab/out/fx2/A/washer.stl ~/fx2/
prusa-slicer --help 2>&1 | head -n 3 | tee "$O/prusaslicer-version.txt"
ps_start
sl_record "$O"
sl_mark "recording started: PrusaSlicer 2.9.2"
sl_mark "PrusaSlicer: empty bed"; sl_nap 3
ps_open /home/maker/fx2/washer.stl washer
sl_mark "washer.stl: dropped"; sl_mark "dialog: shown"
sl_shot "$O/s-dialog.png"; sl_nap 15
ps_dialog_click No
ps_select
sl_mark "size boxes: shown"; sl_shot "$O/s-size-no.png"; sl_nap 10
sl_key Delete "Delete: the object"; sl_mark "object: deleted"; sl_nap 1.5
ps_open /home/maker/fx2/washer.stl washer
sl_mark "washer.stl: opened"; sl_mark "dialog: shown"; sl_nap 3
ps_dialog_click No
ps_select; sl_mark "size boxes: shown"; sl_nap 6
sl_key Delete "Delete: the object"; sl_mark "object: deleted"; sl_nap 1.5
ps_open /home/maker/fx2/washer.stl washer
sl_mark "washer.stl: opened again"; sl_mark "dialog: shown"; sl_nap 3
ps_dialog_click Yes
ps_select
sl_mark "size boxes: shown (x 25.4)"; sl_shot "$O/s-size-yes.png"; sl_nap 10
# right-click the ring (the part is big after Yes)
sl_click 763 1008 "the object (to select it)"; sl_nap 1
sl_click 763 1008 "right-click the object" 3; sl_nap 2
sl_mark "right-click menu: shown"; sl_shot "$O/s-menu.png"; sl_nap 4
sl_glide 932 431 20; sl_nap 0.6; sl_mark "Reload from disk: clicked"; sl_click 932 431 "Reload from disk"; sl_nap 4
sl_shot "$O/s-after-reload.png"; sl_mark "after reload: looked"; sl_nap 4
ps_select; sl_shot "$O/s-size-after-reload.png"; sl_nap 3
sl_click 763 1008 "right-click the object (again)" 3; sl_nap 2; sl_shot "$O/s-menu2.png"
sl_glide 1060 539 20; sl_nap 0.6; sl_mark "Revert conversion from imperial units: clicked"; sl_click 1060 539 "Revert conversion"; sl_nap 4
ps_select; sl_shot "$O/s-size-after-revert.png"; sl_nap 3
sl_key Delete "Delete: the object"; sl_mark "object: deleted"; sl_nap 1.5
sl_click 300 1500 "the 3D view"; sl_key ctrl+i "Import: Ctrl+I (your turn)"; sl_nap 3
sl_mark "your turn: file dialog opened live"; sl_shot "$O/s-filedialog.png"; sl_nap 25
sl_key Escape "Escape"; sl_nap 1.5
sl_mark "PrusaSlicer: window hold"; sl_nap 20
sl_mark "recording stopped"; sl_stop
kill "$SL_APP" 2>/dev/null; sl_display_stop
echo "take B done"
