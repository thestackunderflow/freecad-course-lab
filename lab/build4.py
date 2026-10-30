"""Lesson 4's hook built headless, never filmed as a step (lab L4-Q3, L4-Q7): lesson 3's hook (FC_IN) with the same
two names, the same sketch attached to the back face (Face8, FlatFace, as the by-hand take's Create sketch made it),
the same Hole (Diameter = hole_d, through all) and the same 2 mm fillet on the lip's top outer edge as the by-hand take.
PLAIN=1: the circles' centres typed as plain numbers (10 across; 15 and 45 up) = the watch-only plain hook; otherwise
written from the names (width / 2; (plate_height -+ hole_spacing) / 2), as by hand.
    FC_IN=hook-lesson3.FCStd FC_OUT=hook-plain.FCStd PLAIN=1 freecadcmd /lab/lab/build4.py"""
import os

import FreeCAD as App
import Part
import Sketcher

d = App.openDocument(os.environ['FC_IN'])
d.recompute()
ss, body, pad = d.getObject('Spreadsheet'), d.getObject('Body'), d.getObject('Pad')
ss.set('A6', 'hole_d'); ss.set('B6', '4 mm'); ss.setAlias('B6', 'hole_d')
ss.set('A7', 'hole_spacing'); ss.set('B7', '30 mm'); ss.setAlias('B7', 'hole_spacing')
d.recompute()
back = [i for i, f in enumerate(pad.Shape.Faces) if abs(f.normalAt(0, 0).x + 1) < 1e-6 and abs(f.CenterOfMass.x) < 1e-6]
sk = body.newObject('Sketcher::SketchObject', 'Sketch001')
sk.AttachmentSupport = [(pad, 'Face%d' % (back[0] + 1))]
sk.MapMode = 'FlatFace'
d.recompute()
for y in (15, 45):
    g = sk.addGeometry(Part.Circle(App.Vector(10, y, 0), App.Vector(0, 0, 1), 2), False)
    sk.addConstraint(Sketcher.Constraint('Diameter', g, 4))
    cx = sk.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, g, 3, 10))
    cy = sk.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, g, 3, y))
    if os.environ.get('PLAIN') != '1':
        sk.setExpression('Constraints[%d]' % cx, 'Spreadsheet.width / 2')
        sk.setExpression('Constraints[%d]' % cy, '(Spreadsheet.plate_height %s Spreadsheet.hole_spacing) / 2'
                         % ('-' if y == 15 else '+'))
hole = body.newObject('PartDesign::Hole', 'Hole')
hole.Profile = sk
hole.DepthType = 'ThroughAll'
hole.setExpression('Diameter', 'Spreadsheet.hole_d')
sk.Visibility = False
d.recompute()
lip = [i for i, e in enumerate(hole.Shape.Edges)
       if {round(v.X, 3) for v in e.Vertexes} == {40.0} and {round(v.Z, 3) for v in e.Vertexes} == {10.0}]
fil = body.newObject('PartDesign::Fillet', 'Fillet')
fil.Base = (hole, ['Edge%d' % (lip[0] + 1)])
fil.Radius = 2
hole.Visibility = False
d.recompute()
print('built hook', 'plain' if os.environ.get('PLAIN') == '1' else 'names', sk.AttachmentSupport, round(body.Shape.Volume, 4), [round(c.Value, 3) for c in sk.Constraints], sk.solve())
d.saveAs(os.environ['FC_OUT'])
