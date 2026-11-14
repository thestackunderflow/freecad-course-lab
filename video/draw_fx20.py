"""Fix-it fx20 cards (FreeCAD 1.1: "Negative datum values are not valid for the constraint with index 23" when a 17 mm
size is added to the hook's arm top, already set by bottom 25 - lip 5 - back plate 5 = 15). The draw_fx19.py pattern
(helpers copied, no import across files): light, 2560 x 1440, clean line diagrams (the carpenter's notes are the one
analogy, line art), each step adds, earlier steps stay and turn grey. Text 44 px+, 44 columns at most per line.
SCRIPT-fx20.md rev 2 section 4.
  full frame (RGB):  card-carpenter-1..5 (F3; the script's build 2 in two steps (the 4th note, the sum) and
                     build 3 in two (the four labels, then the solver), so no card holds over ~12 s), card-sofar-1..3 (F8), card-end (F11)
  side panels (RGBA, transparent left of SIDE_X): card-decode-1..7 (F4), card-recipe-1..5 (F10),
                     card-question-1..2 (F10, asked, never answered)
  source overlays (RGBA, 2880 x 1800; burnt into derived takes by footage-fx20.py):
      ov-r1-top  (R1 0-24 s: Claude Code's start screen: the banner with the account plan name and the "Auto mode is
                  now ..." notice, left pane x 0-1160, y 0-850; says so)
      ov-r1-odes (R1 from 24 s: the notice's last lines "odes" / "1 more notice hidden" at the pane's top)
      ov-r1-hint (R1: the "Fast mode is now available" / "tmux ..." hint row, y ~1545-1600)
      ov-a-rep   (A: the Report view dock, plain light panel, no text; under the popup close-ups only)
      ov-r1-try  (R1: the input row's greyed suggestions "Try ..." (0-2.1 s) and "save the document" (from ~24 s))
  short-stack.png: the Short's frame 1 (1080 x 960): A/popup.png (Report view + the popup) over B/green.png (the
                   bottom 27 and "Fully constrained").
The F5 check, F9 plug / tool log / check cards are burnt in as labels by footage-fx20.py (no PNG; the fx19 precedent).
Run in the draw image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fx20.py [sheet OUTDIR]
Test: tests/test_draw_fx20.py"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-fx20')
TAKES = os.path.join(LAB, 'out', 'fx20')
FD = '/usr/share/fonts/truetype/dejavu/'
B, R = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf'
W, H = 2560, 1440
SW, SH = 2880, 1800
INK, GREY = (31, 41, 55), (110, 120, 138)
WHITE, PANEL = (255, 255, 255), (250, 251, 253)
DONE, DONEFILL = (160, 167, 178), (244, 246, 248)
BLUE, BLUEFILL = (37, 99, 235), (219, 234, 254)
ORANGE, ORANGEFILL = (234, 88, 12), (255, 237, 213)
RED = (185, 28, 28)
GREEN = (21, 128, 61)
PAPER, WOOD = (254, 249, 195), (180, 120, 60)
MIN_PX = 44
PROBLEMS = []
LOG = {}
CUR = []
SIDE_X = 1430
# the course hook (mm), lab G0/g0a.txt: back plate 5 x 60, bottom 25, lip 5 wide and 10 tall; the arm's top is the
# line (5, 5)-(20, 5): 25 - 5 - 5 = 15, no size of its own
HOOK = [(0, 0), (25, 0), (25, 10), (20, 10), (20, 5), (5, 5), (5, 60), (0, 60), (0, 0)]
R1_TOP = (0, 0, 1160, 850)          # R1 0-24 s: banner (plan name) + "Auto mode is now ..." notice, y 0-800
R1_ODES = (0, 0, 1160, 115)         # R1 24 s on: "odes" / "1 more notice hidden" at the top
R1_HINT = (0, 1545, 1160, 60)       # R1: "Fast mode is now available" / "tmux detected" / "tmux focus-events" (y ~1580)
R1_TRY = (0, 1610, 1160, 92)        # R1: the input row (y ~1655): "Try ..." placeholder, "save the document" suggestion
A_REP = (0, 1392, 1560, 150)        # A: the Report view dock (header y ~1404, red lines y 1440-1530, x 16-1520)
DOCK_FILL = (248, 248, 248)


# --- drawing helpers (copied from draw_fx19.py) -----------------------------------------------------------------------
def font(p, s):
    return ImageFont.truetype(p, s)


def text(d, xy, s, size=64, fill=INK, path=B, anchor='la', maxw=None, box=None, frame=(W, H)):
    CUR.append((s, size))
    if size < MIN_PX:
        PROBLEMS.append(f'{s!r}: {size} px')
    f = font(path, size)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)
    bb = d.textbbox(xy, s, font=f, anchor=anchor)
    if maxw and bb[2] - bb[0] > maxw:
        PROBLEMS.append(f'{s!r}: {bb[2] - bb[0]:.0f} px wide, max {maxw}')
    if bb[0] < 0 or bb[2] > frame[0] or bb[1] < 0 or bb[3] > frame[1]:
        PROBLEMS.append(f'{s!r}: off the frame {bb}')
    if box and (bb[0] < box[0] or bb[1] < box[1] or bb[2] > box[2] or bb[3] > box[3]):
        PROBLEMS.append(f'{s!r}: outside its panel {bb} vs {box}')
    if '<' in s or '>' in s:
        PROBLEMS.append(f'{s!r}: angle bracket')
    if len(s) > 44:
        PROBLEMS.append(f'{s!r}: {len(s)} columns, max 44')
    return bb


def canvas():
    CUR.clear()
    im = Image.new('RGB', (W, H), WHITE)
    return im, ImageDraw.Draw(im)


def panel(box):
    CUR.clear()
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=28, fill=PANEL + (255,), outline=INK + (255,), width=5)
    return im, d


def source():
    CUR.clear()
    im = Image.new('RGBA', (SW, SH), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def header(d, s):
    text(d, (W / 2, 100), s, 84, anchor='mm', maxw=2400)


def save(im, name):
    im.save(os.path.join(OUT, name))
    LOG[name] = list(CUR)
    print(name)


def A(c, alpha=True):
    return c + (255,) if alpha else c


# --- the hook outline -------------------------------------------------------------------------------------------------
def hook_pts(x0, y0, s):
    return [(x0 + x * s, y0 - y * s) for x, y in HOOK]


def hook(d, x0, y0, s, col, width=7, alpha=True, arm=None):
    """The hook's 8 lines; `arm` = the colour of the arm's top line (5, 5)-(20, 5), drawn thicker."""
    pts = hook_pts(x0, y0, s)
    d.line(pts, fill=A(col, alpha), width=width, joint='curve')
    for p in pts[:-1]:
        d.ellipse((p[0] - 8, p[1] - 8, p[0] + 8, p[1] + 8), fill=A(col, alpha))
    if arm:
        d.line((pts[4], pts[5]), fill=A(arm, alpha), width=width + 6)
    return pts


# --- F3: the carpenter's notes ----------------------------------------------------------------------------------------
def note(d, x, y, s, col, w=380, h=120, fill=PAPER, cross=False):
    d.rectangle((x, y, x + w, y + h), fill=fill, outline=col, width=6)
    text(d, (x + w / 2, y + h / 2), s, 60, col, anchor='mm')
    if cross:
        d.line((x - 10, y - 10, x + w + 10, y + h + 10), fill=ORANGE, width=9)


def carpenter(d, x, y, col):
    """A plain line-art carpenter (head, body, arms) beside the bench."""
    d.ellipse((x - 60, y - 60, x + 60, y + 60), outline=col, width=8)
    d.line((x, y + 60, x, y + 330), fill=col, width=10)
    d.line((x, y + 140, x + 150, y + 230), fill=col, width=10)
    d.line((x, y + 140, x - 130, y + 240), fill=col, width=10)
    d.line((x, y + 330, x - 90, y + 520), fill=col, width=10)
    d.line((x, y + 330, x + 90, y + 520), fill=col, width=10)
    d.line((x - 70, y - 60, x + 70, y - 60), fill=col, width=12)   # cap brim


def shelf(d, x0, y0, s, col, fill):
    """The L-shelf from the notes (back 5, shelf 25, lip 5), no rails: the hook outline filled as wood."""
    pts = hook_pts(x0, y0, s)
    d.polygon(pts[:-1], fill=fill)
    d.line(pts, fill=col, width=8, joint='curve')
    return pts


def card_carpenter(step):
    im, d = canvas()
    header(d, 'Notes to a carpenter')
    k = lambda n: INK if step == n else DONE    # noqa: E731
    carpenter(d, 260, 520, k(1))
    note(d, 520, 260, 'shelf 25', k(1))
    note(d, 520, 420, 'lip 5', k(1))
    note(d, 520, 580, 'back 5', k(1))
    pts = shelf(d, 1050, 1080, 13, k(1), (233, 214, 186) if step == 1 else DONEFILL)
    text(d, (1050 + 12.5 * 13, 1080 + 50), 'shelf', 52, k(1), anchor='mt')
    if step >= 2:
        a, b = pts[4], pts[5]
        c2 = ORANGE if step in (2, 3) else DONE
        d.line((a, b), fill=c2, width=16)
        note(d, 1600, 300, 'arm 17', c2, fill=ORANGEFILL if step in (2, 3) else DONEFILL)
        d.line((1590, 360, 1420, 600), fill=c2, width=8)
        d.polygon(((1420, 600), (1420, 550), (1460, 585)), fill=c2)
        text(d, (1600, 450), '(the arm: between back and lip)', 48, GREY if step == 2 else DONE)
    if step >= 3:
        c3 = ORANGE if step == 3 else DONE
        text(d, (1600, 540), '25 - 5 - 5 = 15', 72, c3)
        text(d, (1600, 650), 'four notes, one shelf:', 60, c3)
        text(d, (1600, 730), "can't obey them all", 60, c3)
        text(d, (1600, 810), '(the 4th note handed back)', 52, GREY if step == 3 else DONE)
    if step >= 4:
        rows = ('notes = sizes', 'shelf = the bottom', '4th note = the size we typed', 'handed back = refused')
        for i, t in enumerate(rows[:3]):
            text(d, (140, 1170 + i * 80), t, 56, BLUE if step == 4 else DONE)
        text(d, (1600, 1170), rows[3], 56, BLUE if step == 4 else DONE)
    if step >= 5:
        text(d, (1600, 1250), 'carpenter = the solver:', 56, BLUE)
        text(d, (1600, 1330), 'moves lines until all agree', 52, BLUE)
    save(im, f'card-carpenter-{step}.png')


# --- F4: decode (right half) ------------------------------------------------------------------------------------------
DECODE = [  # one step about every 8 s, in the spoken order (SCRIPT F4)
    ('each line can slide and turn',),
    ('degrees of freedom left: none',),
    ("arm's top = 25 - 5 - 5 = 15",),
    ('new size 17: two orders, one line', '= over-constrained'),
    ("datum = FreeCAD's word", "for a size's number"),
    ("negative = FreeCAD's wording", 'for this clash', '(nothing typed is negative)'),
    ("index 23 = the new size's number", '(rules 0 to 22 were there)'),
]


def card_decode(step):
    box = (SIDE_X, 60, 2540, 1380)
    im, d = panel(box)
    k = lambda n: A(INK if step == n else DONE)    # noqa: E731
    s = 5.2
    x0, y0 = 1900, 440
    col = INK if step <= 2 else DONE
    pts = hook(d, x0, y0, s, col, width=6, arm=(ORANGE if step == 3 else (RED if step == 4 else None)) if step >= 3
               else None)
    if step == 1:
        for p in pts[:-1:2]:      # small arrows: each line can slide
            d.line((p[0] - 30, p[1] + 26, p[0] + 30, p[1] + 26), fill=A(BLUE), width=5)
    if step >= 3:
        a, b = pts[4], pts[5]
        text(d, ((a[0] + b[0]) / 2, a[1] - 14), '15', 46, k(3), anchor='md', box=box)
    if step >= 4:
        a, b = pts[4], pts[5]
        text(d, (a[0] + 20, a[1] + 40), '17', 46, A(RED) if step == 4 else A(DONE), anchor='lt', box=box)
    y = 520
    for i, lines in enumerate(DECODE[:step]):
        for j, ln in enumerate(lines):
            c = k(i + 1)
            if i == 3 and step == 4:
                c = A(RED)
            size = 48 if j == 0 else 46
            text(d, (SIDE_X + 50, y), ln, size, c, box=box, maxw=1040)
            y += 58
        y += 14
    save(im, f'card-decode-{step}.png')


# --- F8: so far -------------------------------------------------------------------------------------------------------
def card_sofar(step):
    """SCRIPT F8: 1 the four notes, the fourth crossed out, "one order too many"; 2 the shelf note 25 to 27, "change the
    size that sets it"; 3 a note stamped "for information", "or add it as a Reference"."""
    im, d = canvas()
    header(d, 'So far')
    c1 = ORANGE if step == 1 else DONE
    note(d, 200, 300, 'shelf 25', INK if step == 1 else DONE, cross=step >= 2)
    note(d, 200, 460, 'lip 5', INK if step == 1 else DONE)
    note(d, 200, 620, 'back 5', INK if step == 1 else DONE)
    note(d, 200, 780, 'arm 17', c1, fill=ORANGEFILL if step == 1 else DONEFILL, cross=True)
    text(d, (1100, 360), 'one order too many', 72, c1)
    if step >= 2:
        c2 = BLUE if step == 2 else DONE
        note(d, 640, 300, 'shelf 27', c2, fill=BLUEFILL if step == 2 else DONEFILL)
        text(d, (1100, 600), 'change the size that sets it', 72, c2)
    if step >= 3:
        c3 = BLUE
        note(d, 200, 1000, 'arm 17', c3, fill=WHITE, w=420)
        d.rectangle((660, 1010, 1000, 1110), outline=GREEN, width=7)
        text(d, (830, 1060), 'for information', 46, GREEN, anchor='mm')
        text(d, (1100, 1060), 'or add it as a Reference', 72, c3, anchor='lm')
    save(im, f'card-sofar-{step}.png')


