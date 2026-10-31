"""Lesson 6: read one saved FreeCAD document after a change (no AI, no GUI), for the must-stay-true list.
    FC_DOC=/path/part.FCStd FC_OUT=/path/read.json freecadcmd /lab/checker/l6read.py
(freecadcmd passes no script arguments through, so the paths come from the environment.)

The part = the last PartDesign Body whose shape has a solid (a document can hold more than one: `bodies` lists them).
Read, all relative to the part's own box (a moved part breaks nothing):
  opening   : a line across the gap at 7.5 mm up, 3 mm in from the side (clear of the holes): the gap between the
              first two solid stretches (the plate and the lip)
  points    : isInside at fixed spots: 0.1 mm inside / outside each wall's inner face (plate at 30 up, base at the
              middle of the gap, lip at 7.5 up), the lip's top (9.9 / 10.1 up, 2.5 mm in from the front)
  solid     : the measure.py row of the part (volume, box, min/max, round faces) for checker/holes.check
  errors    : objects whose State says Invalid or Error; isValid(); the number of solids
  stl       : the Body exported with Mesh.export (FreeCAD's own mesher, default settings): closed, components
  names     : every spreadsheet's aliases and values; every expression (object, property, text)
  drive     : on the same document after the read: the alias `width` set to 20 mm, recompute, the part's box and
              round faces again (the names still drive the part when it follows)
"""
import json
import os

import FreeCAD
import Part

doc = FreeCAD.openDocument(os.environ['FC_DOC'])
# no recompute here: the shapes are read as the run left them (a run that never recomputed is read as it is)


def vec(v):
    return [round(v.x, 6) + 0.0, round(v.y, 6) + 0.0, round(v.z, 6) + 0.0]


def part_of(d):
    bodies = [o for o in d.Objects if o.TypeId == 'PartDesign::Body' and not o.Shape.isNull() and o.Shape.Solids]
    if bodies:
        return bodies[-1], [o.Name for o in bodies]
    roots = [o for o in d.Objects if getattr(o, 'Shape', None) is not None and not o.Shape.isNull() and o.Shape.Solids
             and not [x for x in o.InList if getattr(x, 'Shape', None) is not None and x.Shape.Solids]]
    return (roots[-1] if roots else None), []


def local(o):
    """The part's shape in its own coordinates: a Body's (or part's) Placement undone, so a moved or turned part is
    read like the start part."""
    shp = o.Shape.copy()
    shp.Placement = FreeCAD.Placement()
    return shp


def solid_row(o):
    shp = local(o)
    b = shp.BoundBox
    return {'name': o.Name, 'label': o.Label, 'type': o.TypeId, 'volume_mm3': round(shp.Volume, 4),
            'valid': shp.isValid(), 'solids': len(shp.Solids),
            'bbox_mm': [round(b.XLength, 4), round(b.YLength, 4), round(b.ZLength, 4)],
            'min_mm': [round(b.XMin, 4) + 0.0, round(b.YMin, 4) + 0.0, round(b.ZMin, 4) + 0.0],
            'max_mm': [round(b.XMax, 4) + 0.0, round(b.YMax, 4) + 0.0, round(b.ZMax, 4) + 0.0],
            'cylinders': [{'r': round(f.Surface.Radius, 4), 'axis': vec(f.Surface.Axis),
                           'center': vec(f.Surface.Center), 'area': round(f.Area, 3)}
                          for f in shp.Faces if 'Cylinder' in f.Surface.TypeId]}


def geometry(shp):
    b = shp.BoundBox
    x0, x1, y0, z0 = b.XMin, b.XMax, b.YMin, b.ZMin
    y = y0 + 3.0
    line = Part.LineSegment(FreeCAD.Vector(x0 - 1, y, z0 + 7.5), FreeCAD.Vector(x1 + 1, y, z0 + 7.5)).toShape()
    segs = sorted([(round(min(v.X for v in e.Vertexes) - x0, 4) + 0.0, round(max(v.X for v in e.Vertexes) - x0, 4) + 0.0)
                   for e in shp.common(line).Edges])
    opening = round(segs[1][0] - segs[0][1], 4) if len(segs) >= 2 else None
    mid = (x0 + 5.0 + x1 - 5.0) / 2.0

    def inside(x, z):
        return bool(shp.isInside(FreeCAD.Vector(x, y, z), 1e-6, True))
    pts = {
        'plate_in': inside(x0 + 4.9, z0 + 30), 'plate_out': inside(x0 + 5.1, z0 + 30),
        'base_in': inside(mid, z0 + 4.9), 'base_out': inside(mid, z0 + 5.1),
        'lip_in': inside(x1 - 4.9, z0 + 7.5), 'lip_out': inside(x1 - 5.1, z0 + 7.5),
        'lip_top_in': inside(x1 - 2.5, z0 + 9.9), 'lip_top_out': inside(x1 - 2.5, z0 + 10.1),
    }
    return {'segments_x_at_7_5': segs, 'opening_mm': opening, 'points': pts}


