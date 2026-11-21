"""fc14 (FreeCAD course lesson 14, a key peg on the wall cup: the Thickness's place in the Body), lab instrument run
by freecadcmd, never filmed.

    FC14_OUT=/lab/out/fc14/P FC14_MODE=build freecadcmd /lab/lab/fc14parts.py
        peg-noshell (box + peg), peg-trap (box, peg, Thickness outward), peg-fixed (box, Thickness, peg); proof (wall 3,
        peg_size 12), comparison (trap at wall 3), the headless Move Feature After (route b), a face-picked peg through
        it (Q3d), edges (inward, separate Body), your turn and Short boxes; every number read back by code -> build.json.
    FC14_DOC=x.FCStd FC14_OUT=y.json FC14_MODE=check freecadcmd /lab/lab/fc14parts.py
        a saved file: the cup Body's shape as stored, recomputed, at wall 2 and wall 3 (PLAN 2.5 score), plus the tree.
The part (PLAN 2.1): Params cup_width 60, cup_length 40, cup_height 50, wall 2, peg_size 10, peg_length 15. Body: box
sketch on XY centred (Params.cup_width x Params.cup_length), Pad Params.cup_height; peg sketch on the XZ origin plane,
attachment offset z = Params.cup_length / 2 (XZ normal is -Y, so the plane sits at y -20), a square Params.peg_size
centred x 0, z 40, Pad Params.peg_length (to y -35); Thickness on the top face, Value Params.wall, outward (Reversed
false). Reads are lines through the solid (common with a line) and isInside point tests."""
import json
import os
import re
import shutil
import sys

import FreeCAD
import Part
import Sketcher

OUT = os.environ.get('FC14_OUT', '/lab/out/fc14/P')
MODE = os.environ.get('FC14_MODE', 'build')
V = FreeCAD.Vector
PARAMS = (('cup_width', 60), ('cup_length', 40), ('cup_height', 50), ('wall', 2), ('peg_size', 10), ('peg_length', 15))
REF = re.compile(r'Params\.([A-Za-z_][A-Za-z0-9_]*)')


def log(*a):
    print('FC14', *a)
    sys.stdout.flush()


def origin(body, role):
    return [o for o in body.Origin.OriginFeatures if o.Role == role][0]


def rect(sk, x0, y0, w, h, names=None):
    """a w x h rectangle with its lower-left corner at (x0, y0) in the sketch; names = (width name, expr, pos exprs)"""
    pts = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    for i in range(4):
        a, c = pts[i], pts[(i + 1) % 4]
        sk.addGeometry(Part.LineSegment(V(a[0], a[1], 0), V(c[0], c[1], 0)))
    for i in range(4):
        sk.addConstraint(Sketcher.Constraint('Coincident', i, 2, (i + 1) % 4, 1))
    sk.addConstraint(Sketcher.Constraint('Horizontal', 0))
    sk.addConstraint(Sketcher.Constraint('Horizontal', 2))
    sk.addConstraint(Sketcher.Constraint('Vertical', 1))
    sk.addConstraint(Sketcher.Constraint('Vertical', 3))
    cw = sk.addConstraint(Sketcher.Constraint('DistanceX', 0, 1, 0, 2, w))
    ch = sk.addConstraint(Sketcher.Constraint('DistanceY', 1, 1, 1, 2, h))
    return cw, ch


def box_sketch(b):
    sk = b.newObject('Sketcher::SketchObject', 'Sketch')
    sk.AttachmentSupport = [(origin(b, 'XY_Plane'), '')]
    sk.MapMode = 'FlatFace'
    cw, ch = rect(sk, -30, -20, 60, 40)
    sk.renameConstraint(cw, 'cup_width')
    sk.renameConstraint(ch, 'cup_length')
    sk.setExpression('.Constraints.cup_width', 'Params.cup_width')
    sk.setExpression('.Constraints.cup_length', 'Params.cup_length')
    sk.addConstraint(Sketcher.Constraint('Symmetric', 0, 1, 1, 2, -1, 1))
    return sk


