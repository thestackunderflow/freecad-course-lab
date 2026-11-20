"""FreeCAD course lesson 13 (Thickness: walls grow inward by default, a box drawn 60 wide is 56 inside; untick
"Make thickness inwards" and the drawn lines stay the inside) cards and panels, SCRIPT-fc13.md rev 2.1 section 3.
The draw_fc12.py pattern on draw_fx20.py / draw_fc10.py helpers: light, 2560 x 1440, each step adds and earlier steps
turn grey, card lines 44 columns, code-panel lines 32 columns (Claude's quoted lines 44, re-wrapped at word gaps,
words unchanged from runs/*/reply.txt), no percent sign, never "tooltip". Every number is NUMBERS.json's (out/fc13) or
a lesson / typed number (tests/test_draw_fc13.py).
  full frame:  card-pad-1..5 (F2, the one illustrated beat), card-why-1..5 (F7), card-second-1..3 (F8), card-end (F15)
  Short 1080 x 1080: card-short-why-1..2 (S1)
  source overlays (RGBA 2880 x 1800, burnt in by mcp-canvas primers/footage-fc13.py):
      ov-block-T     F0 / S0: the composited test block on take T's top view (red where it crosses the walls) + chip
      ov-walls-T     F1: the 2 mm walls drawn thin orange inside the drawn lines (T's top view)
      ov-round-F     F8: the rounded outside edges ringed on take F's iso view
      ov-in-*        "checked by code" panels (63 px): T / M top view under the cup, F iso in the right pane, ...
      ov-cc-*        the panels on Claude's files (under FreeCAD's 3D view, or over the terminal for F13)
      ov-quote-A1-1..3  Claude's reply re-set over the terminal pane, "its reply (words as on screen):"
      card-recap-1..3, card-yourturn-1..4  F14 lower-left panels (no answer)
Geometry (gridded frames, 20 Nov, session scratchpad fc13r/fr): T / M top view: drawn lines (1188, 658)-(2172, 1314),
16.4 px/mm, centre (1680, 986); the right pane free from y 720 (T) / 830 (M, under the Measurement panel); F iso: the
front rounded edge x 1770-1810, y 980-1620, the left one x 1100-1135, y 600-1240.
Run in the draw image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fc13.py
Test: tests/test_draw_fc13.py"""
import json
import os
import sys
import textwrap

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw_fx20 as b  # noqa: E402
import draw_fc10 as f10  # noqa: E402

LAB = b.LAB
OUT = os.path.join(LAB, 'video', 'frames-fc13')
TAKES = os.path.join(LAB, 'out', 'fc13')
W, H, SW, SH = b.W, b.H, b.SW, b.SH
INK, GREY, WHITE, DONE = b.INK, b.GREY, b.WHITE, b.DONE
BLUE, ORANGE, RED, GREEN = b.BLUE, b.ORANGE, b.RED, b.GREEN
ORANGEFILL, BLUEFILL = b.ORANGEFILL, b.BLUEFILL
PARTLINE = f10.PARTLINE
canvas, source, header = b.canvas, b.source, b.header
PROBLEMS, LOG, CUR = b.PROBLEMS, b.LOG, b.CUR
text, code_box = f10.text, f10.code_box
NUM = json.load(open(os.path.join(TAKES, 'NUMBERS.json'), encoding='utf-8'))
BUILD, RUNS = NUM['build'], NUM['runs']
TRAP, FIXED, TYPED_W3 = BUILD['trap'], BUILD['fixed'], BUILD['typed_w3']
FIXED_W3, FIXED_CW70 = BUILD['fixed_w3'], BUILD['fixed_cw70']
PANEL_NAMES = []
# take T / M top view (fitted): the drawn lines and the scale
TOP = (1188, 658, 2172, 1314)
PXMM = 16.4
CC_XY = (1175, 1400)
TERM = (0, 0, 1160, 1800)             # F13: the terminal pane, covered (FreeCAD side only)
B1_ROW15 = (56, 546, 1014, 692)       # B1's table: the 1.5 mm row (never shown; OCR 1.5 / 63 at y 569-601)
PX = 63                               # code panels: 63 px on the 2880 source (fc12 cut 3, phones)


def n0(v):
    return f'{v:g}'


