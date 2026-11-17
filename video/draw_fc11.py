"""FreeCAD course lesson 11 (reference constraints: a typed 55 left the plate at 60 and the screw hole cut nothing; a
reference size plus the back line tied to Params fixes it) cards and panels, SCRIPT-fc11.md rev 2.1 section 3. The
draw_fc10.py pattern on draw_fx20.py's helpers: light, 2560 x 1440, clean line art (the class list is the one
analogy), each step adds and earlier steps turn grey, card lines 44 columns, code-panel lines 32 columns, no percent
sign, never the word "blue" (FreeCAD 1.1.4 draws a reference size grey, in brackets), highlight rings thin, never
filled. Every number is NUMBERS.json's (out/fc11) or a lesson / typed number (tests/test_draw_fc11.py).
  full frame:  card-list-1..4 (F2), card-why-1..5 (F7), card-end (F17); Short 1080 x 1080: card-short-why-1..3 (S1)
  stills (2880 x 1800): still-other-red / -inv / -80 (F8b, cut 2): G0b's real FreeCAD screenshots s7-after-ok (the
               "Redundant constraints: (24)" panel, both sizes kept), s9-closed-60 (the "!" on HookSketch), s9-at-80,
               cut above y STILL_CUT (the Report band reads "Over-constrained sketch" on s9-at-80), with a
               checked-by-code panel in the white band below where the screen does not spell it out
  source overlays (RGBA 2880 x 1800, burnt in by mcp-canvas primers/footage-fc11.py):
      ov-ring-60 / -80  take H's right view: a solid ring on the screw hole / a dashed ring where it was
      ov-recap-1..4     F15 lines, lower left;  ov-turn-1..5  F16 your-turn panel (no answer)
      ov-cc-top / ov-cc-auto  Claude Code header + notice (y 0-720) / the auto-mode row (masks)
      ov-cc-quote-B1    run 2's two quoted reply lines (they scroll off the screen before the recording ends)
      PANEL_NAMES       "checked by code" panels: full (56 px bottom left), meas / msg (24 px under the Measurement
                        panel / the solver message, read in the 704 px zoom), sk (40 px top left of the sketch view,
                        read in the 1900 px zoom), cc (52 px over the terminal), short (32 px in the Short's 444 px rect)
Run in the draw image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fc11.py
Test: tests/test_draw_fc11.py"""
import json
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw_fx20 as b  # noqa: E402
import draw_fc10 as f10  # noqa: E402  (text / dashed / harrow / code_box helpers)

LAB = b.LAB
OUT = os.path.join(LAB, 'video', 'frames-fc11')
TAKES = os.path.join(LAB, 'out', 'fc11')
W, H, SW, SH = b.W, b.H, b.SW, b.SH
INK, GREY, WHITE, DONE = b.INK, b.GREY, b.WHITE, b.DONE
BLUE, ORANGE, RED, GREEN = b.BLUE, b.ORANGE, b.RED, b.GREEN
PARTLINE = f10.PARTLINE
canvas, source, header = b.canvas, b.source, b.header
PROBLEMS, LOG, CUR = b.PROBLEMS, b.LOG, b.CUR
text, dashed, harrow, code_box = f10.text, f10.dashed, f10.harrow, f10.code_box
MONO = f10.MONO
NUM = json.load(open(os.path.join(TAKES, 'NUMBERS.json')))
TK, CL = NUM['takes'], NUM['claude_runs']
STILL_CUT = 1370                   # G0b stills kept above this row (the Report view starts ~1380)
CHIP = 'by code = a script reads the saved model'
# cut 2: 'sk' lower left (the top label covered it), 'cc' in FreeCAD's empty pane (off Claude Code's reply)
KIND = {'full': ((20, 1700), 56, 0.8, 'lb'), 'meas': ((2196, 806), 24, 2560 / 704, 'lt'),
        'msg': ((2196, 790), 24, 2560 / 704, 'lt'), 'sk': ((640, 1420), 40, 2560 / 1900, 'lb'),
        'cc': ((1175, 1060), 42, 0.8, 'lt'), 'short': ((2300, 806), 32, 1080 / 444, 'lt')}
PANEL_NAMES = []


def save(im, name):
    b.OUT = OUT
    b.save(im, name)


def f2(v):
    return f'{v:.2f}'


