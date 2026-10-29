"""Lesson 2 lab checks (unit tests; no display, no network, no Claude): the J's expected numbers worked out without
CAD, which solid of a Part Design document is "the part", the comparison rows (volume, size, which way up, where),
and the sketch facts the lesson reads (plane, constraints, fully constrained)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, LAB)

from checker import compare, outline  # noqa: E402


def test_the_j_expected_numbers_without_cad():
    e = outline.expected(outline.J_MOVES, 20)
    assert e['area_mm2'] == 425.0
    assert e['volume_mm3'] == 8500.0
    assert e['bbox_mm'] == [25.0, 20.0, 60.0]
    assert e['vertices'][0] == e['vertices'][-1] == (0.0, 0.0)


def test_the_j_has_six_free_sizes_once_every_line_is_level_or_upright():
    pts = outline.walk(outline.J_MOVES)[:-1]
    xs, ys = {p[0] for p in pts}, {p[1] for p in pts}
    assert len(pts) == 8 and len(xs) == 4 and len(ys) == 4
    assert outline.free_sizes(outline.J_MOVES) == 6     # (4 - 1) x positions + (4 - 1) y positions


def _row(name, typ, vol, bbox, zr, mn, in_list=()):
    return {'name': name, 'label': name, 'type': typ, 'volume_mm3': vol, 'valid': True, 'solids': 1,
            'bbox_mm': bbox, 'z_range_mm': zr, 'min_mm': mn, 'in_list': list(in_list)}


def _doc(rows, doc='hand.FCStd', sketches=None):
    return {'document': doc, 'freecad': '1.1.4', 'objects': [r['name'] for r in rows], 'solids': rows,
            'sketches': sketches or []}


def test_the_part_is_the_body_not_its_pad_feature():
    body = _row('Body', 'PartDesign::Body', 8500.0, [25.0, 20.0, 60.0], [0.0, 60.0], [0.0, 0.0, 0.0])
    pad = _row('Pad', 'PartDesign::Pad', 8500.0, [25.0, 20.0, 60.0], [0.0, 60.0], [0.0, 0.0, 0.0], in_list=['Body'])
    assert [r['name'] for r in compare.final_solids(_doc([body, pad]))] == ['Body']
    # lesson 1's plain block (no body) still counts as the part
    box = _row('Box', 'Part::Box', 6000.0, [5.0, 20.0, 60.0], [0.0, 60.0], [0.0, 0.0, 0.0])
    assert [r['name'] for r in compare.final_solids(_doc([box]))] == ['Box']


def test_upside_down_is_a_difference_even_when_volume_and_size_match():
    up = _row('Body', 'PartDesign::Body', 8500.0, [25.0, 20.0, 60.0], [0.0, 60.0], [0.0, 0.0, 0.0])
    down = _row('Body', 'PartDesign::Body', 8500.0, [25.0, 20.0, 60.0], [-60.0, 0.0], [0.0, 0.0, -60.0])
    r = compare.compare(_doc([up]), _doc([down], doc='claude.FCStd'), expected=8500.0)
    assert r['rows']['volume']['ok'] and r['rows']['size']['ok']
    assert r['rows']['up']['ok'] is False and 'up' in r['differences']
    assert r['upright'] == {'hand': True, 'claude': False}


def test_a_pad_the_other_way_in_y_is_reported_as_position_not_as_upside_down():
    a = _row('Body', 'PartDesign::Body', 8500.0, [25.0, 20.0, 60.0], [0.0, 60.0], [0.0, -20.0, 0.0])
    b = _row('Body', 'PartDesign::Body', 8500.0, [25.0, 20.0, 60.0], [0.0, 60.0], [0.0, 0.0, 0.0])
    r = compare.compare(_doc([a]), _doc([b]), expected=8500.0)
    assert r['rows']['up']['ok'] is True and r['upright'] == {'hand': True, 'claude': True}
    assert r['differences'] == ['position']


def test_sketch_facts_are_compared_side_by_side():
    sk_h = {'name': 'Sketch', 'support': [['XZ_Plane', ['']]], 'map_mode': 'FlatFace', 'constraints': 22,
            'fully_constrained': True, 'up_vector': [0.0, 0.0, 1.0], 'normal': [0.0, -1.0, 0.0], 'geometry': 8}
    sk_c = dict(sk_h, constraints=0, fully_constrained=False, support=[])
    row = _row('Body', 'PartDesign::Body', 8500.0, [25.0, 20.0, 60.0], [0.0, 60.0], [0.0, 0.0, 0.0])
    r = compare.compare(_doc([row], sketches=[sk_h]), _doc([row], sketches=[sk_c]), expected=8500.0)
    assert r['sketch'] == {'hand': {'plane': 'XZ_Plane', 'constraints': 22, 'fully_constrained': True,
                                    'up_vector': [0.0, 0.0, 1.0], 'lines': 8},
                           'claude': {'plane': None, 'constraints': 0, 'fully_constrained': False,
                                      'up_vector': [0.0, 0.0, 1.0], 'lines': 8}}
    assert r['same'] is True          # the solid is the same; the sketch facts are reported, not part of "same"


def test_a_mirrored_j_is_not_upright_even_with_z_0_to_60():
    up = _row('Body', 'PartDesign::Body', 8500.0, [25.0, 20.0, 60.0], [0.0, 60.0], [0.0, -20.0, 0.0])
    mirrored = _row('Body', 'PartDesign::Body', 8500.0, [25.0, 20.0, 60.0], [0.0, 60.0], [-25.0, -20.0, 0.0])
    r = compare.compare(_doc([up]), _doc([mirrored]), expected=8500.0)
    assert r['upright'] == {'hand': True, 'claude': False} and r['differences'] == ['position']


def test_the_plane_is_read_from_the_origin_sub_element_as_freecad_saves_it():
    sk = {'name': 'Sketch', 'support': [['Origin', ['XZ_Plane']]], 'constraints': 23, 'fully_constrained': True,
          'up_vector': [0.0, 0.0, 1.0], 'geometry': 8}
    row = _row('Body', 'PartDesign::Body', 8500.0, [25.0, 20.0, 60.0], [0.0, 60.0], [0.0, -20.0, 0.0])
    r = compare.compare(_doc([row], sketches=[sk]), _doc([row], sketches=[sk]), expected=8500.0)
    assert r['sketch']['hand']['plane'] == 'XZ_Plane'
