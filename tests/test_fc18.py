"""fc18 (FreeCAD course lesson 18, a round pen cup by Revolve: the outline's width is the radius). Checks the numbers
lab/fc18parts.py measured under freecadcmd (out/fc18/P/build.json) against the plan (PLAN rev 2 2.1-2.4) and the pass
rule of the Claude-run score (PLAN 2.5, lab/fc18score.py).
Run: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_fc18.py"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lab'))
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc18')


def b():
    with open(os.path.join(HERE, 'P', 'build.json')) as f:
        return json.load(f)


def near(a, x, tol=0.01):
    return a is not None and abs(a - x) < tol


def vol(dia, h=80.0, w=2.0):
    r = dia / 2.0
    return math.pi * (r * r * h - (r - w) ** 2 * (h - w))


def quiet(state):
    return all(v[0] == ['Up-to-date'] and v[1] == 'Valid' for v in state.values())


def cup(s, dia, h=80.0, w=2.0, tol=1.0):
    m = s['m']
    return (s['builds'] and m['solids'] == 1 and near(m['outside_x'], dia) and near(m['outside_y'], dia)
            and near(m['z'][0], 0) and near(m['z'][1], h) and near(m['inside'], dia - 2 * w)
            and m['floor_ok'] and m['top_open'] and near(m['volume'], vol(dia, h, w), tol))


def test_q1_four_start_files_one_solid_names_bound():
    q = b()['q1']
    for k in ('round-start', 'round-name', 'round-typed30', 'round-fixed'):
        assert k in q['files'], k
    for k in ('round-name', 'round-typed30', 'round-fixed'):
        assert q[k]['builds'] and q[k]['m']['solids'] == 1 and q[k]['sketch_dof'] == 0, k
    assert q['round-fixed']['width_expr'] == 'Params.cup_diameter / 2'
    assert q['round-name']['width_expr'] == 'Params.cup_diameter'
    assert q['round-typed30']['width_expr'] is None


def test_q2_upright_on_xy_z_0_80_top_open():
    s = b()['q1']['round-fixed']['m']
    assert near(s['z'][0], 0) and near(s['z'][1], 80) and s['top_open'] and s['floor_ok']


def test_q3_trap_120_no_message_and_typed60_same():
    q = b()['q3']
    assert cup(q['name'], 120.0) and quiet(q['name']['state'])
    assert near(q['name']['m']['volume'], 80450, 1)
    assert near(q['typed60']['m']['volume'], q['name']['m']['volume'], 0.01) and near(q['typed60']['m']['outside_x'], 120)


def test_q4_fix_60_across_volume_34080():
    s = b()['q1']['round-fixed']
    assert cup(s, 60.0) and near(s['m']['volume'], 34080, 1) and near(s['width_value'], 30)


def test_q5_proof_80_and_comparison():
    q = b()['q5']
    assert cup(q['fixed_reopened_80'], 80.0) and near(q['fixed_reopened_80']['m']['volume'], 48280, 1)
    assert near(q['name_80']['m']['outside_x'], 160) and near(q['typed30_80']['m']['outside_x'], 60)


def test_q6_builds_at_sizes_and_walls():
    for k, s in b()['q6'].items():
        dia, w = s['set']['cup_diameter'], s['set']['wall']
        assert cup(s, dia, 80.0, w), k


def test_q9_your_turn_and_short():
    q = b()['q9']
    assert near(q['fixed_45']['m']['outside_x'], 45) and near(q['fixed_45']['width_value'], 22.5)
    assert near(q['name_45']['m']['outside_x'], 90) and near(q['name_40']['m']['outside_x'], 80)


def test_scorer_pass_fixed_fail_trap_and_typed30():
    sc = {}
    for k in ('round-fixed', 'round-name', 'round-typed30'):
        with open(os.path.join(HERE, 'G0', 'score', k + '.check.json')) as f:
            sc[k] = json.load(f)
    assert sc['round-fixed']['pass'] and sc['round-fixed']['cls'] == 1
    assert not sc['round-name']['pass'] and sc['round-name']['cls'] == 3
    assert not sc['round-typed30']['pass'] and sc['round-typed30']['cls'] == 2
    assert sc['round-typed30']['criteria']['60']['a'] and not sc['round-typed30']['criteria']['80']['a']


def test_numbers_json_has_runs():
    with open(os.path.join(HERE, 'NUMBERS.json')) as f:
        n = json.load(f)
    assert set(n['runs']) == {'A1', 'B1'} and n['runs_total_usd'] <= 0.50
    assert near(n['q3_trap']['outside_x'], 120) and near(n['q4_fix']['outside_x'], 60)
