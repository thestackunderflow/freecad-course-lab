#!/bin/bash
# fx3 run R1 (LAB-fx3 section 4, pre-registered; one run): Claude Code, no plug connected, the log line pasted,
# then "what do I change?". Started by claude-run/run.sh with LESSON=fx3 (token in the env, deleted by run.sh).
set -u
RUN=${1:-R1}
O=/lab/out/fx3/runs/$RUN; mkdir -p "$O"
. /lab/lab/common.sh
cd ~ && mkdir -p ~/r1
claude_home /home/maker/r1
curl -LsSf https://astral.sh/uv/0.13.6/install.sh | sh > "$O/uv-install.txt" 2>&1
export PATH="$HOME/.local/bin:$PATH"
mkdir -p ~/.config/Claude && cp /lab/out/fx3/C/claude_desktop_config.json ~/.config/Claude/
claude mcp add --scope user freecad -- /home/maker/.local/bin/uvx freecad-mcp@0.1.28 > "$O/mcp-add-state.txt" 2>&1
claude mcp remove --scope user freecad > "$O/mcp-remove-before.txt" 2>&1
printf 'auto mode: Claude Code 2.1.308 default launch (no flags), as lesson 7 R1; no CLAUDE.md in the folder\n' > "$O/mode.txt"
claude --version > "$O/claude-version.txt" 2>&1
claude mcp list > "$O/mcp-list-before.txt" 2>&1
ls -la ~/r1 > "$O/ls-before.txt" 2>&1
printf 'The FreeCAD MCP plug fails in Claude Desktop. The log says: spawn uvx ENOENT. In my terminal, uvx works. What should I change?
' > "$O/prompt.txt"
sl_display $W $H
cd ~/r1
term_open cc 0 0 46 36 30 bash
xdotool mousemove 2000 700
sl_record "$O" nomouse
sl_mark "recording started: a terminal in an empty folder, no plug connected"
sl_nap 1.5
say_cmd cc 'claude' "claude start: typed"
wait_pane cc 'auto mode|❯' 40 && sl_mark "claude: start screen"
sl_nap 3
SL_SHOT_WAKE=0 sl_shot "$O/suggested-prompt-crop.png"
cd /lab && python3 - "$O" <<'PY'
import subprocess, sys
sys.path.insert(0, '/lab')
from lab import drive
o = sys.argv[1]
text = open(o + '/prompt.txt', encoding='utf-8').read().rstrip('\n')
def paste(name, t, delay=0.0):
    subprocess.run(['tmux', 'load-buffer', '-b', 'fx3', '-'], input=t.encode('utf-8'), check=True)
    subprocess.run(['tmux', 'paste-buffer', '-p', '-b', 'fx3', '-t', name], check=True)
drive.type_text = paste
drive.main(o, 'cc', [text])
PY
sl_nap 3
SL_SHOT_WAKE=0 sl_shot "$O/suggested-prompt-crop.png"
pane cc 400 > "$O/pane-after-m1.txt"
sl_nap 2
sl_mark "recording stopped"
sl_stop
pane cc 3000 > "$O/pane-full.txt"
cp ~/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
ls -la ~/r1 > "$O/ls-after.txt" 2>&1
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
pane cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
python3 - "$O" <<'PY'
import json, os, sys
d = sys.argv[1]
rows = [json.loads(l) for l in open(os.path.join(d, 'events.jsonl')) if l.strip()]
out = []
for r in rows:
    out.append((r['event'], r['t']))
    if r['event'] == 'turn 1: Enter':
        out.append(('claude: typed', r['t']))
open(os.path.join(d, 'events.tsv'), 'w').write(''.join('%s\t%.2f\n' % x for x in out))
PY
tmux kill-server 2>/dev/null; sl_display_stop
echo "R1 take done"
