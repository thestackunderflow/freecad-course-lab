"""fc12 (FreeCAD course lesson 12, hooks round a post: PolarPattern Extent vs Spacing), lab instrument run by
freecadcmd, never filmed.

    FC12_OUT=/lab/out/fc12/P FC12_MODE=build freecadcmd /lab/lab/fc12parts.py
        stand-ring (6 / 360 Extent), stand-trap (hooks 4, Extent 240), stand-fixed (hooks 4, Spacing =Params.hook_gap),
        stand-typed180 (hooks 4, Extent 180, the control); the proof (hooks 3, 6), the hooks-7 edge and the your-turn
        (8 hooks on a wider post at 360 / 315 / 270), every number read back by code -> build.json.
    FC12_DOC=x.FCStd FC12_OUT=y.json FC12_MODE=check [FC12_HOOKS=3] freecadcmd /lab/lab/fc12parts.py
The part: a post (circle d = post_diameter on XY, padded plate_height) and lesson 3's hook on XZ, its back face at
radius post_diameter / 2 - 1 (one solid), arm and lip out along +X (the first hook at 0 deg), padded width both ways.
Occurrences = Params.hooks in every file. A hook's angle = the direction of its lip's outer face centre."""
import json
import math
import os
import shutil
import sys

import FreeCAD
import Part
import Sketcher

OUT = os.environ.get('FC12_OUT', '/lab/out/fc12/P')
MODE = os.environ.get('FC12_MODE', 'build')
V = FreeCAD.Vector
PROFILE = [(0, 0), (25, 0), (25, 10), (20, 10), (20, 5), (5, 5), (5, 60), (0, 60)]
PARAMS = (('plate_height', '60'), ('thickness', '5'), ('hook_depth', '25'), ('lip_height', '10'), ('width', '20'),
          ('post_diameter', '50'), ('hooks', '6'), ('hook_gap', '60 deg'))


def log(*a):
    print('FC12', *a)
    sys.stdout.flush()


def origin(body, role):
    return [o for o in body.Origin.OriginFeatures if o.Role == role][0]


def sized(sk, con, name, expr):
    c = sk.addConstraint(con)
    sk.renameConstraint(c, name)
    sk.setExpression('.Constraints.' + name, expr)


def stand_doc(name, hooks=6, mode='Extent', angle=360.0, angle_expr=None, offset_expr=None, offset=None,
              post_diameter=50):
    d = FreeCAD.newDocument(name)
    s = d.addObject('Spreadsheet::Sheet', 'Params')
    for i, (n, v) in enumerate(PARAMS, 1):
        if n == 'hooks':
            v = str(hooks)
        if n == 'post_diameter':
            v = str(post_diameter)
        s.set('A%d' % i, n)
        s.set('B%d' % i, v)
        s.setAlias('B%d' % i, n)
    d.recompute()
    b = d.addObject('PartDesign::Body', 'Body')
    b.Label = 'Stand'
    ps = b.newObject('Sketcher::SketchObject', 'PostSketch')
    ps.AttachmentSupport = [(origin(b, 'XY_Plane'), '')]
    ps.MapMode = 'FlatFace'
    ps.addGeometry(Part.Circle(V(0, 0, 0), V(0, 0, 1), post_diameter / 2.0))
    ps.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
    sized(ps, Sketcher.Constraint('Diameter', 0, post_diameter), 'post_diameter', 'Params.post_diameter')
    post = b.newObject('PartDesign::Pad', 'Post')
    post.Profile = ps
    post.setExpression('Length', 'Params.plate_height')
    hk = b.newObject('Sketcher::SketchObject', 'HookSketch')
    hk.AttachmentSupport = [(origin(b, 'XZ_Plane'), '')]
    hk.MapMode = 'FlatFace'
    d.recompute()
    ux = hk.getGlobalPlacement().Rotation.multVec(V(1, 0, 0))
    sx = 1 if ux.x > 0 else -1                       # sketch u -> world X sign (read, not assumed)
    r0 = post_diameter / 2.0 - 1
    n = len(PROFILE)
    pts = [(sx * (r0 + a), c) for a, c in PROFILE]
    for i in range(n):
        a, c = pts[i], pts[(i + 1) % n]
        hk.addGeometry(Part.LineSegment(V(a[0], a[1], 0), V(c[0], c[1], 0)))
    for i in range(n):
        hk.addConstraint(Sketcher.Constraint('Coincident', i, 2, (i + 1) % n, 1))
    for i in range(n):
        hk.addConstraint(Sketcher.Constraint('Horizontal' if i % 2 == 0 else 'Vertical', i))
    sized(hk, Sketcher.Constraint('Distance', 0, 25), 'hook_depth', 'Params.hook_depth')
    sized(hk, Sketcher.Constraint('Distance', 1, 10), 'lip_height', 'Params.lip_height')
    sized(hk, Sketcher.Constraint('Distance', 2, 5), 'lip_thickness', 'Params.thickness')
    sized(hk, Sketcher.Constraint('Distance', 6, 5), 'thickness', 'Params.thickness')
    sized(hk, Sketcher.Constraint('Distance', 7, 60), 'plate_height', 'Params.plate_height')
    sized(hk, Sketcher.Constraint('DistanceY', 0, 1, 4, 1, 5), 'arm_thickness', 'Params.thickness')
    sized(hk, Sketcher.Constraint('DistanceX', -1, 1, 0, 1, sx * r0), 'back_radius',
          '%s(Params.post_diameter / 2 - 1)' % ('-' if sx < 0 else ''))
    hk.addConstraint(Sketcher.Constraint('PointOnObject', 0, 1, -1))
    hook = b.newObject('PartDesign::Pad', 'Hook')
    hook.Profile = hk
    hook.setExpression('Length', 'Params.width')
    hook.SideType = 'Symmetric'                     # 1.1: Midplane is deprecated (its notice showed in the first takes)
    d.recompute()
    p = b.newObject('PartDesign::PolarPattern', 'PolarPattern')
    p.Originals = [hook]
    p.Axis = (origin(b, 'Z_Axis'), [''])
    p.setExpression('Occurrences', 'Params.hooks')
    p.Mode = mode
    if mode == 'Extent':
        if angle_expr:
            p.setExpression('Angle', angle_expr)
        else:
            p.Angle = angle
    else:
        if offset_expr:
            p.setExpression('Offset', offset_expr)
        else:
            p.Offset = offset
    b.Tip = p
    d.recompute()
    return d


