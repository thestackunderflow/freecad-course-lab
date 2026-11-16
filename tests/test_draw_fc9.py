"""fc9 cards (FreeCAD course lesson 9, LinearPattern coat rack; SCRIPT-fc9.md rev 2 section 3): every card drawn, light,
2560 x 1440 (the Short's card 1080 x 960), text 44 px+ and 44 columns at most, no "%" anywhere, each step only adds,
the recap side panel transparent on the recording's side, every text inside the 5 percent safe area, highlight boxes
thin outlines (no fill), every number equal to NUMBERS.json (or the fence arithmetic / lesson numbers), no "80" on any
card (the your-turn answer is the pinned comment only), the Claude Code covers on the left pane only.
Run in the draw image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fc9.py"""
import json
import os
import re
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fc9 as d  # noqa: E402

STEPS = {'card-fence': 5, 'card-length': 4, 'card-trap': 5, 'card-recap': 4, 'card-yourturn': 3}
EXPECTED = [f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)] + ['card-end.png']
SHORT = ['card-short-why-1.png', 'card-short-why-2.png']
SIDE = {'card-recap': ('left', 1430)}
OVERLAYS = {'ov-cc-top.png': (0, 175), 'ov-cc-save.png': (1630, 1700), 'ov-cc-start.png': (1540, 1705),
            'ov-cc-hint.png': (1540, 1600)}
NUM = json.load(open(os.path.join(d.TAKES, 'NUMBERS.json')))
FORBIDDEN = ('dropped', 'missing', 'error', 'overall length', 'latest', 'slicer', 'print', 'offset 30',
             'claude measured', 'saved the file', 'next')


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
    for n in EXPECTED + SHORT + list(OVERLAYS):
        assert n in have, n


def test_no_text_over_44_columns_or_under_44_px_no_percent(drawn):
    for name, items in drawn.LOG.items():
        for s, px in items:
            assert px >= 44, (name, s, px)
            assert '%' not in s, (name, s)
            for ln in s.split('\n'):
                assert len(ln) <= 44, (name, ln)


def test_light_sized_and_side_panels_transparent(drawn):
    for n in EXPECTED:
        im = Image.open(os.path.join(drawn.OUT, n))
        assert im.size == (2560, 1440), n
        side = [v for p, v in SIDE.items() if n.startswith(p)]
        if side:
            where, x = side[0]
            assert im.mode == 'RGBA' and im.crop((0, 0, x, 1440)).getchannel('A').getextrema() == (0, 0), n
        else:
            assert sum(im.convert('L').resize((64, 36)).getdata()) / (64 * 36) > 200, n
    for n in SHORT:
        im = Image.open(os.path.join(drawn.OUT, n))
        assert im.size == (1080, 960), n
        assert sum(im.convert('L').resize((54, 48)).getdata()) / (54 * 48) > 200, n


def test_text_inside_the_safe_area(drawn):
    assert not [p for p in drawn.PROBLEMS if 'safe' in p]
    assert drawn.SAFE == (128, 72, 2432, 1368)


def test_each_step_only_adds_text(drawn):
    for pre, k in list(STEPS.items()) + [('card-short-why', 2)]:
        for i in range(2, k + 1):
            a, b = set(texts(drawn, f'{pre}-{i - 1}.png')), set(texts(drawn, f'{pre}-{i}.png'))
            assert a <= b, (pre, i, a - b)


def test_script_lines(drawn):
    t = all_text(drawn)
    for v in ('6 m, not 10', '4 posts, 3 spaces', 'Length = 120', 'margin 20', 'last hook 20',
              'first start 20 + Length 180 = 200', '4 steps × 45', 'touching nothing: a warning only',
              'fence: first post to last post', 'Occurrences includes the first hook',
              'Extent Length: first start to last start', 'at 180: the last copy floats, warning only',
              'Your turn, no AI:', 'strip 140 · 3 hooks, 20 wide · margins 20', 'Length = ?  Then measure both ends.'):
        assert v in t, v
    low = ' '.join(t).lower()
    for bad in FORBIDDEN:
        assert bad not in low, bad
    assert not re.search(r'\bfree\b', low)
    assert '<' not in low and '>' not in low


