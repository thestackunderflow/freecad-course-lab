"""fc18 (FreeCAD course lesson 18, a round pen cup by Revolve: the outline's width is the radius), lab instrument run by
freecadcmd, never filmed. A new part (PLAN 2.1): Params cup_diameter 60, cup_height 80, wall 2; Body; Sketch on
XZ_Plane (sketch H = world X, V = world Z), the 6-line half-section (0,0) -> (W,0) -> (W,H) -> (W-w,H) -> (W-w,w) ->
(0,w) -> (0,0), fully constrained: width (DistanceX of the floor line) = W, height =Params.cup_height, rim and floor
=Params.wall; Revolution about the sketch's V_Axis ("Vertical sketch axis"), Angle 360. Readers of lab/fc14-15parts.py.

    FC18_OUT=/lab/out/fc18/P FC18_MODE=build freecadcmd /lab/lab/fc18parts.py
        round-start (names, empty Body), round-name (W =Params.cup_diameter: the trap), round-typed30 (W 30 typed),
        round-fixed (W =Params.cup_diameter / 2), G0 Q1-Q3, Q5, Q6, Q9 by code -> build.json
    FC18_DOC=x.FCStd FC18_OUT=y.json FC18_MODE=check freecadcmd /lab/lab/fc18parts.py
        a saved file (Claude's or ours): as saved, then cup_diameter 60 / 80 / 45 (PLAN 2.5, lab/fc18score.py)."""
import json
import math
import os
import shutil
import sys

os.environ['FC15_MODE'] = 'lib'
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fc15parts.py')).read())   # noqa: S102 (readers)

OUT18 = os.environ.get('FC18_OUT', '/lab/out/fc18/P')
MODE18 = os.environ.get('FC18_MODE', 'build')
NAMES18 = (('cup_diameter', 60), ('cup_height', 80), ('wall', 2))


def log18(*a):
    print('FC18', *a)
    sys.stdout.flush()


def start_doc18(name):
    d = FreeCAD.newDocument(name)
    s = d.addObject('Spreadsheet::Sheet', 'Params')
    for i, (n, v) in enumerate(NAMES18, 1):
        s.set('A%d' % i, n)
        s.set('B%d' % i, str(v))
        s.setAlias('B%d' % i, n)
    d.recompute()
    b = d.addObject('PartDesign::Body', 'Body')
    b.Label = 'Cup'
    d.recompute()
    return d


def half_section(d, width, plane='XZ_Plane'):
    """width: a number (typed) or an expression string for the width constraint"""
    b = main_body(d)
    sk = b.newObject('Sketcher::SketchObject', 'Sketch')
    sk.AttachmentSupport = [(origin(b, plane), '')]
    sk.MapMode = 'FlatFace'
    W = 30.0
    pts = [(0, 0), (W, 0), (W, 80), (W - 2, 80), (W - 2, 2), (0, 2)]
    for i in range(6):
        a, c = pts[i], pts[(i + 1) % 6]
        sk.addGeometry(Part.LineSegment(V(a[0], a[1], 0), V(c[0], c[1], 0)))
    for i in range(6):
        sk.addConstraint(Sketcher.Constraint('Coincident', i, 2, (i + 1) % 6, 1))
    for i in (0, 2, 4):
        sk.addConstraint(Sketcher.Constraint('Horizontal', i))
    for i in (1, 3, 5):
        sk.addConstraint(Sketcher.Constraint('Vertical', i))
    sk.addConstraint(Sketcher.Constraint('Coincident', 0, 1, -1, 1))          # the floor line starts at the origin
    cw = sk.addConstraint(Sketcher.Constraint('DistanceX', 0, 1, 0, 2, W))
    ch = sk.addConstraint(Sketcher.Constraint('DistanceY', 1, 1, 1, 2, 80.0))
    cr = sk.addConstraint(Sketcher.Constraint('DistanceX', 2, 2, 2, 1, 2.0))   # rim: inside line to outside line
    cf = sk.addConstraint(Sketcher.Constraint('DistanceY', 5, 2, 5, 1, 2.0))   # floor: origin up to the floor top
    for c, n in ((cw, 'width'), (ch, 'height'), (cr, 'rim'), (cf, 'floor')):
        sk.renameConstraint(c, n)
    sk.setExpression('.Constraints.height', 'Params.cup_height')
    sk.setExpression('.Constraints.rim', 'Params.wall')
    sk.setExpression('.Constraints.floor', 'Params.wall')
    if isinstance(width, str):
        sk.setExpression('.Constraints.width', width)
    else:
        sk.setDatum(cw, FreeCAD.Units.Quantity('%s mm' % width))
    d.recompute()
    return sk


