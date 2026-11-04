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
ADDON_SRC=$HOME/Downloads/freecad-mcp-0.1.28
mkdir -p ~/Downloads && unzip -qo /opt/pre/freecad-mcp-0.1.28.zip -d ~/Downloads
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
  pcmanfm -n "$1" > /dev/null 2>&1 &
  for i in $(seq 1 60); do
    after=$(wmctrl -l | awk '{print $1}' | sort)
    FM_ID=$(comm -13 <(echo "$before") <(echo "$after") | head -1); [ -n "$FM_ID" ] && break; sleep 0.5
  done
  sleep 1; xdotool windowsize --sync "$FM_ID" "$4" "$5"; xdotool windowmove --sync "$FM_ID" "$2" "$3"; sleep 1.5
}
fm_close_all() { pkill pcmanfm; sleep 1.5; }
a0_unfilmed() { fc_open "$OUT/app-a0-unfilmed.log" 8; fc_exit; }
old_machine() {  # not filmed: a computer that ran an older FreeCAD: unversioned config and data folders, the add-on in the old Mod
  a0_unfilmed
  mv "$HOME/.config/FreeCAD/v1-1/"*.cfg "$HOME/.config/FreeCAD/"; rm -rf "$HOME/.config/FreeCAD/v1-1" "$FC/v1-1"
  install_old
  ls -R $HOME/.config/FreeCAD $FC > "$OUT/old-machine-ls-$GROUP.txt" 2>&1
}
install_old() { mkdir -p "$FC/Mod"; cp -r "$ADDON_SRC/addon/FreeCADMCP" "$FC/Mod/"; }

cdrag() {
  # ---- C-drag ----
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
  DRAGX1=${DRAGX1:-203}; DRAGY1=${DRAGY1:-118}; DRAGX2=${DRAGX2:-2100}; DRAGY2=${DRAGY2:-500}
  sl_drag $DRAGX1 $DRAGY1 $DRAGX2 $DRAGY2 "file manager: drag FreeCADMCP to v1-1/Mod"; sl_nap 2
  shot $T/after-drag.png
  ls -R $FC > $T/ls-after-drag.txt
  fm_close_all
  sl_mark "FreeCAD: restarting"; fc_open "$T/app2.log" 8
  wb_pick_mcp; shot $T/workbench-list.png
  sl_click $BTN_START "FreeCAD: Start RPC Server"; sl_nap 1; sl_mark "status bar: started"; sl_nap 5
  shot $T/status-bar.png; shot $T/window-mcp-active.png
  fc_exit; recstop
}
cterm() {
  # ---- C-terminal ----
  mv $FC/v1-1/Mod/FreeCADMCP $FC/Mod/ 2>/dev/null; rmdir $FC/v1-1/Mod 2>/dev/null; mkdir -p $OUT/C-terminal; ls -R $FC > $OUT/C-terminal/ls-reset.txt
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
}

BTN_COPY="2170 983"; BTN_ARROW="2375 983"
a2_start() {      # a2_start TAKE: fresh old machine, FreeCAD started, the dialog waited for, recorded
  old_machine; rec $1; mkdir -p $T; cp "$OUT/old-machine-ls-$GROUP.txt" $T/ls-before.txt
  sl_mark "FreeCAD: starting"
  QT_SCALE_FACTOR=1.5 sl_app "$T/app.log" "$FC_APP"; FC_PID=$SL_APP
  local w; w=$(sl_wait_window "Welcome to FreeCAD 1.1" 90) && DLG=$w || { DLG=; sl_mark "NO DIALOG"; }
  sl_nap 2; sl_mark "welcome dialog: shown"; sl_nap 6
  [ -n "$DLG" ] && xdotool getwindowname $DLG > $T/dialog-title.txt
  wmctrl -l > $T/windows-dialog.txt; shot $T/dialog.png
}
a2_wait_main() {  # after a choice: wait for the dialog to go, then for the main window; place it
  for i in $(seq 1 60); do wmctrl -l | grep -q "Welcome to FreeCAD 1.1" || break; sleep 0.5; done
  sleep 3; local w; w=$(sl_wait_window "FreeCAD 1.1.4" 120) && place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 8
}
a2_inspect() {    # console path, workbench list
  console_open; console_print; shot $T/console-path.png
  wb_open "workbench list: opened"; shot $T/workbench-list$1.png; sl_key Escape "workbench list: closed"; sl_nap 1
}
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
  fc_exit; recstop; fm_close_all
  # ---- B ----
  rec B
  sl_mark "FreeCAD: starting"; fc_open "$T/app.log" 8
  shot $T/start.png
  console_open; shot $T/console-empty.png; console_print; shot $T/console-path.png
  # left open for C-drag; recording of B stops here
  recstop
  cdrag; cterm
  ;;
