"""fc10 (FreeCAD course lesson 10, fully constrained sketches), lab instrument run by freecadcmd, never filmed.

    FC10_OUT=/lab/out/fc10/P FC10_MODE=build freecadcmd /lab/lab/fc10parts.py
        hook-pinned.FCStd / hook-unpinned.FCStd (the take / Claude start files, built from scratch, not from the fc2/fc3
        hand files), each resized by code (60 -> 80, 60 -> 100, 60 -> 80 -> 100) and the your-turn rectangle; every
        number read back by code -> build.json.
    FC10_DOC=x.FCStd FC10_OUT=y.json FC10_MODE=check freecadcmd /lab/lab/fc10parts.py
        any saved file (a take's, a Claude run's): DoF, bottom / top (world ZMin / ZMax), hole -> y.json.
    FC10_DOC=x.FCStd FC10_OUT=y.json FC10_MODE=resize FC10_H=80 freecadcmd /lab/lab/fc10parts.py
        the headless leg of G0 Q2: open, Params.plate_height = H, recompute, check.
Part (PLAN 2.1): lesson 3's profile in the XZ plane (across = world X, up = world Z), corners (0,0) (25,0) (25,10)
(20,10) (20,5) (5,5) (5,60) (0,60); 8 lines, 8 joins, 8 flat/upright, 6 sizes bound to Params; Pad Params.width.
The stake: HoleSketch on the YZ base plane, a 4.5 circle placed FROM THE ORIGIN at (width / 2 across, plate_height -
15 up), Pocket through all, both ways. Pinned copy: + Coincident (bottom back corner, origin)."""
import json
import os
import shutil
import sys

import FreeCAD
import Part
import Sketcher

OUT = os.environ.get('FC10_OUT', '/lab/out/fc10/P')
MODE = os.environ.get('FC10_MODE', 'build')
V = FreeCAD.Vector
PROFILE = [(0, 0), (25, 0), (25, 10), (20, 10), (20, 5), (5, 5), (5, 60), (0, 60)]
PARAMS = (('plate_height', 60), ('thickness', 5), ('hook_depth', 25), ('lip_height', 10), ('width', 20))


def log(*a):
    print('FC10', *a)
    sys.stdout.flush()


def origin(body, role):
    return [o for o in body.Origin.OriginFeatures if o.Role == role][0]


def sized(sk, con, name, expr):
    c = sk.addConstraint(con)
    sk.renameConstraint(c, name)
    sk.setExpression('.Constraints.' + name, expr)


def hook_doc(name, pinned):
    d = FreeCAD.newDocument(name)
    s = d.addObject('Spreadsheet::Sheet', 'Params')
    for i, (n, v) in enumerate(PARAMS, 1):
        s.set('A%d' % i, n)
        s.set('B%d' % i, str(v))
        s.setAlias('B%d' % i, n)
    d.recompute()
    b = d.addObject('PartDesign::Body', 'Body')
    b.Label = 'Hook'
    sk = b.newObject('Sketcher::SketchObject', 'HookSketch')
    sk.AttachmentSupport = [(origin(b, 'XZ_Plane'), '')]
    sk.MapMode = 'FlatFace'
    n = len(PROFILE)
    for i in range(n):
        a, c = PROFILE[i], PROFILE[(i + 1) % n]
        sk.addGeometry(Part.LineSegment(V(a[0], a[1], 0), V(c[0], c[1], 0)))
    for i in range(n):                                       # 8 joins
        sk.addConstraint(Sketcher.Constraint('Coincident', i, 2, (i + 1) % n, 1))
    for i in range(n):                                       # 8 flat / upright
        sk.addConstraint(Sketcher.Constraint('Horizontal' if i % 2 == 0 else 'Vertical', i))
    # 6 sizes: L0 bottom 25 hook_depth, L1 front 10 lip_height, L2 lip top 5, L6 plate top 5, L7 back 60, arm 5 up
    sized(sk, Sketcher.Constraint('Distance', 0, 25), 'hook_depth', 'Params.hook_depth')
    sized(sk, Sketcher.Constraint('Distance', 1, 10), 'lip_height', 'Params.lip_height')
    sized(sk, Sketcher.Constraint('Distance', 2, 5), 'lip_thickness', 'Params.thickness')
    sized(sk, Sketcher.Constraint('Distance', 6, 5), 'thickness', 'Params.thickness')
    sized(sk, Sketcher.Constraint('Distance', 7, 60), 'plate_height', 'Params.plate_height')
    sized(sk, Sketcher.Constraint('DistanceY', 0, 1, 4, 1, 5), 'arm_thickness', 'Params.thickness')
    if pinned:
        sk.addConstraint(Sketcher.Constraint('Coincident', 0, 1, -1, 1))   # bottom back corner on the origin
    pad = b.newObject('PartDesign::Pad', 'Pad')
    pad.Profile = sk
    pad.setExpression('Length', 'Params.width')
    d.recompute()
    bb = pad.Shape.BoundBox
    across = 1 if (bb.YMin + bb.YMax) > 0 else -1           # the pad's middle in world Y (sign read, not assumed)
    hs = b.newObject('Sketcher::SketchObject', 'HoleSketch')
    hs.AttachmentSupport = [(origin(b, 'YZ_Plane'), '')]
    hs.MapMode = 'FlatFace'
    d.recompute()
    pl = hs.getGlobalPlacement()
    # sketch u, v -> world: find which local axis is world Y and which is world Z (sign included)
    uy, vz = pl.Rotation.multVec(V(1, 0, 0)), pl.Rotation.multVec(V(0, 1, 0))
    su = round(uy.y) * across
    sv = round(vz.z)
    hs.addGeometry(Part.Circle(V(10 * su, 45 * sv, 0), V(0, 0, 1), 2.25))
    hs.addConstraint(Sketcher.Constraint('Diameter', 0, 4.5))
    sized(hs, Sketcher.Constraint('DistanceX', -1, 1, 0, 3, 10 * su), 'across', '%sParams.width / 2' % ('-' if su < 0 else ''))
    sized(hs, Sketcher.Constraint('DistanceY', -1, 1, 0, 3, 45 * sv), 'up', '%s(Params.plate_height - 15)' % ('-' if sv < 0 else ''))
    pk = b.newObject('PartDesign::Pocket', 'Pocket')
    pk.Profile = hs
    pk.Type = 'ThroughAll'
    pk.Midplane = True
    b.Tip = pk
    d.recompute()
    return d


