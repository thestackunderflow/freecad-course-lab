#!/bin/bash
# fc9 probe container: FreeCAD on the virtual screen, then waits; steps are sent with docker exec (FC9_ATTACH=1).
#   MSYS_NO_PATHCONV=1 docker run -d --name fc9p --network none --user maker --shm-size 1g --memory 6g -v <lab>:/lab \
#     fcc-app:1.1.4-0.1.28 bash /lab/lab/fc9_up.sh OUTDIR
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh
O=${1:-$X/G0/b}; mkdir -p "$O"
fx_start "$O"
echo UP > "$O/.up"
sleep infinity
