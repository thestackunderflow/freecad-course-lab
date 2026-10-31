"""Lesson 6's diagram cards (2560 x 1440, text 56 px or more). Diagrams are visibly diagrams (flat shapes, no fake UI);
every number comes from a lab file (out/l6/hand/read-*.json, out/l6/compare.json). Pegs: a must-stay-true list = a
haircut ticket ("2 cm off the back, keep the fringe", then the mirror); Measure = FreeCAD's own tape measure; the pass
rule = an answer key written before the marking.
    docker run --rm --network none -v "<lab>:/work" -w /work cad3way-draw:1 python3 video/draw_l6.py [table|thumbs]
"""
import json
import os
import sys

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, LAB)
sys.path.insert(0, os.path.join(LAB, 'video'))
from draw_l2 import BG, BLUE, GREEN, GREY, INK, PAPER, RED, W, canvas, chip, header, j_poly, text  # noqa: E402

OUT = os.path.join(LAB, 'video', 'frames-l6')
os.makedirs(OUT, exist_ok=True)
L6 = os.path.join(LAB, 'out', 'l6')
PLATE = (176, 190, 212)
HAIR = (120, 84, 52)
SKIN = (238, 206, 178)
TICKET = (255, 250, 228)


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(name)


def read(name):
    return json.load(open(os.path.join(L6, 'hand', f'read-{name}.json'), encoding='utf-8'))


def head(d, cx, cy, r, trimmed=False):
    """A simple head from behind: hair, the back cut shorter when trimmed."""
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=SKIN, outline=INK, width=6)
    low = cy + (0.15 if trimmed else 0.75) * r
    d.chord((cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12), 180, 360, fill=HAIR, outline=INK, width=6)
    d.rectangle((cx - r - 6, cy, cx + r + 6, low), fill=HAIR, outline=INK, width=6)


def card_haircut(step):
    """F2, three reveals: the ticket's change; what to keep; the mirror check."""
    im, d = canvas(); header(d, 'A change, and what must stay true')
    head(d, 520, 760, 230, trimmed=step >= 3)
    text(d, (520, 1060), 'the back', 60, GREY, anchor='ma')
    d.rectangle((1000, 300, 2350, 1120), fill=TICKET, outline=INK, width=6)
    text(d, (1060, 340), 'the ticket', 58, GREY)
    text(d, (1060, 450), 'change: 2 cm off the back', 66, BLUE)
    if step >= 2:
        text(d, (1060, 600), 'keep: the fringe', 66, GREEN)
        text(d, (1060, 690), 'keep: the sides', 66, GREEN)
    if step >= 3:
        text(d, (1060, 860), 'then: check in the mirror', 66, INK)
        chip(d, (W / 2, 1300), 'a model change needs the same: a must-stay-true list', 54, PAPER, INK, anchor='m')
    save(im, f'card-haircut-{step}.png')


def side_j(d, ox, oy, s, depth, label_opening):
    """The hook from the side (the J), plate at the left, with the bracket for hook_depth."""
    from draw_l2 import J  # noqa: F401  (the course's J outline at depth 25; drawn here at any depth)
    t, lip, ph = 5, 10, 60
    pts = [(0, 0), (depth, 0), (depth, lip), (depth - t, lip), (depth - t, t), (t, t), (t, ph), (0, ph)]
    P = [(ox + x * s, oy - z * s) for x, z in pts]
    d.polygon(P, fill=PLATE, outline=INK, width=6)
    y = oy + 60
    d.line((ox, y, ox + depth * s, y), fill=INK, width=5)
    for x in (ox, ox + depth * s):
        d.line((x, y - 22, x, y + 22), fill=INK, width=5)
    text(d, (ox + depth * s / 2, y + 30), 'hook_depth %g' % depth, 58, INK, anchor='ma')
    yy = oy - 7.5 * s
    for a, b, col, lab in ((0, t, BLUE, 'thickness 5'), (t, depth - t, RED if label_opening != depth - 2 * t else GREEN,
                                                          'opening %g' % (depth - 2 * t)),
                           (depth - t, depth, BLUE, 'thickness 5')):
        d.line((ox + a * s + 6, yy, ox + b * s - 6, yy), fill=col, width=7)
    text(d, (ox + depth / 2 * s, yy - 80), 'opening %g' % (depth - 2 * t), 60, GREEN if depth - 2 * t == 45 else RED, anchor='ma')
    text(d, (ox - 20, oy - 2 * s), '5', 56, BLUE, anchor='ra')
    text(d, (ox + depth * s + 20, oy - 2 * s), '5', 56, BLUE)


