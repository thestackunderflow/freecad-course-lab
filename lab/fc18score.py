"""fc18 Claude-run pass rule (PLAN rev 2 section 2.5), on lab/fc18parts.py snaps of the cup at three settings of
`cup_diameter`: '60', '80', '45' (cup_height 80 and wall 2 as in the start file).

criteria(s, dia) -> {criterion: bool}:
  (a) outside x and y extent = cup_diameter +- 0.01
  (b) height 80 +- 0.01, standing z 0..80
  (c) inside diameter cup_diameter - 2 wall at z 40 (ring probes: radius r - wall + 0.05 material, r - wall - 0.05 air,
      r + 0.05 air, five directions) and the floor (0, 0, wall / 2) material, (0, 0, wall + 1) air
  (d) one solid, top open, builds (no object Invalid / Error, valid shape)
Pass = (a)-(d) at all three settings. Reported beside it (not part of pass): (e) made by a PartDesign Revolution inside
the Body; (f) the width setting reads cup_diameter (any expression or Params cell that names it).
cls(...) -> the PLAN 2.5 class: 1 width = cup_diameter / 2 (or a radius name that follows it), 2 typed 30, 3 width =
cup_diameter (the trap), 4 not a revolve, 6 upside down / off the floor, 8 broke the file, 9 other (5 and 7 by hand)."""

SETTINGS = {'60': 60.0, '80': 80.0, '45': 45.0}


def _near(a, b, tol=0.01):
    return a is not None and b is not None and abs(a - b) <= tol


def criteria(s, dia, h=80.0):
    if not s or 'error' in s or 'm' not in s or 'error' in (s.get('m') or {}):
        return {k: False for k in 'abcd'}
    m = s['m']
    z = m.get('z') or [None, None]
    return {
        'a': _near(m.get('outside_x'), dia) and _near(m.get('outside_y'), dia),
        'b': _near(z[0], 0) and _near(z[1], h),
        'c': bool(m.get('ring_ok')) and bool(m.get('floor_ok')),
        'd': m.get('solids') == 1 and bool(m.get('top_open')) and bool(s.get('builds')),
    }


def criteria_ok(at):
    det = {k: criteria(at.get(k), v) for k, v in SETTINGS.items()}
    return all(all(v.values()) for v in det.values()), det


def cls(at, ok, revolve, broke=False):
    if broke:
        return 8
    if ok:
        return 1 if revolve else 4
    m = lambda k: ((at.get(k) or {}).get('m') or {})
    o60, o80 = m('60').get('outside_x'), m('80').get('outside_x')
    z60 = m('60').get('z') or [None, None]
    if _near(o60, 120, 0.05) and _near(o80, 160, 0.05):
        return 3
    if _near(o60, 60, 0.05) and _near(o80, 60, 0.05):
        return 2
    if _near(o60, 60, 0.05) and z60[0] is not None and (z60[1] < 1 or z60[0] < -1):
        return 6
    return 9
