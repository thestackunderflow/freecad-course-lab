rm -f /tmp/menu.json
Q "exec(open('/lab/lab/fc14menu.py').read()); arm('/tmp/menu.json', 2500)" >> $L
p=$(ROW peg Thickness); xdotool mousemove ${p% *} ${p#* }; sleep 0.3; xdotool click 3; sleep 3.5
echo "S2 menu: $(cat /tmp/menu.json)" >> $L
