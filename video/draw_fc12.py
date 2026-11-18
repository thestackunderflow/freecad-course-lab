"""FreeCAD course lesson 12 (polar pattern: 240 typed in Extent put 4 hooks 80 apart; Mode Spacing with
=Params.hook_gap keeps 60) cards and panels, SCRIPT-fc12.md rev 2.1 section 3. The draw_fc11.py pattern on
draw_fx20.py / draw_fc10.py helpers: light, 2560 x 1440, clean line art (the clock is the one analogy), each step adds
and earlier steps turn grey, card lines 44 columns, code-panel lines 32 columns (Claude's quoted lines 44, re-wrapped
at word gaps, words unchanged from runs/*/reply.txt), no percent sign, never "tooltip", outlines thin, never filled.
Every number is NUMBERS.json's (out/fc12) or a lesson / typed / clock number (tests/test_draw_fc12.py).
  full frame:  card-clock-1..4 (F2), card-why-1..6 (F6), card-fix-180 (F7, cut 2), card-end (F15); Short 1080 x 1080: card-short-why-1..3 (S1)
  source overlays (RGBA 2880 x 1800, burnt in by mcp-canvas primers/footage-fc12.py):
      ov-wall-T / -F   the drawn wall line (y = -25 mm) on take T's / F's top view; T: the 4th hook ringed
      ov-sum           F4: "6 x 60 = 360" / "4 x 60 = 240 ?"
      ov-gap-80 / -60 / -F8   "checked by code" panels in the empty right pane under the Measurement panel
      ov-cc-A1 / -B1   the panels on Claude's files (FreeCAD's tree pane, below its tree)
      ov-quote-A1-1..3 / ov-quote-B1   Claude's scrolled-up lines over the terminal pane, "its reply, scrolled up:"
      ov-proof-1..2    F12 lower band: top views drawn from NUMBERS, labelled as drawn
      ov-recap-1..3, ov-turn-1..4   F13 / F14 lower-left panels (no answer)
Run in the draw image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fc12.py
Test: tests/test_draw_fc12.py"""
import json
import math
import os
import sys
import textwrap

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw_fx20 as b  # noqa: E402
import draw_fc10 as f10  # noqa: E402

LAB = b.LAB
OUT = os.path.join(LAB, 'video', 'frames-fc12')
TAKES = os.path.join(LAB, 'out', 'fc12')
W, H, SW, SH = b.W, b.H, b.SW, b.SH
INK, GREY, WHITE, DONE = b.INK, b.GREY, b.WHITE, b.DONE
BLUE, ORANGE, RED, GREEN = b.BLUE, b.ORANGE, b.RED, b.GREEN
PARTLINE = f10.PARTLINE
canvas, source, header = b.canvas, b.source, b.header
PROBLEMS, LOG, CUR = b.PROBLEMS, b.LOG, b.CUR
text, harrow, code_box = f10.text, f10.harrow, f10.code_box
MONO = f10.MONO
NUM = json.load(open(os.path.join(TAKES, 'NUMBERS.json'), encoding='utf-8'))
TK, RUNS, BUILD = NUM['takes'], NUM['runs'], NUM['build']
PANEL_NAMES = []
# take T top view (fitted at 51.9): post centre (1680, 998), 9.6 px/mm; F top view (49.1): centre (1680, 1104), 10.24
WALL_T = (1100, 998 + round(25 * 9.6), 2260)
WALL_F = (1100, 1104 + round(25 * 10.24), 2260)
RING_T = (1508, 1300, 232)            # the 4th hook (240) on T's top view
RP = (2136, 800)                      # the right-pane panel (under the Measurement panel, y 590-770)


def save(im, name):
    b.OUT = OUT
    b.save(im, name)


def n0(v):
    return f'{v:g}'


def gaps(t):
    return 'gaps: ' + ' '.join(n0(g) for g in t['gaps'])


def angles(a):
    return ' '.join(n0(x) for x in a)


