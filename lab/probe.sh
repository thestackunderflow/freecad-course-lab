#!/bin/bash
# Probe: FreeCAD 1.1.4 in a fresh profile on the 2880x1800 display; screenshots after start (scale $1).
set -u
. /lab/lab/common.sh
O=/lab/out/scratch/probe/${2:-fc}; mkdir -p "$O"
sl_display $W $H
fc_start "$O/app.log" "${1:-1.8}"
sleep 8
sl_shot "$O/start.png"
xdotool search --onlyvisible --name ".*" | while read w; do echo "$w $(xdotool getwindowname $w) $(xdotool getwindowgeometry $w | tr '\n' ' ')"; done > "$O/windows.txt"
find $HOME -maxdepth 5 -not -path '*/.cache/*' > "$O/home.txt"
fc_quit
