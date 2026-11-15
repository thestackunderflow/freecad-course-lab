#!/bin/bash
# Task R probe (14 Nov 2026), $0 Claude (no model call: `claude mcp list` only health-checks the server):
#   MSYS_NO_PATHCONV=1 docker run --rm --user maker --shm-size 1g --memory 6g -v <lab>:/lab \
#     fcc-app:1.1.4-0.1.31 bash /lab/lab/r031_probe.sh /lab/out/r031
# A fresh profile; the add-on folder from the v0.1.31 tag ZIP copied into Mod (as fc1 F9-F10); auto-start OFF so the
# RPC server is started by its own command, as fc1 does; then uvx freecad-mcp@0.1.31 (and @0.1.28 for the tool list)
# and Claude Code's `claude mcp add` + `claude mcp list`, as fc1 F14-F16. Screenshots s1-s4 in OUT.
. /lab/lab/common.sh
A=${ADDON:-0.1.31}   # docker run -e ADDON=0.1.28: the same run with the filmed add-on (the server stays @0.1.31)
O=${1:-/lab/out/r031}; mkdir -p "$O"; export R031_OUT=/tmp/r031; mkdir -p $R031_OUT
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
mkdir -p "$FC_DATA/Mod" && unzip -q /opt/pre/freecad-mcp-$A.zip -d /tmp/z \
  && cp -r /tmp/z/freecad-mcp-$A/addon/FreeCADMCP "$FC_DATA/Mod/"
grep -o '<version>[^<]*' "$FC_DATA/Mod/FreeCADMCP/package.xml" > "$O/addon-version.txt"
autostart_on false
tools_install
sl_display $W $H
QT_SCALE_FACTOR=1.8 sl_app "$O/app.log" "$FC_APP" /lab/lab/r031_gui.py; FC_PID=$SL_APP
sl_wait_window "FreeCAD" 180 > /dev/null
sleep 6; sl_shot "$O/s1-start.png"
for i in $(seq 1 120); do [ -e $R031_OUT/stage1 ] && break; sleep 0.5; done
sl_shot "$O/s2-mcp-menu.png"
for i in $(seq 1 120); do [ -e $R031_OUT/stage2 ] && break; sleep 0.5; done
sl_shot "$O/s3-rpc-started.png"
cp $R031_OUT/gui.json "$O/gui.json" 2>/dev/null
cd /lab
python3 -m lab.r031_mcp 0.1.28 "$O/mcp-028.jsonl" > "$O/mcp-028.json" 2>> "$O/mcp.err"
python3 -m lab.r031_mcp 0.1.31 "$O/mcp-031.jsonl" call > "$O/mcp-031.json" 2>> "$O/mcp.err"
mkdir -p ~/proj && cd ~/proj && claude_home "$HOME/proj"
term_open shell 40 1000 100 16 30
say_cmd shell "claude mcp add freecad -- uvx freecad-mcp@0.1.31"
wait_pane shell 'Added stdio MCP server' 60
say_cmd shell "claude mcp list"
wait_pane shell 'freecad: .*(Connected|Failed)' 180
sleep 1; sl_shot "$O/s4-claude-mcp-list.png"; pane shell 200 > "$O/claude-mcp-list.txt"
cd /lab && python3 - > "$O/report-end.txt" 2>&1 <<'PY'
from lab import fcrpc
print(fcrpc.run("""from PySide import QtWidgets
import FreeCADGui
for d in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
    if 'Report' in d.objectName():
        for t in d.findChildren(QtWidgets.QPlainTextEdit) + d.findChildren(QtWidgets.QTextEdit):
            print(t.toPlainText())"""))
PY
cd /lab && python3 - "$O" <<'PY'
import json, sys
o = sys.argv[1]
ev = json.load(open(f'{o}/gui.json'))
m28, m31 = json.load(open(f'{o}/mcp-028.json')), json.load(open(f'{o}/mcp-031.json'))
ev.update(initialize_ok=m31['initialize_ok'], server_info=m31.get('server_info'), call=m31.get('call'),
          tools28=m28['tools'], tools31=m31['tools'], mcp_list=open(f'{o}/claude-mcp-list.txt').read(),
          addon_version=open(f'{o}/addon-version.txt').read().strip())
json.dump(ev, open(f'{o}/evidence.json', 'w'), indent=1)
PY
python3 -m lab.r031 "$O"
kill $FC_PID 2>/dev/null; sl_display_stop
