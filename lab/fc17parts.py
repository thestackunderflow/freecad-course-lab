"""fc17 (FreeCAD course lesson 17, a second key peg by Mirror: the plane is the fold between the two pegs), lab instrument
run by freecadcmd, never filmed. Built on lesson 16's fixed cup (out/fc16/P/hole-fixed.FCStd: Pad, Thickness outward
=Params.wall, Sketch001 on XZ offset =Params.cup_length / 2, Pad001 peg, HoleSketch, Pocket =Params.wall) with the readers
of lab/fc14parts.py .. lab/fc16parts.py. New name `peg_x` 15 (Params A8 / B8): Sketch001's constraint peg_x0 becomes
=Params.peg_x - Params.peg_size / 2, so the peg sits at x 10..20.

    FC17_OUT=/lab/out/fc17/P FC17_MODE=build freecadcmd /lab/lab/fc17parts.py
        peg-moved, mirror-xz (the trap), mirror-yz (the fix), mirror-vaxis (the panel's default Vertical sketch axis),
        G0 Q1, Q2, Q4, Q5, Q6, Q9, Q10, Q11 by code -> build.json (+ ref volumes for the score)
    FC17_DOC=x.FCStd FC17_OUT=y.json FC17_MODE=check freecadcmd /lab/lab/fc17parts.py
        a saved file (Claude's): as saved, recomputed, at peg_x 15 / 20 / 8 and wall 3 (PLAN 2.5, lab/fc17score.py)."""
import json
import os
import shutil
import sys

os.environ['FC16_MODE'] = 'lib'
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fc16parts.py')).read())   # noqa: S102 (readers)

OUT17 = os.environ.get('FC17_OUT', '/lab/out/fc17/P')
MODE17 = os.environ.get('FC17_MODE', 'build')
START17 = '/lab/out/fc16/P/hole-fixed.FCStd'
SETS = {'15': {'peg_x': 15}, '20': {'peg_x': 20}, '8': {'peg_x': 8}, 'w3': {'peg_x': 15, 'wall': 3}}


def log17(*a):
    print('FC17', *a)
    sys.stdout.flush()


def add_peg_x(d, v=15):
    s = d.getObject('Params')
    s.set('A8', 'peg_x')
    s.set('B8', str(v))
    s.setAlias('B8', 'peg_x')
    d.recompute()
    d.getObject('Sketch001').setExpression('.Constraints.peg_x0', 'Params.peg_x - Params.peg_size / 2')
    d.recompute()
    touch_all(d)


def add_mirror(d, plane, originals=('Pad001',), name='Mirrored'):
    """plane: 'XZ' / 'YZ' / 'XY' (Body origin planes), 'vaxis' (Sketch001 V_Axis), or an object (datum plane)"""
    b = main_body(d)
    m = b.newObject('PartDesign::Mirrored', name)
    m.Originals = [d.getObject(o) for o in originals]
    if plane == 'vaxis':
        m.MirrorPlane = (d.getObject('Sketch001'), ['V_Axis'])
    elif isinstance(plane, str):
        m.MirrorPlane = (origin(b, plane + '_Plane'), [''])
    else:
        m.MirrorPlane = (plane, [''])
    b.Tip = m                      # the GUI command puts the Tip on the new feature; Body.newObject does not here
    d.recompute()
    touch_all(d)
    return m


def mirror_info(d):
    out = []
    b = main_body(d)
    for o in (b.Group if b else []):
        if o.TypeId == 'PartDesign::Mirrored':
            mp = o.MirrorPlane
            r = {'name': o.Name, 'originals': [x.Name for x in o.Originals],
                 'plane': [getattr(mp[0], 'Role', None) or mp[0].Name, list(mp[1])] if mp and mp[0] else None,
                 'mode': str(getattr(o, 'TransformMode', '')), 'state': list(o.State)}
            try:
                r['status'] = o.getStatusString()
            except Exception:
                pass
            rej = getattr(o, 'RejectedShape', None) or getattr(o, 'Rejected', None)
            if rej is not None and hasattr(rej, 'isNull') and not rej.isNull():
                r['rejected_bbox'] = [round(rej.BoundBox.XMin, 3), round(rej.BoundBox.XMax, 3), round(rej.BoundBox.YMin, 3),
                                      round(rej.BoundBox.YMax, 3), round(rej.BoundBox.ZMin, 3), round(rej.BoundBox.ZMax, 3)]
            out.append(r)
    return out


