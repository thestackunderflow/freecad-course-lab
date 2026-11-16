"""FreeCAD course lesson 10 (fully constrained sketches: one slip slid the plate 9.15 down, one Coincident at the origin
pins it) cards and panels, SCRIPT-fc10.md rev 2 section 3. The draw_fc9.py pattern on draw_fx20.py's helpers (the
sticky note and the why card follow draw_sc10.py, the SolidCraft twin): light, 2560 x 1440, clean line art only (the
sticky note is the one analogy), each step adds and earlier steps turn grey, text 44 px+ and 44 columns at most, no
percent sign, everything inside the 5 percent safe area, highlight boxes thin orange outlines, never filled. Every
number is NUMBERS.json's (out/fc10) or a lesson / typed number (tests/test_draw_fc10.py checks it).
  full frame (RGB):  card-note-1..5 (F2), card-why-1..6 (F8), card-yourturn-1..4 (F18, alone), card-end (F19)
  Short (1080 x 1080, RGB; cut 2 taller view): card-short-why-1..2 (S1)
  source overlays (RGBA, 2880 x 1800; burnt into derived takes by mcp-canvas primers/footage-fc10.py):
      ov-floor-T / -TB / -A  the front view (fixed camera per take, NUMBERS takes.*.px): the hook drawn at the 60
                    anchors dashed grey (T, A: where it stood), the floor line z = 0 red
      ov-recap-1..2 F17: the two recap lines, lower left (over the property view), one lit per clause
      ov-cc-top     A1 / B1 while Claude Code's header is on screen (A1 to 17.0 s, B1 to 21.0 s): y 0-230, left pane
      ov-cc-title   after that: the window title row only (y 0-24, left pane)
      ov-cc-save    the input row, from Claude Code's greyed "save the document" suggestion (A1 ~19 s, B1 ~41 s)
      ov-cc-fix-A1 / -B1  cut 2: the "Claude [plan]" box burnt in by lab/fc10redact.sh stays on screen after the header
                    scrolls away and hid reply words; repainted with the words reply.txt has at those columns, used
                    only after the header left (A1 17.0 s, B1 40.5 s: the row is static from there, frame-checked)
      ov-full-*     "checked by code" panels for full-window shots: bottom left over the property view, 56 px on the
                    source (45 px on the 2560 frame); ov-meas-* / ov-msg-* small ones under the Measurement panel /
                    the solver message, read inside the 704 px wide zoom (24 px on the source = 87 px on the frame);
                    ov-cc-A1 / -B1 over the terminal's unquoted lines; ov-short-* for the Short's 1080 x 1080 view (cut 2: 32 px in a 444 px rect, one fact per line)
Run in the draw image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fc10.py [sheet OUTDIR]
Test: tests/test_draw_fc10.py"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw_fx20 as b  # noqa: E402

LAB = b.LAB
OUT = os.path.join(LAB, 'video', 'frames-fc10')
TAKES = os.path.join(LAB, 'out', 'fc10')
b.OUT = OUT
W, H, SW, SH = b.W, b.H, b.SW, b.SH
INK, GREY, WHITE, DONE = b.INK, b.GREY, b.WHITE, b.DONE
BLUE, ORANGE, RED, GREEN = b.BLUE, b.ORANGE, b.RED, b.GREEN
NOTE = (254, 243, 199)
PARTLINE = (71, 85, 105)
GHOST = (110, 120, 138)
canvas, source, header, save = b.canvas, b.source, b.header, b.save
PROBLEMS, LOG, CUR = b.PROBLEMS, b.LOG, b.CUR
SAFE = (round(W * 0.05), round(H * 0.05), round(W * 0.95), round(H * 0.95))
MONO = b.FD + 'DejaVuSansMono.ttf'
CC_TOP = (0, 0, 1160, 230)          # Claude Code's header rows (logo, "Claude Code v...", model, folder)
CC_TITLE = (0, 0, 1160, 24)         # the terminal window's title row
CC_SAVE = (40, 1625, 1110, 80)      # the input row's text (the greyed "save the document" suggestion)
FULL_PX, FULL_K = 56, 0.8           # full window: 2880 + 2 x 160 pad = 3200 -> 2560
SMALL_PX, SMALL_K = 24, 2560 / 704  # the Measurement / message zoom: 704 px wide
SHORT_PX, SHORT_K = 32, 1080 / 444  # cut 2: the Short's close-up rect 444 px wide (was 30 px in 690: too small)
SHORT_MEAS_R = [2286, 580, 444, 444]   # = shorts-footage-fc10.py RECTS['meas'] (the Result values x ~2303-2715)
SHORT_MSG_R = [2190, 600, 484, 484]    # = RECTS['msg'] (the message x 2196-2666)
SHORT_MEAS_XY = (2300, 806)            # under the Result row, left-aligned with its values
SHORT_MSG_XY = (2200, 790)             # under the solver message
FULL_XY = (20, 1700)                # bottom-left anchor of the full-window panels (the property view, left of the hook)
MEAS_XY = (2196, 806)               # top-left: under the Measurement panel's Result row
MSG_XY = (2196, 790)                # top-left: under the solver message
A1_XY, B1_XY = (20, 1250), (20, 1110)   # top-left: over the terminal's unquoted lines (A1 / B1 final replies)
NUM = json.load(open(os.path.join(TAKES, 'NUMBERS.json')))
TK, CL = NUM['takes'], NUM['claude_runs']


def f2(v):
    return f'{0.0 if abs(v) < 0.005 else v:.2f}'


def hole(v):
    s = f2(v)
    return s[:-1] if s.endswith('0') else s           # 15.0, 5.85, 13.68


def text(d, xy, s, size=56, fill=INK, path=b.B, anchor='la', maxw=None, box=None, frame=(W, H), safe=True):
    bb = b.text(d, xy, s, size, fill, path, anchor, maxw, box, frame)
    lim = SAFE if frame == (W, H) else (round(frame[0] * 0.05), round(frame[1] * 0.05), round(frame[0] * 0.95),
                                         round(frame[1] * 0.95))
    if safe and (bb[0] < lim[0] or bb[1] < lim[1] or bb[2] > lim[2] or bb[3] > lim[3]):
        PROBLEMS.append(f'{s!r}: outside the safe area {bb}')
    if '%' in s:
        PROBLEMS.append(f'{s!r}: a percent sign')
    return bb


def dashed(d, a, z, col, width=6, dash=22):
    (x0, y0), (x1, y1) = a, z
    n = max(1, int(math.hypot(x1 - x0, y1 - y0) // (2 * dash)))
    for i in range(n + 1):
        t0, t1 = i / (n + 0.5), min((i + 0.5) / (n + 0.5), 1.0)
        d.line((x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0, x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1), fill=col,
               width=width)


def harrow(d, x0, y0, x1, y1, col, w=7, s=26):
    d.line((x0, y0, x1, y1), fill=col, width=w)
    ux, uy = x1 - x0, y1 - y0
    n = max(1.0, math.hypot(ux, uy))
    ux, uy = ux / n, uy / n
    d.polygon([(x1, y1), (x1 - ux * s - uy * s * 0.6, y1 - uy * s + ux * s * 0.6),
               (x1 - ux * s + uy * s * 0.6, y1 - uy * s - ux * s * 0.6)], fill=col)


def biarrow(d, x0, y0, x1, y1, col, w=7, s=26):
    harrow(d, x0, y0, x1, y1, col, w, s)
    harrow(d, x1, y1, x0, y0, col, w, s)


def pin(d, x, y, col, r=22):
    d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=7)
    d.line((x, y + r, x, y + r + 40), fill=col, width=7)


# --- F2: the sticky note -------------------------------------------------------------------------------------------------
def card_note(step):
    """1 a square note on a whiteboard against a ruler, 2 arrows: 2 ways to move, 3 taller with no pin: top up? bottom
    down? some of each? (dashed), 4 a pin in the bottom corner: only the top grows, 5 pinned: 0 ways to move."""
    im, d = canvas()
    header(d, 'A sticky note on a whiteboard')
    x0, x1, y0, y1 = 1000, 1400, 560, 960
    ry = y1 + 6
    c1 = INK if step == 1 else DONE
    d.rectangle((x0, y0, x1, y1), outline=c1, width=7, fill=NOTE if step == 1 else None)
    d.line((560, ry, 2000, ry), fill=c1, width=8)
    for i in range(16):
        x = 560 + i * 96
        d.line((x, ry, x, ry + (40 if i % 2 == 0 else 24)), fill=c1, width=5)
    text(d, (560, ry + 60), 'ruler: keeps it straight', 52, c1)
    if step >= 2:
        c2 = BLUE if step == 2 else DONE
        biarrow(d, x0 - 300, 760, x0 - 60, 760, c2)
        biarrow(d, x1 + 180, y0 - 40, x1 + 180, y0 + 200, c2)
        text(d, (x1 + 260, 600), '2 ways to move', 64, c2)
    if step >= 3:
        c3 = ORANGE if step == 3 else DONE
        dashed(d, (x0, y0 - 200), (x1, y0 - 200), c3, 7)
        dashed(d, (x0, y1 + 200), (x1, y1 + 200), c3, 7)
        harrow(d, 1200, y0 - 20, 1200, y0 - 180, c3, 6, 22)
        harrow(d, 1200, y1 + 20, 1200, y1 + 180, c3, 6, 22)
        text(d, (200, y0 - 230), 'no pin: top up?', 56, c3)
        text(d, (200, y1 + 170), 'bottom down?', 56, c3)
        text(d, (200, y1 + 250), 'some of each?', 56, c3)
    if step >= 4:
        c4 = GREEN if step == 4 else DONE
        pin(d, x0 + 40, y1 - 70, c4)
        d.line((x0, y1, x1, y1), fill=c4, width=10)
        harrow(d, 1300, y0 - 20, 1300, y0 - 180, c4, 8, 26)
        text(d, (1480, y0 - 230), 'pinned: only the top grows', 56, c4)
    if step >= 5:
        text(d, (1480, 1140), 'pinned: 0 ways to move', 64, INK)
    save(im, f'card-note-{step}.png')


# --- F8: why (the back line, the tries by code, the pin) ----------------------------------------------------------------
A_BOT = -TK['A']['check']['zmin']                                # 1.32
A_UP = TK['A']['check']['zmax'] - NUM['part']['plate_height']   # 18.68
TRIES = NUM['g0']['unpinned_80_tries']
DROPS = []
for _t in TRIES:
    if f"{-_t['zmin']:.2f}" not in DROPS:
        DROPS.append(f"{-_t['zmin']:.2f}")
DROPS = [f'{A_BOT:.2f}'] + sorted((x for x in DROPS if x != f'{A_BOT:.2f}'), key=float)   # 1.32, 6.97, 10.39


def card_why(step):
    """1 the back line 60, both ends open, 2 stretched to 80, 3 + "18.68 up · 1.32 down" (take A), 3-5 the code panel: same
    file, same change, 11 tries, bottom down 1.32 · 6.97 · 10.39 (one value per build), 6 the bottom end pinned at the
    origin: all 20 goes up (the sticky-note pin inset at a third of the frame)."""
    im, d = canvas()
    header(d, 'Why did the bottom move?')
    k = 9.0
    x, base = 620, 1180
    c1 = INK if step == 1 else DONE
    top60, bot60 = base - 60 * k, base
    d.line((x, top60, x, bot60), fill=c1, width=10)
    for yy in (top60, bot60):
        d.ellipse((x - 18, yy - 18, x + 18, yy + 18), outline=c1, width=6, fill=WHITE)
    text(d, (x - 50, (top60 + bot60) / 2), 'back line 60', 52, c1, anchor='rm')
    if step >= 2:
        c2 = BLUE if step == 2 else DONE
        up, dn = A_UP * k, A_BOT * k
        x2 = x + 240
        d.line((x2, top60 - up, x2, bot60 + dn), fill=c2, width=10)
        for yy in (top60 - up, bot60 + dn):
            d.ellipse((x2 - 18, yy - 18, x2 + 18, yy + 18), outline=c2, width=6, fill=WHITE)
        dashed(d, (x - 30, top60), (x2 + 100, top60), c2, 4)
        text(d, (x2, top60 - up - 50), 'now 80', 52, c2, anchor='mb')
    if step >= 3:     # the numbers land with "This time, 1.32 down" (build 3), never a sentence early
        text(d, (x + 290, (top60 + bot60) / 2), f'{A_UP:.2f} up · {A_BOT:.2f} down', 52,
             BLUE if step == 3 else DONE, anchor='lm')
        c3 = INK if step <= 5 else DONE
        bx = (1080, 230, 2320, 560)
        d.rounded_rectangle(bx, radius=16, fill=WHITE, outline=PARTLINE if step <= 5 else DONE, width=4)
        text(d, (bx[0] + 32, bx[1] + 28), 'checked by code', 54, c3)
        text(d, (bx[0] + 32, bx[1] + 110), f'same file, same change, {len(TRIES)} tries:', 52, c3, path=MONO)
        bb = text(d, (bx[0] + 32, bx[1] + 200), 'bottom down ' + DROPS[0], 52, c3, path=MONO)
        for v in DROPS[1:step - 2]:          # each build adds one value (a separate item: earlier ones stay)
            bb = text(d, (bb[2] + 31, bx[1] + 200), '· ' + v, 52, c3, path=MONO)
    if step >= 6:
        x5 = 2390
        d.line((x - 120, base, x5 + 120, base), fill=ORANGE, width=4)
        text(d, (1180, base + 30), 'origin (0, 0)', 52, ORANGE)
        d.line((x5, base - 80 * k, x5, base), fill=GREEN, width=10)
        d.ellipse((x5 - 18, base - 80 * k - 18, x5 + 18, base - 80 * k + 18), outline=GREEN, width=6, fill=WHITE)
        pin(d, x5, base - 40, GREEN)
        harrow(d, x5 + 80, base - 60 * k, x5 + 80, base - 80 * k, GREEN, 7, 22)
        text(d, (x5 - 40, base - 30 * k), 'all 20 goes up', 56, GREEN, anchor='rm')
        nx, ny = 1120, 640                   # the sticky-note pin, inset at a third of the frame
        d.rectangle((nx, ny, nx + 220, ny + 180), outline=GREEN, width=5, fill=NOTE)
        pin(d, nx + 30, ny + 140, GREEN, 14)
        text(d, (nx + 250, ny + 90), 'like the note', 52, GREEN, anchor='lm')
    save(im, f'card-why-{step}.png')


# --- F18 your turn (alone) ----------------------------------------------------------------------------------------------
TURN = ['Your turn, no AI:', 'Rectangle away from the origin, sizes 40, 30', 'How many degrees of freedom?',
        'Pin a corner. 40 → 60: which side moves?']


def card_yourturn(step):
    im, d = canvas()
    text(d, (260, 260), TURN[0], 84, INK if step == 1 else DONE)
    for i, ln in enumerate(TURN[1:step]):
        text(d, (260, 480 + i * 220), ln, 68, BLUE if i == step - 2 else DONE)
    save(im, f'card-yourturn-{step}.png')


# --- F19 the end card ---------------------------------------------------------------------------------------------------
def card_end():
    im, d = canvas()
    text(d, (180, 220), 'FreeCAD + Claude course', 72, INK)
    text(d, (180, 330), 'lesson 10: fully constrained', 60, BLUE)
    shot = Image.open(os.path.join(TAKES, 'B', 'iso.png')).convert('RGB').crop((1000, 200, 2400, 988))
    im.paste(shot.resize((960, 540)), (180, 470))
    d.rectangle((180, 470, 1140, 1010), outline=PARTLINE, width=3)
    text(d, (180, 1030), 'pinned at the origin, then 80 (filmed)', 44, GREY, path=b.R)
    text(d, (180, 1150), 'Lesson 9, lesson 2, the course', 52, INK)
    text(d, (180, 1230), 'Subscribe: every lesson filmed', 48, GREY)
    save(im, 'card-end.png')


# --- the Short's why card (1080 x 960) ----------------------------------------------------------------------------------
def card_short_why(step):
    CUR.clear()
    fr = (1080, 1080)                   # cut 2: the Short's taller view; lines and words stay in ink (sc10 cut 2)
    im = Image.new('RGB', fr, WHITE)
    d = ImageDraw.Draw(im)
    k, x0, base = 7.5, 380, 840
    c1 = INK
    pts = [(x0 + x * k, base - y * k) for x, y in b.HOOK]
    d.line(pts, fill=c1, width=8)
    text(d, (540, 110), 'every line held straight', 56, c1, anchor='mm', frame=fr)
    text(d, (x0 - 30, base - 30 * k), 'held', 48, c1, anchor='rm', frame=fr)
    text(d, (x0 + 25 * k + 30, base - 5 * k), 'held', 48, c1, anchor='lm', frame=fr)
    if step >= 2:
        biarrow(d, x0 - 220, base - 50 * k, x0 - 60, base - 50 * k, BLUE)
        biarrow(d, x0 + 25 * k + 90, base - 58 * k, x0 + 25 * k + 90, base - 38 * k, BLUE)
        d.line((x0 - 260, base + 40, x0 + 25 * k + 200, base + 40), fill=ORANGE, width=6)
        text(d, (540, 975), 'no tie to the origin (0, 0)', 54, ORANGE, anchor='mm', frame=fr)
    save(im, f'card-short-why-{step}.png')


# --- source overlays (2880 x 1800) --------------------------------------------------------------------------------------
def _ov(name, box):
    im, d = source()
    x, y, w, h = box
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=WHITE + (255,))
    save(im, name)


def front_px(take):
    s = TK[take]['px']['front px'].split()
    return {s[i]: (int(s[i + 1]), int(s[i + 2])) for i in range(0, len(s), 3)}


def ov_floor(take, ghost):
    """The floor line z = 0 (red, floor-left to floor-right, thin) and, for an unpinned take, the hook as drawn at 60
    (dashed grey) from the at60 / at0 anchors on the back edge."""
    im, d = source()
    p = front_px(take)
    (x0, y0), (_, y60) = p['at0'], p['at60']
    k = (y0 - y60) / 60.0
    if ghost:
        pts = [(x0 + x * k, y0 - y * k) for x, y in b.HOOK]
        for a, z in zip(pts, pts[1:]):
            dashed(d, a, z, GHOST + (255,), 5, 16)
    d.line((p['floor-left'][0] - 80, y0, p['floor-right'][0] + 80, y0), fill=RED + (255,), width=5)
    save(im, f'ov-floor-{take}.png')


RECAP = ['A size sets length, not which end stays', 'Read the message. Pin, then resize.']
RECAP_BOX = (20, 1300, 1400, 1700)


def ov_recap(step):
    im, d = source()
    d.rounded_rectangle(RECAP_BOX, radius=18, fill=WHITE + (245,), outline=PARTLINE + (255,), width=4)
    f = b.font(b.B, FULL_PX)
    for i, ln in enumerate(RECAP[:step]):
        col = (BLUE if i == step - 1 else DONE) + (255,)
        CUR.append((ln, round(FULL_PX * FULL_K)))
        xy = (RECAP_BOX[0] + 32, RECAP_BOX[1] + 70 + i * 150)
        d.text(xy, ln, font=f, fill=col)
        bb = d.textbbox(xy, ln, font=f)
        if bb[2] > RECAP_BOX[2] or bb[3] > RECAP_BOX[3] or len(ln) > 44:
            PROBLEMS.append(f'{ln!r}: outside its panel {bb}')
    save(im, f'ov-recap-{step}.png')


# --- the "checked by code" panels (one style) ---------------------------------------------------------------------------
def code_box(d, x, y, lines, title, px, k, anchor='lt', chip=None):
    fh, fl = b.font(b.B, px), b.font(MONO, px)
    lh, pad = round(px * 1.3), round(px * 0.55)
    rows = [(title, fh)] + [(t, fl) for t in lines]
    w = max(d.textlength(t, font=f) for t, f in rows) + 2 * pad
    h = lh * len(rows) + pad
    ch = (lh + pad) if chip else 0
    if anchor == 'lb':
        y = y - h - ch
    if x < 0 or y < 0 or x + w > SW or y + h + ch > SH:
        PROBLEMS.append(f'panel off the frame {(x, y, w, h)}')
    d.rounded_rectangle((x, y, x + w, y + h), radius=round(px * 0.3), fill=WHITE + (255,),
                        outline=PARTLINE + (255,), width=max(2, px // 14))
    for i, (t, f) in enumerate(rows):
        d.text((x + pad, y + pad * 0.6 + i * lh), t, font=f, fill=(INK if i else GREY) + (255,))
        CUR.append((t, round(px * k)))
        if '%' in t or len(t) > 44:
            PROBLEMS.append(f'{t!r}: code panel line')
    if chip:
        f = b.font(b.B, px)
        cw = d.textlength(chip, font=f) + 2 * pad
        cy = y + h + pad * 0.6
        d.rounded_rectangle((x, cy, x + cw, cy + lh), radius=round(px * 0.3), fill=(219, 234, 254, 255))
        d.text((x + pad, cy + lh * 0.1), chip, font=f, fill=BLUE + (255,))
        CUR.append((chip, round(px * k)))
    return (x, y, x + w, y + h + ch)


def code_panel(name, lines, xy, px, k, anchor='lt', title='checked by code', chip=None):
    im, d = source()
    code_box(d, xy[0], xy[1], lines, title, px, k, anchor, chip)
    save(im, name)


def bt(c):
    return f"bottom {f2(c['zmin'])} · top {f2(c['zmax'])}"


CHIP = 'by code = a script reads the saved model'


def panels():
    T, TB, A, C, D = (TK[t]['check'] for t in ('T', 'TB', 'A', 'C', 'D'))
    P = TK['P']['live']['start']
    t2 = f"hole {hole(T['hole_to_top'])} from top (was 0 · 60 · {hole(P['hole_to_top'])[:-2]})"
    full = (FULL_XY, FULL_PX, FULL_K, 'lb')
    meas = (MEAS_XY, SMALL_PX, SMALL_K, 'lt')
    code_panel('ov-full-T.png', [bt(T), t2], *full, chip=CHIP)
    code_panel('ov-meas-T.png', [bt(T), t2], *meas, chip=CHIP)
    code_panel('ov-meas-TB.png', [bt(TB), f"hole {hole(TB['hole_to_top'])} from top"], *meas)
    code_panel('ov-full-P.png', [f"hole {hole(P['hole_to_top'])} from top"], *full)
    msg = TK['P']['solver_text'][0]                                  # "['Under-constrained: ', '2 Degrees of Freedom']"
    head, link = (x.strip().strip("'") for x in msg.strip('[]').split("', '"))
    code_panel('ov-msg-P.png', [f'panel text: {head.strip()}', link], MSG_XY, SMALL_PX, SMALL_K)
    a = [bt(A), f"hole {hole(A['hole_to_top'])} from top"]
    code_panel('ov-meas-A.png', a, *meas)
    code_panel('ov-full-A.png', a, *full)
    code_panel('ov-meas-C.png', [bt(C), f"hole {hole(C['hole_to_top'])} from top"], *meas)
    d1 = ['pinned: ' + bt(D), f"hole {hole(D['hole_to_top'])} from top"]
    tries = NUM['controls_refilm']['takeA_80_to_100_tries']
    vals = [f2(t['zmin']) for t in tries]
    once = [v for v in vals if vals.count(v) == 1][0]
    twice = [v for v in vals if vals.count(v) == 2][0]
    code_panel('ov-full-D1.png', d1, *full)
    code_panel('ov-full-D2.png', d1 + [f'unpinned copy at 100, {len(tries)} tries:',
                                       f'bottom {once} once · {twice} twice'], *full)
    for run, xy in (('A1', A1_XY), ('B1', B1_XY)):
        h = CL[run]['score']['hook']
        code_panel(f'ov-cc-{run}.png', [f"{h['dof']} degrees of freedom · bottom {f2(h['zmin'])}",
                                        f"top {f2(h['zmax'])} · hole {hole(h['hole_to_top'])} from top"],
                   xy, FULL_PX, FULL_K, title='checked by code (its file):')
    short = (SHORT_MEAS_XY, SHORT_PX, SHORT_K, 'lt')
    code_panel('ov-short-T.png', [f"bottom {f2(T['zmin'])}", f"hole {hole(T['hole_to_top'])} from top",
                                  f"(was 0 · {hole(P['hole_to_top'])[:-2]})"], *short)
    code_panel('ov-short-P.png', ['panel text:', link], SHORT_MSG_XY, SHORT_PX, SHORT_K)
    code_panel('ov-short-TB.png', [f"bottom {f2(TB['zmin'])}", f"hole {hole(TB['hole_to_top'])} from top"], *short)


# --- cut 2: the redaction box repainted with the reply's own words -------------------------------------------------------
REDACT = (600, 118, 320, 52)            # lab/fc10redact.sh: drawbox x=600 y=118 w=320 h=52 (the header's plan name)
TERM_X0, TERM_COL, TERM_PX, TERM_Y = 3, 25, 41, 120   # xterm DejaVu Sans Mono: column c at x 3 + 25c (fitted on frames)
TERM_INK = {'A1': (83, 88, 84), 'B1': (0, 0, 0)}      # A1's row is a grey tool summary, B1's the reply in ink
RESTORE = {}


def ov_cc_fix(run, key):
    """The reply.txt line holding `key` (it sits on the redaction row once the header is gone), its characters at the
    box's columns drawn on the terminal's white, clipped to the box."""
    line = next(ln for ln in open(os.path.join(TAKES, 'runs', run, 'reply.txt'), encoding='utf-8').read().splitlines()
                if key in ln)
    RESTORE[run] = line
    im, _ = source()
    x, y, w, h = REDACT
    lay = Image.new('RGBA', (w, h), WHITE + (255,))
    dl = ImageDraw.Draw(lay)
    f = b.font(MONO, TERM_PX)
    c0 = (x - TERM_X0) // TERM_COL
    for c in range(c0, c0 + w // TERM_COL + 2):
        if c < len(line):
            dl.text((TERM_X0 + TERM_COL * c - x, TERM_Y - y), line[c], font=f, fill=TERM_INK[run] + (255,))
    im.paste(lay, (x, y))
    save(im, f'ov-cc-fix-{run}.png')


def sheet(outdir):
    names = sorted(n for n in os.listdir(OUT) if n.endswith('.png'))
    tw, th, cols = 640, 400, 4
    rows = -(-len(names) // cols)
    sh = Image.new('RGB', (tw * cols, (th + 30) * rows), (90, 90, 90))
    dd = ImageDraw.Draw(sh)
    for i, n in enumerate(names):
        im = Image.open(os.path.join(OUT, n)).convert('RGBA')
        bg = Image.new('RGBA', im.size, (60, 70, 85, 255))
        t = Image.alpha_composite(bg, im).convert('RGB')
        t.thumbnail((tw - 8, th - 8))
        x, y = (i % cols) * tw, (i // cols) * (th + 30)
        sh.paste(t, (x + 4, y + 4))
        dd.text((x + 6, y + th), n, font=b.font(b.R, 22), fill=(255, 255, 255))
    sh.save(os.path.join(outdir, 'cards-sheet-fc10.jpg'), quality=85)


def main():
    os.makedirs(OUT, exist_ok=True)
    PROBLEMS.clear()
    LOG.clear()
    for s in range(1, 6):
        card_note(s)
    for s in range(1, 7):
        card_why(s)
    for s in range(1, 5):
        card_yourturn(s)
    for s in (1, 2):
        card_short_why(s)
        ov_recap(s)
    card_end()
    _ov('ov-cc-top.png', CC_TOP)
    _ov('ov-cc-title.png', CC_TITLE)
    _ov('ov-cc-save.png', CC_SAVE)
    ov_cc_fix('A1', 'Searched for 1 pattern')
    ov_cc_fix('B1', 'nothing pinned it there')
    ov_floor('T', True)
    ov_floor('TB', False)
    ov_floor('A', True)
    panels()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
