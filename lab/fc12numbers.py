"""fc12: every number the lesson may show, collected from the lab's own outputs -> out/fc12/NUMBERS.json
    python lab/fc12numbers.py"""
import glob
import json
import os
import re

X = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc12')


def ld(*p):
    f = os.path.join(X, *p)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else None


def slim(r):
    if not r:
        return None
    pat = r.get('pattern') or {}
    return {k: r.get(k) for k in ('angles', 'gaps', 'hooks_seen', 'lip_faces', 'solids', 'count_bound', 'side_ok',
                                  'into_wall', 'clearance_mm', 'volume')} | {
        'mode': pat.get('mode'), 'angle': pat.get('angle'), 'offset': pat.get('offset'),
        'occurrences': pat.get('occurrences'), 'expr': pat.get('expr')}


def take_lines(t):
    f = os.path.join(X, t, 'take.log')
    if not os.path.exists(f):
        return {}
    s = open(f, encoding='utf-8', errors='replace').read()
    out = {'measures': re.findall(r'measure: .*?Result:" field:([0-9.]+)', s)}
    m = re.search(r'tooltip: (.*)', s)
    if m:
        out['tooltip'] = m.group(1)
    m = re.search(r'messages: (.*)', s)
    if m:
        out['messages'] = m.group(1)
    return out


def main():
    b = ld('P', 'build.json') or {}
    n = {'source': 'freecad-course-lab out/fc12 (lab/fc12parts.py, G0, takes, runs); FreeCAD 1.1.4 + freecad-mcp 0.1.28',
         'build': {k: slim(v) for k, v in b.items()}, 'g0': {}, 'takes': {}, 'runs': {}}
    for f in sorted(glob.glob(os.path.join(X, 'G0', '*.check.json'))):
        n['g0'][os.path.basename(f)[:-11]] = slim(json.load(open(f)))
    for t in ('R', 'O', 'T', 'M', 'F', 'P', 'Y', 'K'):
        rec = ld(t, 'record.json')
        if rec:
            n['takes'][t] = dict(take_lines(t), end=slim(ld(t, 'check.json')))
    for d in sorted(glob.glob(os.path.join(X, 'runs', '*'))):
        r = os.path.basename(d)
        meta = ld('runs', r, 'meta.json') or {}
        n['runs'][r] = {'cost_usd': meta.get('cost_usd'), 'wall_s': meta.get('wall_s'),
                        'score': ld('runs', r, 'score.json'),
                        'after': slim(ld('runs', r, 'after.check.json')),
                        'at3': slim(ld('runs', r, 'after-h3.check.json')),
                        'at6': slim(ld('runs', r, 'after-h6.check.json'))}
    json.dump(n, open(os.path.join(X, 'NUMBERS.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('NUMBERS.json', len(n['build']), 'build cases,', len(n['g0']), 'g0,', len(n['takes']), 'takes,', len(n['runs']), 'runs')


if __name__ == '__main__':
    main()
