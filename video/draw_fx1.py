"""Fix-it fx1 cards (FreeCAD 1.1 reads v1-1/Mod), white, 2560 x 1440, text 52 px or more.
  card-drawer-1..6  the tool-cabinet analogy (old FreeCAD/Mod drawer, new v1-1 drawer, the name rule, the first-start
                    question on an old machine, the old guide, "the files are there; FreeCAD never looks")
  card-paths        the four v1-1/Mod paths (Linux as filmed; the others from the project's docs)
  card-sofar-1..3, card-box-1..4, card-recap-1..3, card-quiz, card-ans-1..3, card-outro-1..2, card-short-q
Every value comes from out/fx1 (ANSWERS.md). Runs on the host or in any image with Pillow:
    python video/draw_fx1.py"""
import os

from PIL import Image, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-fx1')
os.makedirs(OUT, exist_ok=True)
W, H = 2560, 1440


def _pick(*names):
    for n in names:
        if os.path.exists(n):
            return n
    raise SystemExit('no font: ' + names[0])


DJ = '/usr/share/fonts/truetype/dejavu/'
WF = 'C:/Windows/Fonts/'
B = _pick(DJ + 'DejaVuSans-Bold.ttf', WF + 'arialbd.ttf')
R = _pick(DJ + 'DejaVuSans.ttf', WF + 'arial.ttf')
MONO = _pick(DJ + 'DejaVuSansMono.ttf', WF + 'consola.ttf')
MONOB = _pick(DJ + 'DejaVuSansMono-Bold.ttf', WF + 'consolab.ttf', WF + 'consola.ttf')
WHITE, INK, GREY, RED, GREEN, BLUE = (255, 255, 255), (31, 41, 55), (110, 120, 138), (183, 28, 28), (27, 127, 59), (29, 78, 216)
AMBER, AMBER_BG, GREEN_BG, LIGHT, FAINT = (180, 110, 0), (253, 236, 214), (221, 240, 227), (241, 245, 249), (205, 211, 220)
WOOD, WOOD_D, DUST = (214, 186, 140), (150, 118, 76), (196, 190, 180)


def font(p, s):
    return ImageFont.truetype(p, s)


def canvas():
    im = Image.new('RGB', (W, H), WHITE)
    return im, ImageDraw.Draw(im)


def text(d, xy, s, size=72, fill=INK, path=B, anchor='la'):
    d.text(xy, s, font=font(path, size), fill=fill, anchor=anchor)


def header(d, s):
    text(d, (W / 2, 110), s, 92, anchor='mm')


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(name)


def box(d, x0, y0, x1, y1, fill=LIGHT, outline=INK, w=6):
    d.rounded_rectangle((x0, y0, x1, y1), radius=26, fill=fill, outline=outline, width=w)


def cross(d, cx, cy, s=70, col=RED):
    d.line((cx - s, cy - s, cx + s, cy + s), fill=col, width=18)
    d.line((cx - s, cy + s, cx + s, cy - s), fill=col, width=18)


def arrow(d, x0, y0, x1, y1, col=INK, w=12):
    import math
    d.line((x0, y0, x1, y1), fill=col, width=w)
    a = math.atan2(y1 - y0, x1 - x0)
    for s in (2.6, -2.6):
        d.line((x1, y1, x1 + 50 * math.cos(a + s), y1 + 50 * math.sin(a + s)), fill=col, width=w)


def dots(d, step, n, y=1360):
    for k in range(n):
        x = W / 2 + (k - (n - 1) / 2) * 90
        d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=INK if k < step else FAINT)


