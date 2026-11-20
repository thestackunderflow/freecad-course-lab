"""fc13 cards and panels (FreeCAD course lesson 13, Thickness / Make thickness inwards; SCRIPT-fc13.md rev 2.1
section 3): every card drawn and light, card lines 44 columns at most, code-panel lines 32 at most (Claude's quoted
lines 44), no percent sign and no "tooltip" in any text, every number on a card or panel equal to NUMBERS.json (or a
lesson / typed number), the your-turn panels carry no answer (74, 47, 86, 53), the Short cards 1080 x 1080, the code
panels on Claude's files at 63 px or more, nothing drawn outside its frame.
Run in the draw image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fc13.py"""
import json
import os
import re
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fc13 as d  # noqa: E402

STEPS = {'card-pad': 5, 'card-why': 5, 'card-second': 3}
CARDS = [f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)] + ['card-end.png']
SHORT = ['card-short-why-1.png', 'card-short-why-2.png']
OVS = ([f'card-recap-{i}.png' for i in (1, 2, 3)] + [f'card-yourturn-{i}.png' for i in (1, 2, 3, 4)] +
       ['ov-block-T.png', 'ov-walls-T.png', 'ov-round-F.png'])
NUM = json.load(open(os.path.join(d.TAKES, 'NUMBERS.json'), encoding='utf-8'))
LESSON = {'1', '2', '3', '4', '13', '0', '1.1.4', '2.1.308', '5.5', '0.10', '0.07', '80', '50', '70', '64', '52',
          '60.00', '56.00', '36.00', '70.00', '2.00', '1.00'}
ANSWERS = ('74', '47', '86', '53')


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


def test_all_drawn(run):
    for n in CARDS + SHORT + OVS + d.PANEL_NAMES:
        assert n in run, n
        assert os.path.exists(os.path.join(d.OUT, n)), n
    assert len(d.PANEL_NAMES) >= 10


def test_no_problems(run):
    assert d.PROBLEMS == []


def test_cards_light_and_sized(run):
    for n in CARDS:
        im = Image.open(os.path.join(d.OUT, n)).convert('RGB')
        assert im.size == (2560, 1440), n
        assert sum(im.resize((1, 1)).getpixel((0, 0))) / 3 > 200, n
    for n in SHORT:
        assert Image.open(os.path.join(d.OUT, n)).size == (1080, 1080), n
    for n in OVS + d.PANEL_NAMES:
        assert Image.open(os.path.join(d.OUT, n)).size == (2880, 1800), n


def test_columns_and_words(run):
    for n, rows in run.items():
        for t, _ in rows:
            assert '%' not in t and 'tooltip' not in t.lower(), (n, t)
            for ln in t.split('\n'):
                lim = 44 if (n.startswith(('card', 'ov-quote')) or n.startswith('ov-')) else 32
                assert len(ln) <= lim, (n, ln)
    for n in d.PANEL_NAMES:
        if n.startswith('ov-quote'):
            continue
        for t in texts(run, n)[1:]:
            assert len(t) <= 32, (n, t)


def test_numbers_from_numbers_json(run):
    ok = nums_ok()
    for n, rows in run.items():
        if n.startswith('ov-quote') or n == 'card-end.png':
            continue
        for t, _ in rows:
            for x in re.findall(r'\d+(?:\.\d+)?', t):
                assert x in ok, (n, t, x)


def test_your_turn_no_answer(run):
    for n in [f'card-yourturn-{i}.png' for i in (1, 2, 3, 4)]:
        for t in texts(run, n):
            for a in ANSWERS:
                assert not re.search(rf'\b{a}\b', t), (n, t)


def test_steps_add(run):
    for s in ('card-pad', 'card-second', 'card-recap', 'card-yourturn'):
        k = STEPS.get(s, 3 if s == 'card-recap' else 4)
        for i in range(2, k + 1):
            prev = set(texts(run, f'{s}-{i - 1}.png'))
            assert prev <= set(texts(run, f'{s}-{i}.png')), (s, i)


def test_claude_panels_big(run):
    for n in d.PANEL_NAMES:
        if n.startswith('ov-cc'):
            assert min(px for _, px in run[n]) >= 50, n      # 63 px drawn, logged at k = 0.8


def test_key_sums_drawn(run):
    allt = ' | '.join(t for rows in run.values() for t, _ in rows)
    for s in ('60 − 2 − 2 = 56', '40 − 2 − 2 = 36', '50 − 2 = 48', '60 + 2 + 2 = 64', '64 − 3 − 3 = 58',
              'inside: 56 × 36, 48 deep', 'outside 66 × 46', 'wall 3: inside 60 × 40', 'wall 3: 60 × 40, 47 deep'):
        assert s in allt, s
