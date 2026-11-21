"""fc16 NUMBERS.json from the lab's outputs (out/fc16/P/build.json by code, runs/*): python3 lab/fc16numbers.py"""
import json
import os

X = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc16')
B = json.load(open(os.path.join(X, 'P', 'build.json')))


def h(s, *keys):
    return {k: s['hole'].get(k) for k in keys}


K = ('skin', 'pit_depth', 'back_hole_w', 'front_solid', 'front_hole_w', 'peg_solid', 'outside_w', 'outside_l', 'inside_w',
     'inside_l', 'inside_d', 'solids', 'volume')
N = {'source': 'out/fc16/P/build.json (lab/fc16parts.py, freecadcmd 1.1.4) + out/fc16/runs/*',
     'start_file': B['start_file'],
     'q9_branch': {'lesson14_cup_builds': {w: v['builds'] for w, v in B['q9'].items()},
                   'lesson15_rim_both_builds': {w: v['builds'] for w, v in B['q9_lesson15_rim_both'].items()}},
     'pocket_types': B['pocket_types'],
     'q1_typed2_wall2': dict(h(B['q1_typed_w2'], *K), open=all(B['q1_typed_w2']['hole']['axis_air'].values()),
                             face=B['q1_typed_w2']['face'], reversed=B['q1_typed_w2']['reversed'],
                             sketch_normal=B['q1_typed_w2']['sketch_normal']),
     'q2_sketch_centre': {w: v['centre'] for w, v in B['q2'].items()},
     'q2_support': {w: v['support'] for w, v in B['q2'].items()},
     'q3_typed2_wall3': dict(h(B['q3_typed_w3'], *K), axis_air=B['q3_typed_w3']['hole']['axis_air'],
                             state=B['q3_typed_w3']['state']),
     'q4_through_wall3': dict(h(B['q4_through_w3'], *K), axis_air=B['q4_through_w3']['hole']['axis_air']),
     'q4_through_wall2': h(B['through_w2'], *K),
     'q5_fix_expr': B['q5']['expr'],
     'q5_fix': {w: dict(h(B['q5'][w], *K), open=all(B['q5'][w]['hole']['axis_air'].values())) for w in ('2', '3')},
     'q6_proof': {k: dict(h(B['q6'][k], *K), open=all(B['q6'][k]['hole']['axis_air'].values()))
                  for k in ('reopen_w2', 'reopen_w4', 'hole6', 'typed_w4')},
     'q7_second_ways': {k: v for k, v in B['q7'].items()},
     'q10_hole_tool': B['q10'],
     'q11_your_turn': {k: h(v, 'skin', 'front_solid') for k, v in B['q11'].items()},
     'runs': {}}
for run in ('A1', 'B1'):
    d = os.path.join(X, 'runs', run)
    if not os.path.exists(os.path.join(d, 'after.check.json')):
        continue
    c = json.load(open(os.path.join(d, 'after.check.json')))
    m = json.load(open(os.path.join(d, 'meta.json')))
    N['runs'][run] = {'cost_usd': float(m['cost_usd']), 'wall_s': m['wall_s'], 'pass': c['pass'],
                      'criteria': c['criteria'], 'depth_stored': c['stored']['depth'],
                      'at_walls': {w: dict(depth=c['at_wall%s' % w]['depth'],
                                           **h(c['at_wall%s' % w], 'skin', 'back_hole_w', 'front_solid', 'outside_w'))
                                   for w in (2, 3, 12)},
                      'wall_left': c['stored']['wall'], 'tree': c['tree']['group']}
N['runs_total_usd'] = round(sum(r['cost_usd'] for r in N['runs'].values()), 4)
json.dump(N, open(os.path.join(X, 'NUMBERS.json'), 'w'), indent=1, default=str)
print('NUMBERS', N['runs_total_usd'], {k: (v['pass'], v['cost_usd']) for k, v in N['runs'].items()})
