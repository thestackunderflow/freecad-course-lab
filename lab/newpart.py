"""After Claude's turn (lab instrument, not filmed as a step): which document and object hold Claude's part, and its
sketch? Prints "DOC OBJ SKETCH" for the part in a document other than the by-hand one (`hand`): the solid no other
solid is built from (a Part Design Body, not its Pad), and the first sketch in that document ("-" if none)."""
import json
import sys

sys.path.insert(0, '/lab')
from lab import fcrpc  # noqa: E402

CODE = """import FreeCAD, json
rows = []
for d in FreeCAD.listDocuments().values():
    for o in d.Objects:
        s = getattr(o, 'Shape', None)
        if s is None or s.isNull() or not s.Solids:
            continue
        top = not any(getattr(x, 'Shape', None) is not None and not x.Shape.isNull() and x.Shape.Solids for x in o.InList)
        rows.append([d.Name, o.Name, o.Label, o.TypeId, round(s.Volume, 4), top])
sk = {d.Name: [o.Name for o in d.Objects if o.TypeId == 'Sketcher::SketchObject'] for d in FreeCAD.listDocuments().values()}
print(json.dumps({'solids': rows, 'sketches': sk}))"""


def pick(state, hand_doc='hand'):
    cand = [r for r in state['solids'] if r[0] != hand_doc and r[5]]
    if not cand:
        return None
    doc, obj = cand[-1][0], cand[-1][1]
    sks = state['sketches'].get(doc) or []
    return doc, obj, (sks[0] if sks else '-')


if __name__ == '__main__':
    st = json.loads(fcrpc.run(CODE))
    p = pick(st)
    json.dump({'state': st, 'claude': p}, open(sys.argv[1], 'w'), indent=1)
    print(' '.join(p) if p else '')
