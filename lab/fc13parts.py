"""fc13 (FreeCAD course lesson 13, a wall cup: Thickness and "Make thickness inwards"), lab instrument run by
freecadcmd, never filmed.

    FC13_OUT=/lab/out/fc13/P FC13_MODE=build freecadcmd /lab/lab/fc13parts.py
        cup-box (no shell), cup-trap (Thickness inward, the default), cup-fixed (outward), cup-typed (64 x 44 x 52 typed,
        Thickness =Params.wall inward: for comparison); proof (wall 3, cup_width 70), edge (inward wall 20), your turn,
        Short box, the Reversed headless route (Q3) and the hook cases (Q9), every number read back by code -> build.json.
    FC13_DOC=x.FCStd FC13_OUT=y.json FC13_MODE=check [FC13_WALL=3] [FC13_WIDTH=70] freecadcmd /lab/lab/fc13parts.py
        a saved file measured as stored, then recomputed (Thickness touched), then at wall 3 / the inside-width name 70
        (the name found by tracing the sketch's width expression, PLAN 2.5 rules).
The part: Params (cup_width 60, cup_length 40, cup_height 50, wall 2); Body: a rectangle on XY centred on the origin
(width = Params.cup_width along X, length = Params.cup_length along Y), Pad = Params.cup_height up from z 0; Thickness on
the Pad's top face, Value = Params.wall. Inside / outside are read with lines through the part's centre (common of the
solid with a line): across X at y 0, across Y at x 0 (both at mid height of the cavity), and down Z at x = y = 0."""
import json
import os
import re
import shutil
import sys

import FreeCAD
import Part
import Sketcher

OUT = os.environ.get('FC13_OUT', '/lab/out/fc13/P')
MODE = os.environ.get('FC13_MODE', 'build')
V = FreeCAD.Vector
PARAMS = (('cup_width', '60'), ('cup_length', '40'), ('cup_height', '50'), ('wall', '2'))


def log(*a):
    print('FC13', *a)
    sys.stdout.flush()


def origin(body, role):
    return [o for o in body.Origin.OriginFeatures if o.Role == role][0]


def rect_sketch(b, name, w, l, wexpr=None, lexpr=None, cx=0.0, cy=0.0):
    sk = b.newObject('Sketcher::SketchObject', name)
    sk.AttachmentSupport = [(origin(b, 'XY_Plane'), '')]
    sk.MapMode = 'FlatFace'
    x0, x1, y0, y1 = cx - w / 2.0, cx + w / 2.0, cy - l / 2.0, cy + l / 2.0
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for i in range(4):
        a, c = pts[i], pts[(i + 1) % 4]
        sk.addGeometry(Part.LineSegment(V(a[0], a[1], 0), V(c[0], c[1], 0)))
    for i in range(4):
        sk.addConstraint(Sketcher.Constraint('Coincident', i, 2, (i + 1) % 4, 1))
    sk.addConstraint(Sketcher.Constraint('Horizontal', 0))
    sk.addConstraint(Sketcher.Constraint('Horizontal', 2))
    sk.addConstraint(Sketcher.Constraint('Vertical', 1))
    sk.addConstraint(Sketcher.Constraint('Vertical', 3))
    c = sk.addConstraint(Sketcher.Constraint('DistanceX', 0, 1, 0, 2, w))
    sk.renameConstraint(c, 'cup_width')
    if wexpr:
        sk.setExpression('.Constraints.cup_width', wexpr)
    c = sk.addConstraint(Sketcher.Constraint('DistanceY', 1, 1, 1, 2, l))
    sk.renameConstraint(c, 'cup_length')
    if lexpr:
        sk.setExpression('.Constraints.cup_length', lexpr)
    if cx == 0 and cy == 0:      # centred on the origin: the diagonal's midpoint on the origin
        sk.addConstraint(Sketcher.Constraint('Symmetric', 0, 1, 1, 2, -1, 1))
    else:
        sk.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, 0, 1, x0))
        sk.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, 0, 1, y0))
    return sk


