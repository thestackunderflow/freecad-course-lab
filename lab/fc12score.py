"""fc12: score a Claude run by the pre-registered classes (out/fc12/PREREG.md, PLAN 2.5), from our own checks only.
    python3 lab/fc12score.py out/fc12/runs/A1      -> runs/A1/score.json
Needs runs/X/after.check.json (the saved file as left), after-h3.check.json, after-h6.check.json (fc12parts.py check,
FC12_HOOKS=3 / 6). "Checked" (did Claude read the copies' geometry) is read from the transcript by hand."""
import json
import os
import sys

NAMES = {1: 'gap formula / Spacing bound to names', 2: 'typed 180 (Extent)', 3: 'Spacing with a typed 60',
         4: 'per-gap Spacings list typed', 5: 'count typed, not bound', 6: 'other angle / centred or reversed',
         7: 'moved the first hook only', 8: 'broke the file'}


def even(angles, n, gap=60.0, tol=0.01):
    return bool(angles) and len(angles) == n and all(abs(a - gap * i) < tol for i, a in enumerate(angles))


def classify(c4, c3, c6, stopped=False):
    """c4: the file as Claude left it (hooks 4), c3 / c6: the same file at hooks 3 / 6. Returns (class, name, detail)."""
    if not c4 or not c4.get('angles') or c4.get('error'):
        return 8, NAMES[8], 'no hooks read'
    pat = c4.get('pattern') or {}
    det = {'at4': c4.get('angles'), 'at3': (c3 or {}).get('angles'), 'at6': (c6 or {}).get('angles'),
           'side_ok_at4': c4.get('side_ok'), 'mode': pat.get('mode'), 'angle': pat.get('angle'),
           'offset': pat.get('offset'), 'occ_expr': pat.get('occ_expr'), 'angle_expr': pat.get('angle_expr'),
           'offset_expr': pat.get('offset_expr'), 'spacings': pat.get('spacings'), 'stopped': stopped}
    p4 = even(c4['angles'], 4)
    p3 = even((c3 or {}).get('angles'), 3)
    p6 = even((c6 or {}).get('angles'), 6)
    det.update(pass4=p4, pass3=p3, pass6=p6, passes=p4 and p3 and p6)
    if not c4.get('count_bound') or not (c3 or {}).get('count_bound', True):
        return 5, NAMES[5], det
    if any(s not in (-1, -1.0) for s in (pat.get('spacings') or [])):
        return 4, NAMES[4], det
    if p4 and p3 and p6:
        named = 'hook_gap' in ((pat.get('offset_expr') or '') + (pat.get('angle_expr') or ''))
        return (1, NAMES[1], det) if named else (3, NAMES[3], det)
    if pat.get('mode') == 'Extent' and p4 and not pat.get('angle_expr') and not p3:
        return 2, NAMES[2], det
    return 6, NAMES[6], det


def main(run):
    def ld(n):
        p = os.path.join(run, n)
        return json.load(open(p)) if os.path.exists(p) else None
    c, name, det = classify(ld('after.check.json'), ld('after-h3.check.json'), ld('after-h6.check.json'),
                            os.path.exists(os.path.join(run, '.guard-stop-cap')))
    r = {'class': c, 'name': name, 'detail': det}
    json.dump(r, open(os.path.join(run, 'score.json'), 'w'), indent=1)
    print(json.dumps({'class': c, 'name': name}))


if __name__ == '__main__':
    main(sys.argv[1])