# --- F10 --------------------------------------------------------------------------------------------------------------
RECIPE = [('1. XY sketch: rectangle 40 x 20', 'at the origin'), ('2. Size the bottom 40', 'and a side 20'),
          ('3. Size the top 41:', 'refused?'), ('4. Again, Reference ticked:', '(40 mm)'),
          ('5. Pad 10; console:', 'about 8000')]


def card_recipe(step):
    """F10's recipe as a side panel (the E recording plays on the left): one line per spoken clause."""
    box = (SIDE_X, 80, 2540, 1360)
    im, d = panel(box)
    text(d, (SIDE_X + 50, 130), 'Your turn', 64, A(INK), box=box)
    y = 250
    for i, lines in enumerate(RECIPE[:step]):
        for ln in lines:
            text(d, (SIDE_X + 50, y), ln, 52, A(INK if i + 1 == step else DONE), box=box, maxw=1020)
            y += 66
        y += 34
    text(d, (SIDE_X + 50, 1230), 'new to this? FreeCAD course,', 44, A(GREY), box=box)
    text(d, (SIDE_X + 50, 1288), 'lesson 2', 44, A(GREY), box=box)
    save(im, f'card-recipe-{step}.png')


def card_question(step):
    box = (SIDE_X, 140, 2540, 1300)
    im, d = panel(box)
    text(d, (1985, 300), 'Arm top sized 15', 64, A(INK), anchor='mm', box=box)
    text(d, (1985, 390), '(it already is): OK?', 64, A(INK), anchor='mm', box=box)
    pts = hook(d, 1870, 1060, 9, DONE, arm=ORANGE)
    a, b = pts[4], pts[5]
    text(d, ((a[0] + b[0]) / 2, a[1] - 16), '15?', 56, A(ORANGE), anchor='md', box=box)
    if step >= 2:
        text(d, (1985, 1180), 'Pause and think', 64, A(BLUE), anchor='mm', box=box)
    save(im, f'card-question-{step}.png')


