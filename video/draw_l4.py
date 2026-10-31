"""Lesson 4's diagram cards (2560 x 1440, text 56 px or more). Diagrams are visibly diagrams (flat shapes, no fake UI);
every number comes from the tested checker (checker/holes.py expected) or a lab file.
Pegs: a pencil mark on a shelf ("10 from the left edge" vs "half the width") = a position written from names; sanding
a table corner = a fillet.
    docker run --rm --network none -v "<lab>:/work" -w /work cad3way-draw:1 python3 video/draw_l4.py [compare]
"""
import json
import math
import os
import sys

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, LAB)
sys.path.insert(0, os.path.join(LAB, 'video'))
from checker import holes  # noqa: E402
from draw_l2 import AMBER, BG, BLUE, GREEN, GREY, INK, PAPER, RED, R, W, canvas, chip, header, text  # noqa: E402,F401

OUT = os.path.join(LAB, 'video', 'frames-l4')
os.makedirs(OUT, exist_ok=True)
WOOD = (222, 184, 135)
WOOD_D = (160, 120, 80)
PLATE = (176, 190, 212)


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(name)


def card_today(kind):
    """F2 inserts: a screw through the back plate into a wall; a table corner sanded round."""
    im, d = canvas()
    if kind == 'hole':
        header(d, 'A hole for a screw')
        d.rectangle((300, 250, 520, 1250), fill=(214, 211, 204), outline=GREY, width=6)      # the wall
        text(d, (410, 1300), 'wall', 64, GREY, anchor='ma')
        d.rectangle((520, 350, 640, 1150), fill=PLATE, outline=INK, width=7)                 # the back plate, side view
        d.rectangle((520, 1050, 1300, 1150), fill=PLATE, outline=INK, width=7)               # the arm
        d.rectangle((1220, 900, 1300, 1150), fill=PLATE, outline=INK, width=7)               # the lip
        d.rectangle((520, 560, 640, 620), fill=BG)                                           # the hole, cut through
        d.rectangle((640, 545, 670, 635), fill=INK)                                          # the screw head
        d.rectangle((330, 580, 640, 600), fill=INK)                                          # the shank into the wall
        text(d, (820, 590), 'a hole through the back plate', 68, BLUE, anchor='lm')
        text(d, (820, 690), 'so a screw holds the hook', 68, BLUE, anchor='lm')
    else:
        header(d, 'A fillet: a sanded corner')
        for k, (ox, rounded) in enumerate(((330, False), (1420, True))):
            top, side = 520, 1100
            if rounded:
                r = 170
                cxr, cyr = ox + 820 - r, top + r
                arc = [(cxr + r * math.cos(math.radians(a)), cyr - r * math.sin(math.radians(a))) for a in range(90, -1, -5)]
                d.polygon([(ox, side), (ox, top)] + arc + [(ox + 820, side)], fill=WOOD, outline=WOOD_D, width=8)
                text(d, (ox + 410, 1180), 'sanded round', 68, GREEN, anchor='ma')
            else:
                d.rectangle((ox, top, ox + 820, side), fill=WOOD, outline=WOOD_D, width=8)
                d.ellipse((ox + 780, top - 40, ox + 860, top + 40), outline=RED, width=10)
                text(d, (ox + 410, 1180), 'a sharp corner', 68, RED, anchor='ma')
        chip(d, (W / 2, 1320), 'FreeCAD: Fillet rounds a sharp edge', 58, PAPER, INK, anchor='m')
    save(im, f'card-today-{kind}.png')


def board(d, x0, y0, width_px, mark):
    """A shelf board seen from the front with one pencil mark (mark = 'left' at 10 units, 'half')."""
    d.rectangle((x0, y0, x0 + width_px, y0 + 160), fill=WOOD, outline=WOOD_D, width=8)
    k = 20
    x = x0 + (10 * k if mark == 'left' else width_px / 2)
    d.line((x, y0 - 30, x, y0 + 190), fill=INK, width=8)
    return x


def card_pencil(step):
    """F3, one step per sentence: 1 a mark "10 from the left edge"; 2 the same mark on a wider board, off to one side;
    3 "half the width" on both boards, still in the middle; 4 the lesson 3 word (an expression)."""
    im, d = canvas(); header(d, 'Marking a screw hole with a pencil')
    board(d, 300, 330, 400, 'left')
    text(d, (300, 560), '"10 from the left edge"', 64, INK)
    if step >= 2:
        board(d, 300, 900, 600, 'left')
        text(d, (300, 1130), 'wider board: off to one side', 64, RED)
    if step >= 3:
        board(d, 1500, 330, 400, 'half')
        text(d, (1500, 560), '"half the width"', 64, INK)
        board(d, 1400, 900, 600, 'half')
        text(d, (1400, 1130), 'wider board: still in the middle', 64, GREEN)
    if step >= 4:
        chip(d, (W / 2, 1320), 'lesson 3: a size written from names = an expression', 56, PAPER, INK, anchor='m')
    save(im, f'card-pencil-{step}.png')


