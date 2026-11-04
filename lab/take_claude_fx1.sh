#!/bin/bash
# Fix-it fx1, run R1 (paid, pre-registered in out/fx1/LAB-fx1.md section 4, committed before the run). Started by
# claude-run/run.sh with LESSON=fx1 (so the run folder is out/fx1/runs/R1). One prompt, empty folder, no plug, no FreeCAD
# running, `claude` with no flags (auto mode, default model). Events: `turn 1: Enter` is the pre-registered
# `claude: typed`; `turn 1: reply done` is `turn 1: reply done`.
set -u
RUN=${1:-R1}
O=/lab/out/fx1/runs/$RUN; mkdir -p "$O"
. /lab/lab/common.sh
PROMPT="Where exactly does the FreeCADMCP add-on folder go for FreeCAD 1.1 on this Linux computer? Give the full path."
cd ~ && tools_install
mkdir -p ~/r1-empty; claude_home /home/maker/r1-empty
cd ~/r1-empty && ls -la > "$O/ls-empty.txt" 2>&1
claude --version > "$O/version.txt" 2>&1
echo "claude" > "$O/command.txt"
claude mcp list > "$O/mcp-list.txt" 2>&1
sl_display $W $H
cd ~/r1-empty
term_open cc 0 0 46 36 30 bash
xdotool mousemove 2000 700
sl_record "$O" nomouse
sl_mark "recording started: a terminal in an empty folder, no plug"
sl_nap 1.5
say_cmd cc 'claude' "claude: started"
wait_pane cc 'auto mode|❯|>' 40 && sl_mark "claude: start screen"
sl_nap 3
SL_SHOT_WAKE=0 sl_shot "$O/reply-start.png"
cd /lab && python3 -m lab.drive "$O" cc "$PROMPT"
sl_nap 3
SL_SHOT_WAKE=0 sl_shot "$O/reply-full.png"
pane cc 3000 > "$O/pane-full.txt"
sl_mark "recording stopped"
sl_stop
cp ~/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
pane cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
tmux kill-server 2>/dev/null; sl_display_stop
echo "R1 take done"
