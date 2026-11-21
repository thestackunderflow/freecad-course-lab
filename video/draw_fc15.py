"""FreeCAD course lesson 15 (a soft rim on the hanging cup: a Fillet of 3 on a 2 mm wall fails with "Input error";
1.5 builds with 0.50 of flat; an inside round of 1 fails because both rounds share the wall's top; wall 3 holds both)
cards and panels, SCRIPT-fc15.md rev 2.1 section 3. The draw_fc14.py pattern on draw_fx20.py / draw_fc10.py helpers:
light, 2560 x 1440, each step adds and earlier steps turn grey, card lines 44 columns, chips / insets / code-panel lines
32, no percent sign, never "tooltip" or "shell" (FreeCAD's feature is Thickness), never the error string (plain
words). The chips with ">" are drawn here (YouTube text never has one). Every number is NUMBERS.json's (out/fc15) or
a lesson / typed number (tests/test_draw_fc15.py). The section is the wall cut at y 0 (a straight side, where the
Thickness's round outside corners do not show), so the drawings need no corner radius.
  full frame:  card-round-1..3 (F1), card-coin-1..3 (F2, the one illustrated analogy beat: a coin traced into the
               corner of a 2 mm card strip; build 3 = coins 1.5 and 1 overlapping), card-why-1..4 (F6), card-rule-1..3
               (F9), still-after-A1 / -B1 (F14: runs/*/after.png + the panel beside), card-end (F16)
  Short:       card-why-s1..3 (S1, 1080 x 1080), card-short-head (1080 x 1920: the frame-1 headline words)
  source overlays (RGBA 2880 x 1800, burnt in by mcp-canvas primers/footage-fc15.py):
      ov-chips-T     F0 / S0: "round 3, wall 2" and "3 > 2" + the rim ringed on T's end state (44.5)
      ov-box-T/-I    F4 / F8: the box's message line ringed (box x 1196-1684, y 790-990; the line y 815-870)
      ov-rim-R       F3 / F6 / S1: the flat top ringed in R's rim zoom (39.8-44.0)
      ov-corner-R    F3: a round outside corner (up and down) ringed in R's isometric view
      ov-flat-F      F9: the leftover flat ringed in F's rim zoom (118.1-126.0)
      ov-err-P       F10: the Fillet001 row (centre y 568) ringed
      ov-sum-I / ov-fits-P / ov-w3-P / ov-w2-P   S2 / F10: the sums drawn ("1.5 + 1 = 2.5 > 2" etc.)
      ov-in-* / ov-cc-* / ov-log-*   "checked by code" / "from the run log" panels (63 px)
      rc-1..3, yt-1  F15 lower-left recap and your-turn panels (no answer); sub-1..2 F11 lower thirds
Geometry (gridded frames + OCR, 21 Nov, session scratchpad fc15r): T 44.5 the cup x 1200-2200, y 325-1550, the box
x 1196-1684, y 790-990 ("BRep..." line x 1339-1660, y ~840, OK 1533 / 936); tree rows (centre y) Pad 439, Thickness
471, Pad001 504, Fillet 536, Fillet001 568; Params rows y 410 + 54 n (wall 572, rim_out 734, rim_in 788); Measure
"Result: 0.50 mm" x 2201-2445, y 775.
Run in the draw image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fc15.py
Test: tests/test_draw_fc15.py"""
import json
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw_fx20 as b  # noqa: E402
import draw_fc10 as f10  # noqa: E402

LAB = b.LAB
OUT = os.path.join(LAB, 'video', 'frames-fc15')
TAKES = os.path.join(LAB, 'out', 'fc15')
W, H, SW, SH = b.W, b.H, b.SW, b.SH
INK, GREY, WHITE, DONE = b.INK, b.GREY, b.WHITE, b.DONE
BLUE, ORANGE, RED, GREEN = b.BLUE, b.ORANGE, b.RED, b.GREEN
ORANGEFILL, BLUEFILL, DONEFILL = b.ORANGEFILL, b.BLUEFILL, b.DONEFILL
PARTLINE = f10.PARTLINE
CLAY, CARD, COIN = (253, 220, 180), (250, 247, 240), (202, 138, 4)
canvas, source, header = b.canvas, b.source, b.header
PROBLEMS, LOG, CUR = b.PROBLEMS, b.LOG, b.CUR
code_box = f10.code_box
NUM = json.load(open(os.path.join(TAKES, 'NUMBERS.json'), encoding='utf-8'))
G0, RUNS = NUM['G0'], NUM['runs']
PRM, FIX, W3, W26, W24 = (G0['params'], G0['fix_r1_5'], G0['walls']['wall_3_0'], G0['walls']['wall_2.6_2'],
                          G0['walls']['wall_2.4_3'])
