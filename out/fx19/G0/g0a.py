# G0a for fx19 (LAB-fx19 section 1, headless). freecadcmd /lab/out/fx19/G0/g0a.py  -> prints the log (tee g0a.txt)
# GAP env: 0.5 (default) or 2.0 (rung 2). Saves /lab/out/fx19/P/hook-gap.FCStd (rung 2: hook-gap-2.FCStd).
import os, shutil, sys, json
sys.path.insert(0, '/lab')
import FreeCAD, Part, Sketcher
from lab import fx19geom as fg

GAP = float(os.environ.get('GAP', '0.5'))
SRC = '/lab/out/l2/hand/hand.FCStd'
OUT = '/lab/out/fx19/P/hook-gap.FCStd' if GAP == 0.5 else '/lab/out/fx19/P/hook-gap-%g.FCStd' % GAP
TMP = '/tmp/g0a-copy.FCStd'
R = {'gap_target': GAP}


def log(*a):
    print('G0A', *a); sys.stdout.flush()


def con_tuples(s):
    return [(c.Type, c.First, c.FirstPos, c.Second, c.SecondPos) for c in s.Constraints]


def geo_pts(s):
    return [((g.StartPoint.x, g.StartPoint.y), (g.EndPoint.x, g.EndPoint.y)) for g in s.Geometry]


def dof(s):
    out = {}
    for name in ():
        if hasattr(s, name):
            try:
                out[name] = getattr(s, name)()
            except Exception as e:
                out[name] = 'error %s' % e
    try:
        out['solve'] = s.solve()
    except Exception as e:
        out['solve'] = 'error %s' % e
    for name in ('DoF', 'FullyConstrained', 'MalformedConstraints', 'Conflicting', 'Redundant'):
        if hasattr(s, name):
            out[name] = getattr(s, name)
    return out


def wires(s):
    return [{'edges': len(w.Edges), 'isClosed': w.isClosed()} for w in s.Shape.Wires]


def objstate(d):
    return {o.Name: {'valid': o.isValid(), 'status': o.getStatusString()} for o in d.Objects}


shutil.copy(SRC, TMP)
d = FreeCAD.openDocument(TMP)
body = d.getObject('Body'); s = d.getObject('Sketch'); pad = d.getObject('Pad')
log('control before: pad volume', pad.Shape.Volume)
body.removeObject(pad); d.removeObject('Pad'); d.recompute()
log('pad deleted; body tip =', body.Tip.Name if body.Tip else None)

geo = geo_pts(s); con = con_tuples(s)
closing = fg.closing_line(geo); first = 0
log('closing line index', closing, 'end points', geo[closing])
log('first line index', first, 'end points', geo[first])
on = fg.on_line(con, closing)
for i in on:
    log('constraint on closing line', i, con[i], 'value', s.Constraints[i].Value)
log('origin-tied points (GeoId, PosId)', fg.origin_tied_points(con))
log('closing line has Vertical rule:', any(con[i][0] == 'Vertical' and con[i][1] == closing for i in on))
j = fg.join_index(con, closing, first)
sizes = fg.length_sizes(con, closing)
log('delete: join Coincident', j, con[j], '; length sizes on closing line', sizes)
R.update(closing=closing, join=j, sizes_on_closing=sizes, origin_tied=fg.origin_tied_points(con))
for i in sorted([j] + sizes, reverse=True):
    s.delConstraint(i)
geo_id, pos_id, pt = fg.move_plan(con, closing, first, GAP)
log('movePoint', geo_id, pos_id, pt)
R['move'] = [geo_id, pos_id, list(pt)]
s.moveGeometry(geo_id, pos_id, FreeCAD.Vector(pt[0], pt[1], 0), 0)
d.recompute(); d.recompute()
geo2 = geo_pts(s)
a = geo2[closing][1]; b = geo2[first][0]
R['gap_measured'] = fg.gap(a, b)
log('after 2 recomputes: closing end', a, 'first start', b, 'gap', '%.6f' % R['gap_measured'])
R['wires'] = wires(s); R['dof'] = dof(s)
log('sketch wires', R['wires'])
log('solver', R['dof'])
log('dof-like attributes', [n for n in dir(s) if 'dof' in n.lower()])
d.recompute()
d.saveAs(OUT)
log('saved', OUT)

# 1b: on a copy, re-add the join, Pad 20
shutil.copy(OUT, '/tmp/g0a-1b.FCStd')
d2 = FreeCAD.openDocument('/tmp/g0a-1b.FCStd')
s2 = d2.getObject('Sketch')
s2.addConstraint(Sketcher.Constraint('Coincident', closing, 2, first, 1))
d2.recompute()
p2 = d2.getObject('Body').newObject('PartDesign::Pad', 'Pad'); p2.Profile = s2; p2.Length = 20
d2.recompute()
R['1b'] = {'volume': p2.Shape.Volume, 'valid': p2.isValid(), 'wires': wires(s2), 'dof': dof(s2),
           'closing_end': geo_pts(s2)[closing][1], 'first_start': geo_pts(s2)[first][0]}
log('1b rejoined: pad valid', p2.isValid(), 'volume', p2.Shape.Volume, 'dof', R['1b']['dof'],
    'closing end', R['1b']['closing_end'], 'first start', R['1b']['first_start'])
FreeCAD.closeDocument(d2.Name)

# 2: Pad on the gap sketch
p = body.newObject('PartDesign::Pad', 'Pad'); p.Profile = s; p.Length = 20
d.recompute()
R['pad'] = {'isValid': p.isValid(), 'status': p.getStatusString(), 'isNull': p.Shape.isNull(),
            'objects': objstate(d)}
log('PAD isValid', p.isValid())
log('PAD status', repr(p.getStatusString()))
log('PAD Shape.isNull', p.Shape.isNull())
log('objects', R['pad']['objects'])
FreeCAD.closeDocument(d.Name)

# 4: control
shutil.copy(SRC, '/tmp/g0a-ctrl.FCStd')
d3 = FreeCAD.openDocument('/tmp/g0a-ctrl.FCStd')
for o in d3.Objects:
    o.touch()
d3.recompute()
pc = d3.getObject('Pad')
R['control'] = {'valid': pc.isValid(), 'volume': pc.Shape.Volume}
log('control: valid', pc.isValid(), 'volume', pc.Shape.Volume)
FreeCAD.closeDocument(d3.Name)
json.dump(R, open(OUT.replace('/P/', '/G0/').replace('.FCStd', '-g0a.json'), 'w'), indent=1, default=str)
log('done')