def card_end():
    """The end card (F11, ~5 s): room on the right for YouTube's end-screen elements. Light, no 'next' wording, no
    AI-voice text (nf-disclose burns that label)."""
    im, d = canvas()
    text(d, (160, 260), 'Fix-it: exact errors, exact fixes', 72, INK)
    text(d, (160, 380), 'FreeCAD 1.1.4, filmed on Linux', 52, GREY)
    text(d, (160, 560), 'The Fix-it before this one:', 56, INK)
    text(d, (160, 640), 'Wire is not closed, the same hook', 56, BLUE)
    text(d, (160, 800), 'FreeCAD course, lesson 3:', 56, INK)
    text(d, (160, 880), 'the sizes that drive the part', 56, BLUE)
    text(d, (160, 1040), 'The answer: in the pinned comment', 56, INK)
    text(d, (160, 1200), 'Subscribe: every error reproduced', 52, GREY)
    text(d, (160, 1270), 'on screen', 52, GREY)
    save(im, 'card-end.png')


# --- source overlays (2880 x 1800) ------------------------------------------------------------------------------------
def _ov(name, box, label=None):
    im, d = source()
    x, y, w, h = box
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=WHITE + (255,))
    if label:
        text(d, (40, y + h - 60 if h > 200 else y + h / 2), label, 44, GREY + (255,), anchor='lm', frame=(SW, SH))
    save(im, name)


