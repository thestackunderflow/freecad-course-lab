"""Lesson 4's pre-registered scoring of one Claude run (rev 2 after the plan gate; written and committed before any run;
out/l4/prereg.json). The run starts from lesson 3's hook (FreeCAD document hook-lesson3, hook_depth 40, width 20).
Message 1 asks for two 4 mm screw holes through the back plate, 30 mm apart centre to centre, centred on the plate's
back face (the side against the wall), and a 2 mm fillet on the lip's top outer edge (B: plus one sentence: put
hole_d and hole_spacing in the spreadsheet and write the holes' size and position from the names). Message 2: "Make
the hook 30 wide instead of 20." The part after each message = the last root solid in the last document that holds
one (lab/newpart.py).

(a) names: the spreadsheet's aliases; the hole names (aliases with "hole" in them); whether the holes' position is
    written from the width alias (an expression naming it on a sketch constraint, a Placement or an AttachmentOffset;
    the properties are listed);
(b) first build right: checker/holes.check at width 20 (two 4 mm holes, through, centred across, 15 and 45 up = the
    back face's reading; the 2 mm fillet on the lip's top outer edge along the whole width; 9,857.168 mm3 +-0.1;
    box 40 x 20 x 60). Every reading is reported on its own (heights_reading, spacing), so a 17.5/47.5 build is named
    as the other reading, not hidden;
(c) the edit followed: holes.check at width 30 with the heights message 1 left (14,848.584 mm3, box 40 x 30 x 60,
    holes centred across, the fillet along all 30 mm); centred and fillet are also reported on their own;
(d) the edit by one cell: (c), an alias whose value went 20 -> 30 is still named by an expression, and no message-2
    call touches anything else (touched(): any create_object or delete_object; an edit_object on anything but a
    spreadsheet; code or arguments matching TOUCH).
Recorded, not deciding: the objects in the document, each hole's distance from both sides, every reply, time, cost.

    python3 -m checker.score_l4 RUN_DIR   (reads measure-first.json, measure-after2.json, transcript.jsonl, stages.txt)"""
import json
import os
import re
import sys

from checker import holes
from checker.score_l3 import _aliases, _changed_alias, _names_in

TOUCH = re.compile(r'movePoint|addGeometry|delGeometry|setDatum|Constraint\(|\.Geometry\s*=(?!=)|delConstraint|'
                   r'setExpression\(|\.Placement\s*=(?!=)|\.Diameter\s*=(?!=)|\.Radius\s*=(?!=)|\.Base\s*=(?!=)|'
                   r'\.Profile\s*=(?!=)|addObject|newObject|removeObject|AttachmentOffset|MapMode|AttachmentSupport|'
                   r'\.Support\s*=(?!=)|\.Shape\s*=(?!=)|\.Height\s*=(?!=)|\.Length\s*=(?!=)|'
                   r'\.set\(\s*[\'"](?:hole\w*|B6|B7)[\'"]')
SHEET = re.compile(r'sheet|param', re.I)
LENGTHS = ('Length', 'LengthFwd', 'Length2', 'LengthRev')
POSITION = re.compile(r'Constraints|Placement|AttachmentOffset')


def _part(m):
    s = (m or {}).get('solids') or []
    top = [r for r in s if not r.get('in_list')] or s
    return top[-1] if top else None


def _width_alias(m, value=20):
    al = _aliases(m)
    if 'width' in al:
        return 'width'
    for k, v in al.items():
        try:
            if abs(float(str(v).split()[0]) - value) < 1e-9:
                return k
        except (ValueError, IndexError):
            pass
    return None


