"""fc14: every number the lesson may show, collected from the lab's own outputs -> out/fc14/NUMBERS.json
    python lab/fc14numbers.py"""
import glob
import json
import os
import re

X = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc14')
KEYS = ('peg_w', 'peg_h', 'peg_x', 'peg_z', 'peg_y', 'peg_tip_y', 'peg_mid_solid', 'front_wall_solid', 'opening_w',
        'opening_h', 'inside_w', 'inside_l', 'inside_d', 'outside_w', 'outside_l', 'floor_top', 'rim_top', 'faces',
        'solids', 'valid', 'volume', 'wall_param', 'peg_param')


def ld(*p):
    f = os.path.join(X, *p)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else None


def slim(r):
    if not r:
        return None
    out = {k: r.get(k) for k in KEYS}
    t = r.get('thickness') or {}
    tr = r.get('tree') or {}
    out.update(thickness_base=t.get('base'), reversed=t.get('reversed'), value_expr=t.get('value_expr'),
               order=tr.get('group'), tip=tr.get('tip'), peg_sketch=(r.get('peg_attach') or {}).get('support'))
    for k in ('move', 'peg_body_solids', 'peg_body_volume', 'error'):
        if r.get(k) is not None:
            out[k] = r[k]
    return out


def take_lines(t, pat):
    f = os.path.join(X, t, 'take.log')
    if not os.path.exists(f):
        return []
    return [ln.strip()[:400] for ln in open(f, encoding='utf-8', errors='replace') if re.search(pat, ln)]


def check(path):
    r = ld(*path)
    if not r:
        return None
    return {'pass': r.get('pass'), 'criteria': r.get('criteria'),
            **{k: slim(r.get(k)) for k in ('stored', 'recomputed', 'at_wall2', 'at_wall3', 'at_wall3_peg12')}}


b = ld('P', 'build.json') or {}
N = {'source': 'freecad-course-lab out/fc14 (lab/fc14parts.py build + check, takes, runs); FreeCAD 1.1.4, freecad-mcp 0.1.28',
     'build': {k: slim(v) for k, v in b.items() if isinstance(v, dict)},
     'G0': {'trap_gui': check(('G0', 'q2-trap-gui.check.json')), 'route_c_gui': check(('G0', 'q3c-fixed-gui.check.json'))},
     'takes': {}, 'runs': {}}
for t in 'RHTMFPY':
    f = os.path.join(X, t, 'screen.mp4')
    N['takes'][t] = {'measure': take_lines(t, r'measure:'), 'state': take_lines(t, r'^(after OK|fixed|wall 3|peg 12|after Delete|H end)'),
                     'messages': take_lines(t, r'^messages|notices at'), 'check': check((t, 'check.json'))}
for run in ('A1', 'B1'):
    d = os.path.join(X, 'runs', run)
    if not os.path.isdir(d):
        continue
    meta = ld('runs', run, 'meta.json') or {}
    N['runs'][run] = {'cost_usd': meta.get('cost_usd'), 'wall_s': meta.get('wall_s'),
                      'prompt': open(os.path.join(d, 'prompt.txt'), encoding='utf-8').read().strip(),
                      'tool_calls': sum(1 for ln in open(os.path.join(d, 'tools.txt'), encoding='utf-8') if ln.startswith('CALL')),
                      'score': check(('runs', run, 'after.check.json'))}
json.dump(N, open(os.path.join(X, 'NUMBERS.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('NUMBERS', len(N['build']), 'build cases;', 'runs', {k: (v['cost_usd'], (v['score'] or {}).get('pass')) for k, v in N['runs'].items()})
