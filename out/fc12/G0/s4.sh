F=stand; echo "== s4 (Q3 fix) $(date -u +%T)" >> $L
p=$(ROW $F PolarPattern); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 4
c=$(FQ "combo_pos('Extent')"); at "$c" "Mode box"; sleep 1.5
s="${c% *} $(( ${c#* } + 42 ))"; echo "popup Spacing at $s (combo $c + 42)" >> $L
shot $O/q3-mode-list.png
at "$s" "Spacing"; sleep 4
echo "panel after Spacing: $(FQ "task_texts()" | grep -o '"Q[A-Za-z:]*Label", "[^"]*"\|"field:[^"]*"\|"combo:[^"]*"' | tr '\n' ' ')" >> $L
echo "state after switch: $(pstate $F)" >> $L
echo "dialogs: $(dialogs) notices: $(FQ "notices()")" >> $L
shot $O/q3-spacing-120.png
lab_save $F $O/q3-switch-preview.FCStd >> $L 2>&1
p=$(FQ "field_pos('Spacing')"); echo "Spacing field $p" >> $L
xdotool mousemove $(( ${p% *} - 40 )) ${p#* }; sleep 0.4; xdotool click 1; sleep 0.3; xdotool key ctrl+a; sleep 0.3
xdotool type --delay 200 "="; sleep 2
echo "after = : $(dialogs) expr_ok $(FQ "expr_ok()")" >> $L
shot $O/q3-expr-open.png
xdotool type --delay 110 "Params.hook_gap"; sleep 1.5; xdotool key Return; sleep 1.5
shot $O/q3-expr-typed.png
echo "editor texts: $(Q "from PySide import QtWidgets
out=[]
for w in QtWidgets.QApplication.topLevelWidgets():
    if w.isVisible() and 'Expression' in w.metaObject().className()+w.windowTitle():
        out += [l.text() for l in w.findChildren(QtWidgets.QLabel) if l.isVisible() and l.text()]
print(out)")" >> $L
e=$(FQ "expr_ok()"); [ "$e" != none ] && at "$e" "Expression OK"; sleep 3
echo "panel after expr: $(FQ "task_texts()" | grep -o '"field:[^"]*"\|"combo:[^"]*"' | tr '\n' ' ')" >> $L
at "$(taskpos any OK)" "OK"; sleep 4
echo "after OK: $(pstate $F)" >> $L
echo "dialogs: $(dialogs) notices: $(FQ "notices()")" >> $L
Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewTop(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L; sleep 2
shot $O/q3-top-fixed.png
lab_save $F $O/q3-fixed-gui.FCStd >> $L 2>&1
