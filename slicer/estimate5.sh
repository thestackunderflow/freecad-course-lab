#!/bin/bash
# Lesson 5 (L5-Q6): PrusaSlicer 2.9.2's own estimate for each STL and orientation, stock MK4S settings (slicer/flatten.py),
# by its command line, no network. Writes OUT/estimates.json.
#   MSYS_NO_PATHCONV=1 docker run --rm --network none -v <lab>:/lab -w /lab fcc-slicer:2.9.2 bash slicer/estimate5.sh OUT FILE...
set -u
OUT=$1; shift; mkdir -p "$OUT"
python3 /lab/slicer/flatten.py /usr/share/PrusaSlicer/profiles/PrusaResearch.ini /tmp/stock.ini
prusa-slicer --version > "$OUT/prusaslicer-version.txt" 2>&1 || true
dpkg -s prusa-slicer | grep '^Version' >> "$OUT/prusaslicer-version.txt"
echo '[' > "$OUT/estimates.json"; first=1
for f in "$@"; do
  for o in "standing:" "side:--rotate-x 90" "back:--rotate-y -90"; do
    n=${o%%:*}; r=${o#*:}; b=$(basename "$f" .stl)
    prusa-slicer --load /tmp/stock.ini $r --binary-gcode=0 --export-gcode -o "/tmp/$b-$n.gcode" "$f" > "$OUT/$b-$n.log" 2>&1
    python3 - "$f" "$n" "/tmp/$b-$n.gcode" "$OUT/$b-$n.log" $first >> "$OUT/estimates.json" <<'PY'
import json, re, sys
f, n, g, log, first = sys.argv[1:6]
t = open(g, errors='replace').read() if __import__('os').path.exists(g) else ''
def k(name):
    m = re.search(r'^; ' + re.escape(name) + r' = (.*)$', t, re.M)
    return m.group(1).strip() if m else None
row = {'file': f.split('/')[-1], 'orientation': n, 'time_normal': k('estimated printing time (normal mode)'),
       'filament_g': k('filament used [g]'), 'layers': t.count(';LAYER_CHANGE'),
       'support_lines': t.count(';TYPE:Support material'), 'printer': k('printer_settings_id'),
       'print': k('print_settings_id'), 'filament': k('filament_settings_id'),
       'warnings': [l.strip() for l in open(log, errors='replace') if 'warning' in l.lower()]}
print(('' if first == '1' else ',') + json.dumps(row))
PY
    first=0
  done
done
echo ']' >> "$OUT/estimates.json"
python3 -c "import json;[print(r['file'],r['orientation'],r['time_normal'],r['filament_g'],r['layers'],r['support_lines'],r['warnings']) for r in json.load(open('$OUT/estimates.json'))]"
