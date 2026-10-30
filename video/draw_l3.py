"""Lesson 3's diagram cards (2560 x 1440, text 56 px or more). Diagrams are visibly diagrams (flat shapes, no fake UI);
every number comes from the tested outline checker (checker/outline.py named_moves) or a lab file. The recipe-card
peg is lesson 2's "the Model tree is the recipe", extended (the SolidCraft lesson 3 used the same picture).
    docker run --rm --network none -v "<lab>:/work" -w /work video-qa:2 python3 video/draw_l3.py
"""
import os
import sys

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, LAB)
sys.path.insert(0, os.path.join(LAB, 'video'))
import draw_l2 as d2  # noqa: E402
from checker import outline  # noqa: E402
from draw_l2 import AMBER, BG, BLUE, GREEN, GREY, INK, PAPER, RED, R, W, canvas, chip, header, text  # noqa: E402

OUT = os.path.join(LAB, 'video', 'frames-l3')
os.makedirs(OUT, exist_ok=True)
NAMES = {'plate_height': 60, 'width': 20, 'thickness': 5, 'hook_depth': 25, 'lip_height': 10}
TEAL = (13, 110, 120)


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(name)


def exp(depth=25, t=5):
    return outline.expected(outline.named_moves(dict(NAMES, hook_depth=depth, thickness=t)), 20)


def jpoly(ox, oy, s, depth=25, t=5):
    pts = outline.walk(outline.named_moves(dict(NAMES, hook_depth=depth, thickness=t)))[:-1]
    return [(ox + x * s, oy - z * s) for x, z in pts]


def card_recipe(step):
    """F3: a recipe card: named amounts at the top, steps that use the name; step 3 the amount changes, both steps follow."""
    im, d = canvas(); header(d, 'A recipe card: amounts at the top')
    d.rounded_rectangle((560, 230, 2000, 1300), radius=30, fill=PAPER, outline=GREY, width=6)
    text(d, (640, 290), 'Amounts', 72, GREY)
    amt = '400 g' if step >= 3 else '200 g'
    d.rounded_rectangle((640, 400, 1500, 520), radius=20, fill=(255, 243, 214) if step >= 3 else (241, 245, 249),
                        outline=AMBER if step >= 3 else GREY, width=5)
    text(d, (680, 460), 'flour', 76, INK, anchor='lm'); text(d, (1460, 460), amt, 76, AMBER if step >= 3 else INK, anchor='rm')
    if step >= 2:
        text(d, (640, 620), 'Steps', 72, GREY)
        hl = GREEN if step >= 3 else INK
        text(d, (680, 760), '2. add the flour', 76, hl)
        text(d, (680, 900), '3. stir', 64, GREY, R)
        text(d, (680, 1040), '4. add the rest of the flour', 76, hl)
        if step >= 3:
            for y in (760, 1040):
                text(d, (1940, y + 40), '← 400 g', 64, GREEN, anchor='rm')
            chip(d, (W / 2, 1330), 'change the amount once: every step that uses it follows', 56, PAPER, GREEN, anchor='m')
    save(im, f'card-recipe-{step}.png')


def card_names(step):
    """F9: the six sizes get names, one sentence at a time (1: depth, lip, plate; 2: the two thicknesses; 3: the drop
    inside the lip = lip_height - thickness; 4: 'expression')."""
    im, d = canvas(); header(d, 'Each size gets a name')
    s, ox, oy = 15, 760, 1110
    d.polygon(jpoly(ox, oy, s), fill=(176, 190, 212), outline=INK, width=7)

    def tag(xy, words, col, anchor='lm', size=60):
        text(d, xy, words, size, col, anchor=anchor)
    d.line((ox, oy + 50, ox + 25 * s, oy + 50), fill=BLUE, width=8)
    tag((ox + 25 * s / 2, oy + 110), '25 = hook_depth', BLUE, 'ma')
    d.line((ox + 25 * s + 50, oy, ox + 25 * s + 50, oy - 10 * s), fill=BLUE, width=8)
    tag((ox + 25 * s + 80, oy - 5 * s), '10 = lip_height', BLUE)
    d.line((ox - 50, oy, ox - 50, oy - 60 * s), fill=BLUE, width=8)
    tag((ox - 80, oy - 30 * s), '60 =', BLUE, 'rm'); tag((ox - 80, oy - 30 * s + 80), 'plate_height', BLUE, 'rm')
    if step >= 2:
        d.line((ox + 20 * s, oy - 10 * s - 40, ox + 25 * s, oy - 10 * s - 40), fill=TEAL, width=8)
        tag((ox + 25 * s + 80, oy - 10 * s - 70), "lip's width 5 = thickness", TEAL)
        d.line((ox + 5 * s + 10, oy - 60 * s + 40, ox + 5 * s + 70, oy - 60 * s + 40), fill=TEAL, width=8)
        tag((ox + 5 * s + 90, oy - 60 * s + 40), "back plate's 5 = thickness", TEAL)
    if step >= 3:
        x = ox + 20 * s - 40
        d.line((x, oy - 10 * s, x, oy - 5 * s), fill=RED, width=10)
        d.polygon([(x - 20, oy - 5 * s - 30), (x + 20, oy - 5 * s - 30), (x, oy - 5 * s)], fill=RED)
        tag((ox + 25 * s + 80, oy - 5 * s - 480), 'the drop inside the lip', RED)
        tag((ox + 25 * s + 80, oy - 5 * s - 400), '= lip_height − thickness', RED)
        tag((ox + 25 * s + 80, oy - 5 * s - 320), '10 − 5 = 5: the arm stays 5 thick', GREY, size=52)
    if step >= 4:
        chip(d, (W / 2, 1300), 'a size written from names = an expression', 60, PAPER, INK, anchor='m')
    save(im, f'card-names-{step}.png')