def mread(d):
    s = main_body(d).Shape
    px, w, ps = param(d, 'peg_x') or 0.0, param(d, 'wall') or 2.0, param(d, 'peg_size') or 10.0
    ins = lambda x, y, z: s.isInside(V(x, y, z), 1e-6, True)
    bb = s.BoundBox
    m = {'solids': len(s.Solids), 'valid': s.isValid(), 'volume': round(s.Volume, 3),
         'bbox': [round(v, 4) for v in (bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax)],
         'y_min': round(bb.YMin, 4), 'y_max': round(bb.YMax, 4), 'y_extent': round(bb.YLength, 4),
         'behind_back': round(bb.YMax - (20 + w), 4)}
    m['pt'] = {'orig': ins(px, -28, 40), 'copy': ins(-px, -28, 40), 'back_orig': ins(px, 28, 40),
               'back_copy': ins(-px, 28, 40)}
    m['plan_pts'] = {'(15,28,40)': ins(15, 28, 40), '(-15,-28,40)': ins(-15, -28, 40), '(15,-28,40)': ins(15, -28, 40),
                     '(-15,28,40)': ins(-15, 28, 40), '(15,-28,-40)': ins(15, -28, -40)}
    xf = segs(s, V(-45, -28, 40), V(45, -28, 40))
    m['x_runs_front'] = xf
    m['x_runs_back'] = segs(s, V(-45, 28, 40), V(45, 28, 40))
    m['centre_gap'] = round((xf[1][0] + xf[1][1]) / 2 - (xf[0][0] + xf[0][1]) / 2, 4) if len(xf) == 2 else None
    m['face_gap'] = round(xf[1][0] - xf[0][1], 4) if len(xf) == 2 else None
    h = hole_read(d)
    m['hole_open'] = all(h['axis_air'].values())
    m['inside'] = [h.get('inside_w'), h.get('inside_l'), h.get('inside_d')]
    m['top_open'] = h.get('top_open')
    m['outside'] = [h.get('outside_w'), h.get('outside_l')]
    a, c = ps / 2.0 - 0.1, ps / 2.0 + 0.1
    pr = {'orig': m['pt']['orig'], 'copy': m['pt']['copy'], 'back_orig': m['pt']['back_orig'], 'back_copy': m['pt']['back_copy']}
    pr['across'] = all(ins(g * (px + e * a), -28, 40) and not ins(g * (px + e * c), -28, 40) for g in (1, -1) for e in (1, -1))
    pr['tips'] = all(ins(g * px, -34.9, 40) and not ins(g * px, -35.1, 40) for g in (1, -1))
    pr['height'] = all(ins(g * px, -28, 40 + e * a) and not ins(g * px, -28, 40 + e * c) for g in (1, -1) for e in (1, -1))
    pr['back_wall'] = all(ins(x, 20 + w / 2.0, 40) for x in (px, -px, 0))
    m['probe'] = pr
    return m


def bad_any(d):
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


def snap17(d, extra=None):
    ok, info = builds(d)
    r = {'builds': ok, 'build_info': info, 'state': feat_state(d), 'bad_any': bad_any(d),
         'peg_x': param(d, 'peg_x'), 'wall': param(d, 'wall'), 'peg_size': param(d, 'peg_size'), 'mirrors': mirror_info(d)}
    try:
        r['m'] = mread(d)
        r['volume'] = r['m']['volume']
    except Exception as e:
        r['m'] = {'error': str(e)[:300]}
    if extra:
        r.update(extra)
    return r


def names(d):
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


def save17(d, name):
    p = os.path.join(OUT17, name + '.FCStd')
    d.saveAs(p)
    return p


def at_sets(path, sets):
    out = {}
    for k, cells in sets.items():
        d = FreeCAD.openDocument(path)
        d.recompute()
        try:
            for a, v in cells.items():
                set_cell(d, a, v)
            out[k] = snap17(d)
        except Exception as e:
            out[k] = {'error': str(e)[:300]}
        FreeCAD.closeDocument(d.Name)
    return out


