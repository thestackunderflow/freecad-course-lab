"""Lesson 6's pre-registered scoring of one changed hook (by hand or by a Claude run; written and committed before any
run; out/l6/prereg.json). Input: the read of the saved document after the turn (checker/l6read.py).

The change C: the opening (the gap between the back plate and the lip, read along a line at 7.5 mm up) = 45.00 +- 0.05.
The must-stay-true list:
  M1 one solid, no errors: 1 solid, isValid, no object in an Invalid/Error state; its STL (FreeCAD's own export of the
     part) closed, one component, no non-manifolds
  M2 the back plate 60 tall and 30 wide: box Z 60.00 and Y 30.00 (+-0.01)
  M3 every wall 5 thick: the points 0.1 mm inside each wall's inner face are in the solid, 0.1 mm beyond are not
     (plate, base, lip)
  M4 the lip 10 tall: in at 9.9 mm up, out at 10.1 (2.5 mm in from the front)
  M5 both holes: checker/holes.check at the part's own depth: 2 holes, 4.00 mm (+-0.01), through, centred across
     (+-0.05), at 15 and 45 up (+-0.05)
  M6 the 2 mm rounded edge on the lip: holes.check fillet_on_lip_edge
  M7 the names still drive it: the six names other than hook_depth still there with their values (width 30, thickness
     5, lip_height 10, plate_height 60, hole_d 4, hole_spacing 30); hook_depth equal to the part's depth (+-0.01);
     each of the start's 12 bindings (object + property, START_BINDINGS) still written from a spreadsheet name; and two
     drive tests on the copy: width 20 -> box Y 20.00 with both holes 10 / 10 from the sides; hook_depth + 5 -> the
     depth and the opening both + 5 (+-0.05)
  V  the volume 17,098.584 +- 1 mm3 (worked out: 14,848.584 + 15 x 5 x 30)
A run passes when C, M1-M7 and V all hold. Recorded, not deciding: the hook_depth value, any new alias, the part's
name and document, moved (the part's Placement not the identity; everything above is read with it undone), turned
(box sizes not depth x 30 x 60 in that order, after the Placement is undone).

    python3 -m checker.score_l6 READ_JSON        (prints the score as JSON)"""
import json
import sys

from checker import holes

OPENING = 45.0
OPEN_TOL = 0.05
VOLUME = 17098.584
VOL_TOL = 1.0
NAMES = {'width': 30.0, 'thickness': 5.0, 'lip_height': 10.0, 'plate_height': 60.0, 'hole_d': 4.0, 'hole_spacing': 30.0}
START_BINDINGS = [('Sketch', 'Constraints[%d]' % i) for i in range(17, 23)] + [
    ('Pad', 'Length'), ('Sketch001', 'Constraints[2]'), ('Sketch001', 'Constraints[3]'), ('Sketch001', 'Constraints[4]'),
    ('Sketch001', 'Constraints[5]'), ('Hole', 'Diameter')]
LINES = ('C', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'V')


def _aliases(r):
    out = {}
    for s in r.get('sheets') or []:
        out.update(s.get('aliases') or {})
    return out


def _sheet_exprs(r):
    names = set()
    for s in r.get('sheets') or []:
        names.update({s['name'] + '.', s['label'] + '.', '<<' + s['label'] + '>>.'})
    return [e for e in r.get('expressions') or [] if any(n in e['expression'] for n in names)]


def _holes(sol, depth):
    return holes.check(sol, dict(holes.NAMES, width=round(sol['bbox_mm'][1], 4), hook_depth=depth))


