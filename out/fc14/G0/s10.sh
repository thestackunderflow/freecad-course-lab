# Q3b route (a): fresh trap; right-click Pad001, Move Feature After..., Thickness; Move Tip question
Q "import FreeCAD; FreeCAD.closeDocument('peg'); print(1)" > /dev/null
cp $X/P/peg-trap.FCStd /tmp/fc14/peg.FCStd; open_doc /tmp/fc14/peg.FCStd > /dev/null 2>&1; FQ "prep('peg')" > /dev/null 2>&1
row_open peg Pad001 > /dev/null 2>&1; sleep 1
uiwatch 60
p=$(ROW peg Pad001); xdotool mousemove ${p% *} ${p#* }; sleep 0.3; xdotool click 1; sleep 0.5; xdotool click 3; sleep 1
m=$(ui menu "Move Feature After"); xdotool mousemove ${m% *} ${m#* }; sleep 0.4; xdotool click 1; sleep 2
c=$(ui combo "Beginning"); xdotool mousemove ${c% *} ${c#* }; sleep 0.4; xdotool click 1; sleep 1.5
q=$(ui popup "Thickness"); echo "S10 popup Thickness at $q" >> $L; xdotool mousemove ${q% *} ${q#* }; sleep 0.4; xdotool click 1; sleep 1
b=$(ui button OK); xdotool mousemove ${b% *} ${b#* }; sleep 0.4; xdotool click 1; sleep 2
echo "S10 after OK ui: $(ui dump)" >> $L
shot $O/q3b-a-question.png
