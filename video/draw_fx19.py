"""Fix-it fx19 cards (FreeCAD 1.1 Pad: "Wire is not closed."; one corner of the sketch does not join), the
solidcraft-course-lab draw_fx15.py pattern with its helpers copied in (no import across labs): light, 2560 x 1440,
clean line diagrams (the fence is the one analogy, line art too), each step adds, earlier steps stay and turn grey.
Text 44 px+, 44 columns at most per line. SCRIPT-fx19.md rev 2 section 4.
  full frame (RGB):  card-fence-1..4 (F3: posts and panels, no rails), card-sofar-1..4 (F8),
                     card-end (F11)
  side panels (RGBA, transparent left of SIDE_X): card-recipe-1..4 (F10), card-decode-1..4 (F4: the hook's 8 lines, the 0.5 mm gap drawn
                     wide and labelled, no fill, Coincident + the grey "also reported" line), card-question-1..2 (F10,
                     asked, never answered)
  source overlays (RGBA, 2880 x 1800; burnt into derived takes by footage-fx19.py):
      ov-r1-top (R1 before 23.4 s: Claude Code's start screen, the banner with the account plan name, covered whole:
      left pane x 0-1160, y 0-850; says so), ov-r1-hint (R1 from 22.5 s: the tmux hint and the greyed suggested prompt
      rows covered; says so), ov-r1-try (R1 0-2.15 s: the input row's greyed placeholder, before the prompt is typed), ov-dock (takes B and C: the Report view dock, plain light panel, no text: the lab's
      "Python code executed successfully." lines)
  short-stack.png: the Short's frame 1 (1080 x 960): A/refusal.png (the box) over B/padded.png (the hook built).
The F5 check, F9 plug / tool log / check cards are burnt in as labels by footage-fx19.py (no PNG; the fx13 precedent).
Run in the draw image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fx19.py [sheet OUTDIR]
Test: tests/test_draw_fx19.py"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-fx19')
TAKES = os.path.join(LAB, 'out', 'fx19')
FD = '/usr/share/fonts/truetype/dejavu/'
B, R = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf'
W, H = 2560, 1440
SW, SH = 2880, 1800
INK, GREY = (31, 41, 55), (110, 120, 138)
WHITE, PANEL = (255, 255, 255), (250, 251, 253)
DONE, DONEFILL = (160, 167, 178), (244, 246, 248)
BLUE, BLUEFILL = (37, 99, 235), (219, 234, 254)
ORANGE, ORANGEFILL = (234, 88, 12), (255, 237, 213)
GREEN = (21, 128, 61)
WATER = (147, 197, 253)
GRASS = (220, 237, 200)
MIN_PX = 44
PROBLEMS = []
LOG = {}
CUR = []
SIDE_X = 1430
# the course hook (mm), lab G0/g0a.txt: line 0 starts at (0, 0); the closing line 7 ends at (0, 0.5) in hook-gap
HOOK = [(0, 0), (25, 0), (25, 10), (20, 10), (20, 5), (5, 5), (5, 60), (0, 60), (0, 0)]
R1_TOP = (0, 0, 1160, 850)          # R1 0-23.4 s: the start screen (banner, plan name, notices) above the prompt row
R1_HINT = (0, 1540, 1160, 165)      # R1 22.5+: "tmux focus-events off ..." (y ~1565) + "Reverse the pad direction" (y ~1665)
R1_TRY = (0, 1635, 1160, 65)        # R1 0-2.15 s: the input row's greyed placeholder suggestion (y ~1665)
DOCK = (0, 1392, 2880, 372)         # B, C: the Report view dock (header y ~1400, lines to ~1760)
DOCK_FILL = (248, 248, 248)


# --- drawing helpers (copied from solidcraft-course-lab video/draw_fx11.py) ------------------------------------------
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


# --- the hook outline (F4, F8) ---------------------------------------------------------------------------------------
def hook_pts(x0, y0, s, gap=0.0):
    """The hook's 9 points on screen (y up in mm, down on screen); the last point raised by `gap` mm (drawn, not to
    scale: the card says 0.5 mm)."""
    pts = [(x0 + x * s, y0 - y * s) for x, y in HOOK]
    pts[-1] = (pts[-1][0], pts[-1][1] - gap * s)
    return pts


def hook(d, x0, y0, s, col, gap=0.0, fill=None, width=7, alpha=True):
    pts = hook_pts(x0, y0, s, gap)
    if fill:
        d.polygon(pts[:-1], fill=A(fill, alpha))
    d.line(pts, fill=A(col, alpha), width=width, joint='curve')
    for p in pts[:-1]:
        d.ellipse((p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9), fill=A(col, alpha))
    return pts


# --- F3: the fence ---------------------------------------------------------------------------------------------------
def fence(d, cx, cy, rw, rh, col, gap=False, water=False):
    """A fenced field seen from above: posts (dots) joined by straight panels; one panel missing when gap."""
    posts = []
    n = 5
    for i in range(n):
        posts.append((cx - rw + 2 * rw * i / (n - 1), cy - rh))
    for i in range(1, 3):
        posts.append((cx + rw, cy - rh + 2 * rh * i / 3))
    for i in range(n):
        posts.append((cx + rw - 2 * rw * i / (n - 1), cy + rh))
    for i in range(1, 3):
        posts.append((cx - rw, cy + rh - 2 * rh * i / 3))
    if water:
        d.rectangle((cx - rw, cy - rh, cx + rw, cy + rh), fill=WATER)
    else:
        d.rectangle((cx - rw, cy - rh, cx + rw, cy + rh), fill=GRASS)
    k = len(posts)
    missing = 5 if gap else -1
    for i in range(k):
        if i == missing:
            continue
        a, b = posts[i], posts[(i + 1) % k]
        d.line((a, b), fill=col, width=12)
    for p in posts:
        d.rectangle((p[0] - 16, p[1] - 16, p[0] + 16, p[1] + 16), fill=col)
    return posts, missing


def card_fence(step):
    im, d = canvas()
    header(d, 'A fence around a field you want to flood')
    cx, cy, rw, rh = 760, 760, 520, 340
    k = lambda n: INK if step == n else DONE    # noqa: E731
    fence(d, cx, cy, rw, rh, INK if step == 1 else DONE, water=True)
    text(d, (cx, cy + rh + 90), 'every post joined: it fills', 56, k(1), anchor='mm')
    if step >= 2:
        cx2 = 1720
        posts, miss = fence(d, cx2, cy, 380, rh, INK if step == 2 else DONE, gap=True)
        a, b = posts[miss], posts[(miss + 1) % len(posts)]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        for j in range(4):    # water running out through the gap
            d.line((mx + 10, my + 40 * j - 60, mx + 150 + 50 * j, my + 40 * j - 30), fill=BLUE, width=10)
        d.ellipse((mx - 34, my - 34, mx + 34, my + 34), outline=ORANGE, width=8)
        text(d, (cx2, cy + rh + 90), 'one gap: the water runs out', 56, ORANGE if step == 2 else DONE, anchor='mm')
    if step >= 3:
        text(d, (180, 1300), 'fence = lines   posts = end points', 60, BLUE if step == 3 else DONE, anchor='lm')
    if step >= 4:
        text(d, (1500, 1300), 'field = face', 60, BLUE, anchor='lm')
    save(im, f'card-fence-{step}.png')


# --- F4: decode (right half) ----------------------------------------------------------------------------------------
def card_decode(step):
    box = (SIDE_X, 120, 2540, 1320)
    im, d = panel(box)
    x = SIDE_X + 50
    k = lambda n: A(INK if step == n else DONE)    # noqa: E731
    s = 11
    x0, y0 = 1560, 1080
    text(d, (x, 170), 'wire = the chain of lines', 52, k(1), box=box)
    if step == 1:
        hook(d, x0, y0, s, INK)
    else:
        pts = hook(d, x0, y0, s, DONE if step >= 3 else INK, gap=2.0)
        end, start = pts[-1], pts[0]
        d.ellipse((start[0] - 40, start[1] - 46, start[0] + 40, start[1] + 20), outline=A(ORANGE), width=7)
        text(d, (start[0] - 20, start[1] + 50), 'gap 0.5 mm', 52, A(ORANGE if step == 2 else DONE), anchor='la',
             box=box)
        text(d, (start[0] - 20, start[1] + 110), '(drawn wider)', 44, A(GREY), anchor='la', box=box)
    if step >= 3:
        text(d, (1950, 300), 'not closed:', 52, k(3), box=box)
        text(d, (1950, 365), 'no closed loop,', 52, k(3), box=box)
        text(d, (1950, 430), 'no face', 52, k(3), box=box)
    if step >= 4:
        text(d, (1950, 560), 'Coincident =', 52, A(BLUE), box=box)
        text(d, (1950, 625), 'keeps the ends', 52, A(BLUE), box=box)
        text(d, (1950, 690), 'together', 52, A(BLUE), box=box)
        for i, ln in enumerate(('Also reported,', 'not filmed: two', 'lines drawn on top', 'of each other')):
            text(d, (1950, 860 + i * 58), ln, 44, A(GREY), box=box)
    save(im, f'card-decode-{step}.png')


# --- F8: so far -----------------------------------------------------------------------------------------------------
def card_sofar(step):
    """In the spoken order (SCRIPT F8): 1 closed fence: Pad fills it; 2 one gap: no face; 3 Validate marks the two
    loose ends, Coincident joins them; 4 Polyline: watch the sign."""
    im, d = canvas()
    header(d, 'So far')
    s = 15
    x0, y0 = 300, 1250
    if step == 1:
        hook(d, x0, y0, s, BLUE, fill=BLUEFILL, width=9, alpha=False)
    else:
        hook(d, x0, y0, s, ORANGE if step == 2 else DONE, gap=2.0, width=9, alpha=False)
    if step == 2:
        d.ellipse((x0 - 50, y0 - 75, x0 + 50, y0 + 25), outline=ORANGE, width=8)
    if step >= 3:
        for (px, py) in ((x0, y0), (x0, y0 - 2 * s)):
            d.rectangle((px - 22, py - 22, px + 22, py + 22), outline=ORANGE if step == 3 else DONE, width=7)
    rows = [('closed fence of lines: Pad fills it', BLUE), ('one gap: no face, Pad refuses', ORANGE),
            ('Validate Sketch marks 2 loose ends;', BLUE), ('Polyline: watch the sign', BLUE)]
    for i, (t, c) in enumerate(rows[:step]):
        text(d, (1000, 360 + i * 230), t, 64, c if i + 1 == step else DONE)
    if step >= 3:
        text(d, (1000, 360 + 2 * 230 + 80), 'Coincident joins them', 64, BLUE if step == 3 else DONE)
    save(im, f'card-sofar-{step}.png')


# --- F10 ------------------------------------------------------------------------------------------------------------
RECIPE = [('0. New sketch on XY:', 'rectangle 30 x 20'), ('1. Click a corner, Delete,', 'drag the end'),
          ('2. Close; Validate;', 'join with C; Pad 10'), ('3. Console: 6,000 mm3?',)]


def card_recipe(step):
    """F10's recipe as a side panel (the E recording plays on the left): one line per spoken clause."""
    box = (SIDE_X, 120, 2540, 1320)
    im, d = panel(box)
    text(d, (SIDE_X + 50, 170), 'Your turn', 64, A(INK), box=box)
    y = 300
    for i, lines in enumerate(RECIPE[:step]):
        for ln in lines:
            text(d, (SIDE_X + 50, y), ln, 56, A(INK if i + 1 == step else DONE), box=box, maxw=1020)
            y += 72
        y += 50
    text(d, (SIDE_X + 50, 1180), 'new to this? FreeCAD course,', 44, A(GREY), box=box)
    text(d, (SIDE_X + 50, 1240), 'lesson 2', 44, A(GREY), box=box)
    save(im, f'card-recipe-{step}.png')


