"""Lesson 6 lab checks (no display, no network, no Claude): checker/l6read.py on changed copies of lesson 5's hook
(lesson 4's width30, kept local: out/l4/hand/width30.FCStd) and the pre-registered scoring checker/score_l6.py.
A right change passes; the obvious slip (hook_depth 45), a size typed into the sketch, a lost fillet, a changed hole,
a missing name and an untouched hook each fail the line they should."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, LAB)

from checker import score_l6  # noqa: E402

START = os.path.join(LAB, 'out', 'l4', 'hand', 'width30.FCStd')
needs = pytest.mark.skipif(not (os.path.exists(START) and shutil.which('freecadcmd')),
                           reason='needs lesson 4 width30.FCStd and freecadcmd (lab image)')

MUTATE = r'''
import os, FreeCAD
doc = FreeCAD.openDocument(os.environ['FC_IN'])
sh = doc.getObject('Spreadsheet')
exec(os.environ['FC_CODE'])
doc.recompute()
doc.saveAs(os.environ['FC_SAVE'])
'''


def read_after(code):
    d = tempfile.mkdtemp()
    m = os.path.join(d, 'mutate.py')
    open(m, 'w').write(MUTATE)
    env = dict(os.environ, FC_IN=START, FC_CODE=code, FC_SAVE=os.path.join(d, 'after.FCStd'))
    subprocess.run(['freecadcmd', m], env=env, check=True, capture_output=True, timeout=300)
    env = dict(os.environ, FC_DOC=os.path.join(d, 'after.FCStd'), FC_OUT=os.path.join(d, 'read.json'))
    subprocess.run(['freecadcmd', os.path.join(LAB, 'checker', 'l6read.py')], env=env, check=True,
                   capture_output=True, timeout=300)
    return json.load(open(os.path.join(d, 'read.json')))


def failed(s):
    return sorted(k for k, v in s['lines'].items() if not v)


@needs
def test_right_change_passes():
    r = read_after("sh.set('hook_depth', '55 mm')")
    s = score_l6.score(r)
    assert r['geometry']['opening_mm'] == pytest.approx(45.0, abs=1e-6)
    assert s['pass'], s
    assert s['hook_depth'] == pytest.approx(55.0)


@needs
def test_untouched_fails_only_opening_and_volume():
    s = score_l6.score(read_after("pass"))
    assert failed(s) == ['C', 'V']


@needs
def test_the_slip_45_gives_35():
    r = read_after("sh.set('hook_depth', '45 mm')")
    assert r['geometry']['opening_mm'] == pytest.approx(35.0, abs=1e-6)
    assert failed(score_l6.score(r)) == ['C', 'V']


@needs
def test_a_new_name_feeding_hook_depth_passes():
    s = score_l6.score(read_after(
        "sh.set('B8', '45 mm'); sh.setAlias('B8', 'opening'); sh.set('B1', '=opening + 2 * thickness')"))
    assert s['pass'], s
    assert s['new_aliases'] == ['opening']


@needs
def test_size_typed_into_the_sketch_breaks_the_names():
    code = ("sk = doc.getObject('Sketch')\n"
            "sk.setExpression('Constraints[17]', None)\n"
            "sk.setDatum(17, FreeCAD.Units.Quantity('55 mm'))")
    s = score_l6.score(read_after(code))
    assert s['lines']['C'] and s['lines']['V']
    assert failed(s) == ['M7']


@needs
def test_fillet_removed_fails_m6():
    code = ("b = doc.getObject('Body'); f = doc.getObject('Fillet'); b.Tip = doc.getObject('Hole')\n"
            "b.removeObject(f); doc.removeObject('Fillet'); sh.set('hook_depth', '55 mm')")
    s = score_l6.score(read_after(code))
    assert 'M6' in failed(s) and 'V' in failed(s)


@needs
def test_hole_changed_fails_m5():
    s = score_l6.score(read_after("sh.set('hook_depth', '55 mm'); sh.set('hole_d', '5 mm')"))
    assert 'M5' in failed(s) and 'M7' in failed(s)


@needs
def test_a_moved_part_still_passes_xy():
    s = score_l6.score(read_after(
        "sh.set('hook_depth', '55 mm'); b = doc.getObject('Body'); b.Placement.Base = FreeCAD.Vector(10, 20, 0)"))
    assert s['pass'], s
    assert s['moved']


def test_scoring_without_a_part_fails_every_line():
    s = score_l6.score({'part': None})
    assert not s['pass'] and not any(s['lines'].values())


@needs
def test_a_lifted_and_turned_part_still_passes():
    s = score_l6.score(read_after(
        "sh.set('hook_depth', '55 mm'); b = doc.getObject('Body')\n"
        "b.Placement = FreeCAD.Placement(FreeCAD.Vector(3, -7, 12), FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 90))"))
    assert s['pass'], s
    assert s['moved']


@needs
def test_opening_name_wired_into_the_sketch_fails_m7():
    code = ("sh.set('B8', '45 mm'); sh.setAlias('B8', 'opening')\n"
            "doc.getObject('Sketch').setExpression('Constraints[17]', 'Spreadsheet.opening + 2 * Spreadsheet.thickness')")
    s = score_l6.score(read_after(code))
    assert s['lines']['C'] and s['lines']['V']
    assert failed(s) == ['M7']
    assert not s['why']['M7']['depth_ok']


@needs
def test_measure_row_is_not_an_error():
    r = read_after("sh.set('hook_depth', '55 mm')\n"
                   "m = doc.addObject('Measure::MeasureDistance', 'Distance')")
    assert score_l6.score(r)['pass']


def test_pick_read_prefers_the_changed_new_document():
    start = {'part': 'Body', 'geometry': {'opening_mm': 30.0}}
    new = {'part': 'Body', 'geometry': {'opening_mm': 45.0}}
    assert score_l6.pick_read({'hook_lesson5': start, 'Hook': new}) == ('Hook', new, True)
    changed = {'part': 'Body', 'geometry': {'opening_mm': 45.0}}
    assert score_l6.pick_read({'hook_lesson5': changed, 'Hook': new})[0] == 'hook_lesson5'
