"""FreeCAD course lesson 9 (LinearPattern coat rack) cards, SCRIPT-fc9.md rev 2 section 3. The draw_fc8.py pattern on
draw_fx20.py's helpers: light, 2560 x 1440, clean line art only (the garden fence is the one analogy), each step adds
and earlier steps turn grey, text 44 px+ and 44 columns at most, no "%" in any text, everything inside the 5 percent
safe area, highlight boxes thin orange outlines (OUTLINE_PX), never filled. Every number is NUMBERS.json's or the fence
arithmetic (tests/test_draw_fc9.py checks it); no "80" anywhere (the your-turn answer is the pinned comment only).
  full frame (RGB):  card-fence-1..5 (F2), card-length-1..4 (F9), card-trap-1..5 (F10, build 4 the fence inset),
                     card-yourturn-1..3 (F20, alone), card-end (F21, room on the right for YouTube's end screen)
  side panel (RGBA, transparent left of SIDE_X): card-recap-1..4 (F19, over take B / the frame 0 crop)
  Short (1080 x 960, RGB): card-short-why-1..2 (S1)
  source overlays (RGBA, 2880 x 1800; burnt into the derived takes A1m / B1m by footage-fc9.py), left pane only:
      ov-cc-top   (y 0-175, every frame: Claude Code's header and the lab's plan cover)
      ov-cc-save  (y 1630-1700, from the "save the document" suggestion: A1 33.0, B1 47.0)
      ov-cc-start (y 1540-1705, 0-2.15 s: the tmux hint row and the greyed "Try ..." placeholder)
      ov-cc-hint  (y 1540-1600, to 4.0 s: the tmux hint row)
  cut 3 (WATCH-fc9-c2 #1) "checked by code" panels (RGBA, 2880 x 1800; burnt into the derived takes Bc / Cc), inside
  the Measure zoom below the Measurement panel: ov-code-fix (F1, F12), ov-code-proof, ov-code-control (F15)
Run in the draw image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fc9.py [sheet OUTDIR]
Test: tests/test_draw_fc9.py"""
import json
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw_fx20 as b  # noqa: E402

LAB = b.LAB
OUT = os.path.join(LAB, 'video', 'frames-fc9')
TAKES = os.path.join(LAB, 'out', 'fc9')
b.OUT = OUT
W, H, SW, SH = b.W, b.H, b.SW, b.SH
INK, GREY, WHITE, DONE = b.INK, b.GREY, b.WHITE, b.DONE
BLUE, ORANGE, RED, GREEN = b.BLUE, b.ORANGE, b.RED, b.GREEN
PART, PARTLINE = (226, 232, 240), (71, 85, 105)
canvas, panel, source, header, save, A = b.canvas, b.panel, b.source, b.header, b.save, b.A
PROBLEMS, LOG = b.PROBLEMS, b.LOG
SAFE = (round(W * 0.05), round(H * 0.05), round(W * 0.95), round(H * 0.95))
OUTLINE_PX = 5
OUTLINES = []
SIDE_X = 1430
CC_TOP = (0, 0, 1160, 175)
CC_SAVE = (0, 1630, 1160, 70)
CC_START = (0, 1540, 1160, 165)
CC_HINT = (0, 1540, 1160, 60)
NUM = json.load(open(os.path.join(TAKES, 'NUMBERS.json')))
P, CS = NUM['part'], NUM['cases']
RW, WD, MG, HK = (f"{P[k]:g}" for k in ('rack_width', 'width', 'margin', 'hooks'))       # 180 20 20 5
FIXL = f"{CS['fix']['length_mm']:g}"                                                     # 120
TRAPL = f"{CS['trap']['length_mm']:g}"                                                   # 180
STARTS = [f'{v:g}' for v in CS['trap']['starts']]                                        # 20 65 110 155 200
STEP = f"{CS['trap']['starts'][1] - CS['trap']['starts'][0]:g}"                         # 45
NSTEP = f"{CS['trap']['occurrences'] - 1:g}"                                             # 4
YT = CS['yourturn']