def n0(v):
    return f'{v:g}'


def find_hole():
    """Centre and radius of the screw hole in take H's right view at 60 (the light pixels inside the green plate)."""
    im = Image.open(os.path.join(TAKES, 'H', 'hole-60.png')).convert('RGB')
    xs, ys = [], []
    for y in range(420, 1100, 2):
        for x in range(1530, 1860, 2):
            r, g, bb = im.getpixel((x, y))
            if r > 200 and g > 200 and bb > 200:
                xs.append(x)
                ys.append(y)
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    return (x0 + x1) // 2, (y0 + y1) // 2, max(x1 - x0, y1 - y0) // 2 + 1


HOLE = find_hole()


# --- F2: the class list ------------------------------------------------------------------------------------------------
def card_list(step):
    im, d = canvas()
    header(d, 'A class list with a total')
    c1 = INK if step == 1 else DONE
    d.rectangle((300, 260, 1000, 380), outline=c1, width=6)
    text(d, (340, 290), 'Total: 30', 64, c1)
    text(d, (1040, 300), 'typed by hand', 52, c1)
    for i in range(8):
        y = 450 + i * 80
        text(d, (300, y), f'{i + 1}.', 44, c1, path=b.R)
        d.line((400, y + 30, 400 + 260 + (i * 53) % 200, y + 30), fill=c1, width=6)
    text(d, (300, 1100), '... 30 names', 52, c1)
    if step >= 2:
        c2 = BLUE if step == 2 else DONE
        text(d, (300, 1190), '31. a new name added', 52, c2)
        text(d, (1040, 400), 'still says 30: which is right?', 56, ORANGE if step == 2 else DONE)
    if step >= 3:
        c3 = GREEN if step == 3 else DONE
        d.rectangle((1500, 560, 2300, 680), outline=c3, width=6)
        text(d, (1540, 590), '= count(names) = 31', 60, c3, path=MONO)
        text(d, (1500, 700), 'counted by the sheet', 52, c3)
    if step >= 4:
        text(d, (1500, 900), 'typed: never follows', 60, ORANGE)
        text(d, (1500, 1010), 'counted: always agrees', 60, GREEN)
    save(im, f'card-list-{step}.png')


# --- F7: why (two parts, one name) -------------------------------------------------------------------------------------
U_SHEET = TK['T']['end_check']['sheet']['plate_height']                   # 80
HOLE_Z = TK['T']['end_check']['sketch_hole_z']                            # 65
TOP = TK['T']['end_check']['zmax']                                        # 60
BELOW = U_SHEET - HOLE_Z                                                  # 15
THICK = TK['T']['end_check']['sheet']['thickness']                        # 5
INNER = TK['T']['end_check']['inner']['value']                            # 55


def outline(d, x0, base, k, col, top, hole_z=None):
    pts = [(x0 + x * k, base - (y if y < 60 else top) * k) for x, y in b.HOOK]
    d.line(pts, fill=col, width=8)
    if hole_z is not None:
        r = 26
        cx, cy = x0 + 2.5 * k, base - hole_z * k
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ORANGE, width=7)
        return cx, cy