def pattern_info(d):
    for o in d.Objects:
        if o.TypeId == 'PartDesign::PolarPattern':
            ex = dict((k.lstrip('.'), v) for k, v in o.ExpressionEngine)
            return {'name': o.Name, 'mode': getattr(o, 'Mode', None), 'angle': round(o.Angle.Value, 6),
                    'offset': round(o.Offset.Value, 6) if hasattr(o, 'Offset') else None,
                    'occurrences': o.Occurrences, 'spacings': [round(x.Value if hasattr(x, 'Value') else x, 6)
                                                               for x in getattr(o, 'Spacings', [])],
                    'reversed': bool(getattr(o, 'Reversed', False)), 'axis': str(o.Axis)[-60:],
                    'originals': [x.Name for x in o.Originals], 'expr': ex,
                    'occ_expr': ex.get('Occurrences'), 'angle_expr': ex.get('Angle'), 'offset_expr': ex.get('Offset'),
                    'state': list(o.State)}
    return None


def lip_angles(shape, r_lip):
    """angles (deg, [0, 360)) of the lip outer faces: planar faces whose centre is at radius r_lip and whose normal points
    out; rounded, deduplicated (a hook on a hook counts once; raw count kept)"""
    raw = []
    for f in shape.Faces:
        if 'Plane' not in f.Surface.TypeId:
            continue
        c = f.CenterOfMass
        r = math.hypot(c.x, c.y)
        if abs(r - r_lip) > 0.05:
            continue
        nrm = f.normalAt(*f.Surface.parameter(c))
        if abs(nrm.z) > 1e-6 or (nrm.x * c.x + nrm.y * c.y) / r < 0.99:
            continue
        raw.append(round(math.degrees(math.atan2(c.y, c.x)) % 360.0, 4) % 360.0)
    uniq = []
    for a in sorted(raw):
        if not uniq or abs(a - uniq[-1]) > 0.01:
            uniq.append(a)
    if len(uniq) > 1 and abs(uniq[0] + 360 - uniq[-1]) < 0.01:
        uniq.pop()
    return uniq, len(raw)


def clearance(d, gap):
    """smallest distance between the hook and a copy turned by gap degrees round Z (the hook pad's added solid)"""
    h = d.getObject('Hook')
    s = h.AddSubShape.copy()
    t = s.copy()
    t.rotate(V(0, 0, 0), V(0, 0, 1), gap)
    return round(s.distToShape(t)[0], 4)


