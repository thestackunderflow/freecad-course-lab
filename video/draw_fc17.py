"""FreeCAD course lesson 17 (the second key peg by Mirror: Base XZ-plane sends the copy out of the back, Base YZ-plane
is the fold between the two pegs) cards, chips, panels, lower thirds and the F15 stills, SCRIPT-fc17.md rev 2 sections
0.1, 1 and 3 and SCRIPT-fc17-short.md. The draw_fc16.py pattern (draw_fx20 helpers as b, draw_fc10 as f10); the paper,
names, top-view and Short drawings are draw_sc17.py's (solidcraft-course-lab) with FreeCAD words ("solid", "no
message, no mark") and the sc17 blind-review fixes: the origin at the cup's middle (never a corner) on every diagram,
card-why-s1 ties the numbers ("centre 27.5 front → 27.5 back"), card-why-s3 keeps "15 right → 15 left" and adds
"missing letter flips". card-axis-1 (F9) is FreeCAD only: the peg sketch's vertical axis turned into the YZ plane.
Light, 2560 x 1440 cards, card lines 44 columns, chips / panels / Short lines 32, no percent sign, no angle brackets,
"−" in drawn sums, never "A1" / "B1" / "body" / "shell" / "proud" on screen. Every number is NUMBERS.json's (out/fc17),
the script's arithmetic or a lesson number.
  full frame (RGB 2560 x 1440): card-fold-1..4 (F2), card-names-1..3 (F6), card-top-1..6 (F7; build 6 = the rule),
      card-axis-1 (F9; lower left kept clear for ov-in-F9), card-centred-1 (F10), card-end (F17)
  Short: card-why-s1..3 (RGB 1080 x 1080, S2); card-short-head (= short-head), short-q, short-series (RGBA 1080 x 1920)
  F15 stills (RGB 2880 x 1800): st-A1 (runs/A1/after.png, footer masked, label), st-A1z (the cup cropped 1.5x, pegs
      ringed, the panel beside), st-B1f / st-B1b (out/fc17/stills front-B1 / rear-B1: lab/fc17_still.sh, the saved
      file in the take kit's Front / Rear views, 80 mm high; pegs ringed / back clear, the panel lower left)
  source overlays (RGBA 2880 x 1800): ov-in-* / ov-sk-F4 (lower left), ov-cc-A1 / -B1 (FreeCAD side of the Claude
      frames), ov-chip-run-A1 / -B1 / -cc-version, rc-1..2 / yt-1 (F16), sub-1..2 (F12)
Geometry (source px, 2880 x 1800): F front-fixed.png (90 mm high): cup x 1166-2193, y 698-1531, pegs y 778-937;
runs/A1/after.png: Claude Code x 0-1157, cup x 1839-2589, y 671-1282, pegs x 1979-2098 / 2330-2449, y 730-848;
stills/*-B1.png (80 mm high at 0 -+28 32, 18 px/mm): cup x 1104-2256, y 662-1598, the hanging hole (1679, 1022).
Run in the draw image:  MSYS_NO_PATHCONV=1 docker run --rm -v "<edu-visualization>:/ev" -w /ev/freecad-course-lab \
  cad3way-draw:1 python3 video/draw_fc17.py
Test: tests/test_draw_fc17.py"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw_fx20 as b  # noqa: E402
import draw_fc10 as f10  # noqa: E402

LAB = b.LAB
OUT = os.path.join(LAB, 'video', 'frames-fc17')
TAKES = os.path.join(LAB, 'out', 'fc17')
W, H, SW, SH = b.W, b.H, b.SW, b.SH
INK, GREY, WHITE, DONE = b.INK, b.GREY, b.WHITE, b.DONE
BLUE, ORANGE, RED, GREEN = b.BLUE, b.ORANGE, b.RED, b.GREEN
DONEFILL = b.DONEFILL
PARTLINE = f10.PARTLINE
PAPER, PAINT, CUP, INSIDE = (254, 252, 243), (220, 38, 38), (203, 213, 225), (241, 245, 249)
COPYFILL, BACKFILL = (187, 247, 208), (254, 202, 202)
canvas, source, header = b.canvas, b.source, b.header
PROBLEMS, LOG, CUR = b.PROBLEMS, b.LOG, b.CUR
code_box = f10.code_box
NUM = json.load(open(os.path.join(TAKES, 'NUMBERS.json'), encoding='utf-8'))
RUNS = NUM['runs']
PX = 63                                 # code panels on the 2880 frame
TOP_BAND = 160                          # title bar + toolbars / the REAL RECORDING chip
CC_RIGHT = 1160                         # Claude Code's pane: x 0-1157 on runs/*/screen.mp4
PANEL_LL = (40, 1690)                   # lower left, anchor bottom (tree / property area, left of the cup)
CC_PANEL = (1170, 1590)                 # Claude frames: FreeCAD side, under its tree, bottom
RUN_CHIP = (1170, 1606)                 # run / version chip under the panels, above y 1700
CUP_MIDDLE = (1450, 700, 1910, 1300)    # the cup's middle on the GUI takes' Front / Rear views (front-fixed.png)
CUP_STILL = (1104, 662, 2256, 1598)     # the cup on stills/front-B1, rear-B1
PEGS_STILL = [(1320, 752, 1500, 932), (1860, 752, 2040, 932)]   # x ±10..20, z 35..45 at 18 px/mm
HOLE_STILL = (1679, 1022)
A1_CROP = (1780, 620, 2650, 1340)       # runs/A1/after.png: the cup
A1_PEGS = [(1979, 730, 2098, 848), (2330, 730, 2449, 848)]
A1_K = 1.5
CHIP_TL = (540, 290)
AXIS = ['x: − left, + right · z up', 'y: − front, + back']
AXIS_S = ['x: − left, + right', 'y: − front, + back · z up']
HEAD = ('MY MIRRORED PEG', 'CAME OUT THE BACK')
ORIGIN_3D = (0, 0, 0)                   # lesson 14 centred the cup on the origin: x and y from its middle
DRAWN = {}


def g(v):
    return f'{v:g}'


def text(d, xy, s, size=56, fill=INK, **kw):
    return f10.text(d, xy, s, size, fill, **kw)


def save(im, name):
    b.OUT = OUT
    b.save(im, name)


def mirror(p, plane):
    """The missing letter flips: XZ flips y, YZ flips x (points (x, y) seen from above)."""
    x, y = p
    return (x, -y) if plane == 'XZ' else (-x, y)


def chip(d, xy, s, px=52, fill=INK, edge=ORANGE, frame=(W, H)):
    """A chip on a card: rounded light box, coloured words (logged); returns its box."""
    f = b.font(b.B, px)
    lines = s.split('\n')
    w = max(d.textlength(x, font=f) for x in lines)
    x, y = xy
    box = (x, y, x + w + 40, y + (px + 14) * len(lines) + 16)
    d.rounded_rectangle(box, radius=14, fill=WHITE, outline=edge, width=4)
    for i, ln in enumerate(lines):
        text(d, (x + 20, y + 10 + i * (px + 14)), ln, px, fill, frame=frame)
    return box


def arrowhead(d, tip, ux, uy, col, size=30):
    px_, py_ = -uy, ux
    d.polygon([tip, (tip[0] - ux * size + px_ * size * 0.5, tip[1] - uy * size + py_ * size * 0.5),
               (tip[0] - ux * size - px_ * size * 0.5, tip[1] - uy * size - py_ * size * 0.5)], fill=col)


def arrow(d, a, z, col, w=10, size=34):
    d.line((a[0], a[1], z[0], z[1]), fill=col, width=w)
    ln = math.hypot(z[0] - a[0], z[1] - a[1]) or 1
    arrowhead(d, z, (z[0] - a[0]) / ln, (z[1] - a[1]) / ln, col, size)


def axis_key(d, xy, lines=AXIS, px=46, frame=(W, H)):
    x, y = xy
    f = b.font(b.B, px)
    w = max(d.textlength(t, font=f) for t in lines) + 48
    box = (x, y, x + w, y + px * 1.45 * len(lines) + 28)
    d.rounded_rectangle(box, radius=14, fill=WHITE, outline=PARTLINE, width=3)
    for i, t in enumerate(lines):
        d.text((x + 24, y + 16 + i * px * 1.45), t, font=f, fill=INK)
        CUR.append((t, px))
    if box[2] > frame[0] * 0.97:
        PROBLEMS.append(f'{lines!r}: axis key off the frame')
    return box


# --- F2: paint on paper (four builds; draw_sc17.card_fold) --------------------------------------------------------------
def sheet(d, box, crease, blobs, on=True, r=46):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=PAPER if on else (248, 248, 245), outline=INK if on else DONE, width=5)
    if crease == 'down':
        f10.dashed(d, ((x0 + x1) / 2, y0 + 10), ((x0 + x1) / 2, y1 - 10), BLUE if on else DONE, width=7, dash=26)
    elif crease == 'across':
        f10.dashed(d, (x0 + 10, (y0 + y1) / 2), (x1 - 10, (y0 + y1) / 2), BLUE if on else DONE, width=7, dash=26)
    for (u, v), twin in blobs:
        cx, cy = x0 + u * (x1 - x0), y0 + v * (y1 - y0)
        col = PAINT if on else DONE
        if twin:
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=10)
        else:
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)


FOLD_CHIPS = {}


def card_fold(step):
    im, d = canvas()
    header(d, 'Paint on paper, then fold')
    one, two = (260, 300, 1180, 1120), (1380, 300, 2300, 1120)
    if step == 1:
        sheet(d, one, 'down', [((0.8, 0.8), False)])
        chip(d, (300, 1200), 'fold down the middle', 60)
    elif step == 2:
        sheet(d, one, 'down', [((0.8, 0.8), False), ((0.2, 0.8), True)])
        chip(d, (300, 1200), 'copy beside it', 60)
    else:
        sheet(d, one, 'down', [((0.8, 0.8), False), ((0.2, 0.8), True)], on=step == 4)
        sheet(d, two, 'across', [((0.8, 0.8), False), ((0.8, 0.2), True)])
        if step == 3:
            FOLD_CHIPS[3] = chip(d, (1420, 1200), 'wrong crease: wrong place', 60)
        else:
            for bx, horiz in ((one, False), (two, True)):
                x0, y0, x1, y1 = bx
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                if horiz:
                    d.rounded_rectangle((x0 - 14, cy - 34, x1 + 14, cy + 34), radius=30, outline=ORANGE, width=8)
                else:
                    d.rounded_rectangle((cx - 34, y0 - 14, cx + 34, y1 + 14), radius=30, outline=ORANGE, width=8)
            # cut 2 (f021): under sheet one, clear of step 3's chip under sheet two (the 0.35 s dissolve showed both)
            FOLD_CHIPS[4] = chip(d, (260, 1200), 'the crease sits between them', 64)
    save(im, f'card-fold-{step}.png')


# --- F6 / F9: the cup in 3D (oblique, from the front, a little above and right) -------------------------------------
K3 = 10
O3 = [1000, 1080]
DEPTH = [0.55, 0.42]                    # how far y (front to back) moves right / up on the page


def P(x, y, z):
    return (O3[0] + x * K3 + y * K3 * DEPTH[0], O3[1] - z * K3 - y * K3 * DEPTH[1])


def poly(d, pts, fill=None, outline=INK, width=4):
    q = [P(*p) for p in pts]
    d.polygon(q, fill=fill, outline=outline)
    if outline and width > 1:
        d.line(q + [q[0]], fill=outline, width=width)


def peg3d(d, x0, x1, ink, end=(148, 163, 184), side=(120, 135, 160), top=(170, 182, 200)):
    """A peg x0..x1, out of the front wall (y −35..−22), z 35..45; its end, the side facing right and its top."""
    poly(d, [(x0, -35, 35), (x1, -35, 35), (x1, -35, 45), (x0, -35, 45)], end, ink)
    poly(d, [(x1, -35, 35), (x1, -22, 35), (x1, -22, 45), (x1, -35, 45)], side, ink)
    poly(d, [(x0, -35, 45), (x1, -35, 45), (x1, -22, 45), (x0, -22, 45)], top, ink)


def cup3d(d, on=True, copy=False, im=None, plane=None):
    """The cup (outside 64 x 44, 50 high, centred on the origin) and its peg(s). With `plane` (pts, colour, alpha) the
    plane is drawn inside the cup: behind a see-through front wall, so it reads as crossing the middle."""
    ink = INK if on else DONE
    x0, x1, y0, y1, z1 = -32, 32, -22, 22, 50
    poly(d, [(x0, y1, 0), (x1, y1, 0), (x1, y1, z1), (x0, y1, z1)], CUP, ink)
    poly(d, [(x1, y0, 0), (x1, y1, 0), (x1, y1, z1), (x1, y0, z1)], (186, 198, 214), ink)
    poly(d, [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], INSIDE, ink)
    poly(d, [(x0 + 2, y0 + 2, z1), (x1 - 2, y0 + 2, z1), (x1 - 2, y1 - 2, z1), (x0 + 2, y1 - 2, z1)], INSIDE, ink, 2)
    front = [(x0, y0, 0), (x1, y0, 0), (x1, y0, z1), (x0, y0, z1)]
    if im is None:
        poly(d, front, CUP, ink)
    else:
        q = [P(x, y, 0) for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
        for a, e in zip(q, q[1:] + q[:1]):
            f10.dashed(d, a, e, GREY, width=3, dash=16)                 # the floor, seen through the front wall
        if plane is not None:
            d = plane_quad(im, *plane)
        ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(ov).polygon([P(*p) for p in front], fill=CUP + (150,))
        im.paste(Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB'))
        d = ImageDraw.Draw(im)
        q = [P(*p) for p in front]
        d.line(q + [q[0]], fill=ink, width=4)
    if copy:
        peg3d(d, -20, -10, ink, end=COPYFILL, side=(134, 214, 160), top=(200, 245, 215))
    peg3d(d, 10, 20, ink)
    return d


def plane_quad(im, pts, col, alpha):
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).polygon([P(*p) for p in pts], fill=col + (alpha,))
    im.paste(Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB'))
    d = ImageDraw.Draw(im)
    q = [P(*p) for p in pts]
    d.line(q + [q[0]], fill=col, width=6)
    return d


def origin_dot(d, label=True):
    o = P(*ORIGIN_3D)
    d.ellipse((o[0] - 14, o[1] - 14, o[0] + 14, o[1] + 14), fill=INK, outline=WHITE, width=3)
    if label:
        text(d, (o[0] - 30, o[1] + 40), 'origin: the middle', 44, INK, anchor='ra')
    return o


def card_names(step):
    """1 the cup, the axes from the origin at the cup's middle (lesson 14 centred it); 2 XZ standing across the
    middle, its x and z lit; 3 y straight through it."""
    O3[:] = [1000, 1060]
    DEPTH[:] = [0.95, 0.75]
    im, d = canvas()
    header(d, 'Planes are named by two directions')
    if step >= 2:
        d = cup3d(d, im=im, plane=([(-44, 0, -4), (44, 0, -4), (44, 0, 62), (-44, 0, 62)], BLUE,
                                   90 if step == 2 else 55))
        f10.dashed(d, P(-32, 0, 50), P(32, 0, 50), BLUE, width=8)
        q = P(-44, 0, 62)
        text(d, (q[0] - 20, q[1] + 10), 'XZ', 80, BLUE, anchor='rm')
        chip(d, (200, 1200), 'XZ: across the middle, like a wall', 56)
    else:
        d = cup3d(d, im=im)
    o = origin_dot(d)
    for name, z, on in (('x', P(36, 0, 0), step == 2), ('z', P(0, 0, 70), step == 2), ('y', P(0, 40, 0), step == 3)):
        col = ORANGE if on else GREY
        arrow(d, o, z, col, w=10 if on else 6)
        text(d, (z[0] + 18, z[1] - 40), name, 64, col)
    if step == 3:
        a, z = P(0, -36, 25), P(0, 38, 25)
        arrow(d, a, z, ORANGE, w=14, size=44)
        text(d, (z[0] + 30, z[1] - 20), 'y: straight through', 60, ORANGE)
    axis_key(d, (1700, 1080))
    DEPTH[:] = [0.55, 0.42]
    save(im, f'card-names-{step}.png')


# --- F7: from above, on the paper ---------------------------------------------------------------------------------------
KT, OT = 12, (1880, 770)
PAPER_BOX = (1330, 250, 2470, 1290)


def T(x, y):
    return (OT[0] + x * KT, OT[1] - y * KT)


def rect_xy(d, x0, x1, y0, y1, fill, outline=INK, width=5):
    a, z = T(x0, y1), T(x1, y0)
    d.rectangle((a[0], a[1], z[0], z[1]), fill=fill, outline=outline, width=width)


def top_cup(d, on=True):
    ink = INK if on else DONE
    rect_xy(d, -32, 32, -22, 22, CUP, ink)
    rect_xy(d, -30, 30, -20, 20, INSIDE, ink, 3)


TOP_CUP_BOX = (T(-32, 0)[0], T(0, 35)[1], T(32, 0)[0], T(0, -35)[1])   # the cup + pegs front and back


def left_chip(d, xy, s, px, **kw):
    box = chip(d, xy, s, px, **kw)
    if box[2] > TOP_CUP_BOX[0] - 20:
        PROBLEMS.append(f'{s!r}: chip reaches the cup {box}')
    return box


def card_top(step):
    """Each build one sentence: 1 the paper; 2 the cup and the peg (x 15, y −27.5), XZ across the middle; 3 the copy
    straight through XZ, +27.5; 4 YZ down the middle; 5 the copy straight through YZ, x −15; 6 the rule."""
    im, d = canvas()
    header(d, 'From above, on the paper')
    d.rectangle(PAPER_BOX, fill=PAPER, outline=DONE, width=4)
    cxp = (PAPER_BOX[0] + PAPER_BOX[2]) / 2
    text(d, (cxp, 1325), 'front (bottom of the page)', 44, GREY, anchor='mm')
    text(d, (cxp, 215), 'back (top of the page)', 44, GREY, anchor='mm')
    left_chip(d, (150, 1240), 'the paper, seen from above', 52, fill=INK if step == 1 else DONE,
              edge=ORANGE if step == 1 else DONE)
    peg = (15, -27.5)
    if step >= 2:
        top_cup(d)
        rect_xy(d, 10, 20, -35, -20, PAINT, INK, 4)                       # the peg = the blob, front right
        p = T(*peg)
        # cut 2 (REVIEW-watch-fc17-c1): Claude's reply says y −35 (the peg's front end); name both numbers
        lx, ly = T(10, 0)[0] - 24, T(0, -22)[1] + 18                     # left of the peg, under the cup's front
        text(d, (lx, ly), 'peg centre: x 15, y −27.5', 44, PAINT, anchor='ra')
        text(d, (lx, ly + 56), 'its end: y −35', 44, PAINT, anchor='ra')
        o = T(0, 0)
        d.ellipse((o[0] - 10, o[1] - 10, o[0] + 10, o[1] + 10), fill=INK)
        a, z = T(-44, 0), T(44, 0)
        d.line((a, z), fill=BLUE if step <= 3 else DONE, width=8)
        text(d, (a[0] - 20, a[1]), 'XZ', 64, BLUE if step <= 3 else DONE, anchor='rm')
    if step >= 3:
        on = step == 3
        c = mirror(peg, 'XZ')
        f10.dashed(d, T(*peg), T(c[0], c[1] - 2.5), ORANGE if on else DONE, width=7)
        arrowhead(d, T(c[0], c[1] - 1), 0, -1, ORANGE if on else DONE, 30)
        rect_xy(d, c[0] - 5, c[0] + 5, c[1] - 7.5, c[1] + 7.5, BACKFILL if on else DONEFILL, PAINT if on else DONE, 5)
        left_chip(d, (150, 260), '27.5 in front → 27.5 behind', 52, fill=INK if on else DONE,
                  edge=ORANGE if on else DONE)
        left_chip(d, (150, 370), 'the crease across → top right', 52, fill=INK if on else DONE,
                  edge=ORANGE if on else DONE)
    if step >= 4:
        a, z = T(0, -48), T(0, 44)
        d.line((a, z), fill=GREEN, width=8)
        text(d, (z[0] + 20, z[1] - 10), 'YZ', 64, GREEN)
    if step >= 5:
        on = step == 5
        c = mirror(peg, 'YZ')
        f10.dashed(d, T(*peg), T(c[0] + 2, c[1]), ORANGE if on else DONE, width=7)
        arrowhead(d, T(c[0] + 5, c[1]), -1, 0, ORANGE if on else DONE, 30)
        rect_xy(d, c[0] - 5, c[0] + 5, c[1] - 7.5, c[1] + 7.5, COPYFILL, GREEN, 5)
        left_chip(d, (150, 480), '15 right → 15 left', 52, fill=INK if on else DONE, edge=ORANGE if on else DONE)
    if step >= 6:
        left_chip(d, (150, 880), 'missing letter flips; the other two stay', 52)
        left_chip(d, (150, 990), 'XZ → y flips', 52, fill=BLUE, edge=BLUE)
        left_chip(d, (590, 990), 'YZ → x flips', 52, fill=GREEN, edge=GREEN)
    axis_key(d, (150, 640), px=44)
    save(im, f'card-top-{step}.png')


# --- F9: FreeCAD's first guess, the sketch's vertical axis = the YZ plane ---------------------------------------------
def card_axis(step=3):
    """3 builds, one per sentence: 1 the sketch's vertical axis up the middle; 2 the fold stood up along it (YZ, front
    to back); 3 the paper folded down the middle + "same plane here"."""
    O3[:] = [1250, 1060]
    im, d = canvas()
    header(d, "FreeCAD's first guess: the sketch's axis")
    DEPTH[:] = [0.75, 0.55]
    plane = ([(0, -36, -2), (0, 36, -2), (0, 36, 60), (0, -36, 60)], GREEN, 80) if step >= 2 else None
    d = cup3d(d, copy=True, im=im, plane=plane)
    f10.dashed(d, P(0, -22, -2), P(0, -22, 58), ORANGE, width=9, dash=24)          # the axis, up the cup's middle
    a, e = P(0, -22, 20), P(-32, -22, 20)
    text(d, (e[0] - 40, e[1] - 30), "the sketch's", 48, ORANGE, anchor='rm')
    text(d, (e[0] - 40, e[1] + 30), 'vertical axis', 48, ORANGE, anchor='rm')
    arrow(d, (e[0] - 30, e[1]), (a[0] - 14, a[1]), ORANGE, w=5, size=24)
    DEPTH[:] = [0.55, 0.42]
    if step >= 2:
        q = P(0, 36, 60)
        text(d, (q[0] + 26, q[1] - 10), 'YZ: front to back', 56, GREEN)
    origin_dot(d, label=False)
    if step >= 3:
        sheet(d, (1880, 560, 2380, 1060), 'down', [((0.8, 0.8), False), ((0.2, 0.8), True)], r=34)
        text(d, (2130, 1100), 'folded down the middle', 44, GREY, anchor='ma')
        chip(d, (1560, 1220), 'same plane here', 64, edge=GREEN)
    save(im, f'card-axis-{step}.png')


# --- F10: centred -------------------------------------------------------------------------------------------------------
def card_centred():
    im, d = canvas()
    header(d, 'Why YZ lands in the middle')
    d.rectangle(PAPER_BOX, fill=PAPER, outline=DONE, width=4)
    top_cup(d)
    rect_xy(d, 10, 20, -35, -20, PAINT, INK, 4)
    rect_xy(d, -20, -10, -35, -20, COPYFILL, GREEN, 5)
    a, z = T(-42, 0), T(42, 0)
    d.line((a, z), fill=(147, 180, 246), width=5)
    text(d, (a[0] - 20, a[1]), 'XZ', 52, (147, 180, 246), anchor='rm')
    a, z = T(0, -40), T(0, 34)
    d.line((a, z), fill=GREEN, width=8)
    text(d, (z[0] + 20, z[1] - 10), 'YZ', 64, GREEN)
    o = T(0, 0)
    d.ellipse((o[0] - 14, o[1] - 14, o[0] + 14, o[1] + 14), fill=INK)
    d.ellipse((o[0] - 50, o[1] - 50, o[0] + 50, o[1] + 50), outline=ORANGE, width=8)
    box = left_chip(d, (150, 420), 'centred in lesson 14', 60)
    arrow(d, (box[2] + 10, (box[1] + box[3]) / 2), (o[0] - 60, o[1] - 30), ORANGE, w=6)
    text(d, (150, 640), "the cup's middle = the origin,", 52, INK)
    text(d, (150, 720), 'where the three planes cross', 52, INK)
    text(d, (150, 830), 'YZ goes through it', 52, GREEN)
    axis_key(d, (150, 1000), px=44)
    save(im, 'card-centred-1.png')


# --- F17 end card -------------------------------------------------------------------------------------------------------
def tile(d, box, lines):
    d.rounded_rectangle(box, radius=24, fill=(248, 250, 252), outline=PARTLINE, width=4)
    y = box[1] + 34
    for i, (s, px) in enumerate(lines):
        text(d, (box[0] + 40, y), s, px, INK if i == 0 else GREY)
        y += px + 24


def card_end():
    im, d = canvas()
    text(d, (180, 160), 'FreeCAD + Claude course', 72, INK)
    text(d, (180, 270), 'lesson 17: mirror across the fold', 60, BLUE)
    shot = Image.open(os.path.join(TAKES, 'F', 'front-fixed.png')).convert('RGB').crop((1180, 615, 2180, 1615))
    im.paste(shot.resize((600, 600), Image.LANCZOS), (180, 400))
    d.rectangle((180, 400, 780, 1000), outline=PARTLINE, width=3)
    text(d, (180, 1020), 'two pegs on the front (filmed)', 44, GREY, path=b.R)
    tile(d, (900, 380, 2380, 640), [('Lesson 16', 56), ('make the Pocket Length the wall', 44)])
    tile(d, (900, 680, 2380, 940), [('SolidCraft vs FreeCAD Assembly:', 56), ('only one can flag a zero gap', 44),
                                    ('the comparison video', 44)])
    tile(d, (900, 980, 2380, 1240), [('FreeCAD + Claude course playlist', 56), ('the whole course, from lesson 1', 44)])
    d.rounded_rectangle((180, 1110, 760, 1230), radius=20, fill=(204, 0, 0))
    text(d, (470, 1170), 'Subscribe', 60, WHITE, anchor='mm')
    save(im, 'card-end.png')


# --- Short (S0, S2, S3) -------------------------------------------------------------------------------------------------
def card_why_short(step, build=3):
    """S2 (1080 x 1080), from above, the origin at the cup's middle: 1 XZ across, the peg's centre 27.5 in front, its
    copy 27.5 behind (13 out of the back wall); 2 YZ down the middle, 15 right → 15 left; 3 + "missing letter flips"."""
    CUR.clear()
    fr = (1080, 1080)
    im = Image.new('RGB', fr, WHITE)
    d = ImageDraw.Draw(im)
    k, o = 9, (540, 620)

    def t(x, y):
        return (o[0] + x * k, o[1] - y * k)

    def r(x0, x1, y0, y1, fill, ol=INK, w=4):
        a, z = t(x0, y1), t(x1, y0)
        d.rectangle((a[0], a[1], z[0], z[1]), fill=fill, outline=ol, width=w)
    r(-32, 32, -22, 22, CUP)
    r(-30, 30, -20, 20, INSIDE, INK, 2)
    r(10, 20, -35, -20, PAINT)
    d.ellipse((o[0] - 8, o[1] - 8, o[0] + 8, o[1] + 8), fill=INK)
    text(d, (540, 1000), 'from above: front at the bottom', 44, GREY, anchor='mm', frame=fr)
    if step == 1:
        # Short cut 2 (REVIEW-watch-fc17-short-c1): builds a plane + peg, b + the path across, s1 + the copy and
        # "13 out"; no 27.5 (never spoken)
        d.line((t(-44, 0), t(44, 0)), fill=BLUE, width=7)
        text(d, (t(-44, 0)[0], t(0, 0)[1] - 64), 'XZ', 52, BLUE, frame=fr)
        c = mirror((15, -27.5), 'XZ')
        if build >= 2:
            f10.dashed(d, t(15, -27.5), t(c[0], c[1] - 2.5), ORANGE, width=6)
            text(d, (t(10, 0)[0] - 24, t(0, 28)[1]), 'straight across', 44, ORANGE, anchor='rm', frame=fr)
        if build >= 3:
            r(10, 20, 20, 35, BACKFILL, PAINT, 4)
            text(d, (540, 240), 'front → back · 13 out', 50, ORANGE, anchor='mm', frame=fr)
            text(d, (t(21, 0)[0] + 12, t(0, 29)[1]), '13 out', 44, PAINT, anchor='lm', frame=fr)
    else:
        d.line((t(0, -38), t(0, 28)), fill=GREEN, width=7)
        text(d, (t(2, 16)[0], t(2, 16)[1]), 'YZ', 52, GREEN, frame=fr)
        c = mirror((15, -27.5), 'YZ')
        f10.dashed(d, t(15, -27.5), t(c[0] + 2, c[1]), ORANGE, width=6)
        r(-20, -10, -35, -20, COPYFILL, GREEN, 4)
        text(d, (540, 330), '15 right → 15 left', 50, ORANGE, anchor='mm', frame=fr)
    if step == 3:
        text(d, (540, 245), 'missing letter flips', 56, ORANGE, anchor='mm', frame=fr)
    axis_key(d, (60, 40), AXIS_S, px=40, frame=fr)
    save(im, f'card-why-s{step}{"ab"[build - 1] if step == 1 and build < 3 else ""}.png')


def band_lines(name, lines, y0, px_list, fill=ORANGE + (242,), col=WHITE):
    """Short overlay (RGBA 1080 x 1920): lines centred, each on its own band (draw_fc16.band_lines)."""
    CUR.clear()
    fr = (1080, 1920)
    im = Image.new('RGBA', fr, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = y0
    for s, px in zip(lines, px_list):
        f = b.font(b.B, px)
        w = d.textlength(s, font=f)
        d.rectangle(((1080 - w) / 2 - 18, y - 8, (1080 + w) / 2 + 18, y + px + 12), fill=fill)
        d.text(((1080 - w) / 2, y), s, font=f, fill=col + (255,))
        if (1080 - w) / 2 - 18 < 0 or len(s) > 32:
            PROBLEMS.append(f'{s!r}: wider than the Short / over 32')
        CUR.append((s, px))
        y += px + 26
    save(im, name)


def short_overlays():
    band_lines('card-short-head.png', HEAD, 60, (76, 76))
    band_lines('short-head.png', HEAD, 60, (76, 76))
    band_lines('short-q.png', ['Peg at x 25, mirror across YZ:', 'where does the copy land?'], 1240, (50, 50),
               fill=WHITE + (245,), col=INK)
    band_lines('short-series.png', ['Full lesson: FreeCAD plus', 'Claude course, lesson 17'], 1240, (50, 50),
               fill=(219, 234, 254, 250), col=BLUE)


# --- source overlays ----------------------------------------------------------------------------------------------------
def src_chip(d, xy, s, col, px=64, rgba=True):
    """A chip on a source frame (opaque light box, coloured words; draw_fc16.src_chip); returns its box."""
    f = b.font(b.B, px)
    lines = s.split('\n')
    w = max(d.textlength(x, font=f) for x in lines)
    x, y = xy
    h = (px + 16) * len(lines) + 20
    a = (lambda c, al=255: c + (al,)) if rgba else (lambda c, al=255: c)
    box = (x, y, round(x + w + 44), y + h)
    d.rounded_rectangle(box, radius=16, fill=a(WHITE, 245), outline=a(col), width=5)
    for i, ln in enumerate(lines):
        d.text((x + 22, y + 10 + i * (px + 16)), ln, font=f, fill=a(col))
        CUR.append((ln, round(px * 0.8)))
        if len(ln) > 32 or '%' in ln:
            PROBLEMS.append(f'{ln!r}: chip line')
    if box[2] > SW or box[3] > SH or box[1] < TOP_BAND:
        PROBLEMS.append(f'{s!r}: chip off the frame / in the top band {box}')
    return box


def chip_file(slug, s, xy, col=ORANGE, px=64):
    im, d = source()
    box = src_chip(d, xy, s, col, px)
    name = f'ov-chip-{slug}.png'
    save(im, name)
    DRAWN[name] = box
    return box


def chips():
    chip_file('cc-version', 'Claude Code 2.1.308 · Sonnet 5.5', RUN_CHIP, INK, px=52)
    chip_file('run-A1', f"not asked to check · ${RUNS['A1']['cost_usd']:.2f}", RUN_CHIP, BLUE, px=52)
    chip_file('run-B1', f"asked to check · ${RUNS['B1']['cost_usd']:.2f}", RUN_CHIP, BLUE, px=52)


def code_panel(name, lines, xy, anchor='lb', title='checked by code'):
    im, d = source()
    box = code_box(d, xy[0], xy[1], lines, title, PX, 0.8, anchor)
    for t in lines + [title]:
        if len(t) > 32:
            PROBLEMS.append(f'{t!r}: code panel line over 32')
    save(im, name)
    DRAWN[name] = tuple(round(v) for v in box)
    return box


def panels():
    fx, tr, pr = NUM['q4_fix_yz'], NUM['q2_trap'], NUM['q6_proof']
    assert fx['x_runs_front'] == [[-20.0, -10.0], [10.0, 20.0]] and fx['x_runs_back'] == [] and fx['solids'] == 1
    code_panel('ov-in-F1.png', ['2 pegs on the front', 'back clear'], PANEL_LL)
    assert tr['x_runs_back'] == [[10.0, 20.0]] and tr['behind_back'] == 13.0 and tr['solids'] == 1
    assert tr['x_runs_front'] == [[10.0, 20.0]] and tr['y_max'] == 35.0
    code_panel('ov-in-F5.png', ['copy at y 20 to 35: behind', 'front: 1 peg · one solid', 'no message, no mark'],
               PANEL_LL)
    assert fx['centre_gap'] == 30.0 and fx['face_gap'] == 20.0 and fx['y_extent'] == 57.0
    # cut 2 (REVIEW-watch-fc17-c1 must-fix 1): each box builds (a = its first line) and holds 8 s+; F8 keeps the
    # spoken lines only (the gap and the back have their own Measure / back shots)
    f8 = ['pegs x 10 to 20, −20 to −10', '15 + 15 = 30 centre to centre']
    code_panel('ov-in-F8a.png', f8[:1], PANEL_LL)
    code_panel('ov-in-F8.png', f8, PANEL_LL)
    assert NUM['q4_fix_vaxis']['volume'] == fx['volume']
    code_panel('ov-in-F9a.png', ['sketch axis = Base YZ'], PANEL_LL)
    code_panel('ov-in-F9.png', ['sketch axis = Base YZ', 'same part, same volume'], PANEL_LL)
    p20, w3 = pr['peg_x20'], pr['wall3']
    assert p20['x_runs_front'] == [[-25.0, -15.0], [15.0, 25.0]] and p20['centre_gap'] == 40.0
    assert p20['face_gap'] == 30.0 and p20['x_runs_back'] == []
    code_panel('ov-in-K1a.png', ['peg_x 20: 40 centre to centre'], PANEL_LL)
    code_panel('ov-in-K1.png', ['peg_x 20: 40 centre to centre', '30 between them'], PANEL_LL)
    assert w3['solids'] == 1 and w3['y_extent'] == 58.0 and w3['x_runs_back'] == []
    code_panel('ov-in-K2.png', ['wall 3: one solid', '58 front to back, back clear'], PANEL_LL)
    xz = pr['xz_peg_x20']
    assert xz['x_runs_back'] == [[15.0, 25.0]] and xz['behind_back'] == 13.0
    code_panel('ov-in-K3.png', ['fixed file, peg_x 20: copy −20', 'XZ file, peg_x 20: copy behind'], PANEL_LL)
    code_panel('ov-sk-F4a.png', ['drawn on the XZ plane'], PANEL_LL, title="the peg's sketch (lesson 14)")
    code_panel('ov-sk-F4.png', ['drawn on the XZ plane', 'so XZ looks right. It is not.'], PANEL_LL,
               title="the peg's sketch (lesson 14)")
    for run in ('A1', 'B1'):
        at = RUNS[run]['at']
        assert RUNS[run]['pass'] and sorted(at) == ['15', '20', '8', 'w3']
        assert all(v['x_runs_back'] == [] and len(v['x_runs_front']) == 2 for v in at.values())
    code_panel('ov-cc-A1.png', ['its file: peg_x 15, 20, 8', 'and wall 3:', '2 pegs front, back clear'], CC_PANEL)
    assert NUM['q4_fix_yz']['y_min'] == -35.0 and NUM['q10_lesson16_cup']['w2']['outside'][1] == 44.0  # 35 − 22 = 13
    code_panel('ov-cc-B1.png', ['its file: peg_x 15, 20, 8', 'and wall 3: passed', 'pegs stick out 13',
                                'hanging hole: back wall'], CC_PANEL)


def ov_lines(name, lines, step, box, px=56, one=False):
    """Lower-left panel: the lines up to `step` (the newest blue, earlier grey; `one`: all in ink)."""
    im, d = source()
    d.rounded_rectangle(box, radius=18, fill=WHITE + (245,), outline=PARTLINE + (255,), width=4)
    f = b.font(b.B, px)
    y = box[1] + 36
    for i, ln in enumerate(lines[:step]):
        col = (INK if one else BLUE if i == step - 1 else GREY) + (255,)
        CUR.append((ln, round(px * 0.8)))
        d.text((box[0] + 32, y), ln, font=f, fill=col)
        bb = d.textbbox((box[0] + 32, y), ln, font=f)
        if bb[2] > box[2] - 10 or bb[3] > box[3] - 10:
            PROBLEMS.append(f'{ln!r}: outside its panel {bb}')
        if len(ln) > 44:
            PROBLEMS.append(f'{ln!r}: over 44')
        y += round(px * 1.35) + round(px * 0.4)
    save(im, name)


RECAP = ['Plane = crease halfway between', 'YZ: x is missing, so x flips']
TURN = ['Your turn: cup with its corner', 'on the origin, inside x 0 to 60,', 'peg at x 45. Mirror across YZ:',
        'where? On the cup?', 'Where must the fold be for x 15?']
SUB = [['Lesson 18: a round pen cup', 'comes out twice as wide'],
       ['Every fix tested in both programs,', 'by hand and with Claude · Subscribe']]
F15_LINES = ['run 1: peg_x 15, 20, 8, wall 3', 'run 2: the same', 'both: 2 pegs front, back clear']
KIT_LABEL = 'its file, saved by our kit\nafter the run (still)'


# --- F15 stills ---------------------------------------------------------------------------------------------------------
def still_a1():
    """Run one: its after.png (Front view, both pegs square-on), the Claude Code footer masked; then the cup cropped
    1.5x, both pegs ringed, the panel beside it and the whole still inset with the crop boxed (draw_fc16.still)."""
    CUR.clear()
    src = os.path.join(TAKES, 'runs', 'A1', 'after.png')
    im = Image.open(src).convert('RGB')
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1640, CC_RIGHT - 3, 1790), fill=WHITE)              # "auto mode on (shift+tab to cycle)"
    src_chip(d, (1600, 1400), 'its file, front (still)', INK, px=56, rgba=False)
    save(im, 'st-A1.png')
    CUR.clear()
    full = Image.open(src).convert('RGB')
    ImageDraw.Draw(full).rectangle((0, 1640, CC_RIGHT - 3, 1790), fill=WHITE)
    z = Image.new('RGB', (SW, SH), WHITE)
    d = ImageDraw.Draw(z)
    x0, y0, x1, y1 = A1_CROP
    cw, ch = round((x1 - x0) * A1_K), round((y1 - y0) * A1_K)
    cx0, cy0 = 50, 300
    z.paste(full.crop(A1_CROP).resize((cw, ch), Image.LANCZOS), (cx0, cy0))
    d.rectangle((cx0 - 3, cy0 - 3, cx0 + cw + 2, cy0 + ch + 2), outline=PARTLINE, width=3)
    for px0, py0, px1, py1 in A1_PEGS:
        a = (cx0 + (px0 - x0) * A1_K - 40, cy0 + (py0 - y0) * A1_K - 40)
        e = (cx0 + (px1 - x0) * A1_K + 40, cy0 + (py1 - y0) * A1_K + 40)
        d.ellipse((a[0], a[1], e[0], e[1]), outline=ORANGE, width=10)
    text(d, (cx0, 190), 'its file, front (still)', 56, INK, frame=(SW, SH), safe=False)
    text(d, (cx0, cy0 + ch + 30), 'two pegs on the front', 48, INK, frame=(SW, SH), safe=False)
    pbx = cx0 + cw + 90
    pbox = tuple(round(v) for v in code_box(d, pbx, cy0, F15_LINES, 'checked by code', PX, 0.8))
    iw = 960
    ki = iw / SW
    th = full.resize((iw, round(SH * ki)), Image.LANCZOS)
    iy = pbox[3] + 60
    z.paste(th, (pbx, iy))
    d.rectangle((pbx - 2, iy - 2, pbx + iw + 2, iy + th.height + 2), outline=PARTLINE, width=3)
    d.rectangle((pbx + round(x0 * ki), iy + round(y0 * ki), pbx + round(x1 * ki), iy + round(y1 * ki)),
                outline=ORANGE, width=5)
    text(d, (pbx, iy + th.height + 14), 'whole still', 44, GREY, frame=(SW, SH), safe=False)
    if pbox[2] > SW or iy + th.height + 70 > SH:
        PROBLEMS.append(f'st-A1z: panel / inset off the frame {pbox}')
    save(z, 'st-A1z.png')
    DRAWN['st-A1z.png:panel'] = pbox
    DRAWN['st-A1z.png:crop'] = (cx0, cy0, cx0 + cw, cy0 + ch)


def still_b1():
    """Run two: the saved file (our kit's lab_save after the run) in the take kit's Front and Rear views: pegs ringed
    on the front, the back wall clear (only the hanging hole) on the rear; the panel lower left, off the cup."""
    for side, src, lab in (('f', 'front', 'its file, front (still)'), ('b', 'rear', 'its file, back (still)')):
        CUR.clear()
        im = Image.open(os.path.join(TAKES, 'stills', f'{src}-B1.png')).convert('RGB')
        d = ImageDraw.Draw(im)
        if side == 'f':
            for x0, y0, x1, y1 in PEGS_STILL:
                d.ellipse((x0 - 50, y0 - 50, x1 + 50, y1 + 50), outline=ORANGE, width=10)
        else:
            x0, y0, x1, y1 = CUP_STILL
            d.rounded_rectangle((x0 - 20, y0 - 20, x1 + 20, y1 + 20), radius=30, outline=GREEN, width=10)
            src_chip(d, (x1 + 50, 1150), 'back clear', GREEN, px=60, rgba=False)
            hx, hy = HOLE_STILL
            text(d, (hx, hy + 70), 'hanging hole', 48, INK, anchor='ma', frame=(SW, SH), safe=False)
        src_chip(d, CHIP_TL, KIT_LABEL, INK, px=52, rgba=False)
        src_chip(d, (CHIP_TL[0], CHIP_TL[1] + 190), lab, BLUE, px=52, rgba=False)
        pbox = tuple(round(v) for v in code_box(d, 40, 1690, F15_LINES, 'checked by code', 52, 0.8, 'lb'))
        if pbox[2] > CUP_STILL[0] - 10:
            PROBLEMS.append(f'st-B1{side}: panel {pbox} reaches the cup')
        save(im, f'st-B1{side}.png')
        DRAWN[f'st-B1{side}.png:panel'] = pbox


def main():
    os.makedirs(OUT, exist_ok=True)
    b.OUT = OUT
    PROBLEMS.clear()
    LOG.clear()
    DRAWN.clear()
    for s in range(1, 5):
        card_fold(s)
    for s in range(1, 4):
        card_names(s)
    for s in range(1, 7):
        card_top(s)
    for s in range(1, 4):
        card_axis(s)
    card_centred()
    card_end()
    for s in range(1, 4):
        card_why_short(s)
    card_why_short(1, 1)
    card_why_short(1, 2)
    short_overlays()
    chips()
    panels()
    for s in (1, 2):
        ov_lines(f'rc-{s}.png', RECAP, s, (20, 1400, 1300, 1690))
    ov_lines('yt-1.png', TURN, 5, (20, 1130, 1300, 1690), one=True)
    for i, lines in enumerate(SUB, 1):
        ov_lines(f'sub-{i}.png', lines, 2, (20, 1470, 1560, 1690), px=54, one=True)
    still_a1()
    still_b1()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
