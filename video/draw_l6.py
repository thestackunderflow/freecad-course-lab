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
    text(d, (200, 960), 'next: the volume line in FreeCAD', 60, GREY)
    save(im, 'card-sum.png')


def card_recap(step):
    """F22, three reveals: the haircut ticket; the tape measure; the answer key."""
    im, d = canvas(); header(d, 'Remember')
    LIGHT = (205, 210, 220)
    on = lambda k: step >= k   # noqa: E731
    d.rectangle((120, 300, 860, 1000), fill=TICKET if on(1) else BG, outline=INK if on(1) else LIGHT, width=6)
    text(d, (170, 350), 'the ticket', 54, GREY if on(1) else LIGHT)
    text(d, (170, 460), 'change: 1 thing', 62, BLUE if on(1) else LIGHT)
    for k, line in enumerate(('keep: line 1', 'keep: line 2', 'keep: ...')):
        text(d, (170, 580 + k * 95), line, 58, GREEN if on(1) else LIGHT)
    text(d, (490, 1060), 'a must-stay-true list', 62, INK if on(1) else LIGHT, anchor='ma')
    d.rounded_rectangle((970, 520, 1590, 760), radius=30, fill=(250, 210, 60) if on(2) else BG,
                        outline=INK if on(2) else LIGHT, width=6)
    for k in range(13):
        x = 1000 + k * 44
        d.line((x, 520, x, 570 + (40 if k % 2 == 0 else 0)), fill=INK if on(2) else LIGHT, width=5)
    text(d, (1280, 800), 'before · after', 58, BLUE if on(2) else LIGHT, anchor='ma')
    text(d, (1280, 1060), 'Measure', 62, INK if on(2) else LIGHT, anchor='ma')
    d.rectangle((1720, 300, 2440, 1000), fill=PAPER if on(3) else BG, outline=INK if on(3) else LIGHT, width=6)
    text(d, (1770, 350), 'ANSWER KEY', 62, INK if on(3) else LIGHT)
    for k in range(5):
        d.line((1780, 500 + k * 100, 2380, 500 + k * 100), fill=GREY if on(3) else LIGHT, width=4)
    text(d, (2080, 1060), 'a pass rule, written first', 62, INK if on(3) else LIGHT, anchor='ma')
    save(im, f'card-recap-{step}.png')


ROWS = ['opening 45', '1 one solid, no errors', '2 plate 60 x 30', '3 walls 5', '4 lip 10', '5 holes 4, centred, 15/45',
        '6 the 2 mm lip edge', '7 the names drive it', 'volume 17,098.6']
KEYS = ['C', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'V']


def frame(path, w, h, box=(1150, 0, 2880, 1800)):
    """The FreeCAD half of a side-by-side take frame (default box), scaled to cover w x h and centre-cropped."""
    from PIL import Image
    im = Image.open(path).convert('RGB').crop(box)
    k = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * k + 0.5), int(im.height * k + 0.5)))
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def column(d, x, y, run, title, sub=None):
    c = json.load(open(os.path.join(L6, 'compare.json'), encoding='utf-8'))['runs'][run]
    d.rectangle((x - 30, y - 40, x + 1010, y + 1130), fill=PAPER, outline=INK, width=5)
    text(d, (x, y - 10), title, 60, INK)
    if sub:
        text(d, (x, y + 62), sub, 46, GREY)
    for k, (lab, key) in enumerate(zip(ROWS, KEYS)):
        ok = c['lines'][key]
        yy = y + 150 + k * 100
        text(d, (x, yy), ('✓ ' if ok else '✗ ') + lab, 56, GREEN if ok else RED)
    return c


def card_run(run, n, src, sub):
    """F14: one run's real final frame (left) with its whole column of the pass rule (right), from compare.json."""
    im, d = canvas()
    im.paste(frame(src, 1440, 1440), (0, 0))
    chip(d, (40, 40), 'REAL FRAME · run %d' % n, 44, PAPER, BLUE)
    c = column(d, 1520, 170, run, 'run %d: %s' % (n, 'passed' if c_pass(run) else 'not passed'), sub)
    save(im, 'card-run%d.png' % n)


def c_pass(run):
    return json.load(open(os.path.join(L6, 'compare.json'), encoding='utf-8'))['runs'][run]['pass']