def text(d, xy, s, size=56, fill=INK, path=b.B, anchor='la', maxw=None, box=None, frame=(W, H), safe=True):
    bb = b.text(d, xy, s, size, fill, path, anchor, maxw, box, frame)
    lim = SAFE if frame == (W, H) else (round(frame[0] * 0.05), round(frame[1] * 0.05), round(frame[0] * 0.95),
                                         round(frame[1] * 0.95))
    if safe and (bb[0] < lim[0] or bb[1] < lim[1] or bb[2] > lim[2] or bb[3] > lim[3]):
        PROBLEMS.append(f'{s!r}: outside the safe area {bb}')
    if '%' in s:
        PROBLEMS.append(f'{s!r}: a percent sign')
    return bb


def outline(d, name, box, alpha=False):
    d.rectangle(box, outline=A(ORANGE, alpha), width=OUTLINE_PX)
    OUTLINES.append((name, box))


def arrowhead(d, tip, dx, col, s=26):
    x, y = tip
    d.polygon([(x, y), (x - dx * s, y - s * 0.7), (x - dx * s, y + s * 0.7)], fill=col)


def harrow(d, x0, x1, y, col, w=7):
    d.line((x0, y, x1, y), fill=col, width=w)
    arrowhead(d, (x1, y), 1, col)
    arrowhead(d, (x0, y), -1, col)


def lit(step, n):
    return INK if step == n else DONE


# --- F2: the garden fence (line art) ---------------------------------------------------------------------------------
def card_fence(step):
    """1 a garden 10 m wide, 2 a 2 m border each side, 3 the fence first post to last: 6 m, not 10, 4 "6 / 2 = 3?"
    crossed out, 5 posts at 0, 2, 4, 6: 4 posts, 3 spaces."""
    im, d = canvas()
    header(d, 'A garden fence')
    x0, x1, k = 330, 2230, 190            # 10 m = 1900 px
    gy = 520
    c1 = INK if step == 1 else DONE
    d.rectangle((x0, gy, x1, gy + 260), outline=c1, width=7)
    harrow(d, x0, x1, gy - 60, c1)
    text(d, ((x0 + x1) / 2, gy - 130), 'garden 10 m', 60, c1, anchor='mm')
    f0, f1 = x0 + 2 * k, x1 - 2 * k
    if step >= 2:
        c2 = BLUE if step == 2 else DONE
        for a, bb in ((x0, f0), (f1, x1)):
            d.line((a, gy + 130, bb, gy + 130), fill=c2, width=5)
            text(d, ((a + bb) / 2, gy + 190), 'border 2 m', 50, c2, anchor='mm')
    if step >= 3:
        c3 = BLUE if step == 3 else DONE
        d.line((f0, gy + 330, f1, gy + 330), fill=c3, width=10)
        for x in (f0, f1):
            d.rectangle((x - 14, gy + 280, x + 14, gy + 380), outline=c3, width=6)
        text(d, ((f0 + f1) / 2, gy + 440), 'fence: first post to last, 6 m', 60, c3, anchor='mm')
        text(d, ((f0 + f1) / 2, gy + 520), '6 m, not 10', 60, c3, anchor='mm')
    if step >= 4:
        c4 = RED if step == 4 else DONE
        bb = text(d, (330, 1180), '6 ÷ 2 = 3?', 64, c4)
        d.line((bb[0] - 10, (bb[1] + bb[3]) / 2, bb[2] + 10, (bb[1] + bb[3]) / 2), fill=c4, width=8)
    if step >= 5:
        for i, x in enumerate((f0, f0 + 2 * k, f0 + 4 * k, f1)):
            d.rectangle((x - 14, gy + 280, x + 14, gy + 380), outline=BLUE, width=6)
            text(d, (x, gy + 250), str(2 * i), 50, BLUE, anchor='md')
        text(d, (900, 1180), 'walk it: 0, 2, 4, 6', 64, BLUE)
        text(d, (1650, 1180), '4 posts, 3 spaces', 64, INK)
    save(im, f'card-fence-{step}.png')


# --- F9: what length? -------------------------------------------------------------------------------------------------
SCALE = 10.5                              # px per mm: the 180 strip = 1890 px
SX0, SY = 335, 640


def strip(d, col, w=180):
    d.rectangle((SX0, SY, SX0 + w * SCALE, SY + 70), outline=col, width=6)


def hookbox(d, start, col, fill=None):
    x = SX0 + start * SCALE
    d.rectangle((x, SY + 70, x + 20 * SCALE, SY + 260), outline=col, width=6, fill=fill)