def test_every_number_from_numbers_json(drawn):
    c, p = NUM['cases'], NUM['part']
    allowed = {f'{v:g}' for v in c['trap']['starts'] + c['fix']['starts'] + c['proof']['starts']}
    allowed |= {f"{p[k]:g}" for k in ('rack_width', 'width', 'margin', 'hooks')}
    allowed |= {f"{c['trap']['length_mm']:g}", f"{c['fix']['length_mm']:g}", f"{c['proof']['length_mm']:g}",
                f"{c['trap']['starts'][1] - c['trap']['starts'][0]:g}", f"{c['trap']['occurrences'] - 1:g}",
                f"{c['yourturn']['hooks']:g}", f"{c['yourturn']['left_gap_mm']:g}", '140'}
    allowed |= {'0', '2', '4', '6', '3', '10', '12', '8', '9', '1.1.4'}   # the fence arithmetic, lesson numbers
    for name in EXPECTED + SHORT:
        for s in texts(drawn, name):
            for n in re.findall(r'\d+(?:[.,]\d+)*', s):
                assert n in allowed, (name, s, n)


def test_no_80_anywhere_and_your_turn_never_answers(drawn):
    for s in all_text(drawn):
        assert not re.search(r'(?<![\d.])80(?![\d.])', s), s
    yt = ' '.join(texts(drawn, 'card-yourturn-3.png'))
    assert 'Length = ?' in yt


def test_highlight_boxes_are_thin_outlines(drawn):
    assert drawn.OUTLINE_PX <= 6
    for name, box in drawn.OUTLINES:
        im = Image.open(os.path.join(drawn.OUT, name)).convert('RGB')
        x0, y0, x1, y1 = box
        inside = im.crop((x0 + drawn.OUTLINE_PX + 4, y0 + drawn.OUTLINE_PX + 4, x1 - drawn.OUTLINE_PX - 4,
                          y1 - drawn.OUTLINE_PX - 4))
        assert (234, 88, 12) not in [p for _, p in inside.getcolors(1 << 20)], name


def test_claude_code_covers(drawn):
    """Header rows y 0-175 (logo, version, model, the lab's plan cover, folder), the "save the document" suggestion
    y 1630-1700, the start-up hint + "Try ..." rows; the left pane only (x 0-1160)."""
    for n, (y0, y1) in OVERLAYS.items():
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
    assert 'lesson 9' in e and 'lesson 8' in e and 'subscribe' in e
    assert 'next' not in e and 'ai-generated' not in e


CODE_PANELS = {'ov-code-fix.png': ('fix', ), 'ov-code-proof.png': ('proof', ),
               'ov-code-control.png': ('proof', 'control')}


def test_cut3_code_panels(drawn):
    """WATCH-fc9-c2 #1: the right-end numbers read by code are on screen when said: a small "checked by code" panel
    with fc9numbers.py's NUMBERS.json values, inside the Measure zoom (MEAS_Z x 2080-2880, y 582-1032), below the
    Measurement panel (y 810) and above the caption band (y 968); readable after the 3.2x zoom (44 px+)."""
    c = NUM['cases']
    for n, cases in CODE_PANELS.items():
        a = Image.open(os.path.join(drawn.OUT, n))
        assert a.size == (2880, 1800) and a.mode == 'RGBA', n
        bb = a.getchannel('A').getbbox()
        assert bb[0] >= 2090 and bb[2] <= 2870 and bb[1] >= 815 and bb[3] <= 962, (n, bb)
        t = texts(drawn, n)
        assert t[0] == 'checked by code · Measure above = left end', t
        assert len(t) == 1 + len(cases), t
        for s, case in zip(t[1:], cases):
            k = c[case]
            assert s.startswith(case) and f"right_gap_mm {k['right_gap_mm']:.1f}" in s, s
            if case != 'fix':
                assert f"length_mm {k['length_mm']:.1f}" in s, s
            else:
                assert f"left_gap_mm {k['left_gap_mm']:.1f}" in s, s
        for s, px in drawn.LOG[n]:
            assert px >= 44 and len(s) <= 44 and '%' not in s, (n, s, px)
    assert '60.0' in texts(drawn, 'ov-code-control.png')[2]
