# Q3b route (b): right-click Thickness, Move Feature After..., the dialog's words, its list
uiwatch 90
p=$(ROW peg Thickness); xdotool mousemove ${p% *} ${p#* }; sleep 0.3; xdotool click 3; sleep 1
m=$(ui menu "Move Feature After"); echo "S4 menu item at $m" >> $L
xdotool mousemove ${m% *} ${m#* }; sleep 0.4; xdotool click 1; sleep 2
echo "S4 dialog: $(ui dump)" >> $L
c=$(ui combo "Beginning"); xdotool mousemove ${c% *} ${c#* }; sleep 0.4; xdotool click 1; sleep 1.5
echo "S4 popup: $(ui dump | python3 -c 'import json,sys; print(json.load(sys.stdin)["popup"])')" >> $L
shot $O/q3b-popup.png
