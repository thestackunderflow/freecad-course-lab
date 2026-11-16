"""fc10: every number of the lab into out/fc10/NUMBERS.json, read only from files code wrote (P/build.json, G0
g0-log.txt / *.check.json, the takes' check.json / take.log, the Claude runs' check.json / meta.json / costguard.json).
    python3 lab/fc10numbers.py [/lab/out/fc10]"""
import glob
import json
import os
import re
import sys

X = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc10')
KEYS = ('dof', 'constraints', 'by_type', 'origin_tied', 'zmin', 'zmax', 'xmin', 'hole_to_top', 'sketch_hole_to_top',
        'hole_in_plate', 'hole_faces', 'volume_mm3', 'solids', 'sheet', 'used', 'redundant', 'conflicting')


def j(*p):
    f = os.path.join(X, *p)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else None


def txt(*p):
    f = os.path.join(X, *p)
    return open(f, encoding='utf-8', errors='replace').read() if os.path.exists(f) else ''


def pick(c):
    return {k: c.get(k) for k in KEYS if c and k in c}


def take(t):
    log = txt(t, 'take.log')
    meas = {}
    for m in re.finditer(r'^(top|bottom) measure: (.*?)\nY: (.*?)\nZ: (.*?)$', log, re.M):
        meas[m.group(1)] = {'x': m.group(2).replace('X: ', ''), 'y': m.group(3), 'z': m.group(4)}
    px = {m.group(1): m.group(2) for m in re.finditer(r'^(front px|right px): (.*)$', log, re.M)}
    live = {m.group(1): json.loads(m.group(2)) for m in re.finditer(r'^(start|after \d+|after close): (\{.*\})$', log, re.M)}
    sol = re.findall(r'^solver: (.*)$', log, re.M)
    sel = re.findall(r'^(?:selection|selection after link): (.*)$', log, re.M)
    return {'gui_measure': meas, 'live': live, 'px': px, 'solver_text': sol, 'selection': sel,
            'check': pick(j(t, 'check.json')), 'done': 'TAKE %s DONE' % t in log}


def g0():
    log = txt('G0', 'g0-log.txt')
    # 11 distinct unpinned 60 -> 80 tries, each counted once: the two G0 GUI runs (by their headless re-read of the GUI
    # file; the "GUI after" line is the same try), take A (filmed GUI), the build's unpinned_80 (P/build.json) and the
    # seven headless G0 tries ("q2 headless 60->80" + "q2 headless repeat 1..6"; the 100 repeats are not 80 tries)
    tries = []

    def add(name, d):
        if d and d.get('dof') == 2 and abs(d.get('zmax', 0) - d.get('zmin', 0) - 80) < 1e-3:
            tries.append({'try': name, 'zmin': d['zmin'], 'zmax': d['zmax'], 'hole_to_top': d['hole_to_top']})
    for m in re.finditer(r'^(q2-unpinned-run\d) headless check of the GUI file: FC10 check (\{.*\})$', log, re.M):
        add('G0 GUI ' + m.group(1)[3:], json.loads(m.group(2)))
    add('take A (GUI, filmed)', (j('A', 'check.json') or {}))
    add('build unpinned_80 (headless)', (j('P', 'build.json') or {}).get('unpinned_80'))
    for m in re.finditer(r'^q2 headless (60->80 of the start file|repeat \d): FC10 check (\{.*\})$', log, re.M):
        add('G0 headless ' + m.group(1).replace(' of the start file', ''), json.loads(m.group(2)))
    h100 = [json.loads(m.group(1)) for m in re.finditer(r'^q2 headless 100 repeat \d: FC10 check (\{.*\})$', log, re.M)]
    return {'verdict': 'out/fc10/G0/VERDICT.txt', 'unpinned_80_tries': tries,
            'unpinned_100_headless': [{'zmin': d['zmin'], 'zmax': d['zmax'], 'hole_to_top': d['hole_to_top'],
                                       'volume_mm3': d['volume_mm3']} for d in h100],
            'pinned_80_gui': pick(j('G0', 'q2-pinned.check.json')),
            'message_unpinned': 'Under-constrained: 2 Degrees of Freedom', 'message_pinned': 'Fully constrained',
            'link_selects': 'Vertex1..Vertex16 (every corner)',
            'pin_route': 'box around the corner (Vertex1, Vertex16, RootPoint) -> Coincident Constraint (one constraint)',
            'ctrl_click_same_spot': 'deselects the corner', 'coincident_menu_text': 'Coincident Constraint',
            'coincident_shortcut': 'C', 'lock_menu_text': 'Lock Position'}


build = j('P', 'build.json') or {}
N = {'freecad': '1.1.4 (fcc-app:1.1.4-0.1.28, freecad-mcp add-on + plug 0.1.28)',
     'part': {'plate_height': 60, 'thickness': 5, 'hook_depth': 25, 'lip_height': 10, 'width': 20,
              'hole_mm': 4.5, 'hole_mm3': 79.5216, 'hook_mm3_no_hole_60': 8500},
     'cases': {k: (pick(v) if k != 'yourturn' else v) for k, v in build.items()},
     'g0': g0(),
     'takes': {t: take(t) for t in ('A', 'B', 'P', 'C', 'D', 'T', 'TB') if os.path.isdir(os.path.join(X, t))},
     'controls': {os.path.basename(f)[:-5]: pick(json.load(open(f, encoding='utf-8')))
                  for f in sorted(glob.glob(os.path.join(X, 'controls', '*.json')))},
     'controls_refilm': j('controls-refilm.json'),
     'claude_runs': {}}
for d in sorted(glob.glob(os.path.join(X, 'runs', '*'))):
    r = os.path.basename(d)
    meta = j('runs', r, 'meta.json') or {}
    checks = {os.path.basename(f): pick(json.load(open(f, encoding='utf-8')))
              for f in glob.glob(os.path.join(d, 'after-*.check.json'))}
    N['claude_runs'][r] = {'cost_usd': meta.get('cost_usd'), 'wall_s': meta.get('wall_s'),
                           'prompt': txt('runs', r, 'prompt.txt').strip(), 'guard': j('runs', r, 'costguard.json'),
                           'version': txt('runs', r, 'claude-version.txt').strip(), 'checks': checks,
                           'score': j('runs', r, 'score.json')}
json.dump(N, open(os.path.join(X, 'NUMBERS.json'), 'w', encoding='utf-8'), indent=1)
print('NUMBERS', json.dumps({t: (v['check'].get('zmin'), v['check'].get('zmax'), v['check'].get('hole_to_top'))
                             for t, v in N['takes'].items()}))