def save(im, name):
    b.OUT = OUT
    b.save(im, name)


def lit(i, step):
    return ORANGE if i == step else DONE


# --- full-frame cards --------------------------------------------------------------------------------------------------
def foam(d, box, col=ORANGE, fill=ORANGEFILL):
    d.rectangle(box, fill=fill, outline=col, width=4)


def card_pad(step):
    """F2: padding a little box (the one illustrated beat). 12 px per mm; the foam 2 thick."""
    im, d = canvas()
    header(d, 'Padding a little box, foam 2 thick')
    k, wl = 12, 56                                   # the foam drawn thick for the picture (sums carry the 2)
    x0, y0, x1, y1 = 240, 380, 960, 860              # the box, 60 across inside
    c1 = INK if step == 1 else DONE
    d.rectangle((x0, y0, x1, y1), outline=c1, width=8)
    text(d, ((x0 + x1) / 2, y0 - 50), '60 inside', 60, c1, anchor='mm')
    if step >= 2:
        foam(d, (x0, y0, x0 + wl, y1), ORANGE if step == 2 else DONE, ORANGEFILL if step == 2 else b.DONEFILL)
        text(d, (x0 + wl + 20, (y0 + y1) / 2), '−2', 64, lit(2, step), anchor='lm')
    if step >= 3:
        foam(d, (x1 - wl, y0, x1, y1), ORANGE if step == 3 else DONE, ORANGEFILL if step == 3 else b.DONEFILL)
        text(d, (x1 - wl - 20, (y0 + y1) / 2), '−2', 64, lit(3, step), anchor='rm')
        text(d, (x0, y1 + 60), f"60 − 2 − 2 = {n0(TRAP['inside_w'])}", 72, lit(3, step))
    if step >= 4:
        X0, X1 = 1540, 2260
        c4 = ORANGE if step == 4 else DONE
        d.rectangle((X0 - wl, y0 - wl, X1 + wl, y1 + wl), fill=ORANGEFILL if step == 4 else b.DONEFILL,
                    outline=c4, width=4)
        d.rectangle((X0, y0, X1, y1), fill=WHITE, outline=INK if step == 4 else DONE, width=8)
        text(d, ((X0 + X1) / 2, y0 - 80), 'foam wrapped round the outside', 52, c4, anchor='mm')
        text(d, ((X0 + X1) / 2, (y0 + y1) / 2 - 40), 'inside still 60', 64, GREEN if step == 4 else DONE,
             anchor='mm')
        text(d, (X0 - wl, y1 + 60), f"outside {n0(FIXED['outside_w'])}", 72, c4)
    if step >= 5:
        d.line((1540 - 24, 1140, 2260 + 24, 1140), fill=ORANGE, width=14)
        d.line((1540 - 24, 1140, 1540 - 24, 1040), fill=INK, width=6)
        d.line((2260 + 24, 1140, 2260 + 24, 1040), fill=INK, width=6)
        text(d, (1900, 1080), '?', 110, ORANGE, anchor='mm')
        text(d, (240, 1110), 'and the floor? (seen from the side)', 64, ORANGE)
    save(im, f'card-pad-{step}.png')


def section(d, box, col, label=None):
    d.rectangle(box, outline=col, width=8)
    if label:
        text(d, ((box[0] + box[2]) / 2, box[1] - 50), label, 56, col, anchor='mm')


