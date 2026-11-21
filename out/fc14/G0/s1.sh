# Q3b route (b) in the GUI: peg-trap open, tree right-click Thickness, the menu's words
mkdir -p /tmp/fc14; cp $X/P/peg-trap.FCStd /tmp/fc14/peg.FCStd
open_doc /tmp/fc14/peg.FCStd >> $L 2>&1
FQ "prep('peg')" >> $L 2>&1
report_hide; sleep 2
echo "S1 notices at open: $(FQ "notices()")" >> $L
row_open peg Thickness >> $L 2>&1
echo "S1 before: $(bstate peg)" >> $L
p=$(ROW peg Thickness); echo "S1 row $p" >> $L
xdotool mousemove ${p% *} ${p#* }; sleep 0.5; xdotool click 1; sleep 1; xdotool click 3; sleep 2
echo "S1 menu: $(FQ14 "menu_items()")" >> $L
shot $O/q3b-menu.png
