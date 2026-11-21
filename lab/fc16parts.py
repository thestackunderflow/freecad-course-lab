"""fc16 (FreeCAD course lesson 16, a hanging hole in the wall cup's back wall: Pocket depth vs the Thickness wall), lab
instrument run by freecadcmd, never filmed. Built on lesson 14's fixed cup (out/fc14/P/peg-fixed.FCStd: Pad, Thickness
outward =Params.wall, Sketch001, Pad001 peg, Tip Pad001): G0 Q9 branch, lesson 15's rim-both (Fillet rim_out 1.5 +
Fillet001 rim_in 1) does not build at wall 2 (logged as q9_lesson15_rim_both) with the readers
of lab/fc14parts.py + lab/fc15parts.py.

    FC16_OUT=/lab/out/fc16/P FC16_MODE=build freecadcmd /lab/lab/fc16parts.py
        hole-start (+ Params hole_size 5), hole-typed (HoleSketch on the back outside face, circle =Params.hole_size at
        x 0 z 30, Pocket Length 2), hole-through (Type ThroughAll), hole-fixed (Length =Params.wall), G0 Q1-Q11 -> build.json
    FC16_DOC=x.FCStd FC16_OUT=y.json FC16_MODE=check freecadcmd /lab/lab/fc16parts.py
        a saved file (Claude's): stored, recomputed, at wall 2, 3 and 12 (PLAN 2.5 score, lab/fc16score.py)."""
import json
import os
import shutil
import sys

os.environ['FC15_MODE'] = 'lib'
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fc15parts.py')).read())   # noqa: S102 (readers)
import Sketcher  # noqa: E402

OUT = os.environ.get('FC16_OUT', '/lab/out/fc16/P')
MODE16 = os.environ.get('FC16_MODE', 'build')
START = '/lab/out/fc14/P/peg-fixed.FCStd'   # G0 Q9 branch: lesson 15's rim-both fails at wall 2
L15 = '/lab/out/fc15/P/rim-both.FCStd'


def log16(*a):
    print('FC16', *a)
    sys.stdout.flush()


def add_hole_param(d, v=5):
    s = d.getObject('Params')
    s.set('A7', 'hole_size')
    s.set('B7', str(v))
    s.setAlias('B7', 'hole_size')
    d.recompute()


def back_face(shape, w):
    """the back outside face: planar, normal +y, at y 20 + wall, holding (0, 20 + wall, 30)"""
    for i, f in enumerate(shape.Faces, 1):
        if 'Plane' not in f.Surface.TypeId:
            continue
        bb = f.BoundBox
        if abs(bb.YMin - (20 + w)) < 1e-6 and abs(bb.YMax - (20 + w)) < 1e-6 and f.isInside(V(0, 20 + w, 30), 1e-6, True):
            return 'Face%d' % i
    return None


def inside_back_face(shape):
    for i, f in enumerate(shape.Faces, 1):
        bb = f.BoundBox
        if 'Plane' in f.Surface.TypeId and abs(bb.YMin - 20) < 1e-6 and abs(bb.YMax - 20) < 1e-6 and bb.ZMax > 40:
            return 'Face%d' % i
    return None


def add_hole(d, kind='Length', length=2.0, expr=None):
    """HoleSketch on the back outside face of the Tip, circle =Params.hole_size at x 0 z 30, then a Pocket"""
    b = main_body(d)
    base = b.Tip
    w = param(d, 'wall')
    face = back_face(base.Shape, w)
    sk = b.newObject('Sketcher::SketchObject', 'HoleSketch')
    sk.AttachmentSupport = [(base, face)]
    sk.MapMode = 'FlatFace'
    d.recompute()
    loc = sk.Placement.inverse().multVec(V(0, 20 + w, 30))
    sk.addGeometry(Part.Circle(V(loc.x, loc.y, 0), V(0, 0, 1), 2.5), False)
    sk.addConstraint(Sketcher.Constraint('Diameter', 0, 5.0))
    sk.setExpression('Constraints[0]', 'Params.hole_size')
    sk.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, 0, 3, loc.x))
    sk.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, 0, 3, loc.y))
    d.recompute()
    p = b.newObject('PartDesign::Pocket', 'Pocket')
    p.Profile = sk
    set_depth(d, p, kind, length, expr)
    return sk, p, face


