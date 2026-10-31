"""Lesson 6: every run's score, our filmed Measure, the replay, and Claude's own check coded by hand from its last reply
(verbatim, PLAN-L6 §3 rule: per line "said, with a number" / "said, no number" / "not checked"; against our script all
lines measured OK in every run, so "said OK, measured OK" wherever it said a line). Writes out/l6/compare.json.
    python3 -m lab.compare6"""
import json
import os

L6 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'l6')
LINES = ['M1 one solid, no errors', 'M2 plate 60 x 30', 'M3 walls 5', 'M4 lip 10', 'M5 holes 4 mm, centred, 15/45',
         'M6 2 mm lip edge', 'M7 names drive it']
N, S, X = 'said, with a number', 'said, no number', 'not checked'
# coded from runs/*/score.json replies (the last reply of each run), quotes kept short
CODED = {
    'B1': {'change': 'hook_depth 40 -> 55 in the sheet (one cell)', 'said': [N, N, N, N, N, N, S],
           'quote': 'I set hook_depth in the spreadsheet from 40 mm to 55 mm ... Opening 45.0 mm'},
    'B2': {'change': 'hook_depth 40 -> 55 in the sheet (one cell)', 'said': [N, N, N, N, N, N, S],
           'quote': 'I changed one spreadsheet value: hook_depth went from 40 to 55 mm'},
    'B3': {'change': "a new name 'opening' = 45 mm; hook_depth = 2 * thickness + opening (55)", 'said': [N, N, N, N, N, N, S],
           'quote': 'the opening is now its own parameter, opening'},
    'A1': {'change': 'hook_depth 40 -> 55 in the sheet (one cell)', 'said': [N, N, N, N, N, S, X],
           'quote': 'The two 4 mm mounting holes are still in place and still centered ... the lip fillet kept their references'},
}
NOTES = {
    'A1': 'measured the opening, the box (55 x 30 x 60) and the volume; said "the 5 mm thickness, 10 mm lip height, 60 mm '
          'plate height and 30 mm width are unchanged" (the sheet values, coded "with a number"); the 4 mm holes "still '
          'in place and still centered" (heights 15/45 not mentioned); the fillet "kept its references" (no radius); '
          'nothing about the names still driving the sizes; offered to add an opening name.',
}


def main():
    out = {'hand': {}, 'runs': {}}
    for s in ('depth40', 'depth45', 'depth55'):
        sc = json.load(open(os.path.join(L6, 'hand', f'score-{s}.json')))
        out['hand'][s] = {'pass': sc['pass'], 'opening_mm': sc['opening_mm'], 'volume_mm3': sc['volume_mm3'],
                          'failed': [k for k, v in sc['lines'].items() if not v]}
    for r in ('B1', 'B2', 'B3', 'A1'):
        d = os.path.join(L6, 'runs', r)
        sc = json.load(open(os.path.join(d, 'score.json'), encoding='utf-8'))
        meta = json.load(open(os.path.join(d, 'meta.json')))
        rep = os.path.join(L6, f'replay-{r}', 'compare.json')
        ours = open(os.path.join(d, 'our-measure.txt')).read().strip()
        insp = os.path.join(L6, f'inspect-{r}', 'our-measure.txt')
        out['runs'][r] = {
            'pass': sc['pass'], 'lines': sc['lines'], 'hook_depth': sc['hook_depth'], 'opening_mm': sc['opening_mm'],
            'volume_mm3': sc['volume_mm3'], 'new_aliases': sc['new_aliases'], 'cost_usd': float(meta['cost_usd']),
            'wall_s': meta['wall_s'], 'calls': [c['tool'] for c in sc['calls']],
            'trigger_sent': os.path.exists(os.path.join(d, 'trigger.json')),
            'our_filmed_measure': ours,
            'our_filmed_measure_note': ('our pick landed on the fillet edge (lab error, fixed before B2); re-filmed on the '
                                        'saved copy: ' + open(insp).read().strip()) if r == 'B1' and os.path.exists(insp) else None,
            'claude_own_check': dict(zip(LINES, CODED[r]['said'])), 'change': CODED[r]['change'], 'quote': CODED[r]['quote'],
            'note': NOTES.get(r), 'start_file_saved_over': sc.get('start_file_saved_over'),
            'replay': json.load(open(rep)) if os.path.exists(rep) else None,
        }
    b = [out['runs'][r]['pass'] for r in ('B1', 'B2', 'B3')]
    out['summary'] = {'with_list_passed': f'{sum(b)} of 3', 'without_list_A1': 'passed' if out['runs']['A1']['pass'] else 'broke',
                      'lines_said_with_a_number': {r: CODED[r]['said'].count(N) for r in CODED},
                      'replays_matched': sum(1 for r in out['runs'].values() if r['replay'] and r['replay'].get('match')),
                      'claude_cost_usd': round(sum(r['cost_usd'] for r in out['runs'].values()), 4)}
    json.dump(out, open(os.path.join(L6, 'compare.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(json.dumps(out['summary'], indent=1))


if __name__ == '__main__':
    main()
