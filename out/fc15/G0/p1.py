import FreeCAD
d=FreeCAD.openDocument('/lab/out/fc14/P/peg-fixed.FCStd'); d.recompute()
b=d.getObject('Body'); print('FC15', [o.Name for o in b.Group], b.Tip.Name, d.getObject('Params').getContents('A1') if 0 else '')
s=b.Shape
for i,e in enumerate(s.Edges):
    if all(abs(v.Point.z-50)<1e-6 for v in e.Vertexes): print('FC15 E%d'%(i+1), e.Curve.__class__.__name__, [tuple(round(c,2) for c in v.Point) for v in e.Vertexes])
for i,f in enumerate(s.Faces):
    if abs(f.BoundBox.ZMin-50)<1e-6 and abs(f.BoundBox.ZMax-50)<1e-6: print('FC15 F%d'%(i+1), f.Surface.__class__.__name__, len(f.Edges))
