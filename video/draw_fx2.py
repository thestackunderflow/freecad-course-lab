"""Fix-it fx2 cards (PrusaSlicer "defined in inches"), white, one layout per sequence (nothing moves between builds):
  card-rule-1..3   a 2 mm cube is 8 mm3; the 9 mm3 line (asks below, silent above); our washer at 4.75 mm3 under it
  card-3mf-1..3    a 3MF box with the unit written on it; PrusaSlicer 2.3+: no question; FreeCAD writes millimeter
  card-recap-1..3  the three recap lines, revealed one per clause
Every number comes from out/fx2 (A/volume.txt 4.7500880922277675 mm3; ANSWERS.md).
Run in the QA image:  docker run --rm --network none -v "<lab>:/work" -w /work video-qa:2 python3 video/draw_fx2.py"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw_l2 import B, BLUE, GREEN, GREY, INK, PAPER, R, RED, W, canvas, font, header, text  # noqa: E402

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-fx2')
os.makedirs(OUT, exist_ok=True)
WHITE = (255, 255, 255)
LIGHT = (241, 245, 249)
FAINT = (205, 211, 220)
AMBER = (180, 110, 0)


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(name)


def arrow(d, a, b, col=INK, w=10):
    d.line((a, b), fill=col, width=w)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L = 34
    d.polygon([b, (b[0] - L * math.cos(ang - 0.45), b[1] - L * math.sin(ang - 0.45)),
               (b[0] - L * math.cos(ang + 0.45), b[1] - L * math.sin(ang + 0.45))], fill=col)


def cube(d, cx, cy, s, fill=(176, 190, 212), side=(120, 136, 160), top=(206, 216, 232)):
    """A cube drawn in a simple oblique view, front face s x s."""
    o = s * 0.35
    x0, y0 = cx - s / 2 - o / 2, cy - s / 2 + o / 2
    d.polygon([(x0, y0), (x0 + s, y0), (x0 + s + o, y0 - o), (x0 + o, y0 - o)], fill=top, outline=INK)
    d.polygon([(x0 + s, y0), (x0 + s + o, y0 - o), (x0 + s + o, y0 - o + s), (x0 + s, y0 + s)], fill=side, outline=INK)
    d.rectangle((x0, y0, x0 + s, y0 + s), fill=fill, outline=INK, width=4)


# --- the rule: a bar from 0 to 20 mm3, the 9 line --------------------------------------------------------------
BX0, BX1, BY = 200, 2360, 700           # the bar's left, right, and centre line
def vx(v):
    return BX0 + (BX1 - BX0) * v / 20.0


def bar(d, washer=False, cube8=False):
    d.rounded_rectangle((BX0, BY - 70, vx(9), BY + 70), radius=18, fill=(253, 236, 214), outline=AMBER, width=6)
    d.rounded_rectangle((vx(9), BY - 70, BX1, BY + 70), radius=18, fill=(221, 240, 227), outline=GREEN, width=6)
    d.line((vx(9), BY - 150, vx(9), BY + 150), fill=INK, width=12)
    text(d, (vx(9), BY - 200), '9 mm3', 78, INK, anchor='mm')
    text(d, ((BX0 + vx(9)) / 2, BY + 230), 'inches?  Yes = x 25.4', 72, AMBER, anchor='mm')
    text(d, ((vx(9) + BX1) / 2, BY + 230), 'no question', 72, GREEN, anchor='mm')
    text(d, (BX0, BY + 110), '0', 56, GREY, R, anchor='mm')
    text(d, (BX1, BY + 110), '20', 56, GREY, R, anchor='mm')
    if cube8:
        d.ellipse((vx(8) - 26, BY - 26, vx(8) + 26, BY + 26), fill=GREY)
        text(d, (vx(7.0), BY + 105), '2 mm cube: 8', 56, GREY, anchor='mm')
    if washer:
        d.ellipse((vx(4.75) - 34, BY - 34, vx(4.75) + 34, BY + 34), fill=RED)
        text(d, (vx(4.75), BY - 110), 'our washer: 4.75', 66, RED, anchor='mm')


def card_rule(step):
    """steps: 1 the cube; 2 the bar and the line; 3 + the 2 mm cube; 4 + our washer; 5 + both verdicts."""
    im, d = canvas(bg=WHITE); header(d, 'PrusaSlicer’s rule: the whole part’s volume')
    if step == 1:
        cube(d, 1280, 560, 380)
        text(d, (1280, 880), '2 mm cube', 84, INK, anchor='mm')
        text(d, (1280, 1060), '2 x 2 x 2 = 8 mm3', 96, INK, anchor='mm')
        text(d, (1280, 1230), 'a cube 2 mm on each side', 62, GREY, R, anchor='mm')
    else:
        bar(d, washer=step >= 4, cube8=step >= 3)
        msg = {2: ('the slicer compares the volume with 9', GREY, R), 3: ('a 2 mm cube is 8: under the line', GREY, R),
               4: ('under the line: it asks', RED, B), 5: ('under the line: it asks   ·   above it: never', RED, B)}[step]
        text(d, (1280, 1180), msg[0], 70 if step < 5 else 64, msg[1], msg[2], anchor='mm')
    save(im, f'card-rule-{step}.png')


# --- the 3MF box -----------------------------------------------------------------------------------------------
def box3mf(d, cx, cy, tag=True, lit=False, w=820, h=420):
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=30, fill=LIGHT,
                        outline=BLUE if lit else INK, width=10)
    text(d, (cx, cy - 120), '3MF', 120, INK, anchor='mm')
    text(d, (cx, cy - 20), 'a file', 56, GREY, R, anchor='mm')
    if tag:
        d.rounded_rectangle((cx - 350, cy + 60, cx + 350, cy + 170), radius=18, fill=WHITE, outline=GREEN, width=8)
        text(d, (cx, cy + 115), 'unit="millimeter"', 58, GREEN, anchor='mm')


def card_3mf(step):
    im, d = canvas(bg=WHITE); header(d, 'A 3MF carries its unit')
    if step == 1:
        box3mf(d, 1280, 640, True, lit=True)
        text(d, (1280, 1060), 'the unit is written inside the file', 72, INK, anchor='mm')
        text(d, (1280, 1200), 'like the unit written on a box', 62, GREY, R, anchor='mm')
    elif step == 2:
        box3mf(d, 640, 640, True)
        arrow(d, (1090, 640), (1560, 640), GREEN, 14)
        d.rounded_rectangle((1600, 520, 2400, 760), radius=28, fill=(221, 240, 227), outline=GREEN, width=8)
        text(d, (2000, 600), 'PrusaSlicer', 66, INK, anchor='mm')
        text(d, (2000, 690), 'no question', 78, GREEN, anchor='mm')
        text(d, (1280, 1060), 'PrusaSlicer 2.9.2: no question for 3MF', 70, INK, anchor='mm')
    else:
        d.rounded_rectangle((200, 520, 900, 760), radius=28, fill=LIGHT, outline=INK, width=8)
        text(d, (550, 600), 'FreeCAD', 76, INK, anchor='mm')
        text(d, (550, 690), 'File, Export, 3MF', 56, GREY, R, anchor='mm')
        arrow(d, (930, 640), (1500, 640), BLUE, 14)
        text(d, (1215, 570), 'writes', 60, BLUE, R, anchor='mm')
        box3mf(d, 1950, 640, True, lit=True, w=800)
        text(d, (1280, 1060), 'FreeCAD writes millimeter into the box', 70, INK, anchor='mm')
    save(im, f'card-3mf-{step}.png')


RECAP = [('1  STL', 'no unit · under 9 mm3 it asks'),
         ('2  Tiny part · inch numbers', 'No · Yes · check the size boxes'),
         ('3  3MF', 'carries the unit · 2.9.2 does not ask')]


def card_recap(step):
    im, d = canvas(bg=WHITE); header(d, 'Recap: the inches question')
    for k, (head, line) in enumerate(RECAP):
        y = 260 + k * 360
        on = k < step
        d.rounded_rectangle((120, y, 2440, y + 310), radius=26, fill=LIGHT if on else WHITE,
                            outline=INK if on else FAINT, width=6)
        text(d, (170, y + 90), head, 78, INK if on else FAINT, anchor='lm')
        if on:
            text(d, (170, y + 220), '→ ' + line, 72, GREEN, anchor='lm')
    save(im, f'card-recap-{step}.png')


AST = ['solid Mesh', '  facet normal 0.998630 0.052336 0.000000', '    outer loop',
       '      vertex 2.486305 0.261321 0.300000', '      vertex 2.500000 -0.000000 0.300000',
       '      vertex 2.500000 -0.000000 0.000000', '    endloop', '  endfacet']
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'


def card_ast(step):
    """The first lines of the real washer.ast (out/fx2/A/washer-ast-head.txt) as text; step 4 adds the unit-word count
    (out/fx2/A/washer-ast-unitwords.txt: 0). The lab recording of this step failed (less: command not found), so it is a card."""
    im, d = canvas(bg=WHITE); header(d, 'washer.ast: the first lines of the real file')
    d.rounded_rectangle((120, 200, 2440, 1000), radius=26, fill=LIGHT, outline=INK, width=6)
    shown = (3, 6, 8, 8)[step - 1]
    for k, ln in enumerate(AST[:shown]):
        text(d, (180, 260 + k * 88), ln, 62, INK, MONO)
    if step >= 3:
        text(d, (1280, 1110), 'plain numbers: mm? in?', 84, RED, anchor='mm')
    if step == 4:
        text(d, (1280, 1250), 'unit words in the whole file (mm, inch, unit): 0', 66, GREEN, anchor='mm')
    save(im, f'card-ast-{step}.png')


# --- cut 2 (watch-through c1 fixes), 4 Nov 2026 ---------------------------------------------------------------
def card_vol():
    """The washer's volume, two ways: the 5 x 5 x 0.3 block (7.5 mm3) and the real washer with its hole (4.75 mm3)."""
    im, d = canvas(bg=WHITE); header(d, 'How small is tiny? The volume')
    d.rectangle((300, 300, 800, 800), fill=(236, 240, 246), outline=INK, width=8)
    d.ellipse((325, 325, 775, 775), fill=(176, 190, 212), outline=INK, width=6)
    d.ellipse((480, 480, 620, 620), fill=(236, 240, 246), outline=INK, width=6)
    text(d, (550, 860), '5 x 5 x 0.3 mm', 70, INK, anchor='mm')
    text(d, (1280, 420), 'the solid block: 5 x 5 x 0.3', 70, GREY, R, anchor='lm')
    text(d, (1280, 520), '= 7.5 mm3', 110, INK, anchor='lm')
    text(d, (1280, 700), 'minus the hole: our washer', 70, GREY, R, anchor='lm')
    text(d, (1280, 800), '= 4.75 mm3', 110, RED, anchor='lm')
    text(d, (1280, 1000), 'both are under 9 mm3', 84, GREEN, anchor='lm')
    save(im, 'card-vol-1.png')


