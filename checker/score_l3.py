"""Lesson 3's pre-registered scoring of one Claude run (rev 2, written and committed before any run; out/l3/prereg.json).
Inputs: checker/measure.py's JSON for the document after message 1 ("first"), message 2 ("after2") and message 3
("after3"), and the arguments of every tool call Claude sent for messages 2 and 3 (from the plug's log).
The part after each message = the last root solid in the last document that holds one (lab/newpart.py picks it).

(a) names used: the spreadsheet aliases; how many expressions anywhere in the document name an alias (sketch sizes,
    pad or extrusion lengths, any property of any object);
(b) first build right: 8,500 mm3 (+-0.1), box 25 x 20 x 60 (+-0.01), Z 0..60;
(c) message 2 ("Make the hook 40 deep instead of 25.") followed: 10,000, 40 x 20 x 60, Z 0..60; other readings are
    recorded, not failed as names: "arm 40 inside (box 45)", "clear 40 inside (box 50)", "40 as the extrude";
(d) edit 2 by one cell: (c), an alias whose value went 25 -> 40 is still named by an expression, and no message-2 call
    moves a point, adds or deletes geometry, sets a size or rebinds a sketch size;
(e) message 3 ("Make it 8 thick instead of 5.") followed: 15,040, 40 x 20 x 60, Z 0..60;
(f) edit 3 by one cell: as (d), for an alias that went 5 -> 8.
Recorded, not deciding: the sketch corners (construction lines skipped by measure.py), the alias spellings.

    python3 -m checker.score_l3 RUN_DIR      (reads measure-{first,after2,after3}.json, transcript.jsonl, stages.txt;
                                             writes score.json)"""
import json
import os
import re
import sys

from checker import outline

NAMES = {'plate_height': 60, 'width': 20, 'thickness': 5, 'hook_depth': 25, 'lip_height': 10}


def _expected(depth, t):
    e = outline.expected(outline.named_moves(dict(NAMES, hook_depth=depth, thickness=t)), NAMES['width'])
    return e['volume_mm3'], e['bbox_mm']


EXPECTED = {'first': _expected(25, 5), 'after2': _expected(40, 5), 'after3': _expected(40, 8)}
CORNERS = {'first': (25, 5), 'after2': (40, 5), 'after3': (40, 8)}
SKETCH_EDITS = re.compile(r'movePoint|addGeometry|delGeometry|setDatum|Constraint\(|\.Geometry\s*=|LineSegment|'
                          r'delConstraint|renameConstraint|setExpression\(\s*[\'"]\.?Constraints')


def _corners(stage):
    d, t = CORNERS[stage]
    return outline.walk(outline.named_moves(dict(NAMES, hook_depth=d, thickness=t)))[:-1]


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
    s = m.get('solids') or []
    top = [r for r in s if not r.get('in_list')] or s
    return top[-1] if top else None


def _aliases(m):
    out = {}
    for sh in m.get('sheets') or []:
        out.update(sh.get('aliases') or {})
    return out


def _num(v):
    m = re.match(r'\s*(-?[0-9.]+)', str(v))
    return float(m.group(1)) if m else None


def _names_in(expr, aliases):
    return [a for a in aliases if expr and re.search(r'(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])' % re.escape(a), expr)]


def names_used(m):
    al = _aliases(m)
    ex = [e for e in m.get('expressions') or [] if _names_in(e.get('expression'), al)]
    return {'aliases': sorted(al), 'exprs_from_names': len(ex),
            'sketch_sizes_from_names': sum(1 for e in ex if 'Constraints' in e.get('property', '')),
            'length_from_name': any(e.get('property') in ('Length', 'LengthFwd', 'Length2', 'LengthRev') for e in ex),
            'used': bool(al) and bool(ex)}


def check_build(m, stage):
    vol, box = EXPECTED[stage]
    p, misses = _part(m) if m else None, []
    if p is None:
        return False, ['no solid']
    if abs(p['volume_mm3'] - vol) > 0.1:
        misses.append('volume')
    if any(abs(a - b) > 0.01 for a, b in zip(p['bbox_mm'], box)):
        misses.append('size')
    z0, z1 = p['z_range_mm']
    if not (abs(z0) <= 0.01 and abs(z1 - 60) <= 0.01):
        misses.append('height')
    return not misses, misses


