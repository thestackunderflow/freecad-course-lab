import FreeCAD as App, Part
doc = App.newDocument("cube3")
obj = doc.addObject("Part::Feature", "cube3")
obj.Shape = Part.makeBox(3, 3, 3)
doc.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.Selection.addSelection(obj)
print(Gui.Selection.getSelection()[0].Shape.Volume)
