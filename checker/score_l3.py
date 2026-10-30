"""Lesson 3's pre-registered scoring of one Claude run (written and committed before any run; see out/l3/prereg.json).
Inputs: checker/measure.py's JSON for the document after message 1 ("first") and after message 2 ("after"), and the
code of the calls Claude sent for message 2 (from the plug's log).

(a) names used: the spreadsheet aliases found; how many of the sketch's sizes and whether the pad's length are written
    from a spreadsheet name (an expression that names an alias);
(b) first build right: 8,500 mm3 (+-0.1), box 25 x 20 x 60, the eight corners of lesson 2's J (+-0.01, sketch plane,
    any order), standing up (Z 0..60, lip at +X);
(c) edit followed ("Make the hook 40 deep instead of 25."): 10,000 mm3, box 40 x 20 x 60, the corners with the arm
    40 deep, standing up; a 45 box with a 40 mm arm inside is recorded as "read differently", not as a failure of names;
(d) edit by one cell: (c) holds, the hook_depth alias now reads 40, the sizes still come from names, and message 2's
    code moves no point and adds or rewrites no line or size in the sketch.

    python3 -m checker.score_l3 FIRST.json AFTER.json CALLS.json OUT.json"""
import json
import re
import sys

from checker import outline

NAMES = {'plate_height': 60, 'width': 20, 'thickness': 5, 'hook_depth': 25, 'lip_height': 10}
SKETCH_EDITS = re.compile(r'movePoint|addGeometry|delGeometry|setDatum|Constraint\(|\.Geometry\s*=|LineSegment|'
                          r'delConstraint|renameConstraint')


def _corners(depth):
    return outline.walk(outline.named_moves(dict(NAMES, hook_depth=depth)))[:-1]


def _same_corners(got, want, tol=0.01):
    if not got or len(got) != len(want):
        return False
    left = [tuple(p) for p in got]
    for w in want:
        hit = [p for p in left if abs(p[0] - w[0]) <= tol and abs(p[1] - w[1]) <= tol]
        if not hit:
            return False
        left.remove(hit[0])
    return True


def _part(m):
    s = [r for r in m.get('solids') or [] if not r.get('in_list')] or (m.get('solids') or [])
    return s[-1] if s else None


def _aliases(m):
    out = {}
    for sh in m.get('sheets') or []:
        out.update(sh.get('aliases') or {})
    return out


def _from_name(expr, aliases):
    return bool(expr) and any(re.search(r'\b%s\b' % re.escape(a), expr) for a in aliases)


def names_used(m):
    al = _aliases(m)
    sk = (m.get('sketches') or [{}])[0]
    dims = [d for d in sk.get('dimensions') or [] if _from_name(d.get('expression'), al)]
    pads = m.get('pads') or [{}]
    pad = _from_name((pads[0] or {}).get('expression'), al)
    return {'aliases': sorted(al), 'dims_from_names': len(dims), 'pad_from_name': pad,
            'used': bool(al) and (len(dims) > 0 or pad)}


def check_build(m, volume, bbox, corners):
    p, misses = _part(m), []
    if p is None:
        return False, ['no solid']
    if abs(p['volume_mm3'] - volume) > 0.1:
        misses.append('volume')
    if any(abs(a - b) > 0.01 for a, b in zip(p['bbox_mm'], bbox)):
        misses.append('size')
    z0, z1 = p['z_range_mm']
    if not (abs(z0) <= 0.01 and abs(z1 - 60) <= 0.01 and p['min_mm'][0] >= -0.01):
        misses.append('upright')
    sk = (m.get('sketches') or [{}])[0]
    if not _same_corners(sk.get('corners_xy'), corners):
        misses.append('corners')
    return not misses, misses


def score(first, after, edit_code):
    ok1, miss1 = check_build(first, 8500.0, [25.0, 20.0, 60.0], _corners(25))
    ok2, miss2 = check_build(after, 10000.0, [40.0, 20.0, 60.0], _corners(40))
    p = _part(after)
    reading = 'box 40' if ok2 else ('arm 40 inside (box 45)' if p and abs(p['bbox_mm'][0] - 45) <= 0.01 else 'other')
    n_first, n_after = names_used(first), names_used(after)
    al = _aliases(after)
    cell = str(al.get('hook_depth', '')).replace('mm', '').strip()
    try:
        cell_40 = abs(float(cell) - 40) <= 1e-9
    except ValueError:
        cell_40 = False
    touched = any(SKETCH_EDITS.search(c or '') for c in edit_code)
    return {'names': n_first, 'names_after_edit': n_after,
            'first_build_right': ok1, 'first_build_misses': miss1,
            'edit_followed': ok2, 'edit_misses': miss2, 'edit_reading': reading,
            'edit_by_one_cell': bool(ok2 and cell_40 and n_after['dims_from_names'] > 0 and not touched),
            'edit_touched_sketch': touched}


if __name__ == '__main__':
    f, a, c = (json.load(open(p, encoding='utf-8')) for p in sys.argv[1:4])
    code = [x.get('arguments', {}).get('code', '') for x in c] if isinstance(c, list) else []
    r = score(f, a, code)
    json.dump(r, open(sys.argv[4], 'w', encoding='utf-8'), indent=1)
    print(json.dumps(r, indent=1))
