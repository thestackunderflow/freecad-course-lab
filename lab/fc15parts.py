"""fc15 (FreeCAD course lesson 15, a soft rim on the hanging cup: the round has to fit in the wall), lab instrument run
by freecadcmd, never filmed. Built on lesson 14's fixed file (out/fc14/P/peg-fixed.FCStd: Pad, Thickness, Sketch001,
Pad001, Tip Pad001) with lab/fc14parts.py's readers.

    FC15_OUT=/lab/out/fc15/P FC15_MODE=build freecadcmd /lab/lab/fc15parts.py
        rim-start (+ Params rim_out 3, rim_in 1, no rounds), rim-trap (Fillet =Params.rim_out on ONE outer rim edge, r 3),
        rim-ok (r 1.5), rim-both (+ Fillet001 =Params.rim_in on the four inner rim edges), G0 Q2-Q8 by code -> build.json
    FC15_DOC=x.FCStd FC15_OUT=y.json FC15_MODE=check freecadcmd /lab/lab/fc15parts.py
        a saved file (Claude's): stored, recomputed, at wall 2, 3 and 1.6 (PLAN 2.5 score, lab/fc15score.py).
Rim (PLAN 2.1): the flat ring at z 50, inner loop x +-30 / y +-20 (4 lines, sharp corners), outer loop x +-32 / y +-22
(4 lines + 4 arcs of radius `wall`, from the Thickness's Arc join)."""
import json
import math
import os
import shutil
import sys

os.environ['FC14_MODE'] = 'lib'
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fc14parts.py')).read())   # noqa: S102 (readers)

OUT = os.environ.get('FC15_OUT', '/lab/out/fc15/P')
MODE15 = os.environ.get('FC15_MODE', 'build')
START = '/lab/out/fc14/P/peg-fixed.FCStd'
EPS = 1e-4


def log15(*a):
    print('FC15', *a)
    sys.stdout.flush()


def add_rim_params(d, rim_out=3, rim_in=1):
    s = d.getObject('Params')
    for row, (n, v) in ((7, ('rim_out', rim_out)), (8, ('rim_in', rim_in))):
        s.set('A%d' % row, n)
        s.set('B%d' % row, str(v))
        s.setAlias('B%d' % row, n)
    d.recompute()


def rim_edges(shape, z=50.0):
    """(outer, inner) edge names on the rim plane: outer = touches |x| > 30 + EPS or |y| > 20 + EPS"""
    outer, inner = [], []
    for i, e in enumerate(shape.Edges, 1):
        if not all(abs(v.Point.z - z) < 1e-6 for v in e.Vertexes) or abs(e.BoundBox.ZMax - z) > 1e-6:
            continue
        far = any(abs(v.Point.x) > 30 + EPS or abs(v.Point.y) > 20 + EPS for v in e.Vertexes)
        (outer if far else inner).append(('Edge%d' % i, e.Curve.__class__.__name__,
                                          [round(c, 3) for c in e.CenterOfMass]))
    return outer, inner


def pick_outer_click(shape):
    """the one edge a viewer clicks: the outer line on +x (x 32)"""
    outer, _ = rim_edges(shape)
    for n, kind, c in outer:
        if kind == 'Line' and c[0] > 31:
            return n
    return outer[0][0]


def rim_face(shape, z=50.0):
    for i, f in enumerate(shape.Faces, 1):
        if 'Plane' in f.Surface.TypeId and abs(f.BoundBox.ZMin - z) < 1e-6 and abs(f.BoundBox.ZMax - z) < 1e-6:
            return 'Face%d' % i
    return None


def tip(d):
    return main_body(d).Tip


def add_fillet(d, name, base, subs, expr=None, radius=None):
    b = main_body(d)
    f = b.newObject('PartDesign::Fillet', name)
    f.Base = (base, subs)
    if expr:
        f.setExpression('Radius', expr)
    elif radius is not None:
        f.Radius = radius
    d.recompute()
    return f


def feat_state(d):
    out = {}
    for o in main_body(d).Group:
        if o.TypeId.startswith('PartDesign::') and list(o.State):
            st = list(o.State)
            msg = ''
            try:
                msg = o.getStatusString()
            except Exception:
                pass
            out[o.Name] = [st, msg]
    return out