def card_why(step):
    """F7: each wall grows inward from the drawn line. Top section (left), side section (right), 12 px per mm;
    build 5 replaces the top section with the outward walls (outside corners rounded, radius = the wall)."""
    im, d = canvas()
    header(d, 'Why 56? Each wall grows inward')
    k = 12
    wl = round(2 * k)
    x0, y0 = 300, 420
    x1, y1 = x0 + 60 * k, y0 + 40 * k                 # 60 x 40 drawn
    if step < 5:
        section(d, (x0, y0, x1, y1), INK if step == 1 else DONE, 'drawn 60 × 40, from above')
        if step >= 2:
            c = ORANGE if step == 2 else DONE
            foam(d, (x0, y0, x0 + wl, y1), c, ORANGEFILL if step == 2 else b.DONEFILL)
            foam(d, (x1 - wl, y0, x1, y1), c, ORANGEFILL if step == 2 else b.DONEFILL)
            text(d, (x0, y1 + 50), f"across: 60 − 2 − 2 = {n0(TRAP['inside_w'])}", 64, c)
        if step >= 3:
            c = ORANGE if step == 3 else DONE
            foam(d, (x0 + wl, y0, x1 - wl, y0 + wl), c, ORANGEFILL if step == 3 else b.DONEFILL)
            foam(d, (x0 + wl, y1 - wl, x1 - wl, y1), c, ORANGEFILL if step == 3 else b.DONEFILL)
            text(d, (x0, y1 + 140), f"front to back: 40 − 2 − 2 = {n0(TRAP['inside_l'])}", 64, c)
    else:
        r = wl                                         # radius 2 = the wall, at this scale
        d.rounded_rectangle((x0 - wl, y0 - wl, x1 + wl, y1 + wl), radius=r, fill=ORANGEFILL, outline=ORANGE,
                            width=4)
        d.rectangle((x0, y0, x1, y1), fill=WHITE, outline=INK, width=8)
        text(d, ((x0 + x1) / 2, y0 - 80), 'walls outside the line instead', 52, ORANGE, anchor='mm')
        text(d, ((x0 + x1) / 2, (y0 + y1) / 2), f"inside {n0(FIXED['inside_w'])}", 72, GREEN, anchor='mm')
        text(d, (x0 - wl, y1 + 60), f"outside 60 + 2 + 2 = {n0(FIXED['outside_w'])}", 64, ORANGE)
    if step >= 4:
        c = ORANGE if step == 4 else DONE
        X0, Y0 = 1500, 420
        X1, Y1 = X0 + 60 * k, Y0 + 50 * k             # 60 wide, 50 tall, from the side
        d.line((X0, Y0, X0, Y1, X1, Y1, X1, Y0), fill=INK if step == 4 else DONE, width=8)
        f10.dashed(d, (X0, Y0), (X1, Y0), c, 5)
        text(d, ((X0 + X1) / 2, Y0 - 50), 'from the side: top open, 0', 56, c, anchor='mm')
        fc = ORANGEFILL if step == 4 else b.DONEFILL
        foam(d, (X0, Y0, X0 + wl, Y1), c, fc)
        foam(d, (X1 - wl, Y0, X1, Y1), c, fc)
        foam(d, (X0 + wl, Y1 - wl, X1 - wl, Y1), c, fc)
        text(d, (X0 + wl + 16, Y1 - wl - 16), 'floor', 52, c, anchor='lb')
        text(d, (X0, Y1 + 50), f"down: 50 − 2 = {n0(TRAP['inside_d'])}", 64, c)
    save(im, f'card-why-{step}.png')


def card_second(step):
    """F8: the second way, full frame (never over the trap cup); each line lit as said."""
    im, d = canvas()
    header(d, 'A second way')
    lines = ['Or keep inward, with names:',
             f"width = inside + 2 × wall ({n0(TYPED_W3['outside_w'])})",
             f"height = inside + 1 wall ({n0(BUILD['typed']['outside_h'])})"]
    for i, ln in enumerate(lines[:step]):
        text(d, (200, 330 + i * 150), ln, 84, BLUE if i == step - 1 else DONE)
    k, wl = 9, 18
    x0, y0 = 1560, 820
    if step >= 2:
        c = BLUE if step == 2 else DONE
        d.rectangle((x0, y0, x0 + 64 * k, y0 + 44 * k), outline=c, width=7)
        f10.dashed(d, (x0 + wl, y0 + wl), (x0 + 64 * k - wl, y0 + wl), c, 4)
        f10.dashed(d, (x0 + wl, y0 + 44 * k - wl), (x0 + 64 * k - wl, y0 + 44 * k - wl), c, 4)
        text(d, (x0 + 32 * k, y0 - 50), 'drawn 64, inside 60', 52, c, anchor='mm')
    if step >= 3:
        c = BLUE
        X0, Y0 = 200, 860
        d.line((X0, Y0, X0, Y0 + 52 * 9, X0 + 60 * 9, Y0 + 52 * 9, X0 + 60 * 9, Y0), fill=c, width=7)
        f10.dashed(d, (X0, Y0 + 52 * 9 - wl), (X0 + 60 * 9, Y0 + 52 * 9 - wl), c, 4)
        text(d, (X0 + 60 * 9 + 40, Y0 + 26 * 9), 'drawn 52 tall:\ninside 50 deep', 52, c, anchor='lm')
    save(im, f'card-second-{step}.png')


