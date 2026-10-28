#!/bin/bash
# Take "no-plug" (F0 "before setup"; lab Q0), paid. A container like a viewer's before the setup: FreeCAD 1.1.4
# installed (`freecad` and `freecadcmd` on PATH) and open on the right with an empty document, Claude Code installed
# with its own tools and its default mode, NO MCP server added, no add-on. The same request typed; whatever Claude
# does is filmed and its Bash calls are in the session log. The four outcomes written in PLAN.md before the run:
# it tells you how / it hands you a script / it builds one out of sight / it opens a new FreeCAD window itself.
set -u
RUN=${1:-no-plug}
O=/lab/out/l1/runs/$RUN; mkdir -p "$O"
. /lab/lab/common.sh
M1=${M1:-"Make a block 5 by 20 by 60 millimetres in FreeCAD, then tell me its volume."}
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; mkdir -p ~/hook; claude_home /home/maker/hook
claude mcp list > "$O/mcp-list.txt" 2>&1
which freecad freecadcmd > "$O/which.txt" 2>&1
claude --version > "$O/claude-version.txt" 2>&1
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 6
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 1
xdotool key ctrl+n; sleep 2
cd ~/hook
term_open cc 0 0 46 36 30 claude
wait_pane cc 'auto mode|❯' 40; sleep 4
xdotool mousemove 2000 900
sl_record "$O"
sl_mark "recording started: Claude Code (no MCP server) and FreeCAD with an empty document"
sl_nap 2
cd /lab && python3 -m lab.drive "$O" cc "$M1"
sl_nap 4
sl_mark "recording stopped"
sl_stop
pane cc 600 > "$O/pane-full-after.txt"
cp ~/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
xdotool search --onlyvisible --name ".*" 2>/dev/null | while read w; do echo "$w $(xdotool getwindowname "$w" 2>/dev/null)"; done | grep -v "^[0-9]* $" > "$O/windows-after.txt"
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
pane cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
python3 - "$O" <<'EOF'
import json, sys
o = sys.argv[1]
calls = []
for line in open(o + '/session.jsonl', encoding='utf-8'):
    try:
        r = json.loads(line)
    except ValueError:
        continue
    for c in ((r.get('message') or {}).get('content') or []):
        if isinstance(c, dict) and c.get('type') == 'tool_use':
            calls.append({'tool': c.get('name'), 'input': c.get('input')})
json.dump(calls, open(o + '/tool-uses.json', 'w'), indent=1)
print(len(calls), [c['tool'] for c in calls])
EOF
find ~ -name "*.FCStd" -newer "$O/claude-version.txt" 2>/dev/null > "$O/fcstd-made.txt"
fc_quit; tmux kill-server 2>/dev/null; sl_display_stop
echo "no-plug take done"
