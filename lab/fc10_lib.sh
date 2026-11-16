# fc10 helpers (FreeCAD course lesson 10, fully constrained sketches) on top of common.sh + fx19_lib.sh + fx20_lib.sh
# + fc9_lib.sh (rowclk, btn, at, vp, taskpos, FQ).
#   . /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh
X=/lab/out/fc10
check10() {    # check10 FCSTD OUT.json [H]: lab/fc10parts.py check (or resize to H) mode, headless, its own process
  if [ -n "${3:-}" ]; then
    FC10_DOC=$1 FC10_OUT=$2 FC10_MODE=resize FC10_H=$3 timeout 120 /opt/freecad/AppRun freecadcmd /lab/lab/fc10parts.py 2>&1 | tr '\r\t' '\n\n' | grep '^FC10' | tail -1
  else
    FC10_DOC=$1 FC10_OUT=$2 FC10_MODE=check timeout 120 /opt/freecad/AppRun freecadcmd /lab/lab/fc10parts.py 2>&1 | tr '\r\t' '\n\n' | grep '^FC10' | tail -1
  fi
}
live() {       # live DOC [nosolve]: the numbers a person cannot see, read from the open document (not filmed)
  Q "import FreeCAD, json
d = FreeCAD.getDocument('$1'); s = d.getObject('Body').Shape; sk = d.getObject('HookSketch'); hs = d.getObject('HoleSketch')
bb = s.BoundBox; c = hs.getGlobalPlacement().multVec(hs.Geometry[0].Center)
dof = sk.DoF if '${2:-}' == 'nosolve' else (sk.solve(), sk.DoF)[1]
print(json.dumps({'dof': dof, 'constraints': len(sk.Constraints), 'zmin': round(bb.ZMin, 4), 'zmax': round(bb.ZMax, 4),
  'xmin': round(bb.XMin, 4), 'hole_z': round(c.z, 4), 'hole_to_top': round(bb.ZMax - c.z, 4), 'volume': round(s.Volume, 3),
  'plate_height': d.getObject('Params').get('plate_height')}))"
}
selnames() { Q "import FreeCADGui
print([(s.ObjectName, list(s.SubElementNames)) for s in FreeCADGui.Selection.getSelectionEx()])"; }
cmdtext() { Q "import FreeCADGui
c = FreeCADGui.Command.get('$1'); print(c.getInfo() if c else 'none')"; }