def card_end():
    im, d = canvas()
    text(d, (180, 220), 'FreeCAD + Claude course', 72, INK)
    text(d, (180, 330), 'lesson 13: Thickness, walls inward', 60, BLUE)
    shot = Image.open(os.path.join(TAKES, 'F', 'fix-iso.png')).convert('RGB').crop((1000, 250, 2400, 1650))
    im.paste(shot.resize((600, 600)), (180, 450))
    d.rectangle((180, 450, 780, 1050), outline=PARTLINE, width=3)
    text(d, (180, 1080), 'the fixed cup (filmed)', 44, GREY, path=b.R)
    text(d, (180, 1180), 'Lesson 4 · Lesson 1 · the course', 52, INK)
    save(im, 'card-end.png')


def card_short_why(step):
    """S1, 1080 x 1080: 1 the top section, walls inside both lines; 2 the side section, floor only (top open)."""
    CUR.clear()
    fr = (1080, 1080)
    im = Image.new('RGB', fr, WHITE)
    d = ImageDraw.Draw(im)
    k, wl = 10, 20
    x0, y0 = 240, 110
    c1 = ORANGE if step == 1 else DONE
    d.rectangle((x0, y0, x0 + 60 * k, y0 + 40 * k), outline=INK if step == 1 else DONE, width=7)
    foam(d, (x0, y0, x0 + wl, y0 + 40 * k), c1, ORANGEFILL if step == 1 else b.DONEFILL)
    foam(d, (x0 + 60 * k - wl, y0, x0 + 60 * k, y0 + 40 * k), c1, ORANGEFILL if step == 1 else b.DONEFILL)
    text(d, (x0 - 16, y0 + 20 * k), '−2', 56, c1, anchor='rm', frame=fr)
    text(d, (x0 + 60 * k + 16, y0 + 20 * k), '−2', 56, c1, anchor='lm', frame=fr)
    text(d, (540, y0 + 20 * k), f"60 − 2 − 2 = {n0(TRAP['inside_w'])}", 60, c1, anchor='mm', frame=fr)
    if step >= 2:
        X0, Y0 = 290, 640
        k2 = 7
        X1, Y1 = X0 + 60 * k2, Y0 + 240
        d.line((X0, Y0, X0, Y1, X1, Y1, X1, Y0), fill=INK, width=7)
        f10.dashed(d, (X0, Y0), (X1, Y0), ORANGE, 4)
        foam(d, (X0 + 14, Y1 - 14, X1 - 14, Y1))
        text(d, ((X0 + X1) / 2, Y0 - 34), 'top open: 0', 48, ORANGE, anchor='mm', frame=fr)
        text(d, (X1 + 20, Y1 - 10), 'floor −2', 48, ORANGE, anchor='lm', frame=fr, safe=False)
        text(d, (540, Y1 + 70), f"50 − 2 = {n0(TRAP['inside_d'])}", 60, ORANGE, anchor='mm', frame=fr)
    save(im, f'card-short-why-{step}.png')


# --- source overlays ----------------------------------------------------------------------------------------------------
def chip(d, xy, s, px=52):
    f = b.font(b.B, px)
    w = d.textlength(s, font=f)
    x, y = xy
    d.rounded_rectangle((x, y, x + w + 40, y + px + 30), radius=14, fill=WHITE + (240,), outline=PARTLINE + (255,),
                        width=3)
    d.text((x + 20, y + 12), s, font=f, fill=INK + (255,))
    CUR.append((s, round(px * 0.8)))


