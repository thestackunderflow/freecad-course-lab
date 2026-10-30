"""Lesson 3 lab checks (unit tests; no display, no network, no Claude): the named walk and its expected numbers worked
out without CAD (hook_depth 25 and 40), the lab-query guard (a query must never raise inside FreeCAD: in lesson 2 an
"Internal C++ object already deleted" error reached FreeCAD's console and the add-on's error showed on screen), and
the pre-registered scoring of a Claude run (names used, first build right, edit followed, edit by one cell)."""
import contextlib
import io
import os
import sys
import types

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, LAB)

from checker import outline, score_l3  # noqa: E402
from lab import fcrpc  # noqa: E402

NAMES = {'plate_height': 60, 'width': 20, 'thickness': 5, 'hook_depth': 25, 'lip_height': 10}


# ---- the named walk ------------------------------------------------------------------------------------------
def test_the_named_walk_gives_lesson_twos_j_at_the_starting_sizes():
    assert outline.named_moves(NAMES) == outline.J_MOVES


def test_hook_depth_40_gives_10000_and_a_box_15_mm_deeper():
    e = outline.expected(outline.named_moves(dict(NAMES, hook_depth=40)), NAMES['width'])
    assert e['area_mm2'] == 500.0 and e['volume_mm3'] == 10000.0
    assert e['bbox_mm'] == [40.0, 20.0, 60.0]
    assert e['vertices'][:-1] == [(0.0, 0.0), (40.0, 0.0), (40.0, 10.0), (35.0, 10.0), (35.0, 5.0), (5.0, 5.0),
                                  (5.0, 60.0), (0.0, 60.0)]


def test_one_thickness_cell_moves_three_sizes():
    used = outline.uses_of('thickness')
    assert used == ['lip width', 'lip inside (lip_height - thickness)', 'back plate thickness']


# ---- the lab-query guard -------------------------------------------------------------------------------------
class _Deleted(types.ModuleType):
    def __getattr__(self, name):
        raise RuntimeError('Internal C++ object (QTreeWidgetItem) already deleted.')


@pytest.mark.parametrize('name', ['ROW', 'ARROW', 'VP', 'DOCS', 'SAVE', 'CELL'])
def test_a_lab_query_never_raises_inside_freecad(name, monkeypatch):
    for mod in ('FreeCAD', 'FreeCADGui', 'PySide', 'PySide.QtCore', 'PySide.QtWidgets'):
        monkeypatch.setitem(sys.modules, mod, _Deleted(mod))
    code = fcrpc.guard(getattr(fcrpc, name).format(doc='D', obj='O', path='/tmp/x', pts=[(0, 0, 0)], cell='B1',
                                                    sheet='Spreadsheet'))
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, 'q', 'exec'), {})        # what the add-on does; it must not raise
    assert buf.getvalue().startswith(fcrpc.LABERR)


def test_the_client_retries_a_lab_error_and_then_gets_the_answer(monkeypatch):
    answers = iter([fcrpc.LABERR + ' RuntimeError: deleted', '512 640'])
    monkeypatch.setattr(fcrpc, '_exec', lambda code: next(answers))
    monkeypatch.setattr(fcrpc, 'RETRY_WAIT', 0)
    assert fcrpc.run('print(1)') == '512 640'


def test_the_client_raises_on_its_own_side_after_its_tries(monkeypatch):
    calls = []
    monkeypatch.setattr(fcrpc, '_exec', lambda code: calls.append(code) or fcrpc.LABERR + ' RuntimeError: deleted')
    monkeypatch.setattr(fcrpc, 'RETRY_WAIT', 0)
    with pytest.raises(RuntimeError):
        fcrpc.run('print(1)')
    assert len(calls) == fcrpc.TRIES and all(fcrpc.LABERR in c for c in calls)   # every attempt sent guarded


