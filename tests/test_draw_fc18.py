"""fc18 cards / overlays (video/draw_fc18.py, SCRIPT-fc18.md rev 2 section 3): every file drawn, the sizes, no problem
lines (32 columns on chips / panels / Short, 44 on cards), never the run names, no percent sign or angle brackets, every
number NUMBERS.json's. Run in the draw image:
  MSYS_NO_PATHCONV=1 docker run --rm -v "<edu-visualization>:/ev" -w /ev/freecad-course-lab cad3way-draw:1 \
    python3 -m pytest -q tests/test_draw_fc18.py"""
import os
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'video'))
import draw_fc18 as d  # noqa: E402

FULL = ['card-half-1.png', 'card-half-2.png', 'card-end.png']
SRC = ['ov-tile-0.png', 'ov-in-F1.png', 'ov-in-F7.png', 'ov-in-F7-1.png', 'ov-in-F7-2.png', 'ov-in-K.png',
       'ov-in-C.png', 'ov-in-B1.png', 'ov-in-A1.png', 'ov-in-F8.png', 'ov-chip-r120.png', 'ov-chip-r60.png', 'ov-chip-r80.png', 'ov-chip-nodia.png',
       'ov-chip-plane.png', 'ov-chip-far.png', 'ov-chip-cc-version.png', 'ov-chip-run-A1.png', 'ov-chip-run-B1.png',
       'rc-1.png', 'yt-1.png', 'yt-2.png', 'sub-1.png', 'sub-2.png', 'sub-3.png']
STILLS = ['st-A1a.png', 'st-A1b.png', 'st-A1c.png', 'st-B1a.png', 'st-B1b.png', 'st-B1c.png']
SHORT = ['short-head.png', 'short-q.png', 'short-series.png', 'short-tile.png']


@pytest.fixture(scope='module')
def drawn():
    d.main()
    return d


def test_files_and_sizes(drawn):
    for f in FULL:
        assert Image.open(os.path.join(d.OUT, f)).size == (2560, 1440), f
    for f in SRC:
        assert Image.open(os.path.join(d.OUT, f)).size == (2880, 1800), f
    for f in SHORT:
        assert Image.open(os.path.join(d.OUT, f)).size == (1080, 1920), f
    for f in STILLS:
        im = Image.open(os.path.join(d.OUT, f))
        assert im.size == (2880, 1800) and im.mode == 'RGB', f


def test_no_problems(drawn):
    assert d.PROBLEMS == []


def test_words(drawn):
    words = ' '.join(d.WORDS)
    for bad in ('A1', 'B1', '%', '<', '>', 'bounding box', 'SolidCraft +'):
        assert bad not in words, bad
    for want in ('120 across', '60 across', 'R 60 × 2 = 120', 'R 30 × 2 = 60', 'R 40 × 2 = 80', 'no Diameter mode',
                 '80,450', '34,080', 'about 2.4 × the plastic', '160 across', 'XZ', 'MY REVOLVED CUP CAME',
                 'OUT TWICE AS WIDE', '$0.11', '$0.08'):
        assert want in words, want


def test_numbers_are_the_labs(drawn):
    n = d.NUM
    assert n['q3_trap']['outside_x'] == 120.0 and n['q4_fix']['outside_x'] == 60.0
    assert round(n['q3_trap']['volume']) == 80450 and round(n['q4_fix']['volume']) == 34080
    assert n['q5']['fixed_reopened_80']['outside_x'] == 80.0 and n['q5']['name_80']['outside_x'] == 160.0
    assert n['q9']['name_40']['outside_x'] == 80.0 and n['q9']['fixed_45']['outside_x'] == 45.0 and n['q9']['name_45']['outside_x'] == 90.0
    assert n['runs']['A1']['pass'] and n['runs']['B1']['pass']


def texts(name):
    return [t for t, _ in d.LOG[name]]


