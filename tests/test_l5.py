"""Lesson 5 lab checks (unit tests; no display, no network, no Claude): the STL checker (closed, parts, volume, the
hook's holes as polygons), the live cost guard's estimate, the slicer preset flattener, and the pre-registered scoring
of a Claude run (score_l5)."""
import json
import math
import os
import struct
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, LAB)

from checker import mesh5  # noqa: E402
from lab import costguard  # noqa: E402

CUBE_V = [(0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0), (0, 0, 10), (10, 0, 10), (10, 10, 10), (0, 10, 10)]
CUBE_F = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6),
          (3, 0, 4), (3, 4, 7)]


def write_stl(path, tris, ascii_=False):
    if ascii_:
        with open(path, 'w') as f:
            f.write('solid t\n')
            for t in tris:
                f.write(' facet normal 0 0 0\n  outer loop\n')
                for v in t:
                    f.write('   vertex %f %f %f\n' % tuple(v))
                f.write('  endloop\n endfacet\n')
            f.write('endsolid t\n')
        return
    with open(path, 'wb') as f:
        f.write(b'\0' * 80 + struct.pack('<I', len(tris)))
        for t in tris:
            f.write(struct.pack('<3f', 0, 0, 0))
            for v in t:
                f.write(struct.pack('<3f', *v))
            f.write(b'\0\0')


def cube(offset=(0, 0, 0)):
    return [[tuple(np.add(CUBE_V[i], offset)) for i in f] for f in CUBE_F]


def prism_hole_plate(sides, d=4.0):
    """A 5 x 30 x 60 plate (x 0..5, y -30..0, z 0..60) is too much to triangulate by hand; instead: the hole's wall
    only, a regular polygon prism along X at (y -15, z 15), corners on the d circle, as the checker reads it."""
    tris = []
    r = d / 2
    for k in range(sides):
        a0, a1 = 2 * math.pi * k / sides, 2 * math.pi * (k + 1) / sides
        p0 = (-15 + r * math.cos(a0), 15 + r * math.sin(a0))
        p1 = (-15 + r * math.cos(a1), 15 + r * math.sin(a1))
        tris.append([(0, *p0), (5, *p0), (5, *p1)])
        tris.append([(0, *p0), (5, *p1), (0, *p1)])
    return tris


# ---- the STL checker -----------------------------------------------------------------------------------------
def test_a_closed_cube_binary(tmp_path):
    p = str(tmp_path / 'c.stl')
    write_stl(p, cube())
    m = mesh5.measure(p)
    assert m['triangles'] == 12 and abs(m['volume_mm3'] - 1000.0) < 1e-6
    assert m['closed'] and m['parts'] == 1 and m['open_edges'] == 0 and m['bbox_mm'] == [10.0, 10.0, 10.0]


def test_ascii_reads_the_same(tmp_path):
    p = str(tmp_path / 'c.ast')
    write_stl(p, cube(), ascii_=True)
    m = mesh5.measure(p)
    assert m['triangles'] == 12 and abs(m['volume_mm3'] - 1000.0) < 1e-6 and m['closed']


def test_a_missing_triangle_is_open(tmp_path):
    p = str(tmp_path / 'o.stl')
    write_stl(p, cube()[:-1])
    m = mesh5.measure(p)
    assert not m['closed'] and m['open_edges'] == 3


def test_a_flipped_triangle_is_not_closed(tmp_path):
    t = cube()
    t[0] = [t[0][0], t[0][2], t[0][1]]
    p = str(tmp_path / 'f.stl')
    write_stl(p, t)
    m = mesh5.measure(p)
    assert not m['closed'] and m['flipped_edges'] == 3


def test_two_cubes_are_two_parts(tmp_path):
    p = str(tmp_path / 'two.stl')
    write_stl(p, cube() + cube((20, 0, 0)))
    m = mesh5.measure(p)
    assert m['parts'] == 2 and m['closed'] and abs(m['volume_mm3'] - 2000.0) < 1e-6


def test_a_26_sided_hole_reads_26_sides_corners_4_flats_3_971(tmp_path):
    p = str(tmp_path / 'h.stl')
    write_stl(p, prism_hole_plate(26))
    h = mesh5.measure(p)['holes'][0]
    assert h['found'] and h['sides'] == 26
    assert abs(h['corner_d'] - 4.0) < 1e-3
    assert abs(h['flat_d'] - 4 * math.cos(math.pi / 26)) < 1e-3 and round(h['flat_d'], 2) == 3.97
    assert mesh5.measure(p)['holes'][1]['found'] is False


