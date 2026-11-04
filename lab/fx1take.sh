#!/bin/bash
# Fix-it video fx1 takes (LAB-fx1.md): FreeCAD 1.1.4 on the virtual display, a terminal on the left, FreeCAD on the right.
#   FCC_PREFIX=fcx1 tools/run.sh lab/fx1take.sh G1|G2|DH|A2COPY|A2SHARE|A2NEW
#   G1  A0 -> A -> B -> C-drag -> C-terminal (one container, one home)
#   G2  D -> E -> F (A0 repeated unfilmed first)
#   DH  D-half;  A2COPY / A2SHARE / A2NEW  the upgraded machine (fresh home with the old Mod folder before first start)
# No profile seed: every container starts from a clean home. out/fx1/<take>/ gets screen.mp4, events.jsonl, cursor.jsonl.
set -u
GROUP=$1
. /lab/lab/common.sh
OUT=/lab/out/fx1
FC=$HOME/.local/share/FreeCAD
ADDON_SRC=/tmp/fcmcp/freecad-mcp-0.1.28
mkdir -p /tmp/fcmcp && unzip -qo /opt/pre/freecad-mcp-0.1.28.zip -d /tmp/fcmcp
# screen positions (display pixels, FreeCAD at QT_SCALE_FACTOR 1.5 placed at 1150,0 1730x1800)
M_VIEW="1326 33"; M_PANELS="1361 873"; M_CONSOLE="1818 973"; M_REPORT="1803 1007"; M_WB="1735 75"; M_TOOLS="1403 33"
BTN_START="1254 186"
sl_display $W $H
xdotool mousemove 2000 900

fc_open() { fc_start "$1" 1.5; place "FreeCAD 1.1.4|FreeCAD" 1150 0 1730 1800; sleep "${2:-6}"; }
fc_exit() { sl_key ctrl+q "FreeCAD: quit"; for i in $(seq 1 60); do pgrep -f AppRun >/dev/null || pgrep -x freecad >/dev/null || break; sleep 0.5; done; sleep 1; FC_PID=; }
shot() { SL_SHOT_WAKE=0 sl_shot "$1"; }
rec() { mkdir -p "$OUT/$1"; T=$OUT/$1; sl_record "$T" nomouse; sl_mark "recording started: $1"; sl_nap 1; }
recstop() { sl_nap 1; sl_mark "recording stopped"; sl_stop; }
notes() { printf '%s\n' "$2" >> "$OUT/$1/notes.md"; }
console_open() { sl_click $M_VIEW "view menu"; sl_nap 1; sl_click $M_PANELS "panels"; sl_nap 1; sl_click $M_CONSOLE "console: opened"; sl_nap 2; }
console_print() { sl_type 'print(App.getUserAppDataDir())' "console: print typed" 80; sl_key Return "console: Return"; sl_nap 1; sl_mark "console: path printed"; sl_nap 5; }
report_open() { sl_click $M_VIEW "view menu"; sl_nap 1; sl_click $M_PANELS "panels"; sl_nap 1; sl_click $M_REPORT "report view: shown"; sl_nap 5; }
wb_open() { sl_click $M_WB "$1"; sl_nap 5; }
wb_pick_mcp() { wb_open "workbench list: opened"; xdotool type --delay 150 "MCP"; sl_nap 0.8; sl_key Return "workbench list: MCP Addon chosen"; sl_nap 2; }
fm_open() {       # fm_open DIR X Y W H -> FM_ID: a PCManFM window placed
  local before after
  before=$(wmctrl -l | awk '{print $1}' | sort)
  pcmanfm "$1" > /dev/null 2>&1 &
  for i in $(seq 1 60); do
    after=$(wmctrl -l | awk '{print $1}' | sort)
    FM_ID=$(comm -13 <(echo "$before") <(echo "$after") | head -1); [ -n "$FM_ID" ] && break; sleep 0.5
  done
  sleep 1; xdotool windowsize --sync "$FM_ID" "$4" "$5"; xdotool windowmove --sync "$FM_ID" "$2" "$3"; sleep 1.5
}
fm_close_all() { for w in $(wmctrl -l | grep -v -E 'FreeCAD|^0x[0-9a-f]+ +-1' | awk '{print $1}'); do wmctrl -i -c "$w"; done; sleep 1; }
a0_unfilmed() { fc_open "$OUT/app-a0-unfilmed.log" 8; fc_exit; }
install_old() { mkdir -p "$FC/Mod"; cp -r "$ADDON_SRC/addon/FreeCADMCP" "$FC/Mod/"; }

