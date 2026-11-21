# fc14 helpers (FreeCAD course lesson 14, a key peg and the Thickness's place in the Body) on top of common.sh + fx19_lib.sh
# + fx20_lib.sh + fc9_lib.sh .. fc13_lib.sh; fc14q.py queries (menu / dialog list / dress-up face list).
X=/lab/out/fc14
check14() {    # check14 FCSTD OUT.json: lab/fc14parts.py check (stored, recomputed, wall 2, wall 3: PLAN 2.5 score), headless
  FC14_DOC=$1 FC14_OUT=$2 FC14_MODE=check timeout 300 /opt/freecad/AppRun freecadcmd /lab/lab/fc14parts.py 2>&1 | tr '\r\t' '\n\n' | grep '^FC14' | tail -1
}
FQ14() { Q "exec(open('/lab/lab/fc8q.py').read()); exec(open('/lab/lab/fc9q.py').read()); exec(open('/lab/lab/fc12q.py').read()); exec(open('/lab/lab/fc14q.py').read()); $1"; }
bstate() {     # the Body as FreeCAD holds it now (not filmed): order, Tip, Thickness base, shown objects, shape
  Q "import FreeCAD, FreeCADGui, json
d = FreeCAD.getDocument('$1'); b = d.getObject('Body'); t = d.getObject('Thickness'); g = FreeCADGui.getDocument('$1')
s = b.Shape; ins = lambda x, y, z: s.isInside(FreeCAD.Vector(x, y, z), 1e-6, True)
w = float(d.getObject('Params').get('wall'))
print(json.dumps({'group': [o.Name for o in b.Group if not o.TypeId.startswith('App::')], 'tip': b.Tip.Name if b.Tip else None,
  'base': None if t is None else [t.Base[0].Name, list(t.Base[1])], 'reversed': None if t is None else bool(t.Reversed),
  'shown': [o.Name for o in b.Group if g.getObject(o.Name) and g.getObject(o.Name).Visibility],
  'state': {o.Name: list(o.State) for o in b.Group if list(o.State) not in ([], ['Up-to-date'])},
  'volume': round(s.Volume, 3), 'solids': len(s.Solids), 'peg_mid': ins(0, -28, 40), 'wall_pt': ins(0, -20 - w / 2, 40),
  'lid_air': not ins(0, 0, 50 + w / 2), 'bottom': ins(0, 0, -w / 2), 'side_nx': ins(-30 - w / 2, 0, 25)}))"
}
W14=/tmp/fc14-ui.json
uiwatch() { Q "exec(open('/lab/lab/fc14menu.py').read()); watch('$W14', ${1:-60})" > /dev/null; }   # before a modal step
ui() {         # ui KIND TEXT: "x y" from the watcher's last dump (KIND menu|popup|button|combo); ui dump: the whole state
  sleep 0.7
  python3 - "$W14" "$1" "${2:-}" <<'PY'
import json, sys
st = json.load(open(sys.argv[1])); k, t = sys.argv[2], sys.argv[3]
if k == 'dump': print(json.dumps(st)); sys.exit()
rows = st['menu'] if k == 'menu' else st['popup'] if k == 'popup' else [b for d in st['dialogs'] for b in (d['buttons'] if k == 'button' else d['combos'])]
for r in rows:
    if str(r[0]).startswith(t):
        print(r[-2], r[-1]); sys.exit()
print('none')
PY
}