def ov_block():
    """F0 / S0: a test block 60 x 40 (what I wanted inside), translucent, red where it crosses the 2 mm walls."""
    im, d = source()
    x0, y0, x1, y1 = TOP
    w = round(TRAP['wall_x'] * PXMM)
    d.rectangle((x0 + 4, y0 + 4, x1 - 4, y1 - 4), fill=BLUE + (70,), outline=BLUE + (255,), width=6)
    for box in ((x0 + 4, y0 + 4, x0 + w, y1 - 4), (x1 - w, y0 + 4, x1 - 4, y1 - 4),
                (x0 + w, y0 + 4, x1 - w, y0 + w), (x0 + w, y1 - w, x1 - w, y1 - 4)):
        d.rectangle(box, fill=(220, 38, 38, 210))
    chip(d, (x0, y0 - 110), 'test block, drawn for the picture')
    save(im, 'ov-block-T.png')


def ov_walls():
    """F1: the walls drawn thin orange inside the drawn lines (inward)."""
    im, d = source()
    x0, y0, x1, y1 = TOP
    w = round(TRAP['wall_x'] * PXMM)
    for box in ((x0, y0, x0 + w, y1), (x1 - w, y0, x1, y1)):
        d.rectangle(box, fill=ORANGE + (230,))
    for box in ((x0 + w, y0, x1 - w, y0 + w), (x0 + w, y1 - w, x1 - w, y1)):
        d.rectangle(box, fill=ORANGE + (120,))
    save(im, 'ov-walls-T.png')


def ov_round():
    """F8: the rounded outside edges on take F's iso view, ringed (outlines only)."""
    im, d = source()
    for x, y, w, h in ((1750, 960, 90, 690), (1080, 580, 80, 680)):
        d.rounded_rectangle((x, y, x + w, y + h), radius=30, outline=ORANGE + (255,), width=8)
    save(im, 'ov-round-F.png')


def ov_lines(name, lines, step, box, px=56, k=0.8):
    im, d = source()
    d.rounded_rectangle(box, radius=18, fill=WHITE + (245,), outline=PARTLINE + (255,), width=4)
    f = b.font(b.B, px)
    for i, ln in enumerate(lines[:step]):
        col = (BLUE if i == step - 1 else DONE) + (255,)
        CUR.append((ln, round(px * k)))
        xy = (box[0] + 32, box[1] + 36 + i * round(px * 1.7))
        d.text(xy, ln, font=f, fill=col)
        bb = d.textbbox(xy, ln, font=f)
        if bb[2] > box[2] or bb[3] > box[3]:
            PROBLEMS.append(f'{ln!r}: outside its panel {bb}')
    save(im, f'{name}-{step}.png')


def code_panel(name, lines, xy, px=PX, k=0.8, title='checked by code', white=()):
    im, d = source()
    for box in white:                 # painted white under the panel (a re-mask that rides with the overlay)
        d.rectangle(box, fill=(255, 255, 255, 255))
    code_box(d, xy[0], xy[1], lines, title, px, k)
    for t in lines:
        if len(t) > 32:
            PROBLEMS.append(f'{t!r}: code panel line over 32')
    save(im, name)
    PANEL_NAMES.append(name)


def wrap(s, width=36):
    return textwrap.wrap(s, width, break_long_words=False, break_on_hyphens=False)


def quote(name, run, lines, extra=(), y=260, px=52, white=()):
    reply = ' '.join(open(os.path.join(TAKES, 'runs', run, 'reply.txt'), encoding='utf-8').read().split())
    assert ' '.join(lines) in reply, lines
    im, d = source()
    for box in white:
        d.rectangle(box, fill=(255, 255, 255, 255))
    code_box(d, 20, y, list(lines) + list(extra), 'its reply (words as on screen):', px, 0.8)
    save(im, name)
    PANEL_NAMES.append(name)


RECAP = ['Thickness grows walls inward by default', 'Across: 2 walls. Down: 1 (top open)',
         'Untick it: your lines stay the inside']
TURN = ['Your turn: draw a box 80 wide, 50 tall', 'Walls 3, inward, top open', 'Inside width? How deep?',
        'Hint: walls across? walls down?']


def ins(v, depth=True):
    s = f"inside: {n0(v['inside_w'])} × {n0(v['inside_l'])}"
    return s + (f", {n0(v['inside_d'])} deep" if depth else '')


