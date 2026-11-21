"""fc17 NUMBERS.json from the lab's outputs (out/fc17/P/build.json by code, runs/*): python3 lab/fc17numbers.py"""
import json
import os

X = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc17')
B = json.load(open(os.path.join(X, 'P', 'build.json')))
K = ('solids', 'volume', 'y_min', 'y_max', 'y_extent', 'behind_back', 'x_runs_front', 'x_runs_back', 'centre_gap', 'face_gap',
     'hole_open', 'inside', 'outside', 'top_open', 'plan_pts', 'bbox')


def h(s):
    d = {k: s['m'].get(k) for k in K}
    d.update(builds=s['builds'], peg_x=s['peg_x'], wall=s['wall'], peg_size=s['peg_size'], state=s['state'],
             mirrors=s['mirrors'])
    return d


N = {'source': 'out/fc17/P/build.json (lab/fc17parts.py, freecadcmd 1.1.4) + out/fc17/runs/*',
     'start_file': B['start_file'] + ' + Params peg_x 15 (Sketch001 peg_x0 = Params.peg_x - Params.peg_size / 2)',
     'q1_peg_moved': h(B['q1']['peg_moved']), 'q1_peg_x20': h(B['q1']['peg_x20']),
     'q10_lesson16_cup': {k: h(v) for k, v in B['q10'].items()},
     'q2_trap': h(B['q2']), 'q2_trap_reopened': h(B['q2_reopened']),
     'q4_fix_yz': h(B['q4']['yz']), 'q4_fix_vaxis': h(B['q4']['vaxis']),
     'q5_xy': h(B['q5_xy']), 'q5_whole_shape_xy': h(B['q5_whole_xy']),
     'q6_proof': {k: h(v) for k, v in B['q6'].items()},
     'ref_volumes': B['ref_volumes'], 'trap_at_score_settings': {k: h(v) for k, v in B['trap_at_sets'].items()},
     'q11': {k: v for k, v in B['q11'].items() if k != 'short_peg25'}, 'q11_short_peg25': h(B['q11']['short_peg25']),
     'runs': {}}
for run in ('A1', 'B1'):
    d = os.path.join(X, 'runs', run)
    if not os.path.exists(os.path.join(d, 'after.check.json')):
        continue
    c = json.load(open(os.path.join(d, 'after.check.json')))
    m = json.load(open(os.path.join(d, 'meta.json')))
    N['runs'][run] = {'cost_usd': float(m['cost_usd']), 'wall_s': m['wall_s'], 'pass': c['pass'],
                      'failed_criteria': {k: [x for x, y in v.items() if not y] for k, v in c['criteria'].items()},
                      'asis': c['asis'], 'mirrors_as_saved': c['stored']['mirrors'], 'tree': c['tree']['group'],
                      'at': {k: h(v) for k, v in c['at'].items() if 'm' in v}}
N['runs_total_usd'] = round(sum(r['cost_usd'] for r in N['runs'].values()), 4)
json.dump(N, open(os.path.join(X, 'NUMBERS.json'), 'w'), indent=1, default=str)
print('NUMBERS', N['runs_total_usd'], {k: (v['pass'], v['cost_usd']) for k, v in N['runs'].items()})