def card_length(step):
    """1 the strip 180, 2 margin 20 each end, 3 the last hook 20 after its start line, 4 Length = 120 (start of the
    first to start of the last)."""
    im, d = canvas()
    header(d, 'So what length?')
    c1 = INK if step == 1 else DONE
    strip(d, c1)
    harrow(d, SX0, SX0 + 180 * SCALE, SY - 60, c1)
    text(d, (SX0 + 90 * SCALE, SY - 120), f'strip {RW}', 60, c1, anchor='mm')
    for s in CS['fix']['starts']:
        hookbox(d, s, DONE)
    if step >= 2:
        c2 = BLUE if step == 2 else DONE
        for a in (0, 160):
            harrow(d, SX0 + a * SCALE, SX0 + (a + 20) * SCALE, SY + 320, c2, 5)
        text(d, (SX0, SY + 380), f'margin {MG}', 52, c2)
        text(d, (SX0 + 180 * SCALE, SY + 380), f'margin {MG}', 52, c2, anchor='ra')
    if step >= 3:
        c3 = BLUE if step == 3 else DONE
        xl = SX0 + 140 * SCALE
        d.line((xl, SY + 40, xl, SY + 300), fill=c3, width=6)
        text(d, (SX0 + 150 * SCALE, SY + 480), f'last hook {WD}', 52, c3, anchor='ma')
    if step >= 4:
        a, z = SX0 + 20 * SCALE, SX0 + 140 * SCALE
        d.line((a, SY + 40, a, SY + 300), fill=ORANGE, width=6)
        harrow(d, a, z, SY + 600, ORANGE, 8)
        text(d, ((a + z) / 2, SY + 680), f'Length = {FIXL}', 72, ORANGE, anchor='mm')
    save(im, f'card-length-{step}.png')


# --- F10: the trap ----------------------------------------------------------------------------------------------------
def card_trap(step):
    """1 the strip 0-180, the first start line at 20; 2 20 + 180 = 200, the red end line at 180; 3 4 steps x 45, the
    starts; 4 the fence inset; 5 hook 5 at 200-220 in the air: a warning only."""
    im, d = canvas()
    header(d, f'Type {TRAPL} instead')
    sc, x0, y = 8.0, 335, 560             # 0..220 mm = 1760 px
    c1 = INK if step == 1 else DONE
    d.rectangle((x0, y, x0 + 180 * sc, y + 60), outline=c1, width=6)
    a = x0 + 20 * sc
    d.line((a, y - 40, a, y + 230), fill=c1, width=6)
    text(d, (a, y - 50), 'first start 20', 50, c1, anchor='md')
    if step >= 2:
        c2 = BLUE if step == 2 else DONE
        harrow(d, a, x0 + 200 * sc, y + 300, c2, 6)
        text(d, (x0, y + 340), f'first start 20 + Length {TRAPL} = {STARTS[-1]}', 56, c2)
        e = x0 + 180 * sc
        for yy in range(y - 80, y + 260, 30):
            d.line((e, yy, e, yy + 16), fill=RED, width=7)
        text(d, (e, y - 90), f'strip ends {RW}', 50, RED, anchor='md')
    if step >= 3:
        c3 = BLUE if step == 3 else DONE
        for s in CS['trap']['starts'][:-1]:
            d.rectangle((x0 + s * sc, y + 60, x0 + (s + 20) * sc, y + 200), outline=c3, width=5)
        text(d, (x0, y + 430), f'{NSTEP} steps × {STEP}', 56, c3)
        text(d, (x0 + 560, y + 430), 'starts ' + ', '.join(STARTS), 56, c3)
    if step >= 4:
        c4 = BLUE if step == 4 else DONE
        ix, iy = 1750, 230                # the fence inset: run 10 m from the first post at 2, garden ends at 10
        d.rectangle((ix, iy, ix + 500, iy + 60), outline=c4, width=5)
        d.line((ix + 100, iy + 100, ix + 600, iy + 100), fill=c4, width=6)
        for x in (ix + 100, ix + 600):
            d.rectangle((x - 9, iy + 70, x + 9, iy + 130), outline=c4, width=4)
        text(d, (ix - 40, iy + 30), 'fence run 10 m:', 48, c4, anchor='rm')
        text(d, (ix - 40, iy + 110), 'last post 2 m past', 48, c4, anchor='rm')
    if step >= 5:
        h = x0 + 200 * sc
        d.rectangle((h, y + 60, h + 20 * sc, y + 200), outline=RED, width=6)
        text(d, (h + 10 * sc, y + 230), 'hook 5', 50, RED, anchor='ma')
        text(d, (x0, y + 610), 'touching nothing: a warning only', 60, RED)
    save(im, f'card-trap-{step}.png')