def errors(d):
    """Objects in an error state; FreeCAD's own Measure rows (Measure::*) are left out (our filmed check adds one)."""
    return [o.Name for o in d.Objects if any(s in ('Invalid', 'Error') for s in (o.State or []))
            and not o.TypeId.startswith('Measure::')]


def sheets(d):
    out = []
    for o in d.Objects:
        if o.TypeId != 'Spreadsheet::Sheet':
            continue
        al = {}
        for cell in o.getUsedCells():
            a = o.getAlias(cell)
            if a:
                v = o.get(cell)
                al[a] = round(float(v.Value), 6) if hasattr(v, 'Value') else (v if isinstance(v, (int, float)) else str(v))
        out.append({'name': o.Name, 'label': o.Label, 'aliases': al})
    return out


def stl(o, path):
    import Mesh
    try:
        Mesh.export([o], path)
        m = Mesh.Mesh(path)
        return {'triangles': m.CountFacets, 'closed': bool(m.isSolid()), 'components': m.countComponents(),
                'non_manifolds': bool(m.hasNonManifolds()), 'volume_mm3': round(m.Volume, 3)}
    except Exception as e:   # noqa: BLE001
        return {'error': repr(e)}


part, bodies = part_of(doc)
res = {'document': os.path.basename(os.environ['FC_DOC']), 'freecad': '.'.join(FreeCAD.Version()[:3]),
       'objects': [o.Name for o in doc.Objects], 'bodies': bodies, 'part': None}
if part is not None:
    res['part'] = part.Name
    res['solid'] = solid_row(part)
    res['geometry'] = geometry(local(part))
    res['placement'] = str(part.Placement)
    res['moved'] = not part.Placement.isIdentity()
    res['errors'] = errors(doc)
    res['stl'] = stl(part, os.environ['FC_OUT'] + '.stl')
    res['tip'] = part.Tip.Name if getattr(part, 'Tip', None) else None
res['sheets'] = sheets(doc)
res['expressions'] = [{'object': o.Name, 'property': k, 'expression': e} for o in doc.Objects
                      for k, e in getattr(o, 'ExpressionEngine', [])]
# the drive test (last: it changes the document in memory; nothing is saved)
drive = {'done': False}
def sheet_with(alias):
    ws = [o for o in doc.Objects if o.TypeId == 'Spreadsheet::Sheet' and alias in [o.getAlias(c) for c in o.getUsedCells()]]
    return ws[-1] if ws else None


ws = sheet_with('width')
if part is not None and ws:
    ws.set('width', '20 mm')
    doc.recompute()
    drive = {'done': True, 'solid': solid_row(part), 'errors': errors(doc)}
res['drive'] = drive
# the second drive test: hook_depth + 5 (the width back to its value first): the part's depth must follow by 5
drive2 = {'done': False}
hs = sheet_with('hook_depth')
if part is not None and hs and ws:
    ws.set('width', '%s mm' % res['solid']['bbox_mm'][1])
    v = hs.get('hook_depth')
    hs.set('hook_depth', '%g mm' % (float(v.Value if hasattr(v, 'Value') else v) + 5))
    doc.recompute()
    drive2 = {'done': True, 'solid': solid_row(part), 'errors': errors(doc), 'geometry': geometry(local(part))}
res['drive_depth'] = drive2
with open(os.environ['FC_OUT'], 'w') as f:
    json.dump(res, f, indent=1)
print(json.dumps({k: res.get(k) for k in ('part', 'geometry')}))