def card_why(step):
    """Why a tiny part means probably inches: 25.4 times smaller on each side, 16,000 times in volume."""
    im, d = canvas(bg=WHITE); header(d, 'Why tiny means "probably inches"')
    if step == 1:
        d.rectangle((300, 380, 800, 880), fill=(236, 240, 246), outline=INK, width=8)
        text(d, (550, 630), '1 inch', 84, INK, anchor='mm')
        text(d, (550, 960), '25.4 mm', 70, GREY, R, anchor='mm')
        arrow(d, (900, 630), (1500, 630), RED, 14)
        text(d, (1200, 570), 'typed 1, read as 1 mm', 52, RED, B, anchor='mm')
        d.rectangle((1640, 600, 1660 + 20, 620 + 20), fill=(176, 190, 212), outline=INK, width=4)
        text(d, (1700, 700), '1 mm', 70, INK, anchor='mm')
        text(d, (1280, 1180), 'a part typed in inches comes out 25.4 x smaller on every side', 66, INK, anchor='mm')
    else:
        text(d, (1280, 360), '25.4 x 25.4 x 25.4', 130, INK, anchor='mm')
        text(d, (1280, 520), '= about 16,000 x smaller in volume', 84, RED, anchor='mm')
        text(d, (1280, 760), 'so a part that tiny is probably in inches', 78, INK, anchor='mm')
        text(d, (1280, 950), 'Yes: x 25.4 on every side puts it right', 72, GREEN, anchor='mm')
        text(d, (1280, 1150), 'the 9 mm3 line is PrusaSlicer’s own cutoff, from its source code', 60, GREY, R, anchor='mm')
    save(im, f'card-why-{step}.png')


