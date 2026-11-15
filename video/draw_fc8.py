"""FreeCAD course lesson 8 (assembly) cards, SCRIPT-fc8.md rev 2 section 4. The draw_sc8.py pattern (the twin lesson;
the drawer and print drawings redrawn with FreeCAD wording) on draw_fx20.py's helpers: light, 2560 x 1440, clean line
art only (the drawer is the one analogy, line art), each step adds and earlier steps turn grey, text 44 px+ and 44
columns at most, everything inside the 5% safe area, highlight boxes thin orange outlines (OUTLINE_PX), never filled.
Every number is NUMBERS.json's (tests/test_draw_fc8.py checks it). Steps follow F-row sentences (a card never runs
ahead of its words):
  full frame (RGB):  card-drawer-1..4 (F2: dresser, jam, gap, map), card-assembly-1..3 (F3), card-joint-1..2 (F6),
                     card-notacheck-1..3 (F9), card-zero-1..3 (F13), card-print-1..4 (F14), card-sofar-1..5 (F19),
                     card-recap-0..4 (F23: the title, then one line per sentence), card-end (F25, room on the right for
                     YouTube's end-screen elements)
  side panel (RGBA, transparent left of SIDE_X): card-yourturn-1..4 (F24, over take D; asked, never answered)
  source overlays (RGBA, 2880 x 1800; burnt into the derived takes A1m / B1m by footage-fc8.py), left pane only:
      ov-cc-top    (y 0-260, every frame of both runs: Claude Code's header with the account plan name)
      ov-cc-notice (y 260-810, until the "Auto mode is now ..." notice has scrolled under the top cover)
      ov-cc-start  (y 1540-1705, 0-2.1 s: the tmux hint row and the greyed "Try ..." placeholder)
      ov-cc-hint   (y 1540-1600, to 4.0 s: the tmux hint row, still there while the first line is typed)
The F21 / F22 Claude cards and every chip are burnt in as labels by footage-fc8.py (no PNG; the sc8 precedent).
Run in the draw image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fc8.py [sheet OUTDIR]
Test: tests/test_draw_fc8.py"""
import json
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw_fx20 as b  # noqa: E402

LAB = b.LAB
OUT = os.path.join(LAB, 'video', 'frames-fc8')
TAKES = os.path.join(LAB, 'out', 'fc8')
b.OUT = OUT
W, H, SW, SH = b.W, b.H, b.SW, b.SH
INK, GREY, WHITE, DONE = b.INK, b.GREY, b.WHITE, b.DONE
BLUE, ORANGE, RED = b.BLUE, b.ORANGE, b.RED
PART, PARTLINE = (226, 232, 240), (71, 85, 105)
canvas, panel, source, header, save, A = b.canvas, b.panel, b.source, b.header, b.save, b.A
PROBLEMS, LOG = b.PROBLEMS, b.LOG
SAFE = (round(W * 0.05), round(H * 0.05), round(W * 0.95), round(H * 0.95))
OUTLINE_PX = 5
OUTLINES = []
SIDE_X = 1430                       # F24: take D left (MIX share 0.55), the your-turn panel right of SIDE_X
CC_TOP = (0, 0, 1160, 260)          # Claude Code's header: logo, "Claude Code v2.1.308", model + plan name, folder
CC_NOTICE = (0, 260, 1160, 550)     # "Auto mode is now ..." notice + "1 more notice hidden" (y 267-800 at start)
CC_START = (0, 1540, 1160, 165)     # the tmux hint row (y ~1566) + the input row's greyed "Try ..." (y ~1663)
CC_HINT = (0, 1540, 1160, 60)       # the tmux hint row alone (OCR: still there until ~3.5 s, after typing starts)
NUM = json.load(open(os.path.join(TAKES, 'NUMBERS.json')))
C = NUM['cases']
GAP = f"{C['gap04']['gap']:g}"                       # 0.4
ZERO = f"{C['touch']['common_mm3']:g}"               # 0


