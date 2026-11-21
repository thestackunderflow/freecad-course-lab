"""FreeCAD course lesson 14 (the Thickness's place in the Body: a key peg joined before Thickness comes out 14 wide
and hollow, open into the cup; the fix puts Thickness before the peg with Set Tip) cards and panels, SCRIPT-fc14.md
rev 2.1 section 3. The draw_fc13.py pattern on draw_fx20.py / draw_fc10.py helpers: light, 2560 x 1440, each step adds
and earlier steps turn grey, card lines 44 columns, chips / insets / code-panel lines 32, no percent sign, never
"tooltip" or "shell" (FreeCAD's feature is Thickness). Every number is NUMBERS.json's (out/fc14) or a lesson / typed
number (tests/test_draw_fc14.py). FreeCAD's outward corners are rounded by the Arc join (G0): the drawings round them,
never giving a radius.
  full frame:  card-balloon-1..4 (F2), card-why-1..5 (F6), card-fixed-1..3 (F7a), still-mfa-1..2 (F7a: the G0 still
               q3b-after-recompute.png, the tree, then the first Report row; still-mfa = the last framing),
               still-after-A1 / -B1 (F12: runs/*/after.png + the panel beside), card-end (F14)
  Short:       card-why-s1..3 (S1, 1080 x 1080), card-short-head (1080 x 1920: the frame-1 headline words)
  source overlays (RGBA 2880 x 1800, burnt in by mcp-canvas primers/footage-fc14.py):
      tip-flag / tip-flag-pad   F7a / F7b: the Tip as a small flag beside the tree's last row (y 504) / Pad (y 439)
      ov-sides-M     F1: the trap peg's two 2 mm walls drawn thin orange on M's top view
      ov-open-T      F0 / F1 / F5 / S0: the square opening ringed in T's angled view (52.5 on)
      ov-wall-F      F7b: the closed front wall ringed in F's angled view (102.1 on)
      ov-in-*        "read from the file" / "checked by code" panels (63 px)
      ov-cc-A1 / -B1 the panel on Claude's files (under FreeCAD's 3D view); ov-quote-B1 its Peg bullets re-set
      card-recap-1..3, card-yourturn-1..3  F13 lower-left panels (no answer)
Geometry (gridded frames + OCR, 21 Nov, session scratchpad fc14r): tree rows (centre y) Params 343, Cup 373, Origin
406, row 4 439, row 5 471, row 6 504, labels from x 145 (Thickness to x 251); M top view: the peg's sides x 1583 /
1780, y 1190-1400 (14.07 px/mm); T 52.5+ into the cup: the opening x 1631-1804, y 1211-1329; G0 still: the first
Report row y 1205-1232 (header y 1182), the second (lab plumbing) from y 1238.
Run in the draw image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fc14.py
Test: tests/test_draw_fc14.py"""
import json
import os
import sys
import textwrap

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw_fx20 as b  # noqa: E402
import draw_fc10 as f10  # noqa: E402

LAB = b.LAB
OUT = os.path.join(LAB, 'video', 'frames-fc14')
TAKES = os.path.join(LAB, 'out', 'fc14')
W, H, SW, SH = b.W, b.H, b.SW, b.SH
INK, GREY, WHITE, DONE = b.INK, b.GREY, b.WHITE, b.DONE
BLUE, ORANGE, RED, GREEN = b.BLUE, b.ORANGE, b.RED, b.GREEN
ORANGEFILL, BLUEFILL, DONEFILL = b.ORANGEFILL, b.BLUEFILL, b.DONEFILL
PARTLINE = f10.PARTLINE
CLAY, BALLOON = (161, 98, 7), (254, 202, 202)
canvas, source, header = b.canvas, b.source, b.header
PROBLEMS, LOG, CUR = b.PROBLEMS, b.LOG, b.CUR
text, code_box = f10.text, f10.code_box
NUM = json.load(open(os.path.join(TAKES, 'NUMBERS.json'), encoding='utf-8'))
BUILD, RUNS = NUM['build'], NUM['runs']
NOSHELL, TRAP, TRAP3, FIXED = BUILD['noshell'], BUILD['trap'], BUILD['trap_wall3'], BUILD['fixed']
FIXED3, FIXED12, YT = BUILD['fixed_wall3'], BUILD['fixed_peg12'], BUILD['yt_before']
PANEL_NAMES = []
PX = 63
ROW_Y = {'Pad': 439, 'row5': 471, 'last': 504}
FLAG_X = 300
SIDES_M = (1583, 1780, 1190, 1400)
OPEN_T = (1600, 1180, 1840, 1360)
WALL_F = (1540, 1140, 1900, 1400)
MFA = os.path.join(TAKES, 'G0', 'q3b-after-recompute.png')
MFA_TREE = (0, 290, 470, 520)          # Model tree: peg, Params, Cup, Origin, Pad, Thickness (red mark), Pad001
MFA_REPORT = (800, 1174, 1480, 1235)   # Report header + "Thickness: Invalid face reference (2 times)" only
MFA_THICK = (0, 455, 470, 488)         # the Thickness row inside the tree crop
CC_XY = (1175, 1360)


