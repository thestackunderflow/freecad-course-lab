#!/bin/bash
# one probe step inside the fc9p container: libs sourced, the running display attached, then the given shell text.
#   MSYS_NO_PATHCONV=1 docker exec fc9p bash /lab/lab/fc9x.sh 'Q "print(1)"'
export FC9_ATTACH=1
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh
O=$X/G0/b
eval "$1"