def test_new_code_panels(drawn):
    """lab 29f31b3: run one's file panel (Claude frames, FreeCAD side) and the fix's 60.00 / inside 56 panel."""
    assert texts('ov-in-A1.png') == ['checked by code', 'run 1 file: 60, 80, 45 across', 'width = diameter / 2']
    assert texts('ov-in-B1.png') == ['checked by code', 'run 2 file: 60, 80, 45 across', 'width = diameter / 2']
    assert texts('ov-in-F8.png') == ['checked by code', 'this cup: 60.00 across']
    assert d.NUM['q4_fix']['inside'] == 56.0


def test_reply_strips(drawn):
    """Claude's long replies as excerpt strips, three builds each; frames inside the reply windows (A1 42.0-50.7,
    B1 55.0-63.3, never B1's 51-55 scroll); every strip above the status rows (y 1451) and scaled 2x+ (phone)."""
    assert 42.0 <= d.REPLY_AT['A1'] <= 50.7 and 55.0 <= d.REPLY_AT['B1'] <= 63.3
    for run in ('A1', 'B1'):
        a, b_, c = (texts(f'st-{run}{x}.png') for x in 'abc')
        chip = 'not asked to check · $0.11' if run == 'A1' else 'asked to check · $0.08'
        assert chip in a and chip in c
        assert 'checked by code' in c and 'checked by code' not in b_ and 'checked by code' not in a
        assert len(d.STRIPS[f'st-{run}a.png']) < len(d.STRIPS[f'st-{run}b.png'])   # b adds strips (builds)
        for name in (f'st-{run}{x}.png' for x in 'abc'):
            for box, k, at in d.STRIPS[name]:
                assert box[3] < 1440, (name, box)                  # never the status rows
                assert k >= 2.0, (name, k)
                w, h = (box[2] - box[0]) * k, (box[3] - box[1]) * k
                assert at[0] >= 40 and at[0] + w <= 2840 and at[1] >= 160 and at[1] + h <= 1760, (name, box)
    assert 'its reply (excerpts)' in texts('st-A1a.png')


def test_tile_labels_on_the_refilmed_cups(drawn):
    """take S re-filmed (bef6515): left "fixed" cup x 812-1430, y 475-1500; right "name" cup x 1918-2685, y 563-1425.
    Each label centred over its cup and above its rim."""
    for key, (x0, x1, y0, _y1) in d.TILE_CUPS.items():
        box = d.DRAWN[f'ov-tile-0.png:{key}']
        assert abs((box[0] + box[2]) / 2 - (x0 + x1) / 2) <= 20, key
        assert box[3] <= y0, key
    assert texts('ov-tile-0.png')[:2] == ['60 across', '120 across']


def test_c6_cause_chip_under_the_120_cup(drawn):
    """fc18 cut 6 (REVIEW-watch-fc18-c5 0:00): the red "width 60: cup 120 across" chip sat under the 60 cup (x 40);
    it now sits centred under the 120 cup, below its base, clear of the left cup."""
    x0, x1, _y0, y1 = d.TILE_CUPS['120']
    box = d.DRAWN['ov-tile-0.png:cause']
    assert abs((box[0] + box[2]) / 2 - (x0 + x1) / 2) <= 20
    assert box[1] > y1 and box[0] > d.TILE_CUPS['60'][1] and box[2] <= 2840


def test_c5_coming_up_builds(drawn):
    """fc18 cut 5 (REVIEW-watch-fc18-c4: 17.5 s idle under the Coming up bar): the Coming up panel builds a third line
    when the voice says "driving SolidCraft and FreeCAD, tested against Claude" (sub-3 = sub-1 + one line, the panel
    grows downward so the first two lines stay put)."""
    assert d.SUB3[:2] == d.SUB[0] and len(d.SUB3) == 3
    assert texts('sub-3.png') == d.SUB3 and texts('sub-1.png') == d.SUB[0]
    assert Image.open(os.path.join(d.OUT, 'sub-3.png')).size == (2880, 1800)