def hook_sketch(d):
    sks = [o for o in d.Objects if o.TypeId == 'Sketcher::SketchObject']
    named = [o for o in sks if o.Name == 'HookSketch']
    if named:
        return named[0]
    lines = [o for o in sks if len([g for g in o.Geometry if 'LineSegment' in g.TypeId]) >= 6]
    return lines[0] if lines else (sks[0] if sks else None)


def hole_info(d, shape):
    """the hole's axis height: from the solid's cylinder faces (r 2.25) and from HoleSketch's circle (where it would be)"""
    r = {}
    cyl = [f for f in shape.Faces if 'Cylinder' in f.Surface.TypeId and abs(f.Surface.Radius - 2.25) < 1e-3]
    r['hole_faces'] = len(cyl)
    if cyl:
        r['hole_z'] = round(cyl[0].Surface.Center.z, 6)
        r['hole_y'] = round(cyl[0].Surface.Center.y, 6)
    hs = d.getObject('HoleSketch')
    if hs is not None and hs.Geometry:
        c = hs.getGlobalPlacement().multVec(hs.Geometry[0].Center)
        r['sketch_hole_z'] = round(c.z, 6)
        r['sketch_hole_y'] = round(c.y, 6)
    return r


def sketch_info(sk):
    if sk is None:
        return {}
    rc = sk.solve()
    cons = [c for c in sk.Constraints]
    r = {'sketch': sk.Name, 'solve': rc, 'dof': sk.DoF, 'constraints': len(cons),
         'by_type': {}, 'redundant': list(sk.RedundantConstraints), 'conflicting': list(sk.ConflictingConstraints),
         'origin_tied': any(c.First in (-1, -2) or c.Second in (-1, -2) or c.Type == 'Block' or
                            (c.Type in ('DistanceX', 'DistanceY') and c.Second == -2000 and c.FirstPos != 0)
                            for c in cons),
         'expressions': [list(e) for e in sk.ExpressionEngine]}
    for c in cons:
        r['by_type'][c.Type] = r['by_type'].get(c.Type, 0) + 1
    pts = [(g.StartPoint, g.EndPoint) for g in sk.Geometry if 'LineSegment' in g.TypeId]
    if pts:
        xs = [p.x for ab in pts for p in ab]
        ys = [p.y for ab in pts for p in ab]
        r['sketch_bbox'] = [round(min(xs), 6), round(min(ys), 6), round(max(xs), 6), round(max(ys), 6)]
    return r


def body_shape(d):
    bodies = [o for o in d.Objects if o.TypeId == 'PartDesign::Body' and o.Shape.Solids]
    if bodies:
        return bodies[0].Shape, bodies[0].Name
    for o in d.Objects:
        if hasattr(o, 'Shape') and o.Shape.Solids and not o.InList:
            return o.Shape, o.Name
    return None, None


