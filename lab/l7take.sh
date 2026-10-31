#!/bin/bash
# Lesson 7 takes ($0, no AI), filmed on the virtual display: a terminal on the left (46 columns), FreeCAD 1.1.4 on the
# right. Every failure is set up off camera the way a viewer's computer would be, then filmed as it happens; the words
# on screen are the programs' own. `test-call` is our test script (lab/l7call.py): it starts the plug with the same
# line Claude Code uses and sends one tool call, printing the reply (and, on an error, the plug's own log line).
#   tools/run.sh lab/l7take.sh A|B|C|D|F|E        out: out/l7/<take>/ (screen.mp4, events.jsonl, cursor.jsonl, panes)
#   A  stop 1: the plug saved with local scope, listed from another folder; the fix (--scope user)
#   B  stop 2: uv never installed (Failed to connect, executable not found); uv's real installer; listed again
#   C  stop 3: FreeCAD closed -> opened without the add-on -> add-on copied, restarted -> Start RPC Server -> OK
#   D  stop 3: port 9875 held by another program: FreeCAD's notification, the call, the program stopped, Start, OK
#   F  stop 3: an old add-on (0.1.24) left in Mod: the warning; replaced with 0.1.28's; restarted; no warning
#   E  stop 4: errors inside FreeCAD's answer: Support vs AttachmentSupport; a folder you may not write to; a save
set -u
TAKE=$1
. /lab/lab/common.sh
O=/lab/out/l7/$TAKE; rm -rf "$O"; mkdir -p "$O"
MOD=$FC_DATA/Mod
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install
mkdir -p ~/hook ~/Downloads ~/bin; claude_home /home/maker/hook; claude_home /home/maker/parts; claude_home /home/maker
printf '#!/bin/sh\nexec python3 -m lab.l7call "$@"\n' > ~/bin/test-call; chmod +x ~/bin/test-call
{ echo 'export PATH="$HOME/bin:$PATH"'; echo "export L7_LOG=$O/test-call.jsonl"; } >> ~/.bashrc
export PATH="$HOME/bin:$PATH" L7_LOG=$O/test-call.jsonl
( cd ~/Downloads && unzip -q /opt/pre/freecad-mcp-0.1.28.zip )
uvx freecad-mcp@0.1.28 --help > /dev/null 2>&1                     # uv's cache warm (lesson 1 timed the cold start)
plug_user() { claude mcp add --scope user freecad -- uvx freecad-mcp@0.1.28 > "$O/mcp-add-offcamera.txt" 2>&1; }
cmd() { say_cmd cc "$1" "$2"; }
waitm() { wait_pane cc "$1" "${3:-60}" && sl_mark "$2" || sl_mark "TIMEOUT: $2"; }
fc_open() { fc_start "$O/app-$1.log" 1.5; place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep "${2:-6}"; }
fc_close() { wmctrl -c "FreeCAD 1.1.4"; for i in $(seq 1 40); do pgrep -x freecad > /dev/null || pgrep -f AppRun > /dev/null || break; sleep 0.25; done; sleep 1; fc_quit; }
pick_mcp() {      # the workbench list opened, MCP Addon chosen by typing its first letters, Enter
  sl_click 1735 75 "workbench list: opened"; sl_nap 2.5
  xdotool type --delay 150 "MCP"; sl_nap 0.8; sl_key Return "workbench list: MCP Addon chosen"; sl_nap 2
}
pane_save() { pane cc 3000 > "$O/pane-$1.txt"; }
sl_display $W $H

