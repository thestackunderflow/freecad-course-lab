"""FreeCAD course lesson 16 (the hanging hole: a Pocket typed 2 deep, as thick as the wall, closes to a 1 mm skin when
the wall goes to 3; Through all opens it but also drills the front wall; the fix: Length = Params.wall) cards, chips,
rings, locators, panels and the two Claude-file stills, SCRIPT-fc16.md rev 2 sections 0.1, 1 and 3 and
SCRIPT-fc16-short.md. The draw_fc15.py pattern (draw_fx20 helpers as b, draw_fc10 as f10); the skewer and the
section drawings are draw_sc16.py's (solidcraft-course-lab) with FreeCAD words ("Pocket Length 2", "Through all",
"to the last face it meets"); the whole-cup drawings keep the Thickness's round outside corners (radius = wall).
Light, 2560 x 1440 cards, each build adds (earlier lines stay, grey), card lines 44 columns, chips / panels 32, no
percent sign, no angle brackets, "−" in drawn sums, never "A1" / "B1" on screen. Every number is NUMBERS.json's
(out/fc16), the script's arithmetic, a lesson number or the run log's.
  full frame (RGB 2560 x 1440): card-skewer-1..4 (F2), card-why-1..4 (F7), card-why-5 (F8), card-end (F16)
  Short: card-why-s1..3 (RGB 1080 x 1080, S2), card-short-head (RGBA 1080 x 1920, frame 1 from 0.0 s),
      short-q / short-series (RGBA 1080 x 1920: the pinned question and the series card, S3)
  F14 stills (RGB 2880 x 1800): st-A1 / st-B1 = out/fc16/stills/inside-*.png (lab/fc16_still.sh: each run's saved
      file, the take kit's Inside view, 64 mm high at 0 20 30) + label; st-A1z / st-B1z = the back wall cropped 1.25x,
      the hole ringed, the F14 panel beside it and the whole still inset with the crop boxed
  source overlays (RGBA 2880 x 1800): ov-chip-* (CHIP_FILES), ov-f0-T / ov-front-A / ov-dot-R (chip + ring), ov-ring-*,
      ov-loc-* (labelled locator boxes on the full window), ov-in-* / ov-cc-* / ov-log-* / ov-quote-B1a/b panels,
      rc-1..3 / yt-1 (F15), sub-1..2 (F11)
Geometry (source px, 21 Nov, gridded frames + tesseract in fc8-ocr:1, session scratchpad fc16r): see the constants
below; Claude Code rows from 2 fps OCR of runs/*/screen.mp4 (x 0-1160) and 15 fps around the reply.
Run in the draw image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fc16.py
Test: tests/test_draw_fc16.py"""
import json
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw_fx20 as b  # noqa: E402
import draw_fc10 as f10  # noqa: E402

LAB = b.LAB
OUT = os.path.join(LAB, 'video', 'frames-fc16')
TAKES = os.path.join(LAB, 'out', 'fc16')
W, H, SW, SH = b.W, b.H, b.SW, b.SH
INK, GREY, WHITE, DONE = b.INK, b.GREY, b.WHITE, b.DONE
BLUE, ORANGE, RED, GREEN = b.BLUE, b.ORANGE, b.RED, b.GREEN
DONEFILL = b.DONEFILL
PARTLINE = f10.PARTLINE
CARD, CARDEDGE, STICK, INSIDE, SKIN = (253, 230, 138), (161, 98, 7), (180, 120, 60), (226, 232, 240), (251, 146, 60)
FRONTHOLE = (254, 202, 202)
canvas, source, header = b.canvas, b.source, b.header
PROBLEMS, LOG, CUR = b.PROBLEMS, b.LOG, b.CUR
code_box = f10.code_box
NUM = json.load(open(os.path.join(TAKES, 'NUMBERS.json'), encoding='utf-8'))
Q3, Q4, Q5, Q6, RUNS = NUM['q3_typed2_wall3'], NUM['q4_through_wall3'], NUM['q5_fix'], NUM['q6_proof'], NUM['runs']
PX = 63                                 # code panels on the 2880 frame
TOP_BAND = 160                          # the title bar + the REAL RECORDING chip (top right, footage-fx2 chip_where)
CC_RIGHT = 1160                         # Claude Code's pane: x 0-1155 on runs/*/screen.mp4
DRAWN, LOC_DRAWN, GAPS, CHIP_FILES = {}, {}, {}, []

# --- measured: GUI takes (source px; times are each take's events.jsonl seconds) -------------------------------------
RING_RESULT = (2186, 762, 2480, 810)    # T 83.8-93.3: Measurement "Result: 1.00 mm" (OCR x 2201-2456, y 775-792)
LOC_MEASURE = (2190, 590, 2870, 815)    # T: the Measurement panel (title y ~605 .. Result row)
RING_TYPE = (2530, 800, 2856, 1014)     # A 18.8-24.8 (F 20.0-26.0): the open Type list, Dimension .. Up to shape
LOC_TYPE = (2190, 680, 2870, 1020)      # A / F: Pocket Parameters, Mode .. Taper rows
RING_DIM = (2530, 806, 2836, 850)       # D 74.9-90.3: Type "Dimension" (field x 2529-2835, y 810-846)
RING_RESULT3 = (2252, 1005, 2398, 1041)  # F 34.0-41.4: Expression Editor "Result 3.00" (OCR x 2263-2383, y 1011-1029)
EXPR_F = (2240, 825, 2872, 1097)        # F 31.2-41.4: the Expression Editor box
RING_FX = (2530, 856, 2826, 910)        # F 41.4-47.3: Length "3.00" + the blue fx icon (field y 863-903)
RING_HOLE_FRONT = (1540, 1036, 1820, 1316)  # A 52.0-61.0 Front view (30 mm high): the hole, centre (1680, 1176)
RING_WALL = (580, 548, 960, 596)        # Params row 4 `wall` (rows y 410 + 54 n; R 18.7, T 13.2, K 19.2)
RING_HOLE_SIZE = (580, 710, 960, 758)   # Params row 7 `hole_size` (R 22.0, K 76.9)
LOC_PARAMS = (470, 370, 980, 775)       # the Params sheet rows 1-7
RING_TREE = (40, 422, 340, 518)         # D 0.1-8.6 and 65+: tree rows Pad 439, Thickness 471, Pad001 504 (R's tree is
                                        # collapsed all take: Params, Cup only)
