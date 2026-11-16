"""fc10: score a Claude run by the pre-registered classes (out/fc10/PREREG.md), from our own checks only.
    python3 lab/fc10score.py out/fc10/runs/A1     -> runs/A1/score.json"""
import glob
import json
import os
import sys


def classify(check, stopped):
    """check: fc10parts.py check dict of the hook document after the run (None if no solid); stopped: the cost cap
    (guard or --max-budget-usd) ended the run."""
    if stopped:
        return 'stopped by the cost cap'
    if not check or check.get('zmin') is None:
        return 'partly done'
    h = (check.get('sheet') or {}).get('plate_height')
    zmin, zmax, top = check['zmin'], check['zmax'], check.get('hole_to_top')
    if h == 80 and abs(zmin) < 0.01 and abs(zmax - 80) < 0.01 and top is not None and abs(top - 15) < 0.01:
        return 'right + pinned' if check.get('dof') == 0 else 'right but still unpinned'
    if abs(zmin) >= 1 or (top is not None and abs(zmax - zmin - 80) < 0.01 and abs(top - 15) >= 1):
        return 'moved'
    return 'partly done'


def main(d):
    checks = sorted(glob.glob(os.path.join(d, 'after-*.check.json')))
    hook = None
    for f in checks:
        c = json.load(open(f, encoding='utf-8'))
        if c.get('sheet') and c.get('zmin') is not None:
            hook = c
            break
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
    r = {'class': classify(hook, stopped), 'stopped': stopped, 'tool_calls': calls,
         'used_execute_code': 'execute_code' in calls,
         'hook': {k: hook.get(k) for k in ('dof', 'zmin', 'zmax', 'hole_to_top', 'constraints', 'by_type',
                                           'origin_tied', 'sheet', 'volume_mm3')} if hook else None,
         'rules_added': (hook.get('constraints') - 22) if hook and hook.get('constraints') is not None else None}
    json.dump(r, open(os.path.join(d, 'score.json'), 'w', encoding='utf-8'), indent=1)
    print('SCORE', os.path.basename(d), json.dumps({k: r[k] for k in ('class', 'rules_added', 'used_execute_code')}))


if __name__ == '__main__':
    main(sys.argv[1])
