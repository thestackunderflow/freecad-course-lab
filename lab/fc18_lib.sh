# fc18 helpers (FreeCAD course lesson 18, a round pen cup by Revolve) on top of common.sh + fx19_lib.sh + fx20_lib.sh +
# fc9_lib.sh .. fc17_lib.sh; lab/fc18parts.py readers.
X18=/lab/out/fc18
check18() {    # check18 FCSTD OUT.json: lab/fc18parts.py check (as saved, recomputed, cup_diameter 60 / 80 / 45: PLAN 2.5), headless
  FC18_DOC=$1 FC18_OUT=$2 FC18_MODE=check timeout 900 /opt/freecad/AppRun freecadcmd /lab/lab/fc18parts.py 2>&1 | tr '\r\t' '\n\n' | grep -o 'FC18 .*' | tail -1
}
FQ18() { Q "exec(open('/lab/lab/fc8q.py').read()); exec(open('/lab/lab/fc9q.py').read()); exec(open('/lab/lab/fc18q.py').read()); $1"; }
