# fc13 helpers (FreeCAD course lesson 13, Thickness on a wall cup) on top of common.sh + fx19_lib.sh + fx20_lib.sh
# + fc9_lib.sh + fc10_lib.sh + fc11_lib.sh + fc12_lib.sh (prop_row / tooltip_text from fc12q.py).
X=/lab/out/fc13
check13() {    # check13 FCSTD OUT.json: lab/fc13parts.py check (stored, recomputed, wall 3, width 70), headless
  FC13_DOC=$1 FC13_OUT=$2 FC13_MODE=check timeout 240 /opt/freecad/AppRun freecadcmd /lab/lab/fc13parts.py 2>&1 | tr '\r\t' '\n\n' | grep '^FC13' | tail -1
}
tstate() {     # the Thickness as FreeCAD holds it now (not filmed)
  Q "import FreeCAD, json
d = FreeCAD.getDocument('$1'); o = d.getObject('Thickness')
s = d.getObject('Body').Shape
print(json.dumps({'value': None if o is None else round(o.Value.Value, 4), 'reversed': None if o is None else bool(o.Reversed),
  'mode': None if o is None else str(o.Mode), 'join': None if o is None else str(o.Join),
  'expr': [] if o is None else [list(e) for e in o.ExpressionEngine], 'base': None if o is None else [o.Base[0].Name, list(o.Base[1])],
  'state': None if o is None else list(o.State), 'solids': len(s.Solids), 'volume': round(s.Volume, 3), 'bbox': [round(s.BoundBox.XLength, 3), round(s.BoundBox.YLength, 3), round(s.BoundBox.ZMin, 3), round(s.BoundBox.ZMax, 3)]}))"
}
FQ13() { Q "exec(open('/lab/lab/fc8q.py').read()); exec(open('/lab/lab/fc9q.py').read()); exec(open('/lab/lab/fc12q.py').read()); $1"; }
