"""FreeCAD course lesson 18 (a round pen cup by Revolve: the sketch's width is the radius, so give it
Params.cup_diameter / 2) fc-only cards, chips, panels, lower thirds and Short overlays, SCRIPT-fc18.md rev 2 section 3
and SCRIPT-fc18-short.md. The shared cards (card-string-1..3 F2, card-top-1..4 F6, card-why-s1..3 S2) are
solidcraft-course-lab video/frames-sc18's PNGs, used as they are (program-neutral words). Helpers: draw_fc17 (as f17).
Light, 2560 x 1440 cards (44 columns), source overlays RGBA 2880 x 1800 (chips / panels 32 columns), Short overlays
RGBA 1080 x 1920 (32 columns); no percent sign, no angle brackets, never the run names on screen. Every number is
NUMBERS.json's (out/fc18) or the script's arithmetic.
Geometry (source px 2880 x 1800, gridded stills 22 Nov, scratchpad fc18g):
  T/measure-trap120: cup x 1216-2144, y 464-1504; Measurement panel x 2190-2865, Mode y 704, Result y 746.
  S/side-by-side (the tile, re-filmed bef6515: the Tasks dock hidden, no Start Part panel): left window "fixed" (60
  cup) x 480-1680, cup x 812-1430, y 475-1500; right window "name" (120 cup) x 1696-2864, cup x 1918-2685, y 563-1425.
  R/params: rows y 410 / 464 / 518, column A x 592-768, B x 768-944.
  F/expr-half: Expression Editor x 1776-2400, y 1370-1664 ("Result 30.00" y 1594); the width label y ~1392.
  Panels anchored lower left at (40, 1690) (the property area, left of the cup).
  Reply strips (st-A1a..c, st-B1a..c, RGB 2880 x 1800): runs/{A1,B1}/reply.png = screen.mp4 at REPLY_AT (A1 46.0 inside
  the reply window 42.0-50.7, B1 59.0 inside 55.0-63.3, never B1's 51-55 scroll); line boxes by tesseract tsv (22 Nov),
  row pitch 49 px, monospace 24.6 px from x 60; the status rows (y 1451 down) are outside every strip.
Run in the draw image:  MSYS_NO_PATHCONV=1 docker run --rm -v "<edu-visualization>:/ev" -w /ev/freecad-course-lab \
  cad3way-draw:1 python3 video/draw_fc18.py
Test: tests/test_draw_fc18.py"""
import json
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw_fc17 as f17  # noqa: E402

b = f17.b
LAB = b.LAB
OUT = os.path.join(LAB, 'video', 'frames-fc18')
TAKES = os.path.join(LAB, 'out', 'fc18')
f17.OUT = OUT
f17.TAKES = TAKES
NUM = json.load(open(os.path.join(TAKES, 'NUMBERS.json'), encoding='utf-8'))
RUNS = NUM['runs']
f17.RUNS = RUNS
W, H, SW, SH = b.W, b.H, b.SW, b.SH
INK, GREY, WHITE, BLUE, ORANGE, RED, GREEN = f17.INK, f17.GREY, f17.WHITE, f17.BLUE, f17.ORANGE, f17.RED, f17.GREEN
PROBLEMS, LOG, CUR = f17.PROBLEMS, f17.LOG, f17.CUR
text, save, canvas, source, header = f17.text, f17.save, f17.canvas, f17.source, f17.header
PANEL_LL = f17.PANEL_LL
DRAWN = f17.DRAWN
CHIP_AT = (40, 1350)                    # chips lower left, above the panels' zone
CHIP_R = (2150, 820)                    # chips under the Measurement panel (x 2190-2865, y 590-770), right of the cup
PROFILE = [(0, 0), (30, 0), (30, 80), (28, 80), (28, 2), (0, 2)]     # the half-section (x = radius, z), mm
CUPGREY = (150, 156, 168)
HEAD = ('MY REVOLVED CUP CAME', 'OUT TWICE AS WIDE')
WORDS = []
TILE_CUPS = {'60': (812, 1430, 475, 1500), '120': (1918, 2685, 563, 1425)}   # re-filmed take S cups, source px
REPLY_AT = {'A1': 46.0, 'B1': 59.0}
STRIPS = {}
GHOST = (200, 205, 214)
STRIP_X, STRIP_K = 170, 2.2