QUOTE = ['STL files have no units.', 'Slicers read the numbers as millimetres,', 'which is what the model uses.',
         'If your slicer asks about units, pick mm.']


def card_claude(step):
    """Claude's real sentence (run R1, reply.txt), then what the real dialog offers, then what Claude said it had not done."""
    im, d = canvas(bg=WHITE); header(d, 'Claude Code, one real run')
    if step == 1:
        d.rounded_rectangle((120, 230, 2440, 1010), radius=26, fill=LIGHT, outline=INK, width=6)
        for k, ln in enumerate(QUOTE):
            text(d, (200, 330 + k * 160), ln, 82, GREEN if k == 3 else INK, B if k == 3 else R, anchor='lm')
        text(d, (1280, 1180), 'the real reply, word for word', 62, GREY, R, anchor='mm')
    elif step == 2:
        text(d, (1280, 330), 'Claude: "pick mm"', 100, GREEN, anchor='mm')
        text(d, (1280, 520), 'but the real dialog has two buttons only:', 72, INK, R, anchor='mm')
        d.rounded_rectangle((760, 700, 1220, 880), radius=24, fill=LIGHT, outline=INK, width=8)
        d.rounded_rectangle((1340, 700, 1800, 880), radius=24, fill=LIGHT, outline=INK, width=8)
        text(d, (990, 790), 'No', 90, INK, anchor='mm')
        text(d, (1570, 790), 'Yes', 90, INK, anchor='mm')
        text(d, (1280, 1080), 'there is no mm button', 76, RED, anchor='mm')
    else:
        d.rounded_rectangle((120, 260, 2440, 860), radius=26, fill=LIGHT, outline=INK, width=6)
        text(d, (200, 400), 'Claude, last line of its reply:', 66, GREY, R, anchor='lm')
        text(d, (200, 560), '"I haven’t loaded the file into a slicer,', 78, INK, anchor='lm')
        text(d, (200, 680), 'so these are expectations."', 78, INK, anchor='lm')
        text(d, (1280, 1060), 'half: it knew STL has no unit', 84, AMBER, anchor='mm')
        text(d, (1280, 1200), 'but never named the inches question', 84, AMBER, anchor='mm')
    save(im, f'card-claude-{step}.png')


