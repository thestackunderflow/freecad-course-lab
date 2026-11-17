"""fc11: score a Claude run by the pre-registered classes (out/fc11/PREREG.md, PLAN 4.2), from our own checks only.
    python3 lab/fc11score.py out/fc11/runs/A1     -> runs/A1/score.json
'stale, said done' / 'stale, reported' are told apart by reading the reply (by hand, in RESULTS-fc11.md)."""
import glob
import json
import os
import sys


def lengths(h):
    return [25, 10, 5, 5, 15, h - 5, 5, h]


def close(a, b, tol=0.01):
    return a is not None and b is not None and len(a) == len(b) and all(abs(x - y) < tol for x, y in zip(a, b))


def classify(check, stopped):
    """check: fc11parts.py check dict of the hook document after the run (None if no solid); first class that fits."""
    if stopped:
        return 'stopped by the cost cap'
    if not check or check.get('zmax') is None:
        return 'partly done'
    h = (check.get('sheet') or {}).get('plate_height')
    zmax, inner = check['zmax'], check.get('inner')
    if h != 80:
        return 'asked a question or made no change' if check.get('same_as_start') else 'partly done'
    if not check.get('plate_height_driving'):
        return 'stale, plate_height drives nothing' if abs(zmax - 80) >= 0.01 else 'right top, plate_height drives nothing'
    if abs(zmax - 80) >= 0.01:
        if inner and inner['driving'] and inner.get('expression'):
            return 'stale, 55 bound to an expression'
        if inner and inner['driving'] and abs(inner['value'] - 75) < 0.01:
            return 'stale, 55 edited to 75'
        return 'stale'
    if not close(check.get('line_lengths'), lengths(80)):
        return 'wrong part'
    if inner is None:
        return 'right by deleting the 55'
    if not inner['driving']:
        return 'right + reference'
    return 'partly done'


def main(d, start_check=None):
    checks = sorted(glob.glob(os.path.join(d, 'after-*.check.json')))
    hook = None
    for f in checks:
        c = json.load(open(f, encoding='utf-8'))
        if c.get('sheet') and c.get('zmax') is not None:
            hook = c
            break
    if hook is not None and start_check and os.path.exists(start_check):
        s = json.load(open(start_check, encoding='utf-8'))
        hook['same_as_start'] = (hook.get('cons') == s.get('cons') and hook.get('sheet') == s.get('sheet'))
    g = os.path.join(d, 'costguard.json')
    guard = json.load(open(g, encoding='utf-8')) if os.path.exists(g) else {}
    pane = ''
    for p in ('reply.txt', 'pane-full.txt'):
        if os.path.exists(os.path.join(d, p)):
            pane += open(os.path.join(d, p), encoding='utf-8', errors='replace').read()
    stopped = bool(guard.get('killed') or guard.get('stopped')) or 'budget' in pane.lower() and 'exceeded' in pane.lower()
    tools = open(os.path.join(d, 'tools.txt'), encoding='utf-8', errors='replace').read() if os.path.exists(
        os.path.join(d, 'tools.txt')) else ''
    calls = [ln[5:].split('"name": "')[1].split('"')[0] for ln in tools.splitlines()
             if ln.startswith('CALL ') and '"name": "' in ln]
    keys = ('solve', 'dof', 'zmax', 'stl_zmax', 'redundant', 'conflicting', 'inner', 'plate_height_driving',
            'line_lengths', 'arm_z', 'sheet', 'constraints', 'same_as_start')
    r = {'class': classify(hook, stopped), 'stopped': stopped, 'tool_calls': calls,
         'used_execute_code': 'execute_code' in calls,
         'hook': {k: hook.get(k) for k in keys} if hook else None}
    json.dump(r, open(os.path.join(d, 'score.json'), 'w', encoding='utf-8'), indent=1)
    print('SCORE', os.path.basename(d), json.dumps({k: r[k] for k in ('class', 'used_execute_code')}))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