def text(d, xy, s, size=56, fill=INK, path=b.B, anchor='la', maxw=None, box=None, frame=(W, H), safe=True):
    bb = b.text(d, xy, s, size, fill, path, anchor, maxw, box, frame)
    if safe and (bb[0] < SAFE[0] or bb[1] < SAFE[1] or bb[2] > SAFE[2] or bb[3] > SAFE[3]):
        PROBLEMS.append(f'{s!r}: outside the safe area {bb}')
    return bb


def outline(d, name, box, alpha=False):
    d.rectangle(box, outline=A(ORANGE, alpha), width=OUTLINE_PX)
    OUTLINES.append((name, box))


def lit(step, n):
    return INK if step == n else DONE


# --- F2: a drawer in a dresser (line art), one step per sentence --------------------------------------------------------
def dresser(d, x, y, w, h, gap, col):
    d.rectangle((x, y, x + w, y + h), outline=col, width=6)                       # the dresser
    hx, hy, hw, hh = x + w * 0.2, y + h * 0.3, w * 0.6, h * 0.4                    # the hole
    d.rectangle((hx, hy, hx + hw, hy + hh), outline=col, width=6)
    d.rectangle((hx + gap, hy + gap, hx + hw - gap, hy + hh - gap), fill=PART, outline=col, width=6)   # the drawer
    d.ellipse((hx + hw / 2 - 16, hy + hh / 2 - 16, hx + hw / 2 + 16, hy + hh / 2 + 16), outline=col, width=6)
    return hx, hy, hw, hh


def card_drawer(step):
    """1 the dresser ("Think of a drawer"), 2 a drawer exactly the hole's size ("would jam"), 3 the small gap round the
    drawer ("so it slides"), 4 the map to the hook and rail + the rule."""
    im, d = canvas()
    header(d, 'A drawer in a dresser')
    hx, hy, hw, hh = dresser(d, 220, 330, 900, 560, 22, PARTLINE)
    if step >= 2:
        x, y = 1400, 820
        col = RED if step == 2 else DONE
        d.rectangle((x, y, x + 520, y + 300), fill=PART, outline=col, width=6)
        d.line((x + 40, y + 150, x + 480, y + 150), fill=col, width=14)
        text(d, (x, y - 90), 'no gap: it jams', 60, col)
    if step >= 3:
        outline(d, f'card-drawer-{step}.png', (int(hx) - 14, int(hy) - 14, int(hx + hw) + 14, int(hy + hh) + 14))
        text(d, (220, 960), 'a small gap: it slides', 60, BLUE if step == 3 else DONE)
    if step >= 4:
        text(d, (1400, 360), "hole = hook's slot", 60, INK)
        text(d, (1400, 450), "drawer = rail's rib", 60, INK)
        text(d, (220, 1100), 'parts that move need a gap', 64, INK)
    save(im, f'card-drawer-{step}.png')


# --- F3: an assembly --------------------------------------------------------------------------------------------------
def hook_outline(d, x, y, col, s=1.0):
    pts = [(x, y), (x + 120 * s, y), (x + 120 * s, y + 420 * s), (x + 330 * s, y + 420 * s), (x + 330 * s, y + 520 * s),
           (x, y + 520 * s)]
    d.line(pts + [pts[0]], fill=col, width=7, joint='curve')


def card_assembly(step):
    im, d = canvas()
    header(d, 'An assembly')
    frame = (220, 260, 1500, 1260)
    d.rounded_rectangle(frame, radius=30, outline=lit(step, 1), width=7)
    text(d, (250, 1180), 'one file', 56, lit(step, 1))
    text(d, (1640, 330), 'parts in one file', 56, lit(step, 1))
    if step >= 2:
        col = BLUE if step == 2 else DONE
        hook_outline(d, 360, 380, col)
        d.rectangle((1000, 360, 1100, 1120), outline=col, width=7)
        text(d, (420, 330), 'hook', 52, col)
        text(d, (1120, 340), 'rail', 52, col)
        text(d, (1640, 450), 'each kept separate', 56, col)
    if step >= 3:
        y = 700
        d.line((790, y, 960, y), fill=ORANGE, width=8)
        arrowhead(d, (960, y), 1, 0, ORANGE)
        arrowhead(d, (790, y), -1, 0, ORANGE)
        text(d, (1640, 570), 'rules for moving', 56, ORANGE)
        text(d, (1640, 700), '= an assembly', 64, INK)
    save(im, f'card-assembly-{step}.png')


