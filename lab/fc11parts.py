"""fc11 (FreeCAD course lesson 11, one length with two sizes: reference constraints), lab instrument run by
freecadcmd, never filmed. Built on lab/fc10parts.py (the same lesson 3 hook, pinned).

    FC11_OUT=/lab/out/fc11/P FC11_MODE=build freecadcmd /lab/lab/fc11parts.py
        hook-pinned.FCStd (lesson 10's end state), hook-redundant.FCStd (+ a DRIVING 55 on the inner face, saved after
        a recompute), hook-reference.FCStd (+ the same 55 as a REFERENCE), each resized by code (80, 100) and the
        your-turn rectangle with its diagonal; every number read back by code -> build.json.
    FC11_DOC=x.FCStd FC11_OUT=y.json FC11_MODE=check freecadcmd /lab/lab/fc11parts.py      (any saved file)
    FC11_DOC=x.FCStd FC11_OUT=y.json FC11_MODE=resize FC11_H=80 freecadcmd /lab/lab/fc11parts.py   (headless leg)
The inner face: line 5, (5,5)-(5,60); its length is plate_height - arm_thickness = 55 already."""
import json
import math
import os
import shutil
import sys

os.environ['FC10_MODE'] = 'lib'          # fc10parts.py: functions only, no build on import
sys.path.insert(0, '/lab/lab')
import fc10parts as F10                   # noqa: E402

import FreeCAD                            # noqa: E402
import Mesh                               # noqa: E402
import Part                               # noqa: E402
import Sketcher                           # noqa: E402

OUT = os.environ.get('FC11_OUT', '/lab/out/fc11/P')
MODE = os.environ.get('FC11_MODE', 'build')
V = FreeCAD.Vector
INNER = 5


def log(*a):
    print('FC11', *a)
    sys.stdout.flush()


def inner_info(sk):
    """the size on the inner face (a Distance / DistanceY on line 5 alone), if any"""
    for i, c in enumerate(sk.Constraints):
        if c.Type in ('Distance', 'DistanceY') and c.First == INNER and c.Second in (-2000, INNER):
            path = '.Constraints.%s' % c.Name if c.Name else '.Constraints[%d]' % i
            ex = [e for p, e in sk.ExpressionEngine if p in (path, '.Constraints[%d]' % i)]
            return {'index': i, 'type': c.Type, 'driving': bool(c.Driving), 'value': round(sk.getDatum(i).Value, 6)
                    if c.Driving else round(c.Value, 6), 'expression': ex[0] if ex else None, 'name': c.Name}
    return None


def ref_value(sk, info):
    """a reference size's shown value is the geometry's length (FreeCAD updates c.Value on solve)"""
    if info is None:
        return None
    g = sk.Geometry[INNER]
    return round(g.length(), 6)


def extra(d, stl_path=None):
    sk = F10.hook_sketch(d)
    r = {}
    if sk is None:
        return r
    r['line_lengths'] = [round(g.length(), 6) for g in sk.Geometry if 'LineSegment' in g.TypeId][:8]
    r['inner'] = inner_info(sk)
    if r['inner'] is not None:
        r['inner']['geometry_length'] = ref_value(sk, r['inner'])
        if not r['inner']['driving']:
            r['inner']['value'] = r['inner']['geometry_length']
    names = {c.Name: (i, c) for i, c in enumerate(sk.Constraints) if c.Name}
    ph = names.get('plate_height')
    bound = [e for p, e in sk.ExpressionEngine if 'plate_height' in e]
    r['plate_height_driving'] = bool(ph and ph[1].Driving and bound)
    r['arm_z'] = round(min(g.StartPoint.y for g in sk.Geometry[4:5]), 6) if len(sk.Geometry) > 4 else None
    r['cons'] = [[i, c.Type, c.First, c.FirstPos, c.Second, c.SecondPos, round(c.Value, 6), bool(c.Driving), c.Name]
                 for i, c in enumerate(sk.Constraints)]
    r['states'] = {o.Name: list(o.State) for o in d.Objects if o.TypeId.startswith(('Sketcher::', 'PartDesign::'))}
    s, _ = F10.body_shape(d)
    if s is not None and stl_path:
        body = [o for o in d.Objects if o.TypeId == 'PartDesign::Body'][0]
        Mesh.export([body], stl_path)
        r['stl_zmax'] = round(Mesh.Mesh(stl_path).BoundBox.ZMax, 6)
        r['stl_zmin'] = round(Mesh.Mesh(stl_path).BoundBox.ZMin, 6)
    return r


def measure(d, stl_path=None):
    r = F10.measure(d)
    r.update(extra(d, stl_path))
    return r


def add_inner(d, driving):
    sk = d.getObject('HookSketch')
    i = sk.addConstraint(Sketcher.Constraint('Distance', INNER, 55))
    if not driving:
        sk.setDriving(i, False)
    d.recompute()
    return i


def resize(d, h):
    d.getObject('Params').set('plate_height', str(h))
    d.recompute()
    d.recompute()