LOC_C1 = (2210, 925, 2830, 982)         # D 34.6: Constraints list, "Constraint1 (5 mm)" row
EXPR_D = (1325, 746, 1975, 1045)        # D 36.8-43.4: the Expression Editor over the Insert Diameter box
DOT_R = (1680, 875)                     # R 48.2-52.4 Rear view (70 mm high, at 0 22 25): x 0, z 30 on the back face
DOT_BOX = (DOT_R[0] - 22, DOT_R[1] - 22, DOT_R[0] + 22, DOT_R[1] + 22)
CIRCLE_D = (1680, 885)                  # D 26.7-29.6: the circle's centre; the typed "5 mm" box x 1710-1884, y 696-741
CHIP_T = (1500, 1180)                   # T 90 / D 113.7 Inside view: below the Measure marks (y 909-1041), in the Short crop
CHIP_A = (1250, 1380)                   # A 52-61 Front view: under the hole ring
CHIP_TL = (540, 290)                    # top left of the 3D view, under the toolbars
VAL_CELL = {4: (1000, 535), 7: (1000, 697)}   # Params rows 4 / 7: right of column B (cells C-D empty)
VAL_LEN = (2070, 840)                   # D 85.0: left of the task panel, on the cup's face, clear of the hole
VAL_DIAM = (1080, 300)                  # D 28.8: above the cup (cup top y 471), left of the "5 mm" box
PANEL_LL = (40, 1690)                   # lower left (tree / property view and the 3D view's left), anchor bottom
# --- measured: Claude runs (2 fps + 15 fps OCR) ----------------------------------------------------------------------
CC_PANEL = (1170, 1590)                 # FreeCAD's property area + 3D view below the cup (cup y up to 1272), bottom
RUN_CHIP = (1170, 1606)                 # run / version chip, under the panels, above y 1700
LOC_PROMPT = {'A1': (8, 800, 1152, 1010), 'B1': (8, 800, 1152, 1110)}   # the prompt rows while typing (2.1-10.3 / -14.3)
RING_A1_EXPR = (746, 807, 1152, 861)    # "Params.wall + 1." x 758-1143, row y 814-854, from 35.93 to the end
RING_A1_VOL = [(676, 1199, 1058, 1249), (45, 1249, 303, 1299)]   # "(39.3, 58.9 and" / "98.2 mm³)." rows 1206 / 1255
RING_A1_WHATEVER = (40, 906, 880, 952)  # "wall whatever the wall thickness." row y 912-944, 10.5-35.5 (sent prompt)
RING_B1_THEN = (40, 1003, 1150, 1104)   # "Then check ... what you find." rows y 1010-1100, 12.5-14.28 (typing)
RING_B1_INTERIM = (40, 1003, 1152, 1154)  # "... binding it to / Params.wall and not using Through All, which / would also
                                          # cut the opposite wall." rows y 1010-1148, 48.8-61.4
ROWS = {  # (top y, bottom y, first visible s, text): rows the footage rings or boxes
    'A1_expr': (814, 854, 35.93, 'through. I set its depth to Params.wall + 1.'),
    'A1_vol': (1206, 1292, 35.93, 'times the wall thickness (39.3, 58.9 and / 98.2 mm³). That means'),
    'A1_called': (471, 511, 35.93, 'Called freecad 5 times (ctrl+o to expand)'),
    'A1_calling': (1108, 1148, 15.0, 'Calling freecad N times... (until 35.5)'),
    'A1_whatever': (912, 944, 10.5, 'wall whatever the wall thickness. (typing: y 953-1002 at 9.5-10.3)'),
    'B1_then': (1010, 1100, 12.5, 'Then check the back wall, the front wall / and the peg and tell me what you find.'),
    'B1_then_sent': (912, 1050, 14.5, 'same lines after Enter, y 912-1050, until 27.0'),
    'B1_interim': (1010, 1148, 48.8, 'binding it to / Params.wall and not using Through All, which / would also cut'),
    'B1_final': (None, None, None, 'I set Pocket.Length = Params.wall. / I didn\'t use Through All ...: never on '
                 'screen (printed and scrolled off at 61.4, 15 fps OCR): ov-quote-B1a / -B1b re-set them'),
}
MASK = {  # Claude Code footer / spinner / token mask: (t0, t1, y0) = white from y0 to the pane bottom, x 0-1160
    'A1': [(0.0, 4.0, 898), (4.0, 6.0, 947), (6.0, 8.0, 996), (8.0, 10.34, 1045), (10.34, 12.0, 996),
           (12.0, 35.93, 1192), (35.93, 44.0, 1437)],
    'B1': [(0.0, 4.0, 898), (4.0, 6.0, 947), (6.0, 8.0, 996), (8.0, 10.0, 1045), (10.0, 11.5, 1094),
           (11.5, 14.28, 1143), (14.28, 16.0, 1100), (16.0, 16.5, 1192), (16.5, 17.0, 1241), (17.0, 48.5, 1437), (48.5, 61.4, 1290),
           (61.4, 69.9, 1437)],
}
HEAD_MASK = {  # header + "Auto mode is now Claude Code's default" banner: (t0, t1, y1) = white from 0 to y1, x 0-1160
    'A1': [(0.0, 35.93, 712), (35.93, 44.0, 80)],
    'B1': [(0.0, 27.25, 712), (27.25, 48.8, 369), (48.8, 69.9, 0)],
}
# --- stills ------------------------------------------------------------------------------------------------------------
STILL_SRC = {r: os.path.join(TAKES, 'stills', f'inside-{r}.png') for r in ('A1', 'B1')}
HOLE_LIGHT = (1680, 962)                # background grey through the hole (light pixels x 1638-1722, y 946-976)
HOLE_AT = (1680, 986)                   # the hole's outline centre (x 1624-1736, y 948-1024)
WALL_PX = (1680, 1100)                  # the back wall's inside face, below the hole
TASK_PANEL = (2186, 586, 2880, 714)     # PartDesign "Start Part / New Body" panel (no active body; over the rim's
                                        # right corner, so not painted: the crop keeps clear of it)