def ov_a_rep():
    """Take A's Report view dock as a plain light panel, no text (used only under the popup close-ups, so FreeCAD's own
    red lines are never cut at the close-up's edge; the F4 Report view zoom uses raw A)."""
    im, d = source()
    x, y, w, h = A_REP
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=DOCK_FILL + (255,))
    save(im, 'ov-a-rep.png')


def short_stack():
    """The Short's frame 1: top, A/popup.png: the hook's bottom (1.1x) over the popup's whole line (x 830-1905, 1:1);
    bottom, B/green.png: the hook's bottom with "27 mm" (x 1760-2120, y 1290-1570, 1.3x) beside "Fully constrained"."""
    CUR.clear()
    im = Image.new('RGB', (1080, 960), WHITE)
    d = ImageDraw.Draw(im)
    a = Image.open(os.path.join(TAKES, 'A', 'popup.png')).convert('RGB')
    im.paste(a.crop((1380, 960, 1940, 1290)).resize((504, 297), Image.LANCZOS), (288, 86))
    im.paste(a.crop((830, 1672, 1905, 1758)), (2, 390))
    d.rectangle((0, 0, 1080, 76), fill=WHITE)
    text(d, (540, 40), '17 MM: REFUSED', 48, RED, anchor='mm', frame=(1080, 960))
    g = Image.open(os.path.join(TAKES, 'B', 'green.png')).convert('RGB')
    hk = g.crop((1760, 1290, 2120, 1570)).resize((468, 364), Image.LANCZOS)
    im.paste(hk, (40, 560))
    fc = g.crop((2200, 720, 2640, 785)).resize((572, 85), Image.LANCZOS)
    im.paste(fc, (500, 700))
    d.rectangle((0, 480, 1080, 556), fill=WHITE)
    text(d, (540, 520), 'ARM 17: FIXED', 48, GREEN, anchor='mm', frame=(1080, 960))
    d.line((0, 480, 1080, 480), fill=INK, width=6)
    save(im, 'short-stack.png')


