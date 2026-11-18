# fc12 helpers (FreeCAD course lesson 12, PolarPattern round a post) on top of common.sh + fx19_lib.sh + fx20_lib.sh
# + fc9_lib.sh + fc10_lib.sh + fc11_lib.sh.
X=/lab/out/fc12
check12() {    # check12 FCSTD OUT.json [HOOKS]: lab/fc12parts.py check (at HOOKS if given), headless, its own process
  FC12_DOC=$1 FC12_OUT=$2 FC12_MODE=check FC12_HOOKS=${3:-} timeout 180 /opt/freecad/AppRun freecadcmd /lab/lab/fc12parts.py 2>&1 | tr '\r\t' '\n\n' | grep '^FC12' | tail -1
}
pstate() {     # the PolarPattern as FreeCAD holds it now (not filmed)
  Q "import FreeCAD, json
o = FreeCAD.getDocument('$1').getObject('PolarPattern')
print(json.dumps({'mode': o.Mode, 'angle': round(o.Angle.Value, 4), 'offset': round(o.Offset.Value, 4), 'occ': o.Occurrences,
  'expr': [list(e) for e in o.ExpressionEngine], 'state': list(o.State), 'solids': len(o.Shape.Solids)}))"
}
FQ12() { Q "exec(open('/lab/lab/fc8q.py').read()); exec(open('/lab/lab/fc9q.py').read()); exec(open('/lab/lab/fc12q.py').read()); $1"; }
rot() {        # rot X Y DEG: "x y" turned DEG round the origin
  awk -v x=$1 -v y=$2 -v t=$3 'BEGIN{pi=atan2(0,-1); c=cos(t*pi/180); s=sin(t*pi/180); printf "%.3f %.3f", x*c-y*s, x*s+y*c}'
}