def corner_cup(fold=None):
    """your turn (Q11): a cup with its corner on the origin (x 0..60, y 0..40, z 0..50), peg 10 x 15 x 10 centred x 45
    on the front (y -15..0, z 35..45), mirrored across YZ or a datum plane at x `fold`"""
    d = FreeCAD.newDocument('yt%s' % (fold or 0))
    b = d.addObject('PartDesign::Body', 'Body')
    box = b.newObject('PartDesign::AdditiveBox', 'Box')
    box.Length, box.Width, box.Height = 60, 40, 50
    peg = b.newObject('PartDesign::AdditiveBox', 'PegBox')
    peg.Length, peg.Width, peg.Height = 10, 15, 10
    peg.Placement = FreeCAD.Placement(V(40, -15, 35), FreeCAD.Rotation())   # no attachment: Placement places it
    d.recompute()
    if fold is None:
        plane = (origin(b, 'YZ_Plane'), [''])
    else:
        pl = b.newObject('PartDesign::Plane', 'Fold')
        pl.AttachmentSupport = [(origin(b, 'YZ_Plane'), '')]
        pl.MapMode = 'FlatFace'
        pl.AttachmentOffset = FreeCAD.Placement(V(0, 0, fold), FreeCAD.Rotation())
        d.recompute()
        plane = (pl, [''])
    m = b.newObject('PartDesign::Mirrored', 'Mirrored')
    m.Originals = [peg]
    m.MirrorPlane = plane
    b.Tip = m
    d.recompute()
    s = b.Shape
    pegshape = Part.makeBox(10, 15, 10, V(40, -15, 35))
    nrm = V(1, 0, 0)
    mir = pegshape.mirror(V(fold or 0, 0, 0), nrm)
    r = {'peg_bbox_x': [round(pegshape.BoundBox.XMin, 3), round(pegshape.BoundBox.XMax, 3)],
         'copy_centre_x_by_part': round(mir.BoundBox.Center.x, 4),
         'copy_on_cup': mir.BoundBox.XMax > 0 and mir.BoundBox.XMin < 60,
         'feature_state': list(m.State), 'solids': len(s.Solids), 'volume': round(s.Volume, 3),
         'x_runs_front': segs(s, V(-80, -7, 40), V(80, -7, 40)),
         'bbox_x': [round(s.BoundBox.XMin, 3), round(s.BoundBox.XMax, 3)]}
    try:
        r['status'] = m.getStatusString()
    except Exception:
        pass
    FreeCAD.closeDocument(d.Name)
    return r


