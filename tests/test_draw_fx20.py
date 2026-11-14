"""fx20 cards (FreeCAD 1.1 "Negative datum values are not valid for the constraint with index 23"): every card in
SCRIPT-fx20.md rev 2 section 4 drawn as a picture exists, light, 2560 x 1440, text 44 px+ and 44 columns at most, each
step only adds, side panels stay transparent on the recording's side, the numbers are the lab's (25 - 5 - 5 = 15, 17,
index 23, 27, 40 x 20, 41, (40 mm), Pad 10, about 8000), the question is never answered (no "redundant", no "refused"),
the R1 overlays cover the start screen (banner) and the hint rows only. Run in the draw image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fx20.py"""
import os
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fx20 as d  # noqa: E402

STEPS = {'card-carpenter': 5, 'card-decode': 7, 'card-sofar': 3, 'card-question': 2, 'card-recipe': 5}
EXPECTED = [f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)]
SIDE = {'card-decode': 1430, 'card-question': 1430, 'card-recipe': 1430}
OVS = ('ov-r1-top.png', 'ov-r1-odes.png', 'ov-r1-hint.png', 'ov-r1-try.png', 'ov-a-rep.png')
FORBIDDEN = ('bug', 'broken', 'wrong', 'ready to print', 'will print', 'claude knew', 'ultra', 'value error',
             'valueerror', 'blue', '17.00', '40.00', '8000.0', 'next video', 'how much plastic', 'rail', 'fence')
ANSWER = ('redundant', 'refused', 'answer', 'it takes', 'yes', 'no:', 'datum 15')


@pytest.fixture(scope='module')
def drawn():
    d.main()
    return d


def all_text(drawn):
    return [s for items in drawn.LOG.values() for s, _ in items]


def test_all_cards_and_overlays_drawn_without_problems(drawn):
    assert drawn.PROBLEMS == []
    have = set(os.listdir(drawn.OUT))
    for n in EXPECTED + list(OVS) + ['short-stack.png', 'card-end.png']:
        assert n in have, n
    assert Image.open(os.path.join(drawn.OUT, 'short-stack.png')).size == (1080, 960)


def test_no_text_over_44_columns_and_44_px(drawn):
    for name, items in drawn.LOG.items():
        for s, px in items:
            assert px >= 44, (name, s, px)
            for ln in s.split('\n'):
                assert len(ln) <= 44, (name, ln)


def test_cards_light_sized_and_side_panels_transparent(drawn):
    for n in EXPECTED + ['card-end.png']:
        im = Image.open(os.path.join(drawn.OUT, n))
        assert im.size == (2560, 1440), n
        side = [x for p, x in SIDE.items() if n.startswith(p)]
        if side:
            assert im.mode == 'RGBA' and im.crop((0, 0, side[0], 1440)).getchannel('A').getextrema() == (0, 0), n
        else:
            px = im.convert('RGB').resize((64, 36)).getdata()
            assert sum(sum(p) / 3 for p in px) / len(px) > 200, n


def test_each_step_only_adds_text(drawn):
    for stem, k in STEPS.items():
        for i in range(2, k + 1):
            prev = {s for s, _ in drawn.LOG[f'{stem}-{i - 1}.png']}
            cur = {s for s, _ in drawn.LOG[f'{stem}-{i}.png']}
            assert prev <= cur, (stem, i, prev - cur)


def test_lab_numbers_and_do_not_say(drawn):
    txt = ' '.join(all_text(drawn)).lower()
    for want in ('25 - 5 - 5 = 15', 'arm 17', 'index 23', 'rectangle 40 x 20', 'top 41', '(40 mm)', 'pad 10',
                 'about 8000', 'shelf 27', 'wire is not closed', 'lesson 3'):
        assert want in txt, want
    for bad in FORBIDDEN:
        assert bad not in txt, bad


def test_question_never_answered(drawn):
    q = ' '.join(s for n in ('card-question-1.png', 'card-question-2.png') for s, _ in drawn.LOG[n]).lower()
    for a in ANSWER:
        assert a not in q, a


def test_overlays_cover_only_their_boxes(drawn):
    for name, box in (('ov-r1-top.png', d.R1_TOP), ('ov-r1-odes.png', d.R1_ODES), ('ov-r1-hint.png', d.R1_HINT),
                      ('ov-r1-try.png', d.R1_TRY), ('ov-a-rep.png', d.A_REP)):
        im = Image.open(os.path.join(drawn.OUT, name))
        assert im.size == (2880, 1800), name
        x, y, w, h = box
        assert im.getchannel('A').getbbox() == (x, y, x + w, y + h), name
    # SCRIPT 0.1: the banner + "Auto mode" notice (y 0-800 until ~24 s) covered across the whole left pane
    assert d.R1_TOP[1] == 0 and d.R1_TOP[3] >= 840 and d.R1_TOP[2] >= 1160
    assert drawn.LOG['ov-a-rep.png'] == []                # a plain panel, no text
