O=$X/G0b; L=$O/g0b-log.txt; F=hook
echo "== s10 $(date -u +%T) G0b 3: fix on the orphan file at 80: click the 55's label, K X" >> $L
Q "import FreeCAD; FreeCAD.closeDocument('$F'); print(1)" >> $L; sleep 2
cp $O/hook-orphan-80gui.FCStd /tmp/fc11/$F.FCStd
open_doc /tmp/fc11/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1; sleep 2
echo "at open: $(live11 $F)" >> $L
echo "rows open: $(row_open $F HookSketch)" >> $L; xdotool mousemove 1500 1500; sleep 1
p=$(ROW $F HookSketch); xdotool mousemove ${p% *} ${p#* }; sleep 0.4; xdotool click --repeat 2 --delay 120 1; sleep 4
FQ "look('$F', 'Front', 12, 0, 30, 90)" >> $L 2>&1; sleep 2
echo "solver at open: $(solver_text)" >> $L
read -r DXp DYp < <(cd /lab && timeout 20 python3 -m lab.dimpt $F HookSketch 22); echo "label 22 px $DXp $DYp" >> $L
xdotool mousemove $DXp $DYp; sleep 0.6; xdotool click 1; sleep 1
echo "sel: $(selnames)" >> $L
xdotool mousemove 1800 1300; sleep 0.3; xdotool key k; sleep 0.3; xdotool key x; sleep 3
echo "dialogs after K X: $(xdotool search --onlyvisible --name '.' getwindowname %@ 2>/dev/null | grep -v -E '^(FreeCAD|openbox)' | tr '\n' '|')" >> $L
shot $O/s10-toggled.png
echo "solver after K X: $(solver_text)" >> $L
echo "after K X: $(live11 $F)" >> $L
