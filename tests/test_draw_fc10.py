"""fc10 cards and panels (FreeCAD course lesson 10, fully constrained sketches; SCRIPT-fc10.md rev 2 section 3):
every card drawn, light, 2560 x 1440 (the Short's 1080 x 960), text 44 px+ and 44 columns at most (code panels on the
source sized for their shot), no percent sign, each step only adds, every text inside the 5 percent safe area, every
number on a card or code panel equal to NUMBERS.json (or a lesson / typed number), the your-turn cards carry no
answer, the "checked by code" panels in one style with the script's lines, the ghost outline at the 60 anchors and
the red floor line from NUMBERS takes.*.px, the Claude Code covers on the left pane only.
Run in the draw image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fc10.py"""
import json
import os
import re
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fc10 as d  # noqa: E402

STEPS = {'card-note': 5, 'card-why': 6, 'card-yourturn': 4}
EXPECTED = [f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)] + ['card-end.png']
SHORT = ['card-short-why-1.png', 'card-short-why-2.png']
PANELS = ['ov-full-T.png', 'ov-meas-T.png', 'ov-meas-TB.png', 'ov-full-P.png', 'ov-msg-P.png', 'ov-meas-A.png',
          'ov-full-A.png', 'ov-meas-C.png', 'ov-full-D1.png', 'ov-full-D2.png', 'ov-cc-A1.png', 'ov-cc-B1.png',
          'ov-short-T.png', 'ov-short-P.png', 'ov-short-TB.png']
OVERLAYS = ['ov-cc-top.png', 'ov-cc-title.png', 'ov-cc-save.png', 'ov-floor-T.png', 'ov-floor-TB.png',
            'ov-floor-A.png', 'ov-recap-1.png', 'ov-recap-2.png'] + PANELS
NUM = json.load(open(os.path.join(d.TAKES, 'NUMBERS.json')))
LESSON = {'1', '2', '3', '4', '9', '10', '1.1.4', '0.1.28', '2.1.308', '0', '15', '30', '40', '60', '80', '100',
          '11', '20', '18.68', '0.00'}


def nums_ok():
    out = set(LESSON)

    def walk(v):
        if isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            out.update({f'{v:g}', f'{v:.1f}', f'{v:.2f}', f'{abs(v):.2f}'})
    walk(NUM)
    return out


@pytest.fixture(scope='module')
def drawn():
    d.main()
    return d


def test_all_drawn_without_problems(drawn):
    assert drawn.PROBLEMS == []
    have = set(os.listdir(drawn.OUT))
    for n in EXPECTED + SHORT + OVERLAYS:
        assert n in have, n
    for n in EXPECTED:
        assert Image.open(os.path.join(drawn.OUT, n)).size == (2560, 1440), n
    for n in SHORT:
        assert Image.open(os.path.join(drawn.OUT, n)).size == (1080, 960), n
    for n in OVERLAYS:
        assert Image.open(os.path.join(drawn.OUT, n)).size == (2880, 1800), n


def test_text_44_columns_44_px_no_percent(drawn):
    for name, items in drawn.LOG.items():
        for s, px in items:
            assert px >= 44, (name, s, px)          # code panels log their size as seen in their shot
            assert '%' not in s and '<' not in s and '>' not in s, (name, s)
            for ln in s.split('\n'):
                assert len(ln) <= 44, (name, ln)


def test_light_cards(drawn):
    for n in EXPECTED + SHORT:
        im = Image.open(os.path.join(drawn.OUT, n)).convert('RGB')
        assert im.getpixel((5, 5)) == (255, 255, 255), n


def test_each_step_adds(drawn):
    for s, k in STEPS.items():
        prev = []
        for i in range(1, k + 1):
            now = [t for t, _ in drawn.LOG[f'{s}-{i}.png']]
            for t in prev:
                assert t in now, (s, i, t)
            prev = now


def test_every_number_from_numbers_json(drawn):
    ok = nums_ok()
    for name, items in drawn.LOG.items():
        for s, _ in items:
            for tok in re.findall(r'-?\d+(?:\.\d+)*', s):
                assert tok in ok or tok.lstrip('-') in ok, (name, s, tok)


def lines(n):
    return [s for s, _ in d.LOG[n]]


