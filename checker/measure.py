"""(From the screen-lab kit's apps/freecad/measure.py, plus the corner position min_mm; lesson 2: which objects use each
solid, the sketches and the bodies' recipe.) The one measuring line for every part in the course, by hand, by Claude
or by the replay.
Measure a saved FreeCAD document headlessly (no GUI): every solid's volume, bounding box and validity; every sketch's
plane, placement, constraints and whether it is fully constrained; every Part Design body's features in order.
    FC_DOC=/path/part.FCStd FC_OUT=/path/measure.json freecadcmd /lab/checker/measure.py
(freecadcmd passes no script arguments through, so the paths come from the environment.)"""
import json
import os

import FreeCAD

doc = FreeCAD.openDocument(os.environ['FC_DOC'])
doc.recompute()


def vec(v):
    return [round(v.x, 6) + 0.0, round(v.y, 6) + 0.0, round(v.z, 6) + 0.0]


rows = []
for o in doc.Objects:
    shp = getattr(o, 'Shape', None)
    if shp is None or shp.isNull() or not shp.Solids:
        continue
    b = shp.BoundBox
    rows.append({'name': o.Name, 'label': o.Label, 'type': o.TypeId, 'volume_mm3': round(shp.Volume, 4),
                 'valid': shp.isValid(), 'solids': len(shp.Solids),
                 'bbox_mm': [round(b.XLength, 4), round(b.YLength, 4), round(b.ZLength, 4)],
                 'z_range_mm': [round(b.ZMin, 4) + 0.0, round(b.ZMax, 4) + 0.0],
                 'min_mm': [round(b.XMin, 4) + 0.0, round(b.YMin, 4) + 0.0, round(b.ZMin, 4) + 0.0],
                 'max_mm': [round(b.XMax, 4) + 0.0, round(b.YMax, 4) + 0.0, round(b.ZMax, 4) + 0.0],
                 'in_list': sorted(x.Name for x in o.InList if getattr(x, 'Shape', None) is not None
                                   and not x.Shape.isNull() and x.Shape.Solids)})

sketches = []
for o in doc.Objects:
    if o.TypeId != 'Sketcher::SketchObject':
        continue
    sup = getattr(o, 'AttachmentSupport', None)
    if sup is None:
        sup = getattr(o, 'Support', None)
    support = [[s[0].Name, list(s[1])] for s in (sup or [])]
    try:
        solve = o.solve()
    except Exception as e:   # noqa: BLE001
        solve = repr(e)
    fc = getattr(o, 'FullyConstrained', None)
    try:
        free = len(o.getGeometryWithDependentParameters())
    except Exception:   # noqa: BLE001
        free = None
    kinds = {}
    for c in o.Constraints:
        kinds[c.Type] = kinds.get(c.Type, 0) + 1
    r = o.getGlobalPlacement().Rotation if hasattr(o, 'getGlobalPlacement') else o.Placement.Rotation
    sketches.append({'name': o.Name, 'label': o.Label, 'support': support, 'map_mode': getattr(o, 'MapMode', None),
                     'geometry': o.GeometryCount if hasattr(o, 'GeometryCount') else len(o.Geometry),
                     'constraints': len(o.Constraints), 'constraint_kinds': kinds, 'solve': solve,
                     'fully_constrained': fc, 'dependent_parameters': free,
                     'normal': vec(r.multVec(FreeCAD.Vector(0, 0, 1))),
                     'up_vector': vec(r.multVec(FreeCAD.Vector(0, 1, 0))),
                     'right_vector': vec(r.multVec(FreeCAD.Vector(1, 0, 0))),
                     'placement': str(o.Placement)})

bodies = []
for o in doc.Objects:
    if o.TypeId == 'PartDesign::Body':
        feats = []
        for f in o.Group:
            d = {'name': f.Name, 'label': f.Label, 'type': f.TypeId}
            if f.TypeId == 'PartDesign::Pad':
                d.update({'length': float(f.Length), 'reversed': bool(f.Reversed), 'pad_type': str(f.Type)})
            feats.append(d)
        bodies.append({'name': o.Name, 'label': o.Label, 'tip': o.Tip.Name if o.Tip else None, 'features': feats,
                       'placement': str(o.Placement)})

# lesson 3: the sketch's corners and sizes (with the expression each size is written from), the spreadsheets' named
# cells, and each pad's length and expression
DIMS = ('Distance', 'DistanceX', 'DistanceY', 'Radius', 'Diameter', 'Angle')
for s in sketches:
    o = doc.getObject(s['name'])
    ee = dict(o.ExpressionEngine)
    pts = []
    for gi, g in enumerate(o.Geometry):
        if g.TypeId != 'Part::GeomLineSegment' or o.getConstruction(gi):
            continue
        for p in (g.StartPoint, g.EndPoint):
            q = [round(p.x, 4) + 0.0, round(p.y, 4) + 0.0]
            if q not in pts:
                pts.append(q)
    s['corners_xy'] = pts
    s['dimensions'] = [{'index': i, 'type': c.Type, 'name': c.Name, 'value': round(c.Value, 4),
                        'expression': next((ee[k] for k in ('Constraints[%d]' % i, '.Constraints[%d]' % i,
                                                            'Constraints.%s' % c.Name, '.Constraints.%s' % c.Name)
                                            if k in ee and (c.Name or '[' in k)), None),
                        'first': c.First, 'second': c.Second}
                       for i, c in enumerate(o.Constraints) if c.Type in DIMS]

sheets = []
for o in doc.Objects:
    if o.TypeId != 'Spreadsheet::Sheet':
        continue
    aliases, cells = {}, {}
    for cell in o.getUsedCells():
        v = o.get(cell)
        txt = str(v)
        if hasattr(v, 'Value') and hasattr(v, 'Unit'):
            txt = ('%g' % v.Value) + ((' ' + str(v).split()[-1]) if str(v.Unit) not in ('', 'Unit: ()') and ' ' in str(v) else '')
        cells[cell] = {'content': o.getContents(cell), 'value': txt}
        a = o.getAlias(cell)
        if a:
            aliases[a] = txt
    sheets.append({'name': o.Name, 'label': o.Label, 'aliases': aliases, 'cells': cells})

pads = []
for o in doc.Objects:
    if o.TypeId == 'PartDesign::Pad':
        pads.append({'name': o.Name, 'length': float(o.Length), 'expression': dict(o.ExpressionEngine).get('Length')})

res = {'document': os.path.basename(os.environ['FC_DOC']), 'freecad': '.'.join(FreeCAD.Version()[:3]),
       'objects': [o.Name for o in doc.Objects], 'solids': rows, 'sketches': sketches, 'bodies': bodies,
       'sheets': sheets, 'pads': pads,
       'expressions': [{'object': o.Name, 'property': k, 'expression': e} for o in doc.Objects
                       for k, e in getattr(o, 'ExpressionEngine', [])]}
with open(os.environ['FC_OUT'], 'w') as f:
    json.dump(res, f, indent=1)
print(json.dumps(res))
