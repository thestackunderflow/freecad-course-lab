"""fc17 (FreeCAD course lesson 17, a second key peg by Mirror: the plane is the fold between them). Checks the numbers
lab/fc17parts.py measured under freecadcmd (out/fc17/P/build.json) against the plan (PLAN rev 2 2.1-2.4) and the pass
rule of the Claude-run score (PLAN 2.5, lab/fc17score.py).
Run: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_fc17.py"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lab'))
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc17')


def b():
    with open(os.path.join(HERE, 'P', 'build.json')) as f:
        return json.load(f)


def near(a, x, tol=0.01):
    return a is not None and abs(a - x) < tol


def quiet(state):
    return all(v[0] == ['Up-to-date'] and v[1] == 'Valid' for v in state.values())


def test_q1_peg_moved_follows_peg_x_one_solid():
    q = b()['q1']
    m = q['peg_moved']['m']
    assert q['peg_moved']['builds'] and m['solids'] == 1 and near(m['x_runs_front'][0][0], 10) and near(m['x_runs_front'][0][1], 20)
    m20 = q['peg_x20']['m']
    assert near(m20['x_runs_front'][0][0], 15) and near(m20['x_runs_front'][0][1], 25)


def test_q10_lesson16_cup_rebuilds_with_peg_at_15_hole_open():
    for w, v in b()['q10'].items():
        assert v['builds'] and v['m']['hole_open'], w


def test_q2_trap_xz_copy_out_the_back_13_one_solid_no_message():
    q = b()['q2']['m']
    assert b()['q2']['builds'] and quiet(b()['q2']['state'])
    assert q['solids'] == 1 and q['pt']['back_orig'] and not q['pt']['copy']
    assert near(q['y_extent'], 70) and near(q['behind_back'], 13) and q['hole_open']


def test_q4_fix_yz_and_vaxis_copy_beside_30_apart_back_clear():
    for k in ('yz', 'vaxis'):
        q = b()['q4'][k]['m']
        assert q['solids'] == 1 and q['pt']['copy'] and not q['pt']['back_orig'] and not q['pt']['back_copy']
        assert near(q['y_extent'], 57) and near(q['centre_gap'], 30) and near(q['face_gap'], 20)
        assert near(q['x_runs_front'][0][0], -20) and near(q['x_runs_front'][1][1], 20)
    assert near(b()['q4']['yz']['m']['volume'], b()['q4']['vaxis']['m']['volume'], 0.01)


def test_q6_proof_peg_x_20_size_12_wall_3_and_comparison():
    q = b()['q6']
    assert near(q['peg_x20']['m']['centre_gap'], 40) and not q['peg_x20']['m']['pt']['back_orig']
    r = q['peg_size12']['m']['x_runs_front']
    assert near(r[0][1] - r[0][0], 12) and near(r[1][1] - r[1][0], 12)
    w3 = q['wall3']['m']
    assert w3['solids'] == 1 and near(w3['y_extent'], 58) and w3['pt']['copy']
    c = q['xz_peg_x20']['m']
    assert c['pt']['back_orig'] and near(c['x_runs_back'][0][0], 15) and near(c['x_runs_back'][0][1], 25)


def test_q11_your_turn_and_short():
    q = b()['q11']
    assert near(q['corner_cup_yz_copy_centre_x'], -45) and q['corner_cup_yz_copy_on_cup'] is False
    assert near(q['corner_cup_fold30_copy_centre_x'], 15)
    assert near(q['short_peg25_copy_centre_x'], -25)


def test_score_rejects_typed_copy_back_copy_and_moved_names():
    from fc17score import criteria_ok

    def snap(px, copy=True, back=False, follow=True):
        cx = -px if follow else -15
        return {'builds': True, 'bad_any': {}, 'peg_x': px, 'wall': 2.0, 'peg_size': 10.0, 'volume': 100.0,
                'm': {'solids': 1, 'y_min': -35.0, 'y_max': 22.0 + (13 if back else 0), 'hole_open': True,
                      'inside': [60.0, 40.0, 50.0], 'top_open': True,
                      'probe': {'orig': True, 'copy': copy and follow, 'back_orig': back, 'back_copy': False,
                                'across': True, 'tips': True, 'height': True, 'back_wall': True}}}
    ref = {'15': 100.0, '20': 100.0, '8': 100.0, 'w3': 100.0}
    good = {'15': snap(15), '20': snap(20), '8': snap(8), 'w3': snap(15)}
    asis = {'names_same': True, 'peg_x': 15.0, 'bad_any': {}}
    assert criteria_ok(good, asis, ref)[0]
    assert not criteria_ok({k: snap(15 if k in ('15', 'w3') else int(k), follow=k in ('15', 'w3')) for k in good},
                           asis, ref)[0]   # a second peg typed at -15
    assert not criteria_ok({k: snap(15, back=True, copy=False) for k in good}, asis, ref)[0]   # the trap
    assert not criteria_ok(good, dict(asis, names_same=False), ref)[0]


def test_numbers_runs_within_cap():
    n = json.load(open(os.path.join(HERE, 'NUMBERS.json')))
    assert n['runs_total_usd'] <= 0.50 and all(r['cost_usd'] <= 0.25 for r in n['runs'].values())
    assert near(n['q2_trap']['behind_back'], 13) and near(n['q4_fix_yz']['centre_gap'], 30)
