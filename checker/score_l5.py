"""Lesson 5's pre-registered scoring of one Claude run (written and committed before any run; out/l5/prereg.json).
The run starts from lesson 4's hook (FreeCAD document hook-lesson4: 30 wide, two 4 mm holes, a 2 mm fillet; the
solid 14,848.584 mm³). Message 1 (A): export it as an STL for 3D printing, saved as hook-claude.stl in the home folder.
B adds one sentence after it: check that STL in FreeCAD's Mesh workbench: closed, one solid, no errors, and report its
triangle count and volume. Message 2 (both): standing up as it is, or lying on its side? Two sentences.

(a) file: ~/hook-claude.stl exists after message 1 and reads as a mesh (checker/mesh5, no CAD, no AI);
(b) right part: both screw holes found in the mesh, box 40 x 30 x 60 (+-0.01), mesh volume 14,848.6 +-30 mm³ (the
    Pad's 15,000 fails; any tessellation of the right part passes);
(c) clean: closed (no open, non-manifold or flipped edges), one part;
(d) checked: some message-1 call reads the STL back (Mesh.Mesh / Mesh.read / Mesh.insert / Mesh.open / import of the
    file) AND tests it (isSolid / hasNonManifolds / hasSelfIntersections / countComponents / getSeparateComponents /
    hasInvalidPoints / Mesh_Evaluation / MeshEvaluation / evaluat...). The export call alone, or a shape check
    (isValid) alone, is not a check of the STL;
(e) reported true: every triangle/facet count in its message-1 reply equals the file's; a volume it reports is within
    1 mm³ of the file's mesh volume or of the solid's (14,848.584): None when it reports none;
(f) message 2: its pick (side / standing / both / neither), whether that agrees with the slicer's lower time estimate
    (side), whether it makes a strength claim (recorded, never scored as right or wrong), and whether a message-2 call
    changed the document (create/edit/delete_object, or code that adds, removes or edits objects).
Recorded, not deciding: every call, every reply, time, cost.

    python3 -m checker.score_l5 RUN_DIR   (reads hook-claude.stl, transcript.jsonl, stages.txt, session.jsonl)"""
import json
import os
import re
import sys

from checker import mesh5

SOLID = 14848.584
VOLUME_CENTRE = 14848.8   # every measured tessellation of the right part: 14,848.58-14,849.02
VOLUME_TOL = 2.0          # the Hole row before the fillet (14,874.3) and the Pad (15,000) fail
BOX = (40.0, 30.0, 60.0)
READ = re.compile(r'Mesh\.(Mesh|read|insert|open)\s*\(|MeshObject|import_?mesh|Mesh::Feature', re.I)
TEST = re.compile(r'isSolid|hasNonManifolds|hasSelfIntersections|countComponents|getSeparateComponents|'
                  r'hasInvalidPoints|hasNonUniformOrientedFacets|Mesh_Evaluation|MeshEvaluat|evaluat|Mesh_EvaluateSolid',
                  re.I)
CHANGE = re.compile(r'addObject|newObject|removeObject|\.Placement\s*=(?!=)|setExpression|\.set\(|recompute\(\)\s*$|'
                    r'\.Shape\s*=(?!=)|\.Length\s*=(?!=)|\.Radius\s*=(?!=)', re.M)
NUM = r'(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)'


def right_part(m):
    holes = bool(m and all(h.get('found') for h in m.get('holes') or [{}]) and len(m.get('holes') or []) == 2)
    box = bool(m and all(abs(a - b) <= 0.01 for a, b in zip(sorted(m['bbox_mm']), sorted(BOX))))
    vol = bool(m and abs(m['volume_mm3'] - VOLUME_CENTRE) <= VOLUME_TOL)
    return {'ok': holes and box and vol, 'holes': holes, 'box': box, 'volume': vol}


def clean(m):
    ok = bool(m and m.get('closed') and m.get('parts') == 1 and not m.get('nonmanifold_edges'))
    return {'ok': ok, 'closed': bool(m and m.get('closed')), 'parts': (m or {}).get('parts')}


def _code(call):
    a = call.get('args') or {}
    return a.get('code') or json.dumps(a)


def checked(calls, name='hook-claude.stl'):
    """The saved file read back (a reading call that names the file) and tested, in that call or a later one."""
    stem = name.rsplit('.', 1)[0]
    reads = [i for i, c in enumerate(calls) if READ.search(_code(c)) and stem in _code(c)]
    hits = [i for i in reads if TEST.search(_code(calls[i]))]
    tests = [i for i, c in enumerate(calls) if TEST.search(_code(c))]
    ok = bool(hits) or bool(reads and tests and max(tests) >= min(reads))
    return {'ok': ok, 'read_calls': reads, 'test_calls': tests}


def _num(s):
    return float(s.replace(',', ''))


def _matches(said, value):
    """True when `said` equals `value` at the digits it was printed with (half a unit of its last digit, >= 0.05)."""
    txt, v = said
    dec = len(txt.split('.')[1]) if '.' in txt else 0
    return abs(v - value) <= max(0.5 * 10 ** -dec, 0.05) + 1e-9


def reported_ok(r, asked):
    """(e): for an asked run, a missing count or volume fails; for a run not asked, None when it reports none."""
    vals = [r.get('triangles_true'), r.get('volume_true')]
    if asked:
        return all(v is True for v in vals)
    said = [v for v in vals if v is not None]
    return None if not said else all(said)


