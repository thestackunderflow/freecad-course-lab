"""fc8 cards (FreeCAD course lesson 8, assembly; SCRIPT-fc8.md rev 2 section 4): every card drawn, light, 2560 x 1440,
text 44 px+ and 44 columns at most, each step only adds, the your-turn side panel transparent on the recording's side,
every text inside the 5% safe area, highlight boxes thin outlines (no fill), every number on a card equal to
NUMBERS.json (or a named outside source: Prusa's 0.3), the your-turn card never answers its question, the Claude Code
covers (2880 x 1800) cover the header (plan name) rows, the start-up notice and the start-up input rows only.
Run in the draw image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fc8.py"""
import json
import os
import re
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fc8 as d  # noqa: E402

STEPS = {'card-drawer': 4, 'card-assembly': 3, 'card-joint': 2, 'card-notacheck': 3, 'card-zero': 3,
         'card-print': 4, 'card-sofar': 5, 'card-recap': 5, 'card-yourturn': 4}
FIRST = {'card-recap': 0}
EXPECTED = [f'{s}-{i}.png' for s, k in STEPS.items() for i in range(FIRST.get(s, 1), FIRST.get(s, 1) + k)] + \
    ['card-end.png']
SIDE = {'card-yourturn': ('left', 1430)}
OVERLAYS = ['ov-cc-top.png', 'ov-cc-notice.png', 'ov-cc-start.png', 'ov-cc-hint.png']
NUM = json.load(open(os.path.join(d.TAKES, 'NUMBERS.json')))
FORBIDDEN = ('we printed', 'it printed', 'fuse', 'slicer', 'failed', 'wrong', 'bug', 'broken', 'minimum',
             '0.3 is enough', 'next', 'latest', 'pin icon', 'common button', 'click a face', 'through the rail',
             'solver')


@pytest.fixture(scope='module')
def drawn():
    d.main()
    return d


def texts(drawn, name):
    return [s for s, _ in drawn.LOG[name]]


def all_text(drawn):
    return [s for items in drawn.LOG.values() for s, _ in items]


def test_all_cards_drawn_without_problems(drawn):
    assert drawn.PROBLEMS == []
    have = set(os.listdir(drawn.OUT))
    for n in EXPECTED + OVERLAYS:
        assert n in have, n


def test_no_text_over_44_columns_or_under_44_px(drawn):
    for name, items in drawn.LOG.items():
        for s, px in items:
            assert px >= 44, (name, s, px)
            for ln in s.split('\n'):
                assert len(ln) <= 44, (name, ln)


def test_light_sized_and_side_panels_transparent(drawn):
    for n in EXPECTED:
        im = Image.open(os.path.join(drawn.OUT, n))
        assert im.size == (2560, 1440), n
        side = [v for p, v in SIDE.items() if n.startswith(p)]
        if side:
            where, x = side[0]
            rect = (x, 0, 2560, 1440) if where == 'right' else (0, 0, x, 1440)
            assert im.mode == 'RGBA' and im.crop(rect).getchannel('A').getextrema() == (0, 0), n
        else:
            assert sum(im.convert('L').resize((64, 36)).getdata()) / (64 * 36) > 200, n


def test_text_inside_the_safe_area(drawn):
    assert not [p for p in drawn.PROBLEMS if 'safe' in p]
    assert drawn.SAFE == (128, 72, 2432, 1368)


def test_each_step_only_adds_text(drawn):
    for pre, k in STEPS.items():
        f = FIRST.get(pre, 1)
        for i in range(f + 1, f + k):
            a, b = set(texts(drawn, f'{pre}-{i - 1}.png')), set(texts(drawn, f'{pre}-{i}.png'))
            assert a <= b, (pre, i, a - b)


