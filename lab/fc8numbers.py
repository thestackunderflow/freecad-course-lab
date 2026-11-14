"""fc8: every number of the lab into out/fc8/NUMBERS.json, read only from files code wrote (build.json, the takes'
check.json / take.log / shape-content.txt, G0 files, the Claude runs' check.json / meta.json / costguard.json).
    python3 lab/fc8numbers.py [/lab/out/fc8]"""
import glob
import json
import os
import re
import sys

X = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc8')


def j(*p):
    f = os.path.join(X, *p)
    return json.load(open(f)) if os.path.exists(f) else None


def txt(*p):
    f = os.path.join(X, *p)
    return open(f, encoding='utf-8', errors='replace').read() if os.path.exists(f) else ''


def drags(log):
    out = []
    for m in re.finditer(r'^(.*?): hook z (-?[0-9.]+) (\{.*\})', log, re.M):
        out.append({'step': m.group(1), 'hook_z_mm': float(m.group(2)), **json.loads(m.group(3))})
    return out


def shape_volume(t):
    m = re.search(r'Volume:\s+([0-9.]+)', t)
    s = re.search(r'\\nSolids:\s+([0-9]+)', t)
    return {'volume_mm3': float(m.group(1)) if m else None, 'solids': int(s.group(1)) if s else None}


build = j('P', 'build.json')
N = {'freecad': '1.1.4 (fcc-app:1.1.4-0.1.28, freecad-mcp add-on + plug 0.1.28)',
     'cases': {c: {k: v.get(k) for k in ('gap', 'slot_head', 'hook_mm3', 'rail_mm3', 'common_mm3', 'common_solids',
                                          'head_side_mm', 'min_distance_mm')} for c, v in build.items()},
     'g0': {'asm_headless': j('P', 'asm.json'), 'gui': j('G0', 'b', 'g0b-gui.json'),
            'after_drag_check': {k: (j('G0', 'b', 'check-after-drag.json') or {}).get(k) for k in ('common_mm3', 'used')}},
     'takes': {}}
for t in 'ABCDE':
    log = txt(t, 'take.log')
    c = j(t, 'check.json') or {}
    r = {'end_check': {k: c.get(k) for k in ('common_mm3', 'head_side_mm', 'bodies', 'used', 'sheet_Params')},
         'recorded': os.path.exists(os.path.join(X, t, 'screen.mp4'))}
    rec = j(t, 'record.json')
    if rec:
        r['record'] = {k: rec.get(k) for k in ('duration_s', 'frames', 'width', 'height', 'fps') if k in rec}
    if t in 'AC':
        r['check_geometry_shape_content'] = shape_volume(txt(t, 'shape-content.txt'))
    if t in 'BE':
        r['slider_hook_z_mm'] = float(re.search(r'hook z after slider (-?[0-9.]+)', log).group(1)) if 'after slider' in log else None
        r['drags'] = drags(log)
    if t == 'D':
        r['measure_gui'] = dict(re.findall(r'^(left|right) measure: combo:\S+ field:([0-9.]+ mm)', log, re.M))
    N['takes'][t] = r
N['claude_runs'] = {}
for d in sorted(glob.glob(os.path.join(X, 'runs', '*'))):
    run = os.path.basename(d)
    meta = j('runs', run, 'meta.json') or {}
    guard = j('runs', run, 'costguard.json')
    checks = {}
    for f in glob.glob(os.path.join(d, 'after-*.check.json')):
        c = json.load(open(f))
        checks[os.path.basename(f)] = {k: c.get(k) for k in ('used', 'bodies', 'common_mm3', 'head_side_mm', 'joints',
                                                              'sheet_Params')}
    tools = txt('runs', run, 'tools.txt')
    N['claude_runs'][run] = {'cost_usd': meta.get('cost_usd'), 'wall_s': meta.get('wall_s'), 'guard': guard,
                             'tool_calls': tools.count('\nCALL ') + tools.startswith('CALL '),
                             'after': checks}
json.dump(N, open(os.path.join(X, 'NUMBERS.json'), 'w'), indent=1)
print('NUMBERS.json', len(json.dumps(N)), 'bytes')