def builds(d):
    b = main_body(d)
    s = b.Shape
    bad = {k: v for k, v in feat_state(d).items() if any(x in ('Invalid', 'Error') for x in v[0])}
    feats = [o for o in b.Group if o.TypeId.startswith('PartDesign::') and o.TypeId != 'PartDesign::Body'
             and 'Origin' not in o.TypeId and o.TypeId not in ('PartDesign::Plane', 'PartDesign::Line', 'PartDesign::Point')]
    last = feats[-1].Name if feats else None
    ok = (not bad and b.Tip is not None and b.Tip.Name == last and not s.isNull() and s.isValid()
          and len(s.Solids) == 1)
    return ok, {'bad': bad, 'tip': b.Tip.Name if b.Tip else None, 'last': last,
                'valid': (not s.isNull()) and s.isValid(), 'solids': 0 if s.isNull() else len(s.Solids)}


def rim_read(d, shape=None):
    """rim at y 0, +x side: leftover flat, the round faces (cylinders touching z 50), point tests from read radii"""
    s = shape if shape is not None else main_body(d).Shape
    w = param(d, 'wall') or 2.0
    r = {'volume': round(s.Volume, 3), 'faces': len(s.Faces), 'solids': len(s.Solids), 'wall': w,
         'rim_out_param': param(d, 'rim_out'), 'rim_in_param': param(d, 'rim_in')}
    flat = []
    for f in s.Faces:
        if 'Plane' in f.Surface.TypeId and abs(f.BoundBox.ZMax - 50) < 1e-6 and abs(f.BoundBox.ZMin - 50) < 1e-6:
            line = Part.LineSegment(V(25, 0, 50), V(40, 0, 50)).toShape()
            for e in f.common(line).Edges:
                xs = sorted(v.Point.x for v in e.Vertexes)
                flat.append((round(xs[0], 4), round(xs[-1], 4)))
    r['flat_segs'] = flat
    r['flat'] = round(sum(b - a for a, b in flat), 4) if flat else 0.0
    rounds = {'out': [], 'in': []}
    for f in s.Faces:
        tid = f.Surface.TypeId
        if 'Cylinder' not in tid or f.BoundBox.ZMax < 50 - 1e-6 or f.BoundBox.ZMin < 40:
            continue
        ax = f.Surface.Axis
        if abs(ax.z) > 1e-6:
            continue   # vertical cylinders = the Thickness's outer corners
        c = f.Surface.Center
        rad = round(f.Surface.Radius, 4)
        # axis along y on the x sides, along x on the y sides; centre inside the wall = 30 + r (in) or 30 + w - r (out)
        off = abs(c.x) if abs(ax.y) > 0.5 else abs(c.y) + 10
        cm = f.CenterOfMass
        offm = abs(cm.x) if abs(ax.y) > 0.5 else abs(cm.y) + 10
        fits = abs(off - (30 + w - rad)) < 1e-3 or abs(off - (30 + rad)) < 1e-3
        side = ('in' if offm < 30 + w / 2.0 else 'out') if fits else '?'
        rounds.setdefault(side, []).append(rad)
    r['round_radii'] = {k: sorted(set(v)) for k, v in rounds.items()}
    r['round_faces'] = {k: len(v) for k, v in rounds.items()}
    r['torus_faces'] = sum(1 for f in s.Faces if 'Toroid' in f.Surface.TypeId)
    inside = lambda x, y, z: s.isInside(V(x, y, z), 1e-6, True)
    pts = {'corner_pt_31.95': inside(30 + w - 0.05, 0, 49.95)}
    ro = r['round_radii']['out'][0] if r['round_radii']['out'] else None
    ri = r['round_radii']['in'][0] if r['round_radii']['in'] else None
    if ro:   # 1.2 r out from the round's centre at 45 deg: air if rounded (distance 1.13 r > r)
        cx, cz = 30 + w - ro, 50 - ro
        k = ro * 0.8
        pts['out_air_+x'] = not inside(cx + k, 0, cz + k)
        pts['out_air_-x'] = not inside(-(cx + k), 0, cz + k)
        pts['out_air_+y'] = not inside(0, cx - 10 + k, cz + k)
        pts['out_air_-y'] = not inside(0, -(cx - 10 + k), cz + k)
        d45 = (w - ro + k) / math.sqrt(2)   # through the plan-view corner arc (centre (30, 20)), at 45 deg
        pts['out_air_corner'] = not inside(30 + (w - ro) / math.sqrt(2) + k / math.sqrt(2), 20 + (w - ro) / math.sqrt(2)
                                           + k / math.sqrt(2), cz + k)
    if ri:
        cx, cz = 30 + ri, 50 - ri
        k = ri * 0.8
        pts['in_air_+x'] = not inside(cx - k, 0, cz + k)
        pts['in_air_-y'] = not inside(0, -(20 + ri - k), cz + k)
    r['points'] = pts
    sx = segs(s, V(-80, 0, 25), V(80, 0, 25))
    r['outside_w'] = round(sx[-1][1] - sx[0][0], 4) if sx else None
    r['inside_w'] = round(sx[1][0] - sx[0][1], 4) if len(sx) >= 2 else None
    m = measure(d, s)
    for k in ('inside_l', 'inside_d', 'peg_w', 'peg_h', 'peg_mid_solid', 'faces'):
        r['m_' + k] = m.get(k)
    return r


