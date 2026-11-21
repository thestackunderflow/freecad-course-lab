#!/bin/bash
# fc14 cut 3 (WATCH-fc14-cut2 must-fix 1): a still of each run's SAVED file (runs/RUN/after-peg.FCStd) with the Body's
# Tip shown (prep: the tip visible, other features hidden, iso + fit = the before.png camera), so the peg shows.
# No Claude, no network:
#   MSYS_NO_PATHCONV=1 docker run --rm --network none --user maker --shm-size 1g -v "<lab>:/lab" -w /lab \
#     fcc-app:1.1.4-0.1.28 bash /lab/lab/fc14_after_still.sh A1 B1
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh; . /lab/lab/fc12_lib.sh; . /lab/lab/fc13_lib.sh; . /lab/lab/fc14_lib.sh
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
addon_install; autostart_on true
sl_display $W $H
fc_start /tmp/app.log 1.5; sleep 8
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 1
for RUN in "$@"; do
  O=/lab/out/fc14/runs/$RUN
  cp "$O/after-peg.FCStd" /tmp/peg.FCStd
  Q "import FreeCAD, FreeCADGui
for n in list(FreeCAD.listDocuments()): FreeCAD.closeDocument(n)
d = FreeCAD.openDocument('/tmp/peg.FCStd')
print(d.Name)"
  FQ "prep('peg')"
  Q "import FreeCAD, FreeCADGui
d = FreeCAD.getDocument('peg'); b = d.getObject('Body')
FreeCADGui.getDocument('peg').getObject('Body').ShapeAppearance = [FreeCAD.Material(DiffuseColor=(0.93, 0.55, 0.20))]
print('tip', b.Tip.Name, [o.Name for o in b.Group if FreeCADGui.getDocument('peg').getObject(o.Name).Visibility])" | tee "$O/after-peg-shot.txt"
  report_hide; xdotool mousemove 2000 1700; sleep 2
  SL_SHOT_WAKE=0 sl_shot "$O/after-peg.png"
done
fc_quit; sl_display_stop
