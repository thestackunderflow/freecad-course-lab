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
       'ov-in-C.png', 'ov-in-B1.png', 'ov-chip-r120.png', 'ov-chip-r60.png', 'ov-chip-r80.png', 'ov-chip-nodia.png',
       'ov-chip-plane.png', 'ov-chip-far.png', 'ov-chip-cc-version.png', 'ov-chip-run-A1.png', 'ov-chip-run-B1.png',
       'rc-1.png', 'yt-1.png', 'yt-2.png', 'sub-1.png', 'sub-2.png']
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
