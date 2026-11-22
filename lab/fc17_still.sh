#!/bin/bash
# fc17 F15 (SCRIPT-fc17 §0.1 "Claude stills show the result"): a Front and a Rear still of each run's SAVED file
# (runs/RUN/after-cup.FCStd), the take kit's Front / Rear views (lab/fc17_take.sh front / rear: at 0 -28 32 and
# 0 28 32, 80 mm high), the take colour, FreeCAD full window, no recording. No Claude, no network, $0:
#   MSYS_NO_PATHCONV=1 docker run --rm --network none --user maker --shm-size 1g -v "<lab>:/lab" -w /lab \
#     fcc-app:1.1.4-0.1.28 bash /lab/lab/fc17_still.sh B1        -> out/fc17/stills/front-B1.png, rear-B1.png
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh; . /lab/lab/fc12_lib.sh; . /lab/lab/fc13_lib.sh; . /lab/lab/fc14_lib.sh; . /lab/lab/fc15_lib.sh; . /lab/lab/fc16_lib.sh; . /lab/lab/fc17_lib.sh
S=$X/stills; mkdir -p $S; L=$S/still.log; : > $L
F=cup
fx_start $S
view() {       # view VIEW CX CY CZ HEIGHT: as lab/fc17_take.sh zoomto, in one step (no glide: nothing is filmed)
  Q "import FreeCAD, FreeCADGui
from pivy import coin
v = FreeCADGui.getDocument('$F').activeView(); v.setAnimationEnabled(False); cam = v.getCameraNode()
getattr(v, 'view$1')()
d = cam.orientation.getValue().multVec(coin.SbVec3f(0, 0, -1)); c = FreeCAD.Vector($2, $3, $4)
p = c - FreeCAD.Vector(d[0], d[1], d[2]) * 200
cam.position.setValue(p.x, p.y, p.z); cam.height.setValue($5)
print(1)" >> $L 2>&1
}
for RUN in "$@"; do
  mkdir -p /tmp/fc17; cp "$X/runs/$RUN/after-cup.FCStd" /tmp/fc17/$F.FCStd
  Q "import FreeCAD
for n in list(FreeCAD.listDocuments()): FreeCAD.closeDocument(n)
print(1)" >> $L 2>&1
  open_doc /tmp/fc17/$F.FCStd >> $L 2>&1
  FQ "prep('$F')" >> $L 2>&1
  Q "import FreeCAD, FreeCADGui
g = FreeCADGui.getDocument('$F'); g.activeView().setAnimationEnabled(False)
g.getObject('Body').ShapeAppearance = [FreeCAD.Material(DiffuseColor=(0.93, 0.55, 0.20))]
print(1)" >> $L 2>&1
  report_hide; xdotool mousemove 2879 1799; sleep 2
  view Front 0 -28 32 80; sleep 2
  echo "$RUN front: $(hstate $F)" >> $L
  SL_SHOT_WAKE=0 sl_shot "$S/front-$RUN.png"
  view Rear 0 28 32 80; sleep 2
  echo "$RUN rear: $(hstate $F)" >> $L
  SL_SHOT_WAKE=0 sl_shot "$S/rear-$RUN.png"
done
fc_quit; sl_display_stop