def n0(v):
    return f'{v:g}'


def save(im, name):
    b.OUT = OUT
    b.save(im, name)


def lit(i, step, on=ORANGE):
    return on if i == step else DONE


def chip_on(d, xy, s, col=ORANGE, px=52, frame=(W, H)):
    """A chip on a card: rounded light box, coloured words (logged)."""
    f = b.font(b.B, px)
    w = d.textlength(s, font=f)
    x, y = xy
    d.rounded_rectangle((x, y, x + w + 40, y + px + 30), radius=14, fill=WHITE, outline=col, width=4)
    text(d, (x + 20, y + 12), s, px, col, frame=frame)


# --- F2: papier-mâché over a balloon ------------------------------------------------------------------------------------
def balloon(d, cx, cy, r, lump, paper, inside, open_top, wl=34, col=ORANGE):
    """A balloon (circle) with a clay lump (rect) on its right; paper `wl` thick round what `paper` covers."""
    lx0, ly0, lx1, ly1 = lump
    if paper:
        d.ellipse((cx - r - wl, cy - r - wl, cx + r + wl, cy + r + wl), fill=ORANGEFILL, outline=col, width=5)
        if paper == 'both':
            d.rounded_rectangle((lx0, ly0 - wl, lx1 + wl, ly1 + wl), radius=wl, fill=ORANGEFILL, outline=col, width=5)
    fill_b = WHITE if inside == 'air' else BALLOON
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill_b, outline=INK if inside != 'air' else col, width=5)
    if paper == 'both':
        d.rectangle((lx0 - 4, ly0, lx1, ly1), fill=WHITE if inside == 'air' else CLAY)
    else:
        d.rectangle((lx0, ly0, lx1, ly1), fill=CLAY, outline=INK, width=4)
    if open_top:
        d.rectangle((cx - 90, cy - r - wl - 6, cx + 90, cy - r + 6), fill=WHITE)


def card_balloon(step):
    """F2 (the one illustrated analogy beat): 1 balloon + clay; 2 paper over both; 3 popped and scooped through the
    top: the clay's space empties too, open into the ball; 4 second panel: paper on the balloon alone, scooped, clay
    glued on after: solid; the key in two lines."""
    im, d = canvas()
    header(d, 'Papier-mâché over a balloon')
    cx, cy, r = 640, 700, 260
    lump = (cx + r - 30, cy - 70, cx + r + 170, cy + 70)
    paper = 'both' if step >= 2 else None
    balloon(d, cx, cy, r, lump, paper, 'air' if step >= 3 else 'full', step >= 3,
            col=ORANGE if step in (2, 3) else DONE)
    if step == 1:
        chip_on(d, (240, 1080), 'a balloon with a lump of clay stuck on', INK)
    if step >= 2:
        chip_on(d, (240, 1080), 'paper over balloon and clay', lit(2, step))
    if step >= 3:
        chip_on(d, (240, 1190), "the clay's space comes out too", lit(3, step, RED))
    if step >= 4:
        cx2 = 1780
        lump2 = (cx2 + r + 34, cy - 70, cx2 + r + 234, cy + 70)
        balloon(d, cx2, cy, r, lump2, 'ball', 'air', True)
        chip_on(d, (1400, 1080), 'clay after: stays solid', GREEN)
        text(d, (1340, 1210), 'balloon = the shape you drew', 52, INK)
        text(d, (1340, 1285), 'paper = the walls Thickness grows', 52, ORANGE)
    save(im, f'card-balloon-{step}.png')


