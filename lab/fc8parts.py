"""fc8 (FreeCAD course lesson 8, assembly), lab instrument run by freecadcmd, never filmed.

    FC8_OUT=/lab/out/fc8/P FC8_MODE=build freecadcmd /lab/lab/fc8parts.py
        fc8-{typo,touch,gap01,gap04}.FCStd + build.json: the sc8 hook and rail (solidcraft-course-lab/lab/sc8parts.py)
        as two Part Design bodies of boxes driven by a spreadsheet `Params` (lesson 3); every number read back by code.
    FC8_OUT=/lab/out/fc8/P2 FC8_MODE=ladder freecadcmd /lab/lab/fc8parts.py
        video D probe P2: gap02/gap03 built if missing, then the six rungs by code -> ladder.json.
    FC8_OUT=... FC8_MODE=asm freecadcmd /lab/lab/fc8parts.py
        G0a: an Assembly by Python on the typo file (links, ground, slider by whole-body references, solve); the hook
        moved 85 up and back into the rail: solver result and the shared volume after each move -> asm.json.
    FC8_DOC=x.FCStd FC8_OUT=y.json FC8_MODE=check freecadcmd /lab/lab/fc8parts.py
        any saved file (a take's, a Claude run's): bodies, Common of the two parts as placed, gaps each side -> y.json.
Coordinates as sc8: w = x + 10 (out from the rail's front face), u = y + 10 (across, from the rib's centre line)."""
import json
import os
import sys

import FreeCAD
import Part

OUT = os.environ.get('FC8_OUT', '/lab/out/fc8/P')
MODE = os.environ.get('FC8_MODE', 'build')
V = FreeCAD.Vector

CASES = {'typo': (0, '11.6'), 'touch': (0, None), 'gap01': (0.1, None), 'gap04': (0.4, None)}
LADDER = {'gap02': (0.2, None), 'gap03': (0.3, None)}   # video D probe P2 rungs (FC8_MODE=ladder)


def log(*a):
    print('FC8', *a)
    sys.stdout.flush()


def box(body, kind, name, L, W, H, x, y, z):
    """A Part Design box; each of L W H x y z is a number or an expression on Params."""
    b = body.newObject('PartDesign::' + kind, name)
    for prop, v in (('Length', L), ('Width', W), ('Height', H)):
        if isinstance(v, str):
            b.setExpression(prop, v)
        else:
            setattr(b, prop, v)
    num = [0 if isinstance(v, str) else v for v in (x, y, z)]
    b.Placement = FreeCAD.Placement(V(*num), FreeCAD.Rotation())
    for prop, v in (('.Placement.Base.x', x), ('.Placement.Base.y', y), ('.Placement.Base.z', z)):
        if isinstance(v, str):
            b.setExpression(prop, v)
    return b


def build(case):
    gap, typo = {**CASES, **LADDER}[case]
    d = FreeCAD.newDocument('fc8_' + case)
    s = d.addObject('Spreadsheet::Sheet', 'Params')
    rows = [('rib_stem', '6'), ('rib_head', '12'), ('gap', str(gap)), ('slot_stem', '=rib_stem + 2 * gap'),
            ('slot_head', typo if typo else '=rib_head + 2 * gap')]
    for i, (n, v) in enumerate(rows, 1):
        s.set('A%d' % i, n)
        s.set('B%d' % i, v)
        s.setAlias('B%d' % i, n)
    d.recompute()
    hook = d.addObject('PartDesign::Body', 'Hook')
    box(hook, 'AdditiveBox', 'Plate', 5, 20, 60, 0, -20, 0)
    box(hook, 'AdditiveBox', 'Arm', 20, 20, 5, 5, -20, 0)
    box(hook, 'AdditiveBox', 'Lip', 5, 20, 5, 20, -20, 5)
    box(hook, 'AdditiveBox', 'Block', '10 - Params.gap', 20, 60, '-10 + Params.gap', -20, 0)
    # the T-slot: the rib's T grown by gap on every face, through the block's back (w -1) and past both ends (z -1..61)
    box(hook, 'SubtractiveBox', 'SlotStem', '4 - Params.gap', 'Params.slot_stem', 62,
        -11, '-10 - Params.slot_stem / 2', -1)
    box(hook, 'SubtractiveBox', 'SlotHead', '3 + 2 * Params.gap', 'Params.slot_head', 62,
        '-7 - Params.gap', '-10 - Params.slot_head / 2', -1)
    rail = d.addObject('PartDesign::Body', 'Rail')
    box(rail, 'AdditiveBox', 'Base', 4, 24, 80, -14, -22, 0)
    box(rail, 'AdditiveBox', 'RibStem', 3, 'Params.rib_stem', 80, -10, '-10 - Params.rib_stem / 2', 0)
    box(rail, 'AdditiveBox', 'RibHead', 3, 'Params.rib_head', 80, -7, '-10 - Params.rib_head / 2', 0)
    d.recompute()
    p = os.path.join(OUT, 'fc8-%s.FCStd' % case)
    d.saveAs(p)
    r = check_shapes(hook.Shape, rail.Shape)
    r.update({'file': p, 'gap': gap, 'slot_head': s.get('slot_head'), 'valid': [hook.isValid(), rail.isValid()]})
    FreeCAD.closeDocument(d.Name)
    return r


