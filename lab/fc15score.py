"""fc15 Claude-run pass rule (PLAN rev 2 section 2.5), on lab/fc15parts.py snap() dicts of the cup's Body at wall 2, 3, 1.6.

passes({2: snap, 3: snap, 1.6: snap}) -> (bool, {wall: {criterion: bool, 'sum': .., 'sum_fraction': ..}}):
  (a) builds: no Invalid / Error feature, Tip = last feature, Body.Shape valid, one solid (snap['builds'])
  (b) both edges rounded: a round face (radius read) on the outer AND the inner rim loop
  (c) reported only: r_out + r_in read, and as a fraction of the wall (G0 Q3: an equal sum fails in FreeCAD 1.1.4)
  (d) inside 60 x 40 x 50, outside 60 + 2 * wall at z 25, peg 10 x 10 solid
  (e) `wall` is the value the scorer set
Pass = (a), (b), (d), (e) at all three walls."""


def _near(a, b, tol=0.01):
    return a is not None and abs(a - b) <= tol


def criteria(s, wall):
    if not s or 'error' in s or 'rim' not in s or 'error' in s['rim']:
        return {k: False for k in 'abde'}
    r = s['rim']
    ro = (r.get('round_radii') or {}).get('out') or []
    ri = (r.get('round_radii') or {}).get('in') or []
    c = {
        'a': bool(s.get('builds')),
        'b': bool(ro) and bool(ri),
        'd': _near(r.get('inside_w'), 60) and _near(r.get('m_inside_l'), 40) and _near(r.get('m_inside_d'), 50, 0.1)
        and _near(r.get('outside_w'), 60 + 2 * wall) and _near(r.get('m_peg_w'), 10) and bool(r.get('m_peg_mid_solid')),
        'e': _near(r.get('wall'), wall),
    }
    if ro and ri:
        c['sum'] = round(max(ro) + max(ri), 4)
        c['sum_fraction'] = round(c['sum'] / wall, 4)
    return c


def passes(at):
    det = {w: criteria(s, w) for w, s in at.items()}
    ok = all(det[w][k] for w in det for k in 'abde')
    return ok, det