G1B)
  a0_unfilmed; install_old; cdrag; cterm
  ;;
CD)
  a0_unfilmed; install_old; cdrag
  ;;
PR)
  mkdir -p $OUT/probe; fc_open "$OUT/probe/app.log" 8
  sl_click $M_TOOLS "tools"; sl_nap 1.5; shot $OUT/probe/tools-menu.png; sl_key Escape; fc_exit
  ;;
G2)
  mkdir -p $OUT/D $OUT/E; a0_unfilmed
  mkdir -p $FC/v1-1/Mod; ls -R $FC > $OUT/D/ls-start.txt
  echo "v1-1/Mod was NOT created by FreeCAD's first start (A0); created unfilmed with mkdir -p so the star copy has a target" > $OUT/D/notes.md
  rec D
  cd ~; term_open cc 0 0 44 36 30 bash; xdotool mousemove 2000 900
  say_cmd cc 'cd ~/Downloads/freecad-mcp-0.1.28' "terminal: cd typed"; sl_nap 1.5
  say_cmd cc 'cp -r addon/FreeCADMCP/* ~/.local/share/FreeCAD/v1-1/Mod/' "terminal: cp star typed"; sl_nap 3; shot $T/01-cp.png
  say_cmd cc 'ls ~/.local/share/FreeCAD/v1-1/Mod' "terminal: ls Mod loose"; sl_nap 4; shot $T/02-ls-loose.png
  ls -R $FC/v1-1/Mod > $T/ls-R-loose.txt; pane cc 3000 > $T/terminal.txt
  sl_mark "FreeCAD: restarting"; fc_open "$T/app.log" 8
  wb_open "workbench list: opened (no MCP Addon)"; shot $T/workbench-list.png; sl_key Escape "workbench list: closed"; sl_nap 1
  report_open; shot $T/report-view.png
  fc_exit; recstop
  cp -r $FC $OUT/D/ls-copy-dummy 2>/dev/null; rm -rf $OUT/D/ls-copy-dummy
  LOOSE=$(ls $FC/v1-1/Mod | grep -v '^FreeCADMCP$' | tr '\n' ' '); echo "$LOOSE" > $OUT/E/loose-entries.txt
  rec E
  say_cmd cc 'clear' "clear"; sl_nap 1
  say_cmd cc 'mkdir ~/.local/share/FreeCAD/v1-1/Mod/FreeCADMCP' "terminal: mkdir FreeCADMCP typed"; sl_nap 3; shot $T/01-mkdir.png
  say_cmd cc "cd ~/.local/share/FreeCAD/v1-1/Mod && mv ${LOOSE}FreeCADMCP/" "terminal: mv loose typed"; sl_nap 3; shot $T/02-mv.png
  echo "mv line typed: cd ~/.local/share/FreeCAD/v1-1/Mod && mv ${LOOSE}FreeCADMCP/" > $T/notes.md
  say_cmd cc 'ls ~/.local/share/FreeCAD/v1-1/Mod' "terminal: ls Mod after mv"; sl_nap 3
  ls $FC/v1-1/Mod > $T/ls-Mod-after-mv.txt
  sl_mark "FreeCAD: restarting"; fc_open "$T/app.log" 8
  wb_open "workbench list: MCP Addon"; shot $T/workbench-list.png; sl_key Escape "workbench list: closed"; sl_nap 1
  fc_exit
  say_cmd cc 'clear' "clear 2"; sl_nap 1
  say_cmd cc 'ls -R ~/.local/share/FreeCAD/v1-1/Mod | head -8' "terminal: ls -R typed"; sl_nap 5; shot $T/04-ls-R.png
  pane cc 3000 > $T/terminal.txt
  recstop
  ;;
DH)
  mkdir -p $OUT/D-half; a0_unfilmed
  mkdir -p $FC/v1-1/Mod/FreeCADMCP; cp $ADDON_SRC/addon/FreeCADMCP/InitGui.py $FC/v1-1/Mod/FreeCADMCP/
  ls -R $FC/v1-1/Mod > $OUT/D-half/ls-R.txt
  rec D-half
  sl_mark "FreeCAD: starting"; fc_open "$T/app.log" 8
  report_open; shot $T/report-view.png
  wb_open "workbench list: opened"; shot $T/workbench-list.png; sl_key Escape "workbench list: closed"; sl_nap 1
  fc_exit; recstop
  ;;
