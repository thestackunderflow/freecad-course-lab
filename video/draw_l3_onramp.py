"""Lesson 3 re-cut (30 Oct 2026, owner: "bring user up to speed"): the two on-ramp cards after the cold open, white,
built in steps on one layout (nothing moves between builds).
  card-where-1..2  F0a: the course so far (lesson 1, lesson 2) and today (lesson 3)
  card-sheet-1..2  F0b: FreeCAD's own spreadsheet; a cell -> a sketch size -> the part
The hook pictures are real frames from the lab (lesson 2's file opened in out/l3/hand); the sketch outline comes from
the tested outline checker. Run in the QA image:
    docker run --rm --network none -v "<lab>:/work" -w /work video-qa:2 python3 video/draw_l3_onramp.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image  # noqa: E402

from draw_l2 import AMBER, BLUE, GREEN, GREY, INK, PAPER, R, W, H, canvas, chip, header, text  # noqa: E402
from draw_l3 import LAB, jpoly, save  # noqa: E402

WHITE = (255, 255, 255)
LIGHT = (241, 245, 249)
HAND = os.path.join(LAB, 'out', 'l3', 'hand')


def real(name, box, size):
    return Image.open(os.path.join(HAND, name)).convert('RGB').crop(box).resize(size)


def arrow(d, a, b, col=INK, w=10):
    d.line((a, b), fill=col, width=w)
    x0, y0 = a
    x1, y1 = b
    import math
    ang = math.atan2(y1 - y0, x1 - x0)
    L = 34
    p1 = (x1 - L * math.cos(ang - 0.45), y1 - L * math.sin(ang - 0.45))
    p2 = (x1 - L * math.cos(ang + 0.45), y1 - L * math.sin(ang + 0.45))
    d.polygon([b, p1, p2], fill=col)


def card_where(step):
    """F0a (after the v3 script gate): a vertical strip, one short line per lesson (44 columns or fewer, 56 px+);
    1 and 2 done, 3 lit in step 2."""
    im, d = canvas(bg=WHITE); header(d, 'The FreeCAD + Claude course')
    rows = [(230, '1', 'Plug Claude into FreeCAD', None),
            (560, '2', 'Draw the hook: plain numbers', None),
            (890, '3', 'Today: give the sizes names', 'one change → every place it is used')]
    for k, (y, num, line, sub) in enumerate(rows):
        lit = k == 2
        if lit and step < 2:
            d.rounded_rectangle((120, y, 2440, y + 290), radius=30, fill=WHITE, outline=(215, 220, 228), width=5)
            text(d, (230, y + 145), num, 96, (190, 196, 206), anchor='mm')
            continue
        d.rounded_rectangle((120, y, 2440, y + 290), radius=30, fill=(232, 245, 236) if lit else LIGHT,
                            outline=GREEN if lit else GREY, width=9 if lit else 5)
        d.ellipse((170, y + 85, 290, y + 205), fill=GREEN if lit else GREY)
        text(d, (230, y + 145), num, 80, PAPER, anchor='mm')
        text(d, (340, y + (110 if sub else 145)), line, 76, GREEN if lit else INK, anchor='lm')
        if sub:
            text(d, (340, y + 205), sub, 60, INK, R, anchor='lm')
    # lesson 1 art: Claude -> plug -> FreeCAD
    for k, lab in enumerate(('Claude', 'plug', 'FreeCAD')):
        bx = 1480 + k * 320
        d.rounded_rectangle((bx, 300, bx + 270, 450), radius=16, fill=PAPER, outline=BLUE if lab == 'plug' else INK, width=5)
        text(d, (bx + 135, 375), lab, 46, BLUE if lab == 'plug' else INK, anchor='mm')
        if k:
            arrow(d, (bx - 56, 375), (bx - 6, 375), INK, 7)
    # lesson 2 art: the real hook (lesson 2's file, opened in the lab)
    im.paste(real('s1-opened.png', (1420, 300, 1950, 1050), (190, 269)), (2160, 571))
    save(im, f'card-where-{step}.png')


def card_where_v1(step):
    """F0a first draft (three columns; too dense for a phone at the v3 gate). Kept for reference, not drawn."""
    im, d = canvas(bg=WHITE); header(d, 'The FreeCAD + Claude course so far')
    boxes = [(110, 260, 860, 1180), (905, 260, 1655, 1180), (1700, 260, 2450, 1180)]
    # lesson 1: Claude -> plug -> FreeCAD
    x0, y0, x1, y1 = boxes[0]
    d.rounded_rectangle(boxes[0], radius=30, fill=LIGHT, outline=GREY, width=5)
    text(d, (x0 + 40, y0 + 40), 'Lesson 1', 64, GREY)
    for k, lab in enumerate(('Claude', 'the plug', 'FreeCAD')):
        by = y0 + 190 + k * 200
        d.rounded_rectangle((x0 + 150, by, x1 - 150, by + 120), radius=18, fill=PAPER, outline=INK, width=5)
        text(d, ((x0 + x1) / 2, by + 60), lab, 58, INK, anchor='mm')
        if k:
            arrow(d, ((x0 + x1) / 2, by - 76), ((x0 + x1) / 2, by - 6), INK, 8)
    text(d, ((x0 + x1) / 2, y1 - 120), 'Claude connected', 58, INK, anchor='mm')
    text(d, ((x0 + x1) / 2, y1 - 55), 'to FreeCAD', 58, INK, anchor='mm')
    # lesson 2: the real hook, plain numbers
    x0, y0, x1, y1 = boxes[1]
    d.rounded_rectangle(boxes[1], radius=30, fill=LIGHT, outline=GREY, width=5)
    text(d, (x0 + 40, y0 + 40), 'Lesson 2', 64, GREY)
    im.paste(real('s1-opened.png', (1420, 300, 1950, 1050), (370, 524)), (x0 + 60, y0 + 140))
    for k, n in enumerate(('25', '10', '5', '5', '60', '5')):
        cx, cy = x0 + 530 + (k % 2) * 110, y0 + 190 + (k // 2) * 130
        d.rounded_rectangle((cx - 48, cy - 44, cx + 48, cy + 44), radius=12, fill=PAPER, outline=BLUE, width=4)
        text(d, (cx, cy), n, 52, BLUE, anchor='mm')
    text(d, ((x0 + x1) / 2, y1 - 120), 'this hook, each size', 58, INK, anchor='mm')
    text(d, ((x0 + x1) / 2, y1 - 55), 'a plain number', 58, INK, anchor='mm')
    # lesson 3: today
    x0, y0, x1, y1 = boxes[2]
    if step >= 2:
        d.rounded_rectangle(boxes[2], radius=30, fill=(232, 245, 236), outline=GREEN, width=9)
        text(d, (x0 + 40, y0 + 40), 'Lesson 3 · today', 64, GREEN)
        for k, (nm, v) in enumerate((('hook_depth', '25'), ('thickness', '5'), ('lip_height', '10'))):
            by = y0 + 190 + k * 150
            d.rounded_rectangle((x0 + 60, by, x1 - 60, by + 110), radius=16, fill=PAPER, outline=GREEN, width=4)
            text(d, (x0 + 95, by + 55), nm, 56, INK, anchor='lm')
            text(d, (x1 - 95, by + 55), v, 56, BLUE, anchor='rm')
        text(d, ((x0 + x1) / 2, y1 - 185), 'give the sizes names:', 56, INK, anchor='mm')
        text(d, ((x0 + x1) / 2, y1 - 120), 'one change, every', 56, GREEN, anchor='mm')
        text(d, ((x0 + x1) / 2, y1 - 55), 'place it is used', 56, GREEN, anchor='mm')
    else:
        d.rounded_rectangle(boxes[2], radius=30, fill=WHITE, outline=(215, 220, 228), width=5)
        text(d, ((x0 + x1) / 2, (y0 + y1) / 2), 'Lesson 3', 64, (190, 196, 206), anchor='mm')
    save(im, f'card-where-{step}.png')


def grid(d, x, y, cw, rh, rows, lit=None):
    """A plain spreadsheet grid: a header row of column letters, a column of row numbers, cells A and B."""
    cols = [90, cw, cw]
    hdr = (226, 232, 240)
    xs = [x]
    for c in cols:
        xs.append(xs[-1] + c)
    d.rectangle((x, y, xs[-1], y + rh), fill=hdr)
    for k, ch in enumerate(('A', 'B')):
        text(d, ((xs[k + 1] + xs[k + 2]) / 2, y + rh / 2), ch, 50, GREY, R, anchor='mm')
    for r, (nm, v) in enumerate(rows):
        ry = y + rh * (r + 1)
        d.rectangle((x, ry, xs[1], ry + rh), fill=hdr)
        text(d, ((xs[0] + xs[1]) / 2, ry + rh / 2), str(r + 1), 50, GREY, R, anchor='mm')
        if lit == r:
            d.rectangle((xs[2], ry, xs[3], ry + rh), fill=(255, 243, 214))
        text(d, (xs[1] + 24, ry + rh / 2), nm, 54, INK, R, anchor='lm')
        text(d, (xs[3] - 24, ry + rh / 2), v, 54, AMBER if lit == r else INK, anchor='rm')
    for k in range(len(rows) + 2):
        d.line((x, y + k * rh, xs[-1], y + k * rh), fill=(190, 198, 210), width=3)
    for xx in xs:
        d.line((xx, y, xx, y + rh * (len(rows) + 1)), fill=(190, 198, 210), width=3)
    if lit is not None:
        ry = y + rh * (lit + 1)
        d.rectangle((xs[2], ry, xs[3], ry + rh), outline=AMBER, width=8)
    return xs, rh


def card_sheet(step):
    """F0b. Step 1: the grid (FreeCAD's own, in the same file, no Excel). Step 2: B1 -> the sketch's bottom size ->
    the part, and the cell changed (25 -> 40): the part redraws."""
    im, d = canvas(bg=WHITE); header(d, "FreeCAD's own spreadsheet")
    rows = [('hook_depth', '40.00 mm' if step >= 2 else '25.00 mm'), ('thickness', '5.00 mm'), ('lip_height', '10.00 mm'),
            ('plate_height', '60.00 mm'), ('width', '20.00 mm')]
    gx, gy = 120, 250
    xs, rh = grid(d, gx, gy, 380, 110, rows, lit=0 if step >= 2 else None)
    if step == 1:
        text(d, (1100, 300), 'looks like Excel or Google Sheets,', 64, INK)
        text(d, (1100, 390), 'but it is part of FreeCAD', 64, INK)
        chip(d, (1100, 560), 'saved inside your FreeCAD file', 60, PAPER, BLUE)
        chip(d, (1100, 720), 'no Excel needed', 60, PAPER, GREEN)
        text(d, (gx, gy + rh * 6 + 60), 'a name in column A for you to read,', 54, GREY, R)
        text(d, (gx, gy + rh * 6 + 140), 'the value in column B', 54, GREY, R)
    else:
        # cell -> sketch size -> part
        s, ox, oy = 11, 1150, 1020
        d.polygon(jpoly(ox, oy, s, 40, 5), fill=(176, 190, 212), outline=INK, width=6)
        d.line((ox, oy + 40, ox + 40 * s, oy + 40), fill=AMBER, width=9)
        text(d, (ox + 20 * s, oy + 80), 'hook_depth: 40', 56, AMBER, anchor='ma')
        text(d, (ox + 20 * s, 240), 'the sketch', 58, GREY, R, anchor='ma')
        cy = gy + rh * 1.5
        d.line((xs[3] + 10, cy, ox - 90, cy), fill=AMBER, width=9)
        d.line((ox - 90, cy, ox - 90, oy + 40), fill=AMBER, width=9)
        arrow(d, (ox - 94, oy + 40), (ox - 12, oy + 40), AMBER, 9)
        im.paste(real('s15-depth40.png', (700, 330, 1430, 1280), (511, 665)), (1930, 330))
        text(d, (2185, 240), 'the part', 58, GREY, R, anchor='ma')
        arrow(d, (ox + 40 * s + 40, oy - 300), (1890, oy - 300), INK, 9)
        chip(d, (W / 2, 1290), 'change a cell: the part redraws itself', 60, PAPER, GREEN, anchor='m')
    save(im, f'card-sheet-{step}.png')


if __name__ == '__main__':
    for n in (1, 2):
        card_where(n)
        card_sheet(n)
    assert H == 1440