# --- F6 / S1: why the peg opens into the cup ----------------------------------------------------------------------------
def outline(x0, y0, k, peg_w=10, peg_l=15):
    """Box 60 x 40 seen from above with the peg (centred on the front side, pointing down), as one polygon."""
    x1, y1 = x0 + 60 * k, y0 + 40 * k
    px0, px1 = x0 + (60 - peg_w) / 2 * k, x0 + (60 + peg_w) / 2 * k
    return [(x0, y0), (x1, y0), (x1, y1), (px1, y1), (px1, y1 + peg_l * k), (px0, y1 + peg_l * k), (px0, y1),
            (x0, y1)], (x0, y0, x1, y1), (px0, y1, px1, y1 + peg_l * k)


def walls(d, box, peg, wl, col, fill):
    """Walls grown outward round box and peg (outside corners rounded, no radius given)."""
    x0, y0, x1, y1 = box
    p0, _, p1, pe = peg
    d.rounded_rectangle((x0 - wl, y0 - wl, x1 + wl, y1 + wl), radius=wl, fill=fill, outline=col, width=4)
    d.rounded_rectangle((p0 - wl, y1 - wl, p1 + wl, pe + wl), radius=wl, fill=fill, outline=col, width=4)


def why(d, step, x0, y0, k, frame, px=56):
    poly, box, peg = outline(x0, y0, k)
    wl = 2 * k
    if step >= 2:
        c = ORANGE if step in (2, 3) else DONE
        walls(d, box, peg, wl, c, ORANGEFILL if step in (2, 3) else DONEFILL)
    d.polygon(poly, fill=(226, 232, 240) if step >= 4 else WHITE)
    d.line(poly + [poly[0]], fill=INK if step == 1 else DONE, width=7)
    return poly, box, peg, wl


def card_why(step):
    """F6: 1 box and peg as one outline (no line where they meet); 2 the walls grown outside the whole outline;
    3 10 + 2 + 2 = 14 lit; 4 the drawn shape greys as the inside, the grey running from the cup into the peg;
    5 the arrow 'never a wall here' at the joint."""
    im, d = canvas()
    header(d, 'Why the peg opens into the cup')
    k = 11
    poly, box, peg, wl = why(d, step, 260, 260, k, (W, H))
    p0, y1, p1, pe = peg
    chip_on(d, (1280, 300), 'joined: one solid', lit(1, step, BLUE))
    if step >= 2:
        chip_on(d, (1280, 420), 'walls grown outside the whole outline', lit(2, step))
    if step >= 3:
        text(d, ((p0 + p1) / 2, pe + wl + 30), '10 + 2 + 2 = 14', 72, lit(3, step), anchor='ma')
    if step >= 4:
        chip_on(d, (1280, 540), 'the drawn shape = the inside', lit(4, step, BLUE))
        text(d, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), 'inside', 64, BLUE if step == 4 else DONE,
             anchor='mm')
        text(d, (p0 - wl - 30, pe - 20), 'inside too', 52, BLUE if step == 4 else DONE, anchor='rm')
    if step >= 5:
        f10.harrow(d, 1260, 1000, p1 + 20, y1 + 6, RED, w=8)
        chip_on(d, (1280, 1000), 'never a wall here', RED)
    save(im, f'card-why-{step}.png')


def card_why_s(step):
    """S1, 1080 x 1080: the F6 drawing, three builds (1 one outline; 2 walls + the sum; 3 the inside, the arrow)."""
    CUR.clear()
    fr = (1080, 1080)
    im = Image.new('RGB', fr, WHITE)
    d = ImageDraw.Draw(im)
    st = {1: 1, 2: 3, 3: 5}[step]
    k = 9
    poly, box, peg, wl = why(d, min(st, 4), 270, 80, k, fr)
    p0, y1, p1, pe = peg
    chip_on(d, (120, 760), 'joined: one solid', lit(1, step, BLUE), px=48, frame=fr)
    if step >= 2:
        text(d, (p1 + wl + 20, (y1 + pe) / 2 - 20), '10 + 2 + 2 = 14', 44, lit(2, step), anchor='lm', frame=fr)
        chip_on(d, (120, 850), 'walls outside the outline', lit(2, step), px=48, frame=fr)
    if step >= 3:
        f10.harrow(d, 700, pe + wl + 10, p1 + 6, y1 + 6, RED, w=7)
        text(d, (540, pe + wl + 14), 'never a wall here', 44, RED, anchor='ma', frame=fr)
    save(im, f'card-why-s{step}.png')


