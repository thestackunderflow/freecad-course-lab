"""fc17 Claude-run pass rule (PLAN rev 2 section 2.5), on lab/fc17parts.py snaps of the cup's Body at four settings:
'15' (peg_x 15), '20' (peg_x 20), '8' (peg_x 8), 'w3' (peg_x 15, wall 3); `asis` = the file as saved, before the
scorer touches anything; `ref` = our fixed file's (mirror-yz) volume at the same four settings.

criteria_ok(at, asis, ref) -> (bool, {setting: {criterion: bool}}):
  (a) original (peg_x, -28, 40) material            (b) copy (-peg_x, -28, 40) material
  (c) back clear: (+-peg_x, 28, 40) air and y max = 20 + wall +- 0.01
  (d) both pegs 10 across: x +-(peg_x +- 4.9) material, +-(peg_x +- 5.1) air at y -28, z 40
  (e) inside 60 x 40 +- 0.01, 50 deep, top open, one solid, hanging hole open
  (f) peg_x is the value the scorer set               (g) back wall intact at x +-peg_x and 0 (y 20 + wall / 2, z 40)
  (h) both tips: (+-peg_x, -34.9, 40) material, (+-peg_x, -35.1, 40) air, y min -35 +- 0.01
  (i) peg height: z 40 +- (peg_size / 2 - 0.1) material, +- (peg_size / 2 + 0.1) air at x +-peg_x, y -28
  (j) volume = ref +- 0.5 mm3                         (k) as saved: names and expressions = the start file's, peg_x 15
  (l) no object in error / invalid after the recompute ("stale" otherwise)
Pass = (a)-(l) at all four settings."""

SETTINGS = {'15': 15.0, '20': 20.0, '8': 8.0, 'w3': 15.0}


def _near(a, b, tol=0.01):
    return a is not None and b is not None and abs(a - b) <= tol


def criteria(s, setting, asis, ref):
    if not s or 'error' in s or 'm' not in s or 'error' in (s.get('m') or {}):
        return {k: False for k in 'abcdefghijkl'}
    m, p = s['m'], s['m'].get('probe') or {}
    w = s.get('wall') or 0.0
    ins = m.get('inside') or [None, None, None]
    return {
        'a': bool(p.get('orig')),
        'b': bool(p.get('copy')),
        'c': not p.get('back_orig') and not p.get('back_copy') and _near(m.get('y_max'), 20 + w),
        'd': bool(p.get('across')),
        'e': _near(ins[0], 60) and _near(ins[1], 40) and _near(ins[2], 50, 0.1) and bool(m.get('top_open'))
        and m.get('solids') == 1 and bool(m.get('hole_open')),
        'f': _near(s.get('peg_x'), SETTINGS[setting]),
        'g': bool(p.get('back_wall')),
        'h': bool(p.get('tips')) and _near(m.get('y_min'), -35),
        'i': bool(p.get('height')),
        'j': _near(s.get('volume'), (ref or {}).get(setting), 0.5),
        'k': bool(asis.get('names_same')) and _near(asis.get('peg_x'), 15) and not asis.get('bad_any'),
        'l': bool(s.get('builds')) and not s.get('bad_any'),
    }


def criteria_ok(at, asis, ref):
    det = {k: criteria(at.get(k), k, asis, ref) for k in SETTINGS}
    return all(all(v.values()) for v in det.values()), det