def card_why(step):
    im, d = canvas()
    header(d, 'Why? Two parts, one name')
    c1 = INK if step == 1 else DONE
    d.rounded_rectangle((820, 196, 1740, 304), radius=14, outline=c1, width=5)
    text(d, (1280, 250), f'Params: plate_height = {n0(U_SHEET)}', 52, c1, anchor='mm', path=MONO)
    harrow(d, 1040, 300, 640, 440, c1)
    harrow(d, 1520, 300, 1920, 440, c1)
    text(d, (300, 460), 'the hole', 56, c1)
    text(d, (1700, 460), 'the outline', 56, c1)
    text(d, (1280, 360), 'two parts, one name', 48, c1, anchor='mm')
    if step >= 2:
        c2 = GREEN if step == 2 else DONE
        text(d, (300, 560), f'hole = {n0(U_SHEET)} − {n0(BELOW)} = {n0(HOLE_Z)}', 56, c2, path=MONO)
        text(d, (300, 650), 'follows', 56, c2)
        text(d, (300, 740), f'checked by code: hole at {n0(HOLE_Z)}', 44, c2)
    if step >= 3:
        c3 = RED if step == 3 else DONE
        d.line((1650, 330, 1800, 420), fill=c3, width=8)
        d.line((1800, 330, 1650, 420), fill=c3, width=8)
        bb = text(d, (1620, 560), f'back {n0(TOP)} = plate_height', 56, c3, path=MONO)
        d.line((bb[0], (bb[1] + bb[3]) / 2, bb[2], (bb[1] + bb[3]) / 2), fill=c3, width=5)
        text(d, (1620, 650), '(the size we deleted)', 48, c3)
    if step >= 4:
        c4 = ORANGE if step == 4 else DONE
        text(d, (1620, 740), f'typed {n0(INNER)} + arm {n0(THICK)} = {n0(TOP)}', 52, c4, path=MONO)
        text(d, (1620, 820), 'never follows', 52, c4)
    if step >= 5:
        k, x0, base = 6.0, 1100, 1350
        cx, cy = outline(d, x0, base, k, INK, TOP, HOLE_Z)
        text(d, (x0 - 40, base - TOP * k), f'top {n0(TOP)}', 48, INK, anchor='rm')
        text(d, (cx + 60, cy - 10), f'hole at {n0(HOLE_Z)}: cuts nothing', 52, ORANGE, anchor='lm')
    save(im, f'card-why-{step}.png')


# --- F17 end card ------------------------------------------------------------------------------------------------------
def card_end():
    im, d = canvas()
    text(d, (180, 220), 'FreeCAD + Claude course', 72, INK)
    text(d, (180, 330), 'lesson 11: reference sizes', 60, BLUE)
    shot = Image.open(os.path.join(TAKES, 'U', 'iso.png')).convert('RGB').crop((1000, 200, 2400, 988))
    im.paste(shot.resize((960, 540)), (180, 470))
    d.rectangle((180, 470, 1140, 1010), outline=PARTLINE, width=3)
    text(d, (180, 1030), 'the fixed hook at 80 (filmed)', 44, GREY, path=b.R)
    text(d, (180, 1150), 'Lesson 1 and the course', 52, INK)
    save(im, 'card-end.png')


# --- the Short's why card (1080 x 1080) --------------------------------------------------------------------------------
def card_short_why(step):
    CUR.clear()
    fr = (1080, 1080)
    im = Image.new('RGB', fr, WHITE)
    d = ImageDraw.Draw(im)
    bb = text(d, (80, 90), f'back {n0(TOP)} = plate_height', 50, INK, path=MONO, frame=fr)
    d.line((bb[0], (bb[1] + bb[3]) / 2, bb[2], (bb[1] + bb[3]) / 2), fill=RED, width=5)
    if step >= 2:
        text(d, (80, 190), f'typed {n0(INNER)} + arm {n0(THICK)} = {n0(TOP)}', 50, INK, path=MONO, frame=fr)
        text(d, (80, 265), 'never follows', 50, ORANGE, frame=fr)
    if step >= 3:
        k, x0, base = 9.0, 300, 980
        cx, cy = outline(d, x0, base, k, INK, TOP, HOLE_Z)
        text(d, (cx + 50, cy), f'{n0(U_SHEET)} − {n0(BELOW)} = {n0(HOLE_Z)}', 46, ORANGE, anchor='lm', path=MONO,
             frame=fr)
        text(d, (cx + 50, cy + 70), 'checked by code:', 44, GREEN, anchor='lm', frame=fr)
        text(d, (cx + 50, cy + 130), f'hole at {n0(HOLE_Z)}', 44, GREEN, anchor='lm', frame=fr)
    save(im, f'card-short-why-{step}.png')


# --- overlays ----------------------------------------------------------------------------------------------------------
def ov_rings():
    x, y, r = HOLE
    R = r + 16
    im, d = source()
    d.ellipse((x - R, y - R, x + R, y + R), outline=ORANGE + (255,), width=6)
    save(im, 'ov-ring-60.png')
    im, d = source()
    n = 24
    import math
    for i in range(n):
        if i % 2 == 0:
            a0, a1 = 360 * i / n, 360 * (i + 1) / n
            d.arc((x - R, y - R, x + R, y + R), a0, a1, fill=ORANGE + (255,), width=6)
    save(im, 'ov-ring-80.png')
    del math


def _ov(name, box):
    im, d = source()
    x, y, w, h = box
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=WHITE + (255,))
    save(im, name)