WALL, ROUT, RIN = PRM['wall'], PRM['rim_out'], PRM['rim_in']
FIXR = FIX['round_radii']['out'][0]
PANEL_NAMES = []
PX = 63
RIM_T = (1200, 300, 1720, 660)          # T 44.5: the rim's back-left corner (the box covers the middle)
BOX_LINE = (1316, 806, 1684, 880)       # the box's message line (T 43.7-50.7, I 67.0-74.1)
RIM_R = (1440, 760, 1980, 1160)         # R 39.8-44.0: the flat top band, mid frame
CORNER_R = (1780, 900, 1930, 1560)      # R iso: the front outside corner (up and down)
FLAT_F = (1240, 640, 2000, 1140)        # F 118.1-126.0: the band with the 1.5 round and its flat
ROW_F001 = (36, 546, 480, 592)          # P 198.4+: the Fillet001 row
CHIP_XY = (520, 1150)                   # in the 3D view, left of the cup, inside the Short's square crop
CC_XY = (1175, 1360)


def n0(v):
    return f'{v:g}'


def f2(v):
    return f'{v:.2f}'


def text(d, xy, s, size=56, fill=INK, **kw):
    """f10.text, except a drawn ">" is allowed (the chips with sums are pictures, never YouTube text)."""
    n = len(PROBLEMS)
    bb = f10.text(d, xy, s, size, fill, **kw)
    if '>' in s and '<' not in s:
        PROBLEMS[n:] = [p for p in PROBLEMS[n:] if not p.endswith('angle bracket')]
    return bb


def save(im, name):
    b.OUT = OUT
    b.save(im, name)


def lit(i, step, on=ORANGE):
    return on if i == step else DONE


def chip_on(d, xy, s, col=ORANGE, px=52, frame=(W, H)):
    """A chip on a card: rounded light box, coloured words (logged); two lines when s has a newline."""
    f = b.font(b.B, px)
    lines = s.split('\n')
    w = max(d.textlength(x, font=f) for x in lines)
    x, y = xy
    d.rounded_rectangle((x, y, x + w + 40, y + (px + 14) * len(lines) + 16), radius=14, fill=WHITE, outline=col,
                        width=4)
    for i, ln in enumerate(lines):
        text(d, (x + 20, y + 12 + i * (px + 14)), ln, px, col, frame=frame)


# --- the wall section (cut at y 0: a straight side) ---------------------------------------------------------------------
def section(d, x0, yt, yb, k, out=None, inn=None, big=None, out_col=ORANGE, in_col=BLUE, big_col=RED, fill=CLAY,
            w=None):
    """The wall strip from x0 (outside) to x0 + wall * k (the cup's inside on the right), top yt. `out` / `inn`: a
    round that is cut (radius in mm); `big`: a radius past the strip, drawn as its arc only, its landing point red."""
    wl = (w if w is not None else WALL) * k
    x1 = x0 + wl
    d.rectangle((x0, yt, x1, yb), fill=fill)
    if out:
        r = out * k
        d.rectangle((x0, yt, x0 + r, yt + r), fill=WHITE)
        d.pieslice((x0, yt, x0 + 2 * r, yt + 2 * r), 180, 270, fill=fill)
    if inn:
        r = inn * k
        d.rectangle((x1 - r, yt, x1, yt + r), fill=WHITE)
        d.pieslice((x1 - 2 * r, yt, x1, yt + 2 * r), 270, 360, fill=fill)
    d.line((x0, yb, x0, yt + (out * k if out else 0)), fill=INK, width=6)
    d.line((x1, yb, x1, yt + (inn * k if inn else 0)), fill=INK, width=6)
    d.line((x0 + (out * k if out else 0), yt, x1 - (inn * k if inn else 0), yt), fill=INK, width=6)
    if out:
        r = out * k
        d.arc((x0, yt, x0 + 2 * r, yt + 2 * r), 180, 270, fill=out_col, width=9)
    if inn:
        r = inn * k
        d.arc((x1 - 2 * r, yt, x1, yt + 2 * r), 270, 360, fill=in_col, width=9)
    if big:
        r = big * k
        d.arc((x0, yt, x0 + 2 * r, yt + 2 * r), 180, 270, fill=big_col, width=9)
        d.line((x1, yt, x0 + r + 30, yt), fill=big_col, width=4)
        d.ellipse((x0 + r - 14, yt - 14, x0 + r + 14, yt + 14), fill=big_col)
    return x1


