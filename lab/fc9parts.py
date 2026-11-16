"""fc9 (FreeCAD course lesson 9, LinearPattern coat rack), lab instrument run by freecadcmd, never filmed.

    FC9_OUT=/lab/out/fc9/P FC9_MODE=build freecadcmd /lab/lab/fc9parts.py
        rack-start.FCStd (the take / Claude start file: one hook on the 180 strip, spreadsheet Params) and one file per
        case (trap, fix, proof, control, yourturn) with a LinearPattern made by code; every number read back by code
        -> build.json.
    FC9_DOC=x.FCStd FC9_OUT=y.json FC9_MODE=check freecadcmd /lab/lab/fc9parts.py
        any saved file (a take's, a Claude run's): hooks, end gaps, air between hooks, solids, pattern settings -> y.json.
Coordinates: the strip runs along X from 0 to rack_width, y 0..5, z 0..60; hooks stand out to -Y, toward a person's
isometric view (lesson 3 profile in the YZ plane: plate y -5..0 z 0..60, arm to y -25, lip y -25..-20 z 5..10), each `width` long in X from x = margin."""
import json
import os
import sys

import FreeCAD
import Part
import Sketcher

OUT = os.environ.get('FC9_OUT', '/lab/out/fc9/P')
MODE = os.environ.get('FC9_MODE', 'build')
V = FreeCAD.Vector
PROFILE = [(0, 0), (-25, 0), (-25, 10), (-20, 10), (-20, 5), (-5, 5), (-5, 60), (0, 60)]   # u = global Y


def log(*a):
    print('FC9', *a)
    sys.stdout.flush()


def origin(body, role):
    return [o for o in body.Origin.OriginFeatures if o.Role == role][0]


def start_doc(name, rack_width=180, hooks=5):
    d = FreeCAD.newDocument(name)
    s = d.addObject('Spreadsheet::Sheet', 'Params')
    for i, (n, v) in enumerate((('rack_width', rack_width), ('width', 20), ('margin', 20), ('hooks', hooks)), 1):
        s.set('A%d' % i, n)
        s.set('B%d' % i, str(v))
        s.setAlias('B%d' % i, n)
    d.recompute()
    b = d.addObject('PartDesign::Body', 'Body')
    b.Label = 'Rack'
    # the strip: a rectangle on XY, x 0..rack_width, y 0..5, padded 60 up
    sk = b.newObject('Sketcher::SketchObject', 'StripSketch')
    sk.AttachmentSupport = [(origin(b, 'XY_Plane'), '')]
    sk.MapMode = 'FlatFace'
    pts = [V(0, 0, 0), V(180, 0, 0), V(180, 5, 0), V(0, 5, 0)]
    for i in range(4):
        sk.addGeometry(Part.LineSegment(pts[i], pts[(i + 1) % 4]))
    for i in range(4):
        sk.addConstraint(Sketcher.Constraint('Coincident', i, 2, (i + 1) % 4, 1))
    sk.addConstraint(Sketcher.Constraint('Horizontal', 0))
    sk.addConstraint(Sketcher.Constraint('Horizontal', 2))
    sk.addConstraint(Sketcher.Constraint('Vertical', 1))
    sk.addConstraint(Sketcher.Constraint('Vertical', 3))
    sk.addConstraint(Sketcher.Constraint('Coincident', 0, 1, -1, 1))       # corner (0, 0) on the origin
    c = sk.addConstraint(Sketcher.Constraint('DistanceX', 0, 1, 0, 2, 180))
    sk.renameConstraint(c, 'rack')
    sk.setExpression('.Constraints.rack', 'Params.rack_width')
    sk.addConstraint(Sketcher.Constraint('DistanceY', 1, 1, 1, 2, 5))
    strip = b.newObject('PartDesign::Pad', 'Strip')
    strip.Profile = sk
    strip.Length = 60
    # the hook: lesson 3's profile on the YZ plane, moved `margin` along X, padded `width`
    hk = b.newObject('Sketcher::SketchObject', 'HookSketch')
    hk.AttachmentSupport = [(origin(b, 'YZ_Plane'), '')]
    hk.MapMode = 'FlatFace'
    hk.setExpression('.AttachmentOffset.Base.z', 'Params.margin')
    for i in range(len(PROFILE)):
        a, c2 = PROFILE[i], PROFILE[(i + 1) % len(PROFILE)]
        hk.addGeometry(Part.LineSegment(V(a[0], a[1], 0), V(c2[0], c2[1], 0)))
    for i in range(len(PROFILE)):
        hk.addConstraint(Sketcher.Constraint('Block', i))
    hook = b.newObject('PartDesign::Pad', 'Hook')
    hook.Profile = hk
    hook.setExpression('Length', 'Params.width')
    d.recompute()
    return d, b, hook


def add_pattern(d, b, hook, length=None, occ=None, length_expr=None, occ_expr=None):
    p = b.newObject('PartDesign::LinearPattern', 'LinearPattern')
    p.Originals = [hook]
    p.Direction = (origin(b, 'X_Axis'), [''])
    p.Mode = 'Extent'
    if length_expr:
        p.setExpression('Length', length_expr)
    else:
        p.Length = length
    if occ_expr:
        p.setExpression('Occurrences', occ_expr)
    else:
        p.Occurrences = occ
    b.Tip = p
    d.recompute()
    return p