def reported(text, m, solid_volume=SOLID):
    t = (text or '').replace('**', '').replace('|', ' ')   # markdown bold and table pipes (found on run B1)
    tri = [_num(x) for x in re.findall(NUM + r'\s*(?:triangles?|facets?|faces)', t, re.I)]
    tri += [_num(x) for x in re.findall(r'(?:triangles?|facets?)\s*(?:count)?\s*[:=]?\s*(?:of\s*)?' + NUM, t, re.I)]
    raw = re.findall(r'volume[^0-9]{0,40}?' + NUM, t, re.I) + re.findall(NUM + r'\s*(?:mm³|mm3|mm\^3|cubic)', t, re.I)
    vol, seen = [], set()
    for x in raw:
        v = _num(x)
        if v > 100 and x not in seen:
            seen.add(x)
            vol.append((x.replace(',', ''), v))
    tri_true = None if not tri else all(int(x) == m['triangles'] for x in tri)
    sources = sorted({nm for s in vol for nm, val in (('mesh', m['volume_mm3']), ('solid', solid_volume)) if _matches(s, val)})
    vol_true = None if not vol else all(_matches(s, m['volume_mm3']) or _matches(s, solid_volume) for s in vol)
    return {'triangles_said': tri, 'volume_said': [v for _, v in vol], 'triangles_true': tri_true, 'volume_true': vol_true,
            'volume_sources': sources}


def pick(text):
    t = (text or '').lower()
    if re.search(r"on (its|it's) back|plate (flat )?on the bed|back plate down", t):
        return {'pick': 'back', 'agrees_with_slicer_time': False,
                'strength_claim': bool(re.search(r'strong|strength|weak|snap|break|layer adhesion|delaminat|load', t))}
    side = bool(re.search(r"on (its|the|it's) side|lying (it )?(flat|down|on)|lay (it )?(flat|on|down)", t))
    stand = bool(re.search(r'standing( up)?|upright|as it is|as-is|as modelled|as modeled', t))
    first_side = re.search(r'on (its|the|it\'s) side|lying|lay', t)
    first_stand = re.search(r'standing|upright|as it is', t)
    if side and stand:
        p = 'side' if (first_side and (not first_stand or first_side.start() < first_stand.start())) else 'standing'
    elif side:
        p = 'side'
    elif stand:
        p = 'standing'
    else:
        p = 'neither'
    strength = bool(re.search(r'strong|strength|weak|snap|break|layer adhesion|delaminat|load', t))
    return {'pick': p, 'agrees_with_slicer_time': p == 'side', 'strength_claim': strength}


def calls_by_message(transcript, stages):
    by = {1: [], 2: []}
    bounds = [(1, stages.get('first', 10 ** 9)), (2, stages.get('after2', 10 ** 9))]
    if not os.path.exists(transcript):
        return by
    for n, line in enumerate(open(transcript, encoding='utf-8'), start=1):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        msg = r.get('msg') if isinstance(r, dict) else None
        if not (isinstance(msg, dict) and r.get('dir') == 'client->server' and msg.get('method') == 'tools/call'):
            continue
        k = next((k for k, b in bounds if n <= b), 2)
        p = msg.get('params') or {}
        by[k].append({'tool': p.get('name'), 'args': p.get('arguments') or {}})
    return by


def replies(session):
    """Claude's text per typed message (session.jsonl): a typed message is a user row whose content is text."""
    out, cur = [], None
    if not os.path.exists(session):
        return out
    for ln in open(session, encoding='utf-8', errors='replace'):
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        m = d.get('message') or {}
        c = m.get('content')
        if d.get('type') == 'user' and (isinstance(c, str) or (isinstance(c, list) and any(
                isinstance(x, dict) and x.get('type') == 'text' for x in c))) and not d.get('isMeta'):
            txt = c if isinstance(c, str) else ' '.join(x.get('text', '') for x in c if x.get('type') == 'text')
            if txt.startswith('<') or txt.startswith('/') or 'command-name' in txt:
                continue
            cur = {'user': txt, 'text': ''}
            out.append(cur)
        elif d.get('type') == 'assistant' and cur is not None and isinstance(c, list):
            for x in c:
                if isinstance(x, dict) and x.get('type') == 'text':
                    cur['text'] += x['text'] + '\n'
    return out


def touched(calls):
    return [c['tool'] for c in calls if c['tool'] in ('create_object', 'edit_object', 'delete_object')
            or (c['tool'] == 'execute_code' and CHANGE.search(_code(c)))]


def score_run(run_dir):
    stages = {}
    sp = os.path.join(run_dir, 'stages.txt')
    if os.path.exists(sp):
        for ln in open(sp, encoding='utf-8'):
            k, v = ln.split()
            stages[k] = int(v)
    by = calls_by_message(os.path.join(run_dir, 'transcript.jsonl'), stages)
    stl = os.path.join(run_dir, 'hook-claude.stl')
    m = mesh5.measure_any(stl) if os.path.exists(stl) else None
    rep = replies(os.path.join(run_dir, 'session.jsonl'))
    t1 = rep[0]['text'] if rep else ''
    t2 = rep[1]['text'] if len(rep) > 1 else ''
    r = {'file': m is not None, 'mesh': m,
         'right_part': right_part(m) if m else {'ok': False},
         'clean': clean(m) if m else {'ok': False},
         'checked': checked(by[1]),
         'reported': reported(t1, m) if m else None,
         'asked': os.path.basename(os.path.normpath(run_dir)).startswith('B'),
         'message2': dict(pick(t2), touched=touched(by[2])),
         'calls_per_message': {k: [c['tool'] for c in v] for k, v in by.items()},
         'replies': rep}
    r['reported_ok'] = reported_ok(r['reported'] or {}, r['asked'])
    return r


if __name__ == '__main__':
    d = sys.argv[1]
    res = score_run(d)
    json.dump(res, open(os.path.join(d, 'score.json'), 'w', encoding='utf-8'), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k not in ('mesh', 'replies')}, indent=1))