def set_depth(d, p, kind, length=2.0, expr=None, upto=None):
    p.setExpression('Length', None)
    p.Type = kind
    if kind == 'Length':
        if expr:
            p.setExpression('Length', expr)
        else:
            p.Length = length
    if kind == 'UpToFace':
        base = p.BaseFeature
        p.UpToFace = (base, [inside_back_face(base.Shape)])
    d.recompute()
    touch_all(d)


def depth_info(d):
    out = []
    for o in main_body(d).Group if main_body(d) else []:
        if o.TypeId in ('PartDesign::Pocket', 'PartDesign::Hole', 'PartDesign::Pad'):
            ex = dict((k.lstrip('.'), v) for k, v in o.ExpressionEngine)
            r = {'name': o.Name, 'kind': o.TypeId.split('::')[1], 'type': str(getattr(o, 'Type', getattr(o, 'DepthType', ''))),
                 'length': round(o.Length.Value, 4) if hasattr(o, 'Length') else round(o.Depth.Value, 4),
                 'expr': ex.get('Length') or ex.get('Depth'), 'reversed': bool(getattr(o, 'Reversed', False)),
                 'midplane': bool(getattr(o, 'Midplane', False))}
            if getattr(o, 'UpToFace', None):
                r['uptoface'] = [o.UpToFace[0].Name, list(o.UpToFace[1])]
            prof = getattr(o, 'Profile', None)
            if prof and prof[0]:
                r['profile'] = prof[0].Name
                sup = getattr(prof[0], 'AttachmentSupport', None)
                r['support'] = [(s[0].Name, list(s[1])) for s in sup] if sup else None
            out.append(r)
    return out


def sketch_centre(d, name='HoleSketch'):
    sk = d.getObject(name)
    for g in sk.Geometry:
        if g.__class__.__name__ == 'Circle':
            c = sk.Placement.multVec(g.Center)
            return [round(c.x, 4), round(c.y, 4), round(c.z, 4)]
    return None


def hole_read(d, shape=None):
    s = shape if shape is not None else main_body(d).Shape
    w = param(d, 'wall') or 2.0
    ins = lambda x, y, z: s.isInside(V(x, y, z), 1e-6, True)
    r = {'wall': w, 'volume': round(s.Volume, 3), 'solids': len(s.Solids), 'valid': s.isValid()}
    r['axis_air'] = {'y20.05': not ins(0, 20.05, 30), 'ymid': not ins(0, 20 + w / 2.0, 30),
                     'yout-0.05': not ins(0, 20 + w - 0.05, 30)}
    ay = [(a, b) for a, b in segs(s, V(0, 0, 30), V(0, 20 + w + 5, 30))]
    r['axis_segs'] = ay
    r['skin'] = round(sum(max(0.0, min(b, 20 + w) - max(a, 20)) for a, b in ay), 4)
    r['skin_mid_solid'] = ins(0, 20.5, 30) if w >= 2.5 else None
    r['pit_floor_y'] = ay[-1][1] if ay else None
    r['pit_depth'] = round(20 + w - ay[-1][1], 4) if ay else round(w, 4)
    ym = 20 + w / 2.0
    bx = segs(s, V(-40, ym, 30), V(40, ym, 30))
    r['back_hole_w'] = next((round(bx[i + 1][0] - bx[i][1], 4) for i in range(len(bx) - 1) if bx[i][1] < 0 < bx[i + 1][0]), 0.0)
    r['dia_ok'] = (not ins(2.4, ym, 30)) and (not ins(-2.4, ym, 30)) and ins(2.6, ym, 30) and ins(-2.6, ym, 30)
    yf = -20 - w / 2.0
    fx = segs(s, V(-40, yf, 30), V(40, yf, 30))
    r['front_solid'] = ins(0, yf, 30)
    r['front_hole_w'] = next((round(fx[i + 1][0] - fx[i][1], 4) for i in range(len(fx) - 1) if fx[i][1] < 0 < fx[i + 1][0]), 0.0)
    r['peg_solid'] = ins(0, -34, 40) and ins(0, -28, 40)
    sx = segs(s, V(-80, 0, 25), V(80, 0, 25))
    sy = segs(s, V(0, -80, 25), V(0, 80, 25))
    r['outside_w'] = round(sx[-1][1] - sx[0][0], 4) if sx else None
    r['inside_w'] = round(sx[1][0] - sx[0][1], 4) if len(sx) >= 2 else None
    r['outside_l'] = round(sy[-1][1] - sy[0][0], 4) if sy else None
    r['inside_l'] = round(sy[1][0] - sy[0][1], 4) if len(sy) >= 2 else None
    sz = segs(s, V(0, 0, -30), V(0, 0, 90))
    r['inside_d'] = round(s.BoundBox.ZMax - sz[0][1], 4) if sz else None
    r['top_open'] = not ins(0, 0, 49.9) and not ins(0, 0, 50 + w / 2.0)
    return r