def r(v):
    return f'{round(v):,}'


def card_half(step):
    """F4, step 1 on "Revolve needs only half the cup": the cup cut down the middle round its centre line; step 2 on
    "a half-section": the right half lit (you draw this), the turn draws the other side."""
    im, d = canvas()
    header(d, 'Revolve needs only half the cup')
    K, cx, fy = 9, W // 2, 1230
    pts = [(cx + K * x, fy - K * z) for x, z in PROFILE]
    mir = [(cx - K * x, fy - K * z) for x, z in PROFILE]
    d.polygon(pts, fill=CUPGREY)
    d.polygon(mir, fill=CUPGREY)
    for y in range(300, 1300, 44):
        d.line((cx, y, cx, y + 24), fill=GREY, width=5)
    text(d, (cx, 290), 'centre line', 48, GREY, anchor='mb')
    text(d, (160, 400), 'the cup, cut down the middle', 56, INK, anchor='lm')
    text(d, (160, 470), '60 across, 80 tall, wall 2', 48, GREY, anchor='lm')
    CUR.extend([('the cup, cut down the middle', 56), ('60 across, 80 tall, wall 2', 48)])
    if step >= 2:
        d.polygon(pts, fill=(255, 226, 196))
        d.line(pts + [pts[0]], fill=ORANGE, width=8)
        text(d, (cx + 40, fy + 70), 'half-section: you draw this', 52, ORANGE, anchor='lm')
        text(d, (cx - 40, fy + 70), 'the turn draws this side', 52, GREY, anchor='rm')
        CUR.extend([('half-section: you draw this', 52), ('the turn draws this side', 52)])
        d.arc((cx - 200, 330, cx + 200, 470), 200, 340, fill=BLUE, width=10)
        f17.arrow(d, (cx + 160, 360), (cx + 196, 392), BLUE, w=10, size=34)
    save(im, f'card-half-{step}.png')


def card_end():
    im, d = canvas()
    text(d, (180, 160), 'FreeCAD + Claude course', 72, INK)
    text(d, (180, 270), 'lesson 18: revolve a cup', 60, BLUE)
    shot = Image.open(os.path.join(TAKES, 'K', 'measure-proof80.png')).convert('RGB').crop((1150, 380, 2210, 1440))
    im.paste(shot.resize((600, 600), Image.LANCZOS), (180, 400))
    d.rectangle((180, 400, 780, 1000), outline=f17.PARTLINE, width=3)
    text(d, (180, 1020), 'the cup at 80, fixed (filmed)', 44, GREY, path=b.R)
    f17.tile(d, (900, 380, 2380, 640), [('Lesson 17', 56), ('the second peg by Mirror', 44)])
    f17.tile(d, (900, 680, 2380, 940), [('SolidCraft vs FreeCAD Assembly:', 56), ('only one can flag a zero gap', 44),
                                        ('the comparison video', 44)])
    f17.tile(d, (900, 980, 2380, 1240), [('FreeCAD + Claude course playlist', 56),
                                         ('the whole course, from lesson 1', 44)])
    d.rounded_rectangle((180, 1110, 760, 1230), radius=20, fill=(204, 0, 0))
    text(d, (470, 1170), 'Subscribe', 60, WHITE, anchor='mm')
    CUR.extend([('FreeCAD + Claude course', 72), ('lesson 18: revolve a cup', 60), ('Lesson 17', 56)])
    save(im, 'card-end.png')


def big_label(d, cx, y, s, col, px=96):
    """A big label centred over a cup (opaque light box)."""
    f = b.font(b.B, px)
    w = d.textlength(s, font=f)
    box = (cx - w / 2 - 30, y, cx + w / 2 + 30, y + px + 40)
    d.rounded_rectangle(box, radius=18, fill=WHITE + (245,), outline=col + (255,), width=6)
    d.text((cx - w / 2, y + 16), s, font=f, fill=col + (255,))
    CUR.append((s, px))
    return box


