F=cup; echo "== s2 (Q3a name in the box, Q2 OK) $(date -u +%T)" >> $L
p=$(FQ "field_pos('Thickness')"); echo "Thickness field $p" >> $L
xdotool mousemove $(( ${p% *} - 40 )) ${p#* }; sleep 0.4; xdotool click 1; sleep 0.3; xdotool key ctrl+a; sleep 0.3
xdotool type --delay 200 "="; sleep 2
echo "after = : expr_ok $(FQ "expr_ok()")" >> $L
shot $O/q3a-expr-open.png
xdotool type --delay 110 "Params.wall"; sleep 1.5; xdotool key Return; sleep 1.5
shot $O/q3a-expr-typed.png
echo "editor texts: $(Q "from PySide import QtWidgets
out=[]
for w in QtWidgets.QApplication.topLevelWidgets():
    if w.isVisible() and 'Expression' in w.metaObject().className()+w.windowTitle():
        out += [l.text() for l in w.findChildren(QtWidgets.QLabel) if l.isVisible() and l.text()]
print(out)")" >> $L
e=$(FQ "expr_ok()"); [ "$e" != none ] && at "$e" "Expression OK"; sleep 4
echo "panel after expr: $(FQ "task_texts()" | grep -o '"field:[^"]*"\|"combo:[^"]*"' | tr '\n' ' ')" >> $L
echo "state before OK: $(tstate $F)" >> $L
shot $O/q2-panel-before-ok.png
at "$(taskpos any OK)" "OK"; sleep 5
echo "after OK: $(tstate $F)" >> $L
echo "dialogs: $(dialogs) notices: $(FQ "notices()")" >> $L
echo "report: $(report_text)" >> $L
FQ "prep('$F')" >> $L 2>&1; sleep 1; shot $O/q2-trap-iso.png
Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewTop(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L; sleep 2
shot $O/q2-trap-top.png
lab_save $F $O/q2-trap-gui.FCStd >> $L 2>&1
check13 $O/q2-trap-gui.FCStd $O/q2-trap-gui.check.json >> $L
