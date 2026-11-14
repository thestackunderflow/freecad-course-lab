#!/bin/bash
# fx20 take D (LAB-fx20 3.D), filmed like fx19 D2: terminal left (86 cols, 30 px), FreeCAD right; then FreeCAD full window
# Same plug, uv cache warmed for fx19 (out/scratch/uvcache-fx19), no network, no AI. Calls: out/fx20/D/noai.py.
#   FCC_PREFIX=fx20 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fx20_D.sh
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh
export UV_CACHE_DIR=/lab/out/scratch/uvcache-fx19
tools_install
export UV_OFFLINE=1
O=$X/D; L=$O/take.log; : > $L
fx_start $O
place "FreeCAD 1.1.4" 1700 0 1180 1800; sleep 1
report_hide
mkdir -p ~/fx20; for n in 1 2; do cp $X/P/hook.FCStd ~/fx20/size-$n.FCStd; cp $X/P/hook-red.FCStd ~/fx20/red-$n.FCStd; done
cp $O/noai.py ~/fx20/noai.py
printf 'export PATH="$HOME/.local/bin:$PATH"\nexport UV_CACHE_DIR=%s UV_OFFLINE=1\nPS1="$ "\n' "$UV_CACHE_DIR" >> ~/.bashrc
cd ~/fx20
term_open cc 0 0 86 46 30 bash
term_focus cc; sleep 1
xdotool mousemove 2700 1700
sl_record "$O" nomouse; sl_mark "recording started: a terminal in ~/fx20 (left), FreeCAD with its socket on (right)"
sl_nap 3
say_cmd cc 'python3 noai.py' "noai: typed"
wait_pane cc '=== call 4' 200
term_focus cc
end=$(( $(date +%s) + 200 )); until [ "$(pane cc | grep -c '^isError')" -ge 4 ]; do [ "$(date +%s)" -ge "$end" ] && break; sleep 0.5; done
sl_mark "both replies printed"; sl_nap 10
SL_SHOT_WAKE=0 sl_shot $O/replies.png
# FreeCAD full window, red-2's sketch open in edit (a lab query: the person's double-click is take A's, F4 left)
place "FreeCAD 1.1.4" 0 0 2880 1800; sleep 0.5
Q "import FreeCADGui
FreeCADGui.getDocument('red_2').setEdit('Sketch')
FreeCADGui.SendMsgToActiveView('ViewFit')
print('edit')" >> $L 2>&1
sl_mark "FreeCAD full window: red-2's sketch, Over-constrained"; sl_nap 8
SL_SHOT_WAKE=0 sl_shot $O/red.png
solver_text >> $L 2>&1
sl_mark "recording stopped"; sl_stop
tmux capture-pane -J -p -S - -t cc | sed -e 's/[[:space:]]*$//' > $O/reply.txt
Q "import FreeCAD
print([(d.Name, d.getObject('Pad').isValid(), d.getObject('Sketch').solve(), len(d.getObject('Sketch').Constraints), d.getObject('Sketch').Geometry[4].length()) for d in FreeCAD.listDocuments().values() if d.getObject('Pad')])" >> $L 2>&1
tmux kill-server 2>/dev/null; fc_quit; sl_display_stop
echo "D done"