def tile_labels():
    """F0 frame 0 (St, the S tile): '60 across' over the left cup, '120 across' over the right one; the right label's
    centres from the re-filmed take S (TILE_CUPS), each above its rim."""
    im, d = source()
    for key, col in (('60', GREEN), ('120', RED)):
        x0, x1, y0, _ = TILE_CUPS[key]
        f17.DRAWN[f'ov-tile-0.png:{key}'] = big_label(d, (x0 + x1) / 2, 320, f'{key} across', col)
    # cut 6 (REVIEW-watch-fc18-c5 0:00): the cause chip centred under the 120 cup (it sat at x 40, under the 60 cup)
    s, x0, x1 = 'width 60: cup 120 across', TILE_CUPS['120'][0], TILE_CUPS['120'][1]
    w = d.textlength(s, font=b.font(b.B, 60)) + 44
    f17.DRAWN['ov-tile-0.png:cause'] = f17.src_chip(d, (round((x0 + x1 - w) / 2), 1560), s, RED, px=60)
    save(im, 'ov-tile-0.png')


def chips():
    for slug, s, col, xy in (('r120', 'R 60 × 2 = 120', RED, CHIP_R), ('r60', 'R 30 × 2 = 60', GREEN, CHIP_R),
                             ('r80', 'R 40 × 2 = 80', GREEN, CHIP_R), ('nodia', 'no Diameter mode', INK, CHIP_R),
                             ('far', '60 + 60 = 120', RED, CHIP_AT),
                             ('plane', 'XZ plane = a standing wall\nXY plane = the floor', BLUE, CHIP_AT)):
        f17.chip_file(slug, s, xy, col, px=64)
    f17.chip_file('cc-version', 'Claude Code 2.1.308 · Sonnet 5.5', f17.RUN_CHIP, INK, px=52)
    f17.chip_file('run-A1', f"not asked to check · ${RUNS['A1']['cost_usd']:.2f}", f17.RUN_CHIP, BLUE, px=52)
    f17.chip_file('run-B1', f"asked to check · ${RUNS['B1']['cost_usd']:.2f}", f17.RUN_CHIP, BLUE, px=52)


def panels():
    tr, fx, q5 = NUM['q3_trap'], NUM['q4_fix'], NUM['q5']
    assert tr['outside_x'] == 120.0 and fx['outside_x'] == 60.0
    f17.code_panel('ov-in-F1.png', ['this cup: 120 across', 'planned: 60 across'], PANEL_LL)   # c2 watch: say which is which
    v = ['120 across: ' + r(tr['volume']) + ' mm³', '60 across: ' + r(fx['volume']) + ' mm³']
    assert abs(NUM['volume_ratio_trap_to_fix'] - 2.36) < 0.01
    f17.code_panel('ov-in-F7.png', v + ['about 2.4 × the plastic'], PANEL_LL)
    f17.code_panel('ov-in-F7-1.png', v[:1], PANEL_LL)
    f17.code_panel('ov-in-F7-2.png', v, PANEL_LL)
    assert q5['fixed_reopened_80']['outside_x'] == 80.0 and q5['name_80']['outside_x'] == 160.0
    f17.code_panel('ov-in-K.png', ['fixed file at 80: 80 across', 'first file at 80: 160 across'], PANEL_LL)
    assert RUNS['A1']['pass'] and RUNS['B1']['pass'] and '80' in RUNS['A1']['at'] and '80' in RUNS['B1']['at']
    f17.code_panel('ov-in-C.png', ['run 1 at 80: 80 across', 'run 2 at 80: 80 across'], PANEL_LL)
    f17.code_panel('ov-in-A1.png', ['run 1 file: 60, 80, 45 across', 'width = diameter / 2'], f17.CC_PANEL)
    f17.code_panel('ov-in-B1.png', ['run 2 file: 60, 80, 45 across', 'width = diameter / 2'], f17.CC_PANEL)
    assert fx['inside'] == 56.0
    f17.code_panel('ov-in-F8.png', ['this cup: 60.00 across'], PANEL_LL)   # c2 watch: 'inside 56' was never spoken