STILL_BG = (247, 247, 247)
STILL_CROP = (1000, 716, 2180, 1453)    # 16:10 on the back wall's inside face (x 1004-2356, y 668-1305), clear of
                                        # the Start Part panel
STILL_K = 1.25


def g(v):
    return f'{v:g}'


def f2(v):
    return f'{v:.2f}'


def text(d, xy, s, size=56, fill=INK, **kw):
    return f10.text(d, xy, s, size, fill, **kw)


def save(im, name):
    b.OUT = OUT
    b.save(im, name)


def lit(i, step, on=INK):
    return on if i == step else GREY


def chip_on(d, xy, s, col=ORANGE, px=52, frame=(W, H), edge=None):
    """A chip on a card: rounded light box, coloured words (logged); two lines when s has a newline."""
    f = b.font(b.B, px)
    lines = s.split('\n')
    w = max(d.textlength(x, font=f) for x in lines)
    x, y = xy
    box = (x, y, x + w + 40, y + (px + 14) * len(lines) + 16)
    d.rounded_rectangle(box, radius=14, fill=WHITE, outline=edge or col, width=4)
    for i, ln in enumerate(lines):
        text(d, (x + 20, y + 10 + i * (px + 14)), ln, px, col, frame=frame)
    return box


def arrow_down(d, x, y0, y1, col, w=12):
    d.line((x, y0, x, y1 - 30), fill=col, width=w)
    d.polygon([(x - 28, y1 - 40), (x + 28, y1 - 40), (x, y1)], fill=col)


# --- F2: the skewer (four rows, one per build; draw_sc16.card_skewer) ------------------------------------------------
def card_skewer(step):
    im, d = canvas()
    header(d, 'A skewer and a cardboard box')
    t, near, far = 44, 760, 1480
    rows = [  # (near wall sheets, mark from tip, tip x, chip)
        (1, t + 14, near + t + 14, 'push to the mark'),
        (2, t + 14, near + t + 14, 'same mark, thicker: stuck'),
        (2, None, far + t + 90, 'all the way: far side too'),
        (2, 2 * t + 14, near + 2 * t + 14, 'mark = the cardboard'),
    ]
    for i, (sheets, mark, tip, label) in enumerate(rows[:step], start=1):
        y = 300 + (i - 1) * 270
        on = i == step
        edge = CARDEDGE if on else DONE
        x_out = near - (sheets - 1) * t
        d.rectangle((x_out, y - 90, near + t, y + 90), fill=CARD if on else (245, 240, 225), outline=edge, width=4)
        if sheets == 2:
            d.line((near, y - 90, near, y + 90), fill=edge, width=3)
        d.rectangle((far, y - 90, far + t, y + 90), fill=CARD if on else (245, 240, 225), outline=edge, width=4)
        d.line((near + t, y + 90, far, y + 90), fill=edge, width=4)
        d.line((150, y, tip - 24, y), fill=STICK if on else DONE, width=14)
        d.polygon([(tip - 26, y - 9), (tip - 26, y + 9), (tip, y)], fill=STICK if on else DONE)
        if mark:
            mx = tip - mark
            d.line((mx, y - 26, mx, y + 26), fill=INK if on else GREY, width=8)
        if i == 3:
            for wx in (near - t, far):
                d.rectangle((wx + 4, y - 9, wx + t - 4, y + 9), fill=STICK if on else DONE)
        chip_on(d, (1640, y - 32), label, INK if on else GREY, px=48, edge=ORANGE if on else DONE)
    text(d, (150, 1270), 'pen mark = how deep you push', 44, GREY, path=b.R)
    save(im, f'card-skewer-{step}.png')


# --- F7 / F8: the top section through the hole ------------------------------------------------------------------------
WHY_SUMS = [(1, '2 − 2 = 0'), (2, '3 − 2 = 1 mm left'), (3, 'that is the skin')]


