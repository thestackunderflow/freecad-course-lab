"""Lesson 5's diagram cards (2560 x 1440, text 56 px or more). Diagrams are visibly diagrams (flat shapes, no fake UI);
every number comes from a lab file (out/l5/compare.json, out/l5/hand/mesh-*.json, out/l5/estimates/estimates.json).
Pegs: an STL = a wrapping of small flat paper triangles (only the outside, no recipe); the tree = lesson 2's recipe
(the Pad row = halfway; the Body or the last row = finished); a slicer = slicing a loaf into thin layers.
    docker run --rm --network none -v "<lab>:/work" -w /work cad3way-draw:1 python3 video/draw_l5.py [thumbs]
"""
import json
import math
import os
import sys

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, LAB)
sys.path.insert(0, os.path.join(LAB, 'video'))
from draw_l2 import BG, BLUE, GREEN, GREY, INK, PAPER, RED, W, canvas, chip, header, j_poly, text  # noqa: E402

OUT = os.path.join(LAB, 'video', 'frames-l5')
os.makedirs(OUT, exist_ok=True)
L5 = os.path.join(LAB, 'out', 'l5')
PLATE = (176, 190, 212)
BREAD = (222, 178, 120)
CRUST = (150, 95, 45)


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(name)


def mesh(name):
    return json.load(open(os.path.join(L5, 'hand', f'mesh-{name}.json'), encoding='utf-8'))


def wrapped_j(im, d, ox, oy, s, tri=True):
    """The hook's J outline; with tri, its surface covered by a lattice of flat triangles (masked to the outline)."""
    from PIL import Image, ImageDraw
    p = j_poly(ox, oy, s)
    d.polygon(p, fill=PLATE, outline=INK, width=6)
    if tri:
        xs, ys = [x for x, _ in p], [y for _, y in p]
        x0, y0, x1, y1 = int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        step = 46
        for y in range(y0 - step, y1 + step, step):
            ld.line((x0 - 400, y, x1 + 400, y), fill=BLUE + (255,), width=3)
        for x in range(x0 - (y1 - y0) - 400, x1 + 400, step):
            ld.line((x, y0, x + (y1 - y0), y1), fill=BLUE + (255,), width=3)
            ld.line((x, y1, x + (y1 - y0), y0), fill=BLUE + (160,), width=2)
        mask = Image.new('L', im.size, 0)
        ImageDraw.Draw(mask).polygon(p, fill=255)
        im.paste(lay, (0, 0), Image.composite(lay, Image.new('RGBA', im.size, (0, 0, 0, 0)), mask))
        d.polygon(p, outline=INK, width=6)


def card_stl():
    im, d = canvas(); header(d, 'An STL: the outside, as triangles')
    wrapped_j(im, d, 330, 1150, 13, tri=False)
    text(d, (590, 1190), 'the part', 64, GREY, anchor='ma')
    text(d, (1180, 760), '→', 140, INK, anchor='mm')
    wrapped_j(im, d, 1500, 1150, 13, tri=True)
    text(d, (1760, 1190), 'wrapped in paper triangles', 64, BLUE, anchor='ma')
    chip(d, (W / 2, 1330), 'no recipe, no names: only the surface', 54, PAPER, INK, anchor='m')
    save(im, 'card-stl.png')


def card_slicer():
    im, d = canvas(); header(d, 'A slicer: thin layers, one at a time')
    x0, y0, x1, y1 = 420, 420, 1500, 1080
    d.rounded_rectangle((x0, y0, x1, y1), radius=160, fill=BREAD, outline=CRUST, width=12)
    for k in range(1, 9):
        x = x0 + k * (x1 - x0) / 9
        d.line((x, y0 + 30, x, y1 - 30), fill=CRUST, width=6)
    for k in range(3):
        sx = 1700 + k * 70
        d.rounded_rectangle((sx, 520 + k * 20, sx + 40, 1000 + k * 20), radius=18, fill=BREAD, outline=CRUST, width=6)
    text(d, (960, 1150), 'slicing a loaf', 66, GREY, anchor='ma')
    text(d, (1850, 1120), 'one layer', 66, GREY, anchor='ma')
    text(d, (1850, 1190), 'at a time', 66, GREY, anchor='ma')
    chip(d, (W / 2, 1300), 'it also works out how long the print takes', 54, PAPER, INK, anchor='m')
    save(im, 'card-slicer.png')


def polygon(d, cx, cy, r, n, col):
    pts = [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]
    d.polygon(pts, fill=PAPER, outline=col, width=6 if n < 100 else 5)


def card_flats():
    """F13 insert: 26 sides vs 229 sides, the flat-to-flat sizes from the checker, and a 0.4 mm printer line."""
    a, b = mesh('hook'), mesh('hook-fine')
    fa, fb = a['holes'][0]['flat_d'], b['holes'][0]['flat_d']
    im, d = canvas(); header(d, 'One 4 mm screw hole, in the file')
    polygon(d, 720, 700, 380, a['holes'][0]['sides'], RED)
    polygon(d, 1840, 700, 380, b['holes'][0]['sides'], GREEN)
    text(d, (720, 1130), f"default: {a['holes'][0]['sides']} sides", 64, RED, anchor='ma')
    text(d, (720, 1210), f'{fa:.2f} mm across the flats', 60, INK, anchor='ma')
    text(d, (1840, 1130), f"0.01: {b['holes'][0]['sides']} sides", 64, GREEN, anchor='ma')
    text(d, (1840, 1210), f'{fb:.2f} mm across the flats', 60, INK, anchor='ma')
    chip(d, (W / 2, 1300), f'difference {fb - fa:.2f} mm · a printer line is about 0.4 mm wide', 52, PAPER, INK, anchor='m')
    save(im, 'card-flats.png')