def card_total():
    c = json.load(open(os.path.join(L6, 'compare.json'), encoding='utf-8'))
    im, d = canvas(); header(d, 'The pass rule, written first')
    for k, (r, n) in enumerate((('B1', 1), ('B2', 2), ('B3', 3))):
        x = 330 + k * 700
        im.paste(frame(os.path.join(L6, 'runs', r, 's1-ourcheck.png') if r != 'B1' else
                       os.path.join(L6, 'inspect-B1', 's1-ourcheck.png'), 600, 380, (1700, 300, 2880, 1100)), (x - 50, 300))
        ok = c['runs'][r]['pass']
        text(d, (x + 250, 720), 'run %d: %s' % (n, 'every line' if ok else 'broke a line'), 58, GREEN if ok else RED, anchor='ma')
    text(d, (W / 2, 900), '%s kept every line' % c['summary']['with_list_passed'], 96, GREEN, anchor='ma')
    chip(d, (W / 2, 1200), 'three runs: a good sign, not a promise', 56, PAPER, INK, anchor='m')
    save(im, 'card-3of3.png')


def card_without(step=2):
    """F16: with the list (3 runs) vs without (1 run): passed, lines said with a number, from compare.json."""
    c = json.load(open(os.path.join(L6, 'compare.json'), encoding='utf-8'))
    im, d = canvas()
    im.paste(frame(os.path.join(L6, 'runs', 'A1', 's1-ourcheck.png'), 1300, 1440), (0, 0))
    chip(d, (40, 40), 'REAL FRAME · the run without the list', 44, PAPER, BLUE)
    s = c['summary']['lines_said_with_a_number']
    x0 = 1380
    d.rectangle((x0, 140, 2520, 1300), fill=PAPER, outline=INK, width=5)
    text(d, (x0 + 40, 180), 'with the list', 58, INK)
    text(d, (x0 + 40, 250), '3 runs', 48, GREY)
    text(d, (x0 + 40, 330), '%s passed (our script)' % c['summary']['with_list_passed'].replace(' of ', '/'), 60, GREEN)
    text(d, (x0 + 40, 420), 'its report:', 46, GREY)
    text(d, (x0 + 40, 480), 'every line, sizes as numbers', 54, INK)
    d.line((x0 + 30, 600, 2490, 600), fill=GREY, width=3)
    if step < 2:
        save(im, 'card-without-1.png')
        return
    text(d, (x0 + 40, 640), 'without the list', 58, INK)
    text(d, (x0 + 40, 710), '1 run', 48, GREY)
    text(d, (x0 + 40, 790), 'passed (our script)' if c['runs']['A1']['pass'] else 'broke a line', 60, GREEN if c['runs']['A1']['pass'] else RED)
    text(d, (x0 + 40, 880), 'its report:', 46, GREY)
    text(d, (x0 + 40, 940), 'opening, size, volume;', 54, INK)
    text(d, (x0 + 40, 1010), "the rest 'unchanged'", 54, INK)
    text(d, (x0 + 40, 1080), 'nothing on the names', 54, RED)
    chip(d, (x0 + 40, 1190), 'one run: a story, not a rate', 46, PAPER, INK)
    save(im, 'card-without.png')


def thumbs():
    """Thumbnails (1280 x 720) from the real by-hand frames: the sheet's hook_depth 45 beside Measure's 35.00 mm."""
    from PIL import Image
    src = Image.open(os.path.join(L6, 'hand', 's4-measure35.png')).convert('RGB')
    a = src.crop((490, 420, 960, 500)).resize((560, 95))       # the sheet's row 1: hook_depth 45.00 mm
    b = src.crop((2190, 760, 2870, 820)).resize((560, 50))     # Measurement: Result 35.00 mm
    part = src.crop((1880, 330, 2880, 1330)).resize((520, 520))
    for name, title in (('thumb-primary.png', 'TYPED 45, GOT 35'), ('thumb-altA.png', '3/3 KEPT EVERY LINE')):
        im, d = canvas(1280, 720)
        d.rectangle((0, 0, 1280, 140), fill=INK)
        text(d, (640, 70), title, 72, PAPER, anchor='mm')
        im.paste(part, (720, 175))
        d.rectangle((714, 169, 1246, 701), outline=RED, width=8)
        im.paste(a, (60, 230)); d.rectangle((54, 224, 626, 331), outline=INK, width=6)
        text(d, (340, 360), 'typed', 48, GREY, anchor='ma')
        im.paste(b, (60, 470)); d.rectangle((54, 464, 626, 526), outline=RED, width=8)
        text(d, (340, 560), 'measured', 48, RED, anchor='ma')
        save(im, name)


if __name__ == '__main__':
    for i in (1, 2, 3):
        card_haircut(i); card_depth(i); card_key(i); card_recap(i)
    card_sum()
    card_run('B1', 1, os.path.join(L6, 'inspect-B1', 's1-ourcheck.png'), 'one cell: hook_depth 55')
    card_run('B2', 2, os.path.join(L6, 'runs', 'B2', 's1-ourcheck.png'), 'one cell: hook_depth 55')
    card_run('B3', 3, os.path.join(L6, 'runs', 'B3', 's1-ourcheck.png'), 'a new name: opening 45')
    card_total(); card_without(1); card_without(); thumbs()