def top_face(shape, ztop=None):
    """'FaceN' of the planar face with normal +Z at the highest z (the cup's top)"""
    best = None
    for i, f in enumerate(shape.Faces, 1):
        if 'Plane' not in f.Surface.TypeId:
            continue
        n = f.normalAt(*f.Surface.parameter(f.CenterOfMass))
        if n.z > 0.999 and (best is None or f.CenterOfMass.z > best[1]):
            best = ('Face%d' % i, f.CenterOfMass.z)
    return best[0]


def cup_doc(name, width=60, length=40, height=50, wall=2, shell=True, reversed_=None, typed=None, join=None,
            hook=None):
    """typed = (w, l, h): sketch + Pad typed (no names), Thickness still =Params.wall. hook = 'before' | 'after' |
    'body': a 10 x 10 x 10 block on the +X outside wall at the foot, joined before the Thickness, padded after it, or a
    separate Body."""
    d = FreeCAD.newDocument(name)
    s = d.addObject('Spreadsheet::Sheet', 'Params')
    vals = {'cup_width': width, 'cup_length': length, 'cup_height': height, 'wall': wall}
    for i, (n, _) in enumerate(PARAMS, 1):
        s.set('A%d' % i, n)
        s.set('B%d' % i, str(vals[n]))
        s.setAlias('B%d' % i, n)
    d.recompute()
    b = d.addObject('PartDesign::Body', 'Body')
    b.Label = 'Cup'
    if typed:
        sk = rect_sketch(b, 'Sketch', typed[0], typed[1])
    else:
        sk = rect_sketch(b, 'Sketch', width, length, 'Params.cup_width', 'Params.cup_length')
    pad = b.newObject('PartDesign::Pad', 'Pad')
    pad.Profile = sk
    if typed:
        pad.Length = typed[2]
    else:
        pad.setExpression('Length', 'Params.cup_height')
    d.recompute()
    last = pad
    W = typed[0] if typed else width
    if hook == 'before':
        hs = rect_sketch(b, 'HookSketch', 10, 10, cx=W / 2.0 + 5 - 0.0, cy=0)
        hp = b.newObject('PartDesign::Pad', 'Hook')
        hp.Profile = hs
        hp.Length = 10
        d.recompute()
        last = hp
    if shell:
        t = b.newObject('PartDesign::Thickness', 'Thickness')
        t.Base = (last, [top_face(last.Shape)])
        t.setExpression('Value', 'Params.wall')
        if reversed_ is not None:
            t.Reversed = reversed_
        if join:
            t.Join = join
        d.recompute()
        last = t
    if hook == 'after':
        hs = rect_sketch(b, 'HookSketch', 10, 10, cx=W / 2.0 + 5 + (0 if not shell or reversed_ is not False else wall), cy=0)
        hp = b.newObject('PartDesign::Pad', 'Hook')
        hp.Profile = hs
        hp.Length = 10
        d.recompute()
        last = hp
    b.Tip = last
    if hook == 'body':
        b2 = d.addObject('PartDesign::Body', 'HookBody')
        hs = rect_sketch(b2, 'HookSketch', 10, 10, cx=W / 2.0 + 5, cy=0)
        hp = b2.newObject('PartDesign::Pad', 'Hook')
        hp.Profile = hs
        hp.Length = 10
    d.recompute()
    return d


def segs(shape, p0, p1):
    """[(a, b)] intervals (along the line's own axis coordinate) where the line p0-p1 lies in the solid"""
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


def thickness_info(d):
    for o in d.Objects:
        if o.TypeId == 'PartDesign::Thickness':
            ex = dict((k.lstrip('.'), v) for k, v in o.ExpressionEngine)
            return {'name': o.Name, 'value': round(o.Value.Value, 6), 'value_expr': ex.get('Value'),
                    'reversed': bool(o.Reversed), 'mode': str(o.Mode), 'join': str(o.Join),
                    'intersection': bool(o.Intersection), 'base': [o.Base[0].Name if o.Base else None,
                                                                   list(o.Base[1]) if o.Base else []],
                    'state': list(o.State), 'in_tip_chain': None}
    return None


def main_body(d):
    bs = [o for o in d.Objects if o.TypeId == 'PartDesign::Body']
    for b in bs:
        if b.Name == 'Body':
            return b
    return bs[0] if bs else None