def head_walls(shape, xlo=-7.2, xhi=-3.8):
    """y of the planar faces whose normal is along y and whose centre sits in the T's head band (x -7..-4)."""
    ys = []
    for f in shape.Faces:
        n = f.normalAt(0, 0)
        c = f.CenterOfMass
        if abs(abs(n.y) - 1) < 1e-9 and xlo < c.x < xhi and -19.9 < c.y < 1.9:
            ys.append(round(c.y, 6))
    return sorted(set(ys))


def check_shapes(hs, rs):
    com = hs.common(rs)
    sw, rw = head_walls(hs), head_walls(rs)
    r = {'hook_mm3': round(hs.Volume, 4), 'rail_mm3': round(rs.Volume, 4),
         'common_mm3': round(com.Volume, 4), 'common_solids': len(com.Solids),
         'hook_bbox': [round(v, 4) for v in (hs.BoundBox.XMin, hs.BoundBox.YMin, hs.BoundBox.ZMin,
                                              hs.BoundBox.XMax, hs.BoundBox.YMax, hs.BoundBox.ZMax)],
         'slot_head_walls_y': sw, 'rib_head_walls_y': rw, 'min_distance_mm': round(hs.distToShape(rs)[0], 6)}
    if len(sw) == 2 and len(rw) == 2:
        r['head_side_mm'] = {'left': round(rw[0] - sw[0], 6), 'right': round(sw[1] - rw[1], 6)}
    return r


def check(doc_path, out):
    """Hook and rail as placed: the bodies' shapes moved by any Assembly link that shows them."""
    d = FreeCAD.openDocument(doc_path)
    d.recompute()
    bodies = [o for o in d.Objects if o.TypeId == 'PartDesign::Body']
    links = [o for o in d.Objects if o.TypeId == 'App::Link']
    r = {'doc': doc_path, 'objects': [(o.Name, o.Label, o.TypeId) for o in d.Objects][:80],
         'bodies': {b.Label: round(b.Shape.Volume, 4) for b in bodies}}

    def placed(label_part):
        for ln in links:
            t = ln.getLinkedObject(True)
            if t is not None and label_part.lower() in (t.Label + t.Name).lower():
                return ln.Shape.copy(), ln.Name
        for b in bodies:
            if label_part.lower() in (b.Label + b.Name).lower():
                return b.Shape.copy(), b.Name
        return None, None

    hs, hn = placed('hook')
    rs, rn = placed('rail')
    r['used'] = [hn, rn]
    if hs is not None and rs is not None:
        r.update(check_shapes(hs, rs))
    sheets = [o for o in d.Objects if o.TypeId == 'Spreadsheet::Sheet']
    for s in sheets:
        r['sheet_' + s.Name] = {a: s.get(a) for a in ('gap', 'rib_head', 'slot_head', 'rib_stem', 'slot_stem')
                                if s.getCellFromAlias(a)}
    joints = []
    for o in d.Objects:
        if hasattr(o, 'JointType') or hasattr(o, 'ObjectToGround'):
            joints.append({k: str(getattr(o, k, None))[:120] for k in ('Name', 'Label', 'JointType', 'ObjectToGround',
                                                                       'Reference1', 'Reference2', 'Activated')})
    r['joints'] = joints
    json.dump(r, open(out, 'w'), indent=1)
    log('check', json.dumps({k: r.get(k) for k in ('common_mm3', 'head_side_mm', 'used', 'bodies')}))