def snap(d, extra=None):
    ok, info = builds(d)
    r = {'builds': ok, 'build_info': info, 'state': feat_state(d), 'wall': param(d, 'wall'), 'depth': None}
    try:
        r['hole'] = hole_read(d)
    except Exception as e:
        r['hole'] = {'error': str(e)[:300]}
    di = [x for x in depth_info(d) if x['kind'] in ('Pocket', 'Hole')]
    r['depths'] = di
    if di:
        x = di[-1]
        r['depth'] = {'type': x['type'], 'expr': x['expr'], 'length': x['length']}
        if x['type'] == 'UpToFace' and x.get('uptoface'):
            r['depth']['face_y'] = None
    if extra:
        r.update(extra)
    return r


def start16(name):
    tmp = '/tmp/%s.FCStd' % name
    shutil.copy(START, tmp)
    d = FreeCAD.openDocument(tmp)
    d.recompute()
    add_hole_param(d)
    return d


def save16(d, name):
    p = os.path.join(OUT, name + '.FCStd')
    d.saveAs(p)
    return p


def at_walls(path, walls, extra_fn=None):
    out = {}
    for w in walls:
        d = FreeCAD.openDocument(path)
        d.recompute()
        set_cell(d, 'wall', w)
        out[str(w)] = snap(d, extra_fn(d) if extra_fn else None)
        FreeCAD.closeDocument(d.Name)
    return out


def scratch(name, kind='Length', length=2.0, expr=None, wall=2.0):
    d = start16(name)
    set_cell(d, 'wall', wall)
    add_hole(d, kind, length, expr)
    return d