# --- F19 recap (side panel over footage) --------------------------------------------------------------------------------
RECAP = ['fence: first post to last post', 'Occurrences includes the first hook',
         'Extent Length: first start to last start', 'at 180: the last copy floats, warning only']


def wrap2(s, w=24):
    words, out, cur = s.split(), [], ''
    for wd in words:
        if cur and len(cur) + 1 + len(wd) > w:
            out.append(cur)
            cur = wd
        else:
            cur = (cur + ' ' + wd).strip()
    out.append(cur)
    return out


def card_recap(step):
    box = (SIDE_X + 20, 120, SAFE[2], 1320)
    im, d = panel(box)
    x = box[0] + 30
    text(d, (x, 170), 'Recap', 60, A(INK, True), box=box)
    y = 300
    for i, ln in enumerate(RECAP[:step]):
        col = A(BLUE if i == step - 1 else DONE, True)
        # the whole line is logged once (the tests read it), drawn wrapped
        b.CUR.append((ln, 46))
        for k, part in enumerate(wrap2(ln)):
            f = b.font(b.B, 46)
            d.text((x, y + k * 62), part, font=f, fill=col)
            bb = d.textbbox((x, y + k * 62), part, font=f)
            if bb[2] > box[2] or bb[3] > box[3]:
                PROBLEMS.append(f'{part!r}: outside its panel')
        y += 62 * len(wrap2(ln)) + 60
    save(im, f'card-recap-{step}.png')


# --- F20 your turn (alone) ----------------------------------------------------------------------------------------------
TURN = ['Your turn, no AI:', f"strip 140 · {YT['hooks']:g} hooks, {WD} wide · margins {YT['left_gap_mm']:g}",
        'Length = ?  Then measure both ends.']


def card_yourturn(step):
    im, d = canvas()
    for i, ln in enumerate(TURN[:step]):
        text(d, (300, 380 + i * 220), ln, 84 if i == 0 else 72, INK if i == 0 else (BLUE if i == step - 1 else DONE))
    save(im, f'card-yourturn-{step}.png')


# --- F21 the end card ---------------------------------------------------------------------------------------------------
def card_end():
    im, d = canvas()
    text(d, (180, 220), 'FreeCAD + Claude course', 72, INK)
    text(d, (180, 330), 'lesson 9: LinearPattern', 60, BLUE)
    shot = Image.open(os.path.join(TAKES, 'B', 'fix-iso.png')).convert('RGB').crop((1000, 400, 2280, 1120))
    im.paste(shot.resize((960, 540)), (180, 470))
    d.rectangle((180, 470, 1140, 1010), outline=PARTLINE, width=3)
    text(d, (180, 1030), 'five hooks, 20 from each end (filmed)', 44, GREY, path=b.R)
    text(d, (180, 1150), 'Lesson 8 and the course: end screen', 52, INK)
    text(d, (180, 1230), 'Subscribe: every lesson filmed', 48, GREY)
    save(im, 'card-end.png')


# --- the Short's why card (1080 x 960) ----------------------------------------------------------------------------------
def card_short_why(step):
    b.CUR.clear()
    im = Image.new('RGB', (1080, 960), WHITE)
    d = ImageDraw.Draw(im)
    fr = (1080, 960)
    c1 = INK if step == 1 else DONE
    sc, x0, y = 3.6, 110, 300              # 0..220 mm = 792 px
    d.rectangle((x0, y, x0 + 180 * sc, y + 30), outline=c1, width=5)
    for s in CS['trap']['starts'][:-1]:
        d.rectangle((x0 + s * sc, y + 30, x0 + (s + 20) * sc, y + 110), outline=c1, width=4)
    h = x0 + 200 * sc
    d.rectangle((h, y + 30, h + 20 * sc, y + 110), outline=RED, width=5)
    e = x0 + 180 * sc
    for yy in range(y - 40, y + 140, 24):
        d.line((e, yy, e, yy + 12), fill=RED, width=5)
    text(d, (540, 110), f'20 + Length {TRAPL} → 5th starts at {STARTS[-1]}', 44, c1, anchor='mm', frame=fr)
    text(d, (540, 180), f'the strip ends at {RW} · warning only', 44, c1, anchor='mm', frame=fr)
    if step >= 2:
        a, z = x0 + 20 * sc, x0 + 200 * sc
        harrow(d, a, z, y + 180, BLUE, 6)
        text(d, (540, 600), 'Length = start of first', 56, BLUE, anchor='mm', frame=fr)
        text(d, (540, 680), '→ start of last', 56, BLUE, anchor='mm', frame=fr)
    save(im, f'card-short-why-{step}.png')


