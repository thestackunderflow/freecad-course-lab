"""fc18 NUMBERS.json from the lab's outputs (out/fc18/P/build.json by code, runs/*): python3 lab/fc18numbers.py"""
import json
import os

X = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc18')
B = json.load(open(os.path.join(X, 'P', 'build.json')))
K = ('outside_x', 'outside_y', 'z', 'inside', 'volume', 'solids', 'valid', 'floor_ok', 'top_open', 'ring_ok', 'bbox')


def h(s):
    d = {k: s['m'].get(k) for k in K}
    d.update(builds=s['builds'], cup_diameter=s['cup_diameter'], wall=s['wall'], cup_height=s['cup_height'],
             width_value=s.get('width_value'), width_expr=s.get('width_expr'), state=s['state'])
    return d


N = {'source': 'out/fc18/P/build.json (lab/fc18parts.py, freecadcmd 1.1.4) + out/fc18/runs/*',
     'start_file': 'round-start.FCStd: Params cup_diameter 60, cup_height 80, wall 2; empty Body (Cup)',
     'q1': {k: h(B['q1'][k]) for k in ('round-name', 'round-typed30', 'round-fixed', 'round-typed60')},
     'q1_sketch': B['q1']['round-fixed']['sketches'], 'q1_revolution': B['q1']['round-fixed']['revolutions'],
     'q2_edges': {k: h(v) for k, v in B['q2'].items()},
     'q3_trap': h(B['q3']['name']), 'q3_typed60': h(B['q3']['typed60']), 'q3_trap_reopened': h(B['q3']['name_reopened']),
     'q4_fix': h(B['q1']['round-fixed']),
     'q5': {k: h(v) for k, v in B['q5'].items()},
     'q6': {k: h(v) for k, v in B['q6'].items()},
     'q9': {k: h(v) for k, v in B['q9'].items()},
     'volume_ratio_trap_to_fix': round(B['q3']['name']['m']['volume'] / B['q1']['round-fixed']['m']['volume'], 4),
     'runs': {}}
for run in ('A1', 'B1'):
    d = os.path.join(X, 'runs', run)
    if not os.path.exists(os.path.join(d, 'after.check.json')):
        continue
    c = json.load(open(os.path.join(d, 'after.check.json')))
    m = json.load(open(os.path.join(d, 'meta.json')))
    calls = [ln for ln in open(os.path.join(d, 'tools.txt'), encoding='utf-8') if ln.startswith('CALL')]
    N['runs'][run] = {'cost_usd': float(m['cost_usd']), 'wall_s': m['wall_s'], 'tool_calls': len(calls), 'pass': c['pass'],
                      'cls': c['cls'], 'failed_criteria': {k: [x for x, y in v.items() if not y] for k, v in c['criteria'].items()},
                      'e_revolve_in_body': c['e_revolve_in_body'], 'f_reads_cup_diameter': c['f_reads_cup_diameter'],
                      'asis': c['asis'], 'sketches': c['recomputed']['sketches'], 'revolutions': c['recomputed']['revolutions'],
                      'tree': c['tree'].get('group'), 'at': {k: h(v) for k, v in c['at'].items() if 'm' in v}}
N['runs_total_usd'] = round(sum(r['cost_usd'] for r in N['runs'].values()), 4)
json.dump(N, open(os.path.join(X, 'NUMBERS.json'), 'w'), indent=1, default=str)
print('NUMBERS', N['runs_total_usd'], {k: (v['pass'], v['cls'], v['cost_usd']) for k, v in N['runs'].items()})
