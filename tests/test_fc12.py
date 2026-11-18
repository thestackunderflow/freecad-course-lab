"""fc12 (FreeCAD course lesson 12, PolarPattern Extent vs Spacing: hooks round a post). Checks the numbers
lab/fc12parts.py measured under freecadcmd (out/fc12/P/build.json) against the plan's arithmetic (PLAN 2.2-2.4), and the
Claude-run classes of lab/fc12score.py (PLAN 2.5, out/fc12/PREREG.md).
Run: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_fc12.py"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lab'))
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc12')


def case(name):
    with open(os.path.join(HERE, 'P', 'build.json')) as f:
        return json.load(f)[name]


def near(a, b, tol=0.01):
    return len(a) == len(b) and all(abs(x - y) < tol for x, y in zip(a, b))


def test_ring_is_six_hooks_60_apart_one_solid_count_bound():
    r = case('ring')
    assert near(r['angles'], [0, 60, 120, 180, 240, 300])
    assert r['solids'] == 1 and r['count_bound']
    assert r['clearance_mm'] > 0


def test_trap_4_at_240_gives_80_and_a_hook_in_the_wall():
    r = case('trap')
    assert near(r['angles'], [0, 80, 160, 240])
    assert r['into_wall'] and r['count_bound']


def test_fix_spacing_bound_to_hook_gap_gives_60():
    r = case('fixed')
    assert r['pattern']['mode'] == 'Spacing'
    assert near(r['angles'], [0, 60, 120, 180]) and r['side_ok']


def test_proof_hooks_3_and_6_and_control():
    assert near(case('fixed_h3')['angles'], [0, 60, 120])
    assert near(case('fixed_h6')['angles'], [0, 60, 120, 180, 240, 300])
    assert near(case('typed180_h3')['angles'], [0, 90, 180])


def test_your_turn_8_hooks():
    assert near(case('yt_360')['gaps'], [45] * 7)
    assert near(case('yt_315')['gaps'], [45] * 7)
    assert near(case('yt_270')['gaps'], [270 / 7] * 7)


def test_score_classes():
    import fc12score as S
    good = {'angles': [0, 60, 120, 180], 'count_bound': True, 'pattern': {'mode': 'Spacing', 'offset_expr': 'Params.hook_gap'}}
    at3 = {'angles': [0, 60, 120], 'count_bound': True}
    at6 = {'angles': [0, 60, 120, 180, 240, 300], 'count_bound': True}
    assert S.classify(good, at3, at6, False)[0] == 1
    typed = {'angles': [0, 60, 120, 180], 'count_bound': True, 'pattern': {'mode': 'Extent', 'angle_expr': None}}
    assert S.classify(typed, {'angles': [0, 90, 180], 'count_bound': True}, at6, False)[0] == 2
    sp60 = {'angles': [0, 60, 120, 180], 'count_bound': True, 'pattern': {'mode': 'Spacing', 'offset_expr': None}}
    assert S.classify(sp60, at3, at6, False)[0] == 3
    unbound = dict(good, count_bound=False)
    assert S.classify(unbound, {'angles': [0, 60, 120, 180], 'count_bound': False}, at6, False)[0] == 5
    assert S.classify(None, None, None, False)[0] == 8
