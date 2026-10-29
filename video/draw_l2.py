"""Lesson 2's diagram cards (2560 x 1440, text 60 px or more). Diagrams are visibly diagrams (flat shapes, no fake UI);
every number comes from a lab file (out/l2/compare-1.json, hand/measure.json, runs/claude-N/measure.json) or from the
tested outline checker. Adapted from the SolidCraft course lab's lesson 2 cards (the same hook, the same pegs).
    docker run --rm --network none -v "<lab>:/work" -w /work video-qa:2 python3 video/draw_l2.py
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, LAB)
from checker import outline  # noqa: E402

L2 = os.path.join(LAB, 'out', 'l2')
OUT = os.path.join(LAB, 'video', 'frames-l2')
os.makedirs(OUT, exist_ok=True)
FD = '/usr/share/fonts/truetype/dejavu/'
B, R = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf'
BG, INK, RED, GREEN, GREY, BLUE, PAPER, AMBER, WALL = (236, 239, 244), (31, 41, 55), (183, 28, 28), (27, 127, 59), \
    (110, 120, 138), (29, 78, 216), (255, 255, 255), (180, 110, 0), (214, 200, 178)
W, H = 2560, 1440
J = outline.walk(outline.J_MOVES)[:-1]
EXP = outline.expected(outline.J_MOVES, 20)


def font(p, s):
    return ImageFont.truetype(p, s)


def canvas(w=W, h=H, bg=BG):
    im = Image.new('RGB', (w, h), bg)
    return im, ImageDraw.Draw(im)


def text(d, xy, s, size=72, fill=INK, path=B, anchor='la'):
    d.text(xy, s, font=font(path, size), fill=fill, anchor=anchor)


def chip(d, xy, s, size=60, fg=PAPER, bg=INK, pad=22, anchor='l'):
    f = font(B, size)
    w = f.getlength(s)
    x, y = xy
    if anchor == 'm':
        x -= (w + 2 * pad) / 2
    elif anchor == 'r':
        x -= w + 2 * pad
    d.rounded_rectangle((x, y, x + w + 2 * pad, y + size + 2 * pad), radius=22, fill=bg)
    d.text((x + pad, y + pad), s, font=f, fill=fg)


def header(d, s):
    text(d, (W / 2, 100), s, 92, anchor='mm')


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(name)


def j_poly(ox, oy, s, flip=False):
    return [(ox + x * s, oy + (z * s if flip else -z * s)) for x, z in J]


def sheet(d, box):
    x0, y0, x1, y1 = box
    d.rectangle((x0 + 18, y0 + 18, x1 + 18, y1 + 18), fill=(200, 205, 214))
    d.rectangle(box, fill=PAPER, outline=GREY, width=5)


def block(d, ox, oy, s, depth, face=(176, 190, 212), side=(120, 136, 160)):
    dx, dy = depth, -depth * 0.55
    f = j_poly(ox, oy, s)
    back = [(x + dx, y + dy) for x, y in f]
    for i in range(len(f)):
        a, b = f[i], f[(i + 1) % len(f)]
        d.polygon([a, b, back[(i + 1) % len(f)], back[i]], fill=side, outline=INK)
    d.polygon(f, fill=face, outline=INK)


def card_paper():
    """F4: a sketch is a drawing on paper (flat lines, no thickness)."""
    im, d = canvas(); header(d, 'A sketch: a drawing on paper')
    sheet(d, (820, 230, 1740, 1220))
    p = j_poly(1130, 1150, 14)
    d.line(p + [p[0]], fill=INK, width=12, joint='curve')
    d.polygon([(1690, 330), (1830, 190), (1870, 230), (1730, 370)], fill=AMBER)
    d.polygon([(1690, 330), (1730, 370), (1670, 390)], fill=INK)
    save(im, 'card-paper-1.png')
    d.line((1980, 700, 1980, 300), fill=GREEN, width=14)
    d.polygon([(1950, 300), (2010, 300), (1980, 250)], fill=GREEN)
    text(d, (2020, 280), 'top edge', 64, GREEN, anchor='lm')
    text(d, (2020, 360), 'decides which way is up', 52, GREY, R, anchor='lm')
    chip(d, (W / 2, 1270), 'flat lines · no thickness yet', 64, anchor='m')
    save(im, 'card-paper.png')


def card_joutline():
    """F7: the hook from the side, with its sizes."""
    im, d = canvas(); header(d, 'The wall hook, from the side')
    d.rectangle((760, 230, 860, 1330), fill=WALL)
    text(d, (740, 1300), 'wall', 52, GREY, anchor='ra')
    s, ox, oy = 16, 860, 1240
    d.polygon(j_poly(ox, oy, s), fill=(176, 190, 212), outline=INK, width=7)
    text(d, (ox - 130, oy - 30 * s), '60', 92, BLUE, anchor='rm')
    text(d, (ox - 130, oy - 30 * s + 100), 'tall', 64, BLUE, R, anchor='rm')
    d.line((ox + 25 * s + 40, oy, ox + 25 * s + 40, oy - 10 * s), fill=BLUE, width=8)
    text(d, (ox + 25 * s + 70, oy - 5 * s), 'lip 10 high', 72, BLUE, anchor='lm')
    d.line((ox, oy + 40, ox + 25 * s, oy + 40), fill=BLUE, width=8)
    text(d, (ox + 25 * s + 70, oy + 40), 'arm 25 deep', 64, BLUE, anchor='lm')
    text(d, (ox + 5 * s + 40, oy - 42 * s), 'all 5 thick', 72, BLUE, anchor='lm')
    kx, ky = ox + 13 * s, oy - 5 * s
    d.line((kx, ky, kx, ky + 40), fill=AMBER, width=10)
    d.ellipse((kx - 34, ky + 40, kx + 34, ky + 108), outline=AMBER, width=12)
    chip(d, (2440, 1250), 'a flipped J', 64, anchor='r')
    save(im, 'card-joutline.png')


def card_joutline_steps():
    """F7 built in 3 steps: the back plate, then the arm, then the lip (each with its sizes)."""
    s, ox, oy = 16, 860, 1240
    parts = [[(0, 0), (5, 0), (5, 60), (0, 60)], [(5, 0), (20, 0), (20, 5), (5, 5)], [(20, 0), (25, 0), (25, 10), (20, 10)]]
    for step in (1, 2, 3):
        im, d = canvas(); header(d, 'The wall hook, from the side')
        d.rectangle((760, 230, 860, 1330), fill=WALL)
        text(d, (740, 1300), 'wall', 52, GREY, anchor='ra')
        for k in range(step):
            poly = [(ox + x * s, oy - z * s) for x, z in parts[k]]
            d.polygon(poly, fill=[(176, 190, 212), (190, 215, 190), (235, 205, 160)][k], outline=INK, width=6)
        text(d, (ox - 130, oy - 30 * s), '60', 92, BLUE, anchor='rm')
        text(d, (ox - 130, oy - 30 * s + 100), 'tall', 64, BLUE, R, anchor='rm')
        text(d, (ox + 5 * s + 40, oy - 42 * s), 'back plate: 5 thick', 64, BLUE, anchor='lm')
        if step >= 2:
            d.line((ox, oy + 40, ox + 25 * s, oy + 40), fill=BLUE, width=8)
            text(d, (ox + 25 * s + 70, oy + 20), 'arm: 25 deep, 5 thick', 64, BLUE, anchor='lm')
        if step >= 3:
            d.line((ox + 25 * s + 40, oy, ox + 25 * s + 40, oy - 10 * s), fill=BLUE, width=8)
            text(d, (ox + 25 * s + 70, oy - 5 * s - 40), 'lip: 10 high', 64, BLUE, anchor='lm')
            kx, ky = ox + 13 * s, oy - 5 * s
            d.line((kx, ky, kx, ky + 40), fill=AMBER, width=10)
            d.ellipse((kx - 34, ky + 40, kx + 34, ky + 108), outline=AMBER, width=12)
            chip(d, (2440, 1250), 'a J facing the other way', 60, anchor='r')
        save(im, f'card-joutline-{step}.png')


def card_pad():
    """F14: Pad pushes the drawing out of the paper into a solid."""
    im, d = canvas(); header(d, 'Pad: push it out of the paper')
    sheet(d, (1100, 260, 1900, 1230))
    p = j_poly(1380, 1160, 13)
    d.line(p + [p[0]], fill=GREY, width=7)
    block(d, 1020, 1240, 13, -230)
    text(d, (500, 700), '20 mm', 92, RED)
    text(d, (500, 810), 'toward you', 64, RED, R)
    chip(d, (2440, 300), 'a flat drawing → a solid', 64, anchor='r')
    save(im, 'card-pad.png')


def card_sum(step):
    """F18: work it out first, built one rectangle at a time (step 1-4)."""
    im, d = canvas(); header(d, 'Work it out first')
    s, ox, oy = 17, 260, 1330
    rects = [((0, 0, 5, 60), (176, 190, 212)), ((5, 0, 25, 5), (190, 215, 190)), ((20, 5, 25, 10), (235, 205, 160))]
    for k, ((x0, z0, x1, z1), c) in enumerate(rects):
        fill = c if k < step else BG
        d.rectangle((ox + x0 * s, oy - z1 * s, ox + x1 * s, oy - z0 * s), fill=fill, outline=INK, width=6)
    tx = 1000
    lines = [('5 x 60 = 300', INK, 'the back plate'), ('20 x 5 = 100', GREEN, "the arm: 25 minus the plate's 5"),
             ('5 x 5 = 25', AMBER, "the lip: 10 minus the arm's 5")]
    for k, (a, col, why) in enumerate(lines[:step]):
        text(d, (tx, 300 + k * 200), a, 92, col)
        text(d, (tx, 400 + k * 200), why, 56, GREY, R)
    if step >= 4:
        d.line((tx, 920, 2400, 920), fill=INK, width=6)
        text(d, (tx, 960), f"{EXP['area_mm2']:.0f} mm²  x 20 mm", 92, INK)
        text(d, (tx, 1100), f"= {EXP['volume_mm3']:,.0f} mm³", 110, RED)
    save(im, f'card-sum-{step}.png')


def card_recap(step):
    """F31: the four pictures, one more per sentence (1-4); 5 adds the measured results."""
    im, d = canvas(); header(d, 'Remember four pictures')
    xs = [330, 950, 1570, 2190]
    if step >= 1:
        sheet(d, (170, 300, 490, 700))
        p = j_poly(270, 660, 6); d.line(p + [p[0]], fill=INK, width=7)
        d.line((460, 420, 460, 330), fill=GREEN, width=10); d.polygon([(440, 330), (480, 330), (460, 300)], fill=GREEN)
        text(d, (xs[0], 760), 'sketch = paper', 56, anchor='ma'); text(d, (xs[0], 840), 'its top edge: up', 48, GREY, R, anchor='ma')
    if step >= 2:
        p = j_poly(840, 660, 6); d.line(p + [p[0]], fill=INK, width=7)
        for x, y in ((840, 660), (990, 660), (840, 300)):
            d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=RED)
        text(d, (xs[1], 760), 'constraint = pin', 56, anchor='ma'); text(d, (xs[1], 840), 'all pinned: nothing moves', 48, GREY, R, anchor='ma')
    if step >= 3:
        block(d, 1460, 660, 6, -110)
        text(d, (xs[2], 760), 'pad = push out', 56, anchor='ma'); text(d, (xs[2], 840), 'out of the paper', 48, GREY, R, anchor='ma')
    if step >= 4:
        d.rounded_rectangle((2010, 320, 2380, 680), radius=24, fill=PAPER, outline=GREY, width=4)
        text(d, (2040, 360), 'Body', 52); text(d, (2070, 450), 'Pad', 52); text(d, (2100, 540), 'Sketch', 52)
        text(d, (xs[3], 760), 'tree = recipe', 56, anchor='ma'); text(d, (xs[3], 840), 'the steps, in order', 48, GREY, R, anchor='ma')
    if step >= 5:
        chip(d, (W / 2, 1000), 'by hand and Claude: 8,500 mm³, 0 to 60, standing up', 60, PAPER, GREEN, anchor='m')
        chip(d, (W / 2, 1150), "Claude's sketch: 16 ways to move, no sizes", 60, PAPER, RED, anchor='m')
    save(im, f'card-recap-{step}.png' if step < 5 else 'card-recap.png')


if __name__ == '__main__':
    for n in range(1, 6):
        card_recap(n)
    card_paper(); card_joutline(); card_joutline_steps(); card_pad()
    for n in range(1, 5):
        card_sum(n)