def build():
    os.makedirs(OUT, exist_ok=True)
    res = {'start_file': START}
    d = start16('hole-start')
    res['pocket_types'] = None
    res['start'] = snap(d, {'tree': tree(d), 'params': {k: param(d, k) for k in
                                                         ('wall', 'peg_size', 'hole_size')}})
    p0 = save16(d, 'hole-start')
    FreeCAD.closeDocument(d.Name)
    res['q9'] = {k: {'builds': v['builds'], 'state': v['state'], 'outside_w': v['hole'].get('outside_w')}
                 for k, v in at_walls(p0, (2, 3, 4, 12)).items()}
    shutil.copy(L15, '/tmp/l15.FCStd')
    res['q9_lesson15_rim_both'] = {k: {'builds': v['builds'], 'state': v['state']}
                                   for k, v in at_walls('/tmp/l15.FCStd', (2, 3, 4, 12)).items()}
    # typed 2 (Q1)
    d = FreeCAD.openDocument(p0)
    sk, pk, face = add_hole(d, 'Length', 2.0)
    res['pocket_types'] = list(pk.getEnumerationsOfProperty('Type'))
    res['q1_typed_w2'] = snap(d, {'face': face, 'support': [(s[0].Name, list(s[1])) for s in sk.AttachmentSupport],
                                  'map_mode': sk.MapMode, 'reversed': pk.Reversed, 'centre': sketch_centre(d),
                                  'sketch_normal': [round(c, 4) for c in sk.Placement.Rotation.multVec(V(0, 0, 1))]})
    pt = save16(d, 'hole-typed')
    FreeCAD.closeDocument(d.Name)
    cen = lambda d: {'centre': sketch_centre(d), 'support': [(s[0].Name, list(s[1]))
                                                             for s in d.getObject('HoleSketch').AttachmentSupport]}
    q2 = at_walls(pt, (2, 3, 4), cen)
    res['q2'] = {k: {'centre': v['centre'], 'support': v['support'], 'builds': v['builds']} for k, v in q2.items()}
    res['q3_typed_w3'] = q2['3']
    res['q6_typed_w4'] = q2['4']
    # Through all (Q4)
    d = FreeCAD.openDocument(pt)
    set_depth(d, d.getObject('Pocket'), 'ThroughAll')
    res['through_w2'] = snap(d)
    ph = save16(d, 'hole-through')
    FreeCAD.closeDocument(d.Name)
    res['q4_through_w3'] = at_walls(ph, (3,))['3']
    # fix (Q5)
    d = FreeCAD.openDocument(pt)
    set_depth(d, d.getObject('Pocket'), 'Length', expr='Params.wall')
    pf = save16(d, 'hole-fixed')
    ex = dict((k.lstrip('.'), v) for k, v in d.getObject('Pocket').ExpressionEngine).get('Length')
    FreeCAD.closeDocument(d.Name)
    q5 = at_walls(pf, (2, 3))
    q5['expr'] = ex
    res['q5'] = q5
    # proof (Q6): opened again, wall 4, then hole_size 6
    d = FreeCAD.openDocument(pf)
    d.recompute()
    q6 = {'reopen_w2': snap(d)}
    set_cell(d, 'wall', 4)
    q6['reopen_w4'] = snap(d)
    set_cell(d, 'hole_size', 6)
    q6['hole6'] = snap(d)
    FreeCAD.closeDocument(d.Name)
    q6['typed_w4'] = res['q6_typed_w4']
    res['q6'] = q6
    # second ways (Q7)
    q7 = {}
    for kind in ('UpToFirst', 'UpToFace'):
        d = FreeCAD.openDocument(pt)
        set_depth(d, d.getObject('Pocket'), kind)
        tmp = '/tmp/q7-%s.FCStd' % kind
        d.saveAs(tmp)
        FreeCAD.closeDocument(d.Name)
        q7[kind] = {k: {'builds': v['builds'], 'state': v['state'], 'axis_air': v['hole'].get('axis_air'),
                        'front_solid': v['hole'].get('front_solid'), 'skin': v['hole'].get('skin'),
                        'depths': v['depths']} for k, v in at_walls(tmp, (2, 3, 4)).items()}
    res['q7'] = q7
    # Hole tool (Q10): defaults, then Dimension 2 + angled point at wall 3
    d = FreeCAD.openDocument(p0)
    set_cell(d, 'wall', 3)
    b = main_body(d)
    w = 3.0
    sk = b.newObject('Sketcher::SketchObject', 'HoleSketch')
    sk.AttachmentSupport = [(b.Tip, back_face(b.Tip.Shape, w))]
    sk.MapMode = 'FlatFace'
    d.recompute()
    loc = sk.Placement.inverse().multVec(V(0, 20 + w, 30))
    sk.addGeometry(Part.Circle(V(loc.x, loc.y, 0), V(0, 0, 1), 2.5), False)
    d.recompute()
    h = b.newObject('PartDesign::Hole', 'Hole')
    h.Profile = sk
    d.recompute()
    q10 = {'defaults': {p: str(getattr(h, p, None)) for p in ('DepthType', 'Depth', 'DrillPoint', 'DrillPointAngle',
                                                              'Diameter', 'DrillForDepth', 'Threaded')},
           'depth_types': list(h.getEnumerationsOfProperty('DepthType')),
           'drill_points': list(h.getEnumerationsOfProperty('DrillPoint'))}
    h.Diameter = 5
    h.DepthType = 'Dimension'
    h.Depth = 2
    for dp in ('Flat', 'Angled'):
        h.DrillPoint = dp
        if dp == 'Angled':
            h.DrillPointAngle = 118
        d.recompute()
        touch_all(d)
        s = snap(d)
        hr = s['hole']
        rad = segs(b.Shape, V(-5, 20.0 + 0.01, 30), V(5, 20.0 + 0.01, 30))
        q10['typed2_%s_w3' % dp] = {'builds': s['builds'], 'axis_air': hr.get('axis_air'), 'axis_segs': hr.get('axis_segs'),
                                    'skin': hr.get('skin'), 'inside_face_segs_x': rad, 'front_solid': hr.get('front_solid')}
    FreeCAD.closeDocument(d.Name)
    res['q10'] = q10
    # your turns (Q11)
    d = scratch('yt1', 'Length', 2.5, wall=2.5)
    q11 = {'long_2.5_w2.5': snap(d)}
    set_cell(d, 'wall', 6)
    q11['long_2.5_w6'] = snap(d)
    FreeCAD.closeDocument(d.Name)
    q11['short_2_w4'] = res['q6_typed_w4']
    res['q11'] = q11
    json.dump(res, open(os.path.join(OUT, 'build.json'), 'w'), indent=1, default=str)
    hs = lambda k: (res[k]['builds'], res[k]['hole'].get('skin'), res[k]['hole'].get('front_solid'))
    log16('built', json.dumps({'q1': hs('q1_typed_w2'), 'q3': hs('q3_typed_w3'), 'q4': hs('q4_through_w3'),
                               'q2': {k: v['centre'] for k, v in res['q2'].items()}}, default=str))