def snap(d, extra=None):
    ok, info = builds(d)
    r = {'builds': ok, 'build_info': info, 'state': feat_state(d)}
    try:
        r['rim'] = rim_read(d)
    except Exception as e:
        r['rim'] = {'error': str(e)[:300]}
    if extra:
        r.update(extra)
    return r


def start_doc(name):
    tmp = '/tmp/%s.FCStd' % name
    shutil.copy(START, tmp)
    d = FreeCAD.openDocument(tmp)
    d.recompute()
    add_rim_params(d)
    d.recompute()
    return d


def save(d, name):
    p = os.path.join(OUT, name + '.FCStd')
    d.saveAs(p)
    return p


def try_out(rout, rin, wall=2.0, outer='click', reopen=None):
    """a fresh rim-start with Fillet (rout, None = none) and Fillet001 (rin) at `wall`: (builds, rim read)"""
    d = start_doc('t%d' % int(1e6 * (rout or 0) + 1e3 * (rin or 0)))
    set_cell(d, 'wall', wall)
    base = tip(d)
    if rout:
        set_cell(d, 'rim_out', rout)
        subs = [pick_outer_click(base.Shape)] if outer == 'click' else [x[0] for x in rim_edges(base.Shape)[0]]
        add_fillet(d, 'Fillet', base, subs, 'Params.rim_out')
        base = tip(d)
    if rin:
        set_cell(d, 'rim_in', rin)
        add_fillet(d, 'Fillet001', tip(d) if not rout else d.getObject('Fillet'),
                   [x[0] for x in rim_edges(main_body(d).Shape)[1]], 'Params.rim_in')
    touch_all(d)
    r = snap(d)
    FreeCAD.closeDocument(d.Name)
    return r


def largest(fn, lo=0.05, hi=3.0, step=0.05):
    best, last = None, None
    v = lo
    while v <= hi + 1e-9:
        r = fn(round(v, 2))
        if r['builds'] and r['rim'].get('round_faces', {}) and (r['rim']['round_faces'].get('out') or
                                                               r['rim']['round_faces'].get('in')):
            best = round(v, 2)
        elif best is not None:
            last = round(v, 2)
            break
        v += step
    return {'largest_builds': best, 'first_fails': last}