# --- the clock -------------------------------------------------------------------------------------------------------
def pt(c, r, a):
    """Clock angle a (degrees clockwise from 12) at radius r round centre c."""
    t = math.radians(a)
    return c[0] + r * math.sin(t), c[1] - r * math.cos(t)


def face(d, c, r, col, lit=(), litcol=None, px=56):
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), outline=col, width=6)
    for n in range(1, 13):
        x, y = pt(c, r - 70, 30 * n)
        text(d, (x, y), str(n), px, litcol if n in lit else col, anchor='mm')


def arc(d, c, r, a0, a1, col, w=12):
    """Clockwise from clock angle a0 to a1 (PIL angles start at 3 o'clock, clockwise)."""
    d.arc((c[0] - r, c[1] - r, c[0] + r, c[1] + r), a0 - 90, a1 - 90, fill=col, width=w)


def dot(d, c, r, a, col, rad=26, ghost=False):
    x, y = pt(c, r, a)
    if ghost:
        d.ellipse((x - rad, y - rad, x + rad, y + rad), outline=col, width=6)
    else:
        d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=col)


def card_clock(step):
    im, d = canvas()
    header(d, 'A clock: a full turn')
    c, r = (760, 800), 470
    c1 = INK if step == 1 else DONE
    face(d, c, r, c1, lit=range(1, 7) if step == 3 else (), litcol=GREEN)
    text(d, (1420, 300), '12 numbers', 60, c1)
    if step >= 2:
        c2 = INK if step == 2 else DONE
        for k in range(12):
            arc(d, c, r + 40, 30 * k + 3, 30 * k + 27, c2, 10)
        arc(d, c, r + 40, 333, 357, ORANGE if step == 2 else DONE, 14)
        text(d, (1420, 400), '12 gaps of 30', 60, c2)
        text(d, (1420, 490), '11 to 12: the gap back round', 52, ORANGE if step == 2 else DONE)
    if step >= 3:
        c3 = GREEN if step == 3 else DONE
        for k in range(6):
            arc(d, c, r + 40, 30 * k + 3, 30 * k + 27, c3, 16)
        text(d, (1420, 620), 'only 12 to 6:', 60, c3)
        text(d, (1420, 710), '7 numbers, 6 gaps', 60, c3)
    if step >= 4:
        y = 1060
        for i in range(7):
            x = 1460 + i * 150
            d.rectangle((x - 12, y - 90, x + 12, y + 90), outline=BLUE, width=5)
        for i in range(6):
            d.line((1460 + i * 150 + 20, y, 1460 + (i + 1) * 150 - 20, y), fill=BLUE, width=5)
        text(d, (1420, 1180), "lesson 9's fence:", 52, BLUE)
        text(d, (1420, 1260), 'a line: one gap fewer', 60, BLUE)
    save(im, f'card-clock-{step}.png')


def card_why(step):
    im, d = canvas()
    header(d, 'Why 80? Extent runs first to last')
    c, r = (700, 800), 440
    face(d, c, r, DONE)
    c1 = ORANGE if step == 1 else DONE
    arc(d, c, r + 40, 0, 240, c1, 14)
    text(d, (1380, 300), 'Length 240: 12 to 8', 60, c1)
    if step >= 2:
        c2 = INK if step == 2 else DONE
        for a in (0, 240):
            dot(d, c, r + 40, a, c2 if step == 2 else INK)
        text(d, (1380, 390), 'a hook at each end', 56, c2)
    if step >= 3:
        c3 = INK if step == 3 else DONE
        for a in (80, 160):
            dot(d, c, r + 40, a, INK)
        for a in (0, 80, 160):
            arc(d, c, r - 10, a + 8, a + 72, BLUE if step == 3 else DONE, 8)
            x, y = pt(c, r - 10, a + 72)
            d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=BLUE if step == 3 else DONE)
        text(d, (1380, 480), '4 hooks, 3 gaps', 56, c3)
    if step >= 4:
        text(d, (1380, 590), '240 ÷ 3 = 80', 72, ORANGE if step == 4 else DONE, path=MONO)
    if step >= 5:      # cut 2 (WATCH nice 4): these lines match the 240 / 3 line, the mini ring is bigger
        c5 = INK if step == 5 else DONE
        text(d, (1380, 710), '6 hooks, first to last:', 60, c5)
        text(d, (1380, 790), '360 ÷ 5 = 72', 72, c5, path=MONO)
        text(d, (1380, 890), 'hook 6 lands on hook 1', 60, c5)
        sc, sr = (1600, 1170), 190
        d.ellipse((sc[0] - sr, sc[1] - sr, sc[0] + sr, sc[1] + sr), outline=DONE, width=5)
        for k in range(6):
            dot(d, sc, sr, 72 * k, ORANGE if (k == 5 and step == 5) else GREY, rad=22 if k < 5 else 36, ghost=True)
    if step >= 6:
        text(d, (1860, 1080), 'so at 360:', 64, GREEN)
        text(d, (1860, 1170), '360 ÷ 6 = 60', 72, GREEN, path=MONO)
    save(im, f'card-why-{step}.png')