def width_mark(d, x0, x1, y, s, col=INK, px=52, frame=(W, H)):
    f10.biarrow(d, x0 + 4, y, x1 - 4, y, col, w=5, s=20)
    text(d, ((x0 + x1) / 2, y - 16), s, px, col, anchor='md', frame=frame)


def overlap_bar(d, xa, xb, yt, col=RED):
    d.rectangle((min(xa, xb), yt - 26, max(xa, xb), yt - 8), fill=col)


# --- F1: a round, its radius --------------------------------------------------------------------------------------------
def card_round(step):
    """F1: 1 a sharp edge; 2 the edge as a curve, radius 1 with its arrow, "round = Fillet"; 3 radius 3 past the
    strip, "3 > 2" beside "the cup's side, 2 thick"; 4 (cut 1 review: one idea per step) adds a small inside curve,
    "same 2"."""
    im, d = canvas()
    header(d, 'A round swaps a sharp edge for a curve')
    k, x0, yt, yb = 170, 900, 520, 1260
    if step == 1:
        x1 = section(d, x0, yt, yb, k)
        f10.harrow(d, 600, 380, x0 - 6, yt - 6, ORANGE, w=7)
        chip_on(d, (200, 300), 'sharp edge', ORANGE)
    elif step == 2:
        x1 = section(d, x0, yt, yb, k, out=RIN)
        r = RIN * k
        f10.harrow(d, x0 + r, yt + r, x0 + r - r * 0.7071, yt + r - r * 0.7071, ORANGE, w=6, s=22)
        text(d, (x0 + r + 20, yt + r + 10), 'radius 1', 52, ORANGE)
        chip_on(d, (200, 300), 'round = Fillet', ORANGE)
    else:
        x1 = section(d, x0, yt, yb, k, inn=RIN if step == 4 else None, big=ROUT, out_col=DONE, in_col=BLUE)
        r = ROUT * k
        f10.harrow(d, x0 + r, yt + r, x0 + r - r * 0.7071, yt + r - r * 0.7071, RED, w=6, s=22)
        text(d, (x0 + r + 20, yt + r + 10), 'radius 3', 52, RED)
        chip_on(d, (200, 300), 'round = Fillet', DONE)
        chip_on(d, (1700, 520), '3 > 2', RED if step == 3 else DONE, px=72)
        if step == 4:
            chip_on(d, (1700, 900), 'same 2', BLUE)
    width_mark(d, x0, x1, yb + 70, "the cup's side, 2 thick", INK if step == 3 else DONE)
    save(im, f'card-round-{step}.png')


# --- F2: a coin traced into the corner of a strip of card ---------------------------------------------------------------
def coin(d, cx, cy, r, col=COIN):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=7)