def peg_sketch_plane(b, peg):
    """on the XZ origin plane moved to the drawn front line (offset bound to Params.cup_length / 2); sketch x = X,
    sketch y = Z (checked by the peg's extents in build)"""
    sk = b.newObject('Sketcher::SketchObject', 'Sketch001')
    sk.AttachmentSupport = [(origin(b, 'XZ_Plane'), '')]
    sk.MapMode = 'FlatFace'
    sk.AttachmentOffset = FreeCAD.Placement(V(0, 0, 20), FreeCAD.Rotation())
    sk.setExpression('.AttachmentOffset.Base.z', 'Params.cup_length / 2')
    cw, ch = rect(sk, -peg / 2.0, 40 - peg / 2.0, peg, peg)
    sk.renameConstraint(cw, 'peg_size')
    sk.renameConstraint(ch, 'peg_size_z')
    sk.setExpression('.Constraints.peg_size', 'Params.peg_size')
    sk.setExpression('.Constraints.peg_size_z', 'Params.peg_size')
    px = sk.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, 0, 1, -peg / 2.0))
    pz = sk.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, 0, 1, 40 - peg / 2.0))
    sk.renameConstraint(px, 'peg_x0')
    sk.renameConstraint(pz, 'peg_z0')
    sk.setExpression('.Constraints.peg_x0', '-Params.peg_size / 2')
    sk.setExpression('.Constraints.peg_z0', '40 - Params.peg_size / 2')
    return sk


def front_face(shape, y):
    for i, f in enumerate(shape.Faces, 1):
        if 'Plane' in f.Surface.TypeId and abs(f.CenterOfMass.y - y) < 1e-6:
            n = f.normalAt(*f.Surface.parameter(f.CenterOfMass))
            if n.y < -0.999:
                return 'Face%d' % i
    return None


def peg_sketch_face(d, b, pad, peg):
    """Q3d: the way most viewers draw it, a sketch on the box Pad's front face (y -20); typed, local frame read back"""
    sk = b.newObject('Sketcher::SketchObject', 'Sketch001')
    sk.AttachmentSupport = [(pad, front_face(pad.Shape, -20))]
    sk.MapMode = 'FlatFace'
    d.recompute()
    inv = sk.Placement.inverse()
    c0 = inv.multVec(V(-peg / 2.0, -20, 40 - peg / 2.0))
    c1 = inv.multVec(V(peg / 2.0, -20, 40 + peg / 2.0))
    x0, x1, y0, y1 = min(c0.x, c1.x), max(c0.x, c1.x), min(c0.y, c1.y), max(c0.y, c1.y)
    rect(sk, x0, y0, x1 - x0, y1 - y0)
    return sk


def top_face(shape):
    best = None
    for i, f in enumerate(shape.Faces, 1):
        if 'Plane' not in f.Surface.TypeId:
            continue
        n = f.normalAt(*f.Surface.parameter(f.CenterOfMass))
        if n.z > 0.999 and (best is None or f.CenterOfMass.z > best[1]):
            best = ('Face%d' % i, f.CenterOfMass.z)
    return best[0]


def add_thickness(d, b, base, reversed_):
    t = b.newObject('PartDesign::Thickness', 'Thickness')
    t.Base = (base, [top_face(base.Shape)])
    t.setExpression('Value', 'Params.wall')
    t.Reversed = reversed_
    d.recompute()
    return t


def add_peg(d, b, peg, on_face=False, pad=None, body=None):
    bb = body or b
    sk = peg_sketch_face(d, bb, pad, peg) if on_face else peg_sketch_plane(bb, peg)
    p = bb.newObject('PartDesign::Pad', 'Pad001')
    p.Profile = sk
    if on_face:
        p.Length = 15
    else:
        p.setExpression('Length', 'Params.peg_length')
    d.recompute()
    return p


def peg_doc(name, order='before', wall=2, peg=10, reversed_=False, on_face=False, sep_body=False):
    """order: 'noshell' (box + peg), 'before' (box, peg, Thickness: the trap), 'after' (box, Thickness, peg: fixed)"""
    d = FreeCAD.newDocument(name)
    s = d.addObject('Spreadsheet::Sheet', 'Params')
    vals = dict(PARAMS)
    vals.update(wall=wall, peg_size=peg)
    for i, (n, _) in enumerate(PARAMS, 1):
        s.set('A%d' % i, n)
        s.set('B%d' % i, str(vals[n]))
        s.setAlias('B%d' % i, n)
    d.recompute()
    b = d.addObject('PartDesign::Body', 'Body')
    b.Label = 'Cup'
    sk = box_sketch(b)
    pad = b.newObject('PartDesign::Pad', 'Pad')
    pad.Profile = sk
    pad.setExpression('Length', 'Params.cup_height')
    d.recompute()
    if sep_body:
        t = add_thickness(d, b, pad, reversed_)
        b2 = d.addObject('PartDesign::Body', 'PegBody')
        add_peg(d, b, peg, body=b2)
        b.Tip = t
        d.recompute()
        return d
    if order in ('noshell', 'before'):
        p = add_peg(d, b, peg, on_face, pad)
        if order == 'before':
            add_thickness(d, b, p, reversed_)
    else:
        add_thickness(d, b, pad, reversed_)
        add_peg(d, b, peg, on_face, pad)
    d.recompute()
    return d


