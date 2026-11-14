# fc8 helpers (FreeCAD course lesson 8, assembly) on top of common.sh + fx19_lib.sh + fx20_lib.sh.
#   . /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc8_lib.sh
# In a probe container started by fc8_up.sh, `docker exec` shells set FC8_ATTACH=1: the display already runs.
X=/lab/out/fc8
[ "${FC8_ATTACH:-0}" = 1 ] && export DISPLAY=$SL_DISPLAY SL_W=$W SL_H=$H
shot() { SL_SHOT_WAKE=0 sl_shot "$1"; }
half() { ffmpeg -v error -y -i "$1" -vf scale=1440:-1 "$2"; }   # half-size copy for reading
lab_save() {   # lab_save DOC PATH: a copy of the open document for measuring (not renamed)
  (cd /lab && timeout 30 python3 -m lab.fcrpc save "$1" "$2")
}
check_doc() {  # check_doc FCSTD OUT.json: lab/fc8parts.py check mode (headless, its own process)
  FC8_DOC=$1 FC8_OUT=$2 FC8_MODE=check timeout 120 /opt/freecad/AppRun freecadcmd /lab/lab/fc8parts.py 2>&1 | tr '\r\t' '\n\n' | grep '^FC8' | tail -1
}
