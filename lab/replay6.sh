#!/bin/bash
# Lesson 6, lab L6-Q5 (no AI, free): a fresh FreeCAD 1.1.4 window (same image) with lesson 5's hook opened under the
# same file name (~/hook-lesson5.FCStd); every MCP tools/call the run logged (all turns, in order) replayed over the
# same plug (`uvx freecad-mcp@0.1.28`, our own client). Then every open document saved, read (checker/l6read) and
# scored (checker/score_l6) exactly like the run; pass = the same verdict on every line and the volume within 0.01 mm3.
# Calls Claude Code made through its own tools (Bash, Write ...) are not in the MCP log: a run whose change came that
# way is labelled "not replayable" (the take's transcript holds no change call).
#   FCC_PREFIX=fc6 tools/run.sh lab/replay6.sh B1
set -u
. /lab/lab/common.sh
RUN=${1:-B1}
R=/lab/out/l6/runs/$RUN
O=/lab/out/l6/replay-$RUN; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 8
cd /lab
cp /lab/out/l4/hand/width30.FCStd ~/hook-lesson5.FCStd
python3 -m lab.opendoc /home/maker/hook-lesson5.FCStd > "$O/opendoc.txt" 2>&1
python3 -m client.replay "$R/transcript.jsonl" "$O/replay.json" -- uvx freecad-mcp@0.1.28 > "$O/replay.log" 2>&1
sleep 2
python3 -m lab.fcrpc docs > "$O/docs.json" 2>&1
python3 - "$O" <<'PY' > "$O/saves.txt" 2>&1
import json, sys
sys.path.insert(0, '/lab')
from lab import fcrpc
o = sys.argv[1]
for name in json.load(open(o + '/docs.json')):
    print(name, fcrpc.run(fcrpc.SAVE.format(doc=name, path='/tmp/after-%s.FCStd' % name)))
PY
fc_quit; sl_display_stop
for f in /tmp/after-*.FCStd; do
  n=$(basename "$f" .FCStd); n=${n#after-}
  FC_DOC="$f" FC_OUT="$O/read-$n.json" freecadcmd /lab/checker/l6read.py > "$O/read-$n.log" 2>&1
done
python3 - "$R" "$O" > "$O/compare.json" <<'PY'
import json, os, sys
sys.path.insert(0, '/lab')
from checker import score_l6
run, rep = sys.argv[1], sys.argv[2]
a = json.load(open(os.path.join(run, 'score.json')))
b = score_l6.score_run(rep)
changes = [c for c in a.get('calls') or [] if c['tool'] in ('execute_code', 'edit_object', 'create_object', 'delete_object')]
out = {'run': {'pass': a['pass'], 'lines': a['lines'], 'volume_mm3': a.get('volume_mm3')},
       'replay': {'pass': b['pass'], 'lines': b['lines'], 'volume_mm3': b.get('volume_mm3')},
       'replayable': bool(changes)}
out['match'] = bool(out['replayable'] and a['lines'] == b['lines'] and a.get('volume_mm3') is not None
                    and b.get('volume_mm3') is not None and abs(a['volume_mm3'] - b['volume_mm3']) <= 0.01)
print(json.dumps(out, indent=1))
PY
echo "replay done ($RUN)"; cat "$O/compare.json"
