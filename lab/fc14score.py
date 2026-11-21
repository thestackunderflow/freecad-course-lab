"""fc14 Claude-run pass rule (PLAN rev 2.1 section 2.5), on lab/fc14parts.py measure() dicts of the cup's Body.Shape.

passes(at_wall2, at_wall3) -> (bool, {criterion: bool}):
  (a) peg middle (0, -28, 40) material, peg x extent at y -30 = 10 +- 0.01, z extent 35..45 +- 0.01
  (b) front wall point (0, -cup_length / 2 - wall / 2, 40) material
  (c) cup inside 60 x 40 +- 0.01, 50 deep, face point tests (top open, bottom and sides closed)
  (d) one solid
  (e) the parameter `wall` exists and was set; outside x extent at z 25, y 0 = 64 (wall 2) / 66 (wall 3) +- 0.01
Both walls must pass every criterion."""


def _near(a, b, tol=0.01):
    return a is not None and abs(a - b) <= tol


def criteria(r, wall):
    if not r or 'error' in r:
        return {k: False for k in 'abcde'}
    pz = r.get('peg_z') or [None, None]
    return {
        'a': bool(r.get('peg_mid_solid')) and _near(r.get('peg_w'), 10) and _near(pz[0], 35) and _near(pz[1], 45),
        'b': bool(r.get('front_wall_solid')),
        'c': _near(r.get('inside_w'), 60) and _near(r.get('inside_l'), 40) and _near(r.get('inside_d'), 50)
        and bool((r.get('faces') or {}).get('ok')),
        'd': r.get('solids') == 1,
        'e': _near(r.get('wall_param'), wall) and _near(r.get('outside_w'), 60 + 2 * wall),
    }


def passes(at2, at3):
    c2, c3 = criteria(at2, 2), criteria(at3, 3)
    both = {k: c2[k] and c3[k] for k in 'abcde'}
    return all(both.values()), {'wall2': c2, 'wall3': c3}