def card_why(step):
    """1 wall 2: the Pocket 2 from the outside face just reaches the inside, "2 − 2 = 0"; 2 wall 3: the outside face out
    by 1, the Pocket (still 2) stops short, "3 − 2 = 1 mm left"; 3 the skin shaded, "that is the skin"; 4 "2 never hears
    about the wall". 5 (F8): the whole cup from above, round outside corners, the Through all arrow out of the back
    wall, across the empty cup, through the front wall: "to the last face it meets"."""
    im, d = canvas()
    header(d, 'Seen from above, cut through the hole')
    if step == 5:
        return card_why_all(im, d, 3)
    k, x0, x1, cx, y_in = 120, 500, 2060, 1280, 1000
    wall = 2 if step <= 1 else 3
    y_out = y_in - wall * k
    hw = round(2.5 * k)
    d.rectangle((x0, y_in, x1, 1300), fill=INSIDE)
    text(d, (cx, 1200), 'inside of the cup', 48, GREY, anchor='mm')
    d.rectangle((x0, y_out, x1, y_in), fill=DONEFILL, outline=INK, width=6)
    if step >= 2:
        yo2 = y_in - 2 * k
        for xx in range(x0, x1, 60):
            d.line((xx, yo2, xx + 30, yo2), fill=GREY, width=4)
        text(d, (x1 + 30, yo2 - 30), 'wall 2', 44, GREY, path=b.R)
        text(d, (x1 + 30, y_out - 30), 'wall 3', 44, INK)
    else:
        text(d, (x1 + 30, y_out - 30), 'wall 2', 44, INK)
    cut_bot = y_out + 2 * k
    d.rectangle((cx - hw, y_out - 3, cx + hw, min(cut_bot, y_in)), fill=WHITE)
    d.line((cx - hw, y_out, cx - hw, min(cut_bot, y_in)), fill=INK, width=6)
    d.line((cx + hw, y_out, cx + hw, min(cut_bot, y_in)), fill=INK, width=6)
    if cut_bot < y_in:
        d.line((cx - hw, cut_bot, cx + hw, cut_bot), fill=INK, width=6)
    if step >= 3 and cut_bot < y_in:
        d.rectangle((cx - hw + 3, cut_bot + 3, cx + hw - 3, y_in - 3), fill=SKIN if step == 3 else (253, 205, 160))
        text(d, (cx + hw + 40, (cut_bot + y_in) // 2), 'skin 1 mm', 52, lit(3, step), anchor='lm')
    arrow_down(d, cx, y_out - 170, cut_bot, BLUE if step <= 2 else GREY)
    text(d, (cx + 50, y_out - 130), 'Pocket Length 2', 56, BLUE if step <= 2 else GREY, anchor='lm')
    text(d, (x1 - 300, y_out - 70), 'outside face', 44, GREY, path=b.R)
    for i, s in WHY_SUMS:
        if step >= i:
            chip_on(d, (150, 280 + (i - 1) * 110), s, lit(i, step), px=60 if i < 3 else 56,
                    edge=ORANGE if i == step else DONE)
    if step >= 4:
        chip_on(d, (150, 1240), '2 never hears about the wall', INK, px=60, edge=ORANGE)
    save(im, f'card-why-{step}.png')


WHY5_K, WHY5_WALL = 18, 3
WHY5_CORNER_R = WHY5_K * WHY5_WALL
WHY5_OUTER = None


def cup_from_above(d, cx, y_back_in, k, wall, inside_l=40, half=30, width=5):
    """The cup cut through the hole, seen from above: FreeCAD's Thickness grew outward, so the outside corners are round
    (radius = wall) and the inside corners sharp. Returns the outer box and the wall lines' y."""
    y_back_out = y_back_in - wall * k
    y_front_in = y_back_in + inside_l * k
    y_front_out = y_front_in + wall * k
    xl, xr = cx - (half + wall) * k, cx + (half + wall) * k
    outer = (xl, y_back_out, xr, y_front_out)
    d.rounded_rectangle(outer, radius=wall * k, fill=DONEFILL, outline=INK, width=width)
    d.rectangle((cx - half * k, y_back_in, cx + half * k, y_front_in), fill=INSIDE, outline=INK, width=max(2, width - 2))
    return outer, (y_back_out, y_back_in, y_front_in, y_front_out)


def card_why_all(im, d, step=3):
    """F8 in three builds (cut 2, WATCH-fc16-cut1 3 + 11): 1 the arrow through the back wall, FreeCAD's guide words on
    screen; 2 on across the inside to the far wall (one solid); 3 the front wall drilled, "front wall too"."""
    global WHY5_OUTER
    k, cx = WHY5_K, 1280
    outer, (y_bo, y_bi, y_fi, y_fo) = cup_from_above(d, cx, 420, k, WHY5_WALL)
    WHY5_OUTER = outer
    hw = round(2.5 * k)
    d.rectangle((cx - hw, y_bo - 2, cx + hw, y_bi), fill=WHITE)
    if step >= 3:
        d.rectangle((cx - hw, y_fi, cx + hw, y_fo + 2), fill=FRONTHOLE)
    tip = {1: y_bi + 160, 2: y_fi, 3: y_fo + 120}[step]
    arrow_down(d, cx, y_bo - 150, tip, RED, w=10)
    text(d, (cx + 60, y_bo - 120), 'Through all', 60, RED)
    text(d, (outer[2] + 40, (y_bo + y_bi) // 2), 'back wall', 44, INK, anchor='lm')
    chip_on(d, (150, 1230), 'FreeCAD guide: up to the last face it meets', INK if step == 1 else GREY, px=56,
            edge=ORANGE if step == 1 else DONE)
    if step >= 2:
        text(d, (outer[2] + 40, (y_fi + y_fo) // 2 - 60), 'far wall', 44, INK if step == 2 else GREY, anchor='lm')
        text(d, (cx + 40, (y_bi + y_fi) // 2 - 30), 'one solid:', 44, GREY, anchor='lm')
        text(d, (cx + 40, (y_bi + y_fi) // 2 + 30), 'the whole cup', 44, GREY, anchor='lm')
    if step >= 3:
        text(d, (outer[2] + 40, (y_fi + y_fo) // 2 + 10), 'front wall too', 48, RED, anchor='lm')
        chip_on(d, (110, 600), 'to the last face\nit meets:\nthe far wall', INK, px=48, edge=ORANGE)
    save(im, f'card-why-5-{step}.png')
    if step == 3:
        save(im, 'card-why-5.png')


def card_why_short(step):
    """S2 (1080 x 1080): 1 the Pocket 2 from the outside face reaches the inside, "2 − 2 = 0"; 2 wall 3, it stops short,
    "3 − 2 = 1 mm left"; 3 the whole cup from above, the Through all arrow into the front wall."""
    CUR.clear()
    fr = (1080, 1080)
    im = Image.new('RGB', fr, WHITE)
    d = ImageDraw.Draw(im)
    cx, k = 540, 60
    if step <= 2:
        wall = 2 if step == 1 else 3
        y_in = 640
        y_out = y_in - wall * k
        d.rectangle((80, y_in, 1000, 900), fill=INSIDE)
        d.rectangle((80, y_out, 1000, y_in), fill=DONEFILL, outline=INK, width=5)
        hw = round(2.5 * k)
        cut_bot = y_out + 2 * k
        d.rectangle((cx - hw, y_out - 2, cx + hw, min(cut_bot, y_in)), fill=WHITE)
        if cut_bot < y_in:
            d.rectangle((cx - hw, cut_bot, cx + hw, y_in - 3), fill=SKIN)
        arrow_down(d, cx, y_out - 120, cut_bot, BLUE, w=9)
        text(d, (540, 960), 'inside of the cup', 44, GREY, anchor='mm', frame=fr)
        text(d, (540, 130), ['2 − 2 = 0', '3 − 2 = 1 mm left'][step - 1], 72, ORANGE, anchor='mm', frame=fr)
        text(d, (540, 225), f'wall {wall}, Pocket Length 2', 52, INK, anchor='mm', frame=fr)
    else:
        kk = 12
        outer, (y_bo, y_bi, y_fi, y_fo) = cup_from_above(d, cx, 300, kk, WHY5_WALL, width=4)
        d.rectangle((cx - 30, y_bo - 2, cx + 30, y_bi), fill=WHITE)
        d.rectangle((cx - 30, y_fi, cx + 30, y_fo + 2), fill=FRONTHOLE)
        arrow_down(d, cx, y_bo - 80, y_fo + 60, RED, w=9)
        text(d, (540, 100), 'Through all', 60, RED, anchor='mm', frame=fr)
        text(d, (cx + 60, y_fo + 14), 'front wall', 44, RED, frame=fr)
        text(d, (outer[0], y_bo - 40), 'back wall', 44, INK, anchor='lm', frame=fr)
        chip_on(d, (80, 900), 'to the last face it meets', INK, px=52, frame=fr, edge=ORANGE)
    save(im, f'card-why-s{step}.png')


# --- F16 end card, the Short's head and S3 cards ------------------------------------------------------------------------
def tile(d, box, lines, col=INK):
    d.rounded_rectangle(box, radius=24, fill=(248, 250, 252), outline=PARTLINE, width=4)
    for i, (s, px) in enumerate(lines):
        text(d, (box[0] + 40, box[1] + 60 + i * (px + 30)), s, px, col if i == 0 else GREY)


def card_end():
    im, d = canvas()
    text(d, (180, 160), 'FreeCAD + Claude course', 72, INK)
    text(d, (180, 270), 'lesson 16: make the Pocket Length the wall', 60, BLUE)
    shot = Image.open(os.path.join(LAB, 'out', 'fc14', 'F', 'fix-iso.png')).convert('RGB').crop((1000, 250, 2400, 1650))
    im.paste(shot.resize((560, 560)), (180, 420))
    d.rectangle((180, 420, 740, 980), outline=PARTLINE, width=3)
    text(d, (180, 1000), 'Lesson 14: Thickness first', 48, INK)
    tile(d, (900, 420, 1560, 980), [('SolidCraft vs FreeCAD', 52), ('Assembly: only one can', 44),
                                    ('flag a zero gap', 44), ('the comparison video', 44)])
    tile(d, (1720, 420, 2380, 980), [('The whole course', 52), ('FreeCAD + Claude,', 44), ('from lesson 1', 44),
                                     ('playlist', 44)])
    d.rounded_rectangle((180, 1110, 760, 1230), radius=20, fill=(204, 0, 0))
    text(d, (470, 1170), 'Subscribe', 60, WHITE, anchor='mm')
    save(im, 'card-end.png')


HEAD = ('POCKET 2 DEEP, WALL 3:', 'HOLE CLOSED')


def band_lines(name, lines, y0, px_list, fill=ORANGE + (242,), col=WHITE):
    """Short overlay (RGBA 1080 x 1920): lines centred, each on its own band."""
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


def card_short_head():
    band_lines('card-short-head.png', HEAD, 60, (60, 76))


def short_cards():
    band_lines('short-q.png', ['Pocket 2 deep, wall goes to 4:', 'open or closed? Skin?'], 1240, (50, 50),
               fill=WHITE + (245,), col=INK)
    band_lines('short-series.png', ['Full lesson: FreeCAD plus', 'Claude course, lesson 16'], 1240, (50, 50),
               fill=(219, 234, 254, 250), col=BLUE)


# --- source overlays -----------------------------------------------------------------------------------------------------
def src_chip(d, xy, s, col, px=64, rgba=True):
    """A chip on a source frame (opaque light box, coloured words); returns its box."""
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
    CHIP_FILES.append(name)
    DRAWN[name] = box
    return box


def ring_on(d, box, col=ORANGE, ellipse=False, width=8):
    if ellipse:
        d.ellipse(box, outline=col + (255,), width=width)
    else:
        d.rounded_rectangle(box, radius=min(24, (box[3] - box[1]) // 2), outline=col + (255,), width=width)


def ring(name, boxes, col=ORANGE, ellipse=False, gap=None, width=8):
    im, d = source()
    for bx in boxes if isinstance(boxes, list) else [boxes]:
        ring_on(d, bx, col, ellipse, width)
    save(im, name)
    if gap:
        bb = boxes if not isinstance(boxes, list) else (min(x[0] for x in boxes), min(x[1] for x in boxes),
                                                        max(x[2] for x in boxes), max(x[3] for x in boxes))
        GAPS[name] = (bb, gap)


def locator(name, box, label, where='above'):
    """[locator: X] (SCRIPT §0.1): an orange box on the full window, labelled outside the box, before the close-up."""
    im, d = source()
    d.rounded_rectangle(box, radius=16, outline=ORANGE + (255,), width=7)
    f = b.font(b.B, 52)
    w = d.textlength(label, font=f)
    x = min(max(box[0], 20), SW - w - 64)
    y = box[1] - 96 if where == 'above' else box[3] + 18
    lab = (x, y, round(x + w + 40), y + 78)
    d.rounded_rectangle(lab, radius=14, fill=WHITE + (250,), outline=ORANGE + (255,), width=4)
    d.text((x + 20, y + 10), label, font=f, fill=ORANGE + (255,))
    CUR.append((label, round(52 * 0.8)))
    if lab[1] < TOP_BAND:
        PROBLEMS.append(f'{name}: label in the top band')
    save(im, name)
    LOC_DRAWN[name] = (box, lab)


def code_panel(name, lines, xy, anchor='lb', title='checked by code', extra=None):
    im, d = source()
    box = code_box(d, xy[0], xy[1], lines, title, PX, 0.8, anchor)
    for t in lines:
        if len(t) > 32:
            PROBLEMS.append(f'{t!r}: code panel line over 32')
    if extra:
        extra(d, box)
    save(im, name)
    DRAWN[name] = box
    return box


def quote(name, run, lines, xy, px=52, anchor='lb'):
    """Claude's own words re-set word for word from reply.txt (printed and scrolled off before any frame showed them)."""
    reply = ' '.join(open(os.path.join(TAKES, 'runs', run, 'reply.txt'), encoding='utf-8').read().split())
    assert ' '.join(lines) in reply, lines
    im, d = source()
    lines = list(lines)
    lines[0] = '“' + lines[0]
    lines[-1] = lines[-1] + '”'
    fh, fl = b.font(b.B, px), b.font(f10.MONO, px)
    title = "Claude's reply, quoted:"
    lh, pad = round(px * 1.3), round(px * 0.55)
    rows = [(title, fh)] + [(t, fl) for t in lines]
    x, y = xy
    w = max(d.textlength(t, font=f) for t, f in rows) + 2 * pad + 24
    h = lh * len(rows) + pad
    if anchor == 'lb':
        y -= h
    box = (x, y, round(x + w), round(y + h))
    d.rounded_rectangle(box, radius=round(px * 0.3), fill=(219, 234, 254, 250), outline=BLUE + (255,), width=4)
    d.rectangle((x + 10, y + 12, x + 22, y + h - 12), fill=BLUE + (255,))
    for i, (t, f) in enumerate(rows):
        d.text((x + pad + 24, y + pad * 0.6 + i * lh), t, font=f, fill=(BLUE if i == 0 else INK) + (255,))
        CUR.append((t, round(px * 0.8)))
    if box[2] > SW or box[3] > SH:
        PROBLEMS.append(f'{name}: quote off the frame')
    save(im, name)
    DRAWN[name] = box


def ov_lines(name, lines, step, box, px=56, one=False):
    """Lower-left panel: the lines up to `step` (the newest blue, earlier grey; `one`: all in ink)."""
    im, d = source()
    d.rounded_rectangle(box, radius=18, fill=WHITE + (245,), outline=PARTLINE + (255,), width=4)
    f = b.font(b.B, px)
    y = box[1] + 36
    for i, ln in enumerate(lines[:step]):
        col = (INK if one else BLUE if i == step - 1 else GREY) + (255,)
        for part in ln.split('\n'):
            CUR.append((part, round(px * 0.8)))
            d.text((box[0] + 32, y), part, font=f, fill=col)
            bb = d.textbbox((box[0] + 32, y), part, font=f)
            if bb[2] > box[2] - 10 or bb[3] > box[3] - 10:
                PROBLEMS.append(f'{part!r}: outside its panel {bb}')
            y += round(px * 1.35)
        y += round(px * 0.4)
    save(im, name)


# --- the frame-0 / front / rear composites ------------------------------------------------------------------------------
def composites():
    im, d = source()
    ring_on(d, RING_RESULT)
    DRAWN['ov-f0-T.png'] = src_chip(d, CHIP_T, f"Pocket 2, wall {g((Q3['outside_w'] - Q3['inside_w']) / 2)}: closed", RED)
    save(im, 'ov-f0-T.png')
    GAPS['ov-f0-T.png'] = (RING_RESULT, (760, 812))
    im, d = source()
    ring_on(d, RING_HOLE_FRONT, RED, ellipse=True, width=10)
    DRAWN['ov-front-A.png'] = src_chip(d, CHIP_A, 'Through all: front drilled', RED)
    save(im, 'ov-front-A.png')
    im, d = source()
    d.ellipse(DOT_BOX, fill=ORANGE + (255,), outline=WHITE + (255,), width=4)
    DRAWN['ov-dot-R.png'] = src_chip(d, (DOT_R[0] + 70, DOT_R[1] - 50), 'x 0, 30 up', ORANGE)
    save(im, 'ov-dot-R.png')


def chips():
    assert Q3['skin'] == 1.0 and not Q3['axis_air']['y20.05'] and NUM['q1_typed2_wall2']['open']
    chip_file('closed-w3', 'Pocket 2, wall 3: closed', CHIP_T, RED)
    chip_file('front-drilled', 'Through all: front drilled', CHIP_A, RED)
    chip_file('sum-3-2', f"3 − 2 = {g(Q3['skin'])} mm left", (2190, 830), RED, px=56)
    chip_file('sum-wall', 'wall − wall = 0', CHIP_TL, GREEN)
    chip_file('open-w2', 'Pocket 2, wall 2: open', CHIP_T, GREEN)
    chip_file('length-wall', 'Length = wall', CHIP_TL, GREEN)
    chip_file('x0-30', 'x 0, 30 up', (DOT_R[0] + 70, DOT_R[1] - 50), ORANGE)
    chip_file('lesson16', 'FreeCAD + Claude, lesson 16', CHIP_TL, BLUE)
    chip_file('course2', 'FreeCAD plus Claude\nlesson 16', CHIP_TL, BLUE)
    chip_file('sped-up', 'sped up', CHIP_TL, INK)
    chip_file('val-5', '5: the diameter', VAL_DIAM, ORANGE, px=56)
    chip_file('val-2', '2', VAL_LEN, ORANGE, px=56)
    chip_file('val-3', '3', VAL_CELL[4], ORANGE, px=56)
    chip_file('val-4', '4', VAL_CELL[4], ORANGE, px=56)
    chip_file('val-6', '6', VAL_CELL[7], ORANGE, px=56)
    chip_file('cc-version', 'Claude Code 2.1.308 · Sonnet 5.5', RUN_CHIP, INK, px=52)
    chip_file('run-A1', f"not asked to check · ${RUNS['A1']['cost_usd']:.2f}", RUN_CHIP, BLUE, px=52)
    chip_file('run-B1', f"asked to check · ${RUNS['B1']['cost_usd']:.2f}", RUN_CHIP, BLUE, px=52)


def rings():
    ring('ov-ring-result.png', RING_RESULT, gap=(760, 812))
    ring('ov-ring-type.png', RING_TYPE, gap=(795, 1020))
    ring('ov-ring-result3.png', RING_RESULT3, gap=(1003, 1043), width=6)
    ring('ov-ring-fx.png', RING_FX, BLUE, gap=(848, 918), width=6)
    ring('ov-ring-hole-front.png', RING_HOLE_FRONT, RED, ellipse=True, width=10)
    ring('ov-ring-wall.png', RING_WALL, gap=(543, 599))
    ring('ov-ring-hole_size.png', RING_HOLE_SIZE, gap=(705, 761))
    ring('ov-ring-dimension.png', RING_DIM, gap=(800, 855), width=6)
    ring('ov-ring-tree.png', RING_TREE, gap=(418, 528), width=6)
    ring('ov-ring-A1-expr.png', RING_A1_EXPR, gap=(805, 863), width=6)
    ring('ov-ring-A1-vol.png', RING_A1_VOL, BLUE, gap=(1189, 1304), width=6)
    ring('ov-ring-A1-whatever.png', RING_A1_WHATEVER, BLUE, gap=(903, 1010), width=6)
    ring('ov-ring-B1-then.png', RING_B1_THEN, BLUE, gap=(993, 1157), width=6)
    ring('ov-ring-B1-interim.png', RING_B1_INTERIM, BLUE, gap=(1001, 1206), width=6)


def locators():
    locator('ov-loc-params.png', LOC_PARAMS, 'Params')
    locator('ov-loc-c1.png', LOC_C1, 'Constraint1')
    locator('ov-loc-expr.png', EXPR_D, 'Expression Editor')
    locator('ov-loc-measure.png', LOC_MEASURE, 'Measure result')
    locator('ov-loc-type.png', LOC_TYPE, 'Type list', where='below')
    for r in ('A1', 'B1'):
        locator(f'ov-loc-prompt-{r}.png', LOC_PROMPT[r], 'the prompt')


def tools(run):
    names = []
    for ln in open(os.path.join(TAKES, 'runs', run, 'tools.txt'), encoding='utf-8'):
        if ln.startswith('CALL '):
            names.append(json.loads(ln[5:])['name'])
    return names


TOOL_NAMES = {r: tools(r) for r in ('A1', 'B1')}
TOOL_COUNTS = {r: len(n) for r, n in TOOL_NAMES.items()}


def panels():
    fx = Q5
    assert all(fx[w]['open'] and fx[w]['front_solid'] and fx[w]['back_hole_w'] == 5.0 for w in ('2', '3'))
    code_panel('ov-in-F1.png', ['back open, front closed'], PANEL_LL)
    assert Q3['state'] and all(v[1] == 'Valid' for v in Q3['state'].values())
    code_panel('ov-in-F6.png', [f"skin {f2(Q3['skin'])} mm, closed", 'every feature Valid', 'no message'], PANEL_LL)
    assert not Q4['front_solid'] and Q4['peg_solid'] and Q4['solids'] == 1
    code_panel('ov-in-F8.png', [f"front wall: hole {f2(Q4['front_hole_w'])} across", 'peg whole'], PANEL_LL)
    code_panel('ov-in-F9.png', ['back open, front closed', f"hole {f2(fx['3']['back_hole_w'])} across"], PANEL_LL)
    w4, t4, h6 = Q6['reopen_w4'], Q6['typed_w4'], Q6['hole6']
    assert w4['open'] and w4['front_solid'] and not t4['open']
    code_panel('ov-in-F10.png', ['wall 4, Length = wall: open', f"typed 2: 4 − 2 = {g(t4['skin'])} mm, closed"],
               PANEL_LL)
    assert h6['open'] and h6['front_solid']
    code_panel('ov-in-F10b.png', [f"hole {f2(h6['back_hole_w'])} across, open",
                                  f"front closed · outside {g(h6['outside_w'])} × {g(h6['outside_l'])}"], PANEL_LL)
    for r in ('A1', 'B1'):
        assert RUNS[r]['pass'] and sorted(RUNS[r]['at_walls'], key=float) == ['2', '3', '12']
    code_panel('ov-cc-A1.png', ['its file, walls 2, 3, 12:', 'back open, front closed'], CC_PANEL)

    def untested(d, box):
        DRAWN['ov-cc-B1.png:label'] = src_chip(d, (box[0], box[1] - 14 - 172), 'it said, untested:\n'
                                               'Through all cuts the far wall', INK, px=60)
    code_panel('ov-cc-B1.png', ['walls 2, 3, 12: back open,', 'front closed'], CC_PANEL, extra=untested)
    a, bb = TOOL_NAMES['A1'], TOOL_NAMES['B1']
    assert a[0] == 'list_documents' and set(a[1:]) == {'execute_code'}
    code_panel('ov-log-A1.png', [f'{len(a)} tool calls:', 'list_documents, then',
                                 f'execute_code {len(a) - 1} times'], CC_PANEL, title='from the run log')
    assert bb[:2] == ['list_documents', 'get_objects'] and set(bb[2:]) == {'execute_code'}
    code_panel('ov-log-B1.png', [f'{len(bb)} tool calls:', 'list_documents, get_objects,',
                                 f'then execute_code {len(bb) - 2} times'], CC_PANEL, title='from the run log')
    quote('ov-quote-B1a.png', 'B1', ['I set Pocket.Length = Params.wall.'], CC_PANEL)
    quote('ov-quote-B1b.png', 'B1', ["I didn't use Through All, because that", 'would also cut the opposite wall.'],
          CC_PANEL)


RECAP = ['A typed Length stays put', 'Through all goes on to the far wall', 'Length = wall']
TURN = ['Your turn: Pocket 2.5 deep, typed,', 'in a wall 2.5 thick; wall goes to 6', 'Skin? Front wall touched?']
SUB = [['Lesson 17: a mirrored second peg', 'comes out through the back wall'],
       ['Every fix tested in both programs,', 'by hand and with Claude · Subscribe']]
LABEL_LINES = ('it said, untested:', 'Through all cuts the far wall')
F14_LINES = ['run 1, walls 2, 3, 12: open', 'run 2, walls 2, 3, 12: open', 'front closed in both',
             'run 1: wall + 1 · run 2: wall']


# --- F14 stills ---------------------------------------------------------------------------------------------------------
def still_src(run):
    return Image.open(STILL_SRC[run]).convert('RGB')     # the Start Part panel stays: it is the real window (takes too)


def still(run, chip):
    """F14: the run's saved file, inside view (still): the full still + label; then the back wall cropped 1.25x, the
    hole ringed, the panel beside it (never over the part) and the whole still inset with the crop boxed."""
    assert RUNS[run]['depth_stored']['expr'] in ('Params.wall + 1', 'Params.wall')
    CUR.clear()
    im = still_src(run)
    d = ImageDraw.Draw(im)
    src_chip(d, CHIP_TL, 'its file, inside view (still)', INK, px=56, rgba=False)
    src_chip(d, (CHIP_TL[0], CHIP_TL[1] + 110), chip, BLUE, px=52, rgba=False)
    save(im, f'st-{run}.png')
    CUR.clear()
    full = still_src(run)
    z = Image.new('RGB', (SW, SH), WHITE)
    d = ImageDraw.Draw(z)
    x0, y0, x1, y1 = STILL_CROP
    cw, ch = round((x1 - x0) * STILL_K), round((y1 - y0) * STILL_K)
    cx0, cy0 = 50, 300
    z.paste(full.crop(STILL_CROP).resize((cw, ch), Image.LANCZOS), (cx0, cy0))
    d.rectangle((cx0 - 3, cy0 - 3, cx0 + cw + 2, cy0 + ch + 2), outline=PARTLINE, width=3)
    crop_box = (cx0, cy0, cx0 + cw, cy0 + ch)
    hx, hy = cx0 + (HOLE_AT[0] - x0) * STILL_K, cy0 + (HOLE_AT[1] - y0) * STILL_K
    d.ellipse((hx - 120, hy - 100, hx + 120, hy + 100), outline=ORANGE, width=10)
    text(d, (cx0, 190), 'its file, inside view (still)', 56, INK, frame=(SW, SH), safe=False)
    text(d, (cx0, cy0 + ch + 30), 'the back wall from inside: the hole is open', 48, INK, frame=(SW, SH), safe=False)
    px0 = cx0 + cw + 90
    pbox = code_box(d, px0, cy0, F14_LINES, 'checked by code', PX, 0.8)
    pbox = tuple(round(v) for v in pbox)
    for ln in F14_LINES:
        if len(ln) > 32:
            PROBLEMS.append(f'{ln!r}: over 32')
    iw = 960
    ki = iw / SW
    th = full.resize((iw, round(SH * ki)), Image.LANCZOS)
    iy = pbox[3] + 60
    z.paste(th, (px0, iy))
    d.rectangle((px0 - 2, iy - 2, px0 + iw + 2, iy + th.height + 2), outline=PARTLINE, width=3)
    d.rectangle((px0 + round(x0 * ki), iy + round(y0 * ki), px0 + round(x1 * ki), iy + round(y1 * ki)), outline=ORANGE,
                width=5)
    text(d, (px0, iy + th.height + 14), 'whole still', 44, GREY, frame=(SW, SH), safe=False)
    if pbox[2] > SW or iy + th.height + 70 > SH:
        PROBLEMS.append(f'st-{run}z: panel / inset off the frame {pbox}')
    save(z, f'st-{run}z.png')
    DRAWN[f'st-{run}z.png:panel'] = pbox
    DRAWN[f'st-{run}z.png:crop'] = crop_box
    DRAWN[f'st-{run}z.png:k'] = STILL_K


def main():
    os.makedirs(OUT, exist_ok=True)
    b.OUT = OUT
    PROBLEMS.clear()
    LOG.clear()
    CHIP_FILES.clear()
    for s in range(1, 5):
        card_skewer(s)
    for s in range(0, 6):
        card_why(s)
    for s in (1, 2):
        im, dd = canvas()
        header(dd, 'Seen from above, cut through the hole')
        card_why_all(im, dd, s)
    for s in range(1, 4):
        card_why_short(s)
    card_end()
    card_short_head()
    short_cards()
    composites()
    chips()
    rings()
    locators()
    panels()
    for s in (1, 2, 3):
        ov_lines(f'rc-{s}.png', RECAP, s, (20, 1100, 1300, 1690))
    ov_lines('yt-1.png', TURN, 3, (20, 1290, 1300, 1690), one=True)
    for i, lines in enumerate(SUB, 1):
        ov_lines(f'sub-{i}.png', lines, 2, (20, 1470, 1560, 1690), px=54, one=True)
    still('A1', 'run 1, not asked to check')
    still('B1', 'run 2, asked to check')
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