def build():
    os.makedirs(OUT, exist_ok=True)
    res = {'start_file': START}
    # Q1 rim-start
    d = start_doc('rim-start')
    s = tip(d).Shape
    outer, inner = rim_edges(s)
    res['q1'] = {'tree': tree(d), 'outer_edges': outer, 'inner_edges': inner, 'rim_face': rim_face(s),
                 'snap': snap(d), 'params': {k: param(d, k) for k in ('wall', 'rim_out', 'rim_in', 'peg_size')}}
    save(d, 'rim-start')
    start_vol, start_faces = res['q1']['snap']['rim']['volume'], res['q1']['snap']['rim']['faces']
    # Q2 trap: one click on the outer edge, =Params.rim_out (3)
    click = pick_outer_click(s)
    f = add_fillet(d, 'Fillet', tip(d), [click], 'Params.rim_out')
    sn = snap(d, {'edge': click})
    rm = sn['rim']
    sn['unchanged_vs_start'] = (abs(rm['volume'] - start_vol) <= 0.01 and rm['faces'] == start_faces)
    sn['fillet_shape_null'] = f.Shape.isNull()
    res['q2_trap_r3'] = sn
    save(d, 'rim-trap')
    # fix: rim_out 1.5
    set_cell(d, 'rim_out', 1.5)
    res['fix_r1_5'] = snap(d)
    save(d, 'rim-ok')
    # the second edge: Fillet001 =Params.rim_in on the four inner edges, at 1
    inner_now = [x[0] for x in rim_edges(main_body(d).Shape)[1]]
    f2 = add_fillet(d, 'Fillet001', d.getObject('Fillet'), inner_now, 'Params.rim_in')
    touch_all(d)
    res['second_edge_1'] = snap(d, {'edges': inner_now})
    save(d, 'rim-both')
    FreeCAD.closeDocument(d.Name)
    # Q4 proof: rim-both opened again, wall 3, 2, 2.6, 2.4, 3 -> 2 -> 3
    d = FreeCAD.openDocument(os.path.join(OUT, 'rim-both.FCStd'))
    d.recompute()
    res['q4_reopen'] = snap(d)
    seq = {}
    for w in (3, 2, 2.6, 2.4, 3):
        set_cell(d, 'wall', w)
        seq['wall_%s_%d' % (w, len(seq))] = snap(d)
    res['q4_walls'] = seq
    set_cell(d, 'wall', 3)
    save(d, 'rim-both-w3')
    FreeCAD.closeDocument(d.Name)
    # Q3 limits by code, 0.05 steps
    q3 = {}
    q3['out_alone'] = largest(lambda v: try_out(v, None))
    q3['in_alone'] = largest(lambda v: try_out(None, v))
    q3['equal_pair'] = largest(lambda v: try_out(v, v), hi=1.5)
    for k, a, b in (('out_2.00', 2.0, None), ('in_2.00', None, 2.0), ('out1.5_in0.5', 1.5, 0.5),
                    ('out0.5_in1.5', 0.5, 1.5), ('out1_in1', 1.0, 1.0), ('out1.5_in0.45', 1.5, 0.45),
                    ('out1.95', 1.95, None), ('in1.95', None, 1.95)):
        r = try_out(a, b)
        q3[k] = {'builds': r['builds'], 'flat': r['rim'].get('flat'), 'radii': r['rim'].get('round_radii'),
                 'state': r['state']}
    res['q3'] = q3
    # Q5 rim face picked (both loops, one radius)
    q5 = {}
    for w, rr in ((2, 1.5), (2, 1.0), (2, 0.8), (3, 1.5)):
        d = start_doc('face%d%d' % (w, int(rr * 10)))
        set_cell(d, 'wall', w)
        fc = rim_face(tip(d).Shape)
        f = add_fillet(d, 'Fillet', tip(d), [fc], radius=rr)
        f.Radius = rr
        d.recompute()
        q5['wall%s_r%s' % (w, rr)] = snap(d, {'face': fc, 'edges_listed': len(f.Base[1])})
        FreeCAD.closeDocument(d.Name)
    res['q5'] = q5
    # Q7 round before the shell: box Pad, Fillet r 3 on its top edges, Thickness outward on the top face, then the peg
    d = FreeCAD.newDocument('beforeshell')
    sp = d.addObject('Spreadsheet::Sheet', 'Params')
    for i, (n, v) in enumerate(PARAMS, 1):
        sp.set('A%d' % i, n)
        sp.set('B%d' % i, str(v))
        sp.setAlias('B%d' % i, n)
    d.recompute()
    b = d.addObject('PartDesign::Body', 'Body')
    sk = box_sketch(b)
    pad = b.newObject('PartDesign::Pad', 'Pad')
    pad.Profile = sk
    pad.setExpression('Length', 'Params.cup_height')
    d.recompute()
    tops = ['Edge%d' % i for i, e in enumerate(pad.Shape.Edges, 1)
            if all(abs(v.Point.z - 50) < 1e-6 for v in e.Vertexes)]
    fb = b.newObject('PartDesign::Fillet', 'Fillet')
    fb.Base = (pad, tops)
    fb.Radius = 3
    d.recompute()
    t = add_thickness(d, b, fb, False)
    add_peg(d, b, 10)
    d.recompute()
    q7 = snap(d, {'thickness_base': [t.Base[0].Name, list(t.Base[1])]})
    sh = main_body(d).Shape
    q7['top_z_at_x31'] = segs(sh, V(31, 0, 40), V(31, 0, 60))
    q7['outer_top_at_y0'] = segs(sh, V(0, 0, 51.5), V(40, 0, 51.5))
    q7['rim_line_z49'] = segs(sh, V(0, 0, 49), V(40, 0, 49))
    res['q7'] = q7
    d.saveAs(os.path.join(OUT, 'round-before-shell.FCStd'))
    FreeCAD.closeDocument(d.Name)
    # Q8 your turns
    res['q8'] = {}
    for k, w, a, b2 in (('long_1.2_1.5_w2.5', 2.5, 1.2, 1.5), ('long_1.2_1.2_w2.5', 2.5, 1.2, 1.2),
                        ('short_0.8_1_w2', 2, 0.8, 1.0)):
        r = try_out(a, b2, wall=w)
        res['q8'][k] = {'builds': r['builds'], 'flat': r['rim'].get('flat'), 'radii': r['rim'].get('round_radii'),
                        'state': r['state']}
    # Q3 extra: the outer edge as all 8 segments (vs one click) at 1.5
    r = try_out(1.5, None, outer='all')
    res['q2_all8_r1_5'] = {'builds': r['builds'], 'faces': r['rim'].get('faces'), 'volume': r['rim'].get('volume'),
                           'points': r['rim'].get('points')}
    json.dump(res, open(os.path.join(OUT, 'build.json'), 'w'), indent=1, default=str)
    log15('built', json.dumps({'q2': [res['q2_trap_r3']['builds'], res['q2_trap_r3']['unchanged_vs_start'],
                                      res['q2_trap_r3']['state']],
                               'fix': [res['fix_r1_5']['builds'], res['fix_r1_5']['rim'].get('flat')],
                               'second': [res['second_edge_1']['builds'], res['second_edge_1']['state']]}, default=str))


