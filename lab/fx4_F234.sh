#!/bin/bash
# fx4 takes F2, F3, F4 (LAB-fx4 sections 3.F2-3.F4) in one fresh container: a new machine, a re-synced clone, an unpinned line.
# Cold runs use timeout 30 (not 8) and the checkout is entered with cd (not --directory): short commands on a 46-column
# screen (deviations noted in ANSWERS.md).
#   tools/run_fx4.sh f234 lab/fx4_F234.sh
set -u
. /lab/lab/common.sh; . /lab/lab/fx4_lib.sh
mkdir -p $X/F2 $X/F3 $X/F4
cd ~
cp /opt/pre/claude "$HOME/.local/bin/" 2>/dev/null || { mkdir -p ~/.local/bin; cp /opt/pre/claude ~/.local/bin/; }
curl -LsSf https://astral.sh/uv/0.13.6/install.sh | sh > $X/F2/uv-install.txt 2>&1
export PATH="$HOME/.local/bin:$PATH"; hash -r
home_init
ls -la ~/.cache ~/.local ~/.local/share 2>&1 > $X/F2/home-before.txt
sl_display $W $H
term_start
J=2026-07-27T00:00:00Z

# ================= F2: a new machine
O=$X/F2
sl_record "$O" nomouse; sl_mark "recording started: a brand-new machine, uv installed"; sl_nap 1.5
run_timed 'timeout 30 uvx freecad-mcp@0.1.19; echo "exit=$?"' "new machine: typed" "new machine: waits" $O/new-machine-run.txt 15
cp $O/new-machine-run.txt $O/new-machine-run-exit.txt
grep -q 'Traceback (most recent call last)' $O/new-machine-run.txt && sl_mark "new machine: traceback"
run_wait "uvx --from freecad-mcp@0.1.19 python -c \"import importlib.metadata as m; print(m.version('mcp'))\"" "new machine version: typed" "new machine version: printed" $O/new-machine-mcp-version.txt 120
sl_nap 3
sl_mark "recording stopped"; stamp $O