def asm():
    """G0a: Assembly by Python on the typo file."""
    import JointObject
    import UtilsAssembly  # noqa: F401
    r = {}
    d = FreeCAD.openDocument(os.path.join(OUT, 'fc8-typo.FCStd'))
    hook, rail = d.getObject('Hook'), d.getObject('Rail')
    a = d.addObject('Assembly::AssemblyObject', 'Assembly')
    jg = a.newObject('Assembly::JointGroup', 'Joints')
    rl = a.newObject('App::Link', 'RailLink')
    rl.LinkedObject = rail
    hl = a.newObject('App::Link', 'HookLink')
    hl.LinkedObject = hook
    d.recompute()
    g = jg.newObject('App::FeaturePython', 'GroundedJoint')
    JointObject.GroundedJoint(g, rl)
    j = jg.newObject('App::FeaturePython', 'Slider')
    JointObject.Joint(j, 3)
    tried = []
    for form, refs in (('whole bodies, subs "RailLink."', [[a, ['RailLink.', 'RailLink.']], [a, ['HookLink.', 'HookLink.']]]),
                       ('whole bodies, links', [[rl, ['', '']], [hl, ['', '']]])):
        try:
            j.Proxy.setJointConnectors(j, refs)
            tried.append([form, 'ok', str(j.Reference1)[:120], str(j.Reference2)[:120]])
            break
        except Exception as e:
            tried.append([form, 'error %s' % e])
    r['slider_refs_tried'] = tried
    hl.Placement = FreeCAD.Placement(V(0, 0, 85), FreeCAD.Rotation())
    res = a.solve()
    r['after_raise_85'] = {'solve': res, 'hook_link_base': list(hl.Placement.Base), 'rot': list(hl.Placement.Rotation.Q),
                           'common_mm3': round(hl.Shape.common(rl.Shape).Volume, 4)}
    for z in (40, 0, -30):
        hl.Placement = FreeCAD.Placement(V(0, 0, z), FreeCAD.Rotation())
        res = a.solve()
        r['moved_to_z_%d' % z] = {'solve': res, 'hook_link_base': [round(v, 6) for v in hl.Placement.Base],
                                  'common_mm3': round(hl.Shape.common(rl.Shape).Volume, 4)}
    # off the line: x 3 (into the rail's base): the slider pulls it back (or not)
    hl.Placement = FreeCAD.Placement(V(3, 1, 20), FreeCAD.Rotation())
    res = a.solve()
    r['pushed_off_line_x3_y1'] = {'solve': res, 'hook_link_base': [round(v, 6) for v in hl.Placement.Base]}
    d.saveAs(os.path.join(OUT, 'fc8-typo-asm.FCStd'))
    json.dump(r, open(os.path.join(OUT, 'asm.json'), 'w'), indent=1)
    log('asm', json.dumps(r)[:900])


def edge_near(shape, pt):
    """The edge a click at pt picks: the edge of shape nearest to pt."""
    return min(shape.Edges, key=lambda e: e.distToShape(Part.Vertex(pt))[0])


def ladder():
    """Video D probe P2: rungs gap02/gap03 built (if missing) next to fc8's files in /lab/out/fc8/P; then on all six rungs
    the Intersection volume, the head walls each side, distToShape hook-rail (ground truth) and the GUI's Measure picks
    (the slot's wall edge + the rib's wall edge at z 0, x -5.5, as take D) -> OUT/ladder.json."""
    P = '/lab/out/fc8/P'
    res = {}
    for case in ('gap02', 'gap03'):
        if not os.path.exists(os.path.join(P, 'fc8-%s.FCStd' % case)):
            global OUT
            o, OUT = OUT, P
            build(case)
            OUT = o
    for case in ('typo', 'touch', 'gap01', 'gap02', 'gap03', 'gap04'):
        d = FreeCAD.openDocument(os.path.join(P, 'fc8-%s.FCStd' % case))
        d.recompute()
        hs, rs = d.getObject('Hook').Shape, d.getObject('Rail').Shape
        r = check_shapes(hs, rs)
        sh = d.getObject('Params').get('slot_head')
        r['slot_head'] = sh
        dts = hs.distToShape(rs)
        r['nearest_points'] = [[[round(c, 4) for c in p] for p in pr] for pr in dts[1][:4]]
        r['gui_picks_mm'] = {}
        for side, sg in (('left', -1), ('right', 1)):
            he = edge_near(hs, V(-5.5, -10 + sg * sh / 2, 0))
            re_ = edge_near(rs, V(-5.5, -10 + sg * 6, 0))
            r['gui_picks_mm'][side] = round(he.distToShape(re_)[0], 6)
        res[case] = r
        FreeCAD.closeDocument(d.Name)
        log('ladder', case, json.dumps({k: r.get(k) for k in ('common_mm3', 'min_distance_mm', 'head_side_mm', 'gui_picks_mm')}))
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(os.path.join(OUT, 'ladder.json'), 'w'), indent=1)


if MODE == 'build':
    os.makedirs(OUT, exist_ok=True)
    allr = {c: build(c) for c in CASES}
    json.dump(allr, open(os.path.join(OUT, 'build.json'), 'w'), indent=1)
    log('build', json.dumps({c: (v['hook_mm3'], v['common_mm3'], v.get('head_side_mm')) for c, v in allr.items()}))
elif MODE == 'ladder':
    ladder()
elif MODE == 'asm':
    asm()
elif MODE == 'check':
    check(os.environ['FC8_DOC'], OUT)
