"""fc11 cards and panels (FreeCAD course lesson 11, reference constraints; SCRIPT-fc11.md rev 2.1 section 3): every
card drawn and light, card lines 44 columns at most, code-panel lines 32 at most, no percent sign and no "blue" in any
text, each step only adds (a later build keeps the earlier text), every number on a card or panel equal to
NUMBERS.json (or a lesson / typed number), the your-turn panels carry no answer (50, 67, 67.08), outlines unfilled,
the hole ring inside the plate, the lab stills cut above y 1380 (no Report band).
Run in the draw image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fc11.py"""
import json
import os
import re
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fc11 as d  # noqa: E402

STEPS = {'card-list': 4, 'card-why': 5}
CARDS = [f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)] + ['card-end.png']
SHORT = [f'card-short-why-{i}.png' for i in (1, 2, 3)]
OVS = ([f'ov-recap-{i}.png' for i in range(1, 5)] + [f'ov-turn-{i}.png' for i in range(1, 6)] +
       ['ov-ring-60.png', 'ov-ring-80.png', 'ov-cc-top.png', 'ov-cc-auto.png', 'ov-cc-quote-B1.png'])
STILLS = ['still-other-red.png', 'still-other-inv.png', 'still-other-80.png', 'short-pair.png']
NUM = json.load(open(os.path.join(d.TAKES, 'NUMBERS.json')))
LESSON = {'1', '2', '3', '4', '5', '6', '7', '8', '10', '11', '15', '24', '23', '30', '31', '40', '45', '55', '60', '65', '75', '80', '95',
          '100', '1.1.4', '0.1.28', '2.1.308', '5.5', '0', '0.12', '0.09', '60.00', '80.00', '100.00', '80.0'}


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


def test_all_drawn_light(run):
    for n in CARDS + SHORT + STILLS:
        im = Image.open(os.path.join(d.OUT, n)).convert('RGB')
        assert sum(im.getpixel((5, im.size[1] - 5))) > 700, n
    for n in OVS + d.PANEL_NAMES:
        assert Image.open(os.path.join(d.OUT, n)).size == (2880, 1800), n
    assert d.PROBLEMS == [], d.PROBLEMS


def test_columns_percent_blue(run):
    for n, rows in run.items():
        for t, _ in rows:
            for ln in t.split('\n'):
                lim = 32 if n in d.PANEL_NAMES and ln != d.CHIP and not ln.startswith(('checked by code', 'lab test')) else 44
                assert len(ln) <= lim, (n, ln)
            assert '%' not in t and 'blue' not in t.lower(), (n, t)


def test_each_step_adds(run):
    for s, k in list(STEPS.items()) + [('card-short-why', 3), ('ov-recap', 4), ('ov-turn', 5)]:
        for i in range(2, k + 1):
            a, b = set(texts(run, f'{s}-{i - 1}.png')), set(texts(run, f'{s}-{i}.png'))
            assert a <= b, (s, i, a - b)


def test_numbers_from_numbers(run):
    ok = nums_ok()
    for n, rows in run.items():
        for t, _ in rows:
            for v in re.findall(r'(?<![\w.])\d+(?:\.\d+)?', t.replace('fc11', '')):
                assert v in ok, (n, t, v)


def test_panels_script_lines(run):
    want = {'ov-meas-F0.png': ['sheet 80 · top 60.00', 'screw hole: none'],
            'ov-sk-F1.png': ['top 80.00 · inside 75 (shown)', 'hole 15 below the top'],
            'ov-sk-F3.png': ['hole = plate_height − 15', 'at 60: hole at 45'],
            'ov-msg-D.png': ['panel text: Under-constrained:', '1 Degrees of Freedom'],
            'ov-full-F6.png': ['top 60.00 · STL 60.00 tall', 'outline sizes on plate_height: 0'],
            'ov-meas-F9.png': ['top 80.00 · inside 75 (shown)', 'hole at 65: 15 below the top'],
            'ov-meas-X2.png': ['fixed: top 100.00 · shown 95', 'deleted-size copy at 100:', 'top 60.00 · no hole'],
            'ov-cc-A1.png': ['top 80.00 · inside 75 (formula)', 'hole at 65: 15 below the top']}
    for n, lines in want.items():
        assert all(x in texts(run, n) for x in lines), (n, texts(run, n))
    assert 'checked by code (its file):' in texts(run, 'ov-cc-B1.png')
    assert 'by code = a script reads the saved model' in texts(run, 'ov-meas-F0.png')