def panels():
    code_panel('ov-in-T.png', [ins(TRAP)], (600, 1350))                     # F0 / F5 (T / M top view, under the cup)
    code_panel('ov-in-T-s.png', [ins(TRAP, False)], (1120, 1360))           # S0 (inside the Short's square crop)
    code_panel('ov-in-F1.png', [ins(FIXED, False)], (2200, 760))            # F1 (F iso, right pane)
    code_panel('ov-in-F8.png', [ins(FIXED), f"outside: {n0(FIXED['outside_w'])} × {n0(FIXED['outside_l'])}"],
               (600, 1350))                                                 # F8 (F top view)
    code_panel('ov-in-P9a.png', [f"outward, wall {n0(FIXED_W3['wall_x'])}:",
                                 f"inside {n0(FIXED_W3['inside_w'])} × {n0(FIXED_W3['inside_l'])}, wall 3",
                                 f"outside {n0(FIXED_W3['outside_w'])} × {n0(FIXED_W3['outside_l'])}"], (480, 1330))
    code_panel('ov-in-P9b.png', [f"typed {n0(TYPED_W3['outside_w'])}, inward, wall 3:",
                                 f"64 − 3 − 3 = {n0(TYPED_W3['inside_w'])}"], (1440, 1330))
    code_panel('ov-in-S2.png', [f"wall 3: inside {n0(FIXED_W3['inside_w'])} × {n0(FIXED_W3['inside_l'])}"],
               (1120, 1360))                                                # S2 (P top view, the Short's crop)
    a, bb = RUNS['A1']['score']['detail'], RUNS['B1']['score']['detail']
    code_panel('ov-cc-A1.png', [f"wall 2: inside {n0(a['at_wall'][0])} × {n0(a['at_wall'][1])}",
                                f"wall 3: inside {n0(a['at_wall3'][0])} × {n0(a['at_wall3'][1])}"], CC_XY,
               title='checked by code (its file):')
    code_panel('ov-cc-B1.png', [f"wall 2: {n0(bb['at_wall'][0])} × {n0(bb['at_wall'][1])}, "
                                f"{n0(bb['at_wall'][2])} deep",
                                f"wall 3: {n0(bb['at_wall3'][0])} × {n0(bb['at_wall3'][1])}, "
                                f"{n0(bb['at_wall3'][2])} deep"], CC_XY, title='checked by code (its file):',
               white=[B1_ROW15])
    assert a['at_wall3'] == bb['at_wall3'] and a['at_width70'] == bb['at_width70']
    both1 = [f"wall 3: {n0(a['at_wall3'][0])} × {n0(a['at_wall3'][1])} (both)",
             f"width 70: {n0(a['at_width70'][0])} × {n0(a['at_width70'][1])} (both)"]
    code_panel('ov-cc-both-1.png', both1, (20, 420), title='checked by code (its files):', white=[TERM])
    code_panel('ov-cc-both-2.png', both1 + [f"both: {n0(a['at_wall'][2])} deep at wall 2", 'fix: cup_height + wall'],
               (20, 420), title='checked by code (its files):', white=[TERM])
    quote('ov-quote-A1-1.png', 'A1', wrap('The sketch is the outer profile, and the Thickness feature cuts inward.'))
    quote('ov-quote-A1-2.png', 'A1', ['- cup_width is now Params.cup_width + 2 *', 'Params.wall.',
                                      '- cup_length is now Params.cup_length + 2 *', 'Params.wall.'])
    quote('ov-quote-A1-3.png', 'A1', wrap('I checked this by slicing the model at mid-height'),
          ['', 'Wall  Inside', '2     60 × 40', '3     60 × 40'])
    quote('ov-quote-B1.png', 'B1', ["I measured it from the model's inner faces."], y=540, px=44,
          white=[B1_ROW15])


def main():
    os.makedirs(OUT, exist_ok=True)
    b.OUT = OUT
    PROBLEMS.clear()
    LOG.clear()
    PANEL_NAMES.clear()
    for s in range(1, 6):
        card_pad(s)
    for s in range(1, 6):
        card_why(s)
    for s in range(1, 4):
        card_second(s)
    card_end()
    for s in (1, 2):
        card_short_why(s)
    ov_block()
    ov_walls()
    ov_round()
    for s in range(1, 4):
        ov_lines('card-recap', RECAP, s, (20, 1200, 1500, 1720))
    for s in range(1, 5):
        ov_lines('card-yourturn', TURN, s, (20, 1100, 1420, 1720), px=54)
    panels()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