def sheet_info(d):
    s = d.getObject('Params')
    if s is None:
        return None
    out = {}
    for c in s.getUsedCells() if hasattr(s, 'getUsedCells') else []:
        a = s.getAlias(c)
        if a:
            out[a] = {'cell': c, 'content': s.getContents(c), 'value': str(s.get(c))}
    return out


def sketch_exprs(d):
    out = {}
    for o in d.Objects:
        if o.TypeId == 'Sketcher::SketchObject':
            out[o.Name] = dict((k, v) for k, v in o.ExpressionEngine)
    for o in d.Objects:
        if o.TypeId.startswith('PartDesign::') and o.ExpressionEngine:
            out[o.Name] = dict((k, v) for k, v in o.ExpressionEngine)
    return out


def measure(d):
    b = main_body(d)
    s = b.Shape
    bb = s.BoundBox
    r = {'solids': len(s.Solids), 'valid': s.isValid(), 'volume': round(s.Volume, 3),
         'outside_w': round(bb.XLength, 4), 'outside_l': round(bb.YLength, 4), 'outside_h': round(bb.ZLength, 4),
         'floor_z': round(bb.ZMin, 4), 'rim_z': round(bb.ZMax, 4)}
    zs = segs(s, V(0, 0, bb.ZMin - 5), V(0, 0, bb.ZMax + 5))
    hollow = bool(zs) and zs[0][1] < bb.ZMax - 1e-6
    r['z_segments'] = zs
    r['hollow'] = hollow
    ztest = (zs[0][1] + bb.ZMax) / 2.0 if hollow else (bb.ZMin + bb.ZMax) / 2.0
    xs = segs(s, V(bb.XMin - 5, 0, ztest), V(bb.XMax + 5, 0, ztest))
    ys = segs(s, V(0, bb.YMin - 5, ztest), V(0, bb.YMax + 5, ztest))
    r['x_segments'], r['y_segments'] = xs, ys
    r['inside_w'] = round(xs[1][0] - xs[0][1], 4) if len(xs) >= 2 else 0.0
    r['inside_l'] = round(ys[1][0] - ys[0][1], 4) if len(ys) >= 2 else 0.0
    r['inside_d'] = round(bb.ZMax - zs[0][1], 4) if hollow else 0.0
    r['floor_top_z'] = zs[0][1] if zs else None
    r['wall_x'] = round(xs[0][1] - xs[0][0], 4) if len(xs) >= 2 else None
    r['wall_y'] = round(ys[0][1] - ys[0][0], 4) if len(ys) >= 2 else None
    r['floor'] = round(zs[0][1] - zs[0][0], 4) if zs else None
    cyl = sorted(set(round(f.Surface.Radius, 4) for f in s.Faces if 'Cylinder' in f.Surface.TypeId))
    r['edge_radii'] = cyl
    r['n_cyl_faces'] = sum(1 for f in s.Faces if 'Cylinder' in f.Surface.TypeId)
    r['n_sphere_faces'] = sum(1 for f in s.Faces if 'Sphere' in f.Surface.TypeId)
    r['n_faces'] = len(s.Faces)
    r['thickness'] = thickness_info(d)
    r['sheet'] = sheet_info(d)
    r['exprs'] = sketch_exprs(d)
    sk = d.getObject('Sketch')
    r['sizes_typed'] = bool(sk) and not any('cup_width' in k for k, _ in sk.ExpressionEngine)
    r['states'] = {o.Name: list(o.State) for o in d.Objects if o.TypeId.startswith(('Sketcher::', 'PartDesign::'))}
    r['tip'] = b.Tip.Name if b.Tip else None
    return r


def hook_probe(d, r):
    """Q9: is the hook block (x = W/2 .. W/2 + 10 outside the wall, z 0..10) solid or hollow, one solid or two"""
    out = {}
    for b in [o for o in d.Objects if o.TypeId == 'PartDesign::Body']:
        s = b.Shape
        bb = s.BoundBox
        xh = bb.XMax - 5.0
        out[b.Name] = {'solids': len(s.Solids), 'volume': round(s.Volume, 3), 'xmax': round(bb.XMax, 4),
                       'hook_centre_inside': s.isInside(V(xh, 0, 5), 1e-6, True),
                       'hook_x_segments': segs(s, V(bb.XMax - 15, 0, 5), V(bb.XMax + 5, 0, 5))}
    r['hook'] = out
    return r