def card_fix180():
    """Cut 2 (WATCH must 2): F7's opening clause ("Extent needs 180: three gaps of 60. Typing that works today, but
    every new count means a new sum") on the clock, in place of the broken 240 top view."""
    im, d = canvas()
    header(d, 'Extent for 4 hooks: 180')
    c, r = (700, 800), 440
    face(d, c, r, DONE)
    arc(d, c, r + 40, 0, 180, GREEN, 14)
    for a in (0, 60, 120, 180):
        dot(d, c, r + 40, a, INK)
    for a in (0, 60, 120):
        arc(d, c, r - 10, a + 6, a + 54, BLUE, 8)
    text(d, (1380, 300), 'Length 180: 12 to 6', 60, INK)
    text(d, (1380, 400), '4 hooks, 3 gaps', 60, BLUE)
    text(d, (1380, 500), '3 × 60 = 180', 80, GREEN, path=MONO)
    text(d, (1380, 700), 'typing 180 works today', 60, INK)
    text(d, (1380, 790), 'every new count: a new sum', 56, ORANGE)
    save(im, 'card-fix-180.png')


def card_short_why(step):
    CUR.clear()
    fr = (1080, 1080)
    im = Image.new('RGB', fr, WHITE)
    d = ImageDraw.Draw(im)
    c, r = (540, 610), 300
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), outline=DONE, width=5)
    for n in (12, 3, 6, 9):
        x, y = pt(c, r - 50, 30 * (n % 12))
        text(d, (x, y), str(n), 46, DONE, anchor='mm', frame=fr)
    arc(d, c, r + 30, 0, 240, ORANGE if step == 1 else DONE, 12)
    text(d, (80, 80), 'Length 240: first hook to last', 50, ORANGE if step == 1 else DONE, frame=fr)
    if step >= 2:
        for a in (0, 80, 160, 240):
            dot(d, c, r + 30, a, INK, rad=22)
        for a in (0, 80, 160):
            arc(d, c, r - 20, a + 8, a + 72, BLUE, 7)
        text(d, (80, 950), '4 hooks, 3 gaps', 50, BLUE if step == 2 else DONE, frame=fr)
    if step >= 3:
        text(d, (80, 160), '240 ÷ 3 = 80', 64, ORANGE, path=MONO, frame=fr)
    save(im, f'card-short-why-{step}.png')


def card_end():
    im, d = canvas()
    text(d, (180, 220), 'FreeCAD + Claude course', 72, INK)
    text(d, (180, 330), 'lesson 12: polar pattern', 60, BLUE)
    shot = Image.open(os.path.join(TAKES, 'P', 'h6-top.png')).convert('RGB').crop((1080, 400, 2280, 1600))
    im.paste(shot.resize((600, 600)), (180, 450))
    d.rectangle((180, 450, 780, 1050), outline=PARTLINE, width=3)
    text(d, (180, 1080), 'six hooks, 60 apart (filmed)', 44, GREY, path=b.R)
    text(d, (180, 1180), 'Lesson 9 · Lesson 1 · the course', 52, INK)
    save(im, 'card-end.png')