# --- F11 / F12: Claude's replies as excerpt strips (whole terminal first in the footage, then these) ----------------
def strip(im, d, name, src, box, at, marks):
    """Paste src.crop(box) at STRIP_K on the still, a ghost frame round it, then each mark (('ring' | 'box', x0, y0,
    x1, y1) in source px) in orange; records (box, k, at) in STRIPS[name]; returns the bottom y."""
    k = STRIP_K
    c = src.crop(box)
    c = c.resize((round(c.width * k), round(c.height * k)), Image.LANCZOS)
    im.paste(c, at)
    d.rectangle((at[0] - 3, at[1] - 3, at[0] + c.width + 2, at[1] + c.height + 2), outline=GHOST, width=3)
    STRIPS.setdefault(name, []).append((box, k, at))
    if box[3] >= 1440 or at[0] + c.width > SW - 40 or at[1] + c.height > SH - 40:
        PROBLEMS.append(f'{name}: strip {box} off the frame / in the status rows')
    for kind, x0, y0, x1, y1 in marks:
        a = (at[0] + (x0 - box[0]) * k, at[1] + (y0 - box[1]) * k)
        z = (at[0] + (x1 - box[0]) * k, at[1] + (y1 - box[1]) * k)
        if kind == 'ring':
            d.rounded_rectangle((a[0] - 16, a[1] - 10, z[0] + 16, z[1] + 10), radius=36, outline=ORANGE, width=10)
        else:
            d.rectangle((a[0] - 12, a[1] - 8, z[0] + 12, z[1] + 8), outline=ORANGE, width=9)
    return at[1] + c.height


# (crop box, marks) per strip, in build order; source px of runs/<run>/reply.png
REPLY = {
    'A1': [[((40, 612, 1150, 662), [('ring', 104, 616, 972, 661)])],                    # outer_radius = d / 2
           [((40, 853, 1150, 950), [('box', 255, 860, 1128, 897), ('box', 103, 910, 252, 946)]),   # 60 mm across
            ((40, 1052, 1150, 1244), [('box', 500, 1056, 926, 1100), ('box', 103, 1105, 1103, 1150),
                                      ('box', 103, 1154, 230, 1198), ('box', 103, 1203, 545, 1240)])]],  # 80, back to 60
    'B1': [[((40, 72, 1150, 126), [('ring', 104, 77, 778, 123)]),                          # radius = d / 2
            ((40, 562, 1150, 664), [('box', 870, 567, 1122, 610), ('box', 103, 615, 774, 660)])],   # radius 30 = 60.0
           [((40, 856, 1150, 1006), [('box', 103, 909, 1122, 1003)])]],                    # 70 -> 70.0, back to 60
}


def still_reply(run, step):
    """Run one / two's reply in three builds on the voice: a "It halved the diameter, in a size it named outer radius" /
    "radius thirty, so sixty across", b "read sixty across, tried eighty, and put sixty back" / "At seventy it read
    seventy, then put sixty back", c + our panel ("By code, it holds at all three sizes we tried")."""
    CUR.clear()
    name = f'st-{run}{"abc"[step - 1]}.png'
    STRIPS.pop(name, None)
    src = Image.open(os.path.join(TAKES, 'runs', run, 'reply.png')).convert('RGB')
    im = Image.new('RGB', (SW, SH), WHITE)
    d = ImageDraw.Draw(im)
    cost = RUNS[run]['cost_usd']
    f17.chip(d, (STRIP_X, 180), ('not asked to check' if run == 'A1' else 'asked to check') + f' · ${cost:.2f}', 64,
             BLUE, BLUE, frame=(SW, SH))
    text(d, (STRIP_X, 300), 'its reply (excerpts)', 48, GREY, path=b.R, frame=(SW, SH))
    y = 380
    for build in REPLY[run][:min(step, 2)]:
        for box, marks in build:
            y = strip(im, d, name, src, box, (STRIP_X, y), marks) + 40
    if step >= 3:
        f10_box = f17.f10.code_box
        lines = [f'run {1 if run == "A1" else 2} file: 60, 80, 45 across', 'width = diameter / 2']
        pb = f10_box(d, STRIP_X, SH - 100, lines, 'checked by code', f17.PX, 0.8, 'lb')
        if pb[1] < y - 20:
            PROBLEMS.append(f'{name}: panel {pb} over the strips (bottom {y})')
    save(im, name)


