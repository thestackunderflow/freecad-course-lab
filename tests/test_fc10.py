"""fc10 (FreeCAD course lesson 10, fully constrained sketches). Checks the numbers lab/fc10parts.py measured under
freecadcmd (out/fc10/P/build.json) against the plan's arithmetic, and NUMBERS.json once lab/fc10numbers.py wrote it.
Run: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_fc10.py"""
import json
import math
import os

import pytest

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc10')
AREA60 = 425                     # lesson 3 profile at plate_height 60 (mm2): plate 5 x 60 + arm 20 x 5 + lip 5 x 5
HOLE = math.pi * 2.25 ** 2 * 5   # the screw hole, 4.5 through the 5 mm plate


def load(*p):
    with open(os.path.join(HERE, *p)) as f:
        return json.load(f)


def vol(h, hole=True):
    return (AREA60 + 5 * (h - 60)) * 20 - (HOLE if hole else 0)


def case(name):
    return load('P', 'build.json')[name]


def test_pinned_at_60_is_fully_constrained_on_the_floor():
    b = case('pinned_60')
    assert b['dof'] == 0
    assert (b['zmin'], b['zmax']) == (pytest.approx(0, abs=1e-6), pytest.approx(60, abs=1e-6))
    assert b['hole_to_top'] == pytest.approx(15, abs=1e-6)
    assert b['volume_mm3'] == pytest.approx(vol(60), abs=0.01)


def test_unpinned_at_60_looks_the_same_but_has_2_dof():
    b = case('unpinned_60')
    assert b['dof'] == 2
    assert b['constraints'] == 8 + 8 + 6          # joins, flat/upright, sizes: no redundant 7th size
    assert (b['zmin'], b['zmax']) == (pytest.approx(0, abs=1e-6), pytest.approx(60, abs=1e-6))
    assert b['hole_to_top'] == pytest.approx(15, abs=1e-6)


@pytest.mark.parametrize('h', [80, 100])
def test_pinned_resize_grows_straight_up(h):
    b = case('pinned_%d' % h)
    assert b['dof'] == 0
    assert (b['zmin'], b['zmax']) == (pytest.approx(0, abs=1e-6), pytest.approx(h, abs=1e-6))
    assert b['hole_to_top'] == pytest.approx(15, abs=1e-6)
    assert b['volume_mm3'] == pytest.approx(vol(h), abs=0.01)


@pytest.mark.parametrize('name,h', [('unpinned_80', 80), ('unpinned_100', 100), ('unpinned_80_100', 100)])
def test_unpinned_resize_keeps_the_size_but_not_the_place(name, h):
    # the size rule holds (plate is h tall) wherever the solver put it; where it went is the lab's finding
    b = case(name)
    assert b['dof'] == 2
    assert b['zmax'] - b['zmin'] == pytest.approx(h, abs=1e-6)
    assert 'hole_z' in b and 'sketch_hole_z' in b


def test_your_turn_rectangle_two_sizes_leave_2_then_pin_far_side_moves():
    y = case('yourturn')
    assert y['dof_drawn'] == 4                 # rectangle tool: 4 joins + 2 flat + 2 upright
    assert y['dof_sized'] == 2                 # + 40 and 30
    assert y['dof_pinned'] == 0
    assert y['pinned_corner_after'] == pytest.approx(y['pinned_corner_before'], abs=1e-6)
    assert y['width_after'] == pytest.approx(60, abs=1e-6)


def test_numbers_file_has_every_section():
    if not os.path.exists(os.path.join(HERE, 'NUMBERS.json')):
        pytest.skip('NUMBERS.json not written yet')
    n = load('NUMBERS.json')
    for k in ('freecad', 'cases', 'g0', 'takes', 'claude_runs'):
        assert k in n


def _c(**k):
    base = {'dof': 2, 'zmin': 0.0, 'zmax': 80.0, 'hole_to_top': 15.0, 'sheet': {'plate_height': 80}}
    base.update(k)
    return base


@pytest.mark.parametrize('check,stopped,cls', [
    (_c(dof=0), False, 'right + pinned'),
    (_c(), False, 'right but still unpinned'),
    (_c(zmin=-1.32, zmax=78.68, hole_to_top=13.68), False, 'moved'),
    (_c(sheet={'plate_height': 60}, zmax=60.0), False, 'partly done'),
    (_c(zmin=-0.5, zmax=79.5, hole_to_top=14.5), False, 'partly done'),
    (_c(dof=0), True, 'stopped by the cost cap'),
    (None, False, 'partly done'),
])
def test_prereg_classes(check, stopped, cls):
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    from lab.fc10score import classify
    assert classify(check, stopped) == cls