def score(r):
    if not r or not r.get('part'):
        return {'pass': False, 'lines': {k: False for k in LINES}, 'why': {'part': 'no solid part found'}}
    sol, g = r['solid'], r['geometry']
    p = g['points']
    depth = sol['bbox_mm'][0]
    h = _holes(sol, depth)
    st = r.get('stl') or {}
    al = _aliases(r)
    ex = _sheet_exprs(r)
    dr = r.get('drive') or {}
    dh = _holes(dr['solid'], dr['solid']['bbox_mm'][0]) if dr.get('done') else None
    why = {}
    lines = {}
    lines['C'] = g.get('opening_mm') is not None and abs(g['opening_mm'] - OPENING) <= OPEN_TOL
    why['C'] = 'opening %s' % g.get('opening_mm')
    lines['M1'] = (sol['solids'] == 1 and sol['valid'] and not r.get('errors') and st.get('closed') is True
                   and st.get('components') == 1 and st.get('non_manifolds') is False)
    why['M1'] = 'solids %s valid %s errors %s stl %s' % (sol['solids'], sol['valid'], r.get('errors'), st)
    lines['M2'] = abs(sol['bbox_mm'][1] - 30.0) <= 0.01 and abs(sol['bbox_mm'][2] - 60.0) <= 0.01
    why['M2'] = 'box %s' % sol['bbox_mm']
    lines['M3'] = all(p[k + '_in'] and not p[k + '_out'] for k in ('plate', 'base', 'lip'))
    lines['M4'] = p['lip_top_in'] and not p['lip_top_out']
    why['M3/M4'] = p
    m5 = [m for m in h['misses'] if m in ('holes', 'hole size', 'centred', 'heights', 'through')]
    lines['M5'] = not m5
    why['M5'] = {'misses': m5, 'hole_d': h['hole_d'], 'heights': h['hole_heights_mm'], 'sides': h['hole_sides_mm']}
    lines['M6'] = bool(h['fillet_on_lip_edge'])
    names_ok = all(k in al and isinstance(al[k], (int, float)) and abs(al[k] - v) <= 1e-6 for k, v in NAMES.items())
    hd = al.get('hook_depth')
    depth_ok = isinstance(hd, (int, float)) and abs(hd - depth) <= 0.01
    bound = {(e['object'], e['property']) for e in ex}
    lost = [b for b in START_BINDINGS if b not in bound]
    drive_ok = bool(dh) and abs(dr['solid']['bbox_mm'][1] - 20.0) <= 0.01 and dh['centred'] and not dr.get('errors') \
        and len(dh['hole_sides_mm']) == 2 and all(s == [10.0, 10.0] for s in dh['hole_sides_mm'])
    d2 = r.get('drive_depth') or {}
    depth2_ok = (bool(d2.get('done')) and abs(d2['solid']['bbox_mm'][0] - depth - 5) <= 0.05
                 and g.get('opening_mm') is not None and d2['geometry'].get('opening_mm') is not None
                 and abs(d2['geometry']['opening_mm'] - g['opening_mm'] - 5) <= 0.05)
    lines['M7'] = names_ok and depth_ok and not lost and drive_ok and depth2_ok
    why['M7'] = {'names_ok': names_ok, 'hook_depth': hd, 'depth_ok': depth_ok, 'lost_bindings': lost,
                 'sheet_expressions': len(ex), 'drive_ok': drive_ok, 'drive_depth_ok': depth2_ok,
                 'drive_box': dr.get('solid', {}).get('bbox_mm') if dr.get('done') else None,
                 'drive_sides': dh['hole_sides_mm'] if dh else None}
    lines['V'] = abs(sol['volume_mm3'] - VOLUME) <= VOL_TOL
    why['V'] = sol['volume_mm3']
    lines = {k: bool(v) for k, v in lines.items()}
    return {'pass': all(lines.values()), 'lines': lines, 'why': why, 'hook_depth': al.get('hook_depth'),
            'new_aliases': sorted(set(al) - set(NAMES) - {'hook_depth'}), 'part': r['part'], 'document': r['document'],
            'moved': bool(r.get('moved')),
            'turned': not (abs(sol['bbox_mm'][1] - 30) < 0.01 and abs(sol['bbox_mm'][2] - 60) < 0.01),
            'volume_mm3': sol['volume_mm3'], 'opening_mm': g.get('opening_mm')}


def pick_read(reads, start='hook_lesson5'):
    """reads: {document name: l6read result}. The start document's part, unless it is unchanged (opening still 30) and
    another document holds a part: then that one (a run that built a new document)."""
    first = reads.get(start)
    others = {k: v for k, v in reads.items() if k != start and v.get('part')}
    unchanged = not first or not first.get('part') or abs((first['geometry'].get('opening_mm') or 0) - 30.0) <= 0.05
    if unchanged and others:
        k = sorted(others)[-1]
        return k, others[k], True
    return start, first, False


def score_run(run_dir):
    """A Claude run's folder: read-<doc>.json for every document saved after the turn; session.jsonl for the replies;
    transcript.jsonl for the calls. Writes nothing; returns the score with the run's replies and calls."""
    import glob
    import os
    from checker import score_l5
    reads = {os.path.basename(p)[5:-5]: json.load(open(p, encoding='utf-8'))
             for p in glob.glob(os.path.join(run_dir, 'read-*.json'))}
    doc, r, new = pick_read(reads)
    out = score(r)
    out['scored_document'] = doc
    out['new_document'] = new
    out['documents'] = sorted(reads)
    out['replies'] = score_l5.replies(os.path.join(run_dir, 'session.jsonl'))
    calls = []
    tp = os.path.join(run_dir, 'transcript.jsonl')
    if os.path.exists(tp):
        for line in open(tp, encoding='utf-8'):
            try:
                m = json.loads(line).get('msg')
            except ValueError:
                continue
            if isinstance(m, dict) and m.get('method') == 'tools/call':
                calls.append({'tool': (m.get('params') or {}).get('name'),
                              'arguments': (m.get('params') or {}).get('arguments')})
    out['calls'] = calls
    for k in ('start.md5', 'start-after.md5'):
        p = os.path.join(run_dir, k)
        out[k] = open(p).read().split()[0] if os.path.exists(p) else None
    out['start_file_saved_over'] = bool(out['start.md5'] and out['start-after.md5'] and out['start.md5'] != out['start-after.md5'])
    return out


if __name__ == '__main__':
    import os
    a = sys.argv[1]
    if os.path.isdir(a):
        res = score_run(a)
        json.dump(res, open(os.path.join(a, 'score.json'), 'w', encoding='utf-8'), indent=1)
        print(json.dumps({k: res[k] for k in ('pass', 'lines', 'scored_document', 'hook_depth', 'opening_mm', 'volume_mm3')}, indent=1))
    else:
        print(json.dumps(score(json.load(open(a, encoding='utf-8'))), indent=1))
