import FreeCAD
d = FreeCAD.openDocument('/lab/out/fc16/P/hole-start.FCStd'); d.recompute()
b = d.getObject('Body'); s = b.Tip.Shape
print('PX tip', b.Tip.Name, [list(o.State) for o in b.Group if o.TypeId.startswith('PartDesign::')])
for i, f in enumerate(s.Faces, 1):
    bb = f.BoundBox
    if bb.YMin > 19: print('PX', i, f.Surface.TypeId, [round(v, 3) for v in (bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax)])
for w in (3, 4, 12):
    d.getObject('Params').set('wall', str(w)); d.recompute()
    for o in b.Group:
        if o.TypeId.startswith('PartDesign::'): o.touch()
    d.recompute()
    print('PX wall', w, [(o.Name, list(o.State), o.getStatusString()) for o in b.Group if o.TypeId.startswith('PartDesign::') and list(o.State)])