def check(doc_path, out):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from fc16score import passes
    res = {'doc': doc_path}
    tmp = '/tmp/fc16-check.FCStd'
    shutil.copy(doc_path, tmp)
    d = FreeCAD.openDocument(tmp)
    res['stored'] = snap(d)
    d.recompute()
    res['recomputed'] = snap(d)
    res['tree'] = tree(d)
    res['objects'] = [(o.Name, o.Label, o.TypeId) for o in d.Objects][:80]
    res['params'] = {}
    sp = d.getObject('Params')
    if sp:
        for c in sp.getUsedCells():
            try:
                res['params'][c] = [sp.getAlias(c), str(sp.get(c))]
            except Exception:
                pass
    FreeCAD.closeDocument(d.Name)
    for w in (2, 3, 12):
        d = FreeCAD.openDocument(tmp)
        d.recompute()
        try:
            set_cell(d, 'wall', w)
            res['at_wall%s' % w] = snap(d)
        except Exception as e:
            res['at_wall%s' % w] = {'error': str(e)[:300]}
        FreeCAD.closeDocument(d.Name)
    ok, detail = passes({w: res['at_wall%s' % w] for w in (2, 3, 12)})
    res['pass'] = ok
    res['criteria'] = detail
    json.dump(res, open(out, 'w'), indent=1, default=str)
    log16('check', json.dumps({w: (res['at_wall%s' % w].get('builds'), (res['at_wall%s' % w].get('hole') or {}).get('skin'),
                                   (res['at_wall%s' % w].get('hole') or {}).get('front_solid'),
                                   res['at_wall%s' % w].get('depth')) for w in (2, 3, 12)}),
          'PASS' if ok else 'FAIL')


if MODE16 == 'build':
    build()
elif MODE16 == 'check':
    check(os.environ['FC16_DOC'], OUT)