def card_coin(step):
    """F2 (the one illustrated beat): 1 a strip of card 2 wide, its corner; 2 a coin the size of a round of 3 laid in
    the corner touching both edges: it touches the top past the far edge, the traced curve red, "no room to land";
    3 coins of 1.5 and 1, one in each top corner: their traced curves overlap in the middle."""
    im, d = canvas()
    header(d, 'Rounding a corner of a strip of card')
    k, x0, yt, yb = 150, 1100, 380, 1250
    x1 = x0 + WALL * k
    d.rectangle((x0, yt, x1, yb), fill=CARD, outline=INK, width=5)
    width_mark(d, x0, x1, yt - 70, '2 mm', INK if step == 1 else DONE)
    if step == 1:
        f10.harrow(d, 800, 300, x0 - 8, yt + 4, ORANGE, w=7)
        chip_on(d, (300, 400), 'its corner', ORANGE)
        r = 0.6 * k     # cut 1 review: the coin the words describe, laid in the corner, touching both edges
        coin(d, x0 + r, yt + r, r)
        d.arc((x0, yt, x0 + 2 * r, yt + 2 * r), 180, 270, fill=ORANGE, width=10)
        chip_on(d, (160, 560), 'a coin, touching both edges', COIN)
    if step == 2:
        r = ROUT * k
        coin(d, x0 + r, yt + r, r)
        d.arc((x0, yt, x0 + 2 * r, yt + 2 * r), 180, 270, fill=RED, width=10)
        d.ellipse((x0 + r - 16, yt - 16, x0 + r + 16, yt + 16), fill=RED)
        text(d, (x0 + r, yt + r), 'coin, size 3', 52, COIN, anchor='mm')
        chip_on(d, (260, 560), 'no room to land', RED)
    if step == 3:
        ro, ri = FIXR * k, RIN * k
        coin(d, x0 + ro, yt + ro, ro)
        coin(d, x1 - ri, yt + ri, ri, BLUE)
        d.arc((x0, yt, x0 + 2 * ro, yt + 2 * ro), 180, 270, fill=ORANGE, width=10)
        d.arc((x1 - 2 * ri, yt, x1, yt + 2 * ri), 270, 360, fill=BLUE, width=10)
        overlap_bar(d, x0 + ro, x1 - ri, yt + 4)
        text(d, (x0 - 30, yt + ro), '1.5', 56, ORANGE, anchor='rm')
        text(d, (x1 + 30, yt + ri), '1', 56, BLUE, anchor='lm')
        chip_on(d, (1700, 560), 'two rounds,\none 2 mm', RED)
    save(im, f'card-coin-{step}.png')


# --- F6: why, the section ------------------------------------------------------------------------------------------------
def card_why(step):
    """F6: 1 the drawn section, the strip 2 wide; 2 a radius of 3 swings from the outside edge past the strip, red;
    3 "room on top: 2" / "round needs: 3"; 4 it shrinks to 1.5 and lands: "2 − 1.5 = 0.5"."""
    im, d = canvas()
    header(d, 'Cut the wall straight down: a section')
    k, x0, yt, yb = 200, 760, 420, 1240
    if step <= 3:
        x1 = section(d, x0, yt, yb, k, big=ROUT if step >= 2 else None)
    else:
        x1 = section(d, x0, yt, yb, k, out=FIXR, out_col=GREEN)
        d.line((x0 + FIXR * k, yt - 4, x1, yt - 4), fill=GREEN, width=12)
    width_mark(d, x0, x1, yb + 70, 'wall 2', INK if step == 1 else DONE)
    text(d, (x0 - 40, 760), 'outside', 52, GREY, anchor='rm')
    text(d, (x1 + 60, 1000), 'inside of the cup', 52, GREY)
    if step >= 2 and step <= 3:
        text(d, (x0 + ROUT * k + 30, yt + 60), 'radius 3', 56, RED)
    if step >= 3:
        chip_on(d, (1700, 520), 'room on top: 2', lit(3, step, BLUE))
        chip_on(d, (1700, 640), 'round needs: 3', lit(3, step, RED))
    if step >= 4:
        text(d, (x0 + FIXR * k + 20, yt + FIXR * k + 20), 'radius 1.5', 52, GREEN)
        chip_on(d, (1700, 820), '2 − 1.5 = 0.5', GREEN, px=64)
    save(im, f'card-why-{step}.png')


# --- F9: the rule --------------------------------------------------------------------------------------------------------
def card_rule(step):
    """F9: 1 the section with the 1.5 round, its flat 0.5 lit; 2 a round of 1 from the inside edge, the overlap red,
    "1.5 + 1 = 2.5 > 2"; 3 the rule: "rim out + rim in" / "less than the wall"."""
    im, d = canvas()
    header(d, 'Both rounds share the same top')
    k, x0, yt, yb = 200, 760, 420, 1240
    if step == 1:
        x1 = section(d, x0, yt, yb, k, out=FIXR, out_col=ORANGE)
        d.line((x0 + FIXR * k, yt - 4, x1, yt - 4), fill=GREEN, width=12)
        chip_on(d, (1700, 520), f"leftover flat {n0(FIX['flat'])}", GREEN)
    else:
        x1 = section(d, x0, yt, yb, k, out=FIXR, inn=RIN, out_col=DONE if step == 3 else ORANGE,
                     in_col=DONE if step == 3 else BLUE)
        overlap_bar(d, x0 + FIXR * k, x1 - RIN * k, yt, RED if step == 2 else DONE)
        text(d, (x0 - 30, yt + 200), 'rim out 1.5', 52, lit(2, step), anchor='rm')
        text(d, (x1 + 40, yt + 120), 'rim in 1', 52, lit(2, step, BLUE))
        chip_on(d, (1700, 520), '1.5 + 1 = 2.5 > 2', lit(2, step, RED), px=60)
    width_mark(d, x0, x1, yb + 70, 'wall 2', DONE)
    if step >= 3:
        chip_on(d, (1500, 800), 'rim out + rim in\nless than the wall', BLUE, px=64)
        text(d, (1520, 1020), 'with a little flat left', 52, INK)
    save(im, f'card-rule-{step}.png')


