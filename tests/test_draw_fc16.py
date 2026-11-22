"""fc16 cards, overlays and stills (FreeCAD course lesson 16, the hanging hole: a Pocket typed 2 deep closes to a 1 mm
skin when the wall goes to 3; Through all opens it and drills the front wall; the fix: Length = Params.wall;
SCRIPT-fc16.md rev 2 sections 0.1, 1 and 3, SCRIPT-fc16-short.md): every card drawn and light, card lines 44 columns at
most, chips / panels 32, no percent sign and no "shell" / "Reversed" / "A1" / "B1" / "To first" / "Up to face" in any
drawn text, every number from NUMBERS.json (or a lesson / typed / run-log number), the your-turn card and the Short's
question carry no answer, each build adds (earlier lines stay), the code panels 63 px on the 2880 frame, nothing in
the top band (the REAL RECORDING chip), no label over a ring or over the text it discusses, the Claude panels right of
the terminal, the inside-view stills of both Claude files show the back-wall hole open.
Run in the draw image:
MSYS_NO_PATHCONV=1 docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q -p no:cacheprovider \
  tests/test_draw_fc16.py"""
import json
import os
import re
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fc16 as d  # noqa: E402

CARDS = ([f'card-skewer-{i}.png' for i in range(1, 5)] + [f'card-why-{i}.png' for i in range(1, 6)] +
         ['card-end.png'])
SHORT = ['card-why-s1.png', 'card-why-s2.png', 'card-why-s3.png']
HEAD = 'card-short-head.png'
SHORT_OV = ['short-q.png', 'short-series.png']
STILLS = ['st-A1.png', 'st-B1.png', 'st-A1z.png', 'st-B1z.png']
LOWER = [f'rc-{i}.png' for i in (1, 2, 3)] + ['yt-1.png', 'sub-1.png', 'sub-2.png']
CHIPS = ['Pocket 2, wall 3: closed', 'Through all: front drilled', '3 − 2 = 1 mm left', 'wall − wall = 0',
         'Pocket 2, wall 2: open', 'Length = wall', 'x 0, 30 up', 'FreeCAD + Claude, lesson 16', 'FreeCAD plus Claude',
         'lesson 16', 'sped up', '5: the diameter', 'Claude Code 2.1.308 · Sonnet 5.5', 'not asked to check · $0.10',
         'asked to check · $0.13']
RINGS = ['ov-ring-result.png', 'ov-ring-type.png', 'ov-ring-result3.png', 'ov-ring-fx.png', 'ov-ring-hole-front.png',
         'ov-ring-wall.png', 'ov-ring-hole_size.png', 'ov-ring-dimension.png', 'ov-ring-tree.png', 'ov-dot-R.png',
         'ov-ring-A1-expr.png', 'ov-ring-A1-vol.png', 'ov-ring-A1-whatever.png', 'ov-ring-B1-then.png',
         'ov-ring-B1-interim.png']
LOCS = ['ov-loc-params.png', 'ov-loc-c1.png', 'ov-loc-expr.png', 'ov-loc-measure.png', 'ov-loc-type.png',
        'ov-loc-prompt-A1.png', 'ov-loc-prompt-B1.png']
PANELS = ['ov-in-F1.png', 'ov-in-F6.png', 'ov-in-F8.png', 'ov-in-F9.png', 'ov-in-F10.png', 'ov-in-F10b.png',
          'ov-cc-A1.png', 'ov-cc-B1.png', 'ov-log-A1.png', 'ov-log-B1.png', 'ov-quote-B1a.png', 'ov-quote-B1b.png']
NUM = json.load(open(os.path.join(d.TAKES, 'NUMBERS.json'), encoding='utf-8'))
LESSON = {'0', '1', '2', '3', '4', '5', '6', '12', '14', '16', '17', '30', '2.5', '0.10', '0.13', '5.5', '39.3',
          '58.9', '98.2'}


def nums_ok():
    out = set(LESSON)

    def walk(v):
        if isinstance(v, dict):
            for k, x in v.items():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            out.update({str(v), f'{v:.2f}', f'{v:g}'})
    walk(NUM)
    out.update(str(n) for n in d.TOOL_COUNTS.values())
    return out


@pytest.fixture(scope='module')
def run():
    d.main()
    return d.LOG


def texts(log, name):
    return [t for t, _ in log[name]]


def alltext(log):
    return ' | '.join(t for rows in log.values() for t, _ in rows)


def alpha(name):
    return Image.open(os.path.join(d.OUT, name)).getchannel('A')


def alpha_in(name, box):
    return alpha(name).crop(box).getbbox() is not None