def measure(d):
    s, used = body_shape(d)
    r = {'used': used}
    if s is not None:
        bb = s.BoundBox
        r.update({'zmin': round(bb.ZMin, 6), 'zmax': round(bb.ZMax, 6), 'xmin': round(bb.XMin, 6),
                  'xmax': round(bb.XMax, 6), 'ymin': round(bb.YMin, 6), 'ymax': round(bb.YMax, 6),
                  'volume_mm3': round(s.Volume, 4), 'solids': len(s.Solids)})
        r.update(hole_info(d, s))
        if 'hole_z' in r:
            r['hole_to_top'] = round(r['zmax'] - r['hole_z'], 6)
        if 'sketch_hole_z' in r:
            r['sketch_hole_to_top'] = round(r['zmax'] - r['sketch_hole_z'], 6)
            r['hole_in_plate'] = bool(r['zmin'] + 2.25 <= r['sketch_hole_z'] <= r['zmax'] - 2.25)
    r.update(sketch_info(hook_sketch(d)))
    for o in d.Objects:
        if o.TypeId.startswith('PartDesign::') and o.TypeId not in ('PartDesign::Body',):
            r.setdefault('features', []).append([o.Name, o.TypeId.split('::')[1], o.isValid()])
    sh = d.getObject('Params')
    if sh is not None:
        r['sheet'] = {a: sh.get(a) for a, _ in PARAMS if sh.getCellFromAlias(a)}
    return r


def resize(d, h):
    d.getObject('Params').set('plate_height', str(h))
    d.recompute()
    d.recompute()


def yourturn():
    """the your-turn rectangle, by code: drawn away from the origin as the rectangle tool makes it (4 joins, 2 flat,
    2 upright), sizes 40 and 30, then the bottom-left corner tied to the origin and 40 -> 60."""
    d = FreeCAD.newDocument('yourturn')
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
    sk.solve()
    r = {'dof_drawn': sk.DoF}
    w = sk.addConstraint(Sketcher.Constraint('Distance', 0, 40))
    sk.addConstraint(Sketcher.Constraint('Distance', 1, 30))
    sk.solve()
    r['dof_sized'] = sk.DoF
    r['sized_corners'] = [[round(g.StartPoint.x, 4), round(g.StartPoint.y, 4)] for g in sk.Geometry]
    sk.addConstraint(Sketcher.Constraint('Coincident', 0, 1, -1, 1))
    sk.solve()
    r['dof_pinned'] = sk.DoF
    r['pinned_corner_before'] = round(sk.Geometry[0].StartPoint.x, 6)
    sk.setDatum(w, FreeCAD.Units.Quantity('60 mm'))
    sk.solve()
    d.recompute()
    g = sk.Geometry[0]
    r['pinned_corner_after'] = round(g.StartPoint.x, 6)
    r['far_side_after'] = round(g.EndPoint.x, 6)
    r['width_after'] = round(g.EndPoint.x - g.StartPoint.x, 6)
    r['corners_after'] = [[round(x.StartPoint.x, 4), round(x.StartPoint.y, 4)] for x in sk.Geometry]
    FreeCAD.closeDocument(d.Name)
    return r


def build():
    os.makedirs(OUT, exist_ok=True)
    allr = {}
    for kind in ('pinned', 'unpinned'):
        d = hook_doc('hook_' + kind, kind == 'pinned')
        p = os.path.join(OUT, 'hook-%s.FCStd' % kind)
        d.saveAs(p)
        allr['%s_60' % kind] = dict(measure(d), file=p)
        FreeCAD.closeDocument(d.Name)
        for seq in ((80,), (100,), (80, 100)):
            d = FreeCAD.openDocument(p)
            for h in seq:
                resize(d, h)
            key = '%s_%s' % (kind, '_'.join(map(str, seq)))
            allr[key] = measure(d)
            if seq == (80,):
                q = os.path.join(OUT, 'hook-%s-80.FCStd' % kind)
                d.saveAs(q)
                allr[key]['file'] = q
            FreeCAD.closeDocument(d.Name)
    allr['yourturn'] = yourturn()
    json.dump(allr, open(os.path.join(OUT, 'build.json'), 'w'), indent=1)
    log('build', json.dumps({k: (v.get('dof'), v.get('zmin'), v.get('zmax'), v.get('hole_to_top'), v.get('sketch_hole_to_top'))
                             for k, v in allr.items() if k != 'yourturn'}))
    log('yourturn', json.dumps(allr['yourturn']))


def check(doc_path, out, h=None):
    if h is not None:
        tmp = '/tmp/fc10-resize.FCStd'
        shutil.copy(doc_path, tmp)
        doc_path = tmp
    d = FreeCAD.openDocument(doc_path)
    if h is not None:
        resize(d, h)
    else:
        d.recompute()
    r = dict(measure(d), doc=doc_path, objects=[(o.Name, o.Label, o.TypeId) for o in d.Objects][:80])
    json.dump(r, open(out, 'w'), indent=1)
    log('check', json.dumps({k: r.get(k) for k in ('dof', 'zmin', 'zmax', 'xmin', 'hole_to_top', 'sketch_hole_to_top',
                                                    'volume_mm3', 'constraints')}))


if MODE == 'build':
    build()
elif MODE == 'check':
    check(os.environ['FC10_DOC'], OUT)
elif MODE == 'resize':
    check(os.environ['FC10_DOC'], OUT, float(os.environ['FC10_H']))
