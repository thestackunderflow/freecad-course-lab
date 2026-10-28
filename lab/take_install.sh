#!/bin/bash
# Take "install" (F7, F12; lab Q4): Claude Code's and uv's real installers, typed at a person's pace into a fresh
# terminal in a fresh home (network on: both download from their sites). Then the old-terminal check for F29.
#   tools/run.sh lab/take_install.sh
set -u
. /lab/lab/common.sh
O=/lab/out/l1/install; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
sl_display $W $H
TERM_ARGS="40 40 64 40 34"
term_open Terminal $TERM_ARGS
sl_record "$O"
sl_mark "recording started: a fresh terminal"
sl_nap 1.5
say_cmd Terminal 'curl -fsSL https://claude.ai/install.sh | bash -s 2.1.308' "claude install: typed"
wait_pane Terminal 'Installation complete' 240 && sl_mark "claude install: finished"
sl_nap 3
pane Terminal 200 > "$O/pane-claude-install.txt"
say_cmd Terminal "echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc" "path line: typed"
sl_nap 1.5
say_cmd Terminal 'exit' "exit: typed"
sl_nap 1.0
sl_mark "new terminal: opening"
term_open Terminal $TERM_ARGS
sl_mark "new terminal: open"
sl_nap 1.0
say_cmd Terminal 'claude --version' "claude version: typed"
wait_pane Terminal 'Claude Code\)' 30 && sl_mark "claude version: shown"
sl_nap 3
pane Terminal > "$O/pane-claude-version.txt"
say_cmd Terminal 'curl -LsSf https://astral.sh/uv/0.13.6/install.sh | sh' "uv install: typed"
wait_pane Terminal "everything's installed" 240 && sl_mark "uv install: finished"
sl_nap 3
pane Terminal 200 > "$O/pane-uv-install.txt"
say_cmd Terminal 'exit' "exit 2: typed"
sl_nap 1.0
sl_mark "new terminal 2: opening"
term_open Terminal $TERM_ARGS
sl_mark "new terminal 2: open"
sl_nap 1.0
say_cmd Terminal 'uv --version' "uv version: typed"
wait_pane Terminal 'uv 0\.13' 30 && sl_mark "uv version: shown"
sl_nap 3
pane Terminal > "$O/pane-uv-version.txt"
sl_mark "recording stopped"
sl_stop
sl_shot "$O/end.png"
# Q4 (not filmed): in a terminal opened BEFORE uv was installed, is uvx found? (here: the second terminal's PATH)
bash -ic 'type uvx; uvx --version' > "$O/q4-new-terminal.txt" 2>&1
env -i HOME=$HOME PATH=/usr/local/bin:/usr/bin:/bin bash -c 'export PATH="$HOME/.local/bin:$PATH"; hash -r; type uvx' > "$O/q4-old-terminal-with-path-line.txt" 2>&1
cat ~/.bashrc | tail -4 > "$O/bashrc-tail.txt"
~/.local/bin/claude --version > "$O/claude-version.txt" 2>&1
tmux kill-server 2>/dev/null; sl_display_stop
echo "install take done"
