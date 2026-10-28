#!/bin/bash
# Run the lab's tests inside the lab image (nothing on the host).   tools/test.sh [pytest args...]
set -eu
export MSYS_NO_PATHCONV=1
LAB=$(cd "$(dirname "$0")/.." && (pwd -W 2>/dev/null || pwd))
[ $# -eq 0 ] && set -- tests
docker run --rm --name "fcc-test-$$" --shm-size 512m --user maker -e HOME=/tmp/h -v "$LAB:/lab" -w /lab \
  ${LAB_PRIVATE_WORDS:+-e LAB_PRIVATE_WORDS="$LAB_PRIVATE_WORDS"} fcc-app:1.1.4-0.1.28 \
  bash -c 'mkdir -p $HOME && python3 -m pytest -p no:cacheprovider -q -rs "$@"' _ "$@"
