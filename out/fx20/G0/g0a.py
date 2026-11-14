# G0a for fx20 (LAB-fx20 section 1, headless). freecadcmd /lab/out/fx20/G0/g0a.py | tee g0a-raw.txt
# Saves /lab/out/fx20/P/hook-red.FCStd (step 3's over-constrained copy, rung c) and G0/g0a.json.
import json, shutil, sys
sys.path.insert(0, '/lab')
import FreeCAD, Sketcher
from lab import fx20geom as fg

SRC = '/lab/out/l2/hand/hand.FCStd'
RED = '/lab/out/fx20/P/hook-red.FCStd'
R = {}
n = [0]


def log(*a):
    print('G0A', *a); sys.stdout.flush()


def fresh():
    n[0] += 1
    p = '/tmp/g0a-%d.FCStd' % n[0]
    shutil.copy(SRC, p)
    d = FreeCAD.openDocument(p)
    return d, d.getObject('Sketch'), d.getObject('Pad')


def geo_pts(s):
    return [((round(g.StartPoint.x, 6), round(g.StartPoint.y, 6)), (round(g.EndPoint.x, 6), round(g.EndPoint.y, 6)))
            for g in s.Geometry]


def con_tuples(s):
    return [(c.Type, c.First, c.FirstPos, c.Second, c.SecondPos) for c in s.Constraints]


def state(d, s, pad):
    out = {'count': len(s.Constraints)}
    try:
        out['solve'] = s.solve()
    except Exception as e:
        out['solve'] = 'error %s' % e
    for k in ('DoF', 'FullyConstrained', 'Conflicting', 'Redundant', 'ConflictingConstraints',
              'RedundantConstraints', 'PartiallyRedundant', 'MalformedConstraints'):
        if hasattr(s, k):
            try:
                out[k] = getattr(s, k)
            except Exception as e:
                out[k] = 'error %s' % e
    out['sketch_status'] = s.getStatusString(); out['sketch_valid'] = s.isValid()
    if pad is not None:
        out['pad_valid'] = pad.isValid(); out['pad_status'] = pad.getStatusString()
        out['pad_volume'] = None if pad.Shape.isNull() else round(pad.Shape.Volume, 4)
    return out


def arm_len(s, i):
    g = s.Geometry[i]
    return round(g.length(), 6)


# step 1
d, s, pad = fresh()
geo = geo_pts(s); con = con_tuples(s)
arm = fg.line_by_ends(geo, (20, 5), (5, 5)); bottom = fg.line_by_ends(geo, (0, 0), (25, 0))
bsize = fg.length_sizes(con, bottom)
log('geometry', geo)
for i, c in enumerate(s.Constraints):
    log('constraint', i, con[i], 'value', c.Value, 'driving', c.Driving, 'name', repr(c.Name))
log('arm-top line index', arm, geo[arm], 'length', arm_len(s, arm), '; bottom line', bottom, 'its sizes', bsize)
R['step1'] = dict(state(d, s, pad), arm=arm, bottom=bottom, bottom_sizes=bsize, geo=geo)
log('step1 state', R['step1'])
log('dof-like attributes', [k for k in dir(s) if 'dof' in k.lower() or 'onflict' in k or 'edundan' in k])
FreeCAD.closeDocument(d.Name)


def setdatum_case(value, label):
    d, s, pad = fresh()
    out = {}
    try:
        idx = s.addConstraint(Sketcher.Constraint('Distance', arm, 15.0))
        out['add_index'] = idx
    except Exception as e:
        out['add_error'] = '%s: %s' % (type(e).__name__, e)
        log(label, 'addConstraint 15 raised', out['add_error'])
        FreeCAD.closeDocument(d.Name); return out
    out['after_add'] = state(d, s, None)
    log(label, 'added Distance 15 on arm top as index', idx, 'state', out['after_add'])
    try:
        s.setDatum(idx, FreeCAD.Units.Quantity('%g mm' % value))
        out['setDatum'] = 'no exception'
    except Exception as e:
        out['setDatum'] = '%s: %s' % (type(e).__name__, e)
    out['value_after'] = s.Constraints[idx].Value if idx < len(s.Constraints) else None
    out['arm_len_after'] = arm_len(s, arm)
    d.recompute()
    out['after'] = state(d, s, pad)
    log(label, 'setDatum(%d, %g mm) ->' % (idx, value), out['setDatum'])
    log(label, 'datum value after', out['value_after'], 'arm length', out['arm_len_after'], 'state', out['after'])
    FreeCAD.closeDocument(d.Name)
    return out


# step 2: what the dialog does (17), then the same value (15, Q12)
R['step2_17'] = setdatum_case(17, 'step2 17:')
R['step2_15'] = setdatum_case(15, 'step2 15:')

# step 3: addConstraint 17 directly (rung c); saved as hook-red.FCStd
d, s, pad = fresh()
out = {}
try:
    out['add_index'] = s.addConstraint(Sketcher.Constraint('Distance', arm, 17.0))
except Exception as e:
    out['add_error'] = '%s: %s' % (type(e).__name__, e)
out['solve'] = s.solve()
d.recompute()
out['state'] = state(d, s, pad)
out['arm_len'] = arm_len(s, arm)
R['step3'] = out
log('step3 addConstraint Distance 17:', out)
d.saveAs(RED)
log('saved', RED)
FreeCAD.closeDocument(d.Name)

# step 4: control (the fix): bottom 25 -> 27 by setDatum; then a reference size on the arm top
d, s, pad = fresh()
out = {}
bi = bsize[0]
try:
    s.setDatum(bi, FreeCAD.Units.Quantity('27 mm')); out['setDatum'] = 'ok'
except Exception as e:
    out['setDatum'] = '%s: %s' % (type(e).__name__, e)
d.recompute()
out['state'] = state(d, s, pad)
ri = s.addConstraint(Sketcher.Constraint('Distance', arm, 17.0))
s.setDriving(ri, False)
s.solve(); d.recompute()
out['ref_index'] = ri; out['ref_value'] = s.Constraints[ri].Value; out['ref_driving'] = s.Constraints[ri].Driving
out['state_with_ref'] = state(d, s, pad); out['arm_len'] = arm_len(s, arm)
R['step4'] = out
log('step4 control:', out)
FreeCAD.closeDocument(d.Name)
json.dump(R, open('/lab/out/fx20/G0/g0a.json', 'w'), indent=1, default=str)
log('done')