RECAP = ['Revolve spins a half-section', 'width = radius = diameter / 2']
TURN = ['Your turn: a vase 45 across.', 'What width goes in the sketch?', '45 in the width: how wide?']
SUB = [['Coming up: Claude Code on a', 'local model, Gemma 4 via Ollama'],
       ['Every fix tested in SolidCraft and FreeCAD,', 'by hand and with Claude · Subscribe']]
# fc18 cut 5 (REVIEW-watch-fc18-c4: 17.5 s idle under the Coming up bar): a third line builds on "driving SolidCraft
# and FreeCAD, tested against Claude"; the panel grows downward, so the first two lines stay put
SUB3 = SUB[0] + ['driving SolidCraft and FreeCAD, vs Claude']


def short_overlays():
    f17.band_lines('short-head.png', HEAD, 60, (68, 68))
    f17.band_lines('short-q.png', ['40 mm cup, 40 in the width:', 'how wide does it come out?'], 1240, (50, 50),
                   fill=WHITE + (245,), col=INK)
    f17.band_lines('short-series.png', ['FreeCAD + Claude', 'course, lesson 18'], 1240, (50, 50),
                   fill=(219, 234, 254, 250), col=BLUE)
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))     # S0 frame 1: a big label over each stacked cup
    d = ImageDraw.Draw(im)
    CUR.clear()
    # take S stacked (VIEW_Y 236, 0.5 scale): the 120 cup's rim spans y ~306-510, so its label sits on the body below
    # the rim (like the 60 label); light patches (FreeCAD grey) hide the nav cube corner of each half
    for y0, y1 in ((236, 302), (776, 846)):
        d.rectangle((696, y0, 830, y1), fill=(255, 255, 255, 255))   # frame 1 dims overlays ~0.86: 255 lands nearest the 225 grey
    big_label(d, 540, 540, '120 across', RED, px=84)
    big_label(d, 540, 1000, '60 across', GREEN, px=84)
    save(im, 'short-tile.png')


def main():
    os.makedirs(OUT, exist_ok=True)
    b.OUT = OUT
    PROBLEMS.clear()
    LOG.clear()
    f17.DRAWN.clear()
    for s in (1, 2):
        card_half(s)
    card_end()
    tile_labels()
    chips()
    panels()
    for run in ('A1', 'B1'):
        for step in (1, 2, 3):
            still_reply(run, step)
    f17.ov_lines('rc-1.png', RECAP, 2, (20, 1400, 1300, 1690), one=True)
    f17.ov_lines('yt-1.png', TURN, 2, (20, 1230, 1300, 1690), one=True)
    f17.ov_lines('yt-2.png', TURN, 3, (20, 1230, 1300, 1690), one=True)
    for i, lines in enumerate(SUB, 1):
        f17.ov_lines(f'sub-{i}.png', lines, 2, (20, 1470, 1560, 1690), px=54, one=True)
    f17.ov_lines('sub-3.png', SUB3, 3, (20, 1470, 1560, 1785), px=54, one=True)
    short_overlays()
    WORDS.clear()
    WORDS.extend(s for v in LOG.values() for s, _ in v)
    for w in WORDS:
        if '%' in w or '<' in w or '>' in w or 'A1' in w or 'B1' in w:
            PROBLEMS.append(f'{w!r}: forbidden on screen')
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
