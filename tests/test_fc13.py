"""fc13 (FreeCAD course lesson 13, a wall cup: Thickness and "Make thickness inwards"). Checks the numbers
lab/fc13parts.py measured under freecadcmd (out/fc13/P/build.json) against the plan's arithmetic (PLAN 2.2-2.4, ACCURACY
C8-C12), and the Claude-run classes of lab/fc13score.py (PLAN 2.5, out/fc13/PREREG.md).
Run: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_fc13.py"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lab'))
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc13')


def case(name):
    with open(os.path.join(HERE, 'P', 'build.json')) as f:
        return json.load(f)[name]


def near(a, b, tol=0.01):
    return a is not None and abs(a - b) < tol


def inside(r, w, l, d):
    return near(r['inside_w'], w) and near(r['inside_l'], l) and near(r['inside_d'], d)


def test_box_is_solid_names_bound_and_inward_is_the_default():
    r = case('box')
    assert r['solids'] == 1 and not r['hollow']
    assert near(r['outside_w'], 60) and near(r['outside_l'], 40) and near(r['outside_h'], 50)
    assert case('default_reversed') is True


def test_trap_inward_gives_56_36_48():
    r = case('trap')
    assert r['solids'] == 1 and r['hollow'] and r['thickness']['reversed'] is True
    assert inside(r, 56, 36, 48) and near(r['outside_w'], 60) and near(r['wall_x'], 2)
    assert 'wall' in (r['thickness']['value_expr'] or '')


def test_fix_outward_gives_60_40_50_outside_64_44_floor_minus_2():
    r = case('fixed')
    assert r['thickness']['reversed'] is False
    assert inside(r, 60, 40, 50) and near(r['outside_w'], 64) and near(r['outside_l'], 44) and near(r['floor_z'], -2)


def test_proof_wall_3_and_width_70_and_comparison():
    assert inside(case('fixed_w3'), 60, 40, 50) and near(case('fixed_w3')['wall_x'], 3)
    assert near(case('fixed_w3')['outside_w'], 66) and near(case('fixed_w3')['outside_l'], 46)
    assert inside(case('fixed_cw70'), 70, 40, 50)
    assert inside(case('typed'), 60, 40, 50 - 2 + 2)     # typed 64 x 44 x 52, inward wall 2
    assert inside(case('typed_w3'), 58, 38, 49)


def test_your_turn_and_short():
    assert near(case('yt_in')['inside_w'], 74) and near(case('yt_in')['inside_d'], 47)
    yo = case('yt_out')
    assert near(yo['inside_w'], 80) and near(yo['inside_d'], 50) and near(yo['outside_w'], 86) and near(yo['outside_h'], 53)
    assert near(case('short_in')['inside_w'], 42) and near(case('short_in')['inside_d'], 46)


def test_score_classes():
    import fc13score as S
    ok = {'inside_w': 60, 'inside_l': 40, 'inside_d': 50, 'wall_x': 2, 'hollow': True, 'solids': 1}
    ok3 = dict(ok, wall_x=3)
    ok70 = dict(ok, inside_w=70)
    out_bound = {'reversed': False, 'value_expr': 'Params.wall', 'value': 2}
    assert S.classify(dict(ok, thickness=out_bound), dict(ok3, thickness=out_bound), dict(ok70))[0] == '1'
    out_typed = {'reversed': False, 'value_expr': None, 'value': 2}
    assert S.classify(dict(ok, thickness=out_typed), dict(ok, thickness=out_typed), ok70)[0] == '3'
    in_bound = {'reversed': True, 'value_expr': 'Params.wall', 'value': 2}
    assert S.classify(dict(ok, thickness=in_bound), dict(ok3, thickness=in_bound), ok70)[0] == '2'
    typed = dict(ok, thickness=in_bound, sizes_typed=True)
    assert S.classify(typed, dict(typed, inside_w=58, inside_l=38, wall_x=3), ok70)[0] == '4'
    gone = {'inside_w': 0, 'inside_l': 0, 'inside_d': 0, 'hollow': False, 'solids': 1, 'thickness': None}
    assert S.classify(gone, gone, gone)[0] == '7'
    assert S.classify(None, None, None)[0] == '8'