def card_yt(step):
    """Your turn: three steps (one per clause), then the question, then the pause card."""
    im, d = canvas(bg=WHITE); header(d, 'Your turn')
    steps = ['1  export a 2 mm cube (under 9 mm3):', '    as an STL and as a 3MF', '2  open both in PrusaSlicer', '3  which one asks?']
    if step <= 3:
        rows = [('1  Export a 2 mm cube (8 mm3)', 'as an STL and as a 3MF'), ('2  Open both in PrusaSlicer', ''), ('3  Which one asks?', '')]
        for k, (a, b) in enumerate(rows):
            y = 280 + k * 300
            on = k < step
            d.rounded_rectangle((200, y, 2360, y + 240), radius=26, fill=LIGHT if on else WHITE, outline=INK if on else FAINT, width=6)
            text(d, (260, y + (90 if b else 120)), a, 84, INK if on else FAINT, anchor='lm')
            if b:
                text(d, (260, y + 180), b, 62, GREY if on else FAINT, R, anchor='lm')
    elif step == 4:
        cube(d, 1280, 560, 340)
        text(d, (1280, 860), 'a 3 mm cube = 27 mm3', 96, INK, anchor='mm')
        text(d, (1280, 1020), 'but drawn in inch numbers by mistake', 70, AMBER, anchor='mm')
        text(d, (1280, 1180), '(you meant 3 inches)', 60, GREY, R, anchor='mm')
    elif step == 5:
        text(d, (1280, 420), 'Will PrusaSlicer ask?', 120, INK, anchor='mm')
        text(d, (1280, 680), 'Why not?', 120, INK, anchor='mm')
        text(d, (1280, 940), 'What tells you it is wrong?', 120, INK, anchor='mm')
    else:
        text(d, (1280, 560), 'Pause the video', 140, INK, anchor='mm')
        text(d, (1280, 800), 'and try it', 120, GREEN, anchor='mm')
    save(im, f'card-yt-{step}.png')


