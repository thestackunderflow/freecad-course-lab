F=stand; echo "== s5 (Q6 Property view, Q4/Q5 headless) $(date -u +%T)" >> $L
p=$(ROW $F PolarPattern); at "$p" "tree: PolarPattern"; sleep 2
d=$(Q "from PySide import QtWidgets
import FreeCADGui
mw=FreeCADGui.getMainWindow()
out=[]
for t in mw.findChildren(QtWidgets.QTabBar):
    if t.isVisible():
        out.append([t.tabText(i) for i in range(t.count())])
print(out)"); echo "tab bars: $d" >> $L
r=$(FQ12 "prop_row('Angle')"); echo "Angle row $r" >> $L
[ "$r" != none ] && { xdotool mousemove $(( ${r% *} - 5 )) $(( ${r#* } + 3 )); sleep 0.3; xdotool mousemove ${r% *} ${r#* }; sleep 3; echo "tooltip: $(FQ12 "tooltip_text()")" >> $L; shot $O/q6-angle-hover.png; }
echo "doc string: $(Q "import FreeCAD; o=FreeCAD.getDocument('$F').getObject('PolarPattern'); print(repr(o.getDocumentationOfProperty('Angle')), repr(o.getDocumentationOfProperty('Offset')))")" >> $L
