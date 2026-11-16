F=hook
gui_resize() {   # gui_resize SRC TAG VALUE
  Q "import FreeCAD
for n in list(FreeCAD.listDocuments()): FreeCAD.closeDocument(n)
print(1)" > /dev/null; sleep 1
  cp "$1" /tmp/fc10/hook.FCStd; open_doc /tmp/fc10/hook.FCStd > /dev/null; FQ "prep('hook')" > /dev/null; sleep 2
  echo "$2 before: $(live hook)" >> $L
  dblrow Params "open Params"; sleep 1
  c=$(B cell 0 1); xdotool mousemove ${c% *} ${c#* }; sleep 0.5; xdotool click 1; sleep 0.5
  xdotool type --delay 150 "$3"; xdotool key Return; sleep 1
  shot $O/$2-params.png
  p=$(B Std_Refresh); xdotool mousemove ${p% *} ${p#* }; sleep 0.5; xdotool click 1; sleep 3
  t=$(B tab hook); xdotool mousemove ${t% *} ${t#* }; sleep 0.5; xdotool click 1; sleep 2
  echo "$2 GUI after: $(live hook nosolve)" >> $L
  FQ "prep('hook')" > /dev/null; Q "import FreeCADGui; FreeCADGui.activeDocument().activeView().viewFront(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" > /dev/null; sleep 1
  shot $O/$2-front.png
  lab_save hook $O/$2.FCStd > /dev/null
  echo "$2 headless check of the GUI file: $(check10 $O/$2.FCStd $O/$2.check.json)" >> $L
}
dblrow() { local p; p=$(ROW $F "$1"); xdotool mousemove ${p% *} ${p#* }; sleep 0.5; xdotool click --repeat 2 --delay 120 1; sleep 3; }
gui_resize $X/P/hook-unpinned.FCStd q2-unpinned-run1 80
gui_resize $X/P/hook-unpinned.FCStd q2-unpinned-run2 80
gui_resize $X/P/hook-pinned.FCStd q2-pinned 80
echo "q2 headless 60->80 of the start file: $(check10 $X/P/hook-unpinned.FCStd $O/q2-headless-unpinned.check.json 80)" >> $L
