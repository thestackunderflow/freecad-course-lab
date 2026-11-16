#!/bin/bash
# video D probe P2 by code (not filmed): FCC_PREFIX=fc8 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fc8_p2code.sh
mkdir -p /lab/out/fc8/P2
FC8_OUT=/lab/out/fc8/P2 FC8_MODE=ladder timeout 300 /opt/freecad/AppRun freecadcmd /lab/lab/fc8parts.py 2>&1 | tr '\r\t' '\n\n' | grep '^FC8'
