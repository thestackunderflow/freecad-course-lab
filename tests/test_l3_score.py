"""Lesson 3's pre-registered scoring of a Claude run (rev 2, after the plan gate's accuracy review; unit tests, no
FreeCAD): the part is judged by its solid (volume, box, height), names by every expression in the file that names an
alias, each edit "by one cell" by the alias whose value changed and by no call rewriting the sketch; corners are
recorded, not deciding."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..')))

from checker import outline, score_l3  # noqa: E402

NAMES = {'plate_height': 60, 'width': 20, 'thickness': 5, 'hook_depth': 25, 'lip_height': 10}


def _m(volume, bbox, z=(0.0, 60.0), corners=None, aliases=None, exprs=None, fc=True):
    """A measure.py-shaped document: one root solid, one sketch, the sheet's aliases, every expression in the file."""
    return {'solids': [{'name': 'Body', 'type': 'PartDesign::Body', 'volume_mm3': volume, 'bbox_mm': list(bbox),
                        'z_range_mm': list(z), 'min_mm': [0.0, -20.0, z[0]], 'valid': True, 'solids': 1, 'in_list': []}],
            'sketches': [{'name': 'Sketch', 'corners_xy': corners or [], 'fully_constrained': fc}],
            'sheets': [{'name': 'Spreadsheet', 'aliases': dict(aliases)}] if aliases else [],
            'expressions': [{'object': o, 'property': k, 'expression': e} for o, k, e in (exprs or [])]}


def J(depth=25, t=5):
    return [list(p) for p in outline.walk(outline.named_moves(dict(NAMES, hook_depth=depth, thickness=t)))[:-1]]


AL = {'plate_height': '60 mm', 'width': '20 mm', 'thickness': '5 mm', 'hook_depth': '25 mm', 'lip_height': '10 mm'}
EX = [('Sketch', '.Constraints.c17', 'Spreadsheet.hook_depth'), ('Sketch', '.Constraints.c18', 'Spreadsheet.lip_height'),
      ('Sketch', '.Constraints.c19', 'Spreadsheet.thickness'),
      ('Sketch', '.Constraints.c20', 'Spreadsheet.lip_height - Spreadsheet.thickness'),
      ('Sketch', '.Constraints.c21', 'Spreadsheet.plate_height'), ('Sketch', '.Constraints.c22', 'Spreadsheet.thickness'),
      ('Pad', 'Length', 'Spreadsheet.width')]
FIRST = _m(8500.0, (25.0, 20.0, 60.0), corners=J(), aliases=AL, exprs=EX)
AFTER2 = _m(10000.0, (40.0, 20.0, 60.0), corners=J(40), aliases=dict(AL, hook_depth='40 mm'), exprs=EX)
AFTER3 = _m(15040.0, (40.0, 20.0, 60.0), corners=J(40, 8), aliases=dict(AL, hook_depth='40 mm', thickness='8 mm'),
            exprs=EX)
CELL2 = ["ss.set('B4', '40 mm'); App.ActiveDocument.recompute()"]
CELL3 = ["ss.set('thickness', '8 mm'); App.ActiveDocument.recompute()"]


def test_the_expected_numbers_after_both_edits_come_from_the_named_walk():
    assert score_l3.EXPECTED == {'first': (8500.0, [25.0, 20.0, 60.0]), 'after2': (10000.0, [40.0, 20.0, 60.0]),
                                 'after3': (15040.0, [40.0, 20.0, 60.0])}


def test_a_named_run_that_builds_right_and_edits_one_cell_each_time_scores_everything():
    s = score_l3.score(FIRST, AFTER2, AFTER3, CELL2, CELL3)
    assert s['names']['aliases'] == sorted(NAMES) and s['names']['exprs_from_names'] == 7 and s['names']['used']
    assert s['first_build_right'] and s['edit2_followed'] and s['edit3_followed']
    assert s['edit2_by_one_cell'] and s['edit3_by_one_cell']
    assert s['edit2_alias'] == 'hook_depth' and s['edit3_alias'] == 'thickness'
    assert s['corners'] == {'first': True, 'after2': True, 'after3': True}


def test_a_wrong_formula_is_caught_by_the_first_build_check_not_by_the_names():
    bad = _m(11500.0, (25.0, 20.0, 60.0), aliases=AL, exprs=EX,
             corners=[[0, 0], [25, 0], [25, 10], [20, 10], [20, 5], [15, 5], [15, 60], [0, 60]])
    s = score_l3.score(bad, bad, None, [], [])
    assert s['names']['used'] is True and s['first_build_right'] is False
    assert 'volume' in s['first_build_misses'] and s['corners']['first'] is False


