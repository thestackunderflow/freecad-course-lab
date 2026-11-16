"""fc9 (FreeCAD course lesson 9, LinearPattern coat rack). Checks the numbers lab/fc9parts.py measured under freecadcmd
(out/fc9/P/build.json) against arithmetic, and NUMBERS.json once lab/fc9numbers.py has written it.
Run: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_fc9.py"""
import json
import os

import pytest

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc9')
HOOK = 425 * 20          # lesson 3 profile (plate 5 x 60 + arm 20 x 5 + lip 5 x 5) x width 20


def load(*p):
    with open(os.path.join(HERE, *p)) as f:
        return json.load(f)


def strip(w):
    return w * 5 * 60


def test_start_file_one_hook_margin_20():
    b = load('P', 'build.json')['start']
    assert b['hooks'] == 1
    assert b['volume_mm3'] == pytest.approx(strip(180) + HOOK, abs=0.01)
    assert b['left_gap_mm'] == pytest.approx(20, abs=1e-6)


def test_trap_length_180_fifth_hook_floats_past_the_end():
    # Extent: step 180 / 4 = 45; starts 20 65 110 155 200; the 5th (200..220) misses the 180 strip.
    # FreeCAD 1.1.4 bodies allow compounds by default (G0: a new GUI body too), so the 5th is KEPT as a second solid
    # floating 20 mm past the strip's end (PLAN said "dropped": that is only true with AllowCompound off, below).
    b = load('P', 'build.json')['trap']
    assert b['allow_compound'] is True
    assert b['hooks'] == 5 and b['hooks_on_strip'] == 4
    assert b['floating'] == [[pytest.approx(200), pytest.approx(220)]]
    assert b['solids'] == 2
    assert b['left_gap_mm'] == pytest.approx(20, abs=1e-6)
    assert b['right_gap_mm'] == pytest.approx(5, abs=1e-6)
    assert b['starts'] == pytest.approx([20, 65, 110, 155, 200], abs=1e-6)


def test_trap_without_compound_drops_the_fifth_hook():
    b = load('P', 'build.json')['trap_nocompound']
    assert b['allow_compound'] is False
    assert b['hooks'] == 4 and b['solids'] == 1
    assert b['volume_mm3'] == pytest.approx(strip(180) + 4 * HOOK, abs=0.01)


def test_fix_length_120_five_hooks_even():
    b = load('P', 'build.json')['fix']
    assert b['hooks'] == 5
    assert (b['left_gap_mm'], b['right_gap_mm']) == (pytest.approx(20, abs=1e-6), pytest.approx(20, abs=1e-6))
    assert b['air_mm'] == pytest.approx([10] * 4, abs=1e-6)
    assert b['volume_mm3'] == pytest.approx(strip(180) + 5 * HOOK, abs=0.01)


def test_proof_formula_follows_220_and_6():
    b = load('P', 'build.json')['proof']
    assert b['length_mm'] == pytest.approx(160, abs=1e-6)
    assert b['hooks'] == 6
    assert (b['left_gap_mm'], b['right_gap_mm']) == (pytest.approx(20, abs=1e-6), pytest.approx(20, abs=1e-6))


def test_control_typed_120_at_220_leaves_60():
    b = load('P', 'build.json')['control']
    assert b['hooks'] == 6
    assert b['right_gap_mm'] == pytest.approx(60, abs=1e-6)


def test_your_turn_140_three_hooks_length_80():
    b = load('P', 'build.json')['yourturn']
    assert b['length_mm'] == pytest.approx(80, abs=1e-6)
    assert b['hooks'] == 3
    assert (b['left_gap_mm'], b['right_gap_mm']) == (pytest.approx(20, abs=1e-6), pytest.approx(20, abs=1e-6))


def test_numbers_file_has_every_section():
    if not os.path.exists(os.path.join(HERE, 'NUMBERS.json')):
        pytest.skip('NUMBERS.json not written yet')
    n = load('NUMBERS.json')
    for k in ('freecad', 'cases', 'g0', 'takes', 'claude_runs'):
        assert k in n