def measure(d):
    b = [o for o in d.Objects if o.TypeId == 'PartDesign::Body'][0]
    s = b.Shape
    sheet = d.getObject('Params')
    pd = float(sheet.get('post_diameter'))
    hd = float(sheet.get('hook_depth'))
    angles, raw = lip_angles(s, pd / 2.0 - 1 + hd)
    gaps = [round(angles[i + 1] - angles[i], 4) for i in range(len(angles) - 1)]
    pat = pattern_info(d)
    occ_expr = (pat or {}).get('occ_expr') or ''
    r = {'angles': angles, 'gaps': gaps, 'lip_faces': raw, 'hooks_seen': len(angles), 'solids': len(s.Solids),
         'valid': s.isValid(), 'volume': round(s.Volume, 3), 'pattern': pat,
         'count_bound': 'hooks' in occ_expr,
         'side_ok': bool(angles) and all(-0.01 <= a <= 180.01 for a in angles),
         'into_wall': any(180.01 < a < 359.99 for a in angles),
         'sheet': {k: str(sheet.get(k)) for k, _ in PARAMS},
         'states': {o.Name: list(o.State) for o in d.Objects if o.TypeId.startswith(('Sketcher::', 'PartDesign::'))}}
    if gaps:
        try:
            r['clearance_mm'] = clearance(d, min(gaps))
        except Exception as e:                         # a Claude file without our Hook pad
            r['clearance_mm'] = None
            r['clearance_err'] = str(e)[:80]
    return r


def set_hooks(d, n):
    d.getObject('Params').set('hooks', str(n))
    d.recompute()
    d.recompute()


def build():
    os.makedirs(OUT, exist_ok=True)
    allr = {}
    files = {'ring': dict(hooks=6), 'trap': dict(hooks=4, angle=240.0),
             'fixed': dict(hooks=4, mode='Spacing', offset_expr='Params.hook_gap'),
             'typed180': dict(hooks=4, angle=180.0)}
    for k, kw in files.items():
        d = stand_doc('stand_' + k, **kw)
        p = os.path.join(OUT, 'stand-%s.FCStd' % k)
        d.saveAs(p)
        allr[k] = dict(measure(d), file=p)
        FreeCAD.closeDocument(d.Name)
    for k, ns in (('fixed', (3, 6, 7)), ('typed180', (3, 6)), ('ring', (7, 4)), ('trap', (3, 6))):
        for n in ns:
            d = FreeCAD.openDocument(os.path.join(OUT, 'stand-%s.FCStd' % k))
            set_hooks(d, n)
            allr['%s_h%d' % (k, n)] = measure(d)
            FreeCAD.closeDocument(d.Name)
    # the switch to Spacing on the trap file (C20): Offset default 120 -> preview 0/120/240/360
    d = FreeCAD.openDocument(os.path.join(OUT, 'stand-trap.FCStd'))
    pp = d.getObject('PolarPattern')
    pp.Mode = 'Spacing'
    d.recompute()
    allr['trap_spacing_default'] = measure(d)
    FreeCAD.closeDocument(d.Name)
    # your turn (Q7): 8 hooks on a wider post (80) at 360 / 315 / 270
    for a in (360, 315, 270):
        d = stand_doc('yt_%d' % a, hooks=8, angle=float(a), post_diameter=80)
        allr['yt_%d' % a] = measure(d)
        FreeCAD.closeDocument(d.Name)
    # 8 hooks at 360 on this post (they touch: never shown)
    d = stand_doc('eight50', hooks=8)
    allr['eight_on_50'] = measure(d)
    FreeCAD.closeDocument(d.Name)
    json.dump(allr, open(os.path.join(OUT, 'build.json'), 'w'), indent=1)
    log('build', json.dumps({k: (v['angles'], v['solids'], v.get('clearance_mm'), v['count_bound']) for k, v in allr.items()}))


def check(doc_path, out, hooks=None):
    if hooks is not None:
        tmp = '/tmp/fc12-hooks.FCStd'
        shutil.copy(doc_path, tmp)
        doc_path = tmp
    d = FreeCAD.openDocument(doc_path)
    if hooks is not None:
        set_hooks(d, hooks)
    else:
        d.recompute()
    try:
        r = dict(measure(d), doc=doc_path)
    except Exception as e:
        r = {'error': str(e)[:200], 'doc': doc_path}
    r['objects'] = [(o.Name, o.Label, o.TypeId) for o in d.Objects][:80]
    json.dump(r, open(out, 'w'), indent=1)
    log('check', json.dumps({k: r.get(k) for k in ('angles', 'gaps', 'solids', 'count_bound', 'side_ok', 'error')}))


if MODE == 'build':
    build()
elif MODE == 'check':
    h = os.environ.get('FC12_HOOKS')
    check(os.environ['FC12_DOC'], OUT, int(h) if h else None)
