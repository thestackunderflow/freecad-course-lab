#!/bin/bash
# one probe step inside the fc8p container: libs sourced, the running display attached, then the given shell text.
#   MSYS_NO_PATHCONV=1 docker exec fc8p bash /lab/lab/fc8x.sh 'Q "print(1)"'
export FC8_ATTACH=1
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc8_lib.sh
O=$X/G0/b
eval "$1"
