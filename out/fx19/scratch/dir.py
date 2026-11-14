import FreeCAD
d=FreeCAD.newDocument('x'); s=d.addObject('Sketcher::SketchObject','S')
print('DIR', [n for n in dir(s) if 'move' in n.lower() or 'dof' in n.lower() or 'solve' in n.lower()])
print('DOC', s.moveGeometry.__doc__ if hasattr(s,'moveGeometry') else None)
