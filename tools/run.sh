#!/bin/bash
# Run one lab script in the lab image as the user "maker" (fresh home each time, hostname "pc"), the lab at /lab.
#   tools/run.sh lab/probe.sh [args...]          (extra docker args: FCC_DOCKER_ARGS="--env-file x")
set -eu
export MSYS_NO_PATHCONV=1
LAB=$(cd "$(dirname "$0")/.." && (pwd -W 2>/dev/null || pwd))
S=$1; shift
docker run --rm --name "fcc-run-$$" --hostname pc --shm-size 1g --memory 6g --user maker -v "$LAB:/lab" -w /lab \
  ${FCC_DOCKER_ARGS:-} fcc-app:1.1.4-0.1.28 bash "/lab/$S" "$@"