case $TAKE in
A)
  cd ~/hook; term_open cc 0 0 46 36 30 bash
  xdotool mousemove 2000 900; sl_record "$O" nomouse; sl_mark "recording started: a terminal in the folder hook"
  sl_nap 1.5
  cmd 'claude mcp add freecad -- uvx freecad-mcp@0.1.28' "add local: typed";  waitm 'local config' "add local: done"; sl_nap 3
  cmd 'claude mcp list' "list in hook: typed";  waitm 'Connected|Failed' "list in hook: Connected"; sl_nap 3.5
  cmd 'clear' "clear"; sl_nap 0.8
  cmd 'cd ~/parts' "cd parts: typed"; sl_nap 1
  cmd 'claude mcp list' "list in parts: typed";  waitm 'No MCP servers' "list in parts: No MCP servers"; sl_nap 4.5
  pane_save no-servers
  cmd 'clear' "clear 2"; sl_nap 0.8
  cmd 'cd ~/hook' "cd hook: typed"; sl_nap 1
  cmd 'claude mcp remove freecad' "remove: typed"; waitm 'Removed' "remove: done"; sl_nap 2.5
  cmd 'claude mcp add --scope user freecad -- uvx freecad-mcp@0.1.28' "add user: typed"; waitm 'user config' "add user: done"; sl_nap 3
  cmd 'cd ~/parts' "cd parts 2: typed"; sl_nap 1
  cmd 'claude mcp list' "list in parts 2: typed"; waitm 'Connected|Failed' "list in parts 2: Connected"; sl_nap 4.5
  ;;
B)
  rm -f ~/.local/bin/uv ~/.local/bin/uvx; rm -rf ~/.cache/uv; hash -r; plug_user
  cd ~; term_open cc 0 0 46 36 30 bash
  xdotool mousemove 2000 900; sl_record "$O" nomouse; sl_mark "recording started: uv was never installed"
  sl_nap 1.5
  cmd 'claude mcp list' "list no uv: typed"; waitm 'Connected|Failed' "list no uv: Failed to connect"; sl_nap 5
  pane_save no-uv
  cmd 'clear' "clear"; sl_nap 0.8
  cmd 'curl -LsSf https://astral.sh/uv/0.13.6/install.sh | sh' "uv install: typed"
  waitm "everything's installed" "uv install: finished" 240; sl_nap 3
  pane_save uv-install
  cmd 'claude mcp list' "list after uv: typed"; waitm 'Connected|Failed' "list after uv: Connected" 120; sl_nap 4.5
  ;;
C)
  plug_user; rm -rf "$MOD"
  cd ~; term_open cc 0 0 46 36 30 bash
  xdotool mousemove 2000 900; sl_record "$O"; sl_mark "recording started: FreeCAD closed, no add-on"
  sl_nap 1.5
  cmd 'claude mcp list' "list closed: typed"; waitm 'Connected|Failed' "list closed: Connected"; sl_nap 3
  cmd 'test-call list_documents' "call closed: typed"; waitm "plug's log" "call closed: error + log"; sl_nap 5
  pane_save closed
  cmd 'clear' "clear"; sl_nap 0.5
  sl_mark "FreeCAD: starting"; fc_open noaddon 4; sl_mark "FreeCAD: open (no add-on)"
  sl_glide 700 1500 20
  cmd 'test-call list_documents' "call noaddon: typed"; waitm "plug's log" "call noaddon: error + log"; sl_nap 3
  sl_click 1735 75 "workbench list: opened (no MCP Addon)"; sl_nap 5
  SL_SHOT_WAKE=0 sl_shot "$O/workbench-list-noaddon.png"
  sl_key Escape "workbench list: closed"; sl_nap 1
  cmd 'clear' "clear 2"; sl_nap 0.5
  cmd 'mkdir -p ~/.local/share/FreeCAD/v1-1/Mod' "mkdir Mod: typed"; sl_nap 1
  cmd 'cp -r ~/Downloads/freecad-mcp-0.1.28/addon/FreeCADMCP ~/.local/share/FreeCAD/v1-1/Mod/' "cp add-on: typed"; sl_nap 1.5
  cmd 'ls ~/.local/share/FreeCAD/v1-1/Mod/FreeCADMCP' "ls add-on: typed"; waitm 'InitGui.py' "ls add-on: InitGui.py shown"; sl_nap 2.5
  sl_mark "FreeCAD: closing"; fc_close; sl_nap 1; sl_mark "FreeCAD: starting again"; fc_open addon 5; sl_mark "FreeCAD: open (add-on in Mod)"
  pick_mcp
  SL_SHOT_WAKE=0 sl_shot "$O/mcp-workbench.png"
  sl_glide 700 1500 20
  cmd 'clear' "clear 3"; sl_nap 0.5
  cmd 'test-call list_documents' "call nostart: typed"; waitm "plug's log" "call nostart: error + log"; sl_nap 4
  pane_save nostart
  sl_click 1254 186 "FreeCAD: Start RPC Server"; sl_nap 4
  SL_SHOT_WAKE=0 sl_shot "$O/started.png"
  sl_glide 700 1500 20
  cmd 'test-call list_documents' "call started: typed"; waitm 'reply: OK' "call started: OK"; sl_nap 4
  pane_save started
  sl_click 1611 186 "FreeCAD: Auto-Start Server"; sl_nap 3
  cat "$FC_DATA/freecad_mcp_settings.json" > "$O/settings-after.json" 2>&1
  sl_glide 700 1500 20
  cmd 'clear' "clear 4"; sl_nap 0.5
  cmd 'claude mcp list' "your turn list: typed"; waitm 'Connected|Failed' "your turn list: Connected"; sl_nap 5
  ;;