def set_cell(d, alias, val):
    d.getObject('Params').set(alias, str(val))
    d.recompute()
    for o in d.Objects:
        if o.TypeId == 'PartDesign::Thickness':
            o.touch()
    d.recompute()


def status(d):
    out = {}
    for o in d.Objects:
        if o.TypeId.startswith(('PartDesign::', 'Sketcher::')):
            st = o.getStatusString() if hasattr(o, 'getStatusString') else ''
            if list(o.State) or (st and st != 'Valid'):
                out[o.Name] = {'state': list(o.State), 'status': st}
    return out


def safe(d, extra=None):
    try:
        r = measure(d)
    except Exception as e:
        r = {'error': str(e)[:200]}
    r['status'] = status(d)
    if extra:
        r.update(extra)
    return r


def build():
    os.makedirs(OUT, exist_ok=True)
    allr = {}
    files = {'box': dict(shell=False), 'trap': dict(), 'fixed': dict(reversed_=False),
             'typed': dict(typed=(64, 44, 52))}
    for k, kw in files.items():
        d = cup_doc('cup_' + k, **kw)
        p = os.path.join(OUT, 'cup-%s.FCStd' % k)
        d.saveAs(p)
        allr[k] = dict(safe(d), file=p)
        if k == 'trap':
            allr['default_reversed'] = bool(d.getObject('Thickness').Reversed)
        FreeCAD.closeDocument(d.Name)
    # proof (Q4 headless) and comparison
    for k, cell, v, key in (('fixed', 'wall', 3, 'fixed_w3'), ('fixed', 'cup_width', 70, 'fixed_cw70'),
                            ('typed', 'wall', 3, 'typed_w3'), ('trap', 'wall', 3, 'trap_w3')):
        d = FreeCAD.openDocument(os.path.join(OUT, 'cup-%s.FCStd' % k))
        set_cell(d, cell, v)
        allr[key] = safe(d)
        FreeCAD.closeDocument(d.Name)
    # Q3 headless: Reversed = False + recompute only, then with touch()
    d = FreeCAD.openDocument(os.path.join(OUT, 'cup-trap.FCStd'))
    t = d.getObject('Thickness')
    t.Reversed = False
    d.recompute()
    allr['rev_false_recompute'] = safe(d, {'must_execute': None})
    t.touch()
    d.recompute()
    allr['rev_false_touch'] = safe(d)
    FreeCAD.closeDocument(d.Name)
    # Q3 Join Intersection on the outward file (edges square?) - recorded only
    d = cup_doc('cup_fixed_inter', reversed_=False, join='Intersection')
    allr['fixed_intersection_join'] = safe(d)
    FreeCAD.closeDocument(d.Name)
    # Q5 edge: inward wall 20 (40 - 40 = 0 across Y)
    d = FreeCAD.openDocument(os.path.join(OUT, 'cup-trap.FCStd'))
    set_cell(d, 'wall', 20)
    allr['edge_w20'] = safe(d)
    FreeCAD.closeDocument(d.Name)
    # Q7 your turn (80 wide, 40 long, 50 tall, wall 3) and the Short box (50 x 40 x 50, wall 4)
    for key, kw in (('yt_in', dict(width=80, wall=3)), ('yt_out', dict(width=80, wall=3, reversed_=False)),
                    ('short_in', dict(width=50, wall=4))):
        d = cup_doc(key, **kw)
        allr[key] = safe(d)
        FreeCAD.closeDocument(d.Name)
    # Q9 hook cases (pinned comment only)
    for key, kw in (('hook_before', dict(hook='before')), ('hook_after', dict(hook='after')),
                    ('hook_body', dict(hook='body')), ('hook_before_out', dict(hook='before', reversed_=False))):
        d = cup_doc(key, **kw)
        allr[key] = hook_probe(d, safe(d))
        FreeCAD.closeDocument(d.Name)
    json.dump(allr, open(os.path.join(OUT, 'build.json'), 'w'), indent=1)
    log('build', json.dumps({k: (v.get('inside_w'), v.get('inside_l'), v.get('inside_d'), v.get('outside_w'),
                                 v.get('edge_radii')) for k, v in allr.items() if isinstance(v, dict)}))


