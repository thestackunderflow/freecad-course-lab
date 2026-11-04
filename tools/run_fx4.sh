#!/bin/bash
# fx4: run one lab script as the user "maker" in a chosen image (default the lab image), fresh home, hostname pc.
#   tools/run_fx4.sh NAME lab/script.sh [IMAGE]      extra docker args in FCC_DOCKER_ARGS
set -eu
export MSYS_NO_PATHCONV=1
LAB=$(cd "$(dirname "$0")/.." && (pwd -W 2>/dev/null || pwd))
N=$1; S=$2; IMG=${3:-fcc-app:1.1.4-0.1.28}
docker run --rm --name "fx4-$N-$$" --hostname pc --shm-size 1g --memory 6g --user maker -v "$LAB:/lab" -w /lab \
  -e PREREG=b2e37a3 ${FCC_DOCKER_ARGS:-} "$IMG" bash "/lab/$S"