# --- F7a: Thickness first ----------------------------------------------------------------------------------------------
def card_fixed(step):
    """F7a: 1 the box alone; 2 its walls (Thickness, outward); 3 the peg added onto the finished wall: 10, solid."""
    im, d = canvas()
    header(d, 'The fix: Thickness first, then the peg')
    k = 11
    poly, box, peg = outline(560, 260, k)
    wl = 2 * k
    x0, y0, x1, y1 = box
    if step >= 2:
        d.rounded_rectangle((x0 - wl, y0 - wl, x1 + wl, y1 + wl), radius=wl, fill=ORANGEFILL if step == 2 else DONEFILL,
                            outline=ORANGE if step == 2 else DONE, width=4)
    d.rectangle(box, fill=WHITE, outline=INK if step == 1 else DONE, width=7)
    chip_on(d, (1500, 300), '1 the box alone', lit(1, step, BLUE))
    if step >= 2:
        chip_on(d, (1500, 420), '2 Thickness: its walls', lit(2, step))
    if step >= 3:
        p0, _, p1, pe = peg
        d.rectangle((p0, y1, p1, pe), fill=CLAY, outline=INK, width=5)
        chip_on(d, (1500, 540), '3 the peg on the finished wall', GREEN)
        chip_on(d, (p1 + 40, pe - 90), '10, solid', GREEN)
    save(im, f'card-fixed-{step}.png')


def still_mfa():
    """F7a: the G0 still (Move Feature After), two framings: 1 the tree (Thickness's red mark ringed); 2 the tree
    smaller + the first Report row only. Never the rows below it (the lab's own plumbing errors)."""
    g0 = Image.open(MFA).convert('RGB')
    tree, rep = g0.crop(MFA_TREE), g0.crop(MFA_REPORT)
    for step in (1, 2):
        im, d = canvas()
        header(d, 'Move Feature After, in my test')
        k = 2.6 if step == 1 else 1.7
        t = tree.resize((round(tree.width * k), round(tree.height * k)), Image.LANCZOS)
        x, y = (W - t.width) // 2 if step == 1 else 200, 220
        im.paste(t, (x, y))
        d.rectangle((x - 3, y - 3, x + t.width + 2, y + t.height + 2), outline=PARTLINE, width=3)
        ty0, ty1 = (MFA_THICK[1] - MFA_TREE[1]) * k + y, (MFA_THICK[3] - MFA_TREE[1]) * k + y
        d.rounded_rectangle((x - 10, ty0 - 8, x + t.width + 10, ty1 + 8), radius=12, outline=RED if step == 1 else DONE,
                            width=6)
        if step == 2:
            k2 = 3.0
            r = rep.resize((round(rep.width * k2), round(rep.height * k2)), Image.LANCZOS)
            rx, ry = (W - r.width) // 2, 1000
            im.paste(r, (rx, ry))
            d.rounded_rectangle((rx - 10, ry - 10, rx + r.width + 10, ry + r.height + 10), radius=12, outline=RED,
                                width=6)
            text(d, (rx, ry - 80), 'Report: "Thickness: Invalid face reference"', 52, RED)
        text(d, (160, 1290), 'lab still, FreeCAD 1.1.4', 44, GREY, path=b.R)
        save(im, f'still-mfa-{step}.png')
        if step == 2:
            save(im, 'still-mfa.png')


def still_after(run, chip):
    """F12: the run's file after the run (still), the panel beside it (never over it)."""
    im, d = canvas()
    shot = Image.open(os.path.join(TAKES, 'runs', run, 'after.png')).convert('RGB')
    shot = shot.crop((1160, 0, SW, SH)) if shot.width == SW else shot
    k = 1460 / shot.width
    s = shot.resize((1460, round(shot.height * k)), Image.LANCZOS)
    im.paste(s, (140, 220))
    d.rectangle((137, 217, 140 + s.width + 2, 220 + s.height + 2), outline=PARTLINE, width=3)
    text(d, (140, 130), 'its file after the run (still)', 56, INK)
    chip_on(d, (1650, 220), chip, BLUE, px=48)
    w3 = RUNS[run]['score']['at_wall3']
    lines = ['both at wall 3:', f"peg {n0(w3['peg_w'])} × {n0(w3['peg_h'])}, solid,", 'wall closed']
    code_box(d, 1650, 420, lines, 'checked by code', 56, 0.8)
    for ln in lines:
        if len(ln) > 32:
            PROBLEMS.append(f'{ln!r}: over 32')
    save(im, f'still-after-{run}.png')