# ---------------- the cabinet ----------------
def cabinet(d, open_new=False, old_dust=True, addon_old=False, hand=False):
    """A cabinet at the left-centre: top drawer = old FreeCAD/Mod, bottom drawer = v1-1."""
    x0, x1 = 420, 1500
    d.rectangle((x0 - 30, 300, x1 + 30, 1220), fill=WOOD_D)
    # old drawer
    d.rectangle((x0, 330, x1, 740), fill=DUST if old_dust else WOOD, outline=WOOD_D, width=8)
    text(d, ((x0 + x1) / 2, 470), 'FreeCAD/Mod', 84, INK, MONOB, 'mm')
    text(d, ((x0 + x1) / 2, 590), 'the old drawer', 56, GREY, R, 'mm')
    d.rounded_rectangle(((x0 + x1) / 2 - 90, 650, (x0 + x1) / 2 + 90, 690), radius=12, fill=WOOD_D)
    # new drawer (pulled out to the right when open)
    dx = 260 if open_new else 0
    d.rectangle((x0 + dx, 780, x1 + dx, 1190), fill=WOOD, outline=WOOD_D, width=8)
    text(d, ((x0 + x1) / 2 + dx, 920), 'v1-1', 110, BLUE, MONOB, 'mm')
    text(d, ((x0 + x1) / 2 + dx, 1050), 'the new drawer', 56, INK, R, 'mm')
    d.rounded_rectangle(((x0 + x1) / 2 + dx - 90, 1110, (x0 + x1) / 2 + dx + 90, 1150), radius=12, fill=WOOD_D)
    if addon_old:
        box(d, 1060, 600, 1480, 720, fill=AMBER_BG, outline=AMBER, w=5)
        text(d, (1270, 660), 'FreeCADMCP', 60, AMBER, MONOB, 'mm')
    if hand:
        # FreeCAD's hand: a blue pointer on the new drawer's handle
        hx, hy = x1 + dx - 260, 1280
        d.ellipse((hx, hy - 60, hx + 120, hy + 60), fill=BLUE)
        text(d, (hx + 160, hy), 'FreeCAD 1.1', 60, BLUE, B, 'lm')


def card_drawer(step):
    im, d = canvas()
    header(d, 'One drawer per FreeCAD version')
    if step == 1:
        cabinet(d)
        text(d, (1700, 560), 'your files live', 64, INK, B, 'la')
        text(d, (1700, 650), 'in one of these', 64, INK, B, 'la')
        text(d, (1700, 820), 'Mod = the folder', 58, GREY, R, 'la')
        text(d, (1700, 900), 'that holds add-ons', 58, GREY, R, 'la')
    elif step == 2:
        cabinet(d)
        parts = [('v', INK), ('1', BLUE), ('-', INK), ('1', GREEN)]
        x = 1680
        for s, c in parts:
            text(d, (x, 640), s, 200, c, MONOB, 'lm')
            x += 150
        text(d, (1680 + 150 + 60, 800), 'major', 54, BLUE, B, 'mm')
        text(d, (1680 + 450 + 60, 800), 'minor', 54, GREEN, B, 'mm')
        text(d, (1680, 960), '1.1 = major 1, minor 1', 60, INK, B, 'la')
        text(d, (1680, 1060), 'FreeCAD 1.1  ->  v1-1', 64, INK, MONOB, 'la')
        text(d, (1680, 1150), "(the rule in FreeCAD's code)", 50, GREY, R, 'la')
    elif step == 3:
        cabinet(d, open_new=True, hand=True)
        text(d, (1830, 520), '1.1 opens', 72, INK, B, 'la')
        text(d, (1830, 610), 'this one', 72, INK, B, 'la')
        arrow(d, 1950, 680, 1950, 820, BLUE)
    elif step == 4:
        cabinet(d)
        box(d, 1580, 330, 2500, 1100, fill=WHITE, outline=INK)
        text(d, (2040, 400), 'a computer that ran', 54, INK, B, 'mm')
        text(d, (2040, 470), 'an older FreeCAD:', 54, INK, B, 'mm')
        text(d, (2040, 580), 'first start of 1.1 asks', 52, GREY, R, 'mm')
        text(d, (2040, 690), 'Welcome to FreeCAD 1.1', 52, INK, B, 'mm')
        box(d, 1660, 770, 2420, 880, fill=(0, 120, 212), outline=(0, 90, 170), w=4)
        text(d, (2040, 825), 'Copy Configuration (Recommended)', 40, WHITE, B, 'mm')
        text(d, (2040, 980), 'old settings -> new drawer', 50, GREY, R, 'mm')
        text(d, (2040, 1050), 'the old drawer stays', 50, GREY, R, 'mm')
    elif step == 5:
        cabinet(d)
        box(d, 1700, 330, 2460, 900, fill=(250, 248, 240), outline=GREY)
        text(d, (2080, 400), 'an older guide', 60, GREY, B, 'mm')
        for k in range(4):
            d.line((1780, 490 + k * 70, 2380, 490 + k * 70), fill=FAINT, width=14)
        text(d, (2080, 800), 'copy to FreeCAD/Mod', 52, INK, MONOB, 'mm')
        arrow(d, 1700, 700, 1520, 540, AMBER)
        text(d, (2080, 1020), 'the old drawer still exists', 54, AMBER, B, 'mm')
    elif step == 6:
        cabinet(d, open_new=True, addon_old=True, hand=True)
        text(d, (2030, 520), 'the files are there;', 64, RED, B, 'mm')
        text(d, (2030, 610), 'FreeCAD never looks', 64, RED, B, 'mm')
    save(im, f'card-drawer-{step}.png')