def card_ans(step):
    """The answer to the your-turn question: 27 is above 9, so no question; the size boxes tell you."""
    im, d = canvas(bg=WHITE); header(d, 'The answer')
    if step == 1:
        d.rounded_rectangle((BX0, BY - 70, vx(9), BY + 70), radius=18, fill=(253, 236, 214), outline=AMBER, width=6)
        d.rounded_rectangle((vx(9), BY - 70, BX1, BY + 70), radius=18, fill=(221, 240, 227), outline=GREEN, width=6)
        d.line((vx(9), BY - 150, vx(9), BY + 150), fill=INK, width=12)
        text(d, (vx(9), BY - 200), '9 mm3', 78, INK, anchor='mm')
        text(d, (BX0, BY + 110), '0', 56, GREY, R, anchor='mm')
        text(d, (BX1, BY + 110), '30', 56, GREY, R, anchor='mm')
        x27 = BX0 + (BX1 - BX0) * 27 / 30.0
        d.ellipse((x27 - 34, BY - 34, x27 + 34, BY + 34), fill=GREEN)
        text(d, (x27 - 60, BY - 110), '3 x 3 x 3 = 27 mm3', 66, GREEN, anchor='rm')
        text(d, (1280, 1000), '27 is above 9: PrusaSlicer does not ask', 80, GREEN, anchor='mm')
        text(d, (1280, 1150), 'no dialog, no warning', 62, GREY, R, anchor='mm')
    else:
        text(d, (1280, 330), 'What tells you it is wrong?', 96, INK, anchor='mm')
        text(d, (1280, 560), 'the size boxes', 100, BLUE, anchor='mm')
        text(d, (1280, 760), 'they read 3 x 3 x 3 mm', 84, INK, anchor='mm')
        text(d, (1280, 920), 'but you meant 3 inches = 76.2 mm', 84, RED, anchor='mm')
        text(d, (1280, 1150), 'no question does not mean the size is right', 66, GREY, R, anchor='mm')
    save(im, f'card-ans-{step}.png')