def test_flat_size_of_26_and_229_sides():
    assert round(mesh5.flat_d(4.0, 26), 3) == 3.971
    assert round(mesh5.flat_d(4.0, 229), 4) == 3.9996


# ---- the live cost guard ---------------------------------------------------------------------------------------
def test_cost_estimate_counts_each_message_once_and_errs_high():
    rows = [{'type': 'assistant', 'message': {'id': 'm1', 'usage': {'input_tokens': 10, 'cache_creation_input_tokens': 16102,
                                                                       'cache_read_input_tokens': 279296, 'output_tokens': 4229}}}]
    rows.append(rows[0])                       # the same message logged twice
    rows.append({'type': 'user', 'message': {'usage': {'output_tokens': 10 ** 9}}})
    tot = costguard.usage([json.dumps(r) for r in rows] + ['not json'])
    assert tot['output_tokens'] == 4229
    est = costguard.estimate(tot)
    assert 0.1479 < est < 0.30                 # lesson 4's B1: /cost $0.1479; the guard reads it high, under the cap


# ---- the slicer's stock presets ---------------------------------------------------------------------------------
BUNDLE = """[vendor]
name = x
[printer:*common*]
bed_shape = 0x0,1x0
nozzle_diameter = 0.6
[printer:*small*]
nozzle_diameter = 0.4
[printer:P]
inherits = *common*; *small*
printer_model = M
[print:*base*]
layer_height = 0.3
perimeters = 2
[print:S]
inherits = *base*
layer_height = 0.2
compatible_printers_condition = x
[filament:F]
temperature = 215
"""


def test_flatten_applies_parents_in_order_then_own_keys():
    sys.path.insert(0, os.path.join(LAB, 'slicer'))
    import flatten
    c = flatten.flatten(BUNDLE, 'P', 'S', 'F')
    assert c['nozzle_diameter'] == '0.4' and c['bed_shape'] == '0x0,1x0' and c['printer_model'] == 'M'
    assert c['layer_height'] == '0.2' and c['perimeters'] == '2' and c['temperature'] == '215'
    assert 'compatible_printers_condition' not in c and c['printer_settings_id'] == 'P'


# ---- the pre-registered scoring (score_l5) ------------------------------------------------------------------------
def _m(**kw):
    base = {'triangles': 272, 'volume_mm3': 14849.019, 'bbox_mm': [40.0, 30.0, 60.0], 'closed': True, 'parts': 1,
            'nonmanifold_edges': 0, 'open_edges': 0, 'flipped_edges': 0,
            'holes': [{'found': True, 'sides': 26}, {'found': True, 'sides': 26}]}
    base.update(kw)
    return base


def test_score_right_part_and_wrong_part():
    from checker import score_l5
    assert score_l5.right_part(_m())['ok']
    pad = _m(triangles=28, volume_mm3=15000.0, holes=[{'found': False}, {'found': False}])
    r = score_l5.right_part(pad)
    assert not r['ok'] and not r['holes'] and not r['volume']
    assert not score_l5.right_part(_m(bbox_mm=[40.0, 20.0, 60.0]))['ok']


def test_score_clean():
    from checker import score_l5
    assert score_l5.clean(_m())['ok']
    assert not score_l5.clean(_m(closed=False, open_edges=3))['ok']
    assert not score_l5.clean(_m(parts=2))['ok']


def test_score_checked_needs_a_read_back_and_a_test():
    from checker import score_l5
    good = "import Mesh\nm = Mesh.Mesh('/home/maker/hook-claude.stl')\nprint(m.isSolid(), m.hasNonManifolds())"
    assert score_l5.checked([{'tool': 'execute_code', 'args': {'code': good}}])['ok']
    only_export = "import Mesh\nMesh.export([b], '/home/maker/hook-claude.stl')\nprint(b.Shape.isValid())"
    assert not score_l5.checked([{'tool': 'execute_code', 'args': {'code': only_export}}])['ok']
    read_no_test = "import Mesh\nm = Mesh.Mesh('/home/maker/hook-claude.stl')\nprint(m.CountFacets)"
    assert not score_l5.checked([{'tool': 'execute_code', 'args': {'code': read_no_test}}])['ok']