def _reading(m):
    p = _part(m) if m else None
    if not p:
        return 'no solid'
    b = [round(x, 2) for x in p['bbox_mm']]
    return {(40.0, 20.0, 60.0): 'box 40', (45.0, 20.0, 60.0): 'arm 40 inside (box 45)',
            (50.0, 20.0, 60.0): 'clear 40 inside (box 50)',
            (25.0, 40.0, 60.0): '40 as the extrude (25 x 40 x 60)'}.get(tuple(b), 'other (box %s)' % b)


def _changed_alias(before, after, old, new):
    a, b = _aliases(before or {}), _aliases(after or {})
    for k in sorted(b):
        if k in a and _num(a[k]) is not None and _num(b[k]) is not None \
                and abs(_num(a[k]) - old) < 1e-9 and abs(_num(b[k]) - new) < 1e-9:
            return k
    return None


def _edit(before, after, stage, old, new, code):
    ok, misses = check_build(after, stage)
    alias = _changed_alias(before, after, old, new)
    still = bool(alias) and any(_names_in(e.get('expression'), [alias]) for e in (after or {}).get('expressions') or [])
    touched = any(SKETCH_EDITS.search(c or '') for c in code)
    return ok, misses, alias, bool(ok and alias and still and not touched), touched


def score(first, after2, after3, code2, code3):
    ok1, miss1 = check_build(first, 'first')
    ok2, miss2, al2, one2, t2 = _edit(first, after2, 'after2', 25, 40, code2)
    r = {'names': names_used(first), 'names_after_edits': names_used(after3 or after2 or first),
         'first_build_right': ok1, 'first_build_misses': miss1,
         'edit2_followed': ok2, 'edit2_misses': miss2, 'edit2_reading': _reading(after2),
         'edit2_alias': al2, 'edit2_by_one_cell': one2, 'edit2_touched_sketch': t2,
         'corners': {}}
    if after3 is not None:
        ok3, miss3, al3, one3, t3 = _edit(after2, after3, 'after3', 5, 8, code3)
        p3 = _part(after3)
        r.update({'edit3_followed': ok3, 'edit3_misses': miss3, 'edit3_alias': al3, 'edit3_by_one_cell': one3,
                  'edit3_touched_sketch': t3,
                  'edit3_reading': ('%g mm3, box %s' % (round(p3['volume_mm3'], 3), ' x '.join('%g' % x for x in p3['bbox_mm'])))
                  if p3 else 'no solid'})
    for stage, m in (('first', first), ('after2', after2), ('after3', after3)):
        if m is not None:
            sk = (m.get('sketches') or [{}])
            r['corners'][stage] = any(_same_corners(s.get('corners_xy'), _corners(stage)) for s in sk)
    return r


def calls_by_message(transcript, stages):
    """Every tools/call's arguments (as JSON text), grouped by the message it belongs to: the take writes the
    transcript's line count each time it saves a copy (stages.txt: first N, after2 N, after3 N)."""
    by = {1: [], 2: [], 3: []}
    bounds = [(1, stages.get('first', 10 ** 9)), (2, stages.get('after2', 10 ** 9)), (3, stages.get('after3', 10 ** 9))]
    for n, line in enumerate(open(transcript, encoding='utf-8'), start=1):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        m = r.get('msg') if isinstance(r, dict) else None
        if not (isinstance(m, dict) and r.get('dir') == 'client->server' and m.get('method') == 'tools/call'):
            continue
        k = next((k for k, b in bounds if n <= b), 3)
        by[k].append(json.dumps((m.get('params') or {}).get('arguments') or {}))
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
    r = score(load('measure-first.json'), load('measure-after2.json'), load('measure-after3.json'), by[2], by[3])
    r['calls_per_message'] = {k: len(v) for k, v in by.items()}
    return r


if __name__ == '__main__':
    d = sys.argv[1]
    res = score_run(d)
    json.dump(res, open(os.path.join(d, 'score.json'), 'w', encoding='utf-8'), indent=1)
    print(json.dumps(res, indent=1))