# ================= F3: a re-synced clone
O=$X/F3
cd /lab
python3 -m pip download --no-deps --no-binary :all: --ignore-requires-python freecad-mcp==0.1.19 -d $O/sdist 2>&1 | tee $O/sdist-download.txt | tail -5
if ! ls $O/sdist/*.tar.gz > /dev/null 2>&1; then
  echo "pip download gave no sdist; curl from PyPI instead" | tee -a $O/sdist-download.txt
  mkdir -p $O/sdist
  URL=$(curl -s https://pypi.org/pypi/freecad-mcp/0.1.19/json | python3 -c "import json,sys; print([u['url'] for u in json.load(sys.stdin)['urls'] if u['packagetype']=='sdist'][0])")
  curl -sL "$URL" -o $O/sdist/$(basename "$URL")
fi
ls $O/sdist | tee -a $O/sdist-download.txt
mkdir -p ~/checkout && tar -xzf $O/sdist/*.tar.gz -C ~/checkout --strip-components=1
ls -la ~/checkout | tee $O/checkout-ls.txt
grep -n "mcp\|requires-python" ~/checkout/pyproject.toml | tee $O/pyproject-lines.txt
cd ~
mcpline() { grep -n -A2 '^name = "mcp"' "$1" 2>&1; }
sl_record "$O" nomouse; sl_mark "recording started: an old checkout, July state"; sl_nap 1.5
term_focus cc; tmux send-keys -t cc "cd ~/checkout" Enter; sleep 0.6
run_wait "uv lock --exclude-newer $J" "lock july: typed" "lock july: done" $O/lock-july.txt 180
mcpline ~/checkout/uv.lock | tee $O/lock-july-mcp.txt; cp ~/checkout/uv.lock $O/lock-july.lock
run_wait "uv sync" "sync july: typed" "sync july: done" $O/sync-july.txt 240
run_timed 'timeout 30 uv run freecad-mcp; echo "exit=$?"' "clone july: typed" "clone july: waits" $O/run-july.txt 15
cp $O/run-july.txt $O/run-july-exit.txt
# (i) the lock is committed and the user re-syncs today
cp -r ~/checkout ~/checkout-i; rm -rf ~/checkout-i/.venv
tmux send-keys -t cc "cd ~/checkout-i" Enter; sleep 0.6
run_wait "uv sync" "resync locked: sync typed" "resync locked: sync done" $O/sync-i.txt 240
run_timed 'timeout 30 uv run freecad-mcp; echo "exit=$?"' "resync locked: typed" "resync locked: waits" $O/run-i.txt 15
cp $O/run-i.txt $O/run-i-exit.txt
# (ii) the user upgrades
run_wait "uv sync --upgrade" "resync upgrade sync: typed" "resync upgrade sync: done" $O/sync-ii.txt 240
mcpline ~/checkout-i/uv.lock | tee $O/lock-ii-mcp.txt; cp ~/checkout-i/uv.lock $O/lock-ii.lock
run_timed 'timeout 30 uv run freecad-mcp; echo "exit=$?"' "resync upgrade: typed" "resync upgrade: waits" $O/run-ii.txt 15
cp $O/run-ii.txt $O/run-ii-exit.txt
# (iii) no lock file in the clone
cp -r ~/checkout ~/checkout-iii; rm -rf ~/checkout-iii/.venv ~/checkout-iii/uv.lock
tmux send-keys -t cc "cd ~/checkout-iii" Enter; sleep 0.6
run_wait "uv sync" "resync nolock sync: typed" "resync nolock sync: done" $O/sync-iii.txt 240
mcpline ~/checkout-iii/uv.lock | tee $O/lock-iii-mcp.txt; cp ~/checkout-iii/uv.lock $O/lock-iii.lock
run_timed 'timeout 30 uv run freecad-mcp; echo "exit=$?"' "resync nolock: typed" "resync nolock: waits" $O/run-iii.txt 15
cp $O/run-iii.txt $O/run-iii-exit.txt
# (iv) the old-video form on the July checkout after its .venv is removed
rm -rf ~/checkout/.venv
tmux send-keys -t cc "cd ~/checkout" Enter; sleep 0.6
run_timed 'timeout 60 uv run freecad-mcp; echo "exit=$?"' "uv run old form: typed" "uv run old form: waits" $O/run-iv.txt 30
cp $O/run-iv.txt $O/run-iv-exit.txt
sl_nap 3
sl_mark "recording stopped"; stamp $O
tmux send-keys -t cc "cd ~" Enter; sleep 0.5

# ================= F4: no version pinned, after the cache is gone
O=$X/F4
sl_record "$O" nomouse; sl_mark "recording started: the container of F3"; sl_nap 1.5
run_wait 'uv cache clean' "cache clean: typed" "cache clean: done" $O/cache-clean.txt 120
ls -la "$(uv cache dir)" > $O/cache-after-clean.txt 2>&1
run_timed 'timeout 60 uvx freecad-mcp; echo "exit=$?"' "unpinned: typed" "unpinned: waits" $O/unpinned-run.txt 30
cp $O/unpinned-run.txt $O/unpinned-run-exit.txt
grep -q 'Traceback (most recent call last)' $O/unpinned-run.txt && sl_mark "unpinned: traceback"
VPY="python -c \"import importlib.metadata as m; print(m.version('freecad-mcp'), m.version('mcp'))\""
run_wait "uvx --from freecad-mcp $VPY" "unpinned versions: typed" "unpinned versions: printed" $O/unpinned-versions.txt 120
run_timed "timeout 30 uvx --exclude-newer $J freecad-mcp; echo \"exit=\$?\"" "unpinned july: typed" "unpinned july: waits" $O/unpinned-july.txt 15
cp $O/unpinned-july.txt $O/unpinned-july-exit.txt
run_wait "uvx --exclude-newer $J --from freecad-mcp $VPY" "unpinned july versions: typed" "unpinned july versions: printed" $O/unpinned-july-versions.txt 120
sl_nap 3
sl_mark "recording stopped"; stamp $O
tmux kill-server 2>/dev/null; sl_display_stop
echo "F234 done"