def test_panel_lines_say_what_the_script_says(drawn):
    assert lines('ov-full-T.png') == ['checked by code', 'bottom -9.15 · top 50.85',
                                      'hole 5.85 from top (was 0 · 60 · 15)', 'by code = a script reads the saved model']
    assert lines('ov-meas-T.png') == lines('ov-full-T.png')
    assert lines('ov-meas-TB.png') == ['checked by code', 'bottom 0.00 · top 60.00', 'hole 15.0 from top']
    assert lines('ov-full-P.png') == ['checked by code', 'hole 15.0 from top']
    assert lines('ov-msg-P.png') == ['checked by code', 'panel text: Under-constrained:', '2 Degrees of Freedom']
    assert lines('ov-meas-A.png') == ['checked by code', 'bottom -1.32 · top 78.68', 'hole 13.68 from top']
    assert lines('ov-full-A.png') == lines('ov-meas-A.png')
    assert lines('ov-meas-C.png') == ['checked by code', 'bottom 0.00 · top 80.00', 'hole 15.0 from top']
    assert lines('ov-full-D1.png') == ['checked by code', 'pinned: bottom 0.00 · top 100.00', 'hole 15.0 from top']
    assert lines('ov-full-D2.png') == lines('ov-full-D1.png') + ['unpinned copy at 100, 3 tries:',
                                                                 'bottom -2.64 once · -11.71 twice']
    assert lines('ov-cc-A1.png') == ['checked by code (its file):', '2 degrees of freedom · bottom -10.39',
                                     'top 69.61 · hole 4.61 from top']
    assert lines('ov-cc-B1.png') == ['checked by code (its file):', '0 degrees of freedom · bottom 0.00',
                                     'top 80.00 · hole 15.0 from top']
    assert lines('ov-short-T.png') == ['checked by code', 'bottom -9.15 · hole 5.85 from top', '(was 0 · 15)']
    assert lines('ov-short-P.png') == ['checked by code', 'panel text:', '2 Degrees of Freedom']
    assert lines('ov-short-TB.png') == ['checked by code', 'bottom 0.00 · hole 15.0 from top']


def test_why_card_tries(drawn):
    t3 = ' '.join(lines('card-why-3.png'))
    assert 'same file, same change, 11 tries:' in t3 and 'bottom down 1.32' in t3
    assert 'bottom down 1.32 · 6.97 · 10.39' in ' '.join(lines('card-why-5.png'))
    assert '18.68 up · 1.32 down' in ' '.join(lines('card-why-3.png'))
    assert '1.32' not in ' '.join(lines('card-why-2.png'))   # 1.32 lands with its sentence (build 3)
    assert 'all 20 goes up' in ' '.join(lines('card-why-6.png'))
    tries = NUM['g0']['unpinned_80_tries']
    assert len(tries) == 11 and all(t['zmin'] < 0 for t in tries)
    assert sorted({f"{-t['zmin']:.2f}" for t in tries}) == ['1.32', '10.39', '6.97']


def test_your_turn_has_no_answer(drawn):
    for i in range(1, 5):
        for s, _ in drawn.LOG[f'card-yourturn-{i}.png']:
            toks = re.findall(r'\d+', s)
            assert '2' not in toks and '4' not in toks and '0' not in toks, s
            if '60' in toks:
                assert '40 → 60' in s, s


def test_floor_overlay_from_the_px_anchors(drawn):
    px = drawn.front_px('T')
    im = Image.open(os.path.join(drawn.OUT, 'ov-floor-T.png'))
    fy = px['at0'][1]
    assert im.getpixel((px['floor-left'][0] + 20, fy))[:3] == d.RED          # the red floor line at z = 0
    x60, y60 = px['at60']
    assert im.getpixel((x60, y60 + 40))[3] > 0 or im.getpixel((x60 + 2, y60 + 40))[3] > 0   # the ghost's back edge
    assert im.getpixel((1000, 300))[3] == 0


def test_claude_covers_left_pane_only(drawn):
    for n in ('ov-cc-top.png', 'ov-cc-title.png', 'ov-cc-save.png'):
        im = Image.open(os.path.join(drawn.OUT, n))
        assert im.getbbox()[2] <= 1160, n
    top = Image.open(os.path.join(drawn.OUT, 'ov-cc-top.png'))
    assert top.getpixel((600, 140))[3] == 255          # "Claude Code v..." header row covered