F)
  mkdir -p $OUT/F; rec F
  sl_mark "FreeCAD: starting"; fc_open "$T/app.log" 8
  date -u +%Y-%m-%d > $T/date.txt
  sl_click $M_TOOLS "tools menu"; sl_nap 1; sl_click 1479 67 "addon manager: opened"
  sl_nap 3; shot $T/warning.png; wmctrl -l > $T/windows-warning.txt
  sl_click 1564 968 "addon manager: Continue clicked"
  for i in 1 2 3 4 5 6 7 8 9 10; do sl_nap 8; wmctrl -l > $T/windows-$i.txt; shot $T/addon-manager-$i.png; done
  recstop
  ;;
F2)
  mkdir -p $OUT/F; T=$OUT/F; rec F
  sl_mark "FreeCAD: starting"; fc_open "$T/app.log" 8
  date -u +%Y-%m-%d > $T/date.txt
  sl_click $M_TOOLS "tools menu"; sl_nap 1; sl_click 1479 67 "addon manager: opened"
  sl_nap 3; shot $T/warning.png
  sl_click 1564 968 "addon manager: Continue clicked"
  for i in 1 2 3 4 5 6 7 8; do sl_nap 6; done; shot $T/addon-manager-loaded.png
  sl_click 2342 518 "addon manager: search box clicked"; sl_type "MCP" "addon manager: search MCP typed" 100
  sl_nap 8; shot $T/search-MCP.png; wmctrl -l > $T/windows-search.txt
  sl_click 1700 577 "addon manager: hit 1 clicked"; sl_nap 10; shot $T/hit-1.png
  recstop
  ;;
A2COPY)
  a2_start A2-copy
  sl_click $BTN_COPY "welcome dialog: Copy clicked"
  for i in $(seq 1 16); do shot $T/progress-$(printf %02d $i).png; sleep 0.3; done
  sl_mark "FreeCAD: restarting"; a2_wait_main
  a2_inspect -1
  report_open; sl_click 1226 1752 "report tab"; sl_nap 3; shot $T/report-view.png
  fc_exit; recstop
  ls -R $FC > $T/ls-after-copy.txt; ls -la $FC >> $T/ls-after-copy.txt; ls -la $HOME/.config/FreeCAD >> $T/ls-after-copy.txt
  { diff -r $FC/Mod $FC/v1-1/Mod; echo "diff exit=$?"; } > $T/diff-Mod.txt 2>&1
  mkdir -p $FC/Mod/SecondAddon
  printf 'import FreeCADGui\nclass SecondAddonWorkbench(FreeCADGui.Workbench):\n    MenuText = "SecondAddon"\n    ToolTip = "lab marker"\n    def Initialize(self):\n        pass\nFreeCADGui.addWorkbench(SecondAddonWorkbench())\n' > $FC/Mod/SecondAddon/InitGui.py
  mkdir -p $OUT/A2-copy-2; T=$OUT/A2-copy-2; sl_record "$T" nomouse; sl_mark "FreeCAD: restarting"
  fc_open "$T/app.log" 8; wb_open "workbench list: opened (no SecondAddon)"; shot $OUT/A2-copy/workbench-list-2.png; sl_key Escape "closed"; fc_exit; recstop
  ;;
A2SHARE)
  a2_start A2-share
  sl_click $BTN_ARROW "welcome dialog: arrow clicked"; sl_nap 1.5; shot $T/dialog-menu.png
  sl_key Down "menu: Down"; sl_key Return "welcome dialog: Share clicked"
  for i in $(seq 1 10); do shot $T/progress-$(printf %02d $i).png; sleep 0.3; done
  a2_wait_main
  a2_inspect ""
  fc_exit; recstop
  ls -la $FC > $T/ls-after-share.txt; ls -la $HOME/.config/FreeCAD >> $T/ls-after-share.txt 2>&1
  find $HOME -name 'v1-1.do_not_migrate' > $T/marker.txt; ls -R $FC >> $T/ls-after-share.txt
  ;;
A2NEW)
  a2_start A2-new
  sl_click $BTN_ARROW "welcome dialog: arrow clicked"; sl_nap 1.5; shot $T/dialog-menu.png
  sl_key Down "menu: Down"; sl_key Down "menu: Down 2"; sl_key Return "welcome dialog: New clicked"
  for i in $(seq 1 10); do shot $T/progress-$(printf %02d $i).png; sleep 0.3; done
  a2_wait_main
  a2_inspect ""
  fc_exit; recstop
  ls -R $FC > $T/ls-after-new.txt; ls -la $FC >> $T/ls-after-new.txt
  ;;
A2P)
  mkdir -p $OUT/probe; old_machine
  fc_start "$OUT/probe/app.log" 1.5; place "FreeCAD" 1150 0 1730 1800; sleep 6
  wmctrl -l > $OUT/probe/windows-a2.txt; shot $OUT/probe/dialog.png
  ;;
*) echo "unknown group $GROUP"; exit 2;;
esac
echo "$GROUP done"
