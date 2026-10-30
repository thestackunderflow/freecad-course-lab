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
    """F3: named amounts at the top; steps that use the name (one of them a sum: half the flour); step 3 the amount
    changes and both steps follow (a preview of an expression)."""
    im, d = canvas(); header(d, 'A recipe card: amounts at the top')
    d.rounded_rectangle((420, 230, 2140, 1260), radius=30, fill=PAPER, outline=GREY, width=6)
    text(d, (500, 290), 'Amounts', 72, GREY)
    amt = '400 g' if step >= 3 else '200 g'
    d.rounded_rectangle((500, 400, 1360, 520), radius=20, fill=(255, 243, 214) if step >= 3 else (241, 245, 249),
                        outline=AMBER if step >= 3 else GREY, width=5)
    text(d, (540, 460), 'flour', 76, INK, anchor='lm'); text(d, (1320, 460), amt, 76, AMBER if step >= 3 else INK, anchor='rm')
    if step >= 2:
        text(d, (500, 620), 'Steps', 72, GREY)
        hl = GREEN if step >= 3 else INK
        text(d, (540, 760), '2. add the flour', 72, hl)
        text(d, (540, 900), '3. stir', 60, GREY, R)
        text(d, (540, 1040), '4. add sugar: half the flour', 72, hl)
        if step >= 3:
            text(d, (2080, 790), '→ 400 g', 64, GREEN, anchor='rm')
            text(d, (2080, 1070), '→ 200 g', 64, GREEN, anchor='rm')
    if step >= 3:
        chip(d, (W / 2, 1300), 'change the flour once: every step that uses it follows', 56, PAPER, GREEN, anchor='m')
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
        rows = [('back plate 5 x 60 = 300', INK), ('arm 30 x 5 = 150', GREEN), ('lip 5 x 10 = 50', AMBER)]
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
        text(d, (470, 830), 'a spreadsheet', 50, GREY, R, anchor='ma')
    if step >= 2:
        chip(d, (1000, 330), 'alias: hook_depth', 56, PAPER, BLUE)
        text(d, (1290, 470), 'the name FreeCAD reads', 50, GREY, R, anchor='ma')
    if step >= 3:
        text(d, (1000, 600), 'drop = lip_height − thickness', 52, RED)
        text(d, (1290, 690), 'an expression: a size from names', 50, GREY, R, anchor='ma')
    if step >= 4:
        chip(d, (1880, 300), '1 cell → 3 sizes', 64, PAPER, GREEN)
        text(d, (2120, 430), 'thickness: plate, arm, lip', 50, GREY, R, anchor='ma')
    if step >= 5:
        chip(d, (W / 2, 1050), 'right or wrong, the part follows: check the first build (8,500 mm³)', 56, PAPER, RED,
             anchor='m')
    save(im, f'card-recap-{step}.png' if step < 5 else 'card-recap.png')


def card_a1_vs_ours():
    """F27: the two readings of "8 thick", from the lab's own corners (hand thick8 and run A1 after message 3)."""
    import json
    L3 = os.path.join(LAB, 'out', 'l3')
    hand = json.load(open(os.path.join(L3, 'hand', 'measure-thick8.json')))
    a1 = json.load(open(os.path.join(L3, 'runs', 'A1', 'measure-after3.json')))
    im, d = canvas(); header(d, '"8 thick": two readings')
    for k, (m, title, sub, col) in enumerate(((hand, 'with names (ours, B1, B2)', 'lip 8 wide x 10 high', GREEN),
                                               (a1, 'without names (A1)', 'lip 5 wide x 13 high', AMBER))):
        ox, oy, sc = 180 + k * 1240, 1150, 12
        pts = [(ox + x * sc, oy - y * sc) for x, y in m['sketches'][0]['corners_xy']]
        d.polygon(pts, fill=(176, 190, 212), outline=INK, width=6)
        part = [r for r in m['solids'] if not r.get('in_list')][-1]
        text(d, (ox, 300), title, 60, col)
        text(d, (ox + 520, 700), sub, 50, INK)
        text(d, (ox + 520, 790), '%s mm³' % format(int(round(part['volume_mm3'])), ','), 70, col)
    chip(d, (W / 2, 1300), 'the name decided what "thickness" means', 56, PAPER, INK, anchor='m')
    save(im, 'card-a1-vs-ours.png')


def card_compare():
    """F27: the comparison rows, from out/l3/compare.json (three columns, 48 px+)."""
    import json
    c = json.load(open(os.path.join(LAB, 'out', 'l3', 'compare.json')))
    r = c['runs']

    def v(run, st):
        return format(int(round(r[run]['parts'][st]['volume_mm3'])), ',')
    im, d = canvas(); header(d, 'Side by side')
    cols = [(860, 'by hand'), (1480, 'with the sentence'), (2140, 'without it')]
    subs = ['', '2 runs: B1, B2', '1 run: A1']
    for (x, t), sub in zip(cols, subs):
        text(d, (x, 230), t, 60, INK, anchor='ma')
        if sub:
            text(d, (x, 305), sub, 48, GREY, R, anchor='ma')
    rows = [('names', '5', '5 · 5', 'none'),
            ('first build', '8,500', '%s · %s' % (v('B1', 'first'), v('B2', 'first')), v('A1', 'first')),
            ('40 deep', '10,000', '%s · %s' % (v('B1', 'after2'), v('B2', 'after2')), v('A1', 'after2') + ' (redrawn)'),
            ('8 thick', '15,040', '%s · %s' % (v('B1', 'after3'), v('B2', 'after3')), v('A1', 'after3')),
            ('one cell each', 'yes', 'yes · yes', 'no')]
    for k, row in enumerate(rows):
        y = 430 + k * 160
        d.line((120, y - 30, 2440, y - 30), fill=(205, 210, 220), width=3)
        text(d, (140, y + 30), row[0], 56, GREY, anchor='lm')
        for (x, _), val in zip(cols, row[1:]):
            colr = AMBER if val.startswith('15,220') or val == 'no' or val == 'none' else INK
            text(d, (x, y + 30), val, 56, colr, anchor='mm')
    chip(d, (W / 2, 1300), "no-AI replays: B1 8,500 · 10,000 · 15,040 · A1 … 15,220", 52, PAPER, INK, anchor='m')
    save(im, 'card-compare.png')


if __name__ == '__main__':
    for n in (1, 2, 3):
        card_recipe(n)
    for n in (1, 2, 3, 4):
        card_names(n)
    card_expected('depth40'); card_expected('thick8')
    for n in range(1, 6):
        card_recap(n)
    card_a1_vs_ours(); card_compare()