def card_depth(step):
    """F7, three reveals: hook_depth = wall + opening + wall; 5 + 35 + 5 = 45; 5 + 45 + 5 = 55 (S1 too)."""
    im, d = canvas(); header(d, 'hook_depth: the whole bottom, wall to wall')
    depth = 45 if step < 3 else 55
    side_j(d, 260, 1100, 13.5 if depth == 45 else 11.5, depth, 45)
    if step == 1:
        text(d, (1500, 520), 'plate thickness', 66, BLUE)
        text(d, (1500, 610), '+ the opening', 66, INK)
        text(d, (1500, 700), '+ lip thickness', 66, BLUE)
    if step >= 2:
        text(d, (1500, 520), '5 + 35 + 5 = 45', 80, RED)
        text(d, (1500, 620), 'typed 45: opening 35', 60, GREY)
    if step >= 3:
        text(d, (1500, 790), '5 + 45 + 5 = 55', 80, GREEN)
        text(d, (1500, 890), 'for a 45 opening: 55', 60, GREY)
    save(im, f'card-depth-{step}.png')


def card_key(step):
    """F9, three reveals: written first; the pass = opening 45 + the 7 lines + the volume; read by our script."""
    im, d = canvas(); header(d, 'The pass rule: an answer key, written first')
    d.rectangle((260, 300, 1100, 1180), fill=PAPER, outline=INK, width=6)
    text(d, (300, 340), 'ANSWER KEY', 60, INK)
    for k in range(7):
        y = 470 + k * 95
        d.line((320, y, 1040, y), fill=GREY, width=3)
    text(d, (680, 1110), 'written before the marking', 50, GREY, anchor='ma')
    if step >= 2:
        text(d, (1300, 400), 'PASS =', 70, INK)
        text(d, (1300, 500), 'opening 45', 66, GREEN)
        text(d, (1300, 590), '+ all 7 lines', 66, GREEN)
        text(d, (1300, 680), '+ the volume we worked out', 66, GREEN)
    if step >= 3:
        chip(d, (1300, 900), 'read by our script from the saved file', 54, PAPER, INK)
        chip(d, (1300, 1020), "not from Claude's words", 54, PAPER, RED)
    save(im, f'card-key-{step}.png')


def card_sum():
    """F19: the worked-out volume, from the hand reads (40 and 55)."""
    a, b = read('depth40')['solid']['volume_mm3'], read('depth55')['solid']['volume_mm3']
    im, d = canvas(); header(d, 'The volume, worked out before')
    text(d, (200, 380), 'lesson 5: %s mm³' % f'{a:,.1f}', 76, INK)
    text(d, (200, 540), '+ 15 more mm of base × 5 thick × 30 wide', 66, BLUE)
    text(d, (200, 640), '= + 2,250 mm³', 76, BLUE)
    text(d, (200, 820), 'expected: %s mm³' % f'{a + 2250:,.1f}', 76, INK)
    text(d, (200, 960), 'measured: %s mm³' % f'{b:,.1f}', 76, GREEN if abs(b - a - 2250) < 0.05 else RED)
    save(im, 'card-sum.png')


def card_recap(step):
    """F22, three reveals: the haircut ticket; the tape measure; the answer key."""
    im, d = canvas(); header(d, 'Remember')
    d.rectangle((150, 330, 830, 900), fill=TICKET, outline=INK, width=6)
    text(d, (190, 370), 'change: 1 thing', 56, BLUE)
    text(d, (190, 460), 'keep: the list', 56, GREEN)
    text(d, (490, 960), 'a must-stay-true list', 58, INK, anchor='ma')
    if step >= 2:
        d.rounded_rectangle((1000, 520, 1560, 720), radius=30, fill=(250, 210, 60), outline=INK, width=6)
        for k in range(12):
            x = 1030 + k * 44
            d.line((x, 520, x, 560 + (30 if k % 2 == 0 else 0)), fill=INK, width=4)
        text(d, (1280, 960), 'Measure before + after', 58, INK, anchor='ma')
    if step >= 3:
        d.rectangle((1760, 330, 2400, 900), fill=PAPER, outline=INK, width=6)
        text(d, (1800, 370), 'ANSWER KEY', 56, INK)
        text(d, (2080, 960), 'a pass rule, written first', 58, INK, anchor='ma')
    save(im, f'card-recap-{step}.png')


if __name__ == '__main__':
    for i in (1, 2, 3):
        card_haircut(i); card_depth(i); card_key(i); card_recap(i)
    card_sum()
