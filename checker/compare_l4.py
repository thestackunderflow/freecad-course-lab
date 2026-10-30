"""Lesson 4: the side-by-side table (by hand / with the sentence: B1, B2 / without: A1) from the lab's own files,
for the comparison card and the README. Every cell is read from a score.json or the by-hand checks.
    python3 -m checker.compare_l4        (writes out/l4/compare.json)"""
import json
import os

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
O = os.path.join(LAB, 'out', 'l4')


def load(*p):
    f = os.path.join(O, *p)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else None


def sides(c):
    s = (c or {}).get('hole_sides_mm') or []
    return ' · '.join('%g' % x for x in s[0]) if s else '—'


def cell_runs(runs, fn):
    vals = [fn(r) for r in runs if r]
    if not vals:
        return {'text': '—'}
    texts = [v[0] for v in vals]
    oks = [v[1] for v in vals]
    return {'text': ' / '.join(texts) if len(set(texts)) > 1 else texts[0],
            'ok': all(oks) if all(o is not None for o in oks) else None}


def main():
    hand = {k: load('hand', 'check-%s.json' % k) for k in ('fillet', 'width30')}
    b = [load('runs', r, 'score.json') for r in ('B1', 'B2')]
    a = [load('runs', 'A1', 'score.json')]
    rows = []

    def row(label, hand_cell, fn):
        rows.append({'label': label, 'cells': [hand_cell, cell_runs(b, fn), cell_runs(a, fn)]})
    h1, h2 = hand['fillet'] or {}, hand['width30'] or {}
    row('hole names', {'text': '2 names', 'ok': True},
        lambda s: (('%d names' % len(s['names']['hole_names'])) if s['names']['hole_names'] else 'none', bool(s['names']['hole_names'])))
    row('first build', {'text': '%.2f' % h1.get('volume_mm3', 0), 'ok': h1.get('ok')},
        lambda s: ('%.2f' % s['first_build'].get('volume_mm3', 0) if 'volume_mm3' in s['first_build'] else 'no solid',
                   s['first_build_right']))
    row('30 wide: holes', {'text': sides(h2), 'ok': h2.get('centred')},
        lambda s: (sides(s.get('after_edit')), s.get('centred_after_edit')))
    row('30 wide: fillet', {'text': 'kept' if h2.get('fillet_on_lip_edge') else 'lost', 'ok': h2.get('fillet_on_lip_edge')},
        lambda s: ('kept' if s.get('fillet_after_edit') else 'lost', s.get('fillet_after_edit')))
    row('the change', {'text': 'one cell', 'ok': True},
        lambda s: ('one cell' if s.get('edit_by_one_cell') else 'cell + a rule', s.get('edit_by_one_cell')))
    rep = load('replay-B1', 'score.json')
    out = {'rows': rows, 'runs': {'B1': b[0], 'B2': b[1], 'A1': a[0]}, 'replay_B1': rep,
           'replay': None}
    if rep:
        fb = rep.get('first_build') or {}
        ae = rep.get('after_edit') or {}
        out['replay'] = 'no-AI replay of the first run: %.2f, then 30 wide: %s' % (fb.get('volume_mm3', 0), sides(ae))
    json.dump(out, open(os.path.join(O, 'compare.json'), 'w', encoding='utf-8'), indent=1)
    for r in rows:
        print(r['label'], '|', ' | '.join(c['text'] for c in r['cells']))
    print(out['replay'])


if __name__ == '__main__':
    main()
