#!/bin/bash
# fx19 R1 (LAB-fx19 section 4, pre-registered, one run, no retry). FreeCAD 1.1.4 (right) with hook-gap.FCStd open (no
# Pad), the add-on's socket on; Claude Code (left) started with --strict-mcp-config --mcp-config naming ONLY the freecad
# server (the logging proxy around uvx freecad-mcp@0.1.28), model claude-sonnet-5-5, Claude Code's own default (auto)
# mode. One message, typed once; cap $0.25 (lab/costguard.py). After: read-after.json (no AI), after.png, reply,
# tools, session.jsonl, /cost. Started by claude-run/fx19run.sh: the sign-in file mounted read-only at /creds.json,
# copied in, deleted on exit.
set -u
O=/lab/out/fx19/runs/R1
M1='Pad the sketch in this document 20 mm.'
CAP=0.25
[ -e "$O/events.jsonl" ] && { echo "refusing: $O has a run"; exit 1; }
mkdir -p "$O"
unset ANTHROPIC_API_KEY
mkdir -p "$HOME/.claude"; cp /creds.json "$HOME/.claude/.credentials.json"
trap 'rm -f "$HOME/.claude/.credentials.json"' EXIT
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true
mkdir -p ~/fx19 ~/run-fx19; claude_home /home/maker/run-fx19
cp $X/P/hook-gap.FCStd ~/fx19/hook-gap.FCStd
uvx freecad-mcp@0.1.28 --help > /dev/null 2>&1          # the plug's packages fetched before the recording
python3 - "$O" <<'PY'
import json, os, sys
o = sys.argv[1]
e = {'command': 'python3', 'args': ['/lab/proxy/mcp_log_proxy.py', '--log', o + '/transcript.jsonl', '--png-dir', o,
                                   '--', 'uvx', 'freecad-mcp@0.1.28']}
json.dump({'mcpServers': {'freecad': e}}, open(os.path.join(o, 'entry.json'), 'w'), indent=1)
PY
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 DISABLE_AUTOUPDATER=1
claude --version > "$O/claude-version.txt" 2>&1
# never record the owner's claude.ai account connectors
(cd ~/run-fx19 && claude mcp list) 2>&1 | grep -v '^claude\.ai ' > "$O/mcp-list.txt"
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 8
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 1
Q "import FreeCAD, FreeCADGui
d = FreeCAD.openDocument('/home/maker/fx19/hook-gap.FCStd')
for o in d.Objects:
    if o.TypeId in ('Sketcher::SketchObject', 'PartDesign::Body'):
        FreeCADGui.getDocument(d.Name).getObject(o.Name).Visibility = True
FreeCADGui.activateWorkbench('PartDesignWorkbench')
FreeCADGui.activeDocument().activeView().viewIsometric(); FreeCADGui.SendMsgToActiveView('ViewFit')
print(d.Name)" > "$O/setup-rpc.txt" 2>&1
report_hide
sleep 2
SL_SHOT_WAKE=0 sl_shot "$O/before.png"
cd ~/run-fx19
term_open cc 0 0 46 36 30 "claude --model claude-sonnet-5-5 --strict-mcp-config --mcp-config $O/entry.json"
wait_pane cc 'auto mode|❯' 60; sleep 4
pane cc > "$O/pane-start.txt"
xdotool mousemove 2000 700
(cd /lab && python3 -m lab.costguard "$O" cc "$CAP") > "$O/costguard.log" 2>&1 &
sl_record "$O"
sl_mark "recording started: Claude Code (left, FreeCAD plug only), FreeCAD with hook-gap open, no Pad (right)"
sl_nap 2
cd /lab && python3 -m lab.drive "$O" cc "$M1"
sl_nap 3
touch "$O/.guard-stop"
tmux capture-pane -p -J -S -3000 -t cc | sed -e 's/[[:space:]]*$//' > "$O/reply.txt"
sl_mark "recording stopped"; sl_stop
SL_SHOT_WAKE=0 sl_shot "$O/after.png"
python3 - "$O" > "$O/read-after.txt" 2>&1 <<'PY'
import json, sys
sys.path.insert(0, '/lab')
from lab import fcrpc
o = sys.argv[1]
out = fcrpc.run("""import FreeCAD, json
R = {}
for d in FreeCAD.listDocuments().values():
    r = {'file': d.FileName, 'pads': [], 'sketches': [], 'solids': []}
    for x in d.Objects:
        if x.TypeId.startswith('PartDesign::') and 'Pad' in x.TypeId:
            r['pads'].append({'name': x.Name, 'valid': x.isValid(), 'status': x.getStatusString(),
                              'volume': None if x.Shape.isNull() else x.Shape.Volume})
        elif x.TypeId == 'Sketcher::SketchObject':
            ends = []
            for g in x.Geometry:
                if hasattr(g, 'StartPoint'):
                    ends += [g.StartPoint, g.EndPoint]
            open_v = [(round(p.x, 4), round(p.y, 4)) for p in ends if sum((p - q).Length < 1e-6 for q in ends) == 1]
            r['sketches'].append({'name': x.Name, 'wires_closed': [w.isClosed() for w in x.Shape.Wires],
                                  'open_vertices': open_v, 'constraints': len(x.Constraints), 'dof': x.DoF})
        elif hasattr(x, 'Shape') and x.TypeId in ('Part::Extrusion', 'PartDesign::Body', 'Part::Feature'):
            r['solids'].append({'name': x.Name, 'type': x.TypeId, 'valid': x.isValid(),
                                'volume': None if x.Shape.isNull() else x.Shape.Volume})
    R[d.Name] = r
print(json.dumps(R))""")
json.dump(json.loads(out), open(o + '/read-after.json', 'w'), indent=1)
print(out[:2000])
PY
python3 - "$O" > "$O/tools.txt" 2>&1 <<'PY'
import json, sys
o = sys.argv[1]
for ln in open(o + '/transcript.jsonl', encoding='utf-8'):
    try:
        r = json.loads(ln)
    except ValueError:
        continue
    m = r.get('msg') or {}
    if m.get('method') == 'tools/call':
        print('CALL', json.dumps(m.get('params'))[:3000])
    elif 'result' in m and isinstance(m['result'], dict) and 'content' in m['result']:
        print('REPLY', json.dumps(m['result'])[:3000])
PY
cp ~/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
grep -o '"model":"[^"]*"' "$O/session.jsonl" | sort | uniq -c > "$O/model.txt"
tmux send-keys -t cc Escape; sleep 1
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
pane cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
rm -f "$HOME/.claude/.credentials.json"
fc_quit; tmux kill-server 2>/dev/null; sl_display_stop
echo "R1 done"
