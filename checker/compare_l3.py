"""Lesson 3's summary across the by-hand take, the plain take, the Claude runs and the no-AI replays (all from the
lab's own measure.json / score.json files): out/l3/compare.json.
    python3 -m checker.compare_l3 [OUT_L3_DIR]"""
import json
import os
import sys


def part(p):
    m = json.load(open(p, encoding='utf-8'))
    s = [r for r in m['solids'] if not r.get('in_list')] or m['solids']
    s = s[-1]
    return {'volume_mm3': s['volume_mm3'], 'bbox_mm': s['bbox_mm'], 'z_range_mm': s['z_range_mm'],
            'fully_constrained': [k.get('fully_constrained') for k in m.get('sketches') or []]}


def build(L):
    out = {'hand': {k: part(os.path.join(L, 'hand', 'measure-%s.json' % k)) for k in ('named', 'depth40', 'thick8', 'back5')},
           'plain_25_to_40': part(os.path.join(L, 'plain', 'measure-plain40.json')), 'runs': {}, 'replays': {}}
    for r in sorted(os.listdir(os.path.join(L, 'runs'))):
        d = os.path.join(L, 'runs', r)
        if not os.path.exists(os.path.join(d, 'score.json')):
            continue
        meta = json.load(open(os.path.join(d, 'meta.json'), encoding='utf-8'))
        out['runs'][r] = {'cost_usd': float(meta['cost_usd'] or 0), 'score': json.load(open(os.path.join(d, 'score.json'))),
                          'parts': {k: part(os.path.join(d, 'measure-%s.json' % k)) for k in ('first', 'after2', 'after3')}}
    for f in sorted(os.listdir(L)):
        if f.startswith('replay-') and os.path.exists(os.path.join(L, f, 'score.json')):
            out['replays'][f[7:]] = json.load(open(os.path.join(L, f, 'score.json'), encoding='utf-8'))
    return out


if __name__ == '__main__':
    L = sys.argv[1] if len(sys.argv) > 1 else 'out/l3'
    res = build(L)
    json.dump(res, open(os.path.join(L, 'compare.json'), 'w', encoding='utf-8'), indent=1)
    for r, v in res['runs'].items():
        p = v['parts']
        print(r, v['cost_usd'], p['first']['volume_mm3'], p['after2']['volume_mm3'], p['after3']['volume_mm3'],
              v['score']['names']['used'], v['score']['edit2_by_one_cell'], v['score'].get('edit3_by_one_cell'))
