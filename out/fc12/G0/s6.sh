F=stand; echo "== s6 (measure route) $(date -u +%T)" >> $L
mkdir -p /tmp/fc12; cp $X/T/end.FCStd /tmp/fc12/$F.FCStd; open_doc /tmp/fc12/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1; report_hide; sleep 2
Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewTop(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L; sleep 2
try() {  # try NAME X1 Y1 Z1 X2 Y2 Z2
  local p; p=$(vp $2 $3 $4 $5 $6 $7); set -- "$1" $p
  btn Std_Measure "Measure"; sleep 2
  xdotool mousemove $2 $3; sleep 0.5; xdotool click 1; sleep 1.2
  xdotool mousemove $4 $5; sleep 0.5; xdotool keydown ctrl; xdotool click 1; xdotool keyup ctrl; sleep 3
  echo "$1: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*' | tr '\n' ' ') sel $(selnames)" >> $L
  at "$(taskpos any Close)" "Close"; sleep 1.5
  Q "import FreeCADGui; FreeCADGui.Selection.clearSelection(); print(1)" > /dev/null
}
# lip-top radial side edges, the +10 side of each hook (x 44..49 at y +10, z 10)
try side+ 46.5 10 10 $(rot 46.5 10 80) 10
# lip-top radial side edges, the -10 side
try side- 46.5 -10 10 $(rot 46.5 -10 80) 10
# arm-top inner radial edges (x 29..44 at y +10, z 5)
try arm+ 36.5 10 5 $(rot 36.5 10 80) 5
