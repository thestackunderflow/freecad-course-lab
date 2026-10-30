#!/bin/bash
# Lesson 4, lab L4-Q7 (no display, free): lesson 3's hook as lesson 3 left it (back5: hook_depth 40) with the holes and
# the fillet built as by hand (lab/build4.py: the sketch attached to the back face), centres from names and as plain
# numbers; then width 20 -> 30 alone, then thickness 5 -> 8 at width 30, then back to 20 and 5. A copy saved and
# measured at each stage; holes.check on each. Writes out/l4/fillet-tests.json and the two built files.
#   FCC_PREFIX=fc4 tools/run.sh lab/fillet_tests4.sh
set -u
O=/lab/out/l4/fillet-tests; rm -rf "$O"; mkdir -p "$O"
for kind in names plain; do
  P=0; [ $kind = plain ] && P=1
  FC_IN=/lab/out/l3/hand/back5.FCStd FC_OUT=$O/$kind-start.FCStd PLAIN=$P freecadcmd /lab/lab/build4.py > "$O/build-$kind.log" 2>&1
  cat > /tmp/stages.py <<PY
import FreeCAD as App
d = App.openDocument('$O/$kind-start.FCStd'); ss = d.getObject('Spreadsheet')
for name, cells in (('width30', [('B5', '30 mm')]), ('width30-thick8', [('B2', '8 mm')]), ('back', [('B5', '20 mm'), ('B2', '5 mm')])):
    for c, v in cells:
        ss.set(c, v)
    d.recompute()
    bad = [o.Name for o in d.Objects if hasattr(o, 'isValid') and not o.isValid()]
    open('$O/$kind-' + name + '.invalid.txt', 'w').write(' '.join(bad))
    d.saveCopy('$O/$kind-' + name + '.FCStd')
PY
  freecadcmd /tmp/stages.py > "$O/stages-$kind.log" 2>&1
  for st in start width30 width30-thick8 back; do
    FC_DOC=$O/$kind-$st.FCStd FC_OUT=$O/measure-$kind-$st.json freecadcmd /lab/checker/measure.py > /dev/null 2>&1
  done
done
cd /lab && python3 - "$O" <<'PY'
import json, os, sys
sys.path.insert(0, '/lab')
from checker import holes, score_l4
o = sys.argv[1]
names = {'start': dict(width=20), 'width30': dict(width=30), 'width30-thick8': dict(width=30, thickness=8),
         'back': dict(width=20)}
res = {'start_file': 'out/l3/hand/back5.FCStd (lesson 3 by hand, hook_depth 40)', 'built_by': 'lab/build4.py', 'runs': {}}
for kind in ('names', 'plain'):
    for st, n in names.items():
        m = json.load(open(os.path.join(o, 'measure-%s-%s.json' % (kind, st))))
        c = holes.check(score_l4._part(m), dict(holes.NAMES, **n))
        c['invalid_objects'] = open(os.path.join(o, '%s-%s.invalid.txt' % (kind, st))).read().split() if st != 'start' else []
        res['runs']['%s/%s' % (kind, st)] = c
json.dump(res, open('/lab/out/l4/fillet-tests.json', 'w'), indent=1)
for k, c in res['runs'].items():
    print(k, c['ok'], c['misses'], c['hole_sides_mm'], c['fillet_on_lip_edge'], round(c['volume_mm3'], 4), c['invalid_objects'])
PY
