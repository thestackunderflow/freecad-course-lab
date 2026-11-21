uiwatch 30
p=$(ROW peg Thickness); xdotool mousemove ${p% *} ${p#* }; sleep 0.3; xdotool click --repeat 2 --delay 120 1; sleep 1.5
shot $O/q3b-edit-1s.png
echo "S8 ui: $(ui dump)" >> $L
sleep 3
echo "S8 panel: $(FQ "task_texts()" | cut -c1-900)" >> $L
echo "S8 edit: $(Q "import FreeCADGui; print(FreeCADGui.getDocument(\"peg\").getInEdit())")" >> $L