def arrowhead(d, tip, dx, dy, col, s=26):
    x, y = tip
    if dx:
        pts = [(x, y), (x - dx * s, y - s * 0.7), (x - dx * s, y + s * 0.7)]
    else:
        pts = [(x, y), (x - s * 0.7, y - dy * s), (x + s * 0.7, y - dy * s)]
    d.polygon(pts, fill=col)


# --- F6: a slider joint (full frame) ----------------------------------------------------------------------------------
def card_joint(step):
    """1 "a joint, a rule between two components" (the hook on the rail), 2 the slider: one line, the rest crossed out."""
    im, d = canvas()
    header(d, 'A joint')
    text(d, (1300, 330), 'joint = a rule', 64, lit(step, 1))
    text(d, (1300, 420), 'between two components', 56, lit(step, 1))
    rx = 700
    d.rectangle((rx - 50, 300, rx + 50, 1250), outline=PARTLINE, width=6)          # the rail
    text(d, (rx - 80, 1200), 'rail', 52, GREY, anchor='rm')
    d.rectangle((rx - 150, 620, rx + 150, 860), outline=lit(step, 1) if step == 1 else BLUE, width=7)   # the hook
    text(d, (rx + 180, 650), 'hook', 52, INK, anchor='lm')
    if step >= 2:
        d.line((rx, 380, rx, 590), fill=BLUE, width=8)
        arrowhead(d, (rx, 370), 0, -1, BLUE)
        d.line((rx, 890, rx, 1100), fill=BLUE, width=8)
        arrowhead(d, (rx, 1110), 0, 1, BLUE)
        for x0, x1 in ((rx - 520, rx - 220), (rx + 220, rx + 520)):
            d.line((x0, 740, x1, 740), fill=DONE, width=6)
            cx = (x0 + x1) / 2
            d.line((cx - 34, 706, cx + 34, 774), fill=ORANGE, width=9)
            d.line((cx - 34, 774, cx + 34, 706), fill=ORANGE, width=9)
        text(d, (1300, 640), 'slider: one line only', 64, BLUE)
        text(d, (1300, 740), 'like a drawer on its runners', 52, GREY)
    save(im, f'card-joint-{step}.png')


# --- F9: a drag is not a check ----------------------------------------------------------------------------------------
def card_notacheck(step):
    im, d = canvas()
    header(d, 'Why nothing stopped it')
    rx = 420
    d.rectangle((rx - 40, 300, rx + 40, 1000), outline=PARTLINE, width=6)
    d.rectangle((rx - 120, 560, rx + 120, 740), outline=lit(step, 1), width=7)
    d.line((rx, 330, rx, 530), fill=lit(step, 1), width=7)
    arrowhead(d, (rx, 320), 0, -1, lit(step, 1))
    d.line((rx, 770, rx, 970), fill=lit(step, 1), width=7)
    arrowhead(d, (rx, 980), 0, 1, lit(step, 1))
    text(d, (760, 420), 'joint: which way it may move', 64, lit(step, 1))
    text(d, (760, 510), '(along the rail)', 52, GREY)
    if step >= 2:
        col = RED if step == 2 else DONE
        x, y = 760, 680
        d.rectangle((x, y, x + 1340, y + 140), outline=col, width=6)
        text(d, (x + 40, y + 70), 'joint: does it overlap? never asked', 60, col, anchor='lm')
        cx, cy = x + 1440, y + 70          # a cross beside the box, never over its words
        d.line((cx - 45, cy - 45, cx + 45, cy + 45), fill=col, width=10)
        d.line((cx - 45, cy + 45, cx + 45, cy - 45), fill=col, width=10)
    if step >= 3:
        text(d, (760, 1000), 'a drag is not a check', 80, BLUE)
    save(im, f'card-notacheck-{step}.png')