def card_question(step):
    box = (SIDE_X, 140, 2540, 1300)
    im, d = panel(box)
    k1 = A(INK)
    text(d, (1985, 300), 'Ends on one spot,', 60, k1, anchor='mm', box=box)
    text(d, (1985, 390), 'no Coincident: Pad?', 60, k1, anchor='mm', box=box)
    hook(d, 1880, 1060, 9, DONE)
    text(d, (1880 + 40, 1060 - 30), '?', 80, A(ORANGE), anchor='lm', box=box)
    if step >= 2:
        text(d, (1985, 1180), 'Pause and think', 64, A(BLUE), anchor='mm', box=box)
    save(im, f'card-question-{step}.png')


def card_end():
    """The end card (F11, ~5 s): room on the right for YouTube's end-screen elements. Light, no 'next' wording, no
    AI-voice text (nf-disclose burns that label)."""
    im, d = canvas()
    text(d, (160, 300), 'Fix-it: exact errors, exact fixes', 72, INK)
    text(d, (160, 420), 'FreeCAD 1.1.4, filmed on Linux', 52, GREY)
    text(d, (160, 620), 'FreeCAD course, lesson 2:', 56, INK)
    text(d, (160, 700), 'this hook, drawn step by step', 56, BLUE)
    text(d, (160, 900), 'The answer: in the pinned comment', 56, INK)
    text(d, (160, 1100), 'Subscribe: every error reproduced', 52, GREY)
    text(d, (160, 1170), 'on screen', 52, GREY)
    save(im, 'card-end.png')


