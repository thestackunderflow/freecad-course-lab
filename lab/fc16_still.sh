#!/bin/bash
# fc16 F14 (SCRIPT-fc16 §0.1 "Claude stills show the result"): one inside-view still of each run's SAVED file
# (runs/RUN/after-cup.FCStd), the take kit's "Inside (64 mm high, at 0 20 30)" camera (lab/fc16_take.sh zoomto +
# inside), the take colour, FreeCAD full window, no recording. No Claude, no network, $0:
#   MSYS_NO_PATHCONV=1 docker run --rm --network none --user maker --shm-size 1g -v "<lab>:/lab" -w /lab \
#     fcc-app:1.1.4-0.1.28 bash /lab/lab/fc16_still.sh A1 B1        -> out/fc16/stills/inside-A1.png, inside-B1.png
# The PartDesign "Start Part / New Body" task panel shows on these stills (no active body), as in the takes; the
# F14 crop (draw_fc16.STILL_CROP) keeps clear of it.
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh; . /lab/lab/fc12_lib.sh; . /lab/lab/fc13_lib.sh; . /lab/lab/fc14_lib.sh; . /lab/lab/fc15_lib.sh; . /lab/lab/fc16_lib.sh
S=$X/stills; mkdir -p $S; L=$S/still.log; : > $L
F=cup
fx_start $S
zoomto() {     # as lab/fc16_take.sh, in one step (no glide: nothing is filmed)
  Q "import FreeCAD, FreeCADGui
from pivy import coin
v = FreeCADGui.getDocument('$F').activeView(); v.setAnimationEnabled(False); cam = v.getCameraNode()
v.viewFront(); v.setCameraOrientation(FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -45).multiply(v.getCameraOrientation()))
d = cam.orientation.getValue().multVec(coin.SbVec3f(0, 0, -1)); c = FreeCAD.Vector($1, $2, $3)
p = c - FreeCAD.Vector(d[0], d[1], d[2]) * 200
cam.position.setValue(p.x, p.y, p.z); cam.height.setValue($4)
print(1)" >> $L 2>&1
}
for RUN in "$@"; do
  mkdir -p /tmp/fc16; cp "$X/runs/$RUN/after-cup.FCStd" /tmp/fc16/$F.FCStd
  Q "import FreeCAD
for n in list(FreeCAD.listDocuments()): FreeCAD.closeDocument(n)
print(1)" >> $L 2>&1
  open_doc /tmp/fc16/$F.FCStd >> $L 2>&1
  FQ "prep('$F')" >> $L 2>&1
  Q "import FreeCAD, FreeCADGui
g = FreeCADGui.getDocument('$F'); g.activeView().setAnimationEnabled(False)
g.getObject('Body').ShapeAppearance = [FreeCAD.Material(DiffuseColor=(0.93, 0.55, 0.20))]
print(1)" >> $L 2>&1
  report_hide; xdotool mousemove 2879 1799; sleep 2
  zoomto 0 20 30 64; sleep 2
  echo "$RUN: $(hstate $F)" >> $L
  SL_SHOT_WAKE=0 sl_shot "$S/inside-$RUN.png"
done
fc_quit; sl_display_stop