def card_rules(step):
    """F9: the plate from the back (20 x 60), the origin dot; 1 across = width / 2; 2 the 60 bar split 15 / 30 / 15;
    3 lower = (60 - 30) / 2 = 15; 4 upper = 15 + 30 = 45 = (60 + 30) / 2."""
    im, d = canvas(); header(d, 'The pencil marks, written as rules')
    s, ox, oy = 17, 520, 1290          # 20 x 60 mm at 17 px/mm
    d.rectangle((ox, oy - 60 * s, ox + 20 * s, oy), fill=PLATE, outline=INK, width=7)
    d.ellipse((ox - 16, oy - 16, ox + 16, oy + 16), fill=RED)
    text(d, (ox - 30, oy + 20), 'start', 52, RED, anchor='ra')
    for z in (15, 45):
        cx, cy = ox + 10 * s, oy - z * s
        d.ellipse((cx - 2 * s, cy - 2 * s, cx + 2 * s, cy + 2 * s), outline=INK, width=6)
    tx = 1150
    if step >= 1:
        d.line((ox, oy - 15 * s, ox + 10 * s, oy - 15 * s), fill=BLUE, width=7)
        text(d, (tx, 300), 'across: width / 2 = 20 / 2 = 10', 70, BLUE)
    if step >= 2:
        bx = ox - 90
        for a, b, col, lab in ((0, 15, GREEN, '15'), (15, 45, AMBER, '30 apart'), (45, 60, GREEN, '15')):
            d.line((bx, oy - a * s + 6, bx, oy - b * s - 6), fill=col, width=14)
            text(d, (bx - 20, oy - (a + b) / 2 * s), lab, 56, col, anchor='rm')
        text(d, (tx, 440), 'up: 60 tall − 30 apart = 30 left', 70, INK)
        text(d, (tx, 540), '= two gaps of 15', 70, GREEN)
    if step >= 3:
        text(d, (tx, 720), 'lower: (60 − 30) / 2 = 15', 70, INK)
    if step >= 4:
        text(d, (tx, 860), 'upper: 15 + 30 = 45', 70, INK)
        text(d, (tx, 960), '= (60 + 30) / 2', 70, AMBER)
        chip(d, (W / 2 + 300, 1300), 'four rules: across and up, for each circle', 56, PAPER, INK, anchor='m')
    save(im, f'card-rules-{step}.png')


def card_expected(kind):
    """F16 (build) and F17 (30 wide): the number worked out first, from checker/holes.expected."""
    w = 20 if kind == 'build' else 30
    e = holes.expected(dict(holes.NAMES, width=w))
    hole = 2 * math.pi * 2 ** 2 * 5
    fil = (4 - math.pi) * w
    im, d = canvas(); header(d, 'Worked out first' + (': 30 wide' if w == 30 else ''))
    # the corner sliver: a 2 x 2 square minus a quarter circle
    cx, cy, s = 360, 900, 150
    d.rectangle((cx, cy - 2 * s, cx + 2 * s, cy), fill=AMBER, outline=INK, width=5)
    d.pieslice((cx - 2 * s, cy - 2 * s, cx + 2 * s, cy + 2 * s), 270, 360, fill=PLATE, outline=INK, width=5)
    text(d, (cx + s, cy + 40), 'the corner a 2 mm fillet', 50, GREY, anchor='ma')
    text(d, (cx + s, cy + 100), 'shaves off: 2 x 2 − ¼ circle', 50, GREY, anchor='ma')
    tx = 1000
    rows = [('start' if w == 20 else 'the hook, 30 wide', '%s' % ('10,000' if w == 20 else '15,000'), INK),
            ('2 holes · r 2 · 5 thick', '− %.2f' % hole, BLUE),
            ('fillet: (4 − π) x %d long' % w, '− %.2f' % fil, AMBER)]
    if w == 20:
        rows[0] = ("lesson 3's hook", '10,000', INK)
    for k, (a, b, col) in enumerate(rows):
        text(d, (tx, 300 + k * 150), a, 64, col)
        text(d, (2450, 300 + k * 150), b, 72, col, anchor='ra')
    y = 300 + 3 * 150 + 20
    d.line((tx, y, 2450, y), fill=INK, width=6)
    text(d, (2450, y + 40), '= %s mm³' % format(round(e['volume_mm3'], 2), ',.2f'), 110, RED, anchor='ra')
    save(im, f'card-expected-{kind}.png')


