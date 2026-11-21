# fc16 helpers (FreeCAD course lesson 16, a hanging hole: Pocket depth vs the Thickness wall) on top of common.sh + fx19_lib.sh
# + fx20_lib.sh + fc9_lib.sh .. fc15_lib.sh; lab/fc16parts.py readers.
X=/lab/out/fc16
check16() {    # check16 FCSTD OUT.json: lab/fc16parts.py check (stored, recomputed, wall 2, 3, 12: PLAN 2.5 score), headless
  FC16_DOC=$1 FC16_OUT=$2 FC16_MODE=check timeout 600 /opt/freecad/AppRun freecadcmd /lab/lab/fc16parts.py 2>&1 | tr '\r\t' '\n\n' | grep '^FC16' | tail -1
}
hstate() {     # the Pocket as FreeCAD holds it now (not filmed): Type, Length, expression, states, hole points
  Q "import FreeCAD, json
d = FreeCAD.getDocument('$1'); b = d.getObject('Body'); s = b.Shape; p = d.getObject('Pocket')
w = float(d.getObject('Params').get('wall')); ins = lambda x, y, z: s.isInside(FreeCAD.Vector(x, y, z), 1e-6, True)
st = {o.Name: [list(o.State), o.getStatusString()] for o in b.Group if o.TypeId.startswith('PartDesign::') and list(o.State) != ['Up-to-date']}
print(json.dumps({'wall': w, 'type': str(p.Type) if p else None, 'length': round(p.Length.Value, 3) if p else None,
  'expr': dict((k.lstrip('.'), v) for k, v in p.ExpressionEngine).get('Length') if p else None, 'state': st,
  'back_open': [not ins(0, y, 30) for y in (20.05, 20 + w / 2, 20 + w - 0.05)], 'front_solid': ins(0, -20 - w / 2, 30),
  'volume': round(s.Volume, 3), 'solids': len(s.Solids)}))"
}
