#!/bin/bash
# fx2 takes C and F, FreeCAD halves: the 1 x 0.5 x 0.25 block and the 3 mm cube, each exported as STL (two recordings).
#   FCC_PREFIX=fx2c tools/run.sh lab/fx2_CF_fc.sh
set -u
O=/lab/out/fx2/C/fc; mkdir -p "$O" /lab/out/fx2/F/fc; rm -f "$O"/* /lab/out/fx2/F/fc/* 2>/dev/null
. /lab/lab/fx2_head.sh
fx2_open_fc
one() {  # one DIR NAME LABEL EVENT "doc line" "dims"  (build + volume + export)
  O=$1; sl_record "$O"; sl_mark "recording started: FreeCAD 1.1.4"; sl_nap 1.5
  cat > "$O/build-$2.py" <<PY
import FreeCAD as App, Part
doc = App.newDocument("$2")
obj = doc.addObject("Part::Feature", "$2")
obj.Shape = Part.makeBox($5)
doc.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.Selection.addSelection(obj)
print(Gui.Selection.getSelection()[0].Shape.Volume)
PY
  while IFS= read -r line; do console "$line" "$2 line"; done < "$O/build-$2.py"
  sl_nap 2; sl_mark "$4"; sl_nap 3; sl_shot "$O/s-built.png"
  Q "import FreeCAD
print(repr(FreeCAD.ActiveDocument.getObject('$2').Shape.Volume))" | tee "$O/volume.txt"
  export_as /home/maker/fx2/$2.stl "$3" type
  sl_mark "Export STL: done"; sl_shot "$O/s-stl-done.png"
  cp ~/fx2/$2.stl "$O/"
  sl_stop
}
one /lab/out/fx2/C/fc block "block" "block 1 x 0.5 x 0.25: shown in FreeCAD" "1, 0.5, 0.25"
Q "import FreeCAD
FreeCAD.closeDocument('block')
print(1)" > /dev/null
one /lab/out/fx2/F/fc cube3 "cube" "cube 3 mm: shown in FreeCAD" "3, 3, 3"
fc_quit; sl_display_stop
echo "take C/F fc done"