def test_score_reported_numbers_against_the_file():
    from checker import score_l5
    m = _m()
    r = score_l5.reported("The STL has 272 triangles, volume 14,849.02 mm³, closed.", m, solid_volume=14848.584)
    assert r['triangles_true'] is True and r['volume_true'] is True
    r = score_l5.reported("It has 544 facets and a volume of 14,849 mm3.", m, solid_volume=14848.584)
    assert r['triangles_true'] is False and r['volume_true'] is True
    r = score_l5.reported("Volume 14848.58 mm³ (the solid's), 272 facets.", m, solid_volume=14848.584)
    assert r['volume_true'] is True
    r = score_l5.reported("Volume 15,000 mm³.", m, solid_volume=14848.584)
    assert r['volume_true'] is False and r['triangles_true'] is None


def test_score_message_two_pick():
    from checker import score_l5
    assert score_l5.pick("Print it lying on its side: the layers follow the J.")['pick'] == 'side'
    assert score_l5.pick("Standing up as it is, so the holes stay round.")['pick'] == 'standing'
    p = score_l5.pick("Lay it on its side; it will be much stronger than standing up.")
    assert p['pick'] == 'side' and p['strength_claim']
    assert score_l5.pick("Either works.")['pick'] == 'neither'


# ---- rev 2 after the plan gate (DECISIONS-L5 A2-A4, SHOULD) -------------------------------------------------------
def test_rev2_the_hole_row_before_the_fillet_fails_the_volume():
    from checker import score_l5
    hole_row = _m(volume_mm3=15000.0 - 2 * math.pi * 2 ** 2 * 5)   # 14,874.3: holes in, no fillet
    assert not score_l5.right_part(hole_row)['volume']
    for v in (14848.584, 14848.598, 14849.015):                    # every measured tessellation of the right part
        assert score_l5.right_part(_m(volume_mm3=v))['ok']


def test_rev2_a_turned_hook_is_found_and_marked_moved(tmp_path):
    walls = prism_hole_plate(26) + [[(x, y, z + 30) for (x, y, z) in tri] for tri in prism_hole_plate(26)]   # both holes
    t = [[(z, -y, x) for (x, y, z) in tri] for tri in walls]   # a turned copy of the two hole walls
    t += [[(0, 0, 0), (60, 0, 0), (60, 30, 0)], [(0, 0, 40), (60, 30, 40), (60, 0, 40)]]   # makes the box 60 x 30 x 40
    p = str(tmp_path / 'turned.stl')
    write_stl(p, t)
    m = mesh5.measure_any(p)
    assert m['moved'] is True and m['holes'][0]['found'] and m['holes'][0]['sides'] == 26


def test_rev2_reported_numbers_name_their_source():
    from checker import score_l5
    m = _m()
    r = score_l5.reported("Volume 14,849.02 mm³", m, solid_volume=14848.584)
    assert r['volume_true'] and r['volume_sources'] == ['mesh']
    r = score_l5.reported("Volume 14,848.58 mm³", m, solid_volume=14848.584)
    assert r['volume_true'] and r['volume_sources'] == ['solid']
    r = score_l5.reported("Volume 14,849 mm³", m, solid_volume=14848.584)
    assert r['volume_true'] and r['volume_sources'] == ['mesh', 'solid']
    r = score_l5.reported("Volume 14,848.9 mm³", m, solid_volume=14848.584)
    assert r['volume_true'] is False


def test_rev2_checked_must_read_the_saved_file_not_a_new_mesh():
    from checker import score_l5
    rebuilt = "import MeshPart\nm = MeshPart.meshFromShape(Shape=b.Shape)\nprint(m.isSolid())"
    assert not score_l5.checked([{'tool': 'execute_code', 'args': {'code': rebuilt}}], 'hook-claude.stl')['ok']
    other = "import Mesh\nm = Mesh.Mesh('/tmp/other.stl')\nprint(m.isSolid())"
    assert not score_l5.checked([{'tool': 'execute_code', 'args': {'code': other}}], 'hook-claude.stl')['ok']
    via_var = "import Mesh, os\np = os.path.expanduser('~/hook-claude.stl')\nm = Mesh.Mesh(p)\nprint(m.isSolid())"
    assert score_l5.checked([{'tool': 'execute_code', 'args': {'code': via_var}}], 'hook-claude.stl')['ok']


def test_rev2_asked_run_without_numbers_fails_e():
    from checker import score_l5
    assert score_l5.reported_ok({'triangles_true': None, 'volume_true': True}, asked=True) is False
    assert score_l5.reported_ok({'triangles_true': True, 'volume_true': True}, asked=True) is True
    assert score_l5.reported_ok({'triangles_true': None, 'volume_true': None}, asked=False) is None


def test_rev2_pick_knows_on_its_back():
    from checker import score_l5
    assert score_l5.pick("Print it flat on its back, plate on the bed.")['pick'] == 'back'
