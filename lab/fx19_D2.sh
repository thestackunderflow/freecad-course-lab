#!/bin/bash
# fx19 take D2 (pickup of take D, 14 Nov render stage): take D's terminal was never readable on film (xterm font too
# small for the frame, then FreeCAD raised over it when noai.py opened gap-1/gap-2, from ~7.5 s; replies.png shows
# FreeCAD only). D2 = the same noai.py calls, filmed as R1 is: the terminal on the left (86 cols, 30 px),
# FreeCAD placed on the right (x 1700-2880; attempt 1 at 1450 clipped the 76-column reply line), so nothing covers the replies. Same plug, same cache, no network, no AI.
#   FCC_PREFIX=fx19 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fx19_D2.sh
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh
export UV_CACHE_DIR=/lab/out/scratch/uvcache-fx19
tools_install
export UV_OFFLINE=1
O=$X/D2; L=$O/take.log; : > $L
fx_start $O
place "FreeCAD 1.1.4" 1700 0 1180 1800; sleep 1
report_hide
mkdir -p ~/fx19; for n in 1 2; do cp $X/P/hook-gap.FCStd ~/fx19/gap-$n.FCStd; done
cp $O/noai.py ~/fx19/noai.py
printf 'export PATH="$HOME/.local/bin:$PATH"\nexport UV_CACHE_DIR=%s UV_OFFLINE=1\nPS1="$ "\n' "$UV_CACHE_DIR" >> ~/.bashrc
cd ~/fx19
term_open cc 0 0 86 46 30 bash
term_focus cc; sleep 1
xdotool mousemove 2700 1700
sl_record "$O" nomouse; sl_mark "recording started: a terminal in ~/fx19 (left), FreeCAD with its socket on (right)"
sl_nap 3
say_cmd cc 'python3 noai.py' "noai: typed"
wait_pane cc '=== call 2' 200
term_focus cc
end=$(( $(date +%s) + 200 )); until [ "$(pane cc | grep -c '^isError')" -ge 2 ]; do [ "$(date +%s)" -ge "$end" ] && break; sleep 0.5; done
sl_mark "both replies printed"; sl_nap 10
SL_SHOT_WAKE=0 sl_shot $O/replies.png
sl_mark "recording stopped"; sl_stop
tmux capture-pane -J -p -S - -t cc | sed -e 's/[[:space:]]*$//' > $O/reply.txt
Q "import FreeCAD
print([(d.Name, d.getObject('Pad').isValid(), d.getObject('Pad').getStatusString()) for d in FreeCAD.listDocuments().values() if d.getObject('Pad')])" >> $L 2>&1
tmux kill-server 2>/dev/null; fc_quit; sl_display_stop
echo "D2 done"
