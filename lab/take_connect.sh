#!/bin/bash
# Take "connect" (F13, F14, F15; lab Q5, Q6, Q12 fallback), paid (one short question). Started by claude-run/run.sh.
# Claude Code and uv installed (as the install take filmed), the add-on in Mod, FreeCAD open on the right with a new
# empty document and the socket on (Auto-Start Server). Filmed: in a wide terminal, `claude mcp add --scope user ...`
# typed, then `claude mcp list` with a COLD uv cache (timed); the terminal narrowed to 46 columns; `claude`; /mcp, the
# server, its details (the Command line is cropped out in the video), View tools, execute_code's description; then
# "What documents are open in FreeCAD?". Between `claude mcp list` and `claude`, the script wraps the entry in the
# logging proxy (nothing typed; the README says so), so every JSON-RPC line is kept.
set -u
RUN=${1:-connect}
O=/lab/out/l1/runs/$RUN; mkdir -p "$O"
. /lab/lab/common.sh
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true; mkdir -p ~/hook; claude_home /home/maker/hook
rm -rf ~/.cache/uv
claude --version > "$O/claude-version.txt" 2>&1
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 6
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 1
xdotool key ctrl+n; sleep 2
python3 -m lab.fcrpc ping > "$O/socket-ping.txt" 2>&1
cd ~/hook
term_open cc 0 0 74 36 30 bash
xdotool mousemove 2300 1500
sl_record "$O" nomouse
sl_mark "recording started: a terminal (wide) and FreeCAD with the socket on"
sl_nap 1.5
say_cmd cc 'claude mcp add --scope user freecad -- uvx freecad-mcp@0.1.28' "mcp add: typed"
wait_pane cc 'to user config' 30 && sl_mark "mcp add: done"
sl_nap 2.5
say_cmd cc 'claude mcp list' "mcp list: typed"
wait_pane cc 'Connected|Failed|failed' 90 && sl_mark "mcp list: result shown"
sl_nap 4
pane cc 200 > "$O/pane-mcp-list.txt"
# not typed, not visible: wrap the entry in the logging proxy (forwards every byte unchanged)
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
say_cmd cc 'clear' "clear: typed"
sl_mark "terminal: narrowed to 46 columns"
xdotool windowsize --sync "$(sl_wait_window '^cc$')" 1150 1800; sleep 1.5
say_cmd cc 'claude' "claude: typed"
wait_pane cc 'auto mode|for shortcuts|❯' 40 && sl_mark "claude: start screen"
sl_nap 4
pane cc > "$O/pane-start.txt"
python3 - <<'EOF'
import sys, time; sys.path.insert(0, '/lab')
from lab import drive
drive.type_text('cc', '/mcp', delay=0.12)
EOF
sl_nap 0.6; tmux send-keys -t cc Enter; sl_mark "/mcp: Enter"
wait_pane cc 'Manage MCP servers' 20; sl_nap 3.5; pane cc > "$O/pane-mcp-servers.txt"
tmux send-keys -t cc Enter; sl_mark "/mcp: freecad details"
wait_pane cc 'View tools' 20; sl_nap 3.5; pane cc > "$O/pane-mcp-details.txt"
tmux send-keys -t cc Enter; sl_mark "/mcp: View tools"
wait_pane cc 'Tools for freecad' 20; sl_nap 5; pane cc > "$O/pane-mcp-tools.txt"
for i in 1 2 3 4 5 6 7; do tmux send-keys -t cc Down; sleep 0.35; done; sl_mark "/mcp: on execute_code"
sl_nap 1; tmux send-keys -t cc Enter; sl_mark "/mcp: execute_code description"
wait_pane cc 'arbitrary Python' 20; sl_nap 6; pane cc > "$O/pane-mcp-execute-code.txt"
for i in 1 2 3 4; do tmux send-keys -t cc Escape; sleep 0.6; done; sl_mark "/mcp: closed"
sl_nap 2
python3 -m lab.drive "$O" cc "What documents are open in FreeCAD?"
sl_nap 3
sl_mark "recording stopped"
sl_stop
cp ~/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
pane cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
python3 -c "
import sys, json; sys.path.insert(0, '/lab')
from client import replay
json.dump(replay.call_pairs('$O/transcript.jsonl'), open('$O/calls.json', 'w'), indent=1)
tl = [json.loads(l) for l in open('$O/transcript.jsonl')]
tools = [r['msg']['result']['tools'] for r in tl if r['dir'] == 'server->client' and isinstance(r['msg'], dict) and 'tools' in (r['msg'].get('result') or {})]
json.dump(tools[0] if tools else [], open('$O/tools-list.json', 'w'), indent=1)
print('tools', len(tools[0]) if tools else None)
"
fc_quit; tmux kill-server 2>/dev/null; sl_display_stop
echo "connect take done"
