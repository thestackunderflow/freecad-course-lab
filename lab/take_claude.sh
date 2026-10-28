#!/bin/bash
# Take "claude-N" (F20-F23, F26; lab Q8, Q12, Q14), paid. Started by claude-run/run.sh.
# The state a viewer has after the setup and the by-hand part: Claude Code + uv installed, the plug added with
# --scope user (wrapped in the logging proxy), FreeCAD on the right with its socket on, the by-hand Cube document open
# and the Python console showing; Claude Code already started in the terminal on the left (46 columns).
# Filmed, nobody touching FreeCAD except where a viewer would: File, New Document in FreeCAD (an empty document);
# message 1 typed into Claude Code; Claude's reply; Claude Code's expanded view (Ctrl+O) of what it did; then, as the
# viewer, Claude's block clicked in the tree and the same console line typed; message 2 (something only execute_code
# does), to film whatever Claude Code shows for it. Afterwards (not filmed): /cost, the documents saved and measured.
set -u
RUN=${1:-claude-1}
O=/lab/out/l1/runs/$RUN; mkdir -p "$O"
. /lab/lab/common.sh
M1=${M1:-"Make a block 5 by 20 by 60 millimetres in FreeCAD, then tell me its volume."}
M2=${M2:-"Now use Python to list the objects in that document."}
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true; mkdir -p ~/hook; claude_home /home/maker/hook
printf 'set -g focus-events on\n' >> ~/.tmux.conf
claude mcp add --scope user freecad -- uvx freecad-mcp@0.1.28 > "$O/mcp-add.txt" 2>&1
uvx freecad-mcp@0.1.28 --help > /dev/null 2>&1   # the uv cache warm, as after the connect step
python3 - "$O" <<'EOF'
import json, os, sys
o = sys.argv[1]
p = os.path.expanduser('~/.claude.json')
d = json.load(open(p))
e = d['mcpServers']['freecad']
json.dump({'mcpServers': {'freecad': e}}, open(os.path.join(o, 'entry-as-added.json'), 'w'), indent=1)
d['mcpServers']['freecad'] = dict(e, command='python3', args=['/lab/proxy/mcp_log_proxy.py', '--log', o + '/transcript.jsonl',
                                   '--png-dir', o, '--', e['command']] + list(e.get('args') or []))
json.dump(d, open(p, 'w'), indent=1)
json.dump({'mcpServers': {'freecad': d['mcpServers']['freecad']}}, open(os.path.join(o, 'entry-as-run.json'), 'w'), indent=1)
EOF
claude --version > "$O/claude-version.txt" 2>&1
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 6
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 1
cd /lab && fc_setup_rpc > "$O/setup-rpc.txt" 2>&1; sleep 2
cd ~/hook
term_open cc 0 0 46 36 30 claude
wait_pane cc 'auto mode|❯' 40; sleep 4
pane cc > "$O/pane-start.txt"
xdotool mousemove 2000 700
sl_record "$O"
sl_mark "recording started: Claude Code (left), FreeCAD with the by-hand Cube document (right)"
sl_nap 2
sl_click 1188 33 "FreeCAD: File menu"
sl_click 1267 68 "File: New Document"
sl_nap 2
sl_glide 700 1500 20; sl_mark "to the terminal"
sl_nap 1
cd /lab && python3 -m lab.drive "$O" cc "$M1"
sl_nap 2
tmux send-keys -t cc C-o; sl_mark "Ctrl+O: expanded view"
sl_nap 7; pane cc 400 > "$O/pane-expanded.txt"
tmux send-keys -t cc C-o; sl_mark "Ctrl+O: back"
sl_nap 2
sl_mark "lab query: where is Claude's block"
read -r DOC OBJ < <(python3 -m lab.newblock "$O/newblock.json" 2>>"$O/lab-query.err")
echo "$DOC $OBJ" > "$O/claude-block.txt"
read -r RX RY < <(python3 -m lab.fcrpc row "$DOC" "$OBJ" 2>>"$O/lab-query.err")
sl_nap 1.5
sl_click "$RX" "$RY" "tree: Claude's block"
sl_nap 1.5
sl_click 2016 1722 "console: click"
sl_type "Gui.Selection.getSelection()[0].Shape.Volume" "console: typed the volume line" 85
sl_key Return "console: Enter"
sl_nap 5
sl_glide 700 1500 20; sl_mark "to the terminal 2"
python3 -m lab.drive "$O" cc "$M2"
sl_nap 3
sl_mark "recording stopped"
sl_stop
sl_shot "$O/after.png"
cp ~/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
pane cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
cd /lab
python3 -m lab.fcrpc docs > "$O/docs.json" 2>&1
python3 -m lab.fcrpc save "$DOC" /tmp/claude.FCStd > "$O/save.txt" 2>&1 && cp /tmp/claude.FCStd "$O/claude.FCStd"
FC_DOC=/tmp/claude.FCStd FC_OUT="$O/measure.json" freecadcmd /lab/checker/measure.py > "$O/measure.log" 2>&1
python3 -c "
import sys, json; sys.path.insert(0, '/lab')
from client import replay
json.dump(replay.call_pairs('$O/transcript.jsonl'), open('$O/calls.json', 'w'), indent=1)
"
fc_quit; tmux kill-server 2>/dev/null; sl_display_stop
echo "claude take done: $DOC $OBJ"