def card_end():
    im, d = canvas()
    text(d, (180, 220), 'FreeCAD + Claude course', 72, INK)
    text(d, (180, 330), 'lesson 14: Thickness first', 60, BLUE)
    shot = Image.open(os.path.join(TAKES, 'F', 'fix-iso.png')).convert('RGB').crop((1000, 250, 2400, 1650))
    im.paste(shot.resize((600, 600)), (180, 450))
    d.rectangle((180, 450, 780, 1050), outline=PARTLINE, width=3)
    text(d, (180, 1080), 'the fixed cup (filmed)', 44, GREY, path=b.R)
    text(d, (180, 1180), 'Lesson 13 · Lesson 1 · the course', 52, INK)
    save(im, 'card-end.png')


def card_short_head():
    """The Short's frame-1 headline (1080 x 1920, RGBA): the problem in words from 0.0 s, through the 1 s hold."""
    CUR.clear()
    fr = (1080, 1920)
    im = Image.new('RGBA', fr, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, s in enumerate(('PEG CAME OUT HOLLOW:', '14, NOT 10')):
        f = b.font(b.B, 64)
        w = d.textlength(s, font=f)
        y = 60 + i * 86
        d.rectangle(((1080 - w) / 2 - 18, y - 8, (1080 + w) / 2 + 18, y + 76), fill=ORANGE + (242,))
        d.text(((1080 - w) / 2, y), s, font=f, fill=WHITE + (255,))
        CUR.append((s, 64))
    save(im, 'card-short-head.png')


# --- source overlays ----------------------------------------------------------------------------------------------------
def flag(name, y):
    """The Tip drawn as a small flag beside a tree row (outline + word, never over the row's label)."""
    im, d = source()
    x = FLAG_X
    d.line((x, y - 24, x, y + 22), fill=ORANGE + (255,), width=6)
    d.polygon([(x + 3, y - 24), (x + 64, y - 12), (x + 3, y)], fill=ORANGE + (255,))
    d.text((x + 76, y - 22), 'Tip', font=b.font(b.B, 36), fill=ORANGE + (255,))
    CUR.append(('Tip', 36))
    save(im, name)


def ov_sides():
    """F1: the trap peg's 2 mm walls (top view), thin orange strips inside its two side edges."""
    im, d = source()
    xa, xb, ya, yb = SIDES_M
    w = round((xb - xa) / TRAP['peg_w'] * 2)
    for box in ((xa, ya, xa + w, yb), (xb - w, ya, xb, yb)):
        d.rectangle(box, fill=ORANGE + (200,))
    save(im, 'ov-sides-M.png')


def ring(name, box, col=ORANGE):
    im, d = source()
    d.rounded_rectangle(box, radius=30, outline=col + (255,), width=8)
    save(im, name)


def ov_lines(name, lines, step, box, px=56, k=0.8):
    im, d = source()
    d.rounded_rectangle(box, radius=18, fill=WHITE + (245,), outline=PARTLINE + (255,), width=4)
    f = b.font(b.B, px)
    y = box[1] + 36
    for i, ln in enumerate(lines[:step]):
        col = (BLUE if i == step - 1 else DONE) + (255,)
        for part in ln.split('\n'):
            CUR.append((part, round(px * k)))
            d.text((box[0] + 32, y), part, font=f, fill=col)
            bb = d.textbbox((box[0] + 32, y), part, font=f)
            if bb[2] > box[2] or bb[3] > box[3]:
                PROBLEMS.append(f'{part!r}: outside its panel {bb}')
            y += round(px * 1.35)
        y += round(px * 0.4)
    save(im, f'{name}-{step}.png')


def code_panel(name, lines, xy, px=PX, k=0.8, title='checked by code', white=()):
    im, d = source()
    for box in white:
        d.rectangle(box, fill=(255, 255, 255, 255))
    code_box(d, xy[0], xy[1], lines, title, px, k)
    for t in lines:
        if len(t) > 32:
            PROBLEMS.append(f'{t!r}: code panel line over 32')
    save(im, name)
    PANEL_NAMES.append(name)


def quote(name, run, lines, y=260, px=52, white=()):
    reply = ' '.join(open(os.path.join(TAKES, 'runs', run, 'reply.txt'), encoding='utf-8').read().split())
    assert ' '.join(lines) in reply, lines
    im, d = source()
    for box in white:
        d.rectangle(box, fill=(255, 255, 255, 255))
    code_box(d, 20, y, list(lines), 'its reply (words as written):', px, 0.8)
    save(im, name)
    PANEL_NAMES.append(name)


RECAP = ['Thickness wraps what comes\nbefore it in the tree', 'Joined first: wrapped, emptied,\nopen into the part',
         'Thickness first, then the peg']
TURN = [f"Your turn: a peg drawn {n0(YT['peg_param'])} wide",
        f"joined, then Thickness, walls {n0(YT['wall_param'])} outward", 'How wide? Middle plastic or air?']


def peg(v, mid):
    return f"peg {n0(v['peg_w'])} × {n0(v['peg_h'])}, {mid}"


def panels():
    air = 'middle air' if not TRAP['peg_mid_solid'] else 'middle plastic'
    plastic = 'middle plastic' if FIXED['peg_mid_solid'] else 'middle air'
    code_panel('ov-in-T0.png', [peg(TRAP, air)], (1900, 1470), title='read from the file')      # F0 (T, right pane)
    code_panel('ov-in-F1.png', [peg(FIXED, plastic)], (1784, 1470), title='read from the file')  # F1 (F, right pane)
    code_panel('ov-in-M5.png', [peg(TRAP, air), f"opening {n0(TRAP['opening_w'])} × {n0(TRAP['opening_h'])} into "
                                'the cup'], (1740, 1430))                                        # F5 (M / T)
    code_panel('ov-in-F7.png', [peg(FIXED, plastic), 'wall closed, top open',
                                f"inside {n0(FIXED['inside_w'])} × {n0(FIXED['inside_l'])}, "
                                f"{n0(FIXED['inside_d'])} deep"], (1784, 1340))                    # F7b (F)
    code_panel('ov-in-P8a.png', ['Thickness first, wall 3:', peg(FIXED3, 'solid')], (1880, 1360))
    code_panel('ov-in-P8b.png', ['trap file, wall 3:',
                                 f"10 + 3 + 3 = {n0(TRAP3['peg_w'])}, hollow"], (1880, 1360))
    code_panel('ov-in-P8c.png', [peg(FIXED12, 'solid')], (1880, 1360))
    code_panel('ov-in-S0.png', [peg(TRAP, air)], (1180, 1420))       # the Short (T's angled view, its square crop)
    code_panel('ov-in-S2.png', [peg(FIXED, 'solid')], (1180, 1420))   # the Short (F top view)
    for run in ('A1', 'B1'):
        w2 = RUNS[run]['score']['at_wall2']
        ok = w2['peg_mid_solid'] and w2['front_wall_solid']
        code_panel(f'ov-cc-{run}.png', [f"its file: {peg(w2, 'solid' if ok else 'hollow')}",
                                        'wall closed' if w2['front_wall_solid'] else 'wall open'], CC_XY)
    quote('ov-quote-B1.png', 'B1', ['- The peg is a single solid, 10 × 10 (area', '100 mm²), spanning x −5…5 and z',
                                    '35…45.', '- It is fused to the front wall with no gap', 'or cavity.'], y=440)


def main():
    os.makedirs(OUT, exist_ok=True)
    b.OUT = OUT
    PROBLEMS.clear()
    LOG.clear()
    PANEL_NAMES.clear()
    for s in range(1, 5):
        card_balloon(s)
    for s in range(1, 6):
        card_why(s)
    for s in (1, 2, 3):
        card_why_s(s)
        card_fixed(s)
    still_mfa()
    still_after('A1', 'not asked to check · $0.18')
    still_after('B1', 'asked to check · $0.13')
    card_end()
    card_short_head()
    flag('tip-flag.png', ROW_Y['last'])
    flag('tip-flag-pad.png', ROW_Y['Pad'])
    ov_sides()
    ring('ov-open-T.png', OPEN_T)
    ring('ov-wall-F.png', WALL_F, GREEN)
    for s in (1, 2, 3):
        ov_lines('card-recap', RECAP, s, (20, 1120, 1300, 1720))
        ov_lines('card-yourturn', TURN, s, (20, 1200, 1500, 1720), px=54)
    panels()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
