"""fc17 cards, overlays and stills (FreeCAD course lesson 17, the second key peg by Mirror: Base XZ-plane sends the copy
out of the back, Base YZ-plane is the fold between the two pegs; SCRIPT-fc17.md rev 2 sections 0.1, 1 and 3,
SCRIPT-fc17-short.md): every named file drawn at its size, card lines 44 columns at most, panels / chips / Short lines
32, the panel titles, no "A1" / "B1" / "body" / "shell" / "proud" / percent sign in any drawn text, the end card without
angle brackets, the diagrams put the origin at the cup's middle and the copies where the script says.
Run in the draw image:
MSYS_NO_PATHCONV=1 docker run --rm -v "<edu-visualization>:/ev" -w /ev/freecad-course-lab cad3way-draw:1 \
  python3 -m pytest -q -p no:cacheprovider tests/test_draw_fc17.py"""
import os
import re
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fc17 as d  # noqa: E402

CARDS = ([f'card-fold-{i}.png' for i in range(1, 5)] + [f'card-names-{i}.png' for i in range(1, 4)] +
         [f'card-top-{i}.png' for i in range(1, 7)] + [f'card-axis-{i}.png' for i in range(1, 4)] + ['card-centred-1.png', 'card-end.png'])
SHORT = ['card-why-s1a.png', 'card-why-s1b.png', 'card-why-s1.png', 'card-why-s2.png', 'card-why-s3.png']
SHORT_OV = ['card-short-head.png', 'short-head.png', 'short-q.png', 'short-series.png']
PANELS = ['ov-in-F1.png', 'ov-in-F5.png', 'ov-in-F8.png', 'ov-in-F9.png', 'ov-in-K1.png', 'ov-in-K2.png',
          'ov-in-K3.png', 'ov-sk-F4.png', 'ov-cc-A1.png', 'ov-cc-B1.png',
          'ov-in-F8a.png', 'ov-in-F9a.png', 'ov-in-K1a.png', 'ov-sk-F4a.png']   # cut 2: the first build of each
CHIPS = ['ov-chip-run-A1.png', 'ov-chip-run-B1.png', 'ov-chip-cc-version.png']
LOWER = ['sub-1.png', 'sub-2.png', 'rc-1.png', 'rc-2.png', 'yt-1.png']
STILLS = ['st-A1.png', 'st-A1z.png', 'st-B1f.png', 'st-B1b.png']
ALL = CARDS + SHORT + SHORT_OV + PANELS + CHIPS + LOWER + STILLS


@pytest.fixture(scope='module')
def run():
    d.main()
    return d.LOG


def texts(log, name):
    return [t for t, _ in log[name]]


def alltext(log):
    return ' | '.join(t for rows in log.values() for t, _ in rows)


def alpha_in(name, box):
    return Image.open(os.path.join(d.OUT, name)).getchannel('A').crop(box).getbbox() is not None