def measure(shape):
    """hooks = solids of the shape in y < -0.5; strip = the part in y > 0.5; gaps from the strip's ends; a hook whose x
    range misses the strip is counted as floating."""
    bb = shape.BoundBox
    big = 2000
    front = shape.common(Part.makeBox(2 * big, 200, 400, V(-big, -200.5, -200)))
    back = shape.common(Part.makeBox(2 * big, 200, 400, V(-big, 0.5, -200)))
    hx = sorted([round(s.BoundBox.XMin, 6), round(s.BoundBox.XMax, 6)] for s in front.Solids)
    r = {'volume_mm3': round(shape.Volume, 4), 'solids': len(shape.Solids), 'hooks': len(hx), 'hook_x': hx,
         'bbox': [round(v, 4) for v in (bb.XMin, bb.YMin, bb.ZMin, bb.XMax, bb.YMax, bb.ZMax)]}
    if back.Solids:
        sx = [round(back.BoundBox.XMin, 6), round(back.BoundBox.XMax, 6)]
        r['strip_x'] = sx
        on = [h for h in hx if h[1] > sx[0] + 1e-6 and h[0] < sx[1] - 1e-6]
        r['hooks_on_strip'] = len(on)
        r['floating'] = [h for h in hx if h not in on]
        if on:
            r['left_gap_mm'] = round(on[0][0] - sx[0], 6)
            r['right_gap_mm'] = round(sx[1] - on[-1][1], 6)
            r['air_mm'] = [round(hx[i + 1][0] - hx[i][1], 6) for i in range(len(hx) - 1)]
            r['starts'] = [h[0] for h in hx]
    return r


def pattern_info(d):
    out = []
    for o in d.Objects:
        if o.TypeId == 'PartDesign::LinearPattern':
            out.append({'name': o.Name, 'mode': o.Mode, 'length_mm': round(o.Length.Value, 6),
                        'occurrences': o.Occurrences, 'originals': [x.Name for x in o.Originals],
                        'expressions': [list(e) for e in o.ExpressionEngine], 'valid': o.isValid(),
                        'status': o.getStatusString() if hasattr(o, 'getStatusString') else ''})
    return out


CASES = {  # name: (rack_width, hooks, length, occ, length_expr, occ_expr)
    'trap': (180, 5, 180, 5, None, None),
    'fix': (180, 5, 120, 5, None, None),
    'proof': (220, 6, None, None, 'Params.rack_width - 2 * Params.margin - Params.width', 'Params.hooks'),
    'control': (220, 6, 120, 6, None, None),
    'yourturn': (140, 3, None, None, 'Params.rack_width - 2 * Params.margin - Params.width', 'Params.hooks'),
    'trap_nocompound': (180, 5, 180, 5, None, None),   # the trap with the Body's AllowCompound off (not the default)
}


def build():
    os.makedirs(OUT, exist_ok=True)
    allr = {}
    d, b, hook = start_doc('rack')
    p = os.path.join(OUT, 'rack-start.FCStd')
    d.saveAs(p)
    allr['start'] = dict(measure(b.Shape), file=p, valid=b.isValid(), allow_compound=b.AllowCompound)
    FreeCAD.closeDocument(d.Name)
    for name, (w, n, L, occ, le, oe) in CASES.items():
        d, b, hook = start_doc('rack_' + name, w, n)
        if name.endswith('nocompound'):
            b.AllowCompound = False
        pat = add_pattern(d, b, hook, L, occ, le, oe)
        p = os.path.join(OUT, 'rack-%s.FCStd' % name)
        d.saveAs(p)
        r = measure(b.Shape)
        r.update({'file': p, 'length_mm': round(pat.Length.Value, 6), 'occurrences': pat.Occurrences,
                  'pattern': pattern_info(d), 'rack_width': w, 'allow_compound': b.AllowCompound})
        allr[name] = r
        FreeCAD.closeDocument(d.Name)
    json.dump(allr, open(os.path.join(OUT, 'build.json'), 'w'), indent=1)
    log('build', json.dumps({k: (v['hooks'], v.get('left_gap_mm'), v.get('right_gap_mm')) for k, v in allr.items()}))


def result_shape(d):
    """what a person sees: each Body's shape, plus visible solids outside bodies that nothing else uses."""
    shapes, used = [], []
    in_body = set()
    for b in [o for o in d.Objects if o.TypeId == 'PartDesign::Body']:
        in_body.update(x.Name for x in b.Group)
        if b.Shape.Solids:
            shapes.append(b.Shape)
            used.append(b.Name)
    for o in d.Objects:
        if o.Name in in_body or o.TypeId == 'PartDesign::Body' or not hasattr(o, 'Shape'):
            continue
        if getattr(o, 'Visibility', False) and o.Shape.Solids and not [x for x in o.InList if x.TypeId != 'App::Part']:
            shapes.append(o.Shape)
            used.append(o.Name)
    if not shapes:
        return None, used
    s = shapes[0]
    for x in shapes[1:]:
        s = s.fuse(x)
    return s, used


def check(doc_path, out):
    d = FreeCAD.openDocument(doc_path)
    d.recompute()
    s, used = result_shape(d)
    r = {'doc': doc_path, 'objects': [(o.Name, o.Label, o.TypeId) for o in d.Objects][:80], 'used': used,
         'bodies': len([o for o in d.Objects if o.TypeId == 'PartDesign::Body']), 'pattern': pattern_info(d)}
    if s is not None:
        r.update(measure(s))
    for sh in [o for o in d.Objects if o.TypeId == 'Spreadsheet::Sheet']:
        r['sheet_' + sh.Name] = {a: sh.get(a) for a in ('rack_width', 'width', 'margin', 'hooks')
                                 if sh.getCellFromAlias(a)}
    json.dump(r, open(out, 'w'), indent=1)
    log('check', json.dumps({k: r.get(k) for k in ('hooks', 'left_gap_mm', 'right_gap_mm', 'solids', 'used')}))


if MODE == 'build':
    build()
elif MODE == 'check':
    check(os.environ['FC9_DOC'], OUT)
