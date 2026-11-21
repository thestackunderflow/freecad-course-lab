"""fc16 Claude-run pass rule (PLAN rev 2 section 2.5), on lab/fc16parts.py snap() dicts of the cup's Body at wall 2, 3, 12.

passes({2: snap, 3: snap, 12: snap}) -> (bool, {wall: {criterion: bool}}):
  (a) back hole open: axis points (x 0, z 30) at y 20.05, 20 + wall / 2, 20 + wall - 0.05 are air
  (b) front wall point (0, -20 - wall / 2, 30) is material
  (c) hole 5 across at y 20 + wall / 2 (x +-2.4 air, +-2.6 material)
  (d) builds, peg (0, -34, 40) material, inside 60 x 40 +-0.01, 50 deep, top open, one solid
  (e) `wall` is the value the scorer set and the outside x extent at z 25 is 60 + 2 * wall
  (f) the depth setting, read by code, follows the wall: Type Length with an expression reading Params.wall, or
      Type UpToFirst / UpToFace (on the inside back face)
Pass = (a)-(f) at all three walls."""


def _near(a, b, tol=0.01):
    return a is not None and abs(a - b) <= tol


def follows_wall(dp):
    if not dp:
        return False
    t = dp.get('type')
    if t == 'Length':
        e = dp.get('expr') or ''
        return 'wall' in e
    return t in ('UpToFirst', 'UpToFace')


def criteria(s, wall):
    if not s or 'error' in s or 'hole' not in s or 'error' in (s.get('hole') or {}):
        return {k: False for k in 'abcdef'}
    h = s['hole']
    return {
        'a': all((h.get('axis_air') or {'x': False}).values()),
        'b': bool(h.get('front_solid')),
        'c': bool(h.get('dia_ok')),
        'd': bool(s.get('builds')) and bool(h.get('peg_solid')) and h.get('solids') == 1 and _near(h.get('inside_w'), 60)
        and _near(h.get('inside_l'), 40) and _near(h.get('inside_d'), 50, 0.1) and bool(h.get('top_open')),
        'e': _near(s.get('wall'), wall) and _near(h.get('outside_w'), 60 + 2 * wall),
        'f': follows_wall(s.get('depth')),
    }


def passes(at):
    det = {w: criteria(s, w) for w, s in at.items()}
    ok = all(det[w][k] for w in det for k in 'abcdef')
    return ok, det