# --- S1: the Short's why (1080 x 1080) -----------------------------------------------------------------------------------
def card_why_s(step):
    """S1: 1 the strip 2 wide; 2 a radius-3 quarter circle overhanging, red, "3 > 2"; 3 a second round from the inside
    edge, the two overlapping, "both share" / "the 2"."""
    CUR.clear()
    fr = (1080, 1080)
    im = Image.new('RGB', fr, WHITE)
    d = ImageDraw.Draw(im)
    k, x0, yt, yb = 110, 300, 220, 820
    if step == 1:
        x1 = section(d, x0, yt, yb, k)
    elif step == 2:
        x1 = section(d, x0, yt, yb, k, big=ROUT)
        chip_on(d, (640, 520), '3 > 2', RED, px=64, frame=fr)
    else:
        x1 = section(d, x0, yt, yb, k, out=FIXR, inn=RIN, out_col=ORANGE, in_col=BLUE)
        overlap_bar(d, x0 + FIXR * k, x1 - RIN * k, yt)
        chip_on(d, (640, 420), 'both share\nthe 2', RED, px=56, frame=fr)
    width_mark(d, x0, x1, yb + 70, 'top: 2 across', INK, px=48, frame=fr)
    save(im, f'card-why-s{step}.png')


# --- stills, end card, the Short's headline ----------------------------------------------------------------------------
RUN_LINES = None


def run_lines():
    a, bb = RUNS['A1']['check'], RUNS['B1']['check']

    def r(c, w):
        x = c[f'at_wall{w}']['round_radii']
        return f"{n0(x['out'][0])} + {n0(x['in'][0])}"
    return [f'run 1, wall 3: {r(a, 3)}', f'run 2, wall 3: {r(bb, 3)}', f'run 1, wall 1.6: {r(a, 1.6)}',
            f'run 2, wall 1.6: {r(bb, 1.6)}']


STILL_CROP = {'A1': (1720, 560, 2720, 1420), 'B1': (1720, 400, 2800, 1500)}   # after.png: the cup in its 3D view
STILL_K = {}


def still_after(run, chip):
    """F14: the run's file after the run (still), the panel beside it (never over it)."""
    im, d = canvas()
    full = Image.open(os.path.join(TAKES, 'runs', run, 'after.png')).convert('RGB')
    # fc15 cut 1: the cup cropped from the 3D view (screen px), big; the whole window as an inset beside it
    box = STILL_CROP[run]
    shot = full.crop(box)
    k = min(1300 / shot.width, 1150 / shot.height)
    STILL_K[run] = round(k, 2)
    s = shot.resize((round(shot.width * k), round(shot.height * k)), Image.LANCZOS)
    im.paste(s, (140, 220))
    d.rectangle((137, 217, 140 + s.width + 2, 220 + s.height + 2), outline=PARTLINE, width=3)
    text(d, (140, 130), 'its file after the run (still)', 56, INK)
    chip_on(d, (1500, 220), chip, BLUE, px=48)
    lines = run_lines()
    code_box(d, 1500, 400, lines, 'checked by code', 52, 0.8)
    ki = 600 / full.width
    th = full.resize((600, round(full.height * ki)), Image.LANCZOS)
    im.paste(th, (1500, 860))
    d.rectangle((1498, 858, 1502 + th.width, 862 + th.height), outline=PARTLINE, width=3)
    d.rectangle(tuple(round(v * ki) + o for v, o in zip(box, (1500, 860, 1500, 860))), outline=ORANGE, width=5)
    text(d, (1500, 870 + th.height), 'whole window', 48, GREY)
    for ln in lines:
        if len(ln) > 32:
            PROBLEMS.append(f'{ln!r}: over 32')
    save(im, f'still-after-{run}.png')