def card_edge():
    """F20: edge names. Edge10 = a plain-number mark; FreeCAD 1.x adds a history name; 'not completely solved'."""
    im, d = canvas(); header(d, 'The fillet is stored on "Edge10"')
    rows = [('Edge10: a number, like "10 from the left"', INK),
            ('the shape changes → the count can change', RED),
            ('FreeCAD 1.x: also a name from the part\'s history', BLUE),
            ('it finds the edge again, or flags it', BLUE),
            ('FreeCAD\'s notes: "not completely solved"', GREY)]
    for k, (a, col) in enumerate(rows):
        text(d, (260, 300 + k * 170), a, 72, col)
    save(im, 'card-edge.png')


def card_recap(step):
    """F28: 1 the pencil mark, 2 the Hole drills at each centre, 3 the sanded corner with 'edge 10?'."""
    im, d = canvas(); header(d, 'Remember')
    items = [('a pencil mark: half the width', 'stays in the middle of any board', GREEN),
             ('the Hole tool drills', 'at each circle\'s centre', BLUE),
             ('a fillet sands one edge', 'its name can change: check after a change', AMBER)]
    for k in range(step):
        a, b, col = items[k]
        y = 300 + k * 330
        d.rounded_rectangle((260, y, 2300, y + 270), radius=24, fill=PAPER, outline=col, width=7)
        text(d, (320, y + 50), a, 76, col)
        text(d, (320, y + 160), b, 60, INK)
    save(im, f'card-recap-{step}.png')


def card_compare():
    """F25: by hand / with the sentence (two runs) / without, from out/l4/compare.json."""
    c = json.load(open(os.path.join(LAB, 'out', 'l4', 'compare.json'), encoding='utf-8'))
    im, d = canvas(); header(d, 'Side by side')
    cols = [('by hand', 820), ('with the sentence', 1440), ('without', 2100)]
    for name, x in cols:
        text(d, (x, 230), name, 60, GREY, anchor='ma')
    for k, row in enumerate(c['rows']):
        y = 340 + k * 190
        text(d, (120, y), row['label'], 56, INK)
        for (name, x), cell in zip(cols, row['cells']):
            ok = cell.get('ok')
            text(d, (x, y), cell['text'], 56, GREEN if ok else (RED if ok is False else INK), anchor='ma')
    if c.get('replay'):
        chip(d, (W / 2, 1330), c['replay'], 54, PAPER, INK, anchor='m')
    save(im, 'card-compare.png')


def thumbs():
    """Thumbnails (1280 x 720) from the real frames: the by-hand back view after 30 wide (holes centred) beside the
    plain one (off to one side), under 4 words; the alt names the Claude finding."""
    from PIL import Image
    a = Image.open(os.path.join(LAB, 'out', 'l4', 'hand', 's18-back30.png')).crop((700, 330, 1420, 1330))
    b = Image.open(os.path.join(LAB, 'out', 'l4', 'plain', 's2-back30.png')).crop((1920, 330, 2640, 1330))
    for name, title, sub in (('thumb-primary.png', '30 WIDE: CENTRED?', ('FROM NAMES', 'PLAIN 10')),
                             ('thumb-altA.png', 'SAME CHANGE, TWO RESULTS', ('15 · 15', '10 · 20'))):
        im, d = canvas(1280, 720)
        d.rectangle((0, 0, 1280, 150), fill=INK)
        text(d, (640, 75), title, 92, PAPER, anchor='mm')
        for k, (src, col, lab) in enumerate(((a, GREEN, sub[0]), (b, RED, sub[1]))):
            t = src.resize((360, 500))
            x = 140 + k * 640
            im.paste(t, (x, 175))
            d.rectangle((x - 6, 169, x + 366, 681), outline=col, width=10)
            chip(d, (x + 180, 640), lab, 54, PAPER, col, anchor='m')
        save(im, name)


if __name__ == '__main__':
    if sys.argv[1:] == ['thumbs']:
        thumbs()
    elif sys.argv[1:] == ['compare']:
        card_compare()
    else:
        card_today('hole'); card_today('fillet')
        for i in (1, 2, 3, 4):
            card_pencil(i)
        for i in (1, 2, 3, 4):
            card_rules(i)
        card_expected('build'); card_expected('w30')
        card_edge()
        for i in (1, 2, 3):
            card_recap(i)
