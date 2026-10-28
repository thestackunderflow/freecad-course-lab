#!/bin/bash
# Take "fail-open" (F29; lab Q10b), free (no message is sent to Claude). The next real beginner failure the lab
# reproduced (the planned "uvx not found in an old terminal" did not happen here: Claude Code's installer note puts
# ~/.local/bin on PATH and uv installs into the same folder, out/l1/install/q4-*.txt): Claude Code was already open
# when the plug was added in another terminal. Its /mcp says no servers; /exit and `claude` again; now it lists freecad.
set -u
. /lab/lab/common.sh
O=/lab/out/l1/fail-open; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; mkdir -p ~/hook; claude_home /home/maker/hook
printf 'set -g focus-events on\n' > /tmp/tm.conf
uvx freecad-mcp@0.1.28 --help > /dev/null 2>&1
sl_display $W $H
cd ~/hook
term_open cc 0 0 46 36 30 bash
tmux send-keys -t cc -l 'claude'; tmux send-keys -t cc Enter
wait_pane cc 'auto mode|❯' 40; sleep 3
term_open t2 1440 0 46 36 30 bash
xdotool mousemove 1440 1700
sl_record "$O" nomouse
sl_mark "recording started: Claude Code already open (left), a second terminal (right)"
sl_nap 1.5
say_cmd t2 'claude mcp add --scope user freecad -- uvx freecad-mcp@0.1.28' "t2: mcp add typed"
wait_pane t2 'Added stdio' 30 && sl_mark "t2: mcp add done"
sl_nap 2.5
term_focus cc; sl_mark "back to Claude Code"
python3 -c "import sys; sys.path.insert(0, '/lab'); from lab import drive; drive.type_text('cc', '/mcp', delay=0.12)"
sl_nap 0.6; tmux send-keys -t cc Enter; sl_mark "cc: /mcp Enter"
wait_pane cc 'No MCP servers' 20 && sl_mark "cc: no MCP servers"
sl_nap 5
pane cc 300 > "$O/pane-no-servers.txt"
python3 -c "import sys; sys.path.insert(0, '/lab'); from lab import drive; drive.type_text('cc', '/exit', delay=0.12)"
sl_nap 0.6; tmux send-keys -t cc Enter; sl_mark "cc: /exit"
sl_nap 2
python3 -c "import sys; sys.path.insert(0, '/lab'); from lab import drive; drive.type_text('cc', 'claude', delay=0.12)"
sl_nap 0.5; tmux send-keys -t cc Enter; sl_mark "cc: claude again"
wait_pane cc 'auto mode|❯' 40; sl_nap 3
python3 -c "import sys; sys.path.insert(0, '/lab'); from lab import drive; drive.type_text('cc', '/mcp', delay=0.12)"
sl_nap 0.6; tmux send-keys -t cc Enter; sl_mark "cc: /mcp Enter again"
wait_pane cc 'Manage MCP servers' 20 && sl_mark "cc: freecad listed"
sl_nap 5
pane cc 300 > "$O/pane-listed.txt"
tmux send-keys -t cc Escape
sl_mark "recording stopped"
sl_stop
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 1
tmux kill-server 2>/dev/null; sl_display_stop
echo "fail-open done"; grep -v "^$" "$O/pane-no-servers.txt" | tail -8; grep -v "^$" "$O/pane-listed.txt" | tail -8
