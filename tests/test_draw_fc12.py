"""fc12 cards and panels (FreeCAD course lesson 12, polar pattern Extent vs Spacing; SCRIPT-fc12.md rev 2.1 section
3): every card drawn and light, card lines 44 columns at most, code-panel lines 32 at most (Claude's quoted lines 44),
no percent sign and no "tooltip" in any text, each step only adds, every number on a card or panel equal to
NUMBERS.json (or a lesson / typed / clock number), the your-turn panels carry no answer (45, 38.57), outlines
unfilled, the wall line under the post on both top views, the K mask over the Type / Name lines only.
Run in the draw image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fc12.py"""
import json
import os
import re
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fc12 as d  # noqa: E402

STEPS = {'card-clock': 4, 'card-why': 6}
CARDS = [f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)] + ['card-end.png']
SHORT = [f'card-short-why-{i}.png' for i in (1, 2, 3)]
OVS = ([f'ov-recap-{i}.png' for i in range(1, 4)] + [f'ov-turn-{i}.png' for i in range(1, 5)] +
       [f'ov-proof-{i}.png' for i in (1, 2)] + ['ov-wall-T.png', 'ov-wall-F.png', 'ov-sum.png'])
NUM = json.load(open(os.path.join(d.TAKES, 'NUMBERS.json')))
LESSON = {'10', '1', '2', '3', '4', '5', '6', '7', '8', '9', '11', '12', '30', '72', '360', '240', '80', '60', '120', '180',
          '1.1.4', '0.1.28', '2.1.308', '5.5', '0', '0.11', '0.08', '60.00', '80.00', '90', '315'}


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
            out.update({str(v), f'{v:.2f}', f'{v:g}'})
    walk(NUM)
    return out


@pytest.fixture(scope='module')
def run():
    d.main()
    return d.LOG


def texts(log, name):
    return [t for t, _ in log[name]]


def alpha_box(name, box):
    im = Image.open(os.path.join(d.OUT, name)).convert('RGBA')
    return max(im.crop(box).getchannel('A').getextrema())


def test_all_drawn_light(run):
    for n in CARDS:
        im = Image.open(os.path.join(d.OUT, n)).convert('RGB')
        assert im.size == (2560, 1440) and sum(im.getpixel((5, 1435))) > 700, n
    for n in SHORT:
        assert Image.open(os.path.join(d.OUT, n)).size == (1080, 1080), n
    for n in OVS + d.PANEL_NAMES:
        assert Image.open(os.path.join(d.OUT, n)).size == (2880, 1800), n
    assert d.PROBLEMS == [], d.PROBLEMS


def test_columns_percent_tooltip(run):
    for n, rows in run.items():
        for t, _ in rows:
            for ln in t.split('\n'):
                lim = 32 if (n in d.PANEL_NAMES and not n.startswith('ov-quote')
                             and not ln.startswith('checked by code') and ln != 'its reply, scrolled up:'
                             and ln != 'drawn from the numbers, not a recording' and ' · hooks' not in ln) else 44
                assert len(ln) <= lim, (n, ln)
            assert '%' not in t and 'tooltip' not in t.lower(), (n, t)


def test_each_step_adds(run):
    for s, k in list(STEPS.items()) + [('card-short-why', 3), ('ov-recap', 3), ('ov-turn', 4), ('ov-proof', 2)]:
        for i in range(2, k + 1):
            a, b = set(texts(run, f'{s}-{i - 1}.png')), set(texts(run, f'{s}-{i}.png'))
            assert a <= b, (s, i, a - b)


def test_numbers_from_numbers(run):
    ok = nums_ok()
    for n, rows in run.items():
        for t, _ in rows:
            for v in re.findall(r'(?<![\w.])\d+(?:\.\d+)?', t.replace('fc12', '')):
                assert v in ok, (n, t, v)


def test_panels_script_lines(run):
    want = {'ov-gap-80.png': ['checked by code', 'gaps: 80 80 80'],
            'ov-gap-60.png': ['checked by code', 'gaps: 60 60 60'],
            'ov-gap-F8.png': ['fixed, hooks 3: 60 60', 'typed 180, hooks 3: 90 90'],
            'ov-cc-A1.png': ['checked by code (its file):', 'hooks 4: 0 60 120 180'],
            'ov-cc-B1.png': ['checked by code (its file):', 'hooks 4: 0 60 120 180', 'hooks 3: 0 60 120'],
            'ov-proof-2.png': ['checked by code (its files):', 'hooks 3: 0 60 120 (both)',
                               'hooks 6: ring, 60 apart (both)', 'drawn from the numbers, not a recording']}
    for n, lines in want.items():
        assert all(x in texts(run, n) for x in lines), (n, texts(run, n))


def test_quotes_words_unchanged(run):
    """Claude's lines re-wrapped at word gaps only: the words joined equal a run of reply.txt's words."""
    for run_id, names in (('A1-2', ('ov-quote-A1-1.png', 'ov-quote-A1-2.png', 'ov-quote-A1-3.png')),
                          ('B1-2', ('ov-quote-B1.png',))):
        reply = ' '.join(open(os.path.join(d.TAKES, 'runs', run_id, 'reply.txt'), encoding='utf-8').read().split())
        for n in names:
            body = ' '.join(t for t in texts(run, n) if t != 'its reply, scrolled up:')
            assert body.replace(' / ', ' ') in reply, (n, body)
            assert alpha_box(n, (1165, 0, 2880, 1800)) == 0, n       # over the terminal pane only


def test_yourturn_no_answer(run):
    for i in range(1, 5):
        for t in texts(run, f'ov-turn-{i}.png'):
            assert not re.search(r'(?<!\d)(45|38\.57)(?!\d)', t), t


def test_wall_under_the_post():
    for n, y in (('ov-wall-T.png', d.WALL_T[1]), ('ov-wall-F.png', d.WALL_F[1])):
        im = Image.open(os.path.join(d.OUT, n))
        assert im.getpixel((1680, y))[3] > 0 and im.getpixel((1680, y - 40))[3] == 0, n
    x, y, r = d.RING_T
    assert Image.open(os.path.join(d.OUT, 'ov-wall-T.png')).getpixel((x, y))[3] == 0     # ring unfilled


def test_panels_clear_of_the_model(run):
    """Top-view panels sit in the empty right pane (x 2130 on), under the Measurement panel (y 780 on)."""
    for n in ('ov-gap-80.png', 'ov-gap-60.png', 'ov-gap-F8.png'):
        assert alpha_box(n, (0, 0, 2130, 1800)) == 0 and alpha_box(n, (0, 0, 2880, 780)) == 0, n
    for n in ('ov-cc-A1.png', 'ov-cc-B1.png'):
        assert alpha_box(n, (0, 0, 1165, 1800)) == 0, n


# ---- cut 2 (WATCH-fc12-cut1, 17 Nov) ----
def test_c2_fix_card_and_bigger_why_lines(run):
    assert os.path.exists(os.path.join(d.OUT, 'card-fix-180.png'))
    t = texts(run, 'card-fix-180.png')
    assert '4 hooks, 3 gaps' in t and '3 × 60 = 180' in t
    sz = dict(run['card-why-5.png'])        # nice 4: the 360 / 5 lines read on a phone (the 240 / 3 line is 72)
    assert sz.get('360 ÷ 5 = 72', 0) >= 72 and sz.get('hook 6 lands on hook 1', 0) >= 60
    assert dict(run['card-why-6.png']).get('360 ÷ 6 = 60', 0) >= 72
