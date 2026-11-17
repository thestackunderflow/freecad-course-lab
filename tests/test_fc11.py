"""fc11 (FreeCAD course lesson 11, one length with two sizes: reference constraints). Checks the numbers
lab/fc11parts.py measured under freecadcmd (out/fc11/P/build.json) against the plan's arithmetic, and the Claude-run
classes of lab/fc11score.py (PLAN 4.2, out/fc11/PREREG.md).
Run: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_fc11.py"""
import json
import math
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc11')


def load(*p):
    with open(os.path.join(HERE, *p)) as f:
        return json.load(f)


def case(name):
    return load('P', 'build.json')[name]


def lengths(h):
    """the 8 line lengths of lesson 3's profile at plate_height h (L0 bottom .. L7 back)"""
    return [25, 10, 5, 5, 15, h - 5, 5, h]


def test_pinned_at_60_is_fully_constrained_and_60_tall():
    b = case('pinned_60')
    assert b['dof'] == 0 and b['redundant'] == [] and b['conflicting'] == []
    assert b['zmax'] == pytest.approx(60, abs=1e-6)
    assert b['line_lengths'] == pytest.approx(lengths(60), abs=1e-6)


def test_redundant_file_has_one_redundant_inner_size_and_still_shows_60():
    b = case('redundant_60')
    assert b['inner'] is not None and b['inner']['driving'] is True
    assert b['inner']['value'] == pytest.approx(55, abs=1e-6)
    assert len(b['redundant']) >= 1
    assert b['zmax'] == pytest.approx(60, abs=0.01)


def test_redundant_file_at_80_stays_60_while_the_sheet_says_80():
    b = case('redundant_80')
    assert b['sheet']['plate_height'] == 80
    assert b['zmax'] == pytest.approx(60, abs=0.01)
    assert b['stl_zmax'] == pytest.approx(60, abs=0.01)


@pytest.mark.parametrize('h', [80, 100])
def test_reference_file_follows_and_the_reference_reads_h_minus_5(h):
    b = case('reference_%d' % h)
    assert b['inner']['driving'] is False
    assert b['inner']['value'] == pytest.approx(h - 5, abs=1e-6)
    assert b['zmax'] == pytest.approx(h, abs=1e-6)
    assert b['stl_zmax'] == pytest.approx(h, abs=0.01)
    assert b['line_lengths'] == pytest.approx(lengths(h), abs=1e-6)
    assert b['redundant'] == [] and b['dof'] == 0


def test_your_turn_diagonal_reads_50_then_67_08():
    y = case('yourturn')
    assert y['diagonal_40'] == pytest.approx(50, abs=1e-6)
    assert y['diagonal_60'] == pytest.approx(math.hypot(60, 30), abs=1e-6)
    assert y['driving_diagonal_redundant'] is True


# ---- rev 3 (G0b): the orphan file (plate_height size deleted, inner 55 driving) and the fix ----
def g0b(name):
    return load('G0b', name)


def test_orphan_by_code_at_80_stays_60_and_nothing_reads_plate_height():
    for b in (case('orphan_80'), g0b('orphan-80-h1.json'), g0b('orphan-80-h2.json')):
        assert b['dof'] == 0 and b['redundant'] == [] and b['conflicting'] == []
        assert b['zmax'] == pytest.approx(60, abs=0.01) and b['stl_zmax'] == pytest.approx(60, abs=0.01)
        assert b['plate_height_users'] == []
        assert b['inner']['driving'] is True and b['inner']['value'] == pytest.approx(55, abs=1e-6)


def test_orphan_at_100_control_stays_60():
    assert g0b('orphan-100.json')['zmax'] == pytest.approx(60, abs=0.01)


@pytest.mark.parametrize('h', [80, 100])
def test_gui_fixed_file_follows_and_the_reference_reads_h_minus_5(h):
    b = g0b('fixed-%d.json' % h)
    assert b['zmax'] == pytest.approx(h, abs=0.01) and b['stl_zmax'] == pytest.approx(h, abs=0.01)
    assert b['inner']['driving'] is False and b['inner']['value'] == pytest.approx(h - 5, abs=1e-6)
    assert len(b['plate_height_users']) == 1 and b['plate_height_driving'] is True
    assert b['dof'] == 0 and b['redundant'] == []


def test_pinned_file_has_one_plate_height_user():
    assert len(case('pinned_60')['plate_height_users']) == 1


def test_rectangle_start_file_is_pinned_40_by_30():
    r = case('rect')
    assert r['dof'] == 0 and r['width'] == pytest.approx(40) and r['height'] == pytest.approx(30)
    assert os.path.exists(os.path.join(HERE, 'P', 'rect-pinned.FCStd'))


# ---- the pre-registered classes (PLAN 4.2 rev 3, out/fc11/PREREG.md), first that fits ----
def chk(sheet=80, zmax=80.0, lens=None, inner=None, users=(23,), redundant=(), conflicting=(), invalid=False,
        start_like=False):
    return {'sheet': {'plate_height': sheet}, 'zmax': zmax, 'line_lengths': lens or lengths(zmax),
            'inner': inner, 'plate_height_users': list(users), 'redundant': list(redundant),
            'conflicting': list(conflicting), 'states': {'HookSketch': ['Invalid'] if invalid else ['Up-to-date']},
            'same_as_start': start_like}


REF = {'driving': False, 'value': 75.0, 'expression': None}
DRV55 = {'driving': True, 'value': 55.0, 'expression': None}
DRV75 = {'driving': True, 'value': 75.0, 'expression': None}
EXPR = {'driving': True, 'value': 75.0, 'expression': 'Params.plate_height - Params.thickness'}


@pytest.mark.parametrize('check, stopped, cls', [
    (chk(inner=REF), True, 'stopped by the cost cap'),
    (None, False, 'partly done'),
    (chk(inner=REF), False, 'right + reference'),
    (chk(inner=None), False, 'right by re-linking plate_height'),
    (chk(inner=EXPR, users=(22,)), False, 'right, 55 bound to a formula'),
    (chk(inner=DRV75, users=()), False, 'right now, trap kept'),
    (chk(inner=None, users=()), False, 'right now, trap kept'),
    (chk(lens=[25, 10, 5, 5, 15, 55, 5, 80], inner=DRV55, users=(23,)), False, 'wrong part'),
    (chk(zmax=60.0, lens=lengths(60), inner=DRV55, users=(23,), redundant=[24], invalid=True), False,
     'second driving size by code, kept (sketch invalid)'),
    (chk(zmax=60.0, lens=lengths(60), inner=DRV55, users=()), False, 'stale'),
    (chk(sheet=60, zmax=60.0, inner=DRV55, users=(), start_like=True), False, 'asked a question or made no change'),
    (chk(sheet=60, zmax=60.0, inner=REF), False, 'partly done'),
])
def test_prereg_classes(check, stopped, cls):
    from lab.fc11score import classify
    assert classify(check, stopped) == cls
