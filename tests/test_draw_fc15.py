"""fc15 cards and panels (FreeCAD course lesson 15, a soft rim on the hanging cup: the Fillet has to fit in the wall;
SCRIPT-fc15.md rev 2.1 section 3): every card drawn and light, card lines 44 columns at most, chips / insets /
code-panel lines 32 at most, no percent sign and no "tooltip" / "shell" / "BRep" / "A1" / "B1" in any drawn text,
every number on a card or panel equal to NUMBERS.json (or a lesson / typed number), the your-turn card carries no
answer, the rule never drawn as "anything under the wall builds" / "no more than the wall", the Short cards
1080 x 1080 and the Short headline frame 1080 x 1920 with "FILLET 3 ON A 2 MM WALL:" / "FAILED", the chips with ">"
drawn (never typed into YouTube text), nothing drawn outside its frame.
Run in the draw image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fc15.py"""
import json
import os
import re
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fc15 as d  # noqa: E402

STEPS = {'card-round': 4, 'card-coin': 3, 'card-why': 4, 'card-rule': 3}
CARDS = ([f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)] +
         ['card-end.png', 'still-after-A1.png', 'still-after-B1.png'])
SHORT = ['card-why-s1.png', 'card-why-s2.png', 'card-why-s3.png']
HEAD = 'card-short-head.png'
OVS = ([f'rc-{i}.png' for i in (1, 2, 3)] + ['yt-1.png', 'sub-1.png', 'sub-2.png'] +
       ['ov-rim-R.png', 'ov-box-T.png', 'ov-box-I.png', 'ov-err-P.png', 'ov-flat-F.png', 'ov-chips-T.png',
        'ov-sum-I.png', 'ov-fits-P.png', 'ov-w3-P.png', 'ov-w2-P.png'])
NUM = json.load(open(os.path.join(d.TAKES, 'NUMBERS.json'), encoding='utf-8'))
LESSON = {'0', '1', '2', '3', '4', '14', '15', '16', '1.1.4', '2.1.308', '5.5', '0.22', '0.21', '0.50', '1.50',
          '2.5', '1.5', '1.2', '0.75', '60', '40', '12'}


def nums_ok():
    out = set(LESSON)

    def walk(v):
        if isinstance(v, dict):
            for k, x in v.items():
                walk(x)
                for y in re.findall(r'\d+(?:\.\d+)?', str(k)):
                    out.update({y})
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
    assert len(d.PANEL_NAMES) >= 8


def test_no_problems(run):
    assert d.PROBLEMS == []


def test_cards_light_and_sized(run):
    for n in CARDS:
        im = Image.open(os.path.join(d.OUT, n)).convert('RGB')
        assert im.size == (2560, 1440), n
        assert sum(im.resize((1, 1)).getpixel((0, 0))) / 3 > 200, n
    for n in SHORT:
        im = Image.open(os.path.join(d.OUT, n)).convert('RGB')
        assert im.size == (1080, 1080), n
        assert sum(im.resize((1, 1)).getpixel((0, 0))) / 3 > 200, n
    assert Image.open(os.path.join(d.OUT, HEAD)).size == (1080, 1920)
    for n in OVS + d.PANEL_NAMES:
        assert Image.open(os.path.join(d.OUT, n)).size == (2880, 1800), n


def test_columns_and_words(run):
    for n, rows in run.items():
        for t, _ in rows:
            low = t.lower()
            for bad in ('%', 'tooltip', 'shell', 'brep', 'command not done'):
                assert bad not in low, (n, t)
            assert not re.search(r'\b[ab]1\b', low), (n, t)
            for ln in t.split('\n'):
                lim = 44 if n.startswith(('card', 'still', 'sub', 'ov-quote')) else 32
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
        if n == 'card-end.png':
            continue
        for t, _ in rows:
            for x in re.findall(r'\d+(?:\.\d+)?', re.sub(r'\d+\.\d+\.\d+', '', t)):
                assert x in ok, (n, t, x)


def test_your_turn_no_answer_and_rule_words(run):
    for t in texts(run, 'yt-1.png'):
        assert not re.search(r'\b2\.7\b|\bfails\b(?!\?)|\bbuilds\b(?!,)', t.replace('Builds, or fails?', '')), t
    allt = ' | '.join(t for rows in run.values() for t, _ in rows).lower()
    for bad in ('anything under the wall', 'no more than the wall', 'must fit the wall', 'shell'):
        assert bad not in allt, bad


def test_steps_add(run):
    for s, k in {'rc': 3}.items():
        for i in range(2, k + 1):
            prev = set(texts(run, f'{s}-{i - 1}.png'))
            assert prev <= set(texts(run, f'{s}-{i}.png')), (s, i)


def test_code_panels_big(run):
    for n in d.PANEL_NAMES:
        if n.startswith(('ov-in', 'ov-cc', 'ov-log')):
            assert min(px for _, px in run[n]) >= 50, n      # 63 px drawn, logged at k = 0.8