def main_body(d):
    bs = [o for o in d.Objects if o.TypeId == 'PartDesign::Body']
    for b in bs:
        if b.Name == 'Body':
            return b
    return bs[0] if bs else None


def segs(shape, p0, p1):
    line = Part.LineSegment(p0, p1).toShape()
    c = shape.common(line)
    ax = 0 if abs(p1.x - p0.x) > 1e-9 else (1 if abs(p1.y - p0.y) > 1e-9 else 2)
    out = []
    for e in c.Edges:
        a, b = e.Vertexes[0].Point[ax], e.Vertexes[-1].Point[ax]
        out.append((round(min(a, b), 4), round(max(a, b), 4)))
    out.sort()
    merged = []
    for a, b in out:
        if merged and a - merged[-1][1] < 1e-6:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    return merged


def param(d, alias):
    s = d.getObject('Params')
    try:
        return float(s.get(alias))
    except Exception:
        return None


def thickness_info(d):
    for o in d.Objects:
        if o.TypeId == 'PartDesign::Thickness':
            ex = dict((k.lstrip('.'), v) for k, v in o.ExpressionEngine)
            return {'name': o.Name, 'value': round(o.Value.Value, 6), 'value_expr': ex.get('Value'),
                    'reversed': bool(o.Reversed), 'join': str(o.Join),
                    'base': [o.Base[0].Name if o.Base else None, list(o.Base[1]) if o.Base else []],
                    'base_feature': o.BaseFeature.Name if o.BaseFeature else None, 'state': list(o.State)}
    return None


def tree(d):
    b = main_body(d)
    out = {'bodies': [o.Name for o in d.Objects if o.TypeId == 'PartDesign::Body']}
    if b:
        out['group'] = [o.Name for o in b.Group if o.TypeId.startswith('PartDesign::') and 'Origin' not in o.TypeId
                        or o.TypeId == 'Sketcher::SketchObject']
        out['tip'] = b.Tip.Name if b.Tip else None
        out['base_features'] = {o.Name: (o.BaseFeature.Name if getattr(o, 'BaseFeature', None) else None)
                                for o in b.Group if o.TypeId.startswith('PartDesign::') and hasattr(o, 'BaseFeature')}
    out['visible'] = [o.Name for o in d.Objects if getattr(o, 'Visibility', False)
                      and o.TypeId.startswith(('PartDesign::', 'Part::'))]
    return out


def peg_attach(d):
    for o in d.Objects:
        if o.TypeId == 'Sketcher::SketchObject' and o.Name != 'Sketch':
            ex = dict((k.lstrip('.'), v) for k, v in o.ExpressionEngine)
            sup = o.AttachmentSupport
            return {'name': o.Name, 'support': sup[0][0].Role if sup and hasattr(sup[0][0], 'Role') else
                    (sup[0][0].Name + ':' + ','.join(sup[0][1]) if sup else None),
                    'map_mode': str(o.MapMode), 'offset_z': round(o.AttachmentOffset.Base.z, 4),
                    'offset_expr': ex.get('AttachmentOffset.Base.z'), 'state': list(o.State),
                    'origin': [round(o.Placement.Base[i], 4) for i in range(3)]}
    return None


