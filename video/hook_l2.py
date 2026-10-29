"""Lesson 2's contrast pictures (outcome B: FreeCAD's Claude hook stands up, SolidCraft's hung upside down), made only
from real recordings: the SolidCraft course lab's lesson 2 frame (sc2-claude-after.png, Claude's J below its origin)
and this lab's run 1 frame (run1-part.png, Claude's J as it appeared in FreeCAD). Each part is one tight crop; a
drawn dashed line marks Z = 0 in each (SolidCraft: the sketch origin the part hangs from; FreeCAD: the part's lowest
edge, Z 0 measured); the heights are re-typed from the measurements. Overlays are visibly overlays.
Also the thumbnails (1280 x 720, 4 words or fewer).
    docker run --rm --network none -v "<lab>:/work" -w /work cadcmp-openscad:2021.01 python3 video/hook_l2.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ST = os.path.join(LAB, 'out', 'l2', 'stills')
OUT = os.path.join(LAB, 'video', 'frames-l2')
FD = '/usr/share/fonts/truetype/dejavu/'
B, R = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf'
BG, INK, RED, GREEN, AMBER, PAPER, BLUE = (236, 239, 244), (31, 41, 55), (183, 28, 28), (27, 127, 59), (180, 110, 0), \
    (255, 255, 255), (29, 78, 216)
GREY = (110, 120, 138)
# crops in the 2880 x 1800 sources, and where Z = 0 is inside each crop (source y)
SC = ('sc2-claude-after.png', (1880, 560, 2620, 1760), 925)     # hangs from its origin at y 925
FC = ('run1-part.png', (1880, 240, 2510, 1412), 1404)            # stands on its lowest edge at y 1404


def font(p, s):
    return ImageFont.truetype(p, s)


def chip(d, xy, s, size, bg, anchor='m'):
    f = font(B, size)
    w = f.getlength(s)
    x, y = xy
    if anchor == 'm':
        x -= (w + 40) / 2
    d.rounded_rectangle((x, y, x + w + 40, y + size + 36), radius=20, fill=bg)
    d.text((x + 20, y + 16), s, font=f, fill=PAPER)


def crop(spec, h):
    name, box, zy = spec
    im = Image.open(os.path.join(ST, name)).convert('RGB').crop(box)
    k = h / im.height
    im = im.resize((int(im.width * k), h), Image.LANCZOS)
    return im, int((zy - box[1]) * k)


def dashed(d, y, x0, x1, col=AMBER, w=8):
    for x in range(int(x0), int(x1), 34):
        d.line((x, y, min(x + 20, x1), y), fill=col, width=w)


SCV = ('sc2-claude-after.png', (1990, 850, 2500, 1700), 925)   # tighter crops for the 9:16 Short
FCV = ('run1-part.png', (1920, 220, 2500, 1420), 1404)


def crop_w(spec, cw):
    name, box, zy = spec
    im = Image.open(os.path.join(ST, name)).convert('RGB').crop(box)
    k = cw / im.width
    im = im.resize((cw, int(im.height * k)), Image.LANCZOS)
    return im, int((zy - box[1]) * k)


def pair(w, h, top, ph, ranges=True):
    """Two columns, each part ph tall (in 9:16: each as wide as its column), side by side; returns the image."""
    im = Image.new('RGB', (w, h), BG)
    d = ImageDraw.Draw(im)
    if h > w:
        a, za = crop_w(SCV, w // 2 - 20)
        b, zb = crop_w(FCV, w // 2 - 20)
    else:
        a, za = crop(SC, ph)
        b, zb = crop(FC, ph)
    cx = [w // 4, 3 * w // 4]
    k0 = max(0.5, w / 2560) if w >= h else 0.72
    s1, s2, s3 = int(56 * k0), int(54 * k0), int(44 * k0)
    vert = h > w
    for k, (pic, z, label, rng, col) in enumerate(((a, za, 'SolidCraft' if vert else 'SolidCraft · Claude', ('hangs below' if vert else 'hangs below the floor') if ranges else '', RED),
                                                  (b, zb, 'FreeCAD' if vert else 'FreeCAD · Claude', ('stands on it' if vert else 'stands on the floor') if ranges else '', GREEN))):
        x = cx[k] - pic.width // 2
        im.paste(pic, (x, top))
        dashed(d, top + z, x - 20, x + pic.width + 20)
        d.text((x + pic.width - 10, top + z - s3 - 8), 'floor', font=font(B, s3), fill=AMBER, anchor='ra')
        chip(d, (cx[k], top - int(120 * k0)), label, s1, BLUE if k else INK)
        if rng:
            chip(d, (cx[k], top + pic.height + int(24 * k0)), rng, s2, col)
    return im


def thumb(words, colour, name):
    im = pair(1280, 720, 90, 480, ranges=False)
    d = ImageDraw.Draw(im)
    size = 96
    while font(B, size).getlength(words) > 1180:
        size -= 4
    f = font(B, size)
    tw = f.getlength(words)
    d.rounded_rectangle((640 - tw / 2 - 30, 600, 640 + tw / 2 + 30, 706), radius=20, fill=colour)
    d.text((640, 653), words, font=f, fill=PAPER, anchor='mm')
    im.save(os.path.join(OUT, name), quality=92)
    print(name)


def src(name, box):
    return Image.open(os.path.join(ST, name)).convert('RGB').crop(box)


def fit(im, w, h):
    k = min(w / im.width, h / im.height)
    return im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)


def split(name, a, b, la, lb, ca, cb, title):
    """Two real crops side by side (2560 x 1440), each labelled: a before/after or ours/Claude's."""
    im = Image.new('RGB', (2560, 1440), BG)
    d = ImageDraw.Draw(im)
    d.text((1280, 70), title, font=font(B, 80), fill=INK, anchor='ma')
    for k, (pic, lab, col) in enumerate(((a, la, ca), (b, lb, cb))):
        p = fit(pic, 1180, 1080)
        x = 40 + k * 1260 + (1180 - p.width) // 2
        im.paste(p, (x, 200))
        chip(d, (640 + k * 1280, 200 + p.height + 20), lab, 60, col)
    im.save(os.path.join(OUT, name)); print(name)