def sheet(outdir):
    names = sorted(n for n in os.listdir(OUT) if n.startswith('card-'))
    tw, th, cols = 640, 360, 3
    rows = -(-len(names) // cols)
    sh = Image.new('RGB', (tw * cols, (th + 30) * rows), (90, 90, 90))
    dd = ImageDraw.Draw(sh)
    for i, n in enumerate(names):
        im = Image.open(os.path.join(OUT, n)).convert('RGBA')
        bg = Image.new('RGBA', im.size, (60, 70, 85, 255))
        t = Image.alpha_composite(bg, im).convert('RGB').resize((tw - 8, th - 8))
        x, y = (i % cols) * tw, (i // cols) * (th + 30)
        sh.paste(t, (x + 4, y + 4))
        dd.text((x + 6, y + th), n, font=font(R, 22), fill=(255, 255, 255))
    sh.save(os.path.join(outdir, 'cards-sheet-fx20.jpg'), quality=85)
    sh = Image.new('RGB', (1920, 600), (90, 90, 90))
    r1 = Image.open(os.path.join(TAKES, 'runs', 'R1', 'before.png')).convert('RGBA')
    for n in ('ov-r1-top.png', 'ov-r1-hint.png', 'ov-r1-try.png'):
        r1 = Image.alpha_composite(r1, Image.open(os.path.join(OUT, n)))
    sh.paste(r1.convert('RGB').resize((960, 600)), (0, 0))
    sh.paste(Image.open(os.path.join(OUT, 'short-stack.png')).convert('RGB').resize((675, 600)), (1000, 0))
    sh.save(os.path.join(outdir, 'overlays-sheet-fx20.jpg'), quality=85)


def check_alpha():
    for n in sorted(os.listdir(OUT)):
        if n.startswith(('card-decode', 'card-question', 'card-recipe')):
            im = Image.open(os.path.join(OUT, n))
            if im.mode != 'RGBA' or im.crop((0, 0, SIDE_X, H)).getchannel('A').getextrema() != (0, 0):
                PROBLEMS.append(f'{n}: not transparent left of {SIDE_X}')


def main():
    os.makedirs(OUT, exist_ok=True)
    PROBLEMS.clear()
    LOG.clear()
    for s in (1, 2, 3, 4, 5):
        card_carpenter(s)
    for s in (1, 2, 3):
        card_sofar(s)
    for s in range(1, 8):
        card_decode(s)
    for s in range(1, 6):
        card_recipe(s)
    for s in (1, 2):
        card_question(s)
    card_end()
    _ov('ov-r1-top.png', R1_TOP, "(Claude Code's start screen, hidden)")
    _ov('ov-r1-odes.png', R1_ODES)
    _ov('ov-r1-hint.png', R1_HINT, '(hint line, hidden)')
    _ov('ov-r1-try.png', R1_TRY, '(greyed suggestion, hidden)')
    ov_a_rep()
    short_stack()
    check_alpha()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
