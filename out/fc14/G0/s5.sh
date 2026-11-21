xdotool mousemove 1499 966; sleep 0.4; xdotool click 1; sleep 1
echo "S5 combo now: $(ui dump | python3 -c 'import json,sys; print([d["combos"] for d in json.load(sys.stdin)["dialogs"]])')" >> $L
xdotool mousemove 1337 941; sleep 0.4; xdotool click 1; sleep 3
echo "S5 after OK ui: $(ui dump)" >> $L
echo "S5 after OK: $(bstate peg)" >> $L
echo "S5 report: $(report_text | tail -c 400)" >> $L
shot $O/q3b-after-ok.png
btn Std_Refresh "Recompute"; sleep 3
echo "S5 after recompute: $(bstate peg)" >> $L
echo "S5 dialogs $(dialogs) notices $(FQ "notices()")" >> $L
shot $O/q3b-after-recompute.png
