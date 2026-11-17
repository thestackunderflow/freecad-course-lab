#!/bin/bash
# fc11 probe container (G0): FreeCAD on the virtual screen, then waits; steps are sent with docker exec (FC9_ATTACH=1).
#   MSYS_NO_PATHCONV=1 docker run -d --name fc11p --network none --user maker --shm-size 1g --memory 5g -v <lab>:/lab \
#     fcc-app:1.1.4-0.1.28 bash /lab/lab/fc10_up.sh
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh
O=${1:-$X/G0}; mkdir -p "$O"
fx_start "$O"
echo UP > "$O/.up"
sleep infinity
