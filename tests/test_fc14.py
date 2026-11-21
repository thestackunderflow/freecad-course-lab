"""fc14 (FreeCAD course lesson 14, a key peg on the wall cup: the Thickness's place in the Body). Checks the numbers
lab/fc14parts.py measured under freecadcmd (out/fc14/P/build.json) against the plan's arithmetic (PLAN rev 2.1 2.1-2.4,
ACCURACY C6-C8, C19, C23) and the pass rule of the Claude-run score (PLAN 2.5, lab/fc14parts.score).
Run: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_fc14.py"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lab'))
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc14')


def case(name):
    with open(os.path.join(HERE, 'P', 'build.json')) as f:
        return json.load(f)[name]


def near(a, b, tol=0.01):
    return a is not None and abs(a - b) < tol


def cup_ok(r, wall=2):
    return (near(r['inside_w'], 60) and near(r['inside_l'], 40) and near(r['inside_d'], 50)
            and r['faces']['ok'] and near(r['outside_w'], 60 + 2 * wall))


def test_noshell_peg_on_the_moved_xz_plane_y_minus_35_to_minus_20():
    r = case('noshell')
    assert r['solids'] == 1 and r['peg_attach']['support'] == 'XZ_Plane'
    assert near(r['peg_y'][0], -35) and near(r['peg_y'][1], -20)
    assert r['peg_attach']['offset_expr'] and 'cup_length' in r['peg_attach']['offset_expr']
    assert r['peg_mid_solid'] and near(r['peg_w'], 10) and near(r['peg_h'], 10)


def test_trap_peg_14_hollow_open_into_the_cup_tip_minus_37():
    r = case('trap')
    assert r['solids'] == 1 and r['thickness']['reversed'] is False
    assert near(r['peg_w'], 14) and near(r['peg_h'], 14) and near(r['peg_tip_y'], -37)
    assert r['peg_mid_solid'] is False and r['front_wall_solid'] is False
    assert near(r['opening_w'], 10) and near(r['opening_h'], 10)
    assert near(r['inside_w'], 60) and near(r['inside_l'], 40) and near(r['inside_d'], 50)


def test_fixed_peg_10_solid_wall_closed_faces_right():
    r = case('fixed')
    assert r['solids'] == 1 and r['peg_mid_solid'] and r['front_wall_solid']
    assert near(r['peg_w'], 10) and near(r['peg_h'], 10) and near(r['peg_x'][0], -5) and near(r['peg_z'][0], 35)
    assert cup_ok(r)


def test_proof_wall3_then_peg12():
    r = case('fixed_wall3')
    assert near(r['peg_w'], 10) and r['peg_mid_solid'] and r['front_wall_solid'] and cup_ok(r, 3)
    assert near(r['outside_l'], 46)
    r = case('fixed_peg12')
    assert near(r['peg_w'], 12) and near(r['peg_h'], 12) and r['peg_mid_solid'] and cup_ok(r, 3)


def test_comparison_trap_at_wall3_is_16_hollow():
    r = case('trap_wall3')
    assert near(r['peg_w'], 16) and r['peg_mid_solid'] is False


def test_your_turn_and_short():
    assert near(case('yt_before')['peg_w'], 13) and case('yt_before')['peg_mid_solid'] is False
    assert near(case('yt_after')['peg_w'], 7) and case('yt_after')['peg_mid_solid'] is True
    assert near(case('short_before')['peg_w'], 18) and case('short_before')['peg_mid_solid'] is False


def test_score_pass_rule():
    from fc14score import passes
    good = case('fixed')
    assert passes(good, case('fixed_wall3'))[0] is True
    assert passes(case('trap'), case('trap_wall3'))[0] is False