# --- Claude Code covers (2880 x 1800) -----------------------------------------------------------------------------------
def _ov(name, box):
    im, d = source()
    x, y, w, h = box
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=WHITE + (255,))
    save(im, name)


# --- cut 3: the "checked by code" panels (2880 x 1800, read after the 3.2x Measure zoom) -------------------------------
MONO = b.FD + 'DejaVuSansMono.ttf'
ZOOM = 2880 / 800                      # MEAS_Z is 800 px wide on the 2880 source (the frame is 2560 + the pad)
CODE_X, CODE_Y = 2110, 838
CODE_HEAD = 'checked by code · Measure above = left end'


def code_line(case):
    k = CS[case]
    if case == 'fix':
        return f"fix      left_gap_mm {k['left_gap_mm']:.1f}  right_gap_mm {k['right_gap_mm']:.1f}"
    return f"{case:<8} length_mm {k['length_mm']:.1f}  right_gap_mm {k['right_gap_mm']:.1f}"


def code_panel(name, cases):
    im, d = source()
    hs, ls, lh = 16, 20, 28
    rows = [CODE_HEAD] + [code_line(c) for c in cases]
    fh, fl = b.font(b.B, hs), b.font(MONO, ls)
    w = max(d.textlength(r, font=fl if i else fh) for i, r in enumerate(rows)) + 32
    h = 14 + 24 + lh * len(cases) + 10
    d.rectangle((CODE_X, CODE_Y, CODE_X + w, CODE_Y + h), fill=WHITE + (255,), outline=PARTLINE + (255,), width=2)
    d.text((CODE_X + 16, CODE_Y + 12), CODE_HEAD, font=fh, fill=GREY + (255,))
    b.CUR.append((CODE_HEAD, round(hs * ZOOM * 2560 / 2880)))
    for i, r in enumerate(rows[1:]):
        d.text((CODE_X + 16, CODE_Y + 40 + lh * i), r, font=fl, fill=INK + (255,))
        b.CUR.append((r, round(ls * ZOOM * 2560 / 2880)))
        if '%' in r or len(r) > 44:
            PROBLEMS.append(f'{r!r}: code panel line')
    save(im, name)


def sheet(outdir):
    names = sorted(n for n in os.listdir(OUT) if n.startswith('card-'))
    tw, th, cols = 640, 360, 4
    rows = -(-len(names) // cols)
    sh = Image.new('RGB', (tw * cols, (th + 30) * rows), (90, 90, 90))
    dd = ImageDraw.Draw(sh)
    for i, n in enumerate(names):
        im = Image.open(os.path.join(OUT, n)).convert('RGBA')
        bg = Image.new('RGBA', im.size, (60, 70, 85, 255))
        t = Image.alpha_composite(bg, im).convert('RGB').resize((tw - 8, th - 8))
        x, y = (i % cols) * tw, (i // cols) * (th + 30)
        sh.paste(t, (x + 4, y + 4))
        dd.text((x + 6, y + th), n, font=b.font(b.R, 22), fill=(255, 255, 255))
    sh.save(os.path.join(outdir, 'cards-sheet-fc9.jpg'), quality=85)


def main():
    os.makedirs(OUT, exist_ok=True)
    PROBLEMS.clear()
    LOG.clear()
    OUTLINES.clear()
    for s in range(1, 6):
        card_fence(s)
        card_trap(s)
    for s in range(1, 5):
        card_length(s)
        card_recap(s)
    for s in (1, 2, 3):
        card_yourturn(s)
    for s in (1, 2):
        card_short_why(s)
    card_end()
    _ov('ov-cc-top.png', CC_TOP)
    _ov('ov-cc-save.png', CC_SAVE)
    _ov('ov-cc-start.png', CC_START)
    _ov('ov-cc-hint.png', CC_HINT)
    code_panel('ov-code-fix.png', ('fix',))
    code_panel('ov-code-proof.png', ('proof',))
    code_panel('ov-code-control.png', ('proof', 'control'))
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