def test_script_lines(drawn):
    t = all_text(drawn)
    joined = ' '.join(t)   # the your-turn panel wraps its long lines in two
    for v in ("hole = hook's slot", "drawer = rail's rib", 'a small gap: it slides', 'no gap: it jams',
              'rules for moving', 'slider: one line only', 'drawn: gap 0', 'holes print a little small',
              'Bambu Lab wiki', 'first layer spreads', 'Prusa KB: elephant foot', "won't go together without force",
              '"An initial good measurement for movable', 'parts is at least 0.3 mm." Prusa KB',
              'joint: which way it may move', 'joint: does it overlap? never asked', 'a drag is not a check',
              'touching: shared wall, no shared space', 'shared space = 0 mm³', 'touching is not room to slide',
              'assembly = components, one grounded', 'joined by a joint', 'Intersection: shared space; touch = 0',
              'Measure: reads the gap', 'parts that move need a gap', 'Intersection: overlap, not touching',
              'Your turn, no AI (start file below):', '1. Run Intersection. Read the volume.',
              '2. Set gap to 0.4. Measure both sides.', "Why can't the gap-0 hook slide on a print?"):
        assert v in t or v in joined, v
    low = joined.lower()
    for bad in FORBIDDEN:
        assert bad not in low, bad
    assert '<' not in low and '>' not in low


def test_every_number_from_numbers_json(drawn):
    c = NUM['cases']
    allowed = {f"{c['typo']['slot_head']:g}", f"{c['typo']['common_mm3']:.1f}", f"{c['gap04']['gap']:g}",
               f"{c['touch']['common_mm3']:g}", f"{c['touch']['slot_head']:g}", NUM['freecad']['version']
               if isinstance(NUM['freecad'], dict) and 'version' in NUM['freecad'] else '1.1.4'}
    allowed |= {'0.3', '1', '2', '3', '8', '1.1.4'}   # Prusa's starting value (sourced), list + lesson numbers
    for name in EXPECTED:
        for s in texts(drawn, name):
            for n in re.findall(r'\d+(?:[.,]\d+)*', s):
                assert n in allowed, (name, s, n)


def test_your_turn_never_answers(drawn):
    yt = ' '.join(texts(drawn, 'card-yourturn-4.png'))
    assert '0.40 ' not in yt and 'jam' not in yt.lower() and 'because' not in yt.lower()
    assert not re.search(r'\d+\.\d+ mm', yt)


def test_highlight_boxes_are_thin_outlines(drawn):
    assert drawn.OUTLINE_PX <= 6
    for name, box in drawn.OUTLINES:
        im = Image.open(os.path.join(drawn.OUT, name)).convert('RGB')
        x0, y0, x1, y1 = box
        inside = im.crop((x0 + drawn.OUTLINE_PX + 4, y0 + drawn.OUTLINE_PX + 4, x1 - drawn.OUTLINE_PX - 4,
                          y1 - drawn.OUTLINE_PX - 4))
        assert (234, 88, 12) not in [p for _, p in inside.getcolors(1 << 20)], name   # never filled orange


def test_claude_code_covers(drawn):
    """Header rows (logo, version, model, plan name, folder) y 0-260; the notice y 260-810; the start-up hint + input
    rows y 1540-1705; all in the left pane only (x 0-1160), nothing else covered."""
    for n, (y0, y1) in zip(OVERLAYS, ((0, 260), (260, 810), (1540, 1705), (1540, 1600))):
        a = Image.open(os.path.join(drawn.OUT, n))
        assert a.size == (2880, 1800) and a.mode == 'RGBA', n
        al = a.getchannel('A')
        assert al.crop((0, y0, 1160, y1)).getextrema() == (255, 255), n
        assert al.crop((1160, 0, 2880, 1800)).getextrema() == (0, 0), n
        if y0 > 0:
            assert al.crop((0, 0, 1160, y0)).getextrema() == (0, 0), n
        assert al.crop((0, y1, 1160, 1800)).getextrema() == (0, 0), n


def test_end_card_course_words_no_next_no_label(drawn):
    e = ' '.join(texts(drawn, 'card-end.png')).lower()
    assert 'lesson 8' in e and 'lesson 1' in e and 'subscribe' in e
    assert 'next' not in e and 'ai-generated' not in e