def card_paths(n=4):
    im, d = canvas()
    header(d, 'The same v1-1/Mod, four places')
    rows = [('Linux AppImage (filmed here):', '~/.local/share/FreeCAD/v1-1/Mod'),
            ('Windows:', '%APPDATA%\\FreeCAD\\v1-1\\Mod'),
            ('macOS:', '~/Library/Application Support/FreeCAD/v1-1/Mod'),
            ('Flatpak:', '~/.var/app/org.freecad.FreeCAD/data/FreeCAD/v1-1/Mod')]
    for k, (a, b) in enumerate(rows[:n]):
        y = 250 + k * 255
        box(d, 120, y, 2440, y + 225, fill=GREEN_BG if k == 0 else LIGHT, outline=GREEN if k == 0 else INK, w=5)
        text(d, (170, y + 60), a, 58, INK, B, 'lm')
        text(d, (170, y + 155), b, 60, BLUE, MONOB, 'lm')
    text(d, (W / 2, 1290), "Linux: as filmed.  Windows: issues #116, #140.  macOS, Flatpak: the project's install page.", 46, GREY, R, 'mm')
    text(d, (W / 2, 1370), 'not filmed: check with the console line', 46, GREY, R, 'mm')
    save(im, f'card-paths-{n}.png')


SOFAR = [('Trap 1: the old drawer.', 'a fresh 1.1 reads v1-1/Mod', INK),
         ('Trap 2: the right drawer,', 'still no MCP Addon', AMBER),
         ('every fix tested on screen,', 'not guessed: Subscribe', BLUE)]


