"""Lesson 3 lab checks (unit tests; no display, no network, no Claude): the named walk and its expected numbers worked
out without CAD (hook_depth 25 and 40), the lab-query guard (a query must never raise inside FreeCAD: in lesson 2 an
"Internal C++ object already deleted" error reached FreeCAD's console and the add-on's error showed on screen; and
the scoring is in test_l3_score.py)."""
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

