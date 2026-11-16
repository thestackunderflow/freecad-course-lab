"""fc9: every number of the lab into out/fc9/NUMBERS.json, read only from files code wrote (P/build.json, the takes'
check.json / take.log, G0 files, the Claude runs' check.json / meta.json / costguard.json).
    python3 lab/fc9numbers.py [/lab/out/fc9]"""
import glob
import json
import os
import re
import sys

X = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc9')


def j(*p):
    f = os.path.join(X, *p)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else None


def txt(*p):
    f = os.path.join(X, *p)
    return open(f, encoding='utf-8', errors='replace').read() if os.path.exists(f) else ''


KEYS = ('hooks', 'hooks_on_strip', 'floating', 'left_gap_mm', 'right_gap_mm', 'air_mm', 'starts', 'solids',
        'volume_mm3', 'length_mm', 'occurrences', 'allow_compound', 'rack_width')


def take(t):
    log = txt(t, 'take.log')
    meas = {m.group(1): m.group(2).strip() for m in re.finditer(r'^(\S+) measure: (.*)$', log, re.M)}
    c = j(t, 'check.json') or {}
    return {'gui_measure': meas, 'check': {k: c.get(k) for k in KEYS if k in c}, 'pattern': c.get('pattern'),
            'sheet': c.get('sheet_Params'), 'done': 'TAKE %s DONE' % t in log}


build = j('P', 'build.json') or {}
N = {'freecad': '1.1.4 (fcc-app:1.1.4-0.1.28, freecad-mcp add-on + plug 0.1.28)',
     'part': {'rack_width': 180, 'width': 20, 'margin': 20, 'hooks': 5, 'hook_mm3': 8500, 'strip': '180 x 5 x 60'},
     'cases': {k: {kk: v.get(kk) for kk in KEYS if kk in v} for k, v in build.items()},
     'g0': {'verdict': 'out/fc9/G0/VERDICT.txt', 'trap_gui_check': j('G0', 'b', 'g0-trap.check.json') and
            {k: j('G0', 'b', 'g0-trap.check.json').get(k) for k in ('solids', 'volume_mm3')},
            'toast': 'One transformed shape does not intersect the support (3 times)',
            'allow_compound_new_gui_body': True, 'direction_default_for_hook': 'Horizontal sketch axis',
            'mode_default': 'Extent'},
     'takes': {t: take(t) for t in ('A', 'B', 'C') if os.path.isdir(os.path.join(X, t))},
     'claude_runs': {}}
for d in sorted(glob.glob(os.path.join(X, 'runs', '*'))):
    r = os.path.basename(d)
    meta = j('runs', r, 'meta.json') or {}
    checks = {os.path.basename(f): {k: v for k, v in json.load(open(f, encoding='utf-8')).items()
                                    if k in KEYS + ('used', 'bodies', 'pattern')}
              for f in glob.glob(os.path.join(d, 'after-*.check.json'))}
    N['claude_runs'][r] = {'cost_usd': meta.get('cost_usd'), 'wall_s': meta.get('wall_s'),
                           'prompt': txt('runs', r, 'prompt.txt').strip(), 'guard': j('runs', r, 'costguard.json'),
                           'version': txt('runs', r, 'claude-version.txt').strip(), 'checks': checks}
json.dump(N, open(os.path.join(X, 'NUMBERS.json'), 'w', encoding='utf-8'), indent=1)
print('NUMBERS', json.dumps({t: v['gui_measure'] for t, v in N['takes'].items()}))