def measure(d, shape=None):
    b = main_body(d)
    s = shape if shape is not None else b.Shape
    w = param(d, 'wall') or 0.0
    L = param(d, 'cup_length') or 40.0
    r = {'solids': len(s.Solids), 'volume': round(s.Volume, 3), 'valid': s.isValid(), 'wall_param': param(d, 'wall'),
         'peg_param': param(d, 'peg_size')}
    bb = s.BoundBox
    r['bbox'] = [round(v, 3) for v in (bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax)]
    inside = lambda p: s.isInside(p, 1e-6, True)
    sx = segs(s, V(-80, 0, 25), V(80, 0, 25))
    sy = segs(s, V(0, -19.0, 25), V(0, 80, 25))
    sy_out = segs(s, V(0, -80, 25), V(0, 80, 25))
    r['outside_w'] = round(sx[-1][1] - sx[0][0], 4) if sx else None
    r['inside_w'] = round(sx[1][0] - sx[0][1], 4) if len(sx) >= 2 else None
    r['outside_l'] = round(sy_out[-1][1] - sy_out[0][0], 4) if sy_out else None
    r['inside_l'] = round(sy_out[1][0] - sy_out[0][1], 4) if len(sy_out) >= 2 else None
    sz = segs(s, V(0, 0, -30), V(0, 0, 90))
    rim = segs(s, V(30 + w / 2.0, 0, -30), V(30 + w / 2.0, 0, 90))
    r['floor_top'] = sz[0][1] if sz else None
    r['rim_top'] = rim[-1][1] if rim else None
    r['inside_d'] = round(r['rim_top'] - r['floor_top'], 4) if (sz and rim and not inside(V(0, 0, 30))) else 0.0
    f = {'bottom': inside(V(0, 0, -w / 2.0)), 'lid_air': not inside(V(0, 0, 50 + w / 2.0)),
         'side_px': inside(V(30 + w / 2.0, 0, 25)), 'side_nx': inside(V(-30 - w / 2.0, 0, 25)),
         'side_back': inside(V(0, 20 + w / 2.0, 25))}
    f['ok'] = all(f.values())
    r['faces'] = f
    px = segs(s, V(-40, -30, 40), V(40, -30, 40))
    pz = segs(s, V(0, -30, 0), V(0, -30, 90))
    py = segs(s, V(0, -80, 40), V(0, -L / 2.0, 40))
    r['peg_x'] = [px[0][0], px[-1][1]] if px else None
    r['peg_z'] = [pz[0][0], pz[-1][1]] if pz else None
    r['peg_w'] = round(px[-1][1] - px[0][0], 4) if px else None
    r['peg_h'] = round(pz[-1][1] - pz[0][0], 4) if pz else None
    r['peg_x_segs'] = px
    r['peg_y'] = [py[0][0], py[-1][1]] if py else None
    r['peg_tip_y'] = py[0][0] if py else None
    r['peg_mid_solid'] = inside(V(0, -28, 40))
    r['front_wall_solid'] = inside(V(0, -L / 2.0 - w / 2.0, 40))
    ox = segs(s, V(-25, -L / 2.0 - w / 2.0, 40), V(25, -L / 2.0 - w / 2.0, 40))
    oz = segs(s, V(0, -L / 2.0 - w / 2.0, 20), V(0, -L / 2.0 - w / 2.0, 49))
    r['opening_w'] = round(ox[1][0] - ox[0][1], 4) if len(ox) == 2 else (0.0 if len(ox) == 1 else None)
    r['opening_h'] = round(oz[1][0] - oz[0][1], 4) if len(oz) == 2 else (0.0 if len(oz) == 1 else None)
    return r


def status(d):
    out = {}
    for o in d.Objects:
        if o.TypeId.startswith(('PartDesign::', 'Sketcher::')):
            if list(o.State):
                out[o.Name] = list(o.State)
    return out


def safe(d, extra=None):
    try:
        r = measure(d)
    except Exception as e:
        r = {'error': str(e)[:300]}
    r['status'] = status(d)
    r['tree'] = tree(d)
    r['thickness'] = thickness_info(d)
    r['peg_attach'] = peg_attach(d)
    if extra:
        r.update(extra)
    return r


def touch_all(d):
    for o in d.Objects:
        if o.TypeId.startswith('PartDesign::') and o.TypeId != 'PartDesign::Body':
            o.touch()
    d.recompute()


def set_cell(d, alias, val):
    d.getObject('Params').set(alias, str(val))
    d.recompute()
    touch_all(d)


