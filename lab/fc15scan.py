"""fc15 G0 Q3 full scans (freecadcmd): every 0.05 step, not just the first failure: rim_in alone, equal pairs, 1.5 + x, x + 1"""
import json, os
os.environ['FC15_MODE'] = 'lib'
exec(open('/lab/lab/fc15parts.py').read())
out = {}
st = lambda r: (r['builds'], r['rim'].get('flat'), {k: v[1] for k, v in r['state'].items() if 'Invalid' in v[0]})
for name, fn, vals in (('in_alone', lambda v: try_out(None, v), [i / 20 for i in range(1, 41)]),
                       ('out_alone', lambda v: try_out(v, None), [i / 20 for i in range(1, 41)]),
                       ('equal', lambda v: try_out(v, v), [i / 20 for i in range(1, 21)]),
                       ('out1.5_plus', lambda v: try_out(1.5, v), [i / 20 for i in range(1, 11)]),
                       ('in1_plus_out', lambda v: try_out(v, 1.0), [i / 20 for i in range(1, 21)])):
    out[name] = {str(round(v, 2)): st(fn(round(v, 2))) for v in vals}
    log15(name, ' '.join('%s:%s' % (k, 'B' if v[0] else 'x') for k, v in out[name].items()))
json.dump(out, open('/lab/out/fc15/G0/q3-scan.json', 'w'), indent=1)
