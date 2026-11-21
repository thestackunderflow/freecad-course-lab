# fc15 helpers (FreeCAD course lesson 15, a soft rim: the round has to fit in the wall) on top of common.sh + fx19_lib.sh
# + fx20_lib.sh + fc9_lib.sh .. fc14_lib.sh; lab/fc15parts.py readers.
X=/lab/out/fc15
check15() {    # check15 FCSTD OUT.json: lab/fc15parts.py check (stored, recomputed, wall 2, 3, 1.6: PLAN 2.5 score), headless
  FC15_DOC=$1 FC15_OUT=$2 FC15_MODE=check timeout 600 /opt/freecad/AppRun freecadcmd /lab/lab/fc15parts.py 2>&1 | tr '\r\t' '\n\n' | grep '^FC15' | tail -1
}
fstate() {     # the Body as FreeCAD holds it now (not filmed): order, Tip, each feature's state + message, rim read
  Q "import FreeCAD, json
d = FreeCAD.getDocument('$1'); b = d.getObject('Body'); s = b.Shape
st = {o.Name: [list(o.State), o.getStatusString()] for o in b.Group if o.TypeId.startswith('PartDesign::') and list(o.State) != ['Up-to-date']}
fl = {o.Name: [round(o.Radius.Value, 3), dict((k.lstrip('.'), v) for k, v in o.ExpressionEngine).get('Radius'), list(o.Base[1])] for o in b.Group if o.TypeId == 'PartDesign::Fillet'}
ins = lambda x, y, z: s.isInside(FreeCAD.Vector(x, y, z), 1e-6, True)
w = float(d.getObject('Params').get('wall'))
print(json.dumps({'group': [o.Name for o in b.Group if o.TypeId.startswith('PartDesign::')], 'tip': b.Tip.Name if b.Tip else None,
  'state': st, 'fillets': fl, 'wall': w, 'volume': round(s.Volume, 3), 'faces': len(s.Faces), 'solids': len(s.Solids),
  'bbox_x': [round(s.BoundBox.XMin, 3), round(s.BoundBox.XMax, 3)], 'corner_pt': ins(30 + w - 0.05, 0, 49.95)}))"
}
menubar_pos() { Q "import FreeCADGui
mw = FreeCADGui.getMainWindow(); mb = mw.menuBar(); k = mb.devicePixelRatioF()
for a in mb.actions():
    if a.text().replace('&', '') == '$1':
        c = mb.mapToGlobal(mb.actionGeometry(a).center()); print(int(c.x() * k), int(c.y() * k)); break
else: print('none')"; }
