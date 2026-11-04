#!/bin/bash
# fx2 take A (LAB-fx2 section 3): the washer, the volume line, STL / .ast / 3MF, the .ast as text, the 3MF unzipped.
#   FCC_PREFIX=fx2 tools/run.sh lab/fx2_A.sh
set -u
O=/lab/out/fx2/A; rm -rf "$O"; mkdir -p "$O"
. /lab/lab/fx2_head.sh
fx2_open_fc
sl_record "$O"
sl_mark "recording started: FreeCAD 1.1.4"
sl_nap 1.5
cat > "$O/build-washer.py" <<'PY'
import FreeCAD as App, Part
doc = App.newDocument("washer")
obj = doc.addObject("Part::Feature", "washer")
obj.Shape = Part.makeCylinder(2.5, 0.3).cut(Part.makeCylinder(1.1, 0.3))
doc.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.Selection.addSelection(obj)
PY
while IFS= read -r line; do console "$line" "washer line"; done < "$O/build-washer.py"
sl_nap 1.5
sl_mark "washer: shown"; sl_nap 3
console 'print(Gui.Selection.getSelection()[0].Shape.Volume)' "the volume line" 
sl_mark "volume: printed"; sl_nap 4
sl_shot "$O/s-volume.png"
Q "import FreeCAD
print(repr(FreeCAD.ActiveDocument.washer.Shape.Volume))" | tee "$O/volume.txt"
sl_click 45 36 "File menu (Save As)"; sl_glide 105 595 15; sl_nap 0.4
sl_shot "$O/s-filemenu.png"
sl_key Escape "close menu"; sl_nap 0.5
Q "import FreeCAD
FreeCAD.ActiveDocument.saveAs('/home/maker/fx2/washer.FCStd')
print(1)" > /dev/null
export_as /home/maker/fx2/washer.stl "STL" type
sl_mark "Export STL: done"; sl_shot "$O/s-stl-done.png"
export_as /home/maker/fx2/washer.ast "AST"
sl_mark "Export AST: done"
sl_click 45 36 "File menu (3MF)"; sl_glide 105 554 15; sl_nap 0.5
sl_click 105 554 "File: Export (3MF)"; sl_nap 3.0
sl_mark "Export 3MF: clicked"
sl_click 1404 1225 "Export: the type list"; sl_nap 2.5; sl_shot "$O/s-types.png"
sl_key Escape "close list"; sl_nap 0.8
sl_click 1400 1171 "Export: the file name box (3MF)"; xdotool key ctrl+a
sl_type "/home/maker/fx2/washer.3mf" "Export: typed washer.3mf" 80; sl_nap 0.8
sl_key Return "Export: Enter (3MF)"; sl_nap 4
sl_mark "Export 3MF: done"
ls -l ~/fx2 | tee "$O/ls-fx2-after-exports.txt"
# the .ast in a text viewer (xterm + less), then the unzip
term_open t1 100 100 150 42 26 bash --norc
term_focus t1
say_cmd t1 "less /home/maker/fx2/washer.ast" "less washer.ast"
sl_mark "washer.ast: opened in text viewer"
for i in 1 2 3 4 5 6 7 8; do sl_nap 3; xdotool key space; done
sl_key q "quit less"; sl_nap 1
say_cmd t1 "clear; head -n 12 /home/maker/fx2/washer.ast" "head ast"; sl_nap 3
say_cmd t1 "grep -c -i -E 'mm|inch|unit' /home/maker/fx2/washer.ast" "grep unit words"; sl_nap 3
say_cmd t1 "clear; cd /home/maker/fx2 && unzip -o washer.3mf -d washer-3mf" "unzip"; sl_nap 3
say_cmd t1 "grep -n 'unit=' washer-3mf/3D/3dmodel.model" "grep unit="; sl_nap 3
sl_mark "3mf unit line: shown"; sl_nap 6
sl_shot "$O/s-unit.png"
head -n 12 ~/fx2/washer.ast | tee "$O/washer-ast-head.txt"
grep -c -i -E 'mm|inch|unit' ~/fx2/washer.ast | tee "$O/washer-ast-unitwords.txt"
(cd ~/fx2 && unzip -o washer.3mf -d washer-3mf | tee "$O/unzip.txt"; unzip -l washer.3mf | tee "$O/unzip-list.txt"; grep -n 'unit=' washer-3mf/3D/3dmodel.model | tee "$O/3mf-unit-line.txt"; grep -rn 'unit=' washer-3mf | tee "$O/3mf-unit-grep.txt")
ls -l ~/fx2 | tee "$O/ls-fx2.txt"
cp ~/fx2/washer.stl ~/fx2/washer.ast ~/fx2/washer.3mf ~/fx2/washer.FCStd "$O/"
sl_mark "recording stopped"
sl_stop
fc_quit; sl_display_stop
echo "take A done"