def test_a_run_without_names_that_rewrites_sizes_follows_but_not_by_one_cell():
    f, a2, a3 = (_m(m['solids'][0]['volume_mm3'], m['solids'][0]['bbox_mm'], corners=m['sketches'][0]['corners_xy'])
                 for m in (FIRST, AFTER2, AFTER3))
    s = score_l3.score(f, a2, a3, ['sk.setDatum(17, App.Units.Quantity("40 mm"))'],
                       ['sk.movePoint(2, 2, App.Vector(32, 10, 0))'])
    assert s['names']['used'] is False and s['names']['aliases'] == []
    assert s['first_build_right'] and s['edit2_followed'] and s['edit3_followed']
    assert s['edit2_by_one_cell'] is False and s['edit3_by_one_cell'] is False
    assert s['edit3_reading'] == '15040 mm3, box 40 x 20 x 60'


def test_a_different_reading_of_8_thick_is_recorded_with_its_numbers():
    a3 = _m(15220.0, (40.0, 20.0, 60.0), corners=[[0, 0], [40, 0], [40, 13], [35, 13], [35, 8], [8, 8], [8, 60], [0, 60]])
    s = score_l3.score(FIRST, AFTER2, a3, CELL2, [])
    assert s['edit3_followed'] is False and s['edit3_reading'] == '15220 mm3, box 40 x 20 x 60'


def test_a_correct_build_with_a_construction_line_and_no_part_design_still_scores_right():
    f = _m(8500.0, (25.0, 20.0, 60.0), corners=J() + [[12.5, 0], [12.5, 60]], aliases=AL,
           exprs=[('Extrude', 'LengthFwd', 'Spreadsheet.width'), ('Sketch', 'Constraints[3]', 'Spreadsheet.hook_depth')])
    s = score_l3.score(f, f, None, [], [])
    assert s['first_build_right'] is True and s['corners']['first'] is False
    assert s['names']['used'] is True and s['names']['exprs_from_names'] == 2


def test_the_one_cell_check_finds_the_alias_that_changed_whatever_its_spelling():
    camel = {('HookDepth' if k == 'hook_depth' else k): v for k, v in AL.items()}
    ex = [(o, k, e.replace('hook_depth', 'HookDepth')) for o, k, e in EX]
    f = _m(8500.0, (25.0, 20.0, 60.0), corners=J(), aliases=camel, exprs=ex)
    a2 = _m(10000.0, (40.0, 20.0, 60.0), corners=J(40), aliases=dict(camel, HookDepth='40'), exprs=ex)
    s = score_l3.score(f, a2, None, CELL2, [])
    assert s['edit2_by_one_cell'] is True and s['edit2_alias'] == 'HookDepth'


def test_rebinding_a_size_in_the_sketch_is_not_an_edit_by_one_cell():
    code = ["sk.setExpression('.Constraints.c17', '40 mm'); ss.set('B4', '40 mm')"]
    s = score_l3.score(FIRST, AFTER2, None, code, [])
    assert s['edit2_followed'] is True and s['edit2_by_one_cell'] is False and s['edit2_touched_sketch'] is True


def test_other_readings_of_40_deep_are_recorded_not_failed_as_names():
    for box, reading in (((45.0, 20.0, 60.0), 'arm 40 inside (box 45)'), ((50.0, 20.0, 60.0), 'clear 40 inside (box 50)'),
                         ((25.0, 40.0, 60.0), '40 as the extrude (25 x 40 x 60)')):
        s = score_l3.score(FIRST, _m(1.0, box, aliases=AL, exprs=EX), None, [], [])
        assert s['edit2_followed'] is False and s['edit2_reading'] == reading


def test_the_calls_are_split_by_message_from_the_logged_stage_marks(tmp_path):
    t = tmp_path / 'transcript.jsonl'
    rows = []
    for i, code in enumerate(['build', 'measure', 'edit 40', 'edit 8']):
        rows.append({'seq': i, 'dir': 'client->server', 'msg': {'method': 'tools/call', 'id': i,
                     'params': {'name': 'execute_code', 'arguments': {'code': code}}}})
        rows.append({'seq': i, 'dir': 'server->client', 'msg': {'id': i, 'result': {}}})
    t.write_text(chr(10).join(json.dumps(r) for r in rows) + chr(10), encoding='utf-8')
    stages = {'first': 4, 'after2': 6, 'after3': 8}           # transcript line counts when each copy was saved
    by = score_l3.calls_by_message(str(t), stages)
    assert [[json.loads(c)['code'] for c in by[k]] for k in (1, 2, 3)] == [['build', 'measure'], ['edit 40'], ['edit 8']]