def add_revolution(d, sk, axis='V_Axis', angle=360.0):
    b = main_body(d)
    r = b.newObject('PartDesign::Revolution', 'Revolution')
    r.Profile = sk
    r.ReferenceAxis = (sk, [axis])
    r.Angle = angle
    sk.Visibility = False
    b.Tip = r
    d.recompute()
    touch_all(d)
    return r


def round_doc(name, width):
    d = start_doc18(name)
    sk = half_section(d, width)
    add_revolution(d, sk)
    return d


def the_shape(d):
    b = main_body(d)
    if b is not None and not b.Shape.isNull() and b.Shape.Solids:
        return b.Shape, 'Body'
    best = None
    for o in d.Objects:
        s = getattr(o, 'Shape', None)
        if s is None or s.isNull() or not s.Solids or not getattr(o, 'Visibility', True):
            continue
        if best is None or s.Volume > best[0].Volume:
            best = (s, o.Name)
    return best if best else (None, None)


def mread18(d):
    s, src = the_shape(d)
    dia = param(d, 'cup_diameter') or 60.0
    w = param(d, 'wall') or 2.0
    h = param(d, 'cup_height') or 80.0
    if s is None:
        return {'error': 'no solid', 'src': src}
    bb = s.BoundBox
    ins = lambda x, y, z: s.isInside(V(x, y, z), 1e-6, True)
    r = dia / 2.0
    m = {'src': src, 'solids': len(s.Solids), 'valid': s.isValid(), 'volume': round(s.Volume, 3),
         'bbox': [round(v, 4) for v in (bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax)],
         'outside_x': round(bb.XLength, 4), 'outside_y': round(bb.YLength, 4), 'z': [round(bb.ZMin, 4), round(bb.ZMax, 4)],
         'centre_xy': [round(bb.Center.x, 4), round(bb.Center.y, 4)]}
    xr = segs(s, V(-400, 0, h / 2.0), V(400, 0, h / 2.0))
    m['x_runs_mid'] = xr
    m['inside'] = round(xr[1][0] - xr[0][1], 4) if len(xr) == 2 else None
    m['z_runs_axis'] = segs(s, V(0, 0, -200), V(0, 0, 300))
    dirs = [(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in (0, 90, 180, 270, 45)]
    ring = {}
    for i, (cx, cy) in enumerate(dirs):
        ring[i] = [ins(cx * (r - w + 0.05), cy * (r - w + 0.05), h / 2.0), not ins(cx * (r - w - 0.05), cy * (r - w - 0.05), h / 2.0),
                   not ins(cx * (r + 0.05), cy * (r + 0.05), h / 2.0)]
    m['ring'] = ring
    m['ring_ok'] = all(all(v) for v in ring.values())
    m['floor_ok'] = ins(0, 0, w / 2.0) and not ins(0, 0, w + 1)
    ro = bb.XMax          # the rim probe sits in the wall the part really has (the trap's rim is at 60, not 30)
    m['top_open'] = (not ins(0, 0, h - 0.1)) and not ins(0, 0, h + 0.1) and ins(ro - w / 2.0, 0, h - 0.1)
    return m


def bad_any18(d):
    out = {}
    for o in d.Objects:
        st = list(getattr(o, 'State', []))
        if any(x in ('Invalid', 'Error') for x in st):
            msg = ''
            try:
                msg = o.getStatusString()
            except Exception:
                pass
            out[o.Name] = [st, msg]
    return out


def all_state(d):
    out = {}
    for o in d.Objects:
        if o.TypeId.startswith(('PartDesign::', 'Sketcher::')) and o.TypeId != 'PartDesign::Body' and 'Origin' not in o.TypeId:
            msg = ''
            try:
                msg = o.getStatusString()
            except Exception:
                pass
            out[o.Name] = [list(o.State) or ['Up-to-date'], msg]
    return out


def sketch_info(d):
    out = {}
    for o in d.Objects:
        if o.TypeId != 'Sketcher::SketchObject':
            continue
        r = {'support': [[x[0].Name, list(x[1]) if isinstance(x[1], (list, tuple)) else x[1]] for x in (o.AttachmentSupport or [])],
             'map_mode': o.MapMode, 'exprs': sorted([k.lstrip('.'), v] for k, v in o.ExpressionEngine),
             'geo': len(o.Geometry), 'constraints': len(o.Constraints)}
        for k in ('FullyConstrained',):
            r[k] = getattr(o, k, None)
        try:
            r['solve'] = o.solve()
        except Exception as e:
            r['solve'] = str(e)[:100]
        try:
            i = [c.Name for c in o.Constraints].index('width')
            r['width_value'] = round(o.Constraints[i].Value, 4)
        except ValueError:
            pass
        out[o.Name] = r
    return out


def revolve_info(d):
    out = []
    for o in d.Objects:
        if 'Revolution' in o.TypeId or 'Revolve' in o.TypeId:
            b = [x for x in d.Objects if x.TypeId == 'PartDesign::Body' and o in x.Group]
            r = {'name': o.Name, 'type': o.TypeId, 'in_body': bool(b), 'state': list(o.State)}
            for k in ('Angle', 'Type', 'Reversed', 'Midplane'):
                v = getattr(o, k, None)
                r[k] = str(v) if v is not None else None
            ra = getattr(o, 'ReferenceAxis', None)
            r['axis'] = [ra[0].Name, list(ra[1])] if ra and ra[0] else None
            prof = getattr(o, 'Profile', None)
            r['profile'] = prof[0].Name if isinstance(prof, tuple) and prof and prof[0] else getattr(prof, 'Name', None)
            try:
                r['status'] = o.getStatusString()
            except Exception:
                pass
            out.append(r)
    return out


def names18(d):
    sp = d.getObject('Params')
    p = {}
    if sp:
        for c in sp.getUsedCells():
            try:
                p[c] = [sp.getAlias(c), sp.getContents(c)]
            except Exception:
                pass
    ex = {o.Name: sorted([k.lstrip('.'), v] for k, v in o.ExpressionEngine)
          for o in d.Objects if getattr(o, 'ExpressionEngine', None)}
    return {'params': p, 'exprs': ex}


def reads_dia(nm):
    """(f): an expression names cup_diameter, directly or through a Params cell whose content names it"""
    via = {a for a, c in nm['params'].values() if a and 'cup_diameter' in str(c) and a != 'cup_diameter'}
    hits = []
    for o, lst in nm['exprs'].items():
        for k, v in lst:
            if 'cup_diameter' in v or any(x in v for x in via):
                hits.append([o, k, v])
    return hits


def snap18(d, extra=None):
    bad = bad_any18(d)
    r = {'state': all_state(d), 'bad_any': bad, 'cup_diameter': param(d, 'cup_diameter'), 'wall': param(d, 'wall'),
         'cup_height': param(d, 'cup_height'), 'revolutions': revolve_info(d), 'sketches': sketch_info(d)}
    try:
        r['m'] = mread18(d)
        r['volume'] = r['m'].get('volume')
        r['builds'] = (not bad and 'error' not in r['m'] and r['m']['valid'] and r['m']['solids'] == 1)
    except Exception as e:
        r['m'] = {'error': str(e)[:300]}
        r['builds'] = False
    sk = r['sketches'].get('Sketch') or {}
    r['width_value'] = sk.get('width_value')
    r['width_expr'] = dict((k, v) for k, v in sk.get('exprs', [])).get('Constraints.width')
    r['sketch_dof'] = 0 if (sk.get('FullyConstrained') is True) else sk.get('FullyConstrained')
    if extra:
        r.update(extra)
    return r


def save18(d, name):
    p = os.path.join(OUT18, name + '.FCStd')
    d.saveAs(p)
    return p


def at18(path, sets):
    out = {}
    for k, cells in sets.items():
        d = FreeCAD.openDocument(path)
        d.recompute()
        try:
            for a, v in cells.items():
                set_cell(d, a, v)
            out[k] = snap18(d, {'set': cells})
        except Exception as e:
            out[k] = {'error': str(e)[:300]}
        FreeCAD.closeDocument(d.Name)
    return out


def build():
    os.makedirs(OUT18, exist_ok=True)
    res = {'q1': {'files': {}}}
    d = start_doc18('round_start')
    res['q1']['files']['round-start'] = save18(d, 'round-start')
    res['q1']['round-start'] = {'names': names18(d), 'tree': tree(d)}
    FreeCAD.closeDocument(d.Name)
    files = {}
    for key, width in (('round-name', 'Params.cup_diameter'), ('round-typed30', 30.0),
                       ('round-fixed', 'Params.cup_diameter / 2'), ('round-typed60', 60.0)):
        d = round_doc(key.replace('-', '_'), width)
        files[key] = save18(d, key)
        res['q1']['files'][key] = files[key]
        res['q1'][key] = snap18(d, {'tree': tree(d), 'names': names18(d)})
        FreeCAD.closeDocument(d.Name)
    res['q3'] = {'name': res['q1']['round-name'], 'typed60': res['q1']['round-typed60'],
                 'name_reopened': at18(files['round-name'], {'r': {}})['r']}
    # Q2: the other planes / axis by code (edges for the lab note: which way a beginner's other picks go)
    q2 = {}
    for key, plane, axis in (('xz_vaxis', 'XZ_Plane', 'V_Axis'), ('xz_haxis', 'XZ_Plane', 'H_Axis'),
                             ('yz_vaxis', 'YZ_Plane', 'V_Axis'), ('xy_vaxis', 'XY_Plane', 'V_Axis')):
        d = start_doc18('q2_' + key)
        sk = half_section(d, 'Params.cup_diameter / 2', plane)
        add_revolution(d, sk, axis)
        q2[key] = snap18(d)
        FreeCAD.closeDocument(d.Name)
    res['q2'] = q2
    # Q5 proof: the fixed file opened again, cup_diameter 80; comparison by code
    res['q5'] = {'fixed_reopened_80': at18(files['round-fixed'], {'80': {'cup_diameter': 80}})['80'],
                 'name_80': at18(files['round-name'], {'80': {'cup_diameter': 80}})['80'],
                 'typed30_80': at18(files['round-typed30'], {'80': {'cup_diameter': 80}})['80']}
    # Q6: sizes and walls on the fixed file
    sets = {}
    for dia in (45, 60, 80, 120):
        for w in (2, 3):
            sets['d%d_w%d' % (dia, w)] = {'cup_diameter': dia, 'wall': w}
    res['q6'] = at18(files['round-fixed'], sets)
    # Q9 your turn (45) and the Short (40)
    res['q9'] = {'fixed_45': at18(files['round-fixed'], {'45': {'cup_diameter': 45}})['45'],
                 'name_45': at18(files['round-name'], {'45': {'cup_diameter': 45}})['45'],
                 'name_40': at18(files['round-name'], {'40': {'cup_diameter': 40}})['40']}
    json.dump(res, open(os.path.join(OUT18, 'build.json'), 'w'), indent=1, default=str)
    sm = lambda s: (s['builds'], s['m'].get('outside_x'), s['m'].get('z'), s['m'].get('inside'), s['m'].get('volume'))
    log18('built', json.dumps({'name': sm(res['q3']['name']), 'fixed': sm(res['q1']['round-fixed']),
                               'typed30': sm(res['q1']['round-typed30']), 'p80': sm(res['q5']['fixed_reopened_80']),
                               'q2': {k: sm(v) for k, v in q2.items()}}, default=str))


def check(doc_path, out):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from fc18score import SETTINGS, criteria_ok, cls
    res = {'doc': doc_path}
    tmp = '/tmp/fc18-check.FCStd'
    shutil.copy(doc_path, tmp)
    d = FreeCAD.openDocument(tmp)
    nm = names18(d)
    res['names'] = nm
    res['stored'] = snap18(d)
    d.recompute()
    res['recomputed'] = snap18(d)
    res['tree'] = tree(d)
    res['objects'] = [(o.Name, o.Label, o.TypeId) for o in d.Objects][:80]
    res['asis'] = {'cup_diameter': param(d, 'cup_diameter'), 'cup_height': param(d, 'cup_height'), 'wall': param(d, 'wall'),
                   'bad_any': res['recomputed']['bad_any']}
    FreeCAD.closeDocument(d.Name)
    res['at'] = at18(tmp, {k: {'cup_diameter': v, 'wall': 2} for k, v in SETTINGS.items()})
    ok, det = criteria_ok(res['at'])
    revs = res['recomputed']['revolutions']
    res['e_revolve_in_body'] = any(r['type'] == 'PartDesign::Revolution' and r['in_body'] for r in revs)
    res['e_part_revolution'] = any(r['type'] != 'PartDesign::Revolution' for r in revs)
    res['f_reads_cup_diameter'] = reads_dia(nm)
    broke = not res['recomputed']['builds'] and all(not v.get('builds') for v in res['at'].values())
    res['pass'] = ok
    res['criteria'] = det
    res['cls'] = cls(res['at'], ok, res['e_revolve_in_body'], broke)
    if res['cls'] == 1 and res['e_part_revolution'] and not res['e_revolve_in_body']:
        res['cls'] = 9
    json.dump(res, open(out, 'w'), indent=1, default=str)
    log18('check', json.dumps({k: [k2 for k2, v2 in v.items() if not v2] for k, v in det.items()}),
          'cls', res['cls'], 'f', len(res['f_reads_cup_diameter']), 'PASS' if ok else 'FAIL')


if MODE18 == 'build':
    build()
elif MODE18 == 'check':
    check(os.environ['FC18_DOC'], OUT18)
