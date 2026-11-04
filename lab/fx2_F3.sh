#!/bin/bash
# fx2 take F part 3: the exported plate file (2 x 2 x 2) opened in PrusaSlicer: does it ask?
set -u
. /lab/lab/fx2_head_ps.sh
O=/lab/out/fx2/F/tiny2; mkdir -p "$O"
cp /lab/out/fx2/F/tiny.stl ~/fx2/
ps_start
sl_record "$O"; sl_mark "recording started: PrusaSlicer 2.9.2"; sl_nap 2
ps_open /home/maker/fx2/tiny.stl tiny
sl_mark "tiny.stl: opened"; sl_nap 3; sl_shot "$O/s-tiny-open.png"
sl_mark "dialog: shown (tiny)"; sl_nap 5
sl_stop; kill "$SL_APP" 2>/dev/null; sl_display_stop; echo "take F3 done"