def check(doc_path, out):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from fc15score import passes
    res = {'doc': doc_path}
    tmp = '/tmp/fc15-check.FCStd'
    shutil.copy(doc_path, tmp)
    d = FreeCAD.openDocument(tmp)
    res['stored'] = snap(d)
    d.recompute()
    res['recomputed'] = snap(d)
    res['tree'] = tree(d)
    res['objects'] = [(o.Name, o.Label, o.TypeId) for o in d.Objects][:80]
    res['fillets'] = []
    for o in d.Objects:
        if o.TypeId in ('PartDesign::Fillet', 'PartDesign::Chamfer', 'Part::Fillet'):
            ex = dict((k.lstrip('.'), v) for k, v in o.ExpressionEngine)
            res['fillets'].append({'name': o.Name, 'type': o.TypeId,
                                   'radius': round(o.Radius.Value, 4) if hasattr(o, 'Radius') else None,
                                   'expr': ex.get('Radius'),
                                   'base': [o.Base[0].Name, list(o.Base[1])] if getattr(o, 'Base', None) else None})
    res['params'] = {}
    sp = d.getObject('Params')
    if sp:
        for c in sp.getUsedCells():
            try:
                res['params'][c] = [sp.getAlias(c), str(sp.get(c))]
            except Exception:
                pass
    FreeCAD.closeDocument(d.Name)
    for w in (2, 3, 1.6):
        d = FreeCAD.openDocument(tmp)
        d.recompute()
        try:
            set_cell(d, 'wall', w)
            res['at_wall%s' % w] = snap(d)
            res['at_wall%s' % w]['m'] = measure(d)
        except Exception as e:
            res['at_wall%s' % w] = {'error': str(e)[:300]}
        FreeCAD.closeDocument(d.Name)
    ok, detail = passes({w: res['at_wall%s' % w] for w in (2, 3, 1.6)})
    res['pass'] = ok
    res['criteria'] = detail
    json.dump(res, open(out, 'w'), indent=1, default=str)
    log15('check', json.dumps({w: (res['at_wall%s' % w].get('builds'),
                                   (res['at_wall%s' % w].get('rim') or {}).get('round_radii'),
                                   (res['at_wall%s' % w].get('rim') or {}).get('flat')) for w in (2, 3, 1.6)}),
          'PASS' if ok else 'FAIL')


if MODE15 == 'build':
    build()
elif MODE15 == 'check':
    check(os.environ['FC15_DOC'], OUT)