def move_after(d, feat, target):
    """route (b) by code: the same calls CommandBody.cpp's Move Feature After makes (removeObject, insertObject after)"""
    b = main_body(d)
    f, t = d.getObject(feat), d.getObject(target)
    before = {'tip': b.Tip.Name, 'base': thickness_info(d)['base']}
    b.removeObject(f)
    b.insertObject(f, t, True)
    d.recompute()
    return {'before': before, 'tip_after': b.Tip.Name, 'base_after': thickness_info(d)['base']}


def build():
    os.makedirs(OUT, exist_ok=True)
    allr = {}
    for k, kw in (('noshell', dict(order='noshell')), ('trap', dict(order='before')), ('fixed', dict(order='after'))):
        d = peg_doc('peg_' + k, **kw)
        p = os.path.join(OUT, 'peg-%s.FCStd' % k)
        d.saveAs(p)
        allr[k] = dict(safe(d), file=p)
        if k == 'fixed':
            set_cell(d, 'wall', 3)
            allr['fixed_wall3'] = safe(d)
            set_cell(d, 'peg_size', 12)
            allr['fixed_peg12'] = safe(d)
        if k == 'trap':
            set_cell(d, 'wall', 3)
            allr['trap_wall3'] = safe(d)
        FreeCAD.closeDocument(d.Name)
    # route (b) by code on the trap (Thickness moved after Pad)
    d = peg_doc('peg_rb', order='before')
    mv = move_after(d, 'Thickness', 'Pad')
    allr['route_b_code'] = safe(d, {'move': mv})
    touch_all(d)
    allr['route_b_touched'] = safe(d)
    d.saveAs(os.path.join(OUT, 'peg-route-b.FCStd'))
    set_cell(d, 'wall', 3)
    allr['route_b_code_wall3'] = safe(d)
    set_cell(d, 'wall', 2)
    t = d.getObject('Thickness')        # the fallback: pick the top face again (now the Pad's own top face)
    t.Base = (d.getObject('Pad'), [top_face(d.getObject('Pad').Shape)])
    touch_all(d)
    allr['route_b_repick'] = safe(d)
    set_cell(d, 'wall', 3)
    allr['route_b_repick_wall3'] = safe(d)
    set_cell(d, 'peg_size', 12)
    allr['route_b_repick_peg12'] = safe(d)
    FreeCAD.closeDocument(d.Name)
    # route (a) by code: the peg's Pad moved after the Thickness, Tip set on it (the Move Tip question answered Yes)
    d = peg_doc('peg_ra', order='before')
    b = main_body(d)
    p1, sk1, t = d.getObject('Pad001'), d.getObject('Sketch001'), d.getObject('Thickness')
    b.removeObject(p1)
    b.insertObject(p1, t, True)
    b.Tip = p1
    touch_all(d)
    allr['route_a_code'] = safe(d)
    FreeCAD.closeDocument(d.Name)
    # Q3d: a face-picked peg (sketch on the box Pad's front face), the trap, then the same move
    d = peg_doc('peg_face', order='before', on_face=True)
    allr['face_trap'] = safe(d)
    d.saveAs(os.path.join(OUT, 'peg-face-trap.FCStd'))
    try:
        mv = move_after(d, 'Thickness', 'Pad')
        allr['face_moved'] = safe(d, {'move': mv})
        touch_all(d)
        allr['face_moved_touched'] = safe(d)
    except Exception as e:
        allr['face_moved'] = {'error': str(e)[:300]}
    FreeCAD.closeDocument(d.Name)
    # route (c) by code (the GUI route the lab films): delete Thickness, Tip on Pad, new Thickness, Tip on Pad001;
    # on the plane peg and on the face-picked peg (Q3c / Q3d: does the peg sketch stay attached?)
    for k, kw in (('route_c_code', dict(order='before')), ('face_route_c', dict(order='before', on_face=True))):
        d = peg_doc('peg_' + k, **kw)
        b = main_body(d)
        d.removeObject('Thickness')
        b.Tip = d.getObject('Pad')
        d.recompute()
        t = b.newObject('PartDesign::Thickness', 'Thickness')
        t.Base = (d.getObject('Pad'), [top_face(d.getObject('Pad').Shape)])
        t.setExpression('Value', 'Params.wall')
        t.Reversed = False
        b.Tip = d.getObject('Pad001')
        touch_all(d)
        allr[k] = safe(d)
        set_cell(d, 'wall', 3)
        allr[k + '_wall3'] = safe(d)
        FreeCAD.closeDocument(d.Name)
    # edges (pinned comment only): inward with the peg joined first; a separate-body peg
    d = peg_doc('peg_in', order='before', reversed_=True)
    allr['edge_inward_before'] = safe(d)
    FreeCAD.closeDocument(d.Name)
    d = peg_doc('peg_in2', order='after', reversed_=True)
    allr['edge_inward_after'] = safe(d)
    FreeCAD.closeDocument(d.Name)
    d = peg_doc('peg_sep', sep_body=True)
    r = safe(d)
    r['peg_body_solids'] = len(d.getObject('PegBody').Shape.Solids)
    r['peg_body_volume'] = round(d.getObject('PegBody').Shape.Volume, 3)
    allr['edge_sep_body'] = r
    FreeCAD.closeDocument(d.Name)
    # your turn (peg 7, wall 3) and Short (peg 10, wall 4)
    for k, kw in (('yt_before', dict(order='before', wall=3, peg=7)), ('yt_after', dict(order='after', wall=3, peg=7)),
                  ('short_before', dict(order='before', wall=4, peg=10)),
                  ('short_after', dict(order='after', wall=4, peg=10))):
        d = peg_doc('peg_' + k, **kw)
        allr[k] = safe(d)
        FreeCAD.closeDocument(d.Name)
    json.dump(allr, open(os.path.join(OUT, 'build.json'), 'w'), indent=1)
    for k, r in allr.items():
        log(k, json.dumps({x: r.get(x) for x in ('peg_w', 'peg_h', 'peg_mid_solid', 'front_wall_solid', 'inside_w',
                                                 'inside_l', 'inside_d', 'solids', 'volume')}),
            'faces_ok', (r.get('faces') or {}).get('ok'))