def test_key_words_drawn(run):
    allt = ' | '.join(t for rows in run.values() for t, _ in rows)
    for s in ('3 > 2', 'round 3, wall 2', '2 − 1.5 = 0.5', '1.5 + 1 = 2.5 > 2', '1.5 + 1 = 2.5, fits 3',
              'room on top: 2', 'round needs: 3', 'rim out + rim in', 'less than the wall', 'no room to land',
              'sharp edge', 'round = Fillet', 'same 2', 'same volume, same faces', 'nothing rounded', 'round 1.50',
              'leftover flat 0.50', 'inside 60 × 40', 'on screen: wall-3 shape, 66 wide', 'wall 2.6: builds, flat 0.10',
              'wall 2.4: fails', 'rounds 0.8 + 0.8', 'flat 0.4', 'rounds 0.9 + 0.9', 'flat 0.2',
              'run 1, wall 3: 1.2 + 1.2', 'run 2, wall 3: 1.35 + 1.35', 'run 1, wall 1.6: 0.64 + 0.64',
              'run 2, wall 1.6: 0.72 + 0.72', '0.8 built, 0.85 failed,', '0.9 built (run 2)',
              'FILLET 3 ON A 2 MM WALL:', 'FAILED', 'Your turn: wall 2.5', 'outside 1.2, inside 1.5',
              'Builds, or fails?', 'both share', 'checked by code', 'from the run log', "Claude's reply, quoted:",
              'It builds for walls from 0.75 mm to 10 mm.'):
        assert s in allt, s


def test_quotes_are_its_words(run):
    """B1's rim_round and 0.75-10 lines scrolled off before the recording's last frame: re-set word for word."""
    assert {'ov-quote-B1a.png', 'ov-quote-B1b.png'} <= set(d.PANEL_NAMES)
    assert any('rim_round = 0.45' in t for t in texts(run, 'ov-quote-B1a.png'))


def test_numbers_match_the_lab():
    g = NUM['G0']
    assert g['params']['rim_out'] == 3.0 and g['params']['wall'] == 2.0 and g['params']['rim_in'] == 1.0
    assert g['fix_r1_5']['flat'] == 0.5 and g['walls']['wall_3_0']['outside_w'] == 66.0
    assert g['walls']['wall_2.6_2']['flat'] == 0.1 and not g['walls']['wall_2.4_3']['builds']
    assert 0.85 in g['q3_scan_refusals_below_limit']['equal']
    a, b_ = NUM['runs']['A1']['check'], NUM['runs']['B1']['check']
    assert a['at_wall2']['round_radii'] == {'out': [0.8], 'in': [0.8]} and a['at_wall2']['flat'] == 0.4
    assert b_['at_wall2']['round_radii'] == {'out': [0.9], 'in': [0.9]} and b_['at_wall2']['flat'] == 0.2


def test_locator_insets(run):
    """fc15 cut 1 (lesson 14/15 gate: the full part before every close-up): every rim close-up carries an inset of the
    whole cup (take R's iso view) with the zoomed spot boxed, top left of the 3D view, clear of the labels and rings."""
    for n, word in (('ov-loc-iso.png', 'close up'), ('ov-loc-top.png', 'from above')):
        assert n in run, n
        im = Image.open(os.path.join(d.OUT, n))
        assert im.size == (2880, 1800)
        x0, y0, x1, y1 = im.getbbox()
        assert x0 >= 480 and y0 >= 300 and x1 <= 1120 and y1 <= 900, (n, im.getbbox())
        assert x1 - x0 >= 380 and y1 - y0 >= 400, n
        assert any(word in t for t in texts(run, n)), n
        r, g, b, a = im.getpixel(d.LOC_MARK)
        assert a > 200 and r > 200 and b < 120, (n, d.LOC_MARK, (r, g, b, a))


def test_quotes_read_as_quotes(run):
    """fc15 cut 1 (lesson 14/15 gate): the re-set reply is a labelled quote, never a look-alike of our code panels."""
    for n in ('ov-quote-B1a.png', 'ov-quote-B1b.png'):
        t = texts(run, n)
        assert t[0] == "Claude's reply, quoted:", t
        assert t[1].startswith('\u201c') and t[-1].endswith('\u201d'), t
        assert not any('checked by code' in x for x in t)


def test_after_stills_show_the_part_big(run):
    """fc15 cut 1 (lesson 14 gate: Claude stills show the result): the cup cropped from its 3D view at 1.0x or more
    (was the whole pane at 0.76x), with a whole-window inset beside it (the full window before a crop)."""
    for r in ('A1', 'B1'):
        assert d.STILL_K[r] >= 1.0, (r, d.STILL_K[r])
        assert 'whole window' in texts(run, f'still-after-{r}.png')


def _said(fn, step, monkeypatch):
    seen = []
    monkeypatch.setattr(d, 'chip_on', lambda _d, _xy, s, *a, **k: seen.append(s))
    monkeypatch.setattr(d, 'text', lambda _d, _xy, s, *a, **k: seen.append(s))
    monkeypatch.setattr(d, 'coin', lambda *a, **k: seen.append('COIN'))
    monkeypatch.setattr(d, 'save', lambda *a, **k: None)
    fn(step)
    return seen


def test_cards_build_one_idea_per_step(monkeypatch):
    """fc15 cut 1 blind review (0:27.5, 0:40): the round card dropped radius 3, "3 > 2" and "same 2" at once, and
    the coin card described a coin in the corner while showing an empty strip. Now: round step 3 = radius 3 + 3 > 2,
    step 4 adds the inside round "same 2"; coin step 1 draws a coin that fits, touching both edges."""
    r3, r4 = _said(d.card_round, 3, monkeypatch), _said(d.card_round, 4, monkeypatch)
    assert '3 > 2' in r3 and 'same 2' not in r3
    assert 'same 2' in r4 and '3 > 2' in r4
    c1 = _said(d.card_coin, 1, monkeypatch)
    assert c1.count('COIN') == 1 and any('both edges' in s for s in c1)


def test_t5_panel_clear_of_the_label(run):
    """fc15 cut 2 watch-through: in Ti (T 79-84.4, FIT, 0.8 scale) the lower label 'by code = ...' starts at about
    source y 1556 and hid the panel's last line 'nothing rounded'; the panel must end above 1500."""
    box = Image.open(os.path.join(d.OUT, 'ov-in-T5.png')).getchannel('A').getbbox()
    assert box[3] <= 1500, box
