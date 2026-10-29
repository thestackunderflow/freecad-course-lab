"""Compare two measured blocks (each from checker/measure.py, the same freecadcmd line run on a saved document):
the hand-made one and Claude's (or the replay's). Rows: volume (and the expected volume), size, position, which way is
up (Z range), validity. Any name is fine: Claude may call its block anything.

    python3 -m checker.compare HAND.json CLAUDE.json OUT.json [EXPECTED]"""
import json
import sys

TOL = 1e-6


def final_solids(m):
    """The part itself: solids no other object is built from (a Part Design Body, not its Pad feature inside it;
    lesson 1's plain block). Rows without an in_list (older measure files) all count."""
    s = m.get('solids') or []
    top = [r for r in s if not r.get('in_list')]
    return top or s


def _one(m):
    s = final_solids(m)
    if len(s) != 1:
        raise ValueError(f"{m.get('document')}: expected exactly one solid, found {len(s)}")
    return s[0]


def _close(a, b):
    return all(abs(x - y) <= TOL * max(1.0, abs(x), abs(y)) for x, y in zip(a, b)) and len(a) == len(b)


def compare(hand, claude, expected=None, any_axis_order=False):
    a, b = _one(hand), _one(claude)
    va, vb = round(a['volume_mm3'], 4), round(b['volume_mm3'], 4)
    rows = {}
    ok_v = abs(va - vb) <= TOL * max(1.0, va) and (expected is None or abs(va - expected) <= TOL * max(1.0, expected))
    rows['volume'] = {'hand': va, 'claude': vb, 'expected': expected, 'ok': ok_v}
    sa, sb = a['bbox_mm'], b['bbox_mm']
    ok_s = _close(sorted(sa), sorted(sb)) if any_axis_order else _close(sa, sb)
    rows['size'] = {'hand': sa, 'claude': sb, 'ok': ok_s}
    rows['up'] = {'hand': a['z_range_mm'], 'claude': b['z_range_mm'], 'ok': _close(a['z_range_mm'], b['z_range_mm'])}
    if 'min_mm' in a and 'min_mm' in b:
        rows['position'] = {'hand': a['min_mm'], 'claude': b['min_mm'], 'ok': _close(a['min_mm'], b['min_mm'])}
    rows['valid'] = {'hand': a['valid'], 'claude': b['valid'], 'ok': bool(a['valid'] and b['valid'])}
    diffs = [k for k, r in rows.items() if not r['ok']]
    return {'same': not diffs, 'differences': diffs, 'rows': rows,
            'upright': {'hand': _upright(a), 'claude': _upright(b)},
            'sketch': {'hand': _sketch(hand), 'claude': _sketch(claude)},
            'documents': {'hand': hand.get('document'), 'claude': claude.get('document')},
            'names': {'hand': [a['name'], a.get('label')], 'claude': [b['name'], b.get('label')]}}


def _upright(s):
    """Stands on the floor and rises: its lowest point at Z 0 (or above), its highest above that; and not mirrored:
    the hook's lip on the +X side (its box starts at X 0 or more), as drawn on XZ."""
    z0, z1 = s['z_range_mm']
    x0 = (s.get('min_mm') or [0.0])[0]
    return z0 >= -TOL and z1 > z0 and x0 >= -TOL


def _sketch(m):
    sk = m.get('sketches') or []
    if not sk:
        return None
    k = sk[0]
    sup = k.get('support') or []
    subs = [s for s in (sup[0][1] if sup else []) if s]
    return {'plane': (subs[0] if subs else sup[0][0]) if sup else None, 'constraints': k.get('constraints'),
            'fully_constrained': k.get('fully_constrained'), 'up_vector': k.get('up_vector'), 'lines': k.get('geometry')}


if __name__ == '__main__':
    h, c = (json.load(open(p, encoding='utf-8')) for p in sys.argv[1:3])
    exp = float(sys.argv[4]) if len(sys.argv) > 4 else None
    r = compare(h, c, exp)
    json.dump(r, open(sys.argv[3], 'w', encoding='utf-8'), indent=1)
    print(json.dumps(r, indent=1))