def card_teaser():
    """The next Fix-it: the plug dies on start (the error text from fx4 take A, last clause)."""
    im, d = canvas(bg=WHITE); header(d, 'Next fix')
    d.rounded_rectangle((120, 300, 2440, 760), radius=26, fill=LIGHT, outline=INK, width=6)
    text(d, (200, 440), 'the plug dies on start:', 66, GREY, R, anchor='lm')
    text(d, (200, 600), 'ModuleNotFoundError: No module named', 66, RED, MONO, anchor='lm')
    text(d, (200, 690), "'mcp.server.fastmcp'", 66, RED, MONO, anchor='lm')
    text(d, (1280, 1000), 'the plug = the small helper that connects Claude to your CAD program', 62, INK, R, anchor='mm')
    save(im, 'card-teaser-1.png')


# --- rev 5 (owner rework, 4 Nov 2026): one picture per diagram that builds step by step (each step only adds) -----
def r5_ast(step):
    """F2: the file as text, 4 steps: facet line + tag; + the 3 vertex lines + tag; + plain numbers; + unit words 0."""
    im, d = canvas(bg=WHITE); header(d, 'washer.ast: FreeCAD’s text (ASCII) STL')
    d.rounded_rectangle((100, 200, 1500, 1000), radius=26, fill=LIGHT, outline=INK, width=6)
    shown = (2, 6, 8, 8)[step - 1]
    for k, ln in enumerate(AST[:shown]):
        text(d, (150, 250 + k * 92), ln, 52, INK, MONO)
    # tags on the right, each pointing at its line
    arrow(d, (1740, 342), (1520, 342), BLUE, 8)
    text(d, (1760, 342), 'facet = one triangle', 56, BLUE, anchor='lm')
    if step >= 2:
        arrow(d, (1740, 618), (1520, 618), BLUE, 8)
        text(d, (1760, 618), 'vertex = one corner', 56, BLUE, anchor='lm')
        text(d, (1760, 700), '(x, y, z)', 52, GREY, R, anchor='lm')
    if step >= 3:
        text(d, (910, 1110), 'plain numbers: mm? in?', 84, RED, anchor='mm')
    if step >= 4:
        text(d, (910, 1250), 'unit words in the whole file: 0', 70, GREEN, anchor='mm')
    save(im, f'card-r5-ast-{step}.png')


def r5_why(step):
    """F4: why tiny means inches, 4 steps: the squares; + 25.4 per side; + about 16,000 in volume; + so: probably inches."""
    im, d = canvas(bg=WHITE); header(d, 'Why tiny means "probably inches"')
    d.rectangle((300, 230, 700, 630), fill=(236, 240, 246), outline=INK, width=8)
    text(d, (500, 430), '1 inch', 80, INK, anchor='mm')
    text(d, (500, 690), 'typed: 1 (inch)', 56, GREY, R, anchor='mm')
    arrow(d, (800, 430), (1500, 430), RED, 14)
    text(d, (1160, 350), 'typed in inches, read as mm', 52, RED, B, anchor='mm')
    d.rectangle((1640, 414, 1672, 446), fill=(176, 190, 212), outline=INK, width=4)
    text(d, (1656, 520), '1 mm', 70, INK, anchor='mm')
    text(d, (1656, 600), 'read: 1 (mm)', 56, GREY, R, anchor='mm')
    if step >= 2:
        text(d, (1280, 830), '25.4 x smaller on every side   (1 inch = 25.4 mm)', 70, INK, anchor='mm')
    if step >= 3:
        text(d, (1280, 990), '25.4 x 25.4 x 25.4 = about 16,000 x smaller in volume', 70, RED, anchor='mm')
    if step >= 4:
        d.rounded_rectangle((160, 1110, 2400, 1290), radius=26, fill=(221, 240, 227), outline=GREEN, width=8)
        text(d, (1280, 1200), 'so tiny means probably inches  ·  Yes = x 25.4', 72, GREEN, anchor='mm')
    save(im, f'card-r5-why-{step}.png')