RECAP = ['Fully constrained ≠ the sizes you meant', 'Keep the named size driving',
         'Show the extra one as reference', 'or a formula on Params']
TURN = ['Your turn, no AI:', '40 x 30, pinned', 'helper line corner to corner', 'size it as reference: ?',
        'hint: 30, 40, ?   width 60: ?']


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


def code_panel(name, lines, kind, title='checked by code', chip=None):
    xy, px, k, anchor = KIND[kind]
    im, d = source()
    code_box(d, xy[0], xy[1], lines, title, px, k, anchor, chip)
    save(im, name)
    PANEL_NAMES.append(name)


def quote_b1():
    reply = open(os.path.join(TAKES, 'runs', 'B1', 'reply.txt'), encoding='utf-8').read()
    a, z = 'Params!B1 (plate_height) was used only by', 'The top of the hook is now at 80.0 mm.'
    assert a in reply and z in reply
    im, d = source()
    a1, a2 = a.split(' was ')
    z1, z2 = z.split(' at ')
    code_box(d, 1175, 470, ['"' + a1, ' was ' + a2, ' HoleSketch ..."', '"' + z1, ' at ' + z2 + '"'],
             'its reply, scrolled up:', 42, 0.8)
    save(im, 'ov-cc-quote-B1.png')


def panels():
    T, F, U, X = (TK[t]['end_check'] for t in ('T', 'F', 'U', 'X'))
    P = NUM['build_by_code']['pinned_60']
    ctl = NUM['g0b']['orphan_100_control']
    f0 = [f"sheet {n0(T['sheet']['plate_height'])} · top {f2(T['zmax'])}", 'screw hole: none' if not T['hole_in_plate']
          else 'screw hole: yes']
    code_panel('ov-meas-F0.png', f0, 'meas', chip=CHIP)
    code_panel('ov-sk-F0.png', f0, 'sk')
    f1 = [f"top {f2(F['zmax'])} · inside {n0(F['inner']['value'])} (shown)",
          f"hole {n0(F['zmax'] - F['sketch_hole_z'])} below the top"]
    code_panel('ov-meas-F1.png', f1, 'meas')
    code_panel('ov-sk-F1.png', f1, 'sk')
    code_panel('ov-sk-F3.png', [f"hole = plate_height − {n0(P['zmax'] - P['sketch_hole_z'])}",
                                f"at {n0(P['zmax'])}: hole at {n0(P['sketch_hole_z'])}"], 'sk')
    msg = TK['D']['panel'][1][1].strip('[]').split("', '")
    head, link = (x.strip().strip("'").strip() for x in msg)
    code_panel('ov-msg-D.png', [f'panel text: {head}', link], 'msg')
    code_panel('ov-full-F6.png', [f"top {f2(T['zmax'])} · part {f2(T['stl_zmax'])} tall",
                                  f"outline sizes on plate_height: {len(T['plate_height_users'])}"], 'full')
    f9 = [f"top {f2(U['zmax'])} · inside {n0(U['inner']['value'])} (shown)",
          f"hole at {n0(U['sketch_hole_z'])}: {n0(U['zmax'] - U['sketch_hole_z'])} below the top"]
    code_panel('ov-meas-F9.png', f9, 'meas')
    code_panel('ov-sk-F9.png', f9, 'sk')
    x1 = [f"fixed: top {f2(X['zmax'])} · shown {n0(X['inner']['value'])}"]
    x2 = x1 + [f"deleted-size copy at {n0(X['sheet']['plate_height'])}:",
               f"top {f2(ctl['zmax'])} · " + ('no hole' if not ctl.get('hole_in_plate') else 'hole')]
    code_panel('ov-meas-X1.png', x1, 'meas')
    code_panel('ov-meas-X2.png', x2, 'meas')
    code_panel('ov-sk-X1.png', x1, 'sk')
    code_panel('ov-sk-X2.png', x2, 'sk')
    for run in ('A1', 'B1'):
        c = CL[run]['check']
        code_panel(f'ov-cc-{run}.png', [f"top {f2(c['zmax'])} · inside {n0(c['inner']['value'])} (formula)",
                                        f"hole at {n0(c['sketch_hole_z'])}: {n0(c['zmax'] - c['sketch_hole_z'])} below the top"],
                   'cc', title='checked by code (its file):')
    code_panel('ov-short-T.png', f0, 'short')
    code_panel('ov-short-U.png', [f"top {f2(U['zmax'])} · inside {n0(U['inner']['value'])}",
                                  f"hole {n0(U['zmax'] - U['sketch_hole_z'])} below the top"], 'short')