def cards2():
    hand_sk = os.path.join(LAB, 'out', 'l2', 'hand')
    ins = os.path.join(LAB, 'out', 'l2', 'inspect')
    box = (1400, 250, 2150, 1100)     # cut 2: tight on the dragged corner, so before/after differ at phone size
    s4 = Image.open(os.path.join(hand_sk, 's4-stretched.png')).convert('RGB').crop(box)
    s7 = Image.open(os.path.join(hand_sk, 's7-pinned.png')).convert('RGB').crop(box)
    split('split-stretch.png', s4, s7, 'before the sizes: it stretches', 'fully constrained: it stays', RED, GREEN,
          'Ours: the same corner, dragged')
    s4w = Image.open(os.path.join(hand_sk, 's4-stretched.png')).convert('RGB').crop((1250, 250, 2250, 1650))
    lean = Image.open(os.path.join(ins, 's3-stretched.png')).convert('RGB').crop((1300, 120, 2300, 1350))
    split('split-lean.png', s4w, lean, 'ours, no sizes yet: lines stay level', "Claude's: the plate leans over", AMBER,
          RED, 'No sizes pinned: ours vs Claude\'s')
    # the cause: the two logged lines (re-typed from run 1's transcript) beside SolidCraft's hanging part
    im = Image.new('RGB', (2560, 1440), BG)
    d = ImageDraw.Draw(im)
    d.text((1280, 70), 'Why it stands up in FreeCAD', font=font(B, 80), fill=INK, anchor='ma')
    mono = FD + 'DejaVuSansMono-Bold.ttf'
    d.rounded_rectangle((80, 260, 1400, 760), radius=24, fill=(24, 30, 40))
    for k, ln in enumerate(['xz = [o for o in body.Origin.OutList', '      if o.Role == "XZ_Plane"][0]',
                            'sk.AttachmentSupport = (xz, [""])']):
        d.text((120, 320 + k * 120), ln, font=font(mono, 50), fill=(230, 237, 243))
    chip(d, (740, 800), "run 1's log: the body's own XZ sheet", 54, BLUE)
    chip(d, (740, 920), 'the same sheet we picked: top edge up', 54, GREEN)
    hang, z = crop(SC, 1000)
    im.paste(hang, (1520, 260))
    dashed(d, 260 + z, 1500, 1520 + hang.width + 20)
    chip(d, (1520 + hang.width // 2, 1290), "SolidCraft's plug: top edge down", 54, RED)
    im.save(os.path.join(OUT, 'card-cause.png')); print('card-cause.png')
    # cut 2: the only constraints in run 1's call (re-typed from transcript.jsonl seq 18)
    im = Image.new('RGB', (2560, 1440), BG)
    d = ImageDraw.Draw(im)
    d.text((1280, 70), "Run 1's call: the only pins", font=font(B, 80), fill=INK, anchor='ma')
    d.rounded_rectangle((160, 230, 2400, 1000), radius=24, fill=(24, 30, 40))
    code = ['for i in range(n):', '    a, b = pts[i], pts[(i+1) % n]', '    sk.addGeometry(Part.LineSegment(...))',
            'for i in range(n):', '    sk.addConstraint(Sketcher.Constraint(', '        "Coincident", i, 2, (i+1) % n, 1))',
            'pad.Length = 20']
    for k, ln in enumerate(code):
        col = (255, 214, 102) if 'Coincident' in ln or 'addConstraint' in ln else (230, 237, 243)
        d.text((220, 280 + k * 100), ln, font=font(mono, 54), fill=col)
    chip(d, (1280, 1060), 'Coincident = two ends joined: 8 of them, nothing else', 56, RED)
    chip(d, (1280, 1180), 'no sizes, no level or upright rules', 56, INK)
    im.save(os.path.join(OUT, 'card-code.png')); print('card-code.png')
    # the comparison rows over the two real parts (built in 3 steps)
    rows = [('volume', '8,500 mm³', '8,500 mm³', True), ('size', '25 x 20 x 60', '25 x 20 x 60', True),
            ('height', '0 to 60', '0 to 60', True), ('lowest corner', '0, -20, 0', '0, -20, 0', True),
            ('plane', 'XZ', 'XZ', True), ('steps', 'sketch, pad 20', 'sketch, pad 20', True),
            ('pins', '23', '8', False), ('fully constrained', 'yes', 'no', False)]
    PIN_NOTE = 'ours: 9 joins, 7 level/upright, 1 on an axis, 6 sizes · Claude: 8 joins'
    hand = fit(Image.open(os.path.join(LAB, 'out', 'l2', 'hand', 's10-iso.png')).convert('RGB').crop((1400, 250, 2000, 1300)), 420, 420)
    cl = fit(src('run1-part.png', (1880, 240, 2510, 1412)), 420, 420)
    for n, upto in ((1, 3), (2, 6), (3, 8)):
        im = Image.new('RGB', (2560, 1440), BG)
        d = ImageDraw.Draw(im)
        d.text((1280, 50), 'Side by side, measured by FreeCAD', font=font(B, 76), fill=INK, anchor='ma')
        im.paste(hand, (1180 - hand.width // 2, 150)); im.paste(cl, (1980 - cl.width // 2, 150))
        chip(d, (1180, 590), 'by hand', 52, INK); chip(d, (1980, 590), 'Claude, run 1', 52, BLUE)
        for k, (name, a, b, ok) in enumerate(rows[:upto]):
            y = 700 + k * 88
            col = INK if ok else RED
            d.text((120, y), name, font=font(B if not ok else R, 58), fill=GREY if ok else RED)
            d.text((1180, y), a, font=font(B, 58), fill=INK, anchor='ma')
            d.text((1980, y), b, font=font(B, 58), fill=col, anchor='ma')
            d.text((2420, y), '✓' if ok else '✗', font=font(B, 66), fill=GREEN if ok else RED, anchor='ma')
        if n == 3:
            chip(d, (1280, 1405 - 80), PIN_NOTE, 40, GREY)
            chip(d, (2150, 150), 'run 2 (fresh): the same, 8 pins', 40, BLUE)
        im.save(os.path.join(OUT, f'card-compare-{n}.png')); print(f'card-compare-{n}.png')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    cards2()
    pair(2560, 1440, 200, 1000).save(os.path.join(OUT, 'hook-landscape.png')); print('hook-landscape.png')
    pair(1080, 1920, 420, 1250).save(os.path.join(OUT, 'hook-vertical.png')); print('hook-vertical.png')
    thumb('UPRIGHT, BUT IT STRETCHES', RED, 'thumbnail-primary.jpg')
    thumb('NO SIZES INSIDE', RED, 'thumbnail-altA.jpg')