def names_used(m):
    al = _aliases(m)
    w = _width_alias(m)
    ex = (m or {}).get('expressions') or []
    pos = [e for e in ex if w and _names_in(e.get('expression'), [w]) and POSITION.search(e.get('property') or '')]
    hn = [a for a in sorted(al) if 'hole' in a.lower()]
    return {'aliases': sorted(al), 'hole_names': hn,
            'exprs_from_hole_names': sum(1 for e in ex if _names_in(e.get('expression'), hn)),
            'positions_from_width': bool(pos), 'position_props': ['%s.%s' % (e['object'], e['property']) for e in pos]}


def _text(args_json):
    try:
        a = json.loads(args_json)
    except ValueError:
        return args_json
    return a.get('code') if isinstance(a, dict) and isinstance(a.get('code'), str) else args_json


def touched(calls):
    """calls: (tool name, arguments as JSON text) for one message."""
    for name, args in calls:
        if name in ('create_object', 'delete_object'):
            return True
        if name == 'edit_object':
            try:
                obj = str(json.loads(args).get('obj_name', ''))
            except (ValueError, AttributeError):
                obj = ''
            if not SHEET.search(obj):
                return True
        if TOUCH.search(_text(args) or ''):
            return True
    return False


def _check(m, width, heights=None):
    p = _part(m)
    if p is None:
        return {'ok': False, 'misses': ['no solid'], 'centred': False, 'fillet_on_lip_edge': False,
                'hole_heights_mm': None}
    return holes.check(p, dict(holes.NAMES, width=width), heights=heights)


def score(first, after2, calls2):
    c1 = _check(first, 20)
    r = {'names': names_used(first), 'first_build_right': c1['ok'], 'first_build': c1}
    if after2 is not None:
        c2 = _check(after2, 30, heights=c1.get('hole_heights_mm') or None)
        alias = _changed_alias(first, after2, 20, 30)
        still = bool(alias) and any(_names_in(e.get('expression'), [alias]) for e in after2.get('expressions') or [])
        t = touched(calls2)
        r.update({'names_after_edit': names_used(after2), 'edit_followed': c2['ok'], 'after_edit': c2,
                  'centred_after_edit': c2['centred'], 'fillet_after_edit': c2['fillet_on_lip_edge'],
                  'edit_alias': alias, 'edit_touched_holes': t,
                  'edit_by_one_cell': bool(c2['ok'] and alias and still and not t)})
    return r


def calls_by_message(transcript, stages):
    """Every tools/call as (tool name, arguments JSON), grouped by message (stages.txt: first N, after2 N = the
    transcript's line count when the take saved a copy)."""
    by = {1: [], 2: []}
    bounds = [(1, stages.get('first', 10 ** 9)), (2, stages.get('after2', 10 ** 9))]
    for n, line in enumerate(open(transcript, encoding='utf-8'), start=1):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        m = r.get('msg') if isinstance(r, dict) else None
        if not (isinstance(m, dict) and r.get('dir') == 'client->server' and m.get('method') == 'tools/call'):
            continue
        k = next((k for k, b in bounds if n <= b), 2)
        p = m.get('params') or {}
        by[k].append((p.get('name'), json.dumps(p.get('arguments') or {})))
    return by


def score_run(run_dir):
    def load(name):
        p = os.path.join(run_dir, name)
        return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None
    stages = {}
    sp = os.path.join(run_dir, 'stages.txt')
    if os.path.exists(sp):
        for ln in open(sp, encoding='utf-8'):
            k, v = ln.split()
            stages[k] = int(v)
    by = calls_by_message(os.path.join(run_dir, 'transcript.jsonl'), stages)
    first, after2 = load('measure-first.json'), load('measure-after2.json')
    r = score(first, after2, by[2])
    r['objects_after_edit'] = ((after2 or first) or {}).get('objects')
    r['calls_per_message'] = {k: [c[0] for c in v] for k, v in by.items()}
    return r


if __name__ == '__main__':
    d = sys.argv[1]
    res = score_run(d)
    json.dump(res, open(os.path.join(d, 'score.json'), 'w', encoding='utf-8'), indent=1)
    print(json.dumps(res, indent=1))