def r5_rule(step):
    """F5: the 9 mm3 rule, 4 steps: the bar and the line; + under asks / above no question; + 2 mm cube 8; + washer 4.75."""
    im, d = canvas(bg=WHITE); header(d, 'PrusaSlicer’s rule: the whole part’s volume')
    d.rounded_rectangle((BX0, BY - 70, vx(9), BY + 70), radius=18, fill=(253, 236, 214), outline=AMBER, width=6)
    d.rounded_rectangle((vx(9), BY - 70, BX1, BY + 70), radius=18, fill=(221, 240, 227), outline=GREEN, width=6)
    d.line((vx(9), BY - 150, vx(9), BY + 150), fill=INK, width=12)
    text(d, (vx(9), BY - 200), 'the line: 9 mm3', 78, INK, anchor='mm')
    text(d, (BX0, BY + 110), '0', 56, GREY, R, anchor='mm')
    text(d, (BX1, BY + 110), '20 mm3', 56, GREY, R, anchor='mm')
    text(d, (1280, 300), 'the whole part’s volume, in mm3', 66, GREY, R, anchor='mm')
    if step >= 2:
        text(d, ((BX0 + vx(9)) / 2, BY + 230), 'under: it asks', 72, AMBER, anchor='mm')
        text(d, ((vx(9) + BX1) / 2, BY + 230), 'above: no question (2.9.2)', 72, GREEN, anchor='mm')
    if step >= 3:
        d.ellipse((vx(8) - 30, BY - 30, vx(8) + 30, BY + 30), fill=GREY)
        text(d, (vx(8), BY + 360), '2 mm cube: 2 x 2 x 2 = 8', 60, GREY, anchor='mm')
    if step >= 4:
        d.ellipse((vx(4.75) - 36, BY - 36, vx(4.75) + 36, BY + 36), fill=RED)
        text(d, (vx(4.75), BY - 110), 'our washer: 4.75', 66, RED, anchor='mm')
    save(im, f'card-r5-rule-{step}.png')


def r5_quote(step):
    """F10: Claude's reply line 14 (run R1, reply.txt:14) word for word; + "pick mm" lit; + the real dialog's buttons."""
    im, d = canvas(bg=WHITE); header(d, 'Claude’s reply, word for word')
    d.rounded_rectangle((120, 200, 2440, 860), radius=26, fill=LIGHT, outline=INK, width=6)
    for k, ln in enumerate(QUOTE[:3]):
        text(d, (200, 290 + k * 140), ln, 76, INK, R, anchor='lm')
    y = 290 + 3 * 140
    lead = 'If your slicer asks about units, '
    text(d, (200, y), lead, 76, INK, R, anchor='lm')
    x = 200 + font(R, 76).getlength(lead)
    if step >= 2:
        d.rounded_rectangle((x - 14, y - 58, x + font(B, 76).getlength('pick mm.') + 14, y + 58), radius=14, fill=(221, 240, 227), outline=GREEN, width=6)
    text(d, (x, y), 'pick mm.', 76, GREEN if step >= 2 else INK, B if step >= 2 else R, anchor='lm')
    text(d, (2400, 920), 'run R1, reply line 14', 48, GREY, R, anchor='rm')
    if step >= 3:
        text(d, (480, 1150), 'the real dialog:', 72, INK, anchor='mm')
        for bx, lab in ((860, 'No'), (1320, 'Yes')):
            d.rounded_rectangle((bx, 1070, bx + 380, 1230), radius=22, fill=LIGHT, outline=INK, width=8)
            text(d, (bx + 190, 1150), lab, 84, INK, anchor='mm')
        text(d, (1780, 1150), 'no mm button', 72, RED, anchor='lm')
    save(im, f'card-r5-quote-{step}.png')


