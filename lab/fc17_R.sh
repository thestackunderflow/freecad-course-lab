#!/bin/bash
# fc17 Claude runs A1 / B1 (PLAN 2026-11-21-cad-lesson-17 2.5 rev 2, out/fc17/PREREG.md). Copied from lab/fc16_R.sh.
# FreeCAD 1.1.4 (right) with cup.FCStd open (out/fc17/P/mirror-xz.FCStd: lesson 16 fixed cup, peg moved to peg_x 15,
# Mirrored of Pad001 across the Base XZ plane: the copy sticks out 13 behind the back wall), the add-on socket on; Claude Code (left) with --strict-mcp-config --mcp-config naming ONLY the
# freecad server (logging proxy around uvx freecad-mcp@0.1.28), model claude-sonnet-5-5, --max-budget-usd CAP
# --max-turns 40; live guard lab/costguard.py.
# The recording starts only after Claude Code's start banner has gone (~24 s): 30 s wait, then checked.
# Started by claude-run/fc17run.sh RUN: API key in the env var ANTHROPIC_API_KEY only (never written; the key prompt
# answered by keys before recording, its screen never saved); ~/.claude/settings.json claudeMdExcludes /lab/**.
set -u
RUN=$1; O=/lab/out/fc17/runs/$RUN
A1="I mirrored the key peg on my wall cup to make a second one, but the copy came out of the back. Fix it so the two pegs sit side by side on the front, the same distance either side of the middle, and stay that way if I move the peg."
B1="$A1 Then check where both pegs are, and the back of the cup, and tell me what you find."
case $RUN in A1) M1=$A1;; B1) M1=$B1;; *) echo "RUN A1|B1"; exit 2;; esac
CAP=${CAP:-0.25}
[ -e "$O/events.jsonl" ] && { echo "refusing: $O has a run"; exit 1; }
mkdir -p "$O"; echo "$M1" > "$O/prompt.txt"
[ -n "${ANTHROPIC_API_KEY:-}" ] || { echo "no API key in the env"; exit 2; }
mkdir -p "$HOME/.claude"
printf '{"claudeMdExcludes": ["/lab/**"]}
' > "$HOME/.claude/settings.json"
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh; . /lab/lab/fc12_lib.sh; . /lab/lab/fc13_lib.sh; . /lab/lab/fc14_lib.sh; . /lab/lab/fc15_lib.sh; . /lab/lab/fc16_lib.sh; . /lab/lab/fc17_lib.sh
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true
mkdir -p ~/fc17 ~/run-fc17; claude_home /home/maker/run-fc17
cp $X/P/mirror-xz.FCStd ~/fc17/cup.FCStd
uvx freecad-mcp@0.1.28 --help > /dev/null 2>&1
python3 - "$O" <<'PY'
import json, os, sys
o = sys.argv[1]
e = {'command': 'python3', 'args': ['/lab/proxy/mcp_log_proxy.py', '--log', o + '/transcript.jsonl', '--png-dir', o,
                                   '--', 'uvx', 'freecad-mcp@0.1.28']}
json.dump({'mcpServers': {'freecad': e}}, open(os.path.join(o, 'entry.json'), 'w'), indent=1)
PY
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 DISABLE_AUTOUPDATER=1
claude --version > "$O/claude-version.txt" 2>&1
timeout 60 claude mcp list --strict-mcp-config --mcp-config "$O/entry.json" 2>&1 | grep -v -i "^claude.ai" > "$O/mcp-list.txt"
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 8
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 1
Q "import FreeCAD, FreeCADGui
d = FreeCAD.openDocument('/home/maker/fc17/cup.FCStd')
print(d.Name)" > "$O/setup-rpc.txt" 2>&1
FQ "prep('cup')" >> "$O/setup-rpc.txt" 2>&1
Q "import FreeCAD, FreeCADGui
FreeCADGui.getDocument('cup').getObject('Body').ShapeAppearance = [FreeCAD.Material(DiffuseColor=(0.93, 0.55, 0.20))]
print(1)" >> "$O/setup-rpc.txt" 2>&1
report_hide; sleep 2
SL_SHOT_WAKE=0 sl_shot "$O/before.png"
cd ~/run-fc17
term_open cc 0 0 46 36 30 "claude --model claude-sonnet-5-5 --strict-mcp-config --mcp-config $O/entry.json --max-budget-usd $CAP --max-turns 40"
wait_pane cc 'API key|auto mode|❯' 60
for i in 1 2 3; do   # the custom API key prompt (default No): Up to "Yes", Enter; its screen is never saved
  if pane cc | grep -q -i 'api key'; then tmux send-keys -t cc Up; sleep 0.5; tmux send-keys -t cc Enter; sleep 3; fi
done
pane cc | grep -q -i 'api key' && echo "key prompt still up" > "$O/key-prompt.txt"
wait_pane cc 'auto mode|❯' 60; sleep 30
pane cc > "$O/pane-start.txt"
grep -c -i "ul""tra" "$O/pane-start.txt" > "$O/banner-check.txt"
xdotool mousemove 2000 700
(cd /lab && python3 -m lab.costguard "$O" cc "$CAP") > "$O/costguard.log" 2>&1 &
sl_record "$O"
sl_mark "recording started: Claude Code (left, FreeCAD plug only), FreeCAD with cup open (right)"
sl_nap 2
cd /lab && python3 -m lab.drive "$O" cc "$M1"
sl_nap 3
touch "$O/.guard-stop"
tmux capture-pane -p -J -S -3000 -t cc | sed -e 's/[[:space:]]*$//' > "$O/reply.txt"
sl_mark "recording stopped"; sl_stop
SL_SHOT_WAKE=0 sl_shot "$O/after.png"
Q "import FreeCAD; print('\n'.join(d.Name for d in FreeCAD.listDocuments().values()))" > "$O/docs.txt" 2>&1
for d in $(cat "$O/docs.txt"); do lab_save "$d" "$O/after-$d.FCStd" >> "$O/save.log" 2>&1; done
python3 - "$O" > "$O/tools.txt" 2>&1 <<'PY'
import json, sys
o = sys.argv[1]
for ln in open(o + '/transcript.jsonl', encoding='utf-8'):
    try:
        r = json.loads(ln)
    except ValueError:
        continue
    m = r.get('msg') if isinstance(r, dict) else None
    if not isinstance(m, dict):
        continue
    if m.get('method') == 'tools/call':
        print('CALL', json.dumps(m.get('params'))[:3000])
    elif 'result' in m and isinstance(m['result'], dict) and 'content' in m['result']:
        print('REPLY', json.dumps(m['result'])[:3000])
PY
mkdir -p /lab/out/scratch/fc17; cp ~/.claude/projects/*/*.jsonl "/lab/out/scratch/fc17/$RUN-session.jsonl" 2>/dev/null   # account e-mail inside: never in out/
grep -o '"model":"[^"]*"' "/lab/out/scratch/fc17/$RUN-session.jsonl" | sort | uniq -c > "$O/model.txt"
tmux send-keys -t cc Escape; sleep 1
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
pane cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
fc_quit; tmux kill-server 2>/dev/null; sl_display_stop
# our checks on Claude's file (PLAN 2.5): as saved, recomputed, peg_x 15 / 20 / 8, wall 3
for f in "$O"/after-*.FCStd; do [ -e "$f" ] && check17 "$f" "${f%.FCStd}.check.json" >> "$O/check.log"; done
[ -e "$O/after-cup.check.json" ] && cp "$O/after-cup.check.json" "$O/after.check.json"
echo "$RUN done"
