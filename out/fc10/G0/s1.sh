mkdir -p /tmp/fc10; cp $X/P/hook-unpinned.FCStd /tmp/fc10/hook.FCStd
: > $L
echo "open: $(open_doc /tmp/fc10/hook.FCStd)" >> $L
report_hide; sleep 2
echo "live60: $(live hook)" >> $L
read -r SKX SKY < <(row_open hook HookSketch); echo "HookSketch row $SKX $SKY" >> $L
xdotool mousemove $SKX $SKY; sleep 0.5; xdotool click --repeat 2 --delay 120 1; sleep 4; xdotool mousemove 1500 300; sleep 1
shot $O/q1-edit-unpinned.png
echo "q1 solver_text: $(solver_text)" >> $L
echo "q1 link: $(WG link Degrees)" >> $L
echo "q1 coincident cmd: $(cmdtext Sketcher_ConstrainCoincidentUnified)" >> $L
echo "q1 coincident cmd2: $(cmdtext Sketcher_ConstrainCoincident)" >> $L
echo "q1 lock cmd: $(cmdtext Sketcher_ConstrainLock)" >> $L
echo "q1 button unified: $(B Sketcher_ConstrainCoincidentUnified) plain: $(B Sketcher_ConstrainCoincident)" >> $L
