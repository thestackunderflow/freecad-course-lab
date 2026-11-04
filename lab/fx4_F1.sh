#!/bin/bash
# fx4 take F1 (LAB-fx4 section 3.F1): a July state built with --exclude-newer, then uv cache clean, then the same line today.
# Cold runs use timeout 30 (not 8): the first install of a set of parts takes longer than 8 s; "starts" = Installed line
# printed, no traceback, exit 124 (deviation noted in ANSWERS.md).
#   tools/run_fx4.sh f1 lab/fx4_F1.sh
set -u
. /lab/lab/common.sh; . /lab/lab/fx4_lib.sh
O=$X/F1; mkdir -p $O
cd ~
cp /opt/pre/claude "$HOME/.local/bin/" 2>/dev/null || { mkdir -p ~/.local/bin; cp /opt/pre/claude ~/.local/bin/; }
curl -LsSf https://astral.sh/uv/0.13.6/install.sh | sh > $O/uv-install.txt 2>&1
export PATH="$HOME/.local/bin:$PATH"; hash -r
home_init
ls -la "$(uv cache dir)" > $O/cache-0.txt 2>&1
D=2026-07-27T00:00:00Z
sl_display $W $H
term_start
sl_record "$O" nomouse; sl_mark "recording started: fresh home, uv installed, cache empty"; sl_nap 1.5
run_timed "timeout 30 uvx --exclude-newer $D freecad-mcp@0.1.19; echo \"exit=\$?\"" "july run: typed" "july run: waits" $O/july-run.txt 15
cp $O/july-run.txt $O/july-run-exit.txt
run_wait "uvx --exclude-newer $D --from freecad-mcp@0.1.19 python -c \"import importlib.metadata as m; print(m.version('mcp'))\"" "july version: typed" "july version: printed" $O/july-mcp-version.txt 120
run_timed 'timeout 30 uvx freecad-mcp@0.1.19; echo "exit=$?"' "old copy: typed" "old copy: waits" $O/reuse-run.txt 15
cp $O/reuse-run.txt $O/reuse-run-exit.txt
find "$(uv cache dir)" -maxdepth 2 -name "*environ*" > $O/cache-1.txt 2>&1; ls -la "$(uv cache dir)"/environments-v* >> $O/cache-1.txt 2>&1
if grep -q 'Traceback (most recent call last)' $O/reuse-run.txt; then
  echo "uvx re-resolved on the unflagged line (traceback); baseline = installed tool" > $O/baseline.txt
  run_wait "uv tool install --exclude-newer $D freecad-mcp@0.1.19" "tool install: typed" "tool install: done" $O/tool-install-july.txt 120
  run_timed 'timeout 30 freecad-mcp; echo "exit=$?"' "tool run before: typed" "tool run before: waits" $O/tool-run-before.txt 10
  cp $O/tool-run-before.txt $O/tool-run-before-exit.txt
else
  echo "uvx reused the July environment on the unflagged line (no traceback); baseline = uvx env" > $O/baseline.txt
fi
run_wait 'uv cache clean' "cache clean: typed" "cache clean: done" $O/cache-clean.txt 120
ls -la "$(uv cache dir)" > $O/cache-2.txt 2>&1
run_timed 'timeout 30 uvx freecad-mcp@0.1.19; echo "exit=$?"' "after clean: typed" "after clean: waits" $O/after-clean-run.txt 15
cp $O/after-clean-run.txt $O/after-clean-run-exit.txt
grep -q 'Traceback (most recent call last)' $O/after-clean-run.txt && sl_mark "after clean: traceback"
if [ -f $O/tool-run-before.txt ]; then
  run_timed 'timeout 30 freecad-mcp; echo "exit=$?"' "tool run after: typed" "tool run after: waits" $O/tool-run-after.txt 10
  cp $O/tool-run-after.txt $O/tool-run-after-exit.txt
  uv tool list > $O/tool-list-after.txt 2>&1
fi
sl_nap 3
sl_mark "recording stopped"; stamp $O
tmux kill-server 2>/dev/null; sl_display_stop
echo "F1 done"
