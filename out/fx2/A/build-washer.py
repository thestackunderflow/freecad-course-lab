import FreeCAD as App, Part
doc = App.newDocument("washer")
obj = doc.addObject("Part::Feature", "washer")
obj.Shape = Part.makeCylinder(2.5, 0.3).cut(Part.makeCylinder(1.1, 0.3))
doc.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.Selection.addSelection(obj)
