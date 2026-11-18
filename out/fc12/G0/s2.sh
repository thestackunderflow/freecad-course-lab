F=stand; echo "== s2 $(date -u +%T)" >> $L
p=$(row_open $F PolarPattern); echo "row $p" >> $L; xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 4
echo "panel ring: $(FQ "task_texts()")" >> $L
shot $O/q6-panel-ring.png
