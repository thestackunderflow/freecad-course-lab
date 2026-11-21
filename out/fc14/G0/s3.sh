rm -f /tmp/dlg.json
Q "exec(open('/lab/lab/fc14menu.py').read()); arm_dialog('/tmp/dlg.json', 3000)" >> $L
xdotool mousemove 516 232; sleep 0.5; xdotool click 1; sleep 4
echo "S3 dialog: $(cat /tmp/dlg.json)" >> $L
shot $O/q3b-dialog.png
