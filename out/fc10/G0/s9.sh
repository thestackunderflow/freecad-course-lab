Q "import FreeCAD, FreeCADGui
for n in list(FreeCAD.listDocuments()): FreeCAD.closeDocument(n)
d = FreeCAD.newDocument('rect'); b = d.addObject('PartDesign::Body', 'Body')
sk = b.newObject('Sketcher::SketchObject', 'Sketch')
sk.AttachmentSupport = [([o for o in b.Origin.OriginFeatures if o.Role == 'XY_Plane'][0], '')]; sk.MapMode = 'FlatFace'
d.recompute(); FreeCADGui.activateWorkbench('PartDesignWorkbench'); FreeCADGui.ActiveDocument.setEdit(sk.Name)
print(1)" > /dev/null; sleep 3
Q "import FreeCADGui; v = FreeCADGui.ActiveDocument.ActiveView; v.viewTop(); print(1)" > /dev/null
FQ "look('rect', 'Top', 40, 30, 0, 160)" > /dev/null; sleep 1
read -r AX AY < <(vp 30 20 0); read -r BX BY < <(vp 75 55 0); echo "q5 rect corners at $AX $AY / $BX $BY" >> $L
echo "q5 rect button: $(B Sketcher_CreateRectangle)" >> $L
p=$(B Sketcher_CreateRectangle); xdotool mousemove ${p% *} ${p#* }; sleep 0.5; xdotool click 1; sleep 1
xdotool mousemove $AX $AY; sleep 0.8; xdotool click 1; sleep 0.8
for i in $(seq 1 10); do xdotool mousemove $((AX + (BX - AX) * i / 10)) $((AY + (BY - AY) * i / 10)); sleep 0.05; done
sleep 0.5; xdotool click 1; sleep 1.5; xdotool key Escape; sleep 1; xdotool mousemove 1500 300; sleep 0.5
shot $O/q5-rect.png
echo "q5 solver_text: $(solver_text)" >> $L
Q "import FreeCAD
s = FreeCAD.getDocument('rect').getObject('Sketch')
print('q5 drawn', len(s.Geometry), 'geos', [c.Type for c in s.Constraints], 'DoF', s.DoF, [(round(g.StartPoint.x,2), round(g.StartPoint.y,2)) for g in s.Geometry if 'Line' in g.TypeId])" >> $L
