"""fc14 cards and panels (FreeCAD course lesson 14, the Thickness's place in the Body: a key peg; SCRIPT-fc14.md rev
2.1 section 3): every card drawn and light, card lines 44 columns at most, chips / insets / code-panel lines 32 at most,
no percent sign and no "tooltip" / "shell" / "A1" / "B1" in any drawn text, every number on a card or panel equal to
NUMBERS.json (or a lesson / typed number), the your-turn panels carry no answer (13), the stuck-out length (13 / 12 mm)
never drawn, the Move Feature After still cropped above the lab's plumbing rows, the Short cards 1080 x 1080 and the
Short headline frame 1080 x 1920 with "PEG CAME OUT HOLLOW:" / "14, NOT 10", nothing drawn outside its frame.
Run in the draw image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fc14.py"""
import json
import os
import re
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fc14 as d  # noqa: E402

STEPS = {'card-balloon': 4, 'card-why': 5, 'card-fixed': 3}
CARDS = ([f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)] +
         ['card-end.png', 'still-mfa-1.png', 'still-mfa-2.png', 'still-mfa.png', 'still-after-A1.png',
          'still-after-B1.png'])
SHORT = ['card-why-s1.png', 'card-why-s2.png', 'card-why-s3.png']
HEAD = 'card-short-head.png'
OVS = ([f'card-recap-{i}.png' for i in (1, 2, 3)] + [f'card-yourturn-{i}.png' for i in (1, 2, 3)] +
       ['tip-flag.png', 'tip-flag-pad.png', 'ov-sides-M.png', 'ov-open-T.png', 'ov-wall-F.png'])
NUM = json.load(open(os.path.join(d.TAKES, 'NUMBERS.json'), encoding='utf-8'))
LESSON = {'1', '2', '3', '4', '13', '14', '15', '0', '1.1.4', '2.1.308', '5.5', '0.18', '0.13', '10.00', '14.00',
          '12.00'}


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
    for n in CARDS + SHORT + OVS + [HEAD] + d.PANEL_NAMES:
        assert n in run, n
        assert os.path.exists(os.path.join(d.OUT, n)), n
    assert len(d.PANEL_NAMES) >= 11


def test_no_problems(run):
    assert d.PROBLEMS == []


def test_cards_light_and_sized(run):
    for n in CARDS:
        im = Image.open(os.path.join(d.OUT, n)).convert('RGB')
        assert im.size == (2560, 1440), n
        assert sum(im.resize((1, 1)).getpixel((0, 0))) / 3 > 200, n
    for n in SHORT:
        assert Image.open(os.path.join(d.OUT, n)).size == (1080, 1080), n
    assert Image.open(os.path.join(d.OUT, HEAD)).size == (1080, 1920)
    for n in OVS + d.PANEL_NAMES:
        assert Image.open(os.path.join(d.OUT, n)).size == (2880, 1800), n


def test_columns_and_words(run):
    for n, rows in run.items():
        for t, _ in rows:
            low = t.lower()
            assert '%' not in t and 'tooltip' not in low and 'shell' not in low, (n, t)
            assert not re.search(r'\b[ab]1\b', low), (n, t)
            for ln in t.split('\n'):
                lim = 44 if n.startswith(('card', 'still', 'ov-quote')) else 32
                assert len(ln) <= lim, (n, ln)
    for n in d.PANEL_NAMES + SHORT + [HEAD]:
        if n.startswith('ov-quote'):
            continue
        for t in texts(run, n):
            for ln in t.split('\n'):
                assert len(ln) <= 32, (n, ln)


def test_numbers_from_numbers_json(run):
    ok = nums_ok()
    for n, rows in run.items():
        if n.startswith('ov-quote') or n == 'card-end.png':
            continue
        for t, _ in rows:
            for x in re.findall(r'\d+(?:\.\d+)?', re.sub(r'\d+\.\d+\.\d+', '', t)):
                assert x in ok, (n, t, x)


def test_your_turn_no_answer_no_stuck_out(run):
    for n in [f'card-yourturn-{i}.png' for i in (1, 2, 3)]:
        for t in texts(run, n):
            assert not re.search(r'\b13\b', t), (n, t)
    for n, rows in run.items():
        for t, _ in rows:
            assert not re.search(r'\b1[23] ?mm\b|sticks? out|stuck[- ]out', t), (n, t)


def test_steps_add(run):
    for s, k in dict(STEPS, **{'card-recap': 3, 'card-yourturn': 3}).items():
        if s in ('card-why', 'card-fixed', 'card-balloon'):
            continue                       # drawings: each build greys the last, the words still add
        for i in range(2, k + 1):
            prev = set(texts(run, f'{s}-{i - 1}.png'))
            assert prev <= set(texts(run, f'{s}-{i}.png')), (s, i)


def test_code_panels_big(run):
    for n in d.PANEL_NAMES:
        if n.startswith(('ov-in', 'ov-cc')):
            assert min(px for _, px in run[n]) >= 50, n      # 63 px drawn, logged at k = 0.8


def test_mfa_crop_above_plumbing():
    """The still shows the tree and the first Report row only: its crop ends above the second Report row (y 1238,
    the lab's own 'Error executing Python code' rows) and holds the words 'Invalid face reference'."""
    assert d.MFA_REPORT[3] <= 1236 and d.MFA_REPORT[1] >= 1170
    assert d.MFA_TREE[3] <= 560
    assert 'Invalid face reference' in ' '.join(texts(d.LOG, 'still-mfa-2.png'))
    assert 'lab still, FreeCAD 1.1.4' in texts(d.LOG, 'still-mfa-1.png')


def test_key_words_drawn(run):
    allt = ' | '.join(t for rows in run.values() for t, _ in rows)
    for s in ('10 + 2 + 2 = 14', '10 + 3 + 3 = 16', 'peg 14 × 14, middle air', 'opening 10 × 10 into the cup',
              'peg 10 × 10, middle plastic', 'wall closed, top open', 'inside 60 × 40, 50 deep', 'peg 12 × 12, solid',
              'joined: one solid', 'never a wall here', 'balloon = the shape you drew', 'paper = the walls Thickness grows',
              'PEG CAME OUT HOLLOW:', '14, NOT 10', 'Your turn: a peg drawn 7 wide'):
        assert s in allt, s