# --- source overlays (2880 x 1800) -----------------------------------------------------------------------------------
def ov_r1_top():
    im, d = source()
    x, y, w, h = R1_TOP
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=WHITE + (255,))
    text(d, (40, h - 80), "(Claude Code's start screen, hidden)", 44, GREY + (255,), anchor='lm', frame=(SW, SH))
    save(im, 'ov-r1-top.png')


def ov_r1_hint():
    im, d = source()
    x, y, w, h = R1_HINT
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=WHITE + (255,))
    text(d, (40, y + h / 2), '(hint + greyed suggestion, hidden)', 44, GREY + (255,), anchor='lm', frame=(SW, SH))
    save(im, 'ov-r1-hint.png')


def ov_r1_try():
    im, d = source()
    x, y, w, h = R1_TRY
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=WHITE + (255,))
    text(d, (40, y + h / 2), '(greyed suggestion, hidden)', 44, GREY + (255,), anchor='lm', frame=(SW, SH))
    save(im, 'ov-r1-try.png')


def ov_dock():
    im, d = source()
    x, y, w, h = DOCK
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=DOCK_FILL + (255,))
    save(im, 'ov-dock.png')


STACK_A = (900, 700, 1800, 1050)       # A/refusal.png: the box "Input error" / "Wire is not closed." (x 1260-1620)
STACK_B = (1100, 200, 2300, 1350)      # B/padded.png: the hook built, isometric