# --- F13: touching shares a wall, no space ----------------------------------------------------------------------------
def card_zero(step):
    im, d = canvas()
    header(d, 'Touching')
    x0, y0 = 300, 360
    d.rectangle((x0, y0, x0 + 400, y0 + 700), fill=PART, outline=PARTLINE, width=6)            # the slot's wall
    d.rectangle((x0 + 400, y0, x0 + 800, y0 + 700), outline=PARTLINE, width=6)                 # the rib's wall
    d.line((x0 + 400, y0 - 40, x0 + 400, y0 + 740), fill=lit(step, 1) if step == 1 else BLUE, width=10)
    text(d, (x0, y0 + 760), 'slot wall', 52, GREY)
    text(d, (x0 + 800, y0 + 760), 'rib wall', 52, GREY, anchor='ra')
    text(d, (1300, 420), 'touching: shared wall, no shared space', 50, lit(step, 1))
    if step >= 2:
        col = BLUE if step == 2 else DONE
        d.rounded_rectangle((1290, 600, 2100, 720), radius=24, outline=col, width=5)
        text(d, (1330, 660), f'shared space = {ZERO} mm³', 60, col, anchor='lm')
    if step >= 3:
        text(d, (1300, 880), 'touching is not room to slide', 64, RED)
    save(im, f'card-zero-{step}.png')


# --- F14: why a printer needs the gap (a section through slot and rib) -------------------------------------------------
def t_shape(d, x, y, col, grow=0, width=7, fill=None):
    pts = [(x - grow, y - grow), (x + 360 + grow, y - grow), (x + 360 + grow, y + 90 + grow), (x + 270 + grow, y + 90 + grow),
           (x + 270 + grow, y + 350), (x + 90 - grow, y + 350), (x + 90 - grow, y + 90 + grow), (x - grow, y + 90 + grow)]
    if fill:
        d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=col, width=width, joint='curve')


def card_print(step):
    """1 drawn at gap 0 ("a printer is not exact"), 2 holes smaller + the first layer wider, 3 the walls pressing,
    4 Prusa's sentence."""
    im, d = canvas()
    header(d, 'Why gap 0 is not enough')
    x, y = 420, 520
    t_shape(d, x, y, lit(step, 1), fill=PART)
    t_shape(d, x, y, lit(step, 1), grow=0, width=4)
    text(d, (420, 330), 'slot and rib, cut through', 52, GREY)
    text(d, (1250, 330), 'drawn: gap 0', 60, lit(step, 1))
    if step >= 2:
        col = BLUE if step == 2 else DONE
        t_shape(d, x + 14, y + 14, col, grow=-14, width=5)
        d.line((x + 70, y + 350, x + 290, y + 350), fill=col, width=16)
        text(d, (1250, 460), 'holes print a little small', 60, col)
        text(d, (1250, 535), 'Bambu Lab wiki', 46, GREY, path=b.R)
        text(d, (1250, 650), 'first layer spreads', 60, col)
        text(d, (1250, 725), 'Prusa KB: elephant foot', 46, GREY, path=b.R)
    if step >= 3:
        for px, py in ((x + 90, y + 200), (x + 270, y + 200), (x + 180, y + 90)):
            d.ellipse((px - 22, py - 22, px + 22, py + 22), outline=RED if step == 3 else DONE, width=7)
        text(d, (1250, 860), "won't go together without force", 60, RED if step == 3 else DONE)
    if step >= 4:
        text(d, (1250, 1040), '"An initial good measurement for movable', 50, INK, path=b.R)
        text(d, (1250, 1110), 'parts is at least 0.3 mm." Prusa KB', 50, INK, path=b.R)
    save(im, f'card-print-{step}.png')


# --- F19 so far, F23 recap: one line per spoken clause -----------------------------------------------------------------
SOFAR = ['assembly = components, one grounded', 'joined by a joint', 'a drag is not a check',
         'Intersection: shared space; touch = 0', 'Measure: reads the gap']
