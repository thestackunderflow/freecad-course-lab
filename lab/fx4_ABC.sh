#!/bin/bash
# fx4 takes A, B, C, E0 (LAB-fx4 sections 3.A-3.C, 3.E0): one fresh home, one filmed terminal, three recordings.
#   FCC_PREFIX=fx4 tools/run.sh lab/fx4_ABC.sh        (PREREG=<commit> in FCC_DOCKER_ARGS="-e PREREG=...")
set -u
. /lab/lab/common.sh; . /lab/lab/fx4_lib.sh
mkdir -p $X/A $X/B $X/C $X/E
cd ~
export PATH="$HOME/.local/bin:$PATH"
cp /opt/pre/claude "$HOME/.local/bin/" 2>/dev/null || { mkdir -p ~/.local/bin; cp /opt/pre/claude ~/.local/bin/; }
# ---- pins (before take A) and state building (not filmed)
{ claude --version; echo "prereg commit $PREREG"; cat /etc/os-release | head -4; date -u; } > /tmp/pins-a.txt 2>&1
curl -LsSf https://astral.sh/uv/0.13.6/install.sh | sh > $X/A/uv-install.txt 2>&1
export PATH="$HOME/.local/bin:$PATH"; hash -r
{ uv --version; cat /tmp/pins-a.txt; } > $X/pins.txt
home_init
uv cache dir > $X/A/uv-cache-dir.txt 2>&1
ls -la "$(uv cache dir)" > $X/A/cache-before.txt 2>&1
claude mcp list > $X/C/mcp-list-before.txt 2>&1
sl_display $W $H
term_start

# ================= take A
O=$X/A
sl_record "$O" nomouse; sl_mark "recording started: a terminal, uv installed, cache empty"; sl_nap 1.5
run_wait 'uvx freecad-mcp@0.1.19' "0.1.19: typed" "0.1.19: traceback last line" $O/traceback-0.1.19.txt 120
SL_SHOT_WAKE=0 sl_shot $O/traceback-full.png
sl_nap 15
run_timed 'timeout 8 uvx freecad-mcp@0.1.20; echo "exit=$?"' "0.1.20: typed" "0.1.20: waits" $O/0.1.20.txt 7.5
sl_nap 4
sl_mark "recording stopped"; stamp $O
cp $O/0.1.20.txt $O/0.1.20-exit.txt
tail -n 1 $O/traceback-0.1.19.txt | tee $O/last-line.txt
wc -c $O/last-line.txt | tee $O/last-line-chars.txt
grep -c "This is mcp 2" $O/last-line.txt | tee $O/last-line-form.txt
cd /lab
python3 -I tools/test_mcp.py uvx freecad-mcp@0.1.20 2>&1 | tee $O/test-0.1.20.txt
python3 -I tools/test_mcp.py uvx freecad-mcp@0.1.19 2>&1 | tee $O/test-0.1.19.txt
ls -la "$(uv cache dir)" 2>&1 | tee $O/cache-after.txt
cd ~

# ================= take B
O=$X/B
sl_record "$O" nomouse; sl_mark "recording started: the home of take A"; sl_nap 1.5
PYV="python -c \"import importlib.metadata as m; print(m.version('mcp'))\""
run_wait "uvx --from freecad-mcp@0.1.19 $PYV" "metadata 0.1.19: typed" "metadata: 2.x printed" $O/metadata-0.1.19.txt 120
sl_nap 6
run_wait "uvx --with \"mcp[cli]<2\" --from freecad-mcp@0.1.19 $PYV" "metadata pinned: typed" "metadata pinned: 1.x printed" $O/metadata-pinned.txt 120
sl_nap 6
run_wait "uvx --from freecad-mcp@0.1.28 python -c \"import importlib.metadata as m; print(m.version('mcp')); print(m.requires('freecad-mcp'))\"" "metadata 0.1.28: typed" "metadata 0.1.28: printed" $O/metadata-0.1.28.txt 120
sl_nap 6
sl_mark "recording stopped"; stamp $O
cp $O/metadata-0.1.19.txt $X/pins-mcp-resolved.txt
echo "mcp resolved by 0.1.19 today: $(tail -n 1 $O/metadata-0.1.19.txt)" | tee -a $X/pins.txt

# ================= take C
O=$X/C
sl_record "$O" nomouse; sl_mark "recording started: the home of take B, Claude Code installed"; sl_nap 1.5
run_timed 'timeout 8 uvx --with "mcp[cli]<2" freecad-mcp@0.1.19; echo "exit=$?"' "pinned 0.1.19: typed" "pinned 0.1.19: waits" $O/pinned-0.1.19.txt 7.5
cp $O/pinned-0.1.19.txt $O/pinned-0.1.19-exit.txt
sl_nap 3
run_wait 'claude mcp add --scope user freecad -- uvx freecad-mcp@0.1.28' "add 0.1.28: typed" "add 0.1.28: done" $O/add-0.1.28.txt 60
sl_nap 2
typ 'claude mcp list' "list: typed"
end=$(( $(date +%s) + 120 ))
until tmux capture-pane -p -t cc | grep -qE 'Connected|Failed'; do [ "$(date +%s)" -ge "$end" ] && break; sleep 0.3; done
sl_mark "list: Connected"
wait_prompt 60; save_out $O/list.txt
sl_nap 20
typ 'claude mcp get freecad' "your turn get: typed"
wait_prompt 60; sl_mark "get freecad: printed"; save_out $O/get-freecad.txt
sl_nap 27
typ 'claude mcp list' "list 2: typed"
wait_prompt 90; sl_mark "list 2: printed"; save_out $O/list-2.txt
sl_nap 20
sl_mark "recording stopped"; stamp $O
cd /lab
python3 -I tools/test_mcp.py uvx --with "mcp[cli]<2" freecad-mcp@0.1.19 2>&1 | tee $O/test-pinned.txt
cat ~/.claude.json | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin).get('mcpServers'), indent=1))" | tee $O/user-config-mcp.txt
cd ~

# ================= E0 (text checks, no recording)
O=$X/E
ls /usr/bin/python3* | tee $O/E0-ls-python.txt
python3 --version 2>&1 | tee -a $O/E0-ls-python.txt
uv python list 2>&1 | tee $O/E0-uv-python-list.txt | head -20
uv python find 3.12 2>&1 | tee $O/E0-uv-find-312.txt
uv python find 3.11 2>&1 | tee $O/E0-uv-find-311.txt

tmux kill-server 2>/dev/null; sl_display_stop
echo "ABC done"