# ---- scoring (pre-registered) --------------------------------------------------------------------------------
def _m(volume, bbox, z, mn, corners, sheets=None, exprs=None, pad_expr=None, fc=True):
    return {'solids': [{'name': 'Body', 'type': 'PartDesign::Body', 'volume_mm3': volume, 'bbox_mm': bbox,
                        'z_range_mm': z, 'min_mm': mn, 'valid': True, 'solids': 1, 'in_list': []}],
            'sketches': [{'name': 'Sketch', 'corners_xy': corners, 'fully_constrained': fc,
                          'dimensions': [{'index': i, 'type': 'DistanceX', 'value': 1.0, 'expression': e}
                                         for i, e in enumerate(exprs or [])]}],
            'sheets': sheets or [], 'pads': [{'name': 'Pad', 'length': 20.0, 'expression': pad_expr}]}


J25 = [[0, 0], [25, 0], [25, 10], [20, 10], [20, 5], [5, 5], [5, 60], [0, 60]]
J40 = [[0, 0], [40, 0], [40, 10], [35, 10], [35, 5], [5, 5], [5, 60], [0, 60]]
SHEET = [{'name': 'Spreadsheet', 'aliases': {k: str(v) for k, v in NAMES.items()}}]
EXPRS = ['Spreadsheet.hook_depth', 'Spreadsheet.lip_height', 'Spreadsheet.thickness',
         'Spreadsheet.lip_height - Spreadsheet.thickness', 'Spreadsheet.plate_height', 'Spreadsheet.thickness']


def test_a_named_run_that_builds_right_and_edits_one_cell_scores_all_four():
    first = _m(8500.0, [25.0, 20.0, 60.0], [0.0, 60.0], [0.0, -20.0, 0.0], J25, SHEET, EXPRS, 'Spreadsheet.width')
    after_sheet = [{'name': 'Spreadsheet', 'aliases': dict(SHEET[0]['aliases'], hook_depth='40')}]
    after = _m(10000.0, [40.0, 20.0, 60.0], [0.0, 60.0], [0.0, -20.0, 0.0], J40, after_sheet, EXPRS, 'Spreadsheet.width')
    s = score_l3.score(first, after, edit_code=['App.ActiveDocument.Spreadsheet.set("hook_depth", "40")'])
    assert s['names']['aliases'] == sorted(NAMES) and s['names']['dims_from_names'] == 6
    assert s['names']['pad_from_name'] is True and s['names']['used'] is True
    assert s['first_build_right'] is True and s['edit_followed'] is True and s['edit_by_one_cell'] is True


def test_a_wrong_formula_is_caught_by_the_first_build_check_not_by_the_names():
    bad = [[0, 0], [25, 0], [25, 10], [20, 10], [20, 5], [15, 5], [15, 60], [0, 60]]   # plate inner edge misplaced
    first = _m(11500.0, [25.0, 20.0, 60.0], [0.0, 60.0], [0.0, -20.0, 0.0], bad, SHEET, EXPRS, 'Spreadsheet.width')
    s = score_l3.score(first, first, edit_code=[])
    assert s['names']['used'] is True and s['first_build_right'] is False
    assert 'volume' in s['first_build_misses'] and 'corners' in s['first_build_misses']


def test_a_run_without_names_that_redraws_points_scores_edit_followed_but_not_by_one_cell():
    first = _m(8500.0, [25.0, 20.0, 60.0], [0.0, 60.0], [0.0, -20.0, 0.0], J25)
    after = _m(10000.0, [40.0, 20.0, 60.0], [0.0, 60.0], [0.0, -20.0, 0.0], J40)
    s = score_l3.score(first, after, edit_code=['sk.movePoint(0, 2, App.Vector(40, 0, 0))'])
    assert s['names']['used'] is False and s['names']['aliases'] == []
    assert s['first_build_right'] is True and s['edit_followed'] is True and s['edit_by_one_cell'] is False


def test_reading_40_deep_as_a_45_box_is_recorded_as_read_differently():
    first = _m(8500.0, [25.0, 20.0, 60.0], [0.0, 60.0], [0.0, -20.0, 0.0], J25)
    j45 = [[0, 0], [45, 0], [45, 10], [40, 10], [40, 5], [5, 5], [5, 60], [0, 60]]
    after = _m(11000.0, [45.0, 20.0, 60.0], [0.0, 60.0], [0.0, -20.0, 0.0], j45)
    s = score_l3.score(first, after, edit_code=[])
    assert s['edit_followed'] is False and s['edit_reading'] == 'arm 40 inside (box 45)'