def card_end():
    im, d = canvas()
    text(d, (180, 220), 'FreeCAD + Claude course', 72, INK)
    text(d, (180, 330), 'lesson 15: a rim round that fits the wall', 60, BLUE)
    shot = Image.open(os.path.join(TAKES, 'F', 'fix-iso.png')).convert('RGB').crop((1000, 250, 2400, 1650))
    im.paste(shot.resize((600, 600)), (180, 450))
    d.rectangle((180, 450, 780, 1050), outline=PARTLINE, width=3)
    text(d, (180, 1080), 'the rounded cup (filmed)', 44, GREY, path=b.R)
    text(d, (180, 1180), 'Lesson 14 · Lesson 1 · the course', 52, INK)
    save(im, 'card-end.png')


HEAD = ('FILLET 3 ON A 2 MM WALL:', 'FAILED')


def card_short_head():
    """The Short's frame-1 headline (1080 x 1920, RGBA): the problem in words from 0.0 s, through the 1 s hold."""
    CUR.clear()
    fr = (1080, 1920)
    im = Image.new('RGBA', fr, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, s in enumerate(HEAD):
        px = 56 if i == 0 else 72
        f = b.font(b.B, px)
        w = d.textlength(s, font=f)
        y = 60 + i * 86
        d.rectangle(((1080 - w) / 2 - 18, y - 8, (1080 + w) / 2 + 18, y + px + 12), fill=ORANGE + (242,))
        d.text(((1080 - w) / 2, y), s, font=f, fill=WHITE + (255,))
        if (1080 - w) / 2 - 18 < 0:
            PROBLEMS.append(f'{s!r}: headline wider than the Short')
        CUR.append((s, px))
    save(im, 'card-short-head.png')


# --- source overlays ----------------------------------------------------------------------------------------------------
def ring(name, box, col=ORANGE, extra=None):
    im, d = source()
    d.rounded_rectangle(box, radius=30, outline=col + (255,), width=8)
    if extra:
        extra(d)
    save(im, name)


def src_chip(d, xy, s, col, px=64):
    """A chip on a source overlay (opaque light box, coloured words)."""
    f = b.font(b.B, px)
    lines = s.split('\n')
    w = max(d.textlength(x, font=f) for x in lines)
    x, y = xy
    h = (px + 16) * len(lines) + 20
    d.rounded_rectangle((x, y, x + w + 44, y + h), radius=16, fill=WHITE + (245,), outline=col + (255,), width=5)
    for i, ln in enumerate(lines):
        d.text((x + 22, y + 12 + i * (px + 16)), ln, font=f, fill=col + (255,))
        CUR.append((ln, round(px * 0.8)))
        if len(ln) > 32 or '%' in ln:
            PROBLEMS.append(f'{ln!r}: chip line')
    if x + w + 44 > SW or y + h > SH:
        PROBLEMS.append(f'{s!r}: chip off the frame')
    return y + h


def chips_t():
    """F0 / S0 frame 0 (T 44.5 on): the rim ringed, "round 3, wall 2" and "3 > 2" left of the cup."""
    im, d = source()
    d.rounded_rectangle(RIM_T, radius=30, outline=ORANGE + (255,), width=8)
    y = src_chip(d, CHIP_XY, f'round {n0(ROUT)}, wall {n0(WALL)}', INK)
    src_chip(d, (CHIP_XY[0], y + 24), f'{n0(ROUT)} > {n0(WALL)}', RED, px=80)
    save(im, 'ov-chips-T.png')


def sums():
    for name, s, col in (('ov-sum-I.png', '1.5 + 1 = 2.5 > 2', RED), ('ov-fits-P.png', '1.5 + 1 = 2.5, fits 3', GREEN),
                         ('ov-w3-P.png', 'wall 3:\n1.5 + 1 = 2.5, fits\nleftover flat 0.50', GREEN),
                         ('ov-w2-P.png', 'wall 2:\n2.5 > 2, failed', RED)):
        im, d = source()
        src_chip(d, CHIP_XY, s, col)
        save(im, name)


def ov_lines(name, lines, step, box, px=56, k=0.8, one=False):
    """Lower-left panel: the lines up to `step` (the newest blue, earlier grey; `one`: all in ink)."""
    im, d = source()
    d.rounded_rectangle(box, radius=18, fill=WHITE + (245,), outline=PARTLINE + (255,), width=4)
    f = b.font(b.B, px)
    y = box[1] + 36
    for i, ln in enumerate(lines[:step]):
        col = (INK if one else BLUE if i == step - 1 else DONE) + (255,)
        for part in ln.split('\n'):
            CUR.append((part, round(px * k)))
            d.text((box[0] + 32, y), part, font=f, fill=col)
            bb = d.textbbox((box[0] + 32, y), part, font=f)
            if bb[2] > box[2] or bb[3] > box[3]:
                PROBLEMS.append(f'{part!r}: outside its panel {bb}')
            y += round(px * 1.35)
        y += round(px * 0.4)
    save(im, name)


def code_panel(name, lines, xy, px=PX, k=0.8, title='checked by code'):
    im, d = source()
    code_box(d, xy[0], xy[1], lines, title, px, k)
    for t in lines:
        if len(t) > 32:
            PROBLEMS.append(f'{t!r}: code panel line over 32')
    save(im, name)
    PANEL_NAMES.append(name)


def quote(name, run, lines, xy=CC_XY, px=52):
    """Claude's own words, re-set word for word from reply.txt (lines that scrolled off before the last frame)."""
    reply = ' '.join(open(os.path.join(TAKES, 'runs', run, 'reply.txt'), encoding='utf-8').read().split())
    assert ' '.join(lines) in reply, lines
    # fc15 cut 1: its own look (pale blue, a quote bar, quote marks), never a look-alike of our "checked by code" panel
    im, d = source()
    lines = list(lines)
    lines[0] = lines[0][2:] if lines[0].startswith('- ') else lines[0]   # the Markdown bullet is not a word
    lines[0] = '“' + lines[0]
    lines[-1] = lines[-1] + '”'
    fh, fl = b.font(b.B, px), b.font(f10.MONO, px)
    title = "Claude's reply, quoted:"
    lh, pad = round(px * 1.3), round(px * 0.55)
    rows = [(title, fh)] + [(t, fl) for t in lines]
    x, y = xy
    w = max(d.textlength(t, font=f) for t, f in rows) + 2 * pad + 24
    h = lh * len(rows) + pad
    d.rounded_rectangle((x, y, x + w, y + h), radius=round(px * 0.3), fill=(219, 234, 254, 250),
                        outline=BLUE + (255,), width=4)
    d.rectangle((x + 10, y + 12, x + 22, y + h - 12), fill=BLUE + (255,))
    for i, (t, f) in enumerate(rows):
        d.text((x + pad + 24, y + pad * 0.6 + i * lh), t, font=f, fill=(BLUE if i == 0 else INK) + (255,))
        CUR.append((t, round(px * 0.8)))
    if x + w > SW or y + h > SH:
        PROBLEMS.append(f'{name}: quote off the frame')
    save(im, name)
    PANEL_NAMES.append(name)


ISO_R = os.path.join(TAKES, 'R', 'iso-32.png')   # take R at 32.0 s, the fitted iso view (ffmpeg, video-qa:2)
ISO_CROP = (1180, 260, 2380, 1580)                # the whole cup on that frame
RIM_SPOT = (2068, 814)                            # (31, 0, 50): the right wall's top edge, where every zoom looks
LOC_XY, LOC_H = (510, 310), 480


def _loc_geom():
    s = LOC_H / (ISO_CROP[3] - ISO_CROP[1])
    w = round((ISO_CROP[2] - ISO_CROP[0]) * s)
    mx = LOC_XY[0] + 16 + round((RIM_SPOT[0] - ISO_CROP[0]) * s)
    my = LOC_XY[1] + 16 + round((RIM_SPOT[1] - ISO_CROP[1]) * s)
    return s, w, (mx, my)


LOC_MARK = (_loc_geom()[2][0] - 36, _loc_geom()[2][1])   # a pixel on the mark's left side (tests)


def locator(name, caption):
    """fc15 cut 1: an inset of the whole cup (R's iso view) with the zoomed spot boxed, for the rim close-ups."""
    im, d = source()
    s, w, (mx, my) = _loc_geom()
    x, y = LOC_XY
    pic = Image.open(ISO_R).convert('RGB').crop(ISO_CROP).resize((w, LOC_H), Image.LANCZOS)
    d.rounded_rectangle((x, y, x + w + 32, y + LOC_H + 84), radius=16, fill=WHITE + (250,), outline=ORANGE + (255,),
                        width=5)
    im.paste(pic, (x + 16, y + 16))
    d = ImageDraw.Draw(im)
    d.rectangle((mx - 36, my - 24, mx + 36, my + 24), outline=ORANGE + (255,), width=7)
    f = b.font(b.B, 40)
    d.text((x + 18, y + LOC_H + 26), caption, font=f, fill=INK + (255,))
    CUR.append((caption, round(40 * 0.8)))
    if d.textlength(caption, font=f) > w + 10:
        PROBLEMS.append(f'{caption!r}: wider than the inset')
    save(im, name)


RECAP = ['A round uses its radius\non the top and the side', 'Rim out + rim in\nless than the wall',
         'Change the wall?\nCheck the rounds again']
TURN = [f'Your turn: wall {n0(2.5)}', 'outside 1.2, inside 1.5', 'Builds, or fails?']
SUB = [['Lesson 16: the hanging hole, typed 2 deep,', 'closes to a 1 mm skin at wall 3'],
       ['Every fix tested in both programs,', 'by hand and with Claude · Subscribe']]


def panels():
    t = NUM['takes']
    code_panel('ov-in-T5.png', ['same volume, same faces', 'nothing rounded'], (1880, 1320))         # F5 (T 76.8+)
    code_panel('ov-in-F7.png', [f'round {f2(FIXR)}', f"leftover flat {f2(FIX['flat'])}",
                                f"inside {n0(FIX['inside_w'])} × {n0(FIX['inside_l'])}"], (520, 1150))  # F7 (F 127.6+)
    code_panel('ov-in-P10.png', [f"on screen: wall-3 shape, {n0(W3['outside_w'])} wide",
                                 f"wall {n0(W26['wall'])}: builds, flat {f2(W26['flat'])}",
                                 f"wall {n0(W24['wall'])}: fails"], (1540, 1280))                     # F10 (P 193.5+)
    eq = G0['q3_scan_refusals_below_limit']['equal'][0]
    code_panel('ov-in-P14.png', ['wall 2, each round:', f"{n0(G0['q3_limits']['equal_pair']['largest_builds'])} built,"
                                 f' {n0(eq)} failed,', '0.9 built (run 2)'], (1540, 1280))           # F14 (P 123.1+)
    for run in ('A1', 'B1'):
        w2 = RUNS[run]['check']['at_wall2']
        rr = w2['round_radii']
        code_panel(f'ov-cc-{run}.png', ['its file, wall 2:', f"rounds {n0(rr['out'][0])} + {n0(rr['in'][0])}",
                                        f"flat {n0(w2['flat'])}"], CC_XY)
        code_panel(f'ov-log-{run}.png', [f"{RUNS[run]['n_tool_calls']} tool calls:", 'list_documents, get_objects,',
                                         'then execute_code'], CC_XY, title='from the run log')
    quote('ov-quote-B1a.png', 'B1', ['- New parameter: I added rim_round = 0.45 to', 'the Params sheet (cell B9).'],
          (1175, 300))
    quote('ov-quote-B1b.png', 'B1', ['It builds for walls from 0.75 mm to 10 mm.'], (1175, 300))
    assert t['T'] and t['F'] and t['P']


def main():
    os.makedirs(OUT, exist_ok=True)
    b.OUT = OUT
    PROBLEMS.clear()
    LOG.clear()
    PANEL_NAMES.clear()
    card_round(4)
    for s in (1, 2, 3):
        card_round(s)
        card_coin(s)
        card_rule(s)
        card_why_s(s)
    for s in range(1, 5):
        card_why(s)
    still_after('A1', 'not asked to check · $0.22')
    still_after('B1', 'asked to check · $0.21')
    card_end()
    card_short_head()
    chips_t()
    ring('ov-box-T.png', BOX_LINE, RED)
    ring('ov-box-I.png', BOX_LINE, RED)
    ring('ov-rim-R.png', RIM_R)
    ring('ov-corner-R.png', CORNER_R)
    ring('ov-flat-F.png', FLAT_F, GREEN)
    ring('ov-err-P.png', ROW_F001, RED)
    sums()
    locator('ov-loc-iso.png', 'the rim, close up')
    locator('ov-loc-top.png', 'rim, from above')
    for s in (1, 2, 3):
        ov_lines(f'rc-{s}.png', RECAP, s, (20, 1120, 1300, 1720))
    ov_lines('yt-1.png', TURN, 3, (20, 1300, 1300, 1720), px=56, one=True)
    for i, lines in enumerate(SUB, 1):
        ov_lines(f'sub-{i}.png', lines, 2, (20, 1470, 1560, 1730), px=54, one=True)
    panels()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