def hit(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def test_all_drawn(run):
    for n in CARDS + SHORT + [HEAD] + SHORT_OV + STILLS + LOWER + RINGS + LOCS + PANELS:
        assert n in run, n
        assert os.path.exists(os.path.join(d.OUT, n)), n
    assert d.PROBLEMS == []


def test_sizes_and_light(run):
    for n in CARDS:
        im = Image.open(os.path.join(d.OUT, n)).convert('RGB')
        assert im.size == (2560, 1440), n
        assert sum(im.resize((1, 1)).getpixel((0, 0))) / 3 > 200, n
    for n in SHORT:
        im = Image.open(os.path.join(d.OUT, n)).convert('RGB')
        assert im.size == (1080, 1080), n
        assert sum(im.resize((1, 1)).getpixel((0, 0))) / 3 > 200, n
    assert Image.open(os.path.join(d.OUT, HEAD)).size == (1080, 1920)
    for n in STILLS:
        assert Image.open(os.path.join(d.OUT, n)).size == (2880, 1800), n
    for n in LOWER + RINGS + LOCS + PANELS + d.CHIP_FILES:
        im = Image.open(os.path.join(d.OUT, n))
        assert im.size == (2880, 1800) and im.mode == 'RGBA', n


def test_columns_and_words(run):
    for n, rows in run.items():
        for t, _ in rows:
            low = t.lower()
            for bad in ('%', 'shell', 'reversed', 'tooltip', 'to first', 'up to face', 'wrong', '10 m'):
                assert bad not in low, (n, t)
            assert not re.search(r'\b[ab]1\b', low), (n, t)
            for ln in t.split('\n'):
                lim = 44 if n.startswith(('card', 'st-', 'rc', 'yt', 'sub', 'ov-quote')) else 32
                assert len(ln) <= lim, (n, ln)


def test_numbers_from_the_lab(run):
    ok = nums_ok()
    for n, rows in run.items():
        if n == 'card-end.png':
            continue
        for t, _ in rows:
            for x in re.findall(r'\d+(?:\.\d+)?', re.sub(r'\d+\.\d+\.\d+', '', t)):
                assert x in ok, (n, t, x)


def test_numbers_match_the_lab():
    assert NUM['q3_typed2_wall3']['skin'] == 1.0 and NUM['q4_through_wall3']['front_hole_w'] == 5.0
    assert not NUM['q4_through_wall3']['front_solid'] and NUM['q4_through_wall3']['peg_solid']
    assert NUM['q5_fix_expr'] == 'Params.wall' and NUM['q6_proof']['typed_w4']['skin'] == 2.0
    h6 = NUM['q6_proof']['hole6']
    assert h6['back_hole_w'] == 6.0 and (h6['outside_w'], h6['outside_l']) == (68.0, 48.0) and h6['front_solid']
    assert NUM['runs']['A1']['depth_stored']['expr'] == 'Params.wall + 1'
    assert NUM['runs']['B1']['depth_stored']['expr'] == 'Params.wall'
    assert round(NUM['runs']['A1']['cost_usd'], 2) == 0.10 and round(NUM['runs']['B1']['cost_usd'], 2) == 0.13
    assert NUM['q11_your_turn']['long_2.5_w6']['skin'] == 3.5 and NUM['q11_your_turn']['short_2_w4']['skin'] == 2.0


def test_key_words_drawn(run):
    allt = alltext(run)
    for s in CHIPS + ['checked by code', 'from the run log', "Claude's reply, quoted:", '2 − 2 = 0',
                      'that is the skin', '2 never hears about the wall', 'Pocket Length 2', 'to the last face it meets',
                      'back open, front closed', 'skin 1.00 mm, closed', 'every feature Valid', 'no message',
                      'front wall: hole 5.00 across', 'peg whole', 'hole 5.00 across', 'wall 4, Length = wall: open',
                      'typed 2: 4 − 2 = 2 mm, closed', 'hole 6.00 across, open', 'front closed · outside 68 × 48',
                      'its file, walls 2, 3, 12:', 'walls 2, 3, 12: back open,', 'front closed', 'it said, untested:',
                      'Through all cuts the far wall', 'run 1, walls 2, 3, 12: open', 'run 2, walls 2, 3, 12: open',
                      'front closed in both', 'run 1: wall + 1 · run 2: wall', 'its file, inside view (still)',
                      'POCKET 2 DEEP, WALL 3:', 'HOLE CLOSED', 'A typed Length stays put',
                      'Through all goes on to the far wall', 'Length = wall', 'Your turn: Pocket 2.5 deep, typed,',
                      'in a wall 2.5 thick; wall goes to 6', 'Skin? Front wall touched?',
                      'Lesson 17: a mirrored second peg', 'comes out through the back wall',
                      'Every fix tested in both programs,', 'by hand and with Claude · Subscribe',
                      'Pocket 2 deep, wall goes to 4:', 'open or closed? Skin?', 'Full lesson: FreeCAD plus',
                      'Claude course, lesson 16', 'Subscribe', 'Params', 'Constraint1', 'Expression Editor',
                      'Measure result', 'Type list', 'the prompt', 'whole still']:
        assert s in allt, s


def test_no_answers(run):
    t = ' | '.join(texts(run, 'yt-1.png'))
    assert '3.5' not in t and 'not touched' not in t and 'closed' not in t
    q = ' | '.join(texts(run, 'short-q.png'))
    assert '2 mm' not in q and 'left' not in q


def test_steps_add(run):
    for s, k in (('card-why', 4), ('card-skewer', 4), ('rc', 3)):
        for i in range(2, k + 1):
            prev = set(texts(run, f'{s}-{i - 1}.png')) - {'wall 2', 'wall 3'}
            assert prev <= set(texts(run, f'{s}-{i}.png')), (s, i, prev - set(texts(run, f'{s}-{i}.png')))
    for i, s in ((1, '2 − 2 = 0'), (2, '3 − 2 = 1 mm left'), (3, 'that is the skin'),
                 (4, '2 never hears about the wall')):
        assert s in texts(run, f'card-why-{i}.png')
        if i > 1:
            assert s not in texts(run, f'card-why-{i - 1}.png')
    assert 'Pocket Length 2' in texts(run, 'card-why-1.png')
    assert any('to the last face' in x for x in texts(run, 'card-why-5.png'))
    assert 'to the last face it meets' in texts(run, 'card-why-s3.png')


def test_why5_round_outside_corners(run):
    """FreeCAD's Thickness grows outward: the outside corners are round (radius = wall), the inside ones sharp."""
    assert d.WHY5_CORNER_R == pytest.approx(d.WHY5_WALL * d.WHY5_K)
    im = Image.open(os.path.join(d.OUT, 'card-why-5.png')).convert('RGB')
    x0, y0 = d.WHY5_OUTER[:2]
    assert sum(im.getpixel((x0 + 3, y0 + 3))) > 700          # the very corner is white: rounded off


def test_code_panels_big_and_short(run):
    for n in PANELS[:10]:
        rows = [(t, px) for t, px in run[n] if t not in d.LABEL_LINES]     # the B1 label is a 60 px chip
        assert min(px for _, px in rows) >= 50, n           # 63 px drawn, logged at 0.8
        for t in texts(run, n):
            assert len(t) <= 32, (n, t)


def test_nothing_in_the_top_band(run):
    """The REAL RECORDING chip sits top right (footage-fx2 chip_where); the title bar and toolbars are above y 160."""
    for n in LOWER + RINGS + LOCS + PANELS + d.CHIP_FILES:
        assert not alpha_in(n, (0, 0, 2880, d.TOP_BAND)), n


def test_claude_panels_right_of_the_terminal(run):
    for n in ('ov-cc-A1.png', 'ov-cc-B1.png', 'ov-log-A1.png', 'ov-log-B1.png', 'ov-quote-B1a.png',
              'ov-quote-B1b.png', 'ov-chip-cc-version.png', 'ov-chip-run-A1.png', 'ov-chip-run-B1.png'):
        assert not alpha_in(n, (0, 0, d.CC_RIGHT, 1800)), n
        assert not alpha_in(n, (0, 1700, 2880, 1800)), n


def test_labels_clear_of_rings_and_targets(run):
    """No chip, label or panel over a ring or over the text it rings (blind-review rule)."""
    pairs = [('ov-f0-T.png', d.RING_RESULT, 'chip'), ('ov-front-A.png', d.RING_HOLE_FRONT, 'chip'),
             ('ov-in-F8.png', d.RING_HOLE_FRONT, None), ('ov-dot-R.png', d.DOT_BOX, 'chip')]
    for n, ring, _ in pairs:
        box = d.DRAWN[n]
        assert not hit(box, ring), (n, box, ring)
    for n, (box, lab) in d.LOC_DRAWN.items():
        assert not hit(lab, box), (n, lab, box)                       # the locator's label outside its box
    for n, (ring, gap) in d.GAPS.items():
        assert gap[0] <= ring[1] and ring[3] <= gap[1], (n, ring, gap)   # a text ring sits in the line gaps


def test_reply_rows_measured(run):
    """The rows the footage rings are the OCR'd rows (2 fps + 15 fps scan, 21 Nov): constants carry y and first time."""
    assert d.ROWS['A1_expr'][:2] == (814, 854) and d.ROWS['A1_expr'][2] == pytest.approx(35.93)
    assert d.ROWS['A1_vol'][0] == 1206 and d.ROWS['B1_interim'][2] == pytest.approx(48.8)
    for run_, bands in d.MASK.items():
        ts = [a for a, _, _ in bands]
        assert ts == sorted(ts) and bands[0][0] == 0.0, run_
        assert all(880 <= y0 <= 1450 and t1 > t0 for t0, t1, y0 in bands), run_


def test_quotes_are_its_words(run):
    reply = ' '.join(open(os.path.join(d.TAKES, 'runs', 'B1', 'reply.txt'), encoding='utf-8').read().split())
    for n in ('ov-quote-B1a.png', 'ov-quote-B1b.png'):
        t = texts(run, n)
        assert t[0] == "Claude's reply, quoted:"
        body = ' '.join(t[1:]).strip('“”')
        assert body in reply, body


def test_tool_counts_from_the_log():
    assert d.TOOL_COUNTS == {'A1': 5, 'B1': 5}
    assert d.TOOL_NAMES['A1'][0] == 'list_documents' and d.TOOL_NAMES['B1'][:2] == ['list_documents', 'get_objects']


def test_stills_show_the_hole_open(run):
    """F14: both Claude files, same inside view; the back-wall hole lets the light through (background grey seen
    through it), the wall around it is the part colour."""
    for r in ('A1', 'B1'):
        im = Image.open(d.STILL_SRC[r]).convert('RGB')
        assert min(im.getpixel(d.HOLE_LIGHT)) > 235, (r, im.getpixel(d.HOLE_LIGHT))
        wr, wg, wb = im.getpixel(d.WALL_PX)
        assert wr > wb + 60, (r, (wr, wg, wb))
        assert any('inside view (still)' in t for t in texts(run, f'st-{r}.png'))
        z = texts(run, f'st-{r}z.png')
        assert 'whole still' in z and 'checked by code' in z
        assert not hit(d.DRAWN[f'st-{r}z.png:panel'], d.DRAWN[f'st-{r}z.png:crop']), r
        assert d.DRAWN[f'st-{r}z.png:k'] >= 1.2


def test_end_card_label_band_free(run):
    """The AI-voice label goes in the last 15 s at the bottom (as fc15): the card's bottom band stays empty."""
    im = Image.open(os.path.join(d.OUT, 'card-end.png')).convert('L').crop((0, 1300, 2560, 1440))
    assert im.getextrema()[0] > 240
    assert any('Subscribe' in t for t in texts(run, 'card-end.png'))


def test_short_head(run):
    t = texts(run, HEAD)
    assert t == ['POCKET 2 DEEP, WALL 3:', 'HOLE CLOSED']
    assert alpha_in(HEAD, (0, 0, 1080, 300))


# --- cut 2 (WATCH-fc16-cut1, verified on the frames) -----------------------------------------------------------------
def test_cut2_why_card_opens_without_the_sum(run):
    """F7: card-why-0 is the wall-2 section and the Pocket arrow only; the "2 − 2 = 0" sum comes with card-why-1."""
    t0 = texts(run, 'card-why-0.png')
    assert 'Pocket Length 2' in t0 and 'wall 2' in t0 and '2 − 2 = 0' not in t0
    assert set(t0) <= set(texts(run, 'card-why-1.png'))


def test_cut2_through_all_card_builds(run):
    """F8: card-why-5 in three steps: into the back wall (FreeCAD's guide words on screen), across the inside to the
    far wall, then the front wall drilled."""
    s = [set(texts(run, f'card-why-5-{i}.png')) for i in (1, 2, 3)]
    assert s[0] <= s[1] <= s[2]
    assert any('FreeCAD guide' in x for x in s[0]) and 'back wall' in s[0] and 'front wall too' not in s[0]
    assert 'far wall' in s[1] and 'front wall too' not in s[1]
    assert 'front wall too' in s[2] and 'to the last face' in s[2]
    assert set(texts(run, 'card-why-5.png')) == s[2]


def test_cut2_short_through_all_walls_named(run):
    t = texts(run, 'card-why-s3.png')
    assert 'back wall' in t and 'front wall' in t


def test_cut2_b1_spinner_masked_after_enter(run):
    """B1 Enter at 14.284: until the reply starts (16.0) the spinner row sits at y 1108 and the status row moves; the
    mask starts at 1100 (cut 1 OCR: "auto mode" at 5:10.5)."""
    band = [y for t0, t1, y in d.MASK['B1'] if t0 <= 14.3 < t1][0]
    assert band <= 1100
    assert [y for t0, t1, y in d.MASK['B1'] if t0 <= 16.2 < t1][0] <= 1192
