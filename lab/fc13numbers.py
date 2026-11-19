"""fc13: every number the lesson may show, collected from the lab's own outputs -> out/fc13/NUMBERS.json
    python lab/fc13numbers.py"""
import glob
import json
import os
import re

X = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc13')
KEYS = ('inside_w', 'inside_l', 'inside_d', 'wall_x', 'wall_y', 'floor', 'outside_w', 'outside_l', 'outside_h', 'floor_z',
        'rim_z', 'solids', 'valid', 'hollow', 'volume', 'edge_radii', 'n_cyl_faces', 'n_sphere_faces')


def ld(*p):
    f = os.path.join(X, *p)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else None


def slim(r):
    if not r:
        return None
    t = r.get('thickness') or {}
    out = {k: r.get(k) for k in KEYS}
    out.update(reversed=t.get('reversed'), value=t.get('value'), value_expr=t.get('value_expr'), join=t.get('join'))
    if r.get('hook'):
        out['hook'] = r['hook']
    if r.get('error'):
        out['error'] = r['error']
    return out


def chk(c):
    return None if not c else {k: slim(c.get(k)) for k in ('stored', 'recomputed', 'at_wall3', 'at_width70')} | {
        'width_target': c.get('width_target'), 'wall_alias': c.get('wall_alias')}


def take_lines(t):
    f = os.path.join(X, t, 'take.log')
    if not os.path.exists(f):
        return {}
    s = open(f, encoding='utf-8', errors='replace').read()
    out = {'measures': re.findall(r'(\S+) measure: .*?Result:" field:([0-9.]+ ?mm)', s)}
    for k in ('tooltip', 'messages', 'box at open', 'box before OK', 'notices at open'):
        m = re.search(re.escape(k) + r': (.*)', s)
        if m:
            out[k] = m.group(1)[:300]
    return out


def main():
    b = ld('P', 'build.json') or {}
    n = {'source': 'freecad-course-lab out/fc13 (lab/fc13parts.py, G0, takes, runs); FreeCAD 1.1.4 + freecad-mcp 0.1.28',
         'build': {k: (slim(v) if isinstance(v, dict) else v) for k, v in b.items()}, 'g0': {}, 'takes': {}, 'runs': {}}
    for f in sorted(glob.glob(os.path.join(X, 'G0', '*.check.json'))):
        n['g0'][os.path.basename(f)[:-11]] = chk(json.load(open(f)))
    for t in ('R', 'T', 'M', 'F', 'P', 'Y', 'K'):
        if ld(t, 'record.json'):
            n['takes'][t] = dict(take_lines(t), end=chk(ld(t, 'check.json')))
    for d in sorted(glob.glob(os.path.join(X, 'runs', '*'))):
        if not os.path.isdir(d):
            continue
        r = os.path.basename(d)
        meta = ld('runs', r, 'meta.json') or {}
        n['runs'][r] = {'cost_usd': meta.get('cost_usd'), 'wall_s': meta.get('wall_s'), 'score': ld('runs', r, 'score.json'),
                        'check': chk(ld('runs', r, 'after.check.json'))}
    json.dump(n, open(os.path.join(X, 'NUMBERS.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('NUMBERS.json', len(n['build']), 'build cases,', len(n['g0']), 'g0,', len(n['takes']), 'takes,', len(n['runs']), 'runs')


if __name__ == '__main__':
    main()