def hit(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def test_all_drawn(run):
    for n in ALL:
        assert n in run, n
        assert os.path.exists(os.path.join(d.OUT, n)), n
    assert d.PROBLEMS == []


def test_sizes(run):
    for n in CARDS:
        im = Image.open(os.path.join(d.OUT, n)).convert('RGB')
        assert im.size == (2560, 1440), n
        assert sum(im.resize((1, 1)).getpixel((0, 0))) / 3 > 200, n
    for n in SHORT:
        assert Image.open(os.path.join(d.OUT, n)).size == (1080, 1080), n
    for n in SHORT_OV:
        im = Image.open(os.path.join(d.OUT, n))
        assert im.size == (1080, 1920) and im.mode == 'RGBA', n
    for n in STILLS:
        assert Image.open(os.path.join(d.OUT, n)).size == (2880, 1800), n
    for n in PANELS + CHIPS + LOWER:
        im = Image.open(os.path.join(d.OUT, n))
        assert im.size == (2880, 1800) and im.mode == 'RGBA', n


def test_columns_and_words(run):
    for n, rows in run.items():
        for t, _ in rows:
            low = t.lower()
            assert '%' not in low, (n, t)
            for bad in ('body', 'shell', 'proud', 'a1', 'b1'):
                assert not re.search(rf'\b{bad}\b', low), (n, t)
            lim = 44 if n.startswith(('card-fold', 'card-names', 'card-top', 'card-axis', 'card-centred',
                                      'card-end', 'st-', 'rc', 'yt', 'sub')) else 32
            for ln in t.split('\n'):
                assert len(ln) <= lim, (n, ln)


def test_panel_titles(run):
    for n in PANELS:
        title = "the peg's sketch (lesson 14)" if n.startswith('ov-sk-F4') else 'checked by code'
        assert texts(run, n)[0] == title, n
    for n in ('st-A1z.png', 'st-B1f.png', 'st-B1b.png'):
        assert 'checked by code' in texts(run, n), n


def test_panel_lines_exact(run):
    want = {
        'ov-in-F1.png': ['2 pegs on the front', 'back clear'],
        'ov-in-F5.png': ['copy at y 20 to 35: behind', 'front: 1 peg · one solid', 'no message, no mark'],
        'ov-in-F8a.png': ['pegs x 10 to 20, −20 to −10'],
        'ov-in-F8.png': ['pegs x 10 to 20, −20 to −10', '15 + 15 = 30 centre to centre'],
        'ov-in-F9a.png': ['sketch axis = Base YZ'],
        'ov-in-F9.png': ['sketch axis = Base YZ', 'same part, same volume'],
        'ov-in-K1a.png': ['peg_x 20: 40 centre to centre'],
        'ov-in-K1.png': ['peg_x 20: 40 centre to centre', '30 between them'],
        'ov-in-K2.png': ['wall 3: one solid', '58 front to back, back clear'],
        'ov-in-K3.png': ['fixed file, peg_x 20: copy −20', 'XZ file, peg_x 20: copy behind'],
        'ov-sk-F4a.png': ['drawn on the XZ plane'],
        'ov-sk-F4.png': ['drawn on the XZ plane', 'so XZ looks right. It is not.'],
        'ov-cc-A1.png': ['its file: peg_x 15, 20, 8', 'and wall 3:', '2 pegs front, back clear'],
        'ov-cc-B1.png': ['its file: peg_x 15, 20, 8', 'and wall 3: passed', 'pegs stick out 13',
                         'hanging hole: back wall'],
    }
    for n, lines in want.items():
        assert texts(run, n)[1:] == lines, n


def test_key_words_drawn(run):
    allt = alltext(run)
    for s in ['fold down the middle', 'copy beside it', 'wrong crease: wrong place', 'the crease sits between them',
              'x: − left, + right · z up', 'y: − front, + back', 'x: − left, + right', 'y: − front, + back · z up',
              'the paper, seen from above', 'peg centre: x 15, y −27.5', 'its end: y −35', '27.5 in front → 27.5 behind', 'the crease across → top right',
              '15 right → 15 left', 'missing letter flips; the other two stay', 'XZ → y flips', 'YZ → x flips',
              "the sketch's", 'vertical axis', 'same plane here', 'centred in lesson 14', 'front → back · 13 out', 'missing letter flips',
              'not asked to check · $0.15', 'asked to check · $0.12', 'Claude Code 2.1.308 · Sonnet 5.5',
              'Lesson 18: a round pen cup', 'comes out twice as wide', 'Every fix tested in both programs,',
              'by hand and with Claude · Subscribe', 'Plane = crease halfway between', 'YZ: x is missing, so x flips',
              'Your turn: cup with its corner', 'on the origin, inside x 0 to 60,', 'peg at x 45. Mirror across YZ:',
              'where? On the cup?', 'Where must the fold be for x 15?', 'MY MIRRORED PEG', 'CAME OUT THE BACK',
              'Peg at x 25, mirror across YZ:', 'where does the copy land?', 'Full lesson: FreeCAD plus',
              'Claude course, lesson 17', 'Subscribe', 'its file, front (still)', 'its file, back (still)',
              'its file, saved by our kit', 'after the run (still)']:      # one chip, two lines (32 columns)
        assert s in allt, s


def test_builds_add(run):
    for s, k in (('card-fold', 4), ('card-top', 6), ('rc', 2), ('card-why-s', 3)):
        for i in range(2, k + 1):
            prev = set(texts(run, f'{s}-{i - 1}.png' if s != 'card-why-s' else f'card-why-s{i - 1}.png'))
            cur = set(texts(run, f'{s}-{i}.png' if s != 'card-why-s' else f'card-why-s{i}.png'))
            if s in ('card-fold', 'card-why-s') and i in (2, 3, 4):
                continue        # chips swap per build (one picture each); checked below
            assert prev <= cur, (s, i, prev - cur)
    assert '15 right → 15 left' in texts(run, 'card-why-s3.png')
    assert 'missing letter flips' in texts(run, 'card-why-s3.png')
    assert 'missing letter flips' not in texts(run, 'card-why-s2.png')
    assert 'front → back · 13 out' in texts(run, 'card-why-s1.png')


def test_short_xz_card_builds_without_27_5(run):
    """Short cut 2 (REVIEW-watch-fc17-short-c1 must-fix 2): the XZ card builds (plane + peg, + the path, + the copy
    and 13 out) and never shows the unspoken 27.5."""
    a, b, c = (set(texts(run, f'card-why-{n}.png')) for n in ('s1a', 's1b', 's1'))
    assert 'XZ' in a and '13 out' not in a and '13 out' not in b and '13 out' in c
    assert a <= b <= c
    for n in ('s1a', 's1b', 's1', 's2', 's3'):
        assert not any('27.5' in t for t in texts(run, f'card-why-{n}.png')), n
    from PIL import ImageChops
    im = [Image.open(os.path.join(d.OUT, f'card-why-{n}.png')).convert('RGB') for n in ('s1a', 's1b', 's1')]
    assert ImageChops.difference(im[0], im[1]).getbbox() and ImageChops.difference(im[1], im[2]).getbbox()


def test_axis_key_every_names_and_top_card(run):
    for n in [f'card-names-{i}.png' for i in (1, 2, 3)] + [f'card-top-{i}.png' for i in range(1, 7)]:
        t = texts(run, n)
        assert 'x: − left, + right · z up' in t and 'y: − front, + back' in t, n
    for n in SHORT:
        t = texts(run, n)
        assert 'x: − left, + right' in t and 'y: − front, + back · z up' in t, n


def test_geometry_origin_in_the_middle():
    """The diagrams' origin is the cup's middle (lesson 14 centred it), never a corner; the copies land where the
    script says: XZ sends y −27.5 to +27.5, YZ sends x 15 to −15."""
    cx = (d.T(-32, 0)[0] + d.T(32, 0)[0]) / 2
    cy = (d.T(0, -22)[1] + d.T(0, 22)[1]) / 2
    assert d.T(0, 0) == (cx, cy)
    assert d.mirror((15, -27.5), 'XZ') == (15, 27.5)
    assert d.mirror((15, -27.5), 'YZ') == (-15, -27.5)
    assert d.ORIGIN_3D == (0, 0, 0)


def test_end_card(run):
    t = texts(run, 'card-end.png')
    assert not any('<' in x or '>' in x for x in t)
    allt = ' | '.join(t)
    assert 'Lesson 16' in allt and 'playlist' in allt and 'Subscribe' in allt and 'comparison' in allt
    im = Image.open(os.path.join(d.OUT, 'card-end.png')).convert('L').crop((0, 1300, 2560, 1440))
    assert im.getextrema()[0] > 240          # the AI-voice label band stays empty


def test_claude_panels_off_the_terminal(run):
    for n in ('ov-cc-A1.png', 'ov-cc-B1.png') + tuple(CHIPS):
        assert not alpha_in(n, (0, 0, d.CC_RIGHT, 1800)), n
        assert not alpha_in(n, (0, 1700, 2880, 1800)), n


def test_panels_off_the_cup_middle(run):
    for n in PANELS[:8]:
        assert not hit(d.DRAWN[n], d.CUP_MIDDLE), (n, d.DRAWN[n])
        assert not alpha_in(n, (0, 0, 2880, d.TOP_BAND)), n


def test_stills_panel_beside(run):
    assert not hit(d.DRAWN['st-A1z.png:panel'], d.DRAWN['st-A1z.png:crop'])
    for s in ('f', 'b'):
        assert not hit(d.DRAWN[f'st-B1{s}.png:panel'], d.CUP_STILL), s
    assert 'its file, front (still)' in texts(run, 'st-A1z.png')
    assert 'its file, back (still)' in texts(run, 'st-B1b.png')


def test_short_head(run):
    assert texts(run, 'card-short-head.png') == ['MY MIRRORED PEG', 'CAME OUT THE BACK']
    assert alpha_in('card-short-head.png', (0, 0, 1080, 300))


def test_no_answers(run):
    t = ' | '.join(texts(run, 'yt-1.png'))
    assert '−45' not in t and '30' not in t
    assert '−25' not in ' | '.join(texts(run, 'short-q.png'))


def test_fold_labels_do_not_overlap_in_the_dissolve(run):
    """cut 2 (f021): card-fold-3's chip and card-fold-4's chip sat in the same place, so the 0.35 s dissolve
    showed one over the other."""
    assert not hit(d.FOLD_CHIPS[3], d.FOLD_CHIPS[4]), d.FOLD_CHIPS
