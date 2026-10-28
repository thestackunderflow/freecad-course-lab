#!/bin/bash
# Take "addon" (F9 folders, F10, F11; lab Q2, Q3): the ZIP from the web take (the same pinned file) in ~/Downloads;
# PCManFM: right-click, Extract Here, open the folders down to addon/FreeCADMCP (InitGui.py directly inside); FreeCAD
# (fresh 1.1.4 profile, no Mod folder): View, Panels, Python console, print(App.getUserAppDataDir()); the printed
# folder copied and pasted into the file manager's address bar; a new folder Mod; FreeCADMCP copied into it; FreeCAD
# closed (File, Exit) and started again; the workbench list, MCP Addon; Start RPC Server; the status bar.
#   tools/run.sh lab/take_addon.sh
set -u
. /lab/lab/common.sh
O=/lab/out/l1/addon; rm -rf "$O"; mkdir -p "$O" ~/Downloads
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
cp /opt/pre/freecad-mcp-0.1.28.zip ~/Downloads/
find "$FC_DATA" > "$O/profile-before.txt"
sl_display $W $H
fc_start "$O/app.log" 1.8; sleep 6
GDK_SCALE=2 pcmanfm ~/Downloads > "$O/pcmanfm.log" 2>&1 &
pf=$(sl_wait_window "Downloads" 30); sleep 1
xdotool windowsize --sync "$pf" 1550 1050; xdotool windowmove --sync "$pf" 1250 180; sleep 1
xdotool mousemove 1900 1000
sl_record "$O"
sl_mark "recording started: FreeCAD (start page) and the file manager in Downloads"
sl_nap 1.5
# F9: extract and open the folders
sl_click 1656 403 "zip: right-click" 3
sl_nap 0.8
sl_click 1799 537 "zip: Extract Here"
sl_nap 2.5
SL_HOLD=0.2 sl_click 1656 403 "open freecad-mcp-0.1.28 (double-click)"; xdotool click 1; sl_nap 1.5
SL_HOLD=0.2 sl_click 1656 403 "open addon (double-click)"; xdotool click 1; sl_nap 1.5
SL_HOLD=0.2 sl_click 1656 403 "open FreeCADMCP (double-click)"; xdotool click 1; sl_nap 1.5
sl_click 2030 403 "select InitGui.py"
sl_nap 2.5
sl_shot "$O/s1-freecadmcp.png"
sl_click 1371 291 "Back: to addon"
sl_nap 1.5
# F10: ask FreeCAD where its folder is
sl_click 211 36 "FreeCAD: View menu"
sl_glide 255 1043 20; sl_mark "View: Panels"; sl_nap 0.8
sl_glide 700 1043 10; sl_click 800 1162 "Panels: Python Console"
sl_nap 1.5
sl_click 900 1650 "console: click"
sl_type "print(App.getUserAppDataDir())" "console: typed print line" 90
sl_key Return "console: Enter"
sl_nap 2
sl_shot "$O/s2-printed.png"
sl_drag 20 1615 553 1615 "console: select the printed folder"
sl_key ctrl+c "console: copy"
sl_nap 0.8
sl_mark "switch to the file manager"; sl_focus "addon"; sl_nap 0.8
sl_click 2203 291 "address bar"
sl_key ctrl+a; sl_key ctrl+v "address bar: paste"
sl_nap 0.8
sl_key Return "address bar: Enter"
sl_nap 2
sl_shot "$O/s3-v1-1.png"
sl_key ctrl+shift+n "new folder"
sl_nap 1.2
sl_type "Mod" "new folder: typed Mod" 150
sl_key Return "new folder: OK"
sl_nap 2
sl_click 1371 291 "Back: to addon again"
sl_nap 1.2
sl_click 1656 403 "select FreeCADMCP"
sl_key ctrl+c "copy FreeCADMCP"
sl_nap 0.8
sl_click 1515 291 "Forward: to v1-1"
sl_nap 1.2
SL_HOLD=0.2 sl_click 1843 403 "open Mod (double-click)"; xdotool click 1; sl_nap 1.5
sl_key ctrl+v "paste FreeCADMCP into Mod"
sl_nap 2.5
sl_shot "$O/s4-mod.png"
# F11: restart FreeCAD, pick the workbench, switch the socket on
sl_mark "switch to FreeCAD"; sl_focus "FreeCAD 1.1.4"; sl_nap 0.6
sl_click 45 36 "FreeCAD: File menu"
sl_click 79 816 "File: Exit"
sl_nap 3
sl_mark "FreeCAD: start again"
fc_start "$O/app2.log" 1.8; sl_mark "FreeCAD: window back"
sl_nap 5
sl_focus "FreeCAD 1.1.4"; sl_nap 0.5
sl_click 677 88 "workbench list"
sl_nap 1
sl_shot "$O/s5-workbenches.png"
sl_click 629 218 "workbench: MCP Addon"
sl_nap 2
sl_glide 556 218 20; sl_mark "hover: Auto-Start Server"; sl_nap 2
sl_click 126 218 "Start RPC Server"
sl_nap 4
sl_shot "$O/s6-started.png"
sl_glide 600 1500 20; sl_nap 4
sl_mark "recording stopped"
sl_stop
find "$FC_DATA" -maxdepth 3 > "$O/profile-after.txt"
find ~/Downloads -maxdepth 3 > "$O/downloads-tree.txt"
ss -ltn 2>/dev/null | grep 9875 > "$O/listening.txt" || (cat /proc/net/tcp | awk '$2 ~ /:2693$/' > "$O/listening.txt")
convert "$O/s6-started.png" -crop 1600x60+0+1740 "$O/statusbar.png" 2>/dev/null
fc_quit; pkill pcmanfm; sl_display_stop
echo "addon take done"