def r5_turn(step):
    """F12 + F11a: your turn (steps 1-5), then the answer builds onto the same card (steps 6-8)."""
    im, d = canvas(bg=WHITE); header(d, 'Your turn' if step <= 5 else 'Your turn: the answer')
    rows = [('1  Export a 2 mm cube', 'as an STL and a 3MF'), ('2  Open both in PrusaSlicer', ''), ('3  Which one asks?', '')]
    for k, (a, b) in enumerate(rows[:min(step, 3)]):
        y = 230 + k * 270
        d.rounded_rectangle((100, y, 1260, y + 220), radius=26, fill=LIGHT, outline=INK, width=6)
        text(d, (150, y + (80 if b else 110)), a, 66, INK, anchor='lm')
        if b:
            text(d, (150, y + 165), '   ' + b, 58, GREY, R, anchor='lm')
    if step >= 4:
        d.rounded_rectangle((1300, 230, 2460, 1070), radius=26, fill=WHITE, outline=AMBER, width=6)
        cube(d, 1440, 380, 130)
        text(d, (1560, 330), 'a 3 mm cube: 27 mm3', 66, INK, anchor='lm')
        text(d, (1560, 420), 'drawn in inch numbers', 56, AMBER, R, anchor='lm')
        text(d, (1560, 490), 'by mistake', 56, AMBER, R, anchor='lm')
        for k, q in enumerate(('Will it ask?', 'Why not?', 'What tells you it is wrong?')):
            text(d, (1350, 600 + k * 80), q, 60, INK, anchor='lm')
    if step == 5:
        d.rounded_rectangle((100, 1100, 2460, 1300), radius=26, fill=(221, 240, 227), outline=GREEN, width=8)
        text(d, (1280, 1200), 'Pause and try it', 96, GREEN, anchor='mm')
    if step >= 6:
        x0, x1, by = 1360, 2400, 975
        def ax(v):
            return x0 + (x1 - x0) * v / 30.0
        d.rounded_rectangle((x0, by - 40, ax(9), by + 40), radius=12, fill=(253, 236, 214), outline=AMBER, width=5)
        d.rounded_rectangle((ax(9), by - 40, x1, by + 40), radius=12, fill=(221, 240, 227), outline=GREEN, width=5)
        d.line((ax(9), by - 80, ax(9), by + 80), fill=INK, width=8)
        text(d, (ax(9), by - 105), '9 mm3', 48, INK, anchor='mm')
        text(d, (x0, by + 70), '0', 44, GREY, R, anchor='mm')
        text(d, (x1, by + 70), '30', 44, GREY, R, anchor='mm')
        d.ellipse((ax(27) - 26, by - 26, ax(27) + 26, by + 26), fill=GREEN)
        text(d, (ax(27) + 20, by - 105), '3 x 3 x 3 = 27', 48, GREEN, anchor='rm')
    if step >= 7:
        text(d, (1880, 1135), 'above 9: no question', 66, GREEN, anchor='mm')
    if step >= 8:
        d.rounded_rectangle((100, 1200, 2460, 1340), radius=26, fill=(253, 236, 214), outline=AMBER, width=8)
        text(d, (1280, 1270), 'no question does not mean the size is right', 72, AMBER, anchor='mm')
    save(im, f'card-r5-turn-{step}.png')


def rev5():
    for s in (1, 2, 3, 4):
        r5_ast(s)
        r5_why(s)
        r5_rule(s)
    for s in (1, 2, 3):
        r5_quote(s)
        card_recap(s)
    for s in range(1, 9):
        r5_turn(s)


if __name__ == '__main__' and 'rev5' in sys.argv:
    rev5()
elif __name__ == '__main__':
    card_vol()
    card_teaser()
    for s in (1, 2):
        card_why(s)
        card_ans(s)
    for s in (1, 2, 3):
        card_claude(s)
    for s in (1, 2, 3, 4, 5, 6):
        card_yt(s)
    for s in (1, 2, 3, 4, 5):
        card_rule(s)
    for s in (1, 2, 3, 4):
        card_ast(s)
    for s in (1, 2, 3):
        card_3mf(s)
        card_recap(s)
