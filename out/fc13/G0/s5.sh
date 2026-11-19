F=trap; echo "== s5 (Q5 edge: inward wall 20, through the sheet + Recompute button) $(date -u +%T)" >> $L
Q "import FreeCAD; FreeCAD.getDocument('$F').getObject('Params').set('wall', '20'); print(1)" > /dev/null
rv_clear; btn Std_Refresh "Recompute"; sleep 6
echo "state: $(tstate $F)" >> $L
echo "status: $(Q "import FreeCAD; d=FreeCAD.getDocument('$F'); print([(o.Name, list(o.State), o.getStatusString()) for o in d.Objects if o.TypeId.startswith('PartDesign')])")" >> $L
echo "valid: $(Q "import FreeCAD; print(FreeCAD.getDocument('$F').getObject('Body').Shape.isValid())")" >> $L
echo "dialogs: $(dialogs) notices: $(FQ "notices()")" >> $L
echo "report: $(report_text)" >> $L
FQ "prep('$F')" >> $L 2>&1; sleep 1; shot $O/q5-wall20-iso.png
Q "import FreeCAD; FreeCAD.getDocument('$F').getObject('Params').set('wall', '2'); FreeCAD.getDocument('$F').recompute(); print(1)" > /dev/null