def short_stack():
    CUR.clear()
    im = Image.new('RGB', (1080, 960), WHITE)
    d = ImageDraw.Draw(im)
    for k, (png, crop, lab, col) in enumerate((('A/refusal.png', STACK_A, 'PAD: REFUSED', (185, 28, 28)),
                                                ('B/padded.png', STACK_B, 'ONE JOIN: BUILT', BLUE))):
        y0 = k * 480
        fr = Image.open(os.path.join(TAKES, png)).convert('RGB').crop(crop)
        fr.thumbnail((1080, 410), Image.LANCZOS)
        im.paste(fr, ((1080 - fr.width) // 2, y0 + 70))
        d.rectangle((0, y0, 1080, y0 + 70), fill=WHITE)
        text(d, (540, y0 + 36), lab, 44, col, anchor='mm', frame=(1080, 960))
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
    sh.save(os.path.join(outdir, 'cards-sheet-fx19.jpg'), quality=85)
    tw, th = 960, 600
    sh = Image.new('RGB', (tw * 2, th * 2), (90, 90, 90))
    r1 = Image.open(os.path.join(TAKES, 'runs', 'R1', 'before.png')).convert('RGBA')
    sh.paste(Image.alpha_composite(r1, Image.open(os.path.join(OUT, 'ov-r1-top.png'))).convert('RGB').resize((tw, th)),
             (0, 0))
    b = Image.open(os.path.join(TAKES, 'B', 'joined.png')).convert('RGBA')
    sh.paste(Image.alpha_composite(b, Image.open(os.path.join(OUT, 'ov-dock.png'))).convert('RGB').resize((tw, th)),
             (tw, 0))
    sh.paste(Image.open(os.path.join(OUT, 'short-stack.png')).convert('RGB').resize((675, th)), (0, th))
    sh.save(os.path.join(outdir, 'overlays-sheet-fx19.jpg'), quality=85)


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
    for s in (1, 2, 3, 4):
        card_fence(s)
    for s in (1, 2, 3, 4):
        card_sofar(s)
        card_decode(s)
        card_recipe(s)
    for s in (1, 2):
        card_question(s)
    card_end()
    ov_r1_top()
    ov_r1_hint()
    ov_r1_try()
    ov_dock()
    short_stack()
    check_alpha()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