case $GROUP in
G1)
  mkdir -p $OUT/A0 $OUT/A $OUT/B $OUT/C-drag $OUT/C-terminal
  { env | grep XDG_DATA_HOME; echo "exit=$?"; } > $OUT/A0/xdg-check.txt 2>&1
  echo "XDG_DATA_HOME lines: $(env | grep -c XDG_DATA_HOME)" >> $OUT/A0/xdg-check.txt
  ls -la $HOME/.local/share/ > $OUT/A0/ls-before.txt 2>&1
  date -u +%Y-%m-%d > $OUT/env-date.txt
  # ---- A0 ----
  rec A0
  sl_mark "FreeCAD: starting"; fc_open "$T/app.log" 8
  wmctrl -l > $T/windows-first-start.txt; shot $T/first-start.png
  console_open; shot $T/console-empty.png; console_print; shot $T/console.png
  fc_exit; recstop
  ls -la $FC > $T/ls-FreeCAD.txt 2>&1; ls -la $FC/v1-1 > $T/ls-v1-1.txt 2>&1; find $FC -maxdepth 3 > $T/find.txt; ls -la $HOME/.config/FreeCAD > $T/ls-config.txt 2>&1
  # ---- A ----
  mkdir -p $FC/Mod; cp -r $ADDON_SRC/addon/FreeCADMCP $FC/Mod/
  ls -la $FC/Mod/FreeCADMCP > $OUT/A/ls-old-Mod.txt
  rec A
  fm_open "$FC/Mod/FreeCADMCP" 1150 0 1730 1800; sl_mark "file manager: old Mod/FreeCADMCP"; sl_nap 3; shot $T/filemanager-old-Mod.png
  sl_mark "FreeCAD: starting"; fc_open "$T/app.log" 8
  wb_open "workbench list: opened (no MCP Addon)"; shot $T/workbench-list.png; sl_key Escape "workbench list: closed"; sl_nap 1
  report_open; shot $T/report-view.png
  fc_exit; recstop
  # ---- B ----
  rec B
  sl_mark "FreeCAD: starting"; fc_open "$T/app.log" 8
  shot $T/start.png
  console_open; shot $T/console-empty.png; console_print; shot $T/console-path.png
  # left open for C-drag; recording of B stops here
  recstop
  # ---- C-drag ----
  fc_exit
  rec C-drag
  fm_open "$FC/Mod" 0 0 1430 1000; FM1=$FM_ID
  fm_open "$FC/v1-1" 1450 0 1430 1000; FM2=$FM_ID
  shot $T/filemanagers-start.png
  # new folder Mod inside v1-1 (it does not exist yet): Ctrl+Shift+N in the right window, type the name
  xdotool windowactivate --sync $FM2; sl_nap 0.5
  sl_key ctrl+shift+n "file manager: new folder Mod"; sl_nap 1
  xdotool type --delay 80 "Mod"; sl_key Return "file manager: new folder named"; sl_nap 1.5
  shot $T/new-folder.png
  # open the new Mod in the right window (double click) -> navigate by address bar
  xdotool windowactivate --sync $FM2; sl_key ctrl+l "file manager: address bar"; xdotool type --delay 40 "$FC/v1-1/Mod"; sl_key Return "file manager: open v1-1/Mod"; sl_nap 1.5
  shot $T/filemanagers-ready.png
  mkdir -p $T/ls; ls -R $FC > $T/ls/before-drag.txt
  echo FM1=$FM1 FM2=$FM2 > $T/fm-ids.txt
  DRAGX1=${DRAGX1:-150}; DRAGY1=${DRAGY1:-170}; DRAGX2=${DRAGX2:-2100}; DRAGY2=${DRAGY2:-500}
  sl_drag $DRAGX1 $DRAGY1 $DRAGX2 $DRAGY2 "file manager: drag FreeCADMCP to v1-1/Mod"; sl_nap 2
  shot $T/after-drag.png
  ls -R $FC > $T/ls-after-drag.txt
  fm_close_all
  sl_mark "FreeCAD: restarting"; fc_open "$T/app2.log" 8
  wb_pick_mcp; shot $T/workbench-list.png
  sl_click $BTN_START "FreeCAD: Start RPC Server"; sl_nap 1; sl_mark "status bar: started"; sl_nap 5
  shot $T/status-bar.png; shot $T/window-mcp-active.png
  fc_exit; recstop
  # ---- C-terminal ----
  mv $FC/v1-1/Mod/FreeCADMCP $FC/Mod/ 2>/dev/null; mkdir -p $OUT/C-terminal; ls -R $FC > $OUT/C-terminal/ls-reset.txt
  rec C-terminal
  cd ~; term_open cc 0 0 44 36 30 bash; xdotool mousemove 2000 900
  say_cmd cc 'ls ~/.local/share/FreeCAD' "terminal: ls FreeCAD typed"; sl_nap 3; shot $T/01-ls.png
  say_cmd cc 'mkdir -p ~/.local/share/FreeCAD/v1-1/Mod' "terminal: mkdir -p typed"; sl_nap 3; shot $T/02-mkdir.png
  say_cmd cc 'mv ~/.local/share/FreeCAD/Mod/FreeCADMCP ~/.local/share/FreeCAD/v1-1/Mod/' "terminal: mv typed"; sl_nap 3; shot $T/03-mv.png
  say_cmd cc 'ls ~/.local/share/FreeCAD/v1-1/Mod/FreeCADMCP' "terminal: ls InitGui shown"; sl_nap 3; shot $T/04-ls-InitGui.png
  pane cc 3000 > $T/terminal.txt
  sl_mark "FreeCAD: restarting"; fc_open "$T/app.log" 8
  wb_pick_mcp; shot $T/workbench-list.png
  sl_click $BTN_START "FreeCAD: Start RPC Server"; sl_nap 1; sl_mark "status bar: started"; sl_nap 5
  shot $T/status-bar.png
  fc_exit; recstop
  ls -R $FC > $T/ls-final.txt
  ;;
*) echo "unknown group $GROUP"; exit 2;;
esac
echo "$GROUP done"