D)
  plug_user; addon_install; autostart_on true
  cd ~; term_open cc 0 0 46 22 30 bash; term_open t2 0 1140 46 9 30 bash
  xdotool mousemove 2000 900; sl_record "$O"; sl_mark "recording started: FreeCAD closed; two terminals"
  sl_nap 1.5
  say_cmd t2 'python3 -m http.server 9875' "other program: typed"; wait_pane t2 'Serving HTTP' 20 && sl_mark "other program: serving on 9875"; sl_nap 3
  sl_mark "FreeCAD: starting"; fc_open busy 0; sl_mark "FreeCAD: open"
  for i in $(seq 1 30); do grep -q 'Address already in use' "$O/app-busy.log" 2>/dev/null && break; sleep 0.5; done
  sl_mark "FreeCAD: auto-start failed (notification)"; sl_nap 5
  SL_SHOT_WAKE=0 sl_shot "$O/notification.png"
  sl_glide 700 900 20
  cmd 'test-call list_documents' "call busy: typed"; waitm "plug's log" "call busy: error + log"; sl_nap 5
  pane_save busy
  term_focus t2; sl_key ctrl+c "other program: Ctrl+C"; sl_nap 2
  pick_mcp
  sl_click 1254 186 "FreeCAD: Start RPC Server"; sl_nap 4
  SL_SHOT_WAKE=0 sl_shot "$O/started.png"
  sl_glide 700 900 20
  cmd 'clear' "clear"; sl_nap 0.5
  cmd 'test-call list_documents' "call after: typed"; waitm 'reply: OK' "call after: OK"; sl_nap 4.5
  pane_save after
  ;;
F)
  plug_user; mkdir -p "$MOD"; autostart_on true
  ( cd /tmp && curl -fsSLo old.zip https://github.com/neka-nat/freecad-mcp/archive/refs/tags/v0.1.24.zip && unzip -qo old.zip \
    && cp -r /tmp/freecad-mcp-0.1.24/addon/FreeCADMCP "$MOD/" && sha256sum old.zip ) > "$O/old-fetch.txt" 2>&1
  cd ~; term_open cc 0 0 46 36 30 bash
  fc_open old 8
  xdotool mousemove 2000 900; sl_record "$O"; sl_mark "recording started: FreeCAD with an old add-on (0.1.24)"
  sl_nap 1.5
  cmd 'test-call list_documents' "call old: typed"; waitm 'reply: OK' "call old: OK + warning"; sl_nap 6
  pane_save old
  cmd 'clear' "clear"; sl_nap 0.5
  sl_mark "FreeCAD: closing"; fc_close; sl_nap 1
  cmd 'rm -rf ~/.local/share/FreeCAD/v1-1/Mod/FreeCADMCP' "rm old: typed"; sl_nap 1.5
  cmd 'cp -r ~/Downloads/freecad-mcp-0.1.28/addon/FreeCADMCP ~/.local/share/FreeCAD/v1-1/Mod/' "cp new: typed"; sl_nap 1.5
  sl_mark "FreeCAD: starting again"; fc_open new 8; sl_mark "FreeCAD: open (0.1.28 add-on)"
  sl_glide 700 1500 20
  cmd 'clear' "clear 2"; sl_nap 0.5
  cmd 'test-call list_documents' "call new: typed"; waitm 'reply: OK' "call new: OK, no warning"; sl_nap 4.5
  pane_save new
  ;;
