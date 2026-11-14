# Take P (LAB-fx19 section 3, not filmed, no AI): the start files. freecadcmd /lab/out/fx19/P/make.py | tee P/make.txt
# hook-gap.FCStd is G0a's own file (out/fx19/G0/g0a.py, kept as written). hook-touch.FCStd: the same edits, but the
# closing line's end placed ON (0, 0) exactly by script, with no Coincident rule. Then both reopened and checked
# (on copies; a Pad 20 added to each copy): wire closure, the Pad's state and volume -> P/check.txt.
import shutil, sys, json
sys.path.insert(0, '/lab')
import FreeCAD
from lab import fx19geom as fg

SRC = '/lab/out/l2/hand/hand.FCStd'
P = '/lab/out/fx19/P/'


def log(*a):
    print('P', *a); sys.stdout.flush()


def con_tuples(s):
    return [(c.Type, c.First, c.FirstPos, c.Second, c.SecondPos) for c in s.Constraints]


def geo_pts(s):
    return [((g.StartPoint.x, g.StartPoint.y), (g.EndPoint.x, g.EndPoint.y)) for g in s.Geometry]


shutil.copy(SRC, '/tmp/touch.FCStd')
d = FreeCAD.openDocument('/tmp/touch.FCStd')
body = d.getObject('Body'); s = d.getObject('Sketch')
body.removeObject(d.getObject('Pad')); d.removeObject('Pad'); d.recompute()
con = con_tuples(s); closing = fg.closing_line(geo_pts(s)); j = fg.join_index(con, closing, 0)
for i in sorted([j] + fg.length_sizes(con, closing), reverse=True):
    s.delConstraint(i)
s.moveGeometry(closing, 2, FreeCAD.Vector(0, 0, 0), 0)
d.recompute(); d.recompute()
log('touch: closing end', geo_pts(s)[closing][1], 'first start', geo_pts(s)[0][0],
    'coincidents on the closing end', [c for c in con_tuples(s) if c[0] == 'Coincident' and (closing, 2) in ((c[1], c[2]), (c[3], c[4]))])
d.saveAs(P + 'hook-touch.FCStd')
FreeCAD.closeDocument(d.Name)

R = {}
for name in ('hook-gap', 'hook-touch'):
    shutil.copy(P + name + '.FCStd', '/tmp/chk.FCStd')
    d = FreeCAD.openDocument('/tmp/chk.FCStd')
    s = d.getObject('Sketch')
    for o in d.Objects:
        o.touch()
    d.recompute()
    g = geo_pts(s)
    r = {'objects': [o.Name for o in d.Objects], 'gap': fg.gap(g[7][1], g[0][0]),
         'wires': [{'edges': len(w.Edges), 'isClosed': w.isClosed()} for w in s.Shape.Wires], 'dof': s.DoF}
    p = d.getObject('Body').newObject('PartDesign::Pad', 'Pad'); p.Profile = s; p.Length = 20
    d.recompute()
    r.update(pad_valid=p.isValid(), pad_status=p.getStatusString(),
             pad_volume=None if p.Shape.isNull() else p.Shape.Volume)
    R[name] = r
    log(name, r)
    FreeCAD.closeDocument(d.Name)
json.dump(R, open(P + 'check.json', 'w'), indent=1, default=str)
with open(P + 'check.txt', 'w') as f:
    for k, v in R.items():
        f.write('%s: gap %.6f mm, wires %s, DoF %s, Pad 20 valid %s, status %r, volume %s\n' % (
            k, v['gap'], v['wires'], v['dof'], v['pad_valid'], v['pad_status'], v['pad_volume']))
log('done')
