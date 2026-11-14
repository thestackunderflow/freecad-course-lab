"""fc8 (FreeCAD course lesson 8, assembly): the start files are the sc8 hook and rail. Checks the numbers the build
measured (out/fc8/P/build.json, written by lab/fc8parts.py under freecadcmd) against arithmetic, and NUMBERS.json once
lab/fc8numbers.py has written it. Run: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_fc8.py"""
import json
import os

import pytest

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc8')


def load(*p):
    with open(os.path.join(HERE, *p)) as f:
        return json.load(f)


def test_build_volumes_match_arithmetic():
    b = load('P', 'build.json')
    # hook profile 425 mm2 x 20 = 8500; block 10 x 20 x 60 = 12000; T-slot (6 x 3 + 12 x 3) x 60 = 3240
    assert b['touch']['hook_mm3'] == pytest.approx(8500 + 12000 - 3240, abs=0.01)
    assert b['touch']['rail_mm3'] == pytest.approx(24 * 4 * 80 + (6 * 3 + 12 * 3) * 80, abs=0.01)
    # typo: slot head 11.6 instead of 12 -> 0.2 overlap each side x 3 deep x 60 tall
    assert b['typo']['common_mm3'] == pytest.approx(2 * 0.2 * 3 * 60, abs=0.01)
    assert b['touch']['common_mm3'] == pytest.approx(0, abs=1e-6)
    assert b['gap04']['common_mm3'] == pytest.approx(0, abs=1e-6)


def test_build_gaps_each_side():
    b = load('P', 'build.json')
    for case, g in (('typo', -0.2), ('touch', 0.0), ('gap01', 0.1), ('gap04', 0.4)):
        assert b[case]['head_side_mm']['left'] == pytest.approx(g, abs=1e-6)
        assert b[case]['head_side_mm']['right'] == pytest.approx(g, abs=1e-6)


def test_numbers_file_has_every_section():
    if not os.path.exists(os.path.join(HERE, 'NUMBERS.json')):
        pytest.skip('NUMBERS.json not written yet')
    n = load('NUMBERS.json')
    for k in ('freecad', 'cases', 'g0', 'claude_runs'):
        assert k in n
