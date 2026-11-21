"""fc15 (FreeCAD course lesson 15, a soft rim: the round has to fit in the wall). Checks the numbers lab/fc15parts.py
measured under freecadcmd (out/fc15/P/build.json) against the plan (PLAN rev 2 2.2-2.4, ACCURACY C15, C17-C18) and the
pass rule of the Claude-run score (PLAN 2.5, lab/fc15score.py).
Run: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_fc15.py"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lab'))
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc15')


def b():
    with open(os.path.join(HERE, 'P', 'build.json')) as f:
        return json.load(f)


def near(a, x, tol=0.01):
    return a is not None and abs(a - x) < tol


def test_rim_start_rim_2_wide_names_bound():
    q = b()['q1']
    assert q['params'] == {'wall': 2.0, 'rim_out': 3.0, 'rim_in': 1.0, 'peg_size': 10.0}
    assert near(q['snap']['rim']['flat'], 2.0) and len(q['outer_edges']) == 8 and len(q['inner_edges']) == 4


def test_trap_round_3_not_built_shape_unchanged():
    q = b()['q2_trap_r3']
    assert not q['builds'] and q['unchanged_vs_start'] and q['rim']['points']['corner_pt_31.95']


def test_fix_1_5_one_click_rounds_all_8_segments_flat_0_5():
    q = b()['fix_r1_5']
    assert q['builds'] and near(q['rim']['flat'], 0.5) and q['rim']['round_radii']['out'] == [1.5]
    assert all(q['rim']['points'].get(k) for k in ('out_air_+x', 'out_air_-x', 'out_air_+y', 'out_air_-y', 'out_air_corner'))


def test_second_edge_1_fails_and_proof_wall_3_builds_bracket_2_6_2_4():
    r = b()
    assert not r['second_edge_1']['builds']
    w = r['q4_walls']
    assert w['wall_3_0']['builds'] and near(w['wall_3_0']['rim']['flat'], 0.5)
    assert not w['wall_2_1']['builds'] and w['wall_2.6_2']['builds'] and not w['wall_2.4_3']['builds']


def test_equal_sum_fails_so_rule_is_less_than():
    q = b()['q3']
    assert not q['out_2.00']['builds'] and not q['out1_in1']['builds'] and not q['out1.5_in0.5']['builds']


def test_your_turns():
    q = b()['q8']
    assert not q['long_1.2_1.5_w2.5']['builds'] and q['long_1.2_1.2_w2.5']['builds'] and q['short_0.8_1_w2']['builds']


def _snap(ok, ro, ri, flat, w):
    return {'builds': ok, 'rim': {'round_radii': {'out': [ro] if ro else [], 'in': [ri] if ri else []},
                                  'round_faces': {'out': 4 if ro else 0, 'in': 4 if ri else 0}, 'flat': flat,
                                  'outside_w': 60 + 2 * w, 'inside_w': 60, 'm_inside_l': 40, 'm_inside_d': 50,
                                  'm_peg_w': 10, 'm_peg_mid_solid': True, 'wall': w}}


def test_score_pass_needs_both_rounds_build_at_three_walls():
    from fc15score import passes
    good = {2: _snap(True, 0.9, 0.5, 0.6, 2), 3: _snap(True, 1.35, 0.75, 0.9, 3), 1.6: _snap(True, 0.72, 0.4, 0.48, 1.6)}
    ok, det = passes(good)
    assert ok
    bad = dict(good)
    bad[1.6] = _snap(False, 0.72, 0.4, 0.48, 1.6)
    assert not passes(bad)[0]
    one = {k: _snap(True, v['rim']['round_radii']['out'][0], None, 1, k) for k, v in good.items()}
    assert not passes(one)[0]
    assert near(det[2]['sum_fraction'], 0.7)
