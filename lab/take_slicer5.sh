#!/bin/bash
# Lesson 5 take "slicer" (PLAN-L5 F0, F15-F17; lab L5-Q5), in fcc-slicer:2.9.2 (PrusaSlicer 2.9.2, no network). The two
# STL files exported on camera in the by-hand take (out/l5/hand/hook.stl = the Body, hook-pad.stl = the Pad), stock MK4S
# settings (slicer/flatten.py, shown as "(stock)" user presets). Filmed at a person's pace: the Body's file imported;
# the back (left view) square-on; the corner view; Slice now; the estimate; Rotate X 90; Slice now; the estimate; the
# preview's layers stepped down; then the plate cleared and the Pad's file imported; its back; Slice now; its estimate.
# Not filmed: the first-run "Send system info" dialog answered "Do not send anything" and the hint popup closed before
# the recording starts. 2x GTK scale on a 2880 x 1800 screen.
#   MSYS_NO_PATHCONV=1 docker run --rm --name fc5-slicer --network none --shm-size 1g --memory 4g -v <lab>:/lab \
#     fcc-slicer:2.9.2 bash /lab/lab/take_slicer5.sh
set -u
. /lab/vendor/screenlab-lib/screenlab.sh
O=/lab/out/l5/slicer; rm -rf "$O"; mkdir -p "$O"
C=$HOME/.config/PrusaSlicer; mkdir -p "$C"
python3 /lab/slicer/flatten.py /usr/share/PrusaSlicer/profiles/PrusaResearch.ini --datadir "$C"
cp /lab/out/l5/hand/hook.stl /lab/out/l5/hand/hook-pad.stl ~/
export GDK_SCALE=2
sl_display 2880 1800
sl_app "$O/app.log" prusa-slicer --datadir "$C"
sleep 30
w=$(xdotool search --onlyvisible --name "Send system info" | head -1)
[ -n "$w" ] && { xdotool mousemove 1440 1364 click 1; sleep 2; }
w=$(xdotool search --onlyvisible --name "PrusaSlicer-2" | head -1)
wmctrl -i -r "$w" -b add,maximized_vert,maximized_horz; sleep 3
xdotool mousemove 1898 1700 click 1; sleep 1.5          # the "Did you know" hint popup's close button (not filmed)
xdotool mousemove 1400 900
sl_shot "$O/p0-start.png"
shot() { sl_shot "$O/$1.png"; }
add() {  # add FILE LABEL: Ctrl+I, the path typed, Enter
  sl_key ctrl+i "Import: Ctrl+I ($2)"
  sl_nap 2.5
  sl_type "/home/maker/$1" "Import: typed $1" 80
  sl_nap 0.8
  sl_key Return "Import: Enter ($2)"
  sl_nap 4.0
}
canvas() { sl_click 300 1500 "the 3D view: an empty spot"; sl_nap 0.6; }   # keys go to the 3D view after a click there
view() { canvas; sl_key "$1" "key $1: $2"; sl_nap 1.0; sl_key z "key Z: zoom to the part ($2)"; sl_nap 2.0; }
slice() { sl_glide 2416 1754 20; sl_nap 0.5; sl_click 2416 1754 "Slice now ($1)"; sl_nap 13; sl_mark "the estimate ($1)"; sl_nap 5; }
sl_record "$O"
sl_mark "recording started: PrusaSlicer 2.9.2, stock MK4S settings"
sl_nap 2
add hook.stl "the Body's file"
sl_mark "Size 40 30 60"; sl_nap 3
shot p1-added
view 5 "the left view, the back (Body)"
sl_mark "the back: two holes (Body)"; sl_nap 4.0
shot p2-back
view 0 "the corner view"
slice "standing"
shot p3-standing
sl_click 72 1724 "the 3D view button"; sl_nap 2.0
canvas; sl_key ctrl+a "Ctrl+A: select the part"; sl_nap 1.5
sl_glide 2203 864 20; sl_nap 0.5
sl_click 2203 864 "Rotate X: the box"
xdotool key ctrl+a
sl_type "90" "Rotate X: typed 90" 250
sl_key Return "Rotate X: Enter"
sl_nap 1.0
sl_click 2500 1250 "the side panel: an empty spot"
sl_mark "on its side: Size 40 60 30"; sl_nap 3.0
shot p4-side
slice "on its side"
shot p5-side-sliced
xdotool mousemove 1200 900; sl_nap 0.5
for i in $(seq 1 75); do xdotool key Down; sleep 0.08; done
sl_mark "layers stepped down to the middle"; sl_nap 4.0
shot p6-layers
sl_click 72 1724 "the 3D view button (to clear)"; sl_nap 2.0
canvas; sl_key ctrl+Delete "Ctrl+Delete: clear the plate"; sl_nap 2.0
add hook-pad.stl "the Pad's file"
view 5 "the left view, the back (Pad)"
sl_mark "the back: no holes (Pad)"; sl_nap 4.0
shot p7-pad-back
view 0 "the corner view (Pad)"
slice "the Pad, standing"
shot p8-pad-sliced
sl_mark "recording stopped"
sl_stop
kill "$SL_APP" 2>/dev/null; sl_display_stop
echo "slicer take done"
