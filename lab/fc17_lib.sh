# fc17 helpers (FreeCAD course lesson 17, a second key peg by Mirror) on top of common.sh + fx19_lib.sh + fx20_lib.sh +
# fc9_lib.sh .. fc16_lib.sh; lab/fc17parts.py readers.
X=/lab/out/fc17
check17() {    # check17 FCSTD OUT.json: lab/fc17parts.py check (as saved, recomputed, peg_x 15 / 20 / 8, wall 3: PLAN 2.5), headless
  FC17_DOC=$1 FC17_OUT=$2 FC17_MODE=check timeout 900 /opt/freecad/AppRun freecadcmd /lab/lab/fc17parts.py 2>&1 | tr '\r\t' '\n\n' | grep '^FC17' | tail -1
}