def card_compare():
    """F22: by hand / with the sentence / without, from out/l5/compare.json."""
    c = json.load(open(os.path.join(L5, 'compare.json'), encoding='utf-8'))
    b1, a1 = c['runs']['B1'], c['runs']['A1']
    h = c['hand']['hook']
    im, d = canvas(); header(d, 'Side by side')
    cols = [('by hand', 960), ('with the sentence', 1560), ('without', 2160)]
    for name, x in cols:
        text(d, (x, 220), name, 58, GREY, anchor='ma')

    def cell(ok, s):
        return {'ok': ok, 'text': s}
    rows = [
        ('exported', [cell(True, 'the Body'), cell(b1['right_part'], 'the Body'), cell(a1['right_part'], 'the Body')]),
        ('triangles', [cell(None, str(h['triangles'])), cell(None, str(b1['triangles'])), cell(None, str(a1['triangles']))]),
        ('file checked', [cell(True, 'yes'), cell(b1['checked'], 'yes' if b1['checked'] else 'no'),
                          cell(a1['checked'], 'yes' if a1['checked'] else 'no (said so)')]),
        ('numbers true', [cell(True, '14,849'), cell(b1['reported_ok'], '272 · 14,849'), cell(None, 'none given')]),
        ('print it', [cell(None, 'side: 22 min'), cell(None, 'on its side'), cell(None, 'on its side')]),
    ]
    for k, (label, cells) in enumerate(rows):
        y = 330 + k * 175
        text(d, (110, y), label, 56, INK)
        for (name, x), cl in zip(cols, cells):
            ok = cl['ok']
            text(d, (x, y), cl['text'], 56, GREEN if ok else (RED if ok is False else INK), anchor='ma')
    rp = c['replay_B1']['replay']
    chip(d, (W / 2, 1250), f"no-AI replay of the first run: {rp['triangles']} triangles · "
                           f"{rp['volume_mm3']:,.0f} mm³ · {'same' if c['replay_B1']['pass'] else 'different'}",
         52, PAPER, INK, anchor='m')
    save(im, 'card-compare.png')


def card_recap(step):
    """F24, one reveal per sentence: the wrapping; the recipe (last row = finished) + check the volume; the loaf."""
    im, d = canvas(); header(d, 'Remember')
    wrapped_j(im, d, 300, 980, 9, tri=True)
    text(d, (560, 1040), 'STL = the wrapping', 60, BLUE, anchor='ma')
    if step >= 2:
        rows = [('Body: finished', GREEN), ('Pad: halfway', RED), ('Hole', INK), ('Fillet: last row', GREEN)]
        for k, (r, col) in enumerate(rows):
            text(d, (1000, 330 + k * 120), r, 60, col)
        text(d, (1000, 860), 'closed is not right:', 58, INK)
        text(d, (1000, 940), 'check the volume', 58, INK)
    if step >= 3:
        d.rounded_rectangle((1880, 360, 2400, 720), radius=90, fill=BREAD, outline=CRUST, width=10)
        for k in range(1, 6):
            x = 1880 + k * 520 / 6
            d.line((x, 380, x, 700), fill=CRUST, width=5)
        text(d, (2140, 780), 'slicer = the loaf', 60, INK, anchor='ma')
        text(d, (2140, 870), 'on its side: 22 min', 56, GREEN, anchor='ma')
        text(d, (2140, 950), '(its estimate)', 50, GREY, anchor='ma')
    save(im, f'card-recap-{step}.png')


def thumbs():
    """Thumbnails (1280 x 720) from the real slicer frames: the Body's file from the back (two holes) beside the Pad's
    (no holes), under 4 words; alt B the question."""
    from PIL import Image
    box = (560, 260, 1400, 1700)
    a = Image.open(os.path.join(L5, 'slicer', 'p2-back.png')).crop(box)
    b = Image.open(os.path.join(L5, 'slicer', 'p7-pad-back.png')).crop(box)
    for name, title in (('thumb-primary.png', 'CHECK PASSED, HOLES GONE'), ('thumb-altA.png', 'WHERE ARE THE HOLES?')):
        im, d = canvas(1280, 720)
        d.rectangle((0, 0, 1280, 150), fill=INK)
        text(d, (640, 75), title, 64, PAPER, anchor='mm')
        for k, (src, col, lab) in enumerate(((a, GREEN, 'the Body'), (b, RED, 'the Pad'))):
            t = src.resize((300, 515))
            x = 190 + k * 600
            im.paste(t, (x, 165))
            d.rectangle((x - 6, 159, x + 306, 686), outline=col, width=10)
            for hy in (978, 1318 - 664 + 978) if False else (654, 1318):   # the hole centres in the frame (x 978)
                cx, cy = x + (978 - box[0]) * 300 / (box[2] - box[0]), 165 + (hy - box[1]) * 515 / (box[3] - box[1])
                d.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), outline=col, width=8)
            chip(d, (x + 150, 620), lab, 50, PAPER, col, anchor='m')
        save(im, name)


if __name__ == '__main__':
    if sys.argv[1:] == ['thumbs']:
        thumbs()
    else:
        card_stl(); card_slicer(); card_flats(); card_compare()
        for i in (1, 2, 3):
            card_recap(i)
        thumbs()
