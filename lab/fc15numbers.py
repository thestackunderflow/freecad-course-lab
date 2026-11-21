"""fc15: every number the lesson may show, collected from the lab's own outputs -> out/fc15/NUMBERS.json
    python lab/fc15numbers.py
Sources: out/fc15/P/build.json (G0 by code), out/fc15/G0/q3-scan.json, takes <T>/take.log + check.json,
runs/<RUN>/{meta.json, after.check.json, tools.txt, reply.txt}. Nothing is typed in by hand."""
import json
import os
import re

X = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'fc15')


def ld(*p):
    f = os.path.join(X, *p)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else None


def rim(s):
    if not s:
        return None
    r = s.get('rim') or {}
    return {'builds': s.get('builds'), 'bad': (s.get('build_info') or {}).get('bad'),
            'valid': (s.get('build_info') or {}).get('valid'), 'solids': r.get('solids'),
            'volume': r.get('volume'), 'faces': r.get('faces'), 'wall': r.get('wall'), 'flat': r.get('flat'),
            'flat_segs': r.get('flat_segs'), 'round_radii': r.get('round_radii'),
            'outside_w': r.get('outside_w'), 'inside_w': r.get('inside_w'), 'inside_l': r.get('m_inside_l'),
            'inside_d': r.get('m_inside_d'), 'peg_w': r.get('m_peg_w'), 'peg_h': r.get('m_peg_h'),
            'corner_pt_31.95': (r.get('points') or {}).get('corner_pt_31.95'),
            'unchanged_vs_start': s.get('unchanged_vs_start')}


def take_lines(t, pat):
    f = os.path.join(X, t, 'take.log')
    if not os.path.exists(f):
        return []
    return [ln.strip()[:400] for ln in open(f, encoding='utf-8', errors='replace') if re.search(pat, ln)]


def check(*p):
    c = ld(*p)
    if not c:
        return None
    out = {k: c.get(k) for k in ('pass', 'criteria', 'fillets') if k in c}
    out['order'] = (c.get('tree') or {}).get('group')
    out['tip'] = (c.get('tree') or {}).get('tip')
    out['params'] = {v[0]: v[1] for k, v in (c.get('params') or {}).items() if k.startswith('B') and v[0]}
    for k in ('stored', 'recomputed', 'at_wall2', 'at_wall3', 'at_wall1.6'):
        if k in c:
            out[k] = rim(c[k])
    return out


def run(r):
    d = os.path.join(X, 'runs', r)
    if not os.path.isdir(d):
        return None
    meta = ld('runs', r, 'meta.json') or {}
    prompt = open(os.path.join(d, 'prompt.txt'), encoding='utf-8').read().strip() if os.path.exists(
        os.path.join(d, 'prompt.txt')) else None
    calls = []
    tf = os.path.join(d, 'tools.txt')
    if os.path.exists(tf):
        for ln in open(tf, encoding='utf-8', errors='replace'):
            if ln.startswith('CALL'):
                calls.append(ln[5:].strip()[:600])
    return {'cost_usd': meta.get('cost_usd'), 'wall_s': meta.get('wall_s'), 'launch': meta.get('launch'),
            'prompt': prompt, 'n_tool_calls': len(calls), 'tool_calls': calls, 'check': check('runs', r, 'after.check.json')}


def main():
    b = ld('P', 'build.json') or {}
    n = {'source': 'freecad-course-lab out/fc15 (lab/fc15parts.py build + check, takes, runs); FreeCAD 1.1.4, '
                   'freecad-mcp 0.1.28',
         'G0': {'rim_start': rim((b.get('q1') or {}).get('snap')), 'params': (b.get('q1') or {}).get('params'),
                'outer_edges': len((b.get('q1') or {}).get('outer_edges') or []),
                'inner_edges': len((b.get('q1') or {}).get('inner_edges') or []),
                'trap_r3': rim(b.get('q2_trap_r3')), 'fix_r1_5': rim(b.get('fix_r1_5')),
                'second_edge_1': rim(b.get('second_edge_1')), 'reopen_w2': rim(b.get('q4_reopen')),
                'walls': {k: rim(v) for k, v in (b.get('q4_walls') or {}).items()},
                'q3_limits': {k: v for k, v in (b.get('q3') or {}).items() if 'largest_builds' in v},
                'q3_cases': {k: {'builds': v.get('builds'), 'flat': v.get('flat'), 'radii': v.get('radii')}
                             for k, v in (b.get('q3') or {}).items() if 'largest_builds' not in v},
                'q3_scan_refusals_below_limit': {
                    k: sorted(float(r) for r, v in s.items() if not v[0] and float(r) < 2.0)
                    for k, s in (ld('G0', 'q3-scan.json') or {}).items() if isinstance(s, dict)},
                'q5_rim_face': {k: rim(v) for k, v in (b.get('q5') or {}).items()},
                'q7_round_before_shell': rim(b.get('q7')),
                'q8_your_turns': b.get('q8'),
                'q2_all8_r1_5': b.get('q2_all8_r1_5')},
         'takes': {}, 'runs': {}}
    for t in 'RTFIPY':
        if os.path.isdir(os.path.join(X, t)):
            n['takes'][t] = {
                'done': bool(take_lines(t, r'^TAKE . DONE')),
                'measure': take_lines(t, r' measure: '),
                'state': take_lines(t, r'^(after OK|after Cancel|reopened|wall \d|rim_out|rim_in|.* \d(\.\d+)?: \{)'),
                'boxes': take_lines(t, r'ui after OK|NO ERROR|ERROR BOX|BAIL|SELECTION FIXED'),
                'tooltip': take_lines(t, r'^tooltip'),
                'check': check(t, 'check.json')}
    for r in ('A1', 'B1'):
        v = run(r)
        if v:
            n['runs'][r] = v
    json.dump(n, open(os.path.join(X, 'NUMBERS.json'), 'w', encoding='utf-8'), indent=1)
    print('NUMBERS.json: takes %s, runs %s' % (sorted(n['takes']), sorted(n['runs'])))


if __name__ == '__main__':
    main()
