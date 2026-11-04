import FreeCAD as App, Part
doc = App.newDocument("block")
obj = doc.addObject("Part::Feature", "block")
obj.Shape = Part.makeBox(1, 0.5, 0.25)
doc.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.Selection.addSelection(obj)
print(Gui.Selection.getSelection()[0].Shape.Volume)
