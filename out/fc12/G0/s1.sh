F=stand; echo "== s1 $(date -u +%T)" >> $L
mkdir -p /tmp/fc12; cp $X/P/stand-ring.FCStd /tmp/fc12/$F.FCStd
open_doc /tmp/fc12/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1; report_hide; sleep 2; rv_clear
shot $O/q1-ring-iso.png
echo "pstate ring: $(pstate $F)" >> $L
echo "sheet hook_gap shown: $(Q "import FreeCAD; s=FreeCAD.getDocument('$F').getObject('Params'); print(repr(s.getContents('B8')), repr(s.get('hook_gap')), s.getDisplayUnit('B8') if hasattr(s,'getDisplayUnit') else '')")" >> $L
# Q6: the task panel of the ring
p=$(ROW $F PolarPattern); echo "row $p" >> $L; xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 4
echo "panel ring: $(FQ "task_texts()")" >> $L
shot $O/q6-panel-ring.png
