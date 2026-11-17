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


# ---- the pre-registered classes (PLAN 4.2), first that fits ----
def chk(sheet=80, zmax=80.0, lens=None, inner=None, plate_driving=True, redundant=(), start_like=False):
    return {'sheet': {'plate_height': sheet}, 'zmax': zmax, 'line_lengths': lens or lengths(zmax),
            'inner': inner, 'plate_height_driving': plate_driving, 'redundant': list(redundant),
            'same_as_start': start_like}


REF = {'driving': False, 'value': 75.0, 'expression': None}
DRV55 = {'driving': True, 'value': 55.0, 'expression': None}
DRV75 = {'driving': True, 'value': 75.0, 'expression': None}
EXPR = {'driving': True, 'value': 75.0, 'expression': 'Params.plate_height - Params.thickness'}


@pytest.mark.parametrize('check, stopped, cls', [
    (chk(inner=REF), True, 'stopped by the cost cap'),
    (None, False, 'partly done'),
    (chk(inner=REF), False, 'right + reference'),
    (chk(inner=None), False, 'right by deleting the 55'),
    (chk(zmax=60.0, lens=lengths(60), inner=DRV75, redundant=[17]), False, 'stale, 55 edited to 75'),
    (chk(zmax=60.0, lens=lengths(60), inner=EXPR, redundant=[17]), False, 'stale, 55 bound to an expression'),
    (chk(zmax=60.0, lens=lengths(60), inner=DRV55, plate_driving=False), False, 'stale, plate_height drives nothing'),
    (chk(zmax=60.0, lens=lengths(60), inner=DRV55, redundant=[17]), False, 'stale'),
    (chk(zmax=80.0, lens=[25, 10, 5, 5, 15, 55, 5, 80], inner=DRV55), False, 'wrong part'),
    (chk(sheet=60, zmax=60.0, inner=DRV55, redundant=[17], start_like=True), False, 'asked a question or made no change'),
    (chk(sheet=60, zmax=60.0, inner=REF), False, 'partly done'),
])
def test_prereg_classes(check, stopped, cls):
    from lab.fc11score import classify
    assert classify(check, stopped) == cls
