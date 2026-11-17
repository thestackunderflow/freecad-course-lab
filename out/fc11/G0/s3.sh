F=hook; echo "== s3 $(date -u +%T)" >> $L
echo "tb: $(FQ "toolbars('Sketcher_Dim')" 2>&1 | head -c 600)" >> $L
echo "cmd K D: $(cmdtext Sketcher_ConstrainDistance)" >> $L
echo "cmd dim: $(cmdtext Sketcher_Dimension)" >> $L
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key d; sleep 3
echo "dialogs: $(dialogs)" >> $L
shot $O/q1-dialog.png
