"""fc16 (FreeCAD course lesson 16, a hanging hole in the back wall: Pocket depth vs the Thickness wall). Checks the
numbers lab/fc16parts.py measured under freecadcmd (out/fc16/P/build.json) against the plan (PLAN rev 2 2.1-2.4) and
the pass rule of the Claude-run score (PLAN 2.5, lab/fc16score.py).
Run: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_fc16.py"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lab'))
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc16')


def b():
    with open(os.path.join(HERE, 'P', 'build.json')) as f:
        return json.load(f)


def near(a, x, tol=0.01):
    return a is not None and abs(a - x) < tol


def quiet(state):   # no feature with a mark or a message (feat_state lists every feature's State + status string)
    return all(v[0] == ['Up-to-date'] and v[1] == 'Valid' for v in state.values())


def is_open(h):
    return all(h['axis_air'].values())


def test_q9_lesson15_rim_rebuilds_at_2_3_4_12():
    assert all(b()['q9'][k]['builds'] for k in ('2', '3', '4', '12'))


def test_q1_typed_2_at_wall_2_open_one_solid_no_message():
    q = b()['q1_typed_w2']
    assert q['builds'] and q['hole']['solids'] == 1 and is_open(q['hole']) and quiet(q['state'])
    assert near(q['hole']['back_hole_w'], 5.0, 0.02)


def test_q2_face_sketch_follows_wall():
    c = b()['q2']
    for w, y in (('2', 22), ('3', 23), ('4', 24)):
        assert near(c[w]['centre'][1], y) and near(c[w]['centre'][0], 0) and near(c[w]['centre'][2], 30)


def test_q3_trap_typed_2_at_wall_3_skin_1_closed_no_message():
    q = b()['q3_typed_w3']
    assert q['builds'] and quiet(q['state']) and not is_open(q['hole'])
    assert near(q['hole']['skin'], 1.0) and q['hole']['skin_mid_solid']


def test_q4_through_all_at_wall_3_front_holed_peg_kept():
    q = b()['q4_through_w3']['hole']
    assert is_open(q) and not q['front_solid'] and near(q['front_hole_w'], 5.0, 0.02)
    assert q['peg_solid'] and q['solids'] == 1 and near(q['inside_w'], 60) and near(q['inside_l'], 40)


def test_q5_fix_bound_open_front_closed_at_2_and_3():
    r = b()['q5']
    assert 'Params.wall' in (r['expr'] or '')
    for w in ('2', '3'):
        h = r[w]['hole']
        assert r[w]['builds'] and is_open(h) and h['front_solid'] and near(h['back_hole_w'], 5.0, 0.02)


def test_q6_proof_wall_4_then_hole_6_and_typed_comparison_skin_2():
    q = b()['q6']
    h4 = q['reopen_w4']['hole']
    assert is_open(h4) and h4['front_solid'] and near(h4['outside_w'], 68) and near(h4['outside_l'], 48)
    h6 = q['hole6']['hole']
    assert is_open(h6) and near(h6['back_hole_w'], 6.0, 0.02)
    assert near(q['typed_w4']['hole']['skin'], 2.0)


def test_q11_your_turns():
    q = b()['q11']
    assert near(q['long_2.5_w6']['hole']['skin'], 3.5) and q['long_2.5_w6']['hole']['front_solid']
    assert near(q['short_2_w4']['hole']['skin'], 2.0)


def test_score_needs_open_back_closed_front_and_bound_depth():
    from fc16score import passes

    def snap(w, open_=True, front=True, bound=True):
        return {'builds': True, 'wall': w, 'depth': {'type': 'Length', 'expr': 'Params.wall' if bound else None},
                'hole': {'axis_air': {'a': open_, 'b': open_, 'c': open_}, 'front_solid': front,
                         'dia_ok': True, 'peg_solid': True, 'solids': 1, 'inside_w': 60.0, 'inside_l': 40.0,
                         'inside_d': 50.0, 'top_open': True, 'outside_w': 60 + 2 * w}}
    walls = (2, 3, 12)
    assert passes({w: snap(w) for w in walls})[0]
    assert not passes({w: snap(w, front=False) for w in walls})[0]          # Through all
    assert not passes({w: snap(w, bound=False) for w in walls})[0]          # a big typed number (class 4)
    assert not passes({2: snap(2), 3: snap(3), 12: snap(12, open_=False)})[0]