def still_other(src, name, rows=None):
    """F8b (cut 2): a FreeCAD screenshot of the other-order test (G0b, real app frames, not a filmed take) cut above
    STILL_CUT on white; below it only a checked-by-code panel for what the screen does not spell out. No "lab" word."""
    CUR.clear()
    im = Image.new('RGB', (SW, SH), WHITE)
    im.paste(Image.open(os.path.join(TAKES, 'G0b', src)).convert('RGB').crop((0, 0, SW, STILL_CUT)), (0, 0))
    d = ImageDraw.Draw(im)
    d.line((0, STILL_CUT, SW, STILL_CUT), fill=PARTLINE, width=3)
    if rows:
        code_box(ImageDraw.Draw(im, 'RGBA'), 60, 1410, rows, 'checked by code', 52, 0.8)
    save(im, name)


def other_order_stills():
    g = NUM['g0b']['other_order_3b_at_80']
    still_other('s7-after-ok.png', 'still-other-red.png')       # FreeCAD's panel: Redundant constraints: (24)
    still_other('s9-closed-60.png', 'still-other-inv.png', ['after Close: HookSketch Invalid', '(the ! in the tree)'])
    still_other('s9-at-80.png', 'still-other-80.png', [f"at {n0(U_SHEET)}: top {f2(g['zmax'])}"])


def short_pair():
    """The Short's frame 1 (S0): take H's right view at 60 (the hole, solid ring) beside the same view at 80 (no hole,
    dashed ring), both from the fixed camera, labelled with the cell's value; a 2880 x 1800 still, the Short's square
    rect [640, 100, 1600, 1600]."""
    CUR.clear()
    im = Image.new('RGB', (SW, SH), WHITE)
    x, y, r = HOLE
    cx0, cy0 = x - 400, 250                      # the crop: 800 x 1200 around the plate
    for i, f in enumerate(('hole-60.png', 'hole-80.png')):
        crop = Image.open(os.path.join(TAKES, 'H', f)).convert('RGB').crop((cx0, cy0, cx0 + 800, cy0 + 1200))
        im.paste(crop, (640 + 800 * i, 100))
    d = ImageDraw.Draw(im)
    R = r + 16
    for i in (0, 1):
        hx, hy = 640 + 800 * i + (x - cx0), 100 + (y - cy0)
        if i == 0:
            d.ellipse((hx - R, hy - R, hx + R, hy + R), outline=ORANGE, width=8)
        else:
            for k in range(0, 24, 2):
                d.arc((hx - R, hy - R, hx + R, hy + R), 15 * k, 15 * (k + 1), fill=ORANGE, width=8)
    d.line((1440, 100, 1440, 1300), fill=PARTLINE, width=6)
    fb = b.font(b.B, 96)
    for i, t in enumerate((f"cell {n0(NUM['build_by_code']['pinned_60']['zmax'])}", f'cell {n0(U_SHEET)}')):
        tw = d.textlength(t, font=fb)
        d.text((640 + 800 * i + (800 - tw) / 2, 1360), t, font=fb, fill=INK)
        CUR.append((t, 65))
    save(im, 'short-pair.png')


def main():
    os.makedirs(OUT, exist_ok=True)
    b.OUT = OUT
    PROBLEMS.clear()
    LOG.clear()
    PANEL_NAMES.clear()
    for s in range(1, 5):
        card_list(s)
    for s in range(1, 6):
        card_why(s)
    for s in range(1, 4):
        card_short_why(s)
    card_end()
    ov_rings()
    for s in range(1, 5):
        ov_lines('ov-recap', RECAP, s, (20, 1160, 1420, 1720))
    for s in range(1, 6):
        ov_lines('ov-turn', TURN, s, (20, 1040, 1170, 1720), px=50)   # cut 2: clear of the rectangle's corner
    _ov('ov-cc-top.png', (0, 0, 1160, 720))
    _ov('ov-cc-auto.png', (0, 1686, 1160, 114))
    quote_b1()
    panels()
    other_order_stills()
    short_pair()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
