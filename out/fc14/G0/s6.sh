Q "import FreeCADGui; FreeCADGui.getMainWindow().findChildren(__import__('PySide').QtWidgets.QWidget, 'NotificationArea'); print(1)" > /dev/null
xdotool key Escape; sleep 0.5
p=$(ROW peg Thickness); xdotool mousemove ${p% *} ${p#* }; sleep 0.3; xdotool click --repeat 2 --delay 120 1; sleep 4
echo "S6 panel: $(FQ "task_texts()" | cut -c1-1500)" >> $L
echo "S6 list: $(FQ14 "task_list_items()")" >> $L
echo "S6 state: $(bstate peg)" >> $L
echo "S6 ui: $(dialogs)" >> $L
shot $O/q3b-edit-open.png
