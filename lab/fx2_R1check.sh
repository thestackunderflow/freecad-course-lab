#!/bin/bash
# fx2 R1 second check (not scored): the file Claude wrote, opened in PrusaSlicer 2.9.2 -- does the dialog appear?
set -u
. /lab/lab/fx2_head_ps.sh
O=/lab/out/fx2/runs/R1/check; mkdir -p "$O"
cp /lab/out/fx2/runs/R1/washer.stl ~/fx2/claude-washer.stl
ps_start
sl_record "$O"; sl_mark "recording started: PrusaSlicer 2.9.2"; sl_nap 2
ps_open /home/maker/fx2/claude-washer.stl claude
sl_mark "claude export: opened"; sl_nap 3; sl_shot "$O/s-open.png"; sl_nap 4
sl_stop; kill "$SL_APP" 2>/dev/null; sl_display_stop; echo "R1 check done"
