F=stand; echo "== s3 (Q2 trap) $(date -u +%T)" >> $L
at "$(taskpos any Cancel)" "Cancel"; sleep 2
p=$(row_open $F Params); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 3
c=$(B cell 6 1); echo "hooks cell $c" >> $L
shot $O/q2-params-open.png
at "$c" "cell B7"; sleep 1; xdotool type --delay 200 "4"; xdotool key Return; sleep 2
btn Std_Refresh "Recompute"; sleep 4
echo "after hooks 4 + recompute: $(pstate $F)" >> $L
t=$(B tab "$F"); echo "3D tab $t" >> $L; at "$t" "tab 3D"; sleep 2
p=$(ROW $F PolarPattern); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 4
p=$(FQ "field_pos('Length')"); echo "Length field $p" >> $L
xdotool mousemove $(( ${p% *} - 40 )) ${p#* }; sleep 0.4; xdotool click --repeat 3 --delay 90 1; sleep 0.4
xdotool type --delay 200 "240"; sleep 0.5; xdotool key Tab; sleep 3
echo "panel at 240: $(FQ "task_texts()" | grep -o '"field:[^"]*"\|"combo:[^"]*"' | tr '\n' ' ')" >> $L
shot $O/q2-panel-240.png
at "$(taskpos any OK)" "OK"; sleep 4
echo "after OK: $(pstate $F)" >> $L
echo "dialogs: $(dialogs)" >> $L
echo "notices: $(FQ "notices()")" >> $L
echo "report: $(report_text)" >> $L
FQ "prep('$F')" >> $L 2>&1; Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewTop(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L; sleep 2
shot $O/q2-top-240.png
lab_save $F $O/q2-trap-gui.FCStd >> $L 2>&1
