#!/bin/bash
# one probe step inside the fc11p container: libs sourced, the running display attached, then the given shell text.
#   MSYS_NO_PATHCONV=1 docker exec fc11p bash /lab/lab/fc10x.sh 'Q "print(1)"'
export FC9_ATTACH=1
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh
O=$X/G0; L=$O/g0-log.txt
eval "$1"