RECAP = ['parts that move need a gap', 'a drag is not a check', 'Intersection: overlap, not touching',
         'Measure: reads the gap']


def lines_card(title, lines, step, name):
    im, d = canvas()
    header(d, title)
    for i, ln in enumerate(lines[:step]):
        text(d, (300, 300 + i * 170), ln, 72, BLUE if i == step - 1 else DONE)
    save(im, name)


# --- F24: your turn (right panel over take D) --------------------------------------------------------------------------
TURN = ['Your turn, no AI (start file below):', '1. Run Intersection. Read the volume.',
        f'2. Set gap to {GAP}. Measure both sides.', "Why can't the gap-0 hook slide on a print?"]


def card_yourturn(step):
    box = (SIDE_X + 20, 120, SAFE[2], 1320)
    im, d = panel(box)
    x = box[0] + 30
    for i, ln in enumerate(TURN[:step]):
        y = 190 + i * 230 + (60 if i == 3 else 0)
        col = A(INK if i == 0 else (BLUE if i == step - 1 else DONE), True)
        lines = [ln] if len(ln) <= 26 else wrap2(ln)
        for k, part in enumerate(lines):
            text(d, (x, y + k * 70), part, 50 if i else 52, col, path=b.B if i in (0, 3) else b.R, box=box)
    save(im, f'card-yourturn-{step}.png')


def wrap2(s, w=26):
    words, out, cur = s.split(), [], ''
    for wd in words:
        if cur and len(cur) + 1 + len(wd) > w:
            out.append(cur)
            cur = wd
        else:
            cur = (cur + ' ' + wd).strip()
    out.append(cur)
    return out


# --- F25: the end card ------------------------------------------------------------------------------------------------
def card_end():
    im, d = canvas()
    text(d, (180, 220), 'FreeCAD + Claude course', 72, INK)
    text(d, (180, 330), 'lesson 8: assembly', 60, BLUE)
    shot = Image.open(os.path.join(TAKES, 'D', 'measure-left.png')).convert('RGB').crop((1300, 300, 2620, 1042))
    im.paste(shot.resize((960, 540)), (180, 470))
    d.rectangle((180, 470, 1140, 1010), outline=PARTLINE, width=3)
    text(d, (180, 1030), 'Measure, both sides (filmed)', 44, GREY, path=b.R)
    text(d, (180, 1150), 'Lesson 1 and the course: end screen', 52, INK)
    text(d, (180, 1230), 'Subscribe: every lesson filmed', 48, GREY)
    save(im, 'card-end.png')


# --- Claude Code covers (2880 x 1800) ---------------------------------------------------------------------------------
def _ov(name, box, label=None):
    im, d = source()
    x, y, w, h = box
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=WHITE + (255,))
    if label:
        text(d, (40, y + h / 2), label, 44, GREY + (255,), anchor='lm', frame=(SW, SH), safe=False)
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
    sh.save(os.path.join(outdir, 'cards-sheet-fc8.jpg'), quality=85)


def main():
    os.makedirs(OUT, exist_ok=True)
    PROBLEMS.clear()
    LOG.clear()
    OUTLINES.clear()
    for s in (1, 2, 3, 4):
        card_drawer(s)
        card_print(s)
        card_yourturn(s)
    for s in (1, 2, 3):
        card_assembly(s)
        card_notacheck(s)
        card_zero(s)
    for s in (1, 2):
        card_joint(s)
    for s in range(1, 6):
        lines_card('So far', SOFAR, s, f'card-sofar-{s}.png')
    for s in range(0, 5):
        lines_card('Recap', RECAP, s, f'card-recap-{s}.png')
    card_end()
    _ov('ov-cc-top.png', CC_TOP, "(Claude Code's header, hidden)")
    _ov('ov-cc-notice.png', CC_NOTICE, '(start-up notice, hidden)')
    _ov('ov-cc-start.png', CC_START)
    _ov('ov-cc-hint.png', CC_HINT)
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
