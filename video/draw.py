"""Lesson 1's diagram cards and thumbnails. Diagrams are visibly diagrams (flat shapes, no fake UI); every number comes
from a lab file (out/l1/compare.json, hand/measure.json, runs/claude-1/measure.json). Thumbnails are real frames from
the lab recordings plus 4 words. Cards are 2560 x 1440 (they fill the frame), text 64 px or more.
    docker run --rm --network none -v "<lab>:/work" -w /work cadcmp-openscad:2021.01 python3 video/draw.py
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
L1 = os.path.join(LAB, 'out', 'l1')
OUT = os.path.join(LAB, 'video', 'frames')
os.makedirs(OUT, exist_ok=True)
FD = '/usr/share/fonts/truetype/dejavu/'
B, R = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf'
BG, INK, RED, GREEN, GREY, BLUE, PAPER, AMBER, WALL = (236, 239, 244), (31, 41, 55), (183, 28, 28), (27, 127, 59), \
    (110, 120, 138), (29, 78, 216), (255, 255, 255), (180, 110, 0), (214, 200, 178)
W, H = 2560, 1440
CMP = json.load(open(os.path.join(L1, 'compare.json')))


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
    d.rounded_rectangle((x, y, x + w + 2 * pad, y + size + 2 * pad), radius=22, fill=bg)
    d.text((x + pad, y + pad), s, font=f, fill=fg)


def box(d, xy, label, sub=None, fill=PAPER, outline=INK):
    x0, y0, x1, y1 = xy
    d.rounded_rectangle(xy, radius=36, fill=fill, outline=outline, width=8)
    text(d, ((x0 + x1) / 2, y0 + 90), label, 84, anchor='mm')
    if sub:
        text(d, ((x0 + x1) / 2, y0 + 190), sub, 60, GREY, R, anchor='mm')


def header(d, s):
    text(d, (W / 2, 110), s, 92, anchor='mm')


def workshop(d, socket_on=None, plug=None, steps=False):
    """The map: the Claude app (left) and the workshop (right) with a socket in its wall."""
    box(d, (120, 420, 900, 1060), 'Claude app', 'Claude Code')
    # the workshop: a house shape with a wall on its left side
    d.polygon([(1500, 520), (2000, 300), (2460, 520)], fill=WALL, outline=INK)
    d.rectangle((1500, 520, 2460, 1160), fill=PAPER, outline=INK, width=8)
    d.line((1500, 300, 1500, 300), fill=INK)
    text(d, (1980, 640), 'FreeCAD', 84, anchor='mm')
    text(d, (1980, 740), 'the workshop', 64, GREY, R, anchor='mm')
    if socket_on is not None:
        c = GREEN if socket_on else GREY
        d.rounded_rectangle((1440, 760, 1560, 960), radius=24, fill=c, outline=INK, width=6)
        d.ellipse((1470, 805, 1500, 835), fill=INK)
        d.ellipse((1470, 885, 1500, 915), fill=INK)
        text(d, (1980, 900), 'socket = the add-on', 64, anchor='mm')
        text(d, (1980, 990), 'ON' if socket_on else 'OFF', 72, c, anchor='mm')
    if plug:
        x1 = 1430 if plug == 'in' else 1250
        d.line((900, 860, x1 - 150, 860), fill=BLUE, width=18)
        d.rounded_rectangle((x1 - 150, 790, x1, 930), radius=20, fill=BLUE)
        d.rectangle((x1, 815, x1 + (12 if plug == 'in' else 40), 835), fill=INK)
        d.rectangle((x1, 885, x1 + (12 if plug == 'in' else 40), 905), fill=INK)
        text(d, (1170, 760), 'plug = MCP server', 60, BLUE, anchor='mm')
    if steps:
        for k, s in enumerate(['1  FreeCAD', '2  the add-on', '3  uv', '4  the plug line']):
            chip(d, (140 + k * 600, 1220), s, 56, PAPER, INK if k else BLUE)


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(name)


def cards():
    im, d = canvas(); header(d, "Claude can't reach inside FreeCAD by itself"); workshop(d, socket_on=False)
    save(im, 'card-socket-off.png')
    im, d = canvas(); header(d, 'A socket in the wall: the add-on'); workshop(d, socket_on=True)
    chip(d, (1560, 1200), 'this computer only', 60, PAPER, GREEN)
    save(im, 'card-socket-on.png')
    im, d = canvas(); header(d, 'Your Claude app needs a plug'); workshop(d, socket_on=True, plug='out')
    save(im, 'card-plug-out.png')
    im, d = canvas(); header(d, 'The Claude app starts the plug and pushes it in'); workshop(d, socket_on=True, plug='in')
    chip(d, (300, 1200), 'started by your Claude app', 60, PAPER, BLUE)
    save(im, 'card-plug-in.png')
    im, d = canvas(); header(d, 'Set it up in four steps'); workshop(d, socket_on=True, plug='in', steps=True)
    save(im, 'card-steps.png')
    # the course's wall hook, side view, with the back plate (lesson 1's block) lit
    im, d = canvas(); header(d, 'The wall hook: lesson 1 makes the back plate')
    s, x0, y0 = 14, 1000, 1300                     # 14 px per mm; the J's corner (0, 0) at (x0, y0)
    pts = [(0, 0), (25, 0), (25, 10), (20, 10), (20, 5), (5, 5), (5, 60), (0, 60)]
    d.polygon([(x0 + x * s, y0 - y * s) for x, y in pts], fill=(200, 210, 225), outline=INK)
    d.rectangle((x0, y0 - 60 * s, x0 + 5 * s, y0), fill=AMBER, outline=INK, width=6)
    text(d, (x0 - 40, y0 - 30 * s), 'back plate', 64, AMBER, anchor='rm')
    text(d, (x0 - 40, y0 - 30 * s + 90), '5 x 20 x 60 mm', 60, INK, R, anchor='rm')
    text(d, (x0 + 26 * s + 60, y0 - 8 * s), 'later lessons: the arm and the lip', 56, GREY, R, anchor='lm')
    save(im, 'card-hook-plate.png')
    # the comparison, one row at a time (numbers from compare.json)
    rows = CMP['rows']
    lines = [('volume', f"{rows['volume']['hand']:,.0f} mm³", f"{rows['volume']['claude']:,.0f} mm³"),
             ('size', ' x '.join(f'{v:g}' for v in rows['size']['hand']), ' x '.join(f'{v:g}' for v in rows['size']['claude'])),
             ('corner at', ', '.join(f'{v:g}' for v in rows['position']['hand']), ', '.join(f'{v:g}' for v in rows['position']['claude'])),
             ('height', f"{rows['up']['hand'][0]:g} to {rows['up']['hand'][1]:g}", f"{rows['up']['claude'][0]:g} to {rows['up']['claude'][1]:g}")]
    for n in range(1, 5):
        im, d = canvas(); header(d, 'Side by side, measured by FreeCAD')
        text(d, (1180, 330), 'by hand', 80, anchor='mm'); text(d, (1980, 330), 'Claude', 80, BLUE, anchor='mm')
        for k, (name, a, b) in enumerate(lines[:n]):
            y = 520 + k * 210
            text(d, (180, y), name, 76, GREY, B, anchor='lm')
            text(d, (1180, y), a, 76, anchor='mm'); text(d, (1980, y), b, 76, BLUE, anchor='mm')
            ok = rows[['volume', 'size', 'position', 'up'][k]]['ok']
            text(d, (2400, y), '✓' if ok else '✗', 100, GREEN if ok else RED, anchor='mm')
        if n == 4:
            rep = json.load(open(os.path.join(L1, 'replay', 'measure.json')))['solids'][0]['volume_mm3']
            chip(d, (W / 2, 1250), f'no-AI replay of Claude\'s calls: {rep:,.0f} mm³', 60, PAPER, GREEN, anchor='m')
        save(im, f'card-compare-{n}.png')
    # recap: the map with its three sentences and the two measurements
    im, d = canvas(); header(d, 'Remember the picture'); workshop(d, socket_on=True, plug='in')
    chip(d, (140, 1200), 'by hand: 6,000 mm³', 60, PAPER, INK); chip(d, (1500, 1200), 'Claude: 6,000 mm³', 60, PAPER, BLUE)
    save(im, 'card-recap.png')
    # cut 2 (watch-through c1: the recap card held 27 s): the recap builds one piece at a time, then the outro
    im, d = canvas(); header(d, 'Remember the picture'); workshop(d)
    save(im, 'card-recap-1.png')
    im, d = canvas(); header(d, 'Remember the picture'); workshop(d, socket_on=True)
    save(im, 'card-recap-2.png')
    im, d = canvas(); header(d, 'Remember the picture'); workshop(d, socket_on=True, plug='in')
    save(im, 'card-recap-3.png')
    im, d = canvas(); header(d, "FreeCAD's own numbers are the proof"); workshop(d, socket_on=True, plug='in')
    chip(d, (140, 1200), 'by hand: 6,000 mm³', 60, PAPER, INK); chip(d, (1500, 1200), 'Claude: 6,000 mm³', 60, PAPER, BLUE)
    save(im, 'card-recap-4.png')
    for n, extra in ((1, None), (2, 'A like helps other developers find it')):
        im, d = canvas()
        text(d, (W / 2, 420), 'FreeCAD + Claude Course', 110, anchor='mm')
        text(d, (W / 2, 590), 'lesson 1: connect Claude, make a first part', 72, GREY, R, anchor='mm')
        chip(d, (W / 2, 760), 'every lesson, in order: the course playlist', 64, PAPER, BLUE, anchor='m')
        text(d, (W / 2, 1000), 'FreeCAD 1.1.4 · freecad-mcp 0.1.28 · Claude Code 2.1.308 · filmed on Linux', 52, GREY, R, anchor='mm')
        if extra:
            chip(d, (W / 2, 1120), extra, 60, PAPER, GREEN, anchor='m')
        save(im, f'card-outro-{n}.png')


def thumb(src_png, crop, name, words, color):
    base = Image.open(src_png).convert('RGB').crop(crop).resize((1280, 720), Image.LANCZOS)
    d = ImageDraw.Draw(base)
    size = 112
    while font(B, size).getlength(words) > 1120:
        size -= 4
    f = font(B, size)
    w = f.getlength(words)
    d.rounded_rectangle((640 - w / 2 - 36, 540, 640 + w / 2 + 36, 690), radius=28, fill=color)
    d.text((640, 615), words, font=f, fill=PAPER, anchor='mm')
    base.save(os.path.join(OUT, name), quality=92)
    print(name)


if __name__ == '__main__':
    cards()
    st = os.path.join(L1, 'stills')
    if os.path.exists(os.path.join(st, 'fail-block.png')):
        thumb(os.path.join(st, 'fail-block.png'), (0, 0, 2880, 1620), 'thumbnail-primary.jpg', 'IT WORKS: 6,000 mm³', GREEN)
    if os.path.exists(os.path.join(st, 'fail-connected.png')):
        thumb(os.path.join(st, 'fail-connected.png'), (0, 0, 2880, 1620), 'thumbnail-altA.jpg', 'CONNECTED, BUT?', RED)