# --- overlays ----------------------------------------------------------------------------------------------------------
def wall(name, w, ring=None):
    im, d = source()
    x0, y, x1 = w
    d.line((x0, y, x1, y), fill=PARTLINE + (255,), width=8)
    for x in range(x0, x1, 60):
        d.line((x, y + 4, x - 30, y + 40), fill=PARTLINE + (255,), width=4)
    f = b.font(b.B, 56)
    d.text((x0 - 20, y), 'wall', font=f, fill=PARTLINE + (255,), anchor='rm')
    CUR.append(('wall', 56))
    if ring:
        x, yy, r = ring
        d.ellipse((x - r, yy - r, x + r, yy + r), outline=ORANGE + (255,), width=8)
    save(im, name)


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


def code_panel(name, lines, xy, px=44, k=0.8, title='checked by code'):
    im, d = source()
    code_box(d, xy[0], xy[1], lines, title, px, k)
    save(im, name)
    PANEL_NAMES.append(name)


def wrap(s, width=40):
    """Word gaps only; "(Params.hooks - 1)" stays on one line (the pane broke it after the minus)."""
    keep = s.replace('hooks - 1', 'hooks - 1')
    return [ln.replace(' ', ' ') for ln in textwrap.wrap(keep, width, break_long_words=False,
                                                              break_on_hyphens=False)]


def quote(name, lines, y=380):
    reply = ' '.join(open(os.path.join(TAKES, 'runs', name[9:11] + '-2', 'reply.txt'),
                          encoding='utf-8').read().split())
    assert ' '.join(lines) in reply, lines
    im, d = source()
    code_box(d, 20, y, lines, 'its reply, scrolled up:', 40, 0.8)
    save(im, name)
    PANEL_NAMES.append(name)


def top_view(d, c, angs, label, col):
    rp = 70
    d.ellipse((c[0] - rp, c[1] - rp, c[0] + rp, c[1] + rp), outline=col + (255,), width=6)
    for a in angs:
        t = math.radians(a)
        ux, uy = math.cos(t), -math.sin(t)          # math angle, screen y down
        vx, vy = -uy, ux
        hw = 0.4 * rp
        p = [(c[0] + ux * s + vx * w, c[1] + uy * s + vy * w)
             for s, w in ((0.9 * rp, -hw), (2.1 * rp, -hw), (2.1 * rp, hw), (0.9 * rp, hw))]
        d.polygon(p, outline=col + (255,), width=6)
    d.line((c[0] - 170, c[1] + rp, c[0] + 170, c[1] + rp), fill=PARTLINE + (255,), width=4)
    f = b.font(b.B, 44)
    d.text((c[0], c[1] - 210), label, font=f, fill=INK + (255,), anchor='mm')
    CUR.append((label, 35))


def ov_proof(step):
    im, d = source()
    d.rounded_rectangle((40, 1040, 2840, 1760), radius=18, fill=WHITE + (245,), outline=PARTLINE + (255,), width=4)
    f = b.font(b.R, 44)
    d.text((80, 1066), 'drawn from the numbers, not a recording', font=f, fill=GREY + (255,))
    CUR.append(('drawn from the numbers, not a recording', 35))
    views = [(RUNS['A1-2']['at3']['angles'], 'not asked · hooks 3'), (RUNS['B1-2']['at3']['angles'], 'asked · hooks 3')]
    if step >= 2:
        views += [(RUNS['A1-2']['at6']['angles'], 'not asked · hooks 6'), (RUNS['B1-2']['at6']['angles'], 'asked · hooks 6')]
    for i, (a, lab) in enumerate(views):
        top_view(d, (420 + 680 * i, 1480), a, lab, (GREEN if i >= 2 or step == 1 else DONE))
    a3 = RUNS['A1-2']['at3']['angles']
    assert a3 == RUNS['B1-2']['at3']['angles'] and RUNS['A1-2']['at6']['gaps'] == RUNS['B1-2']['at6']['gaps']
    g6 = set(RUNS['A1-2']['at6']['gaps'])
    assert len(g6) == 1
    code_box(d, 40, 560, [f'hooks 3: {angles(a3)} (both)', f'hooks 6: ring, {n0(g6.pop())} apart (both)'],
             'checked by code (its files):', 56, 0.8)      # cut 2 (WATCH nice 6): was 48
    save(im, f'ov-proof-{step}.png')
    PANEL_NAMES.append(f'ov-proof-{step}.png')


