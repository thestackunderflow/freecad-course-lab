"""After Claude's turn (lab instrument, not filmed as a step): which document and object hold Claude's new block?
Prints "DOC OBJ" for the newest solid that is not the by-hand Cube (document Unnamed, object Box)."""
import json
import sys

sys.path.insert(0, '/lab')
from lab import fcrpc  # noqa: E402

CODE = """import FreeCAD, json
rows = []
for d in FreeCAD.listDocuments().values():
    for o in d.Objects:
        s = getattr(o, 'Shape', None)
        if s is not None and not s.isNull() and s.Solids:
            rows.append([d.Name, o.Name, o.Label, round(s.Volume, 4)])
print(json.dumps(rows))"""

rows = json.loads(fcrpc.run(CODE))
new = [r for r in rows if not (r[0] == 'Unnamed' and r[1] == 'Box')]
json.dump({'solids': rows, 'claude': new[-1] if new else None}, open(sys.argv[1], 'w'), indent=1)
print(f'{new[-1][0]} {new[-1][1]}' if new else '')
