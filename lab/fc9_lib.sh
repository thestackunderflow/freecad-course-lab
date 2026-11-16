# fc9 helpers (FreeCAD course lesson 9, LinearPattern) on top of common.sh + fx19_lib.sh + fx20_lib.sh.
#   . /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh
# In a probe container started by fc9_up.sh, `docker exec` shells set FC9_ATTACH=1: the display already runs.
X=/lab/out/fc9
[ "${FC9_ATTACH:-0}" = 1 ] && export DISPLAY=$SL_DISPLAY SL_W=$W SL_H=$H
shot() { SL_SHOT_WAKE=0 sl_shot "$1"; }
half() { ffmpeg -v error -y -i "$1" -vf scale=1440:-1 "$2"; }   # half-size copy for reading
lab_save() {   # lab_save DOC PATH: a copy of the open document for measuring (not renamed)
  (cd /lab && timeout 30 python3 -m lab.fcrpc save "$1" "$2")
}
check_doc() {  # check_doc FCSTD OUT.json: lab/fc9parts.py check mode (headless, its own process)
  FC9_DOC=$1 FC9_OUT=$2 FC9_MODE=check timeout 120 /opt/freecad/AppRun freecadcmd /lab/lab/fc9parts.py 2>&1 | tr '\r\t' '\n\n' | grep '^FC9' | tail -1
}

# ---- take helpers (every place asked of FreeCAD right before the click; the clicks are a person's) ----
FQ() { Q "exec(open('/lab/lab/fc8q.py').read()); exec(open('/lab/lab/fc9q.py').read()); $1"; }
rowclk() {     # rowclk DOC OBJ LABEL [ctrl]
  local p; p=$(ROW "$1" "$2"); [ -n "$p" ] && [ "$p" != none ] || { echo "no row $2" >> $L; return 1; }
  sl_glide ${p% *} ${p#* } 20; sl_nap 0.4
  if [ "${4:-}" = ctrl ]; then xdotool keydown ctrl; sl_click ${p% *} ${p#* } "$3"; xdotool keyup ctrl
  else sl_click ${p% *} ${p#* } "$3"; fi
}
btn() {        # btn COMMAND LABEL: a toolbar button by its FreeCAD command
  local p; p=$(B "$1"); [ "$p" != none ] || { echo "no button $1" >> $L; return 1; }
  sl_glide ${p% *} ${p#* } 20; sl_nap 0.6; sl_click ${p% *} ${p#* } "$2"
}
at() {         # at "X Y" LABEL: glide and click a place found by a query
  sl_glide ${1% *} ${1#* } 20; sl_nap 0.5; sl_click ${1% *} ${1#* } "$2"
}
vp() { (cd /lab && timeout 20 python3 -m lab.fcrpc vp "$@"); }
taskpos() {    # taskpos KIND TEXT: "x y" of a task-panel entry (KIND row|list|any) whose text is TEXT
  FQ "task_texts()" | python3 -c "import json,sys
d = json.load(sys.stdin)
m = [x for x in d if x[1] == sys.argv[2] and (sys.argv[1] == 'any' or x[0] == sys.argv[1]) and x[2]]
print(' '.join(map(str, m[0][2])) if m else 'none')" "$1" "$2"
}
