#!/bin/bash
# one probe step inside the fc16p container: libs sourced, the running display attached, then the given shell text.
#   MSYS_NO_PATHCONV=1 docker exec fc16p bash /lab/lab/fc16x.sh 'Q "print(1)"'
export FC9_ATTACH=1
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh; . /lab/lab/fc10_lib.sh; . /lab/lab/fc11_lib.sh; . /lab/lab/fc12_lib.sh; . /lab/lab/fc13_lib.sh; . /lab/lab/fc14_lib.sh; . /lab/lab/fc15_lib.sh; . /lab/lab/fc16_lib.sh
O=$X/probe; L=$O/probe-log.txt
eval "$1"
