"""Lesson 4 lab checks (unit tests; no display, no network, no Claude): the screw holes and the fillet worked out without
CAD (lesson 3's hook at hook_depth 40, then width 20 -> 30), how a measured solid's round faces are read as holes and a
fillet (centred or not, through or not, on the lip's top outer edge or not), and the pre-registered scoring."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, LAB)

from checker import holes, score_l4  # noqa: E402
from lab import button  # noqa: E402


# ---- the numbers worked out first ----------------------------------------------------------------------------
def test_lesson_threes_hook_with_two_4mm_holes_and_a_2mm_fillet_is_9857_168():
    e = holes.expected()
    j = 10000.0                                   # lesson 3's hook at hook_depth 40
    hole = 2 * math.pi * 2 ** 2 * 5               # two 4 mm holes through the 5 mm plate
    fil = (2 ** 2 - math.pi * 2 ** 2 / 4) * 20    # the corner a 2 mm fillet removes, along 20 mm
    assert abs(e['volume_mm3'] - (j - hole - fil)) < 1e-9
    assert round(e['volume_mm3'], 3) == 9857.168
    assert e['bbox_mm'] == [40.0, 20.0, 60.0]


def test_width_30_gives_14848_584_and_the_holes_move_to_15():
    e = holes.expected(dict(holes.NAMES, width=30))
    assert round(e['volume_mm3'], 3) == 14848.584
    assert e['bbox_mm'] == [40.0, 30.0, 60.0]
    assert e['hole_from_side_mm'] == 15.0


def test_the_holes_sit_15_and_45_up_and_the_fillet_axis_2_in_from_the_lip_corner():
    e = holes.expected()
    assert e['hole_heights_mm'] == [15.0, 45.0]
    assert e['fillet_axis_xz'] == [38.0, 8.0]


# ---- reading a measured solid ------------------------------------------------------------------------------
def solid(width=20.0, hole_y=None, hole_r=2.0, fillet=True, depth=40.0, t=5.0, vol=None):
    y = -width / 2 if hole_y is None else hole_y
    cyl = [{'r': hole_r, 'axis': [1.0, 0.0, 0.0], 'center': [0.0, y, z], 'area': round(2 * math.pi * hole_r * t, 3)}
           for z in (15.0, 45.0)]
    if fillet:
        cyl.append({'r': 2.0, 'axis': [0.0, -1.0, 0.0], 'center': [depth - 2, 0.0, 8.0],
                    'area': round(math.pi * width, 3)})
    e = holes.expected(dict(holes.NAMES, width=width, hook_depth=depth))
    return {'name': 'Body', 'volume_mm3': e['volume_mm3'] if vol is None else vol, 'valid': True, 'solids': 1,
            'bbox_mm': [depth, width, 60.0], 'min_mm': [0.0, -width, 0.0], 'max_mm': [depth, 0.0, 60.0],
            'z_range_mm': [0.0, 60.0], 'in_list': [], 'cylinders': cyl}


def test_a_right_part_passes_every_check():
    c = holes.check(solid(), holes.NAMES)
    assert c['ok'], c
    assert c['holes'] == 2 and c['hole_d'] == [4.0, 4.0] and c['centred'] and c['through'] and c['fillet_on_lip_edge']


def test_holes_left_at_10_when_the_plate_is_30_wide_are_off_centre_by_5():
    c = holes.check(solid(width=30, hole_y=-10.0), dict(holes.NAMES, width=30))
    assert not c['centred'] and 'centred' in c['misses']
    assert c['hole_sides_mm'] == [[10.0, 20.0], [10.0, 20.0]]


def test_a_missing_fillet_and_a_wrong_hole_size_are_both_named():
    c = holes.check(solid(fillet=False, hole_r=2.5), holes.NAMES)
    assert not c['ok'] and 'fillet' in c['misses'] and 'hole size' in c['misses']


def test_a_fillet_on_a_shorter_stretch_of_the_edge_is_not_the_whole_edge():
    s = solid(width=30)
    s['cylinders'][-1]['area'] = round(math.pi * 20, 3)     # still 20 long: it did not follow the width
    c = holes.check(s, dict(holes.NAMES, width=30))
    assert not c['fillet_on_lip_edge']


# ---- the pre-registered scoring -------------------------------------------------------------------------------
def meas(s, aliases=None, exprs=()):
    return {'solids': [s], 'sheets': [{'name': 'Spreadsheet', 'aliases': aliases or {}}],
            'expressions': [{'object': o, 'property': p, 'expression': e} for o, p, e in exprs]}


BASE = {'hook_depth': '40 mm', 'thickness': '5 mm', 'lip_height': '10 mm', 'plate_height': '60 mm', 'width': '20 mm'}
NAMED = dict(BASE, hole_d='4 mm', hole_spacing='30 mm')
EXPRS = [('Sketch001', 'Constraints[1]', 'Spreadsheet.width / 2'),
         ('Sketch001', 'Constraints[2]', '(Spreadsheet.plate_height - Spreadsheet.hole_spacing) / 2'),
         ('Hole', 'Diameter', 'Spreadsheet.hole_d'), ('Pad', 'Length', 'Spreadsheet.width')]


def test_asked_and_all_right_scores_names_first_build_centred_fillet_and_one_cell():
    first = meas(solid(), NAMED, EXPRS)
    after = meas(solid(width=30), dict(NAMED, width='30 mm'), EXPRS)
    r = score_l4.score(first, after, [('execute_code', '{"code": "sh.set(\'B5\', \'30 mm\')"}')])
    assert r['names']['hole_names'] == ['hole_d', 'hole_spacing'] and r['names']['positions_from_width']
    assert r['first_build_right'] and r['edit_followed'] and r['centred_after_edit'] and r['fillet_after_edit']
    assert r['edit_alias'] == 'width' and r['edit_by_one_cell']


def test_not_asked_with_holes_typed_as_numbers_ends_off_centre():
    first = meas(solid(), BASE, [('Pad', 'Length', 'Spreadsheet.width')])
    after = meas(solid(width=30, hole_y=-10.0), dict(BASE, width='30 mm'), [('Pad', 'Length', 'Spreadsheet.width')])
    r = score_l4.score(first, after, [('execute_code', '{"code": "sh.set(\'B5\', \'30 mm\')"}')])
    assert r['first_build_right'] and not r['names']['hole_names'] and not r['names']['positions_from_width']
    assert r['edit_followed'] is False and r['centred_after_edit'] is False and r['edit_by_one_cell'] is False


def test_moving_the_holes_by_hand_in_the_edit_is_not_one_cell_even_if_it_ends_centred():
    first = meas(solid(), BASE, [('Pad', 'Length', 'Spreadsheet.width')])
    after = meas(solid(width=30), dict(BASE, width='30 mm'), [('Pad', 'Length', 'Spreadsheet.width')])
    r = score_l4.score(first, after, [('execute_code', '{"code": "sh.set(\'B5\', \'30 mm\'); sk.setDatum(1, 15)"}')])
    assert r['centred_after_edit'] and r['edit_followed'] and r['edit_touched_holes'] and not r['edit_by_one_cell']


# ---- the toolbar-button locator --------------------------------------------------------------------------------
def test_the_button_query_names_the_command_and_cannot_raise_inside_freecad():
    code = button.CODE.format(cmd='PartDesign_Hole')
    assert "'PartDesign_Hole'" in code
    compile(code, 'q', 'exec')


# ---- plan gate round 1 (accuracy MUST-FIX 2-3, SHOULDs): readings, split faces, every way an edit can touch ------
def test_a_hole_wall_split_into_two_faces_still_counts_as_through():
    s = solid()
    halves = []
    for c in s['cylinders'][:2]:
        halves += [dict(c, area=round(c['area'] / 2, 3)), dict(c, area=round(c['area'] / 2, 3))]
    s['cylinders'] = halves + s['cylinders'][2:]
    c = holes.check(s, holes.NAMES)
    assert c['through'] and c['holes'] == 2, c


def test_heights_read_as_the_back_face_or_the_free_front_face_are_named_not_hidden():
    s = solid()
    for c in s['cylinders'][:2]:
        c['center'][2] += 2.5
    c = holes.check(s, holes.NAMES)
    assert c['heights_reading'] == '17.5/47.5 (centred on the plate above the arm)' and c['spacing_mm'] == 30.0
    assert 'heights' in c['misses']
    assert holes.check(solid(), holes.NAMES)['heights_reading'] == '15/45 (centred on the back face)'


def test_the_edit_is_followed_when_heights_stay_as_message_1_left_them():
    first, after = solid(), solid(width=30)
    for s in (first, after):
        for c in s['cylinders'][:2]:
            c['center'][2] += 2.5
    r = score_l4.score(meas(first, NAMED, EXPRS), meas(after, dict(NAMED, width='30 mm'), EXPRS),
                       [('execute_code', '{"code": "sh.set(\'B5\', \'30 mm\')"}')])
    assert not r['first_build_right'] and r['edit_followed'] and r['edit_by_one_cell'], r


def test_mcp_tool_edits_count_as_touching_the_holes():
    t = score_l4.touched
    assert t([('create_object', '{"obj_name": "Pocket"}')])
    assert t([('delete_object', '{"obj_name": "Hole"}')])
    assert t([('edit_object', '{"obj_name": "Hole", "properties": {"Diameter": 5}}')])
    assert not t([('edit_object', '{"obj_name": "Spreadsheet", "properties": {}}')])
    assert not t([('get_objects', '{"doc_name": "hook_lesson3"}')])


def test_python_writes_that_move_a_sketch_or_a_shape_count_as_touching():
    t = score_l4.touched
    for code in ('sk.AttachmentOffset = p', 'sk.MapMode = "FlatFace"', 'sk.AttachmentSupport = [(pad, "Face3")]',
                 'cut.Shape = s', 'cyl.Height = 30', 'sh.set("hole_d", "5 mm")', 'sh.set(\'B6\', \'5 mm\')'):
        assert t([('execute_code', '{"code": %s}' % __import__('json').dumps(code))]), code
    assert not t([('execute_code', '{"code": "sh.set(\'B5\', \'30 mm\'); doc.recompute()"}')])


def test_positions_from_width_counts_only_the_hole_profile_or_a_cutting_tool():
    ex = [('Fillet', 'Radius', 'Spreadsheet.width / 10')]
    assert not score_l4.names_used(meas(solid(), NAMED, ex))['positions_from_width']
    ex = [('Sketch001', 'Constraints[1]', 'Spreadsheet.width / 2')]
    n = score_l4.names_used(meas(solid(), NAMED, ex))
    assert n['positions_from_width'] and n['position_props'] == ['Sketch001.Constraints[1]']


def test_message_b_is_one_sentence_in_front_of_message_a():
    d = os.path.join(LAB, 'out', 'l4', 'messages')
    a, b = open(os.path.join(d, 'A-1.txt'), 'rb').read(), open(os.path.join(d, 'B-1.txt'), 'rb').read()
    assert b.endswith(b' ' + a) and b.count(b'.') == a.count(b'.') + 1 and b'\n' not in b.rstrip(b'\n')
    assert open(os.path.join(d, 'A-2.txt'), 'rb').read() == open(os.path.join(d, 'B-2.txt'), 'rb').read()
