#!/bin/bash
# fx2 takes C and D, PrusaSlicer halves: C = the inch-number block (Yes), D = the FreeCAD 3MF (no dialog). Two recordings, one session.
set -u
. /lab/lab/fx2_head_ps.sh
mkdir -p /lab/out/fx2/C /lab/out/fx2/D
cp /lab/out/fx2/C/fc/block.stl /lab/out/fx2/A/washer.3mf ~/fx2/
O=/lab/out/fx2/C; ps_start
sl_record "$O"; sl_mark "recording started: PrusaSlicer 2.9.2"; sl_nap 2
ps_open /home/maker/fx2/block.stl block
sl_mark "dialog: shown"; sl_shot "$O/s-dialog.png"; sl_nap 6
ps_dialog_click Yes
ps_select; sl_mark "size boxes: 25.40 x 12.70 x 6.35"; sl_shot "$O/s-size-yes.png"; sl_nap 10
sl_key Delete "Delete: the object"; sl_nap 2; sl_stop
O=/lab/out/fx2/D
sl_record "$O"; sl_mark "recording started: PrusaSlicer 2.9.2"; sl_mark "PrusaSlicer: empty bed"; sl_nap 3
ps_open /home/maker/fx2/washer.3mf washer3mf
sl_nap 3; sl_shot "$O/s-opened.png"
sl_mark "washer.3mf: opened in PrusaSlicer, no dialog"; sl_nap 2
ps_select; sl_mark "size boxes: shown"; sl_shot "$O/s-size-3mf.png"; sl_nap 10
sl_key Delete "Delete: the object"; sl_nap 2; sl_stop
kill "$SL_APP" 2>/dev/null; sl_display_stop; echo "take C/D ps done"