def test_yourturn_no_answer(run):
    for i in range(1, 6):
        for t in texts(run, f'ov-turn-{i}.png'):
            assert not re.search(r'(?<!\d)(50|67|67\.08)(?!\d)', t), t


def test_ring_in_plate():
    x, y, r = d.HOLE
    assert 1469 < x - r and x + r < 1892 and 351 < y - r and y + r < 1408 and 30 < r < 70
    ring = Image.open(os.path.join(d.OUT, 'ov-ring-60.png'))
    assert ring.getpixel((x, y))[3] == 0          # unfilled


def test_stills_cut_report_band():
    for n in STILLS:
        im = Image.open(os.path.join(d.OUT, n)).convert('RGB')
        assert im.size == (2880, 1800)
        assert d.STILL_CUT <= 1380


# ---- cut 2 (WATCH-fc11-cut1) ----
def alpha_box(name, box):
    im = Image.open(os.path.join(d.OUT, name)).convert('RGBA')
    return max(im.crop(box).getchannel('A').getextrema())


def test_other_order_real_frames_no_lab_words(run):
    """F8b: FreeCAD's own "Redundant constraints: (24)" panel (G0b s7-after-ok, both sizes on the sketch), the tree's
    "!" after Close (s9-closed-60) and the 80 still; no "lab" word on any still."""
    src = Image.open(os.path.join(d.TAKES, 'G0b', 's7-after-ok.png')).convert('RGB')
    red = Image.open(os.path.join(d.OUT, 'still-other-red.png')).convert('RGB')
    for xy in ((2300, 755), (1530, 760), (1610, 790)):
        assert red.getpixel(xy) == src.getpixel(xy), xy
    for n in ('still-other-red.png', 'still-other-inv.png', 'still-other-80.png'):
        for t, _ in run.get(n, []):
            assert 'lab' not in t.lower(), (n, t)
    assert any('Invalid' in t for t, _ in run['still-other-inv.png'])
    assert any('top 60.00' in t for t, _ in run['still-other-80.png'])
    assert not any('top 60.00' in t for t, _ in run['still-other-inv.png'])


def test_sketch_panels_lower_left(run):
    """The sketch-zoom panels sit lower left (the top label covered them at 0:15, 1:27, 4:55); no chip on ov-sk-F0."""
    for n in ('ov-sk-F0.png', 'ov-sk-F3.png', 'ov-sk-F9.png', 'ov-sk-F1.png'):
        assert alpha_box(n, (600, 420, 1460, 1000)) == 0, n
        assert alpha_box(n, (600, 1000, 1460, 1440)) > 0, n
        assert alpha_box(n, (1470, 0, 2880, 1800)) == 0, n
    assert d.CHIP not in texts(run, 'ov-sk-F0.png')


def test_claude_panels_off_the_reply(run):
    """Claude Code's reply fills x 0-1160; the panels sit in FreeCAD's empty pane / view, left of the hook (x 2040)."""
    for n in ('ov-cc-A1.png', 'ov-cc-B1.png', 'ov-cc-quote-B1.png'):
        assert alpha_box(n, (0, 0, 1165, 1800)) == 0, n
        assert alpha_box(n, (2035, 0, 2880, 1800)) == 0, n
        assert alpha_box(n, (1165, 0, 2035, 1800)) > 0, n


def test_yourturn_clear_of_the_rectangle(run):
    """The rectangle's lower-left corner (the diagonal's start) is at about x 1197, y 1345 on take Y."""
    for i in range(1, 6):
        assert alpha_box(f'ov-turn-{i}.png', (1180, 0, 2880, 1800)) == 0, i
