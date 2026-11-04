"""Fix-it fx4 cards (mcp 2 rename + Python 3.12 cousin), white, one layout per sequence:
  card-bound-1..7   a fresh install takes the newest mcp allowed; the missing name; old copy; confirmed triggers; non-triggers
  card-sofar-1..2   the recap bridge
  card-engines-1..3 FreeCAD's engine 3.11 vs the plug's 3.12
  card-recap-1..3   the three recap lines
  card-ans-1..5     the answer to the your-turn question (mcp 3)
Every number comes from out/fx4 (ANSWERS.md): mcp 2.3.0, 1.30.0, 0.1.19, 0.1.28 bound below 3, FreeCAD Python 3.11.14.
Run in the QA image:  docker run --rm --network none -v "<lab>:/work" -w /work video-qa:2 python3 video/draw_fx4.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw_l2 import B, BLUE, GREEN, GREY, INK, R, RED, canvas, header, text  # noqa: E402

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-fx4')
os.makedirs(OUT, exist_ok=True)
WHITE = (255, 255, 255)
LIGHT = (241, 245, 249)
FAINT = (205, 211, 220)
AMBER = (180, 110, 0)


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(name)


def box(d, x0, y0, x1, y1, fill=LIGHT, outline=INK):
    d.rounded_rectangle((x0, y0, x1, y1), radius=26, fill=fill, outline=outline, width=6)


def cross(d, cx, cy, s=70, col=RED):
    d.line((cx - s, cy - s, cx + s, cy + s), fill=col, width=18)
    d.line((cx - s, cy + s, cx + s, cy - s), fill=col, width=18)


def card_bound(step):
    im, d = canvas(bg=WHITE)
    if step == 1:
        header(d, 'A fresh install takes the newest allowed')
        box(d, 160, 380, 1200, 760)
        text(d, (680, 470), 'old plug 0.1.19', 76, INK, anchor='mm')
        text(d, (680, 580), 'parts list says:', 56, GREY, R, anchor='mm')
        text(d, (680, 680), 'mcp 1.12.2 or newer', 70, INK, anchor='mm')
        text(d, (1280, 570), '→', 150, BLUE, anchor='mm')
        box(d, 1360, 380, 2400, 760, fill=(253, 236, 214), outline=AMBER)
        text(d, (1880, 470), 'newest mcp today', 66, GREY, R, anchor='mm')
        text(d, (1880, 590), '2.3.0', 150, RED, anchor='mm')
        text(d, (1280, 1000), 'no upper limit: version 2 is allowed', 74, INK, anchor='mm')
    elif step == 2:
        header(d, 'The plug asks for a name that is gone')
        box(d, 160, 380, 1180, 760)
        text(d, (670, 480), 'the plug asks for', 60, GREY, R, anchor='mm')
        text(d, (670, 600), 'mcp.server.fastmcp', 72, INK, anchor='mm')
        box(d, 1380, 380, 2400, 760, fill=WHITE, outline=FAINT)
        text(d, (1890, 480), 'mcp 2.3.0 shelf', 66, GREY, R, anchor='mm')
        text(d, (1890, 620), 'empty: removed', 80, RED, anchor='mm')
        cross(d, 1280, 570, 90)
        text(d, (1280, 1000), 'ModuleNotFoundError', 90, RED, anchor='mm')
    elif step == 3:
        header(d, 'Your old copy kept working')
        box(d, 160, 380, 2400, 780, fill=(221, 240, 227), outline=GREEN)
        text(d, (1280, 490), 'installed long ago, with an older mcp', 70, INK, anchor='mm')
        text(d, (1280, 640), 'it still has the name it asks for', 66, GREY, R, anchor='mm')
        text(d, (1280, 1000), 'the parts list is read only when installing', 78, INK, anchor='mm')
    elif step in (4, 5):
        header(d, 'A fresh install: you changed nothing')
        items = {4: ['a new machine', 'a uvx line with no cached copy'],
                 5: ['a clone synced with upgrade', 'a clone with no lock file']}[step]
        for k, it in enumerate(items):
            y = 360 + k * 340
            box(d, 160, y, 2400, y + 280, fill=(253, 236, 214), outline=AMBER)
            text(d, (230, y + 140), '→ ' + it, 84, INK, anchor='lm')
        text(d, (1280, 1150), 'result: the newest mcp, 2.3.0 → the error', 66, RED, anchor='mm')
    elif step == 6:
        header(d, 'NOT a fresh install')
        box(d, 160, 380, 2400, 800, fill=(221, 240, 227), outline=GREEN)
        text(d, (1280, 490), 're-sync from a committed lock file', 80, INK, anchor='mm')
        text(d, (1280, 640), 'the lock keeps the old version', 70, GREEN, anchor='mm')
        text(d, (1280, 1050), 'it starts', 90, GREEN, anchor='mm')
    else:
        header(d, 'NOT a fresh install')
        box(d, 160, 380, 2400, 800, fill=(221, 240, 227), outline=GREEN)
        text(d, (1280, 490), 'plain uvx freecad-mcp, no version', 80, INK, anchor='mm')
        text(d, (1280, 640), 'now gets 0.1.28', 80, GREEN, anchor='mm')
        text(d, (1280, 1050), 'and starts', 90, GREEN, anchor='mm')
    save(im, f'card-bound-{step}.png')


def card_sofar(step):
    im, d = canvas(bg=WHITE)
    if step == 1:
        header(d, 'So far: why it broke')
        for k, t in enumerate(['1  a renamed part', '2  an open-ended list', '3  a fresh install']):
            y = 300 + k * 330
            box(d, 160, y, 2400, y + 270, fill=LIGHT, outline=INK)
            text(d, (230, y + 135), t, 90, INK, anchor='lm')
    elif step == 2:
        header(d, 'What broke')
        box(d, 160, 380, 2400, 700, fill=(253, 236, 214), outline=AMBER)
        text(d, (1280, 540), 'a list with no upper limit', 88, INK, anchor='mm')
        text(d, (1280, 800), '+', 110, GREY, anchor='mm')
        box(d, 160, 900, 2400, 1220, fill=(253, 236, 214), outline=AMBER)
        text(d, (1280, 1060), 'the old import (fastmcp)', 88, INK, anchor='mm')
    elif step == 3:
        header(d, 'So far: the two fixes')
        box(d, 160, 340, 2400, 700, fill=(221, 240, 227), outline=GREEN)
        text(d, (230, 440), 'fix', 62, GREY, R, anchor='lm')
        text(d, (230, 580), 'a rewritten plug (0.1.20+)', 88, GREEN, anchor='lm')
        box(d, 160, 800, 2400, 1160, fill=(253, 236, 214), outline=AMBER)
        text(d, (230, 900), 'workaround', 62, GREY, R, anchor='lm')
        text(d, (230, 1040), 'pin mcp below 2', 88, AMBER, anchor='lm')
    else:
        header(d, 'A second failure is next')
        box(d, 160, 400, 2400, 900, fill=LIGHT, outline=INK)
        text(d, (1280, 560), 'the plug  +  FreeCAD', 96, INK, anchor='mm')
        text(d, (1280, 740), 'on the same Python?', 96, RED, anchor='mm')
    save(im, f'card-sofar-{step}.png')


def card_stub(step):
    im, d = canvas(bg=WHITE)
    header(d, 'What mcp 2 left behind')
    box(d, 160, 380, 2400, 960, fill=LIGHT if step < 3 else (253, 236, 214), outline=INK if step < 3 else AMBER)
    msg = {1: ('mcp 2: the old name', 'mcp.server.fastmcp is removed'),
           2: ('since late August', 'a stub file raises this error'),
           3: ('its hint names', 'the rename and the pin: mcp below 2')}[step]
    text(d, (1280, 590), msg[0], 90, INK, anchor='mm')
    text(d, (1280, 780), msg[1], 82, RED if step < 3 else AMBER, anchor='mm')
    save(im, f'card-stub-{step}.png')


def card_recipe():
    im, d = canvas(bg=WHITE)
    header(d, 'A parts list is a shopping list')
    box(d, 160, 360, 1180, 1000)
    text(d, (670, 460), 'recipe card', 62, GREY, R, anchor='mm')
    text(d, (670, 640), 'flour:', 80, INK, anchor='mm')
    text(d, (670, 770), 'any newer brand', 80, INK, anchor='mm')
    text(d, (1280, 680), '=', 140, GREY, anchor='mm')
    box(d, 1380, 360, 2400, 1000, fill=(253, 236, 214), outline=AMBER)
    text(d, (1890, 460), 'parts list', 62, GREY, R, anchor='mm')
    text(d, (1890, 640), 'mcp:', 80, INK, anchor='mm')
    text(d, (1890, 770), '1.12.2 or newer', 80, INK, anchor='mm')
    text(d, (1280, 1180), 'no upper limit: every fresh trip gets the newest', 62, GREY, R, anchor='mm')
    save(im, 'card-recipe.png')


def card_pitch():
    im, d = canvas(bg=WHITE)
    header(d, 'The Fix-it series')
    box(d, 160, 380, 2400, 960, fill=LIGHT)
    text(d, (1280, 560), 'every error reproduced on screen', 88, INK, anchor='mm')
    text(d, (1280, 760), 'not guessed', 88, GREEN, anchor='mm')
    text(d, (1280, 1120), 'Subscribe for the next fix', 80, BLUE, anchor='mm')
    save(im, 'card-pitch.png')


def engine(d, cx, cy, label, col=INK):
    d.rounded_rectangle((cx - 230, cy - 120, cx + 230, cy + 120), radius=24, fill=(214, 222, 235), outline=col, width=6)
    text(d, (cx, cy - 50), 'engine', 54, GREY, R, anchor='mm')
    text(d, (cx, cy + 40), label, 100, col, anchor='mm')


def card_engines(step):
    im, d = canvas(bg=WHITE)
    if step == 1:
        header(d, 'This FreeCAD carries its own engine')
        box(d, 560, 330, 2000, 1100)
        text(d, (1280, 420), 'this FreeCAD', 96, INK, anchor='mm')
        engine(d, 1280, 740, '3.11')
        text(d, (1280, 960), 'Python 3.11.14 (this FreeCAD)', 62, GREY, R, anchor='mm')
    elif step == 2:
        header(d, 'The plug needs a newer engine')
        box(d, 560, 330, 2000, 1000, fill=(221, 240, 227), outline=GREEN)
        text(d, (1280, 430), 'the plug  freecad-mcp 0.1.28', 80, INK, anchor='mm')
        text(d, (1280, 600), 'needs Python 3.12 or later', 90, GREEN, anchor='mm')
        text(d, (1280, 800), 'says its own PyPI page', 62, GREY, R, anchor='mm')
    else:
        header(d, 'It does not fit')
        engine(d, 760, 640, '3.11')
        box(d, 1300, 520, 2300, 780, fill=(221, 240, 227), outline=GREEN)
        text(d, (1800, 650), 'needs 3.12+', 80, GREEN, anchor='mm')
        cross(d, 1190, 650, 70)
        text(d, (1280, 1050), 'FreeCAD’s 3.11 ≠ 3.12 or later', 84, RED, anchor='mm')
    save(im, f'card-engines-{step}.png')


RECAP = [('1  Update the plug', '0.1.28 or newer: rewritten for the new name'),
         ('2  Or pin mcp below 2', 'if you must keep an old plug'),
         ('3  Never into FreeCAD’s Python', 'let uvx bring its own 3.12')]


def card_recap(step):
    im, d = canvas(bg=WHITE)
    header(d, 'Recap: the mcp rename')
    for k, (head, line) in enumerate(RECAP):
        y = 260 + k * 360
        on = k < step
        d.rounded_rectangle((120, y, 2440, y + 310), radius=26, fill=LIGHT if on else WHITE,
                            outline=INK if on else FAINT, width=6)
        text(d, (170, y + 90), head, 78, INK if on else FAINT, anchor='lm')
        if on:
            text(d, (170, y + 220), '→ ' + line, 66, GREEN, anchor='lm')
    save(im, f'card-recap-{step}.png')


ANS = [('mcp 3 comes out', 'the day it ships', INK),
       ('a fresh 0.1.28 still takes', 'the newest mcp below 3', INK),
       ('version 3 stays out', 'the plug keeps running', GREEN),
       ('no limit: a fresh install', 'takes 3 as soon as it is out', RED),
       ('a limit buys time', 'read the release notes', AMBER),
       ('args line: @0.1.28 = pinned', 'plain freecad-mcp = not pinned', INK)]


def card_ans(step):
    im, d = canvas(bg=WHITE)
    header(d, 'The answer')
    a, b, col = ANS[step - 1]
    box(d, 160, 360, 2400, 960)
    text(d, (1280, 560), a, 100, col, anchor='mm')
    text(d, (1280, 760), b, 100, col, anchor='mm')
    for k in range(6):
        x = 1280 + (k - 2.5) * 90
        d.ellipse((x - 18, 1120 - 18, x + 18, 1120 + 18), fill=INK if k < step else FAINT)
    save(im, f'card-ans-{step}.png')


OUTRO = [('Pin the plug', 'freecad-mcp@0.1.28: the plug stops changing', INK),
         ('Its parts follow its own list', '0.1.28 stops mcp below 3', INK),
         ('A pin to a broken version', 'stays broken: move the pin forward', AMBER),
         ('Next fix', 'uvx works in the terminal, the desktop app cannot find it', BLUE)]


def card_outro(step):
    im, d = canvas(bg=WHITE)
    header(d, 'Before you go')
    a, b, col = OUTRO[step - 1]
    box(d, 160, 360, 2400, 960)
    text(d, (1280, 560), a, 96, col, anchor='mm')
    text(d, (1280, 770), b, 66, col, R, anchor='mm')
    save(im, f'card-outro-{step}.png')


if __name__ == '__main__':
    for s_ in (1, 2, 3, 4):
        card_outro(s_)
    for s in range(1, 8):
        card_bound(s)
    for s in (1, 2, 3, 4):
        card_sofar(s)
    for s in (1, 2, 3):
        card_stub(s)
    card_recipe()
    card_pitch()
    for s in (1, 2, 3):
        card_engines(s)
        card_recap(s)
    for s in range(1, 7):
        card_ans(s)