def build():
    os.makedirs(OUT17, exist_ok=True)
    res = {'start_file': START17}
    tmp = '/tmp/peg-moved.FCStd'
    shutil.copy(START17, tmp)
    d = FreeCAD.openDocument(tmp)
    d.recompute()
    res['start16'] = snap17(d)
    add_peg_x(d)
    sk = d.getObject('Sketch001')
    res['q1'] = {'peg_moved': snap17(d, {'tree': tree(d), 'sketch_exprs': names(d)['exprs'].get('Sketch001'),
                                         'params': names(d)['params']})}
    pm = save17(d, 'peg-moved')
    FreeCAD.closeDocument(d.Name)
    res['q1']['peg_x20'] = at_sets(pm, {'20': {'peg_x': 20}})['20']
    res['q10'] = at_sets(pm, {'w2': {'wall': 2}, 'w3': {'wall': 3}})
    files = {}
    for key, plane in (('xz', 'XZ'), ('yz', 'YZ'), ('vaxis', 'vaxis')):
        d = FreeCAD.openDocument(pm)
        d.recompute()
        add_mirror(d, plane)
        files[key] = save17(d, 'mirror-' + key)
        res['mirror_' + key] = snap17(d, {'tree': tree(d)})
        FreeCAD.closeDocument(d.Name)
    res['q2'] = res['mirror_xz']
    res['q2_reopened'] = at_sets(files['xz'], {'15': {}})['15']
    res['q4'] = {'yz': res['mirror_yz'], 'vaxis': res['mirror_vaxis']}
    # Q5 edges (pinned only): XY plane; nothing selected = Whole shape across the Body's XY plane
    d = FreeCAD.openDocument(pm)
    d.recompute()
    add_mirror(d, 'XY')
    res['q5_xy'] = snap17(d)
    FreeCAD.closeDocument(d.Name)
    d = FreeCAD.openDocument(pm)
    d.recompute()
    m = add_mirror(d, 'XY', originals=())
    try:
        m.TransformMode = 'Whole shape'
        d.recompute()
        touch_all(d)
    except Exception as e:
        res['q5_whole_err'] = str(e)[:200]
    res['q5_whole_xy'] = snap17(d, {'modes': list(m.getEnumerationsOfProperty('TransformMode'))})
    FreeCAD.closeDocument(d.Name)
    # Q6 proof on the fixed file opened again: peg_x 20, then peg_size 12, then wall 3 (one after another, as the GUI take)
    d = FreeCAD.openDocument(files['yz'])
    d.recompute()
    q6 = {'reopen': snap17(d)}
    set_cell(d, 'peg_x', 20)
    q6['peg_x20'] = snap17(d)
    set_cell(d, 'peg_size', 12)
    q6['peg_size12'] = snap17(d)
    set_cell(d, 'wall', 3)
    q6['wall3'] = snap17(d)
    FreeCAD.closeDocument(d.Name)
    q6['xz_peg_x20'] = at_sets(files['xz'], {'20': {'peg_x': 20}})['20']
    q6['vaxis_peg_x20'] = at_sets(files['vaxis'], {'20': {'peg_x': 20}})['20']
    res['q6'] = q6
    # score reference: our fixed file at the four score settings; and the trap file at them (the scorer must fail it)
    res['ref'] = at_sets(files['yz'], SETS)
    res['ref_volumes'] = {k: v.get('volume') for k, v in res['ref'].items()}
    res['trap_at_sets'] = at_sets(files['xz'], SETS)
    # Q11 your turn + Short
    yt = corner_cup()
    yt30 = corner_cup(30)
    s25 = at_sets(files['yz'], {'25': {'peg_x': 25}})['25']
    xf = s25['m']['x_runs_front']
    res['q11'] = {'corner_cup_yz': yt, 'corner_cup_fold30': yt30,
                  'corner_cup_yz_copy_centre_x': yt['copy_centre_x_by_part'], 'corner_cup_yz_copy_on_cup': yt['copy_on_cup'],
                  'corner_cup_fold30_copy_centre_x': next(((a + b) / 2 for a, b in yt30['x_runs_front'] if b < 30), None),
                  'short_peg25': s25, 'short_peg25_copy_centre_x': (xf[0][0] + xf[0][1]) / 2 if xf else None}
    res['names_start_xz'] = names(FreeCAD.openDocument(files['xz']))
    json.dump(res, open(os.path.join(OUT17, 'build.json'), 'w'), indent=1, default=str)
    sm = lambda s: (s['builds'], s['m']['solids'], s['m']['y_extent'], s['m']['behind_back'], s['m']['x_runs_front'],
                    s['m']['x_runs_back'])
    log17('built', json.dumps({'q1': sm(res['q1']['peg_moved']), 'xz': sm(res['q2']), 'yz': sm(res['q4']['yz']),
                               'vaxis': sm(res['q4']['vaxis']), 'ref': res['ref_volumes']}, default=str))


def check(doc_path, out):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from fc17score import criteria_ok
    B = json.load(open('/lab/out/fc17/P/build.json'))
    res = {'doc': doc_path}
    tmp = '/tmp/fc17-check.FCStd'
    shutil.copy(doc_path, tmp)
    d = FreeCAD.openDocument(tmp)
    nm = names(d)
    st = B['names_start_xz']
    same_p = nm['params'] == st['params']
    same_e = all(nm['exprs'].get(k) == v for k, v in st['exprs'].items())
    res['names'] = nm
    res['stored'] = snap17(d)
    d.recompute()
    res['recomputed'] = snap17(d)
    res['tree'] = tree(d)
    res['objects'] = [(o.Name, o.Label, o.TypeId) for o in d.Objects][:80]
    res['asis'] = {'names_same': same_p and same_e, 'params_same': same_p, 'exprs_same': same_e,
                   'peg_x': param(d, 'peg_x'), 'bad_any': res['recomputed']['bad_any']}
    FreeCAD.closeDocument(d.Name)
    res['at'] = at_sets(tmp, SETS)
    ok, det = criteria_ok(res['at'], res['asis'], B['ref_volumes'])
    res['pass'] = ok
    res['criteria'] = det
    json.dump(res, open(out, 'w'), indent=1, default=str)
    log17('check', json.dumps({k: [k2 for k2, v2 in v.items() if not v2] for k, v in det.items()}),
          'names_same', res['asis']['names_same'], 'PASS' if ok else 'FAIL')


if MODE17 == 'build':
    build()
elif MODE17 == 'check':
    check(os.environ['FC17_DOC'], OUT17)
