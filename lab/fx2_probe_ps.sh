#!/bin/bash
set -u
O=/lab/out/scratch/fx2probe-ps; mkdir -p "$O"
. /lab/lab/fx2_head_ps.sh
ps_start
sl_click 36 49 "File"; sl_nap 1; sl_glide 96 374 10; sl_nap 1.5; sl_shot "$O/imp.png"
sl_glide 95 428 10; sl_nap 1.5; sl_shot "$O/exp.png"
