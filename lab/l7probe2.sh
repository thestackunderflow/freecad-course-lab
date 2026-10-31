#!/bin/bash
# Lesson 7 probe 2 ($0, no AI): does saveAs into a folder that does not exist fail, or make the folder? And a folder
# this user may not write to. Results: out/l7/probe/c4-save*.txt
set -u
. /lab/lab/common.sh
O=/lab/out/l7/probe
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true
mkdir -p ~/bin; printf '#!/bin/sh\nexec python3 -m lab.l7call "$@"\n' > ~/bin/test-call; chmod +x ~/bin/test-call
export PATH="$HOME/bin:$PATH" L7_LOG=$O/test-call2.jsonl
uvx freecad-mcp@0.1.28 --help > /dev/null 2>&1
cp /lab/out/l3/hand/back5.FCStd ~/hook.FCStd
sl_display $W $H
fc_start "$O/app-save.log" 1.5; sleep 10
printf "import FreeCAD\nFreeCAD.openDocument('/home/maker/hook.FCStd')\nprint(FreeCAD.ActiveDocument.Name)\n" > ~/open.py
printf "App.ActiveDocument.saveAs('/home/maker/parts/hook.FCStd')\n" > ~/save.py
printf "App.ActiveDocument.saveAs('/opt/hook.FCStd')\n" > ~/save-ro.py
printf "import os\nprint(os.path.exists('/home/maker/parts/hook.FCStd'))\n" > ~/check.py
cd /lab
O2=$O/c4-save.txt; : > "$O2"
for f in open save check save-ro; do
  echo "--- $f.py" >> "$O2"; cat ~/$f.py >> "$O2"; test-call execute_code ~/$f.py >> "$O2" 2>&1; echo "exit $?" >> "$O2"
done
ls -la ~/parts /opt/hook.FCStd >> "$O2" 2>&1
SL_SHOT_WAKE=0 sl_shot "$O/c4-save.png"
fc_quit; sl_display_stop
