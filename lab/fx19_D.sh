#!/bin/bash
# fx19 take D (LAB-fx19 3.D): MCP, no AI. FreeCAD running (socket on, behind), a full-window terminal: `python3 noai.py`
# sends two execute_code calls through the plug (uvx freecad-mcp@0.1.28): no prints, then the two prints.
# The plug's packages come from a uv cache warmed beforehand (WARM=1 run, network on); the take itself has no network.
#   FCC_PREFIX=fx19 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fx19_D.sh
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh
export UV_CACHE_DIR=/lab/out/scratch/uvcache-fx19
tools_install
if [ -n "${WARM:-}" ]; then uvx freecad-mcp@0.1.28 --help > /dev/null 2>&1; echo "warm exit $?"; exit 0; fi
export UV_OFFLINE=1
O=$X/D; L=$O/take.log; : > $L
fx_start $O
mkdir -p ~/fx19; for n in 1 2; do cp $X/P/hook-gap.FCStd ~/fx19/gap-$n.FCStd; done
cp $O/noai.py ~/fx19/noai.py
printf 'export PATH="$HOME/.local/bin:$PATH"\nexport UV_CACHE_DIR=%s UV_OFFLINE=1\nPS1="$ "\n' "$UV_CACHE_DIR" >> ~/.bashrc
cd ~/fx19
term_open cc 0 0 120 40 30 bash
term_focus cc; sleep 1
xdotool mousemove 2700 1700
sl_record "$O" nomouse; sl_mark "recording started: a terminal in ~/fx19 (FreeCAD running behind it, socket on)"
sl_nap 3
say_cmd cc 'python3 noai.py' "noai: typed"
wait_pane cc '=== call 2' 200; wait_pane cc 'isError.*\n*.*' 5
end=$(( $(date +%s) + 200 )); until [ "$(pane cc | grep -c '^isError')" -ge 2 ]; do [ "$(date +%s)" -ge "$end" ] && break; sleep 0.5; done
sl_mark "both replies printed"; sl_nap 8
SL_SHOT_WAKE=0 sl_shot $O/replies.png
sl_mark "recording stopped"; sl_stop
tmux capture-pane -J -p -S - -t cc | sed -e 's/[[:space:]]*$//' > $O/reply.txt
Q "import FreeCAD
print([(d.Name, d.getObject('Pad').isValid(), d.getObject('Pad').getStatusString()) for d in FreeCAD.listDocuments().values() if d.getObject('Pad')])" >> $L 2>&1
tmux kill-server 2>/dev/null; fc_quit; sl_display_stop
echo "D done"
