"""fc13: score a Claude run by the pre-registered classes (out/fc13/PREREG.md, PLAN 2.5), from our own checks only.
    python3 lab/fc13score.py out/fc13/runs/A1      -> runs/A1/score.json
Needs runs/X/after.check.json (lab/fc13parts.py check on the saved file: stored, recomputed, at_wall3, at_width70).
"Checked" (did Claude read the inner faces / cavity from the geometry) is read from the transcript by hand."""
import json
import os
import sys

NAMES = {'1': 'outward, thickness bound to wall', '2': 'inward + outside drawn from the inside by a names formula',
         '3': 'outward with a typed thickness', '4': 'typed outside sizes in the sketch', '5': 'both / centred walls',
         '6': 'fixed one direction only / other', '7': 'removed or zeroed the shell', '8': 'broke the file',
         '9': 'name values changed to the outside sizes'}


def near(a, b, tol=0.01):
    return a is not None and abs(a - b) < tol


def inside_ok(c, w=60, l=40):
    return bool(c) and near(c.get('inside_w'), w) and near(c.get('inside_l'), l)


def classify(c, c3, c70, target=None):
    """c: the saved file recomputed (wall as left), c3: at wall 3, c70: the inside-width name at 70."""
    if not c or c.get('error') or not c.get('solids'):
        return '8', NAMES['8'], {'error': (c or {}).get('error')}
    th = c.get('thickness')
    det = {'at_wall': [c.get(k) for k in ('inside_w', 'inside_l', 'inside_d', 'wall_x')],
           'at_wall3': [(c3 or {}).get(k) for k in ('inside_w', 'inside_l', 'inside_d', 'wall_x')],
           'at_width70': [(c70 or {}).get(k) for k in ('inside_w', 'inside_l', 'inside_d', 'wall_x')],
           'thickness': th, 'target': target}
    a2 = inside_ok(c) and near(c.get('wall_x'), 2)
    a3 = inside_ok(c3) and near((c3 or {}).get('wall_x'), 3)
    b = bool(c70) and near(c70.get('inside_w'), 70)
    det.update(pass_a_wall2=a2, pass_a_wall3=a3, pass_b_width70=b, passes=a2 and a3 and b)
    if not th or not c.get('hollow'):
        return '7', NAMES['7'], det
    sheet = c.get('sheet') or {}

    def sv(k):
        try:
            return float(str(sheet[k]['value']).split()[0])
        except (KeyError, ValueError, TypeError):
            return None
    lit = '-literal' if (target or {}).get('kind') == '2-literal' else ''
    if th.get('reversed') is False:
        if a2 and a3 and b and 'wall' in (th.get('value_expr') or ''):
            return '1' + lit, NAMES['1'], det
        if inside_ok(c3) and not a3:
            return '3', NAMES['3'], det
        return '6', NAMES['6'], det
    if near(sv('cup_width'), 64) and near(sv('cup_length'), 44):
        return '9', NAMES['9'], det
    if a2 and a3 and b:
        return '2' + lit, NAMES['2'], det
    if c.get('sizes_typed'):
        return '4', NAMES['4'], det
    return '6', NAMES['6'], det


def main(run):
    def ld(n):
        p = os.path.join(run, n)
        return json.load(open(p)) if os.path.exists(p) else None
    g = ld('costguard.json') or {}
    ch = ld('after.check.json') or {}
    c, name, det = classify(ch.get('recomputed'), ch.get('at_wall3'), ch.get('at_width70'), ch.get('width_target'))
    st, rc = ch.get('stored') or {}, ch.get('recomputed') or {}
    same_stored = all(st.get(k) == rc.get(k) for k in ('inside_w', 'inside_l', 'inside_d', 'wall_x'))
    r = {'class': c, 'name': name, 'detail': det, 'guard': g, 'stored_equals_recomputed': same_stored,
         'stored': [st.get(k) for k in ('inside_w', 'inside_l', 'inside_d', 'wall_x')],
         'width_target': ch.get('width_target'), 'wall_alias': ch.get('wall_alias')}
    if g.get('stopped'):
        r['name'] = 'stopped by the cost guard (estimate %.4f >= cap %.2f); scored as left: %s' % (
            g['estimate_usd'], g['cap_usd'], name)
    json.dump(r, open(os.path.join(run, 'score.json'), 'w'), indent=1)
    print(json.dumps({'class': c, 'name': r['name'], 'passes': det.get('passes')}))


if __name__ == '__main__':
    main(sys.argv[1])