def yourturn():
    """lesson 10's rectangle 40 x 30 pinned; a construction diagonal sized as a reference, then width 40 -> 60; and the
    same diagonal as a driving size (redundant?)"""
    d = FreeCAD.newDocument('yourturn11')
    sk = d.addObject('Sketcher::SketchObject', 'Sketch')
    p = [V(30, 20, 0), V(75, 20, 0), V(75, 55, 0), V(30, 55, 0)]
    for i in range(4):
        sk.addGeometry(Part.LineSegment(p[i], p[(i + 1) % 4]))
    for i in range(4):
        sk.addConstraint(Sketcher.Constraint('Coincident', i, 2, (i + 1) % 4, 1))
    for i in (0, 2):
        sk.addConstraint(Sketcher.Constraint('Horizontal', i))
    for i in (1, 3):
        sk.addConstraint(Sketcher.Constraint('Vertical', i))
    w = sk.addConstraint(Sketcher.Constraint('Distance', 0, 40))
    sk.addConstraint(Sketcher.Constraint('Distance', 1, 30))
    sk.addConstraint(Sketcher.Constraint('Coincident', 0, 1, -1, 1))
    sk.solve()
    dg = sk.addGeometry(Part.LineSegment(V(0, 0, 0), V(40, 30, 0)), True)      # construction
    sk.addConstraint(Sketcher.Constraint('Coincident', dg, 1, 0, 1))
    sk.addConstraint(Sketcher.Constraint('Coincident', dg, 2, 2, 1))
    k = sk.addConstraint(Sketcher.Constraint('Distance', dg, 50))
    sk.setDriving(k, False)
    sk.solve()
    d.recompute()
    r = {'dof': sk.DoF, 'diagonal_40': round(sk.Geometry[dg].length(), 6)}
    sk.setDatum(w, FreeCAD.Units.Quantity('60 mm'))
    sk.solve()
    d.recompute()
    r['diagonal_60'] = round(sk.Geometry[dg].length(), 6)
    r['ref_constraint_value_60'] = round(sk.Constraints[k].Value, 6)
    sk.setDriving(k, True)
    rc = sk.solve()
    r['driving_diagonal_solve'] = rc
    r['driving_diagonal_redundant'] = bool(list(sk.RedundantConstraints) or list(sk.ConflictingConstraints))
    r['driving_diagonal_lists'] = [list(sk.RedundantConstraints), list(sk.ConflictingConstraints)]
    FreeCAD.closeDocument(d.Name)
    return r


def build():
    os.makedirs(OUT, exist_ok=True)
    allr = {}
    files = {}
    for kind in ('pinned', 'redundant', 'reference'):
        d = F10.hook_doc('hook_' + kind, True)
        if kind != 'pinned':
            add_inner(d, kind == 'redundant')
        p = os.path.join(OUT, 'hook-%s.FCStd' % kind)
        d.saveAs(p)
        files[kind] = p
        allr['%s_60' % kind] = dict(measure(d, '/tmp/fc11-%s-60.stl' % kind), file=p)
        FreeCAD.closeDocument(d.Name)
        for h in (80, 100):
            d = FreeCAD.openDocument(p)
            resize(d, h)
            allr['%s_%d' % (kind, h)] = measure(d, '/tmp/fc11-%s-%d.stl' % (kind, h))
            FreeCAD.closeDocument(d.Name)
    # G0 Q1b by code: the redundant file, hook_depth 25 -> 30 at 60 (does anything reach the part?)
    d = FreeCAD.openDocument(files['redundant'])
    d.getObject('Params').set('hook_depth', '30')
    d.recompute()
    allr['redundant_hookdepth30'] = measure(d)
    FreeCAD.closeDocument(d.Name)
    allr['yourturn'] = yourturn()
    json.dump(allr, open(os.path.join(OUT, 'build.json'), 'w'), indent=1)
    log('build', json.dumps({k: (v.get('dof'), v.get('solve'), v.get('redundant'), v.get('conflicting'), v.get('zmax'),
                                 v.get('xmax'), v.get('stl_zmax'), (v.get('inner') or {}).get('value'))
                             for k, v in allr.items() if k != 'yourturn'}))
    log('yourturn', json.dumps(allr['yourturn']))


def check(doc_path, out, h=None):
    if h is not None:
        tmp = '/tmp/fc11-resize.FCStd'
        shutil.copy(doc_path, tmp)
        doc_path = tmp
    d = FreeCAD.openDocument(doc_path)
    if h is not None:
        resize(d, h)
    else:
        d.recompute()
    r = dict(measure(d, '/tmp/fc11-check.stl'), doc=doc_path,
             objects=[(o.Name, o.Label, o.TypeId) for o in d.Objects][:80])
    try:
        os.remove('/tmp/fc11-check.stl')
    except OSError:
        pass
    json.dump(r, open(out, 'w'), indent=1)
    log('check', json.dumps({k: r.get(k) for k in ('dof', 'solve', 'redundant', 'conflicting', 'zmax', 'stl_zmax',
                                                    'inner', 'plate_height_driving', 'line_lengths')}))


if MODE == 'build':
    build()
elif MODE == 'check':
    check(os.environ['FC11_DOC'], OUT)
elif MODE == 'resize':
    check(os.environ['FC11_DOC'], OUT, float(os.environ['FC11_H']))
