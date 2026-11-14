import FreeCAD
d = FreeCAD.openDocument('/lab/out/l2/hand/hand.FCStd')
for o in d.Objects: print(o.Name, o.TypeId, o.Label)
s = [o for o in d.Objects if o.TypeId == 'Sketcher::SketchObject'][0]
for i, g in enumerate(s.Geometry): print('G', i, type(g).__name__, g.StartPoint, g.EndPoint)
for i, c in enumerate(s.Constraints): print('C', i, c.Type, c.First, c.FirstPos, c.Second, c.SecondPos, c.Value, c.Name)