def visible_fused(d):
    sh = [o.Shape for o in d.Objects if getattr(o, 'Visibility', False) and hasattr(o, 'Shape')
          and o.TypeId in ('PartDesign::Body', 'Part::Feature') or (getattr(o, 'Visibility', False)
          and o.TypeId.startswith('Part::') and hasattr(o, 'Shape'))]
    sh = [x for x in sh if not x.isNull() and x.Solids]
    if not sh:
        return None
    f = sh[0]
    for x in sh[1:]:
        f = f.fuse(x)
    return f


def check(doc_path, out):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from fc14score import passes
    res = {'doc': doc_path}
    tmp = '/tmp/fc14-check.FCStd'
    shutil.copy(doc_path, tmp)
    d = FreeCAD.openDocument(tmp)
    res['stored'] = safe(d)
    vf = visible_fused(d)
    res['visible_fused'] = measure(d, vf) if vf is not None else None
    d.recompute()
    res['recomputed'] = safe(d)
    res['objects'] = [(o.Name, o.Label, o.TypeId) for o in d.Objects][:80]
    FreeCAD.closeDocument(d.Name)
    for w in (2, 3):
        d = FreeCAD.openDocument(tmp)
        d.recompute()
        try:
            set_cell(d, 'wall', w)
            res['at_wall%d' % w] = safe(d)
        except Exception as e:
            res['at_wall%d' % w] = {'error': str(e)[:300]}
        FreeCAD.closeDocument(d.Name)
    d = FreeCAD.openDocument(tmp)
    d.recompute()
    try:
        set_cell(d, 'wall', 3)
        set_cell(d, 'peg_size', 12)
        res['at_wall3_peg12'] = safe(d)
    except Exception as e:
        res['at_wall3_peg12'] = {'error': str(e)[:300]}
    FreeCAD.closeDocument(d.Name)
    ok, detail = passes(res['at_wall2'], res['at_wall3'])
    res['pass'] = ok
    res['criteria'] = detail
    json.dump(res, open(out, 'w'), indent=1)
    log('check', json.dumps({k: (res[k].get('peg_w'), res[k].get('peg_mid_solid'), res[k].get('front_wall_solid'),
                                 res[k].get('inside_w'), res[k].get('inside_l'), res[k].get('inside_d'),
                                 (res[k].get('faces') or {}).get('ok'), res[k].get('solids'))
                             for k in ('stored', 'recomputed', 'at_wall2', 'at_wall3')}), 'PASS' if ok else 'FAIL')


if MODE == 'build':
    build()
elif MODE == 'check':
    check(os.environ['FC14_DOC'], OUT)
