# fx2 shared head for PrusaSlicer takes (fcc-slicer:2.9.2, no network, 2880x1800, GDK_SCALE=2)
. /lab/vendor/screenlab-lib/screenlab.sh
C=$HOME/.config/PrusaSlicer; mkdir -p "$C" ~/fx2
python3 /lab/slicer/flatten.py /usr/share/PrusaSlicer/profiles/PrusaResearch.ini --datadir "$C" > /dev/null
sed -i "s/^view_mode = simple/view_mode = expert/" "$C/PrusaSlicer.ini"
export GDK_SCALE=2
ps_start() {   # not filmed: PrusaSlicer up, first-run popups closed, maximised, empty bed
  sl_display 2880 1800
  sl_app "$O/app.log" prusa-slicer --datadir "$C"
  sleep 30
  local w; w=$(xdotool search --onlyvisible --name "Send system info" | head -1)
  [ -n "$w" ] && { xdotool mousemove 1440 1364 click 1; sleep 2; }
  w=$(xdotool search --onlyvisible --name "PrusaSlicer-2" | head -1)
  wmctrl -i -r "$w" -b add,maximized_vert,maximized_horz; sleep 3
  xdotool mousemove 1898 1700 click 1; sleep 1.5
  xdotool mousemove 1400 900
}
ps_open() {  # ps_open PATH LABEL: Ctrl+I, the path typed, Enter
  sl_click 300 1500 "the 3D view: an empty spot"; sl_nap 0.5
  sl_key ctrl+i "Import: Ctrl+I ($2)"; sl_nap 2.5
  sl_type "$1" "Import: typed $1" 80; sl_nap 0.8
  sl_key Return "Import: Enter ($2)"; sl_nap 4.0
}
ps_dialog_click() {  # ps_dialog_click No|Yes
  if [ "$1" = No ]; then sl_glide 1663 1022 20; sl_nap 0.5; sl_mark "No: clicked"; sl_click 1663 1022 "dialog: No"
  else sl_glide 1846 1022 20; sl_nap 0.5; sl_mark "Yes: clicked"; sl_click 1846 1022 "dialog: Yes"; fi
  sl_nap 3
}
ps_select() { sl_click 300 1500 "the 3D view: an empty spot"; sl_nap 0.4; sl_key ctrl+a "Ctrl+A: select the object"; sl_nap 2; }