def two_line(step, items, title, name):
    """An incremental build: lines 1..step, the newest one in colour, the earlier ones grey."""
    im, d = canvas()
    header(d, title)
    n = len(items)
    top, gap = 270, (1080 // n)
    for k in range(step):
        a, b, col = items[k]
        y = top + k * gap
        box(d, 160, y, 2400, y + gap - 40, fill=LIGHT if k == step - 1 else WHITE, outline=INK if k == step - 1 else FAINT)
        c = col if k == step - 1 else GREY
        text(d, (1280, y + (gap - 40) * 0.34), a, 76, c, B, 'mm')
        text(d, (1280, y + (gap - 40) * 0.72), b, 70, c, B, 'mm')
    save(im, name)


def drawer_floor(d, boxed):
    d.rectangle((300, 420, 2260, 1160), fill=WOOD, outline=WOOD_D, width=10)
    text(d, (360, 470), 'v1-1/Mod', 70, BLUE, MONOB, 'la')


def card_box(step):
    im, d = canvas()
    header(d, 'FreeCAD looks for boxes')
    drawer_floor(d, step < 3)
    if step in (1, 2):
        lid = 640 if step == 1 else 560
        box(d, 900, 660, 1660, 1080, fill=AMBER_BG, outline=AMBER)
        d.rectangle((880, lid, 1680, lid + 40), fill=AMBER)
        text(d, (1280, 760), 'FreeCADMCP', 72, AMBER, MONOB, 'mm')
        text(d, (1280, 900), 'InitGui.py', 64, INK, MONOB, 'mm')
        text(d, (1280, 1000), 'Init.py  rpc_server ...', 46, GREY, MONO, 'mm')
        if step == 2:
            d.ellipse((1720, 520, 1880, 680), fill=BLUE)
            arrow(d, 1720, 640, 1480, 880, BLUE)
            text(d, (1900, 600), 'reads InitGui.py', 60, BLUE, B, 'lm')
        text(d, (1280, 1290), 'one folder per add-on', 72, INK, B, 'mm')
    else:
        for k, nm in enumerate(['Init.py', 'InitGui.py', 'package.xml', 'rpc_server']):
            x = 520 + k * 430
            y = 980 + (k % 2) * 70
            text(d, (x, y), nm, 54, INK, MONO, 'mm')
        cross(d, 1280, 750, 110)
        text(d, (1280, 1290), 'no FreeCADMCP box' if step == 3 else 'nothing to read', 80, RED, B, 'mm')
    save(im, f'card-box-{step}.png')


RECAP = [('1. the console line:', 'print(App.getUserAppDataDir())', INK),
         ('2. inside that folder:', 'Mod / FreeCADMCP / InitGui.py', INK),
         ('3. restart FreeCAD', 'MCP Addon in the list', GREEN)]

ANS = [("the rule in 1.1's code:", 'v + major + dash + minor (1.1 = v1-1)', INK),
       ('so 1.2 would open v1-2', '(not tested: 1.2 is not out)', BLUE),
       ("check, don't guess:", 'the console line', GREEN)]

OUTRO = [('Next fix: PrusaSlicer says', 'your part seems to be in inches', INK),
         ('FreeCAD course lessons 1 and 7', 'the setup, and the connection step by step', BLUE)]


def card_quiz():
    im, d = canvas()
    header(d, 'Question')
    box(d, 160, 330, 2400, 1050, fill=AMBER_BG, outline=AMBER)
    text(d, (1280, 520), 'Your friend installs FreeCAD 1.2', 84, INK, B, 'mm')
    text(d, (1280, 700), 'Which drawer will it read,', 84, INK, B, 'mm')
    text(d, (1280, 860), 'and how would they check?', 84, INK, B, 'mm')
    text(d, (1280, 1220), 'pause the video and think', 60, GREY, R, 'mm')
    save(im, 'card-quiz.png')
    d.rounded_rectangle((440, 1120, 2120, 1320), radius=30, fill=WHITE, outline=BLUE, width=6)
    text(d, (1280, 1220), 'hint: the drawer rule, v + major + dash + minor', 46, BLUE, B, 'mm')
    save(im, 'card-quiz-2.png')


def card_short_q():
    im = Image.new('RGB', (1080, 700), WHITE)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 40, 1040, 660), radius=30, fill=AMBER_BG, outline=AMBER, width=8)
    for k, s in enumerate(['Which trap did you hit?', 'A) the old drawer', 'B) loose files', 'say it in the comments']):
        text(d, (540, 150 + k * 140), s, 64 if k < 3 else 50, INK if k < 3 else GREY, B if k < 3 else R, 'mm')
    im.save(os.path.join(OUT, 'card-short-q.png'))
    print('card-short-q.png')


if __name__ == '__main__':
    for s in range(1, 7):
        card_drawer(s)
    for n in (1, 2, 3, 4):
        card_paths(n)
    for s in (1, 2, 3):
        two_line(s, SOFAR, 'So far', f'card-sofar-{s}.png')
        two_line(s, RECAP, 'Recap', f'card-recap-{s}.png')
        two_line(s, ANS, 'The answer', f'card-ans-{s}.png')
    for s in (1, 2):
        two_line(s, OUTRO, 'Before you go', f'card-outro-{s}.png')
    for s in (1, 2, 3, 4):
        card_box(s)
    card_quiz()
    card_short_q()
