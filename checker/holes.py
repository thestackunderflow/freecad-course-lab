"""Lesson 4: two screw holes through the hook's back plate and a fillet on the lip's top outer edge, worked out without
CAD, and the round faces of a measured solid read back as holes and a fillet.

The start is lesson 3's hook as lesson 3 ends it (hook_depth 40, thickness back to 5; 10,000 mm3). Two holes of
diameter hole_d go straight through the back plate (thickness thick), centred across the plate's width, hole_spacing
apart and centred on the plate's height; then a fillet of radius r rounds the lip's top outer edge (the corner where
the lip's top meets its front), along the whole width.
  holes  : 2 x pi x (hole_d / 2)^2 x thickness
  fillet : (r^2 - pi r^2 / 4) x width       (the square corner minus the quarter circle, pushed along the width)
checker/measure.py lists every cylindrical face of a solid (radius, axis, a point on the axis, area): a face whose axis
runs front-to-back through the plate (X) is a hole; one whose axis runs along the width (Y) is a fillet."""
import math

from checker import outline

NAMES = {'plate_height': 60, 'width': 20, 'thickness': 5, 'hook_depth': 40, 'lip_height': 10, 'hole_d': 4,
         'hole_spacing': 30}
FILLET_R = 2.0
TOL = 0.05


def expected(names=None, fillet_r=FILLET_R):
    n = dict(NAMES, **(names or {}))
    j = outline.expected(outline.named_moves(n), n['width'])
    hole = 2 * math.pi * (n['hole_d'] / 2.0) ** 2 * n['thickness']
    fil = (fillet_r ** 2 - math.pi * fillet_r ** 2 / 4.0) * n['width']
    return {'volume_mm3': j['volume_mm3'] - hole - fil, 'bbox_mm': j['bbox_mm'],
            'hole_heights_mm': [(n['plate_height'] - n['hole_spacing']) / 2.0,
                                (n['plate_height'] + n['hole_spacing']) / 2.0],
            'hole_from_side_mm': n['width'] / 2.0,
            'fillet_axis_xz': [float(n['hook_depth']) - fillet_r, float(n['lip_height']) - fillet_r]}


def _along(axis, i):
    return abs(abs(axis[i]) - 1.0) < 1e-3


def read(sol):
    """The holes (axis along X) and fillet faces (axis along Y) of one measured solid."""
    hs, fs = [], []
    for c in sol.get('cylinders') or []:
        if _along(c['axis'], 0):
            key = (round(c['center'][1], 3), round(c['center'][2], 3))
            if key not in [(round(h['y'], 3), round(h['z'], 3)) for h in hs]:
                hs.append({'d': round(2 * c['r'], 4), 'y': c['center'][1], 'z': c['center'][2], 'area': c['area'],
                           'r': c['r']})
        elif _along(c['axis'], 1):
            fs.append({'r': c['r'], 'x': c['center'][0], 'z': c['center'][2], 'area': c['area']})
    hs.sort(key=lambda h: h['z'])
    return hs, fs


def check(sol, names=None, fillet_r=FILLET_R):
    n = dict(NAMES, **(names or {}))
    e = expected(n, fillet_r)
    hs, fs = read(sol)
    y0, y1 = sol['min_mm'][1], sol['max_mm'][1]
    x1 = sol['max_mm'][0]
    mid = (y0 + y1) / 2.0
    misses = []
    if len(hs) != 2:
        misses.append('holes')
    if not hs or any(abs(h['d'] - n['hole_d']) > 0.01 for h in hs):
        misses.append('hole size')
    centred = bool(hs) and all(abs(h['y'] - mid) <= TOL for h in hs)
    if not centred:
        misses.append('centred')
    if [round(h['z'], 2) for h in hs] != [round(z, 2) for z in e['hole_heights_mm']]:
        misses.append('heights')
    through = bool(hs) and all(h['area'] >= 2 * math.pi * h['r'] * n['thickness'] - 0.01 for h in hs)
    if not through:
        misses.append('through')
    on_edge = any(abs(f['r'] - fillet_r) <= 0.01 and abs(f['x'] - (x1 - fillet_r)) <= TOL
                  and abs(f['z'] - (n['lip_height'] - fillet_r)) <= TOL
                  and abs(f['area'] - math.pi * fillet_r / 2.0 * (y1 - y0)) <= 0.05 for f in fs)
    if not on_edge:
        misses.append('fillet')
    if abs(sol['volume_mm3'] - e['volume_mm3']) > 0.1:
        misses.append('volume')
    if any(abs(a - b) > 0.01 for a, b in zip(sol['bbox_mm'], e['bbox_mm'])):
        misses.append('size')
    return {'ok': not misses, 'misses': misses, 'holes': len(hs), 'hole_d': [h['d'] for h in hs],
            'hole_heights_mm': [round(h['z'], 3) for h in hs],
            'hole_sides_mm': [sorted([round(h['y'] - y0, 3), round(y1 - h['y'], 3)]) for h in hs],
            'centred': centred, 'through': through, 'fillet_on_lip_edge': on_edge,
            'volume_mm3': sol['volume_mm3'], 'expected_mm3': round(e['volume_mm3'], 4)}