def ov_sum():
    im, d = source()
    d.rounded_rectangle((500, 1300, 1260, 1560), radius=18, fill=WHITE + (245,), outline=PARTLINE + (255,), width=4)
    f = b.font(b.B, 72)
    for i, (t, col) in enumerate((('6 × 60 = 360 ✔', GREEN), ('4 × 60 = 240 ?', ORANGE))):
        d.text((540, 1330 + i * 110), t, font=f, fill=col + (255,))
        CUR.append((t, 58))
    save(im, 'ov-sum.png')


RECAP = ['Full turn: gaps = hooks, like a clock', 'Extent: first to last, 1 gap fewer',
         'Spacing mode: type the gap itself']
TURN = ['Your turn: 8 hooks, a wider post', 'Extent, Length 360: how far apart?',
        'Extent, Length 315: how far apart?', 'Why the same? Hint: 8 gaps or 7?']


def panels():
    T, F = TK['T']['end'], TK['F']['end']
    code_panel('ov-gap-80.png', [gaps(T)], RP)
    code_panel('ov-gap-60.png', [gaps(F)], RP)
    h3, t3 = NUM['g0']['q4-fixed-gui-h3'], BUILD['typed180_h3']
    code_panel('ov-gap-F8.png', [f"fixed, hooks 3: {' '.join(n0(g) for g in h3['gaps'])}",
                                 f"typed {n0(t3['angle'])}, hooks 3: {' '.join(n0(g) for g in t3['gaps'])}"], RP)
    a4, b4, b3 = RUNS['A1-2']['after'], RUNS['B1-2']['after'], RUNS['B1-2']['at3']
    code_panel('ov-cc-A1.png', [f"hooks 4: {angles(a4['angles'])}"], (1175, 1330), 63,   # cut 3 (WATCH nice 4): 1.5x (was 42)
               title='checked by code (its file):')
    code_panel('ov-cc-B1.png', [f"hooks 4: {angles(b4['angles'])}", f"hooks 3: {angles(b3['angles'])}"],
               (1175, 1330), 63, title='checked by code (its file):')
    quote('ov-quote-A1-1.png', wrap('The pattern uses a hardcoded 240° span, so the four hooks sit 80° apart'))
    quote('ov-quote-A1-2.png', ['The four hooks are now 60° apart.'])
    quote('ov-quote-A1-3.png', wrap("Fix: I set the pattern's Angle to the expression Params.hook_gap * "
                                    '(Params.hooks - 1).'))
    quote('ov-quote-B1.png', ['hooks: 4 (yours)', 'pattern Angle: 180°', 'hook angles: 0, 60, 120, 180',
                              'gaps between neighbours: 60, 60, 60'])


def main():
    os.makedirs(OUT, exist_ok=True)
    b.OUT = OUT
    PROBLEMS.clear()
    LOG.clear()
    PANEL_NAMES.clear()
    for s in range(1, 5):
        card_clock(s)
    for s in range(1, 7):
        card_why(s)
    card_fix180()
    for s in range(1, 4):
        card_short_why(s)
    card_end()
    wall('ov-wall-T.png', WALL_T, RING_T)
    wall('ov-wall-F.png', WALL_F)
    ov_sum()
    for s in range(1, 4):
        ov_lines('ov-recap', RECAP, s, (20, 1200, 1500, 1720))
    for s in range(1, 5):
        ov_lines('ov-turn', TURN, s, (20, 1100, 1420, 1720), px=54)
    for s in (1, 2):
        ov_proof(s)
    panels()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