def card_expected(kind):
    """F16 / F19 inserts: the number worked out before the change (from the tested named walk)."""
    if kind == 'depth40':
        e = exp(40, 5)
        im, dd = canvas(); header(dd, 'Worked out first: 40 deep')
        dd.polygon(jpoly(260, 1250, 15, 40, 5), fill=(176, 190, 212), outline=INK, width=6)
        rows = [('back plate 5 x 60 = 300', INK), ('arm 35 x 5 = 175', GREEN), ('lip 5 x 5 = 25', AMBER)]
        tag = 'box 40 x 20 x 60: 15 deeper'
    else:
        e = exp(40, 8)
        im, dd = canvas(); header(dd, 'Worked out first: 8 thick')
        dd.polygon(jpoly(260, 1250, 15, 40, 8), fill=(176, 190, 212), outline=INK, width=6)
        rows = [('back plate 8 x 60 = 480', INK), ('arm 24 x 8 = 192', GREEN), ('lip 8 x 10 = 80', AMBER),
                ('the drop: 10 − 8 = 2', RED)]
        tag = 'box still 40 x 20 x 60'
    tx = 1200
    for k, (a, col) in enumerate(rows):
        text(dd, (tx, 300 + k * 140), a, 76, col)
    y = 300 + len(rows) * 140 + 30
    dd.line((tx, y, 2450, y), fill=INK, width=6)
    text(dd, (tx, y + 40), f"{e['area_mm2']:,.0f} mm²  x 20 mm", 84, INK)
    text(dd, (tx, y + 170), f"= {e['volume_mm3']:,.0f} mm³", 110, RED)
    chip(dd, (W / 2, 1330), tag, 56, PAPER, INK, anchor='m')
    save(im, f'card-expected-{kind}.png')


def card_recap(step):
    """F30: one picture per sentence (1 amounts, 2 alias, 3 expression, 4 one cell three sizes, 5 check the first build)."""
    im, d = canvas(); header(d, 'Remember')
    if step >= 1:
        d.rounded_rectangle((120, 260, 820, 700), radius=24, fill=PAPER, outline=GREY, width=5)
        text(d, (170, 300), 'hook_depth   25 mm', 50); text(d, (170, 380), 'thickness      5 mm', 50)
        text(d, (170, 460), 'lip_height     10 mm', 50)
        text(d, (470, 760), 'named amounts at the top', 50, INK, anchor='ma')
        text(d, (470, 830), 'a spreadsheet', 46, GREY, R, anchor='ma')
    if step >= 2:
        chip(d, (1000, 330), 'alias: hook_depth', 56, PAPER, BLUE)
        text(d, (1290, 470), 'the name FreeCAD reads', 46, GREY, R, anchor='ma')
    if step >= 3:
        text(d, (1000, 600), 'drop = lip_height − thickness', 52, RED)
        text(d, (1290, 690), 'an expression: a size from names', 46, GREY, R, anchor='ma')
    if step >= 4:
        chip(d, (1880, 300), '1 cell → 3 sizes', 64, PAPER, GREEN)
        text(d, (2120, 430), 'thickness: plate, arm, lip', 46, GREY, R, anchor='ma')
    if step >= 5:
        chip(d, (W / 2, 1050), 'right or wrong, the part follows: check the first build (8,500 mm³)', 56, PAPER, RED,
             anchor='m')
    save(im, f'card-recap-{step}.png' if step < 5 else 'card-recap.png')


if __name__ == '__main__':
    for n in (1, 2, 3):
        card_recipe(n)
    for n in (1, 2, 3, 4):
        card_names(n)
    card_expected('depth40'); card_expected('thick8')
    for n in range(1, 6):
        card_recap(n)