# ---- check mode: Claude's files (PLAN 2.5 scoring rules) ----
REF = re.compile(r'(?:Params|<<Params>>)\.([A-Za-z_][A-Za-z0-9_]*)')


def width_target(d):
    """The (b) target: the Params alias the sketch's width constraint (or the outside-width expression) depends on whose
    value is 60, found by tracing expressions; else a literal 60 inside a reached formula ('2-literal')."""
    sh = sheet_info(d) or {}
    seeds = []
    for o in d.Objects:
        if o.TypeId == 'Sketcher::SketchObject':
            for k, v in o.ExpressionEngine:
                if 'Constraints' in k:
                    seeds += [(k, a) for a in REF.findall(v)]
    reached, todo = [], [a for _, a in seeds]
    while todo:
        a = todo.pop(0)
        if a in reached or a not in sh:
            continue
        reached.append(a)
        todo += REF.findall(sh[a]['content'])
        todo += [x for x in re.findall(r'[A-Za-z_][A-Za-z0-9_]*', sh[a]['content']) if x in sh]
    cands = []
    for a in reached:
        try:
            if abs(float(str(sh[a]['value']).split()[0]) - 60) < 0.01 and not sh[a]['content'].startswith('='):
                cands.append(a)
        except ValueError:
            pass
    if 'cup_width' in cands:
        return {'kind': 'name', 'alias': 'cup_width', 'reached': reached}
    if cands:
        return {'kind': 'name', 'alias': cands[0], 'reached': reached}
    for a in reached:
        if sh[a]['content'].startswith('=') and re.search(r'(?<![0-9.])60(?![0-9.])', sh[a]['content']):
            return {'kind': '2-literal', 'alias': a, 'content': sh[a]['content'], 'reached': reached}
    return {'kind': 'none', 'reached': reached, 'seeds': seeds}


def wall_alias(d):
    t = thickness_info(d)
    if t and t['value_expr']:
        refs = REF.findall(t['value_expr'])
        if refs:
            return refs[0]
    return 'wall'


def check(doc_path, out):
    res = {'doc': doc_path}
    tmp = '/tmp/fc13-check.FCStd'
    shutil.copy(doc_path, tmp)
    d = FreeCAD.openDocument(tmp)
    res['stored'] = safe(d)                       # the shape as saved (no recompute)
    d.recompute()
    for o in d.Objects:
        if o.TypeId == 'PartDesign::Thickness':
            o.touch()
    d.recompute()
    res['recomputed'] = safe(d)
    res['objects'] = [(o.Name, o.Label, o.TypeId) for o in d.Objects][:80]
    res['width_target'] = width_target(d)
    res['wall_alias'] = wall_alias(d)
    FreeCAD.closeDocument(d.Name)
    d = FreeCAD.openDocument(tmp)
    d.recompute()
    try:
        set_cell(d, res['wall_alias'], 3)
        res['at_wall3'] = safe(d)
    except Exception as e:
        res['at_wall3'] = {'error': str(e)[:200]}
    FreeCAD.closeDocument(d.Name)
    d = FreeCAD.openDocument(tmp)
    d.recompute()
    wt = res['width_target']
    try:
        if wt['kind'] == 'name':
            set_cell(d, wt['alias'], 70)
        elif wt['kind'] == '2-literal':
            c = re.sub(r'(?<![0-9.])60(?![0-9.])', '70', wt['content'], count=1)
            d.getObject('Params').set(wt['alias'], c)
            d.recompute()
            set_cell(d, res['wall_alias'], d.getObject('Params').get(res['wall_alias']))
        res['at_width70'] = safe(d) if wt['kind'] != 'none' else {'error': 'no width name traced'}
    except Exception as e:
        res['at_width70'] = {'error': str(e)[:200]}
    FreeCAD.closeDocument(d.Name)
    json.dump(res, open(out, 'w'), indent=1)
    log('check', json.dumps({k: (res[k].get('inside_w'), res[k].get('inside_l'), res[k].get('inside_d'),
                                 res[k].get('wall_x')) for k in ('stored', 'recomputed', 'at_wall3', 'at_width70')}),
        json.dumps(wt))


if MODE == 'build':
    build()
elif MODE == 'check':
    check(os.environ['FC13_DOC'], OUT)