E)
  plug_user; addon_install; autostart_on true
  cp /lab/out/l3/hand/back5.FCStd ~/hook.FCStd
  printf "doc = App.ActiveDocument\nsk = doc.getObject('Body').newObject('Sketcher::SketchObject', 'Sketch1')\nsk.Support = (doc.getObject('XZ_Plane'), [''])\n" > ~/support.py
  printf "doc = App.ActiveDocument\nsk = doc.getObject('Body').newObject('Sketcher::SketchObject', 'Sketch1')\nsk.AttachmentSupport = (doc.getObject('XZ_Plane'), [''])\n" > ~/attach.py
  printf "App.ActiveDocument.saveAs('/opt/hook.FCStd')\n" > ~/save-ro.py
  printf "App.ActiveDocument.saveAs('/home/maker/prints/hook.FCStd')\n" > ~/save.py
  cd ~; term_open cc 0 0 46 36 30 bash
  fc_open hook 8
  ( cd /lab && python3 -c "
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
print(fcrpc.run('''import FreeCAD, FreeCADGui
FreeCAD.openDocument('/home/maker/hook.FCStd')
FreeCADGui.activeDocument().activeView().viewIsometric()
FreeCADGui.SendMsgToActiveView('ViewFit')
FreeCADGui.activateWorkbench('PartDesignWorkbench')
print('ok')'''))" > "$O/setup-open.txt" 2>&1 )
  sleep 2
  xdotool mousemove 2000 900; sl_record "$O"; sl_mark "recording started: lesson 3's hook open, the socket on"
  sl_nap 1.5
  cmd 'cat support.py' "cat support: typed"; sl_nap 4
  cmd 'test-call execute_code support.py' "call support: typed"; waitm "reply: ERROR" "call support: AttributeError"; sl_nap 5
  pane_save support
  cmd 'clear' "clear"; sl_nap 0.5
  cmd 'cat attach.py' "cat attach: typed"; sl_nap 4
  cmd 'test-call execute_code attach.py' "call attach: typed"; waitm "reply: OK" "call attach: OK"; sl_nap 2
  ( cd /lab && python3 -m lab.fcrpc docs > "$O/docs-after-attach.json" 2>&1 )
  sl_nap 3
  pane_save attach
  cmd 'clear' "clear 2"; sl_nap 0.5
  cmd 'cat save-ro.py' "cat save-ro: typed"; sl_nap 3
  cmd 'test-call execute_code save-ro.py' "call save-ro: typed"; waitm "reply: ERROR" "call save-ro: OSError"; sl_nap 5
  pane_save save-ro
  cmd 'clear' "clear 3"; sl_nap 0.5
  cmd 'cat save.py' "cat save: typed"; sl_nap 3
  cmd 'test-call execute_code save.py' "call save: typed"; waitm "reply: OK" "call save: OK"; sl_nap 2
  cmd 'ls -l ~/prints' "ls prints: typed"; waitm 'hook.FCStd' "ls prints: the file"; sl_nap 4.5
  pane_save save
  ;;
esac
sl_mark "recording stopped"
sl_stop
fc_quit; tmux kill-server 2>/dev/null; sl_display_stop
echo "take $TAKE done"
