"""Lesson 7 (fixes) cards, white, built in steps on one layout (nothing moves between builds):
  card-cord-0..4    the course's picture (Claude app, plug, socket in the wall, FreeCAD) and the four stops
  card-path-1..3    how a program's name is found: the PATH folders searched one by one
  card-socket-1..3  the same words, three causes, checked in order
  card-sofar-2, -3  the cord with the stops passed so far
  card-recap-1..4   each stop with its own error words and fix
Run in the QA image:  docker run --rm --network none -v "<lab>:/work" -w /work video-qa:2 python3 video/draw_l7.py"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw_l2 import BLUE, GREEN, GREY, INK, PAPER, R, RED, W, canvas, header, text  # noqa: E402

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-l7')
os.makedirs(OUT, exist_ok=True)
WHITE = (255, 255, 255)
LIGHT = (241, 245, 249)
FAINT = (205, 211, 220)
WALLC = (214, 200, 178)


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(name)


def arrow(d, a, b, col=INK, w=10):
    d.line((a, b), fill=col, width=w)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L = 34
    d.polygon([b, (b[0] - L * math.cos(ang - 0.45), b[1] - L * math.sin(ang - 0.45)),
               (b[0] - L * math.cos(ang + 0.45), b[1] - L * math.sin(ang + 0.45))], fill=col)


XS = [250, 890, 1530, 2170]          # the four stops' centres
NAMES = ['Claude app', 'plug', 'socket', 'FreeCAD']
SUBS = ['Claude Code', 'the MCP server', 'add-on RPC server', 'the workshop']
QS = ['On the list?', 'Does it start?', 'Socket on?', 'The answer?']


def cord(d, y=470, ticks=0, lit=None, numbers=0, faint_after=None):
    """The picture: four boxes joined by the cord; a wall behind the socket. ticks = stops passed (green);
    lit = the stop in focus; numbers = how many stop numbers + questions are shown."""
    d.rectangle((1530 - 40, y - 190, 1530 + 40, y + 190), fill=WALLC)            # the workshop wall
    for k in range(3):
        arrow(d, (XS[k] + 220, y), (XS[k + 1] - 225, y), GREY, 12)
    for k, x in enumerate(XS):
        col = GREEN if k < ticks else (BLUE if lit == k else INK)
        dim = faint_after is not None and k > faint_after
        d.rounded_rectangle((x - 215, y - 120, x + 215, y + 120), radius=26, fill=PAPER,
                            outline=FAINT if dim else col, width=10 if (k < ticks or lit == k) else 6)
        text(d, (x, y - 30), NAMES[k], 62, FAINT if dim else col, anchor='mm')
        text(d, (x, y + 52), SUBS[k], 40, FAINT if dim else GREY, R, anchor='mm')
        if k < numbers:
            d.ellipse((x - 60, y + 175, x + 60, y + 295), fill=GREEN if k < ticks else (BLUE if lit == k else INK))
            text(d, (x, y + 235), '✓' if k < ticks else str(k + 1), 70, PAPER, anchor='mm')
            text(d, (x, y + 360), QS[k], 62, GREEN if k < ticks else (BLUE if lit == k else INK), anchor='mm')


def card_cord(step):
    im, d = canvas(bg=WHITE); header(d, 'Follow the cord')
    cord(d, numbers=step, lit=step - 1 if step else None)
    if step == 0:
        text(d, (W / 2, 1080), 'Lesson 1: the plug goes into a socket in FreeCAD’s wall', 64, INK, R, anchor='mm')
    else:
        text(d, (W / 2, 1080), 'one stop at a time, from Claude’s end', 64, INK, R, anchor='mm')
    save(im, f'card-cord-{step}.png')


def card_path(step):
    im, d = canvas(bg=WHITE); header(d, 'How a program’s name is found: the PATH')
    text(d, (240, 290), 'looking for:', 64, GREY, R)
    d.rounded_rectangle((720, 255, 1060, 375), radius=20, fill=LIGHT, outline=INK, width=6)
    text(d, (890, 315), 'uvx', 76, INK, anchor='mm')
    rows = ['/usr/local/bin', '/usr/bin', '~/.local/bin']
    for k, f in enumerate(rows):
        y = 480 + k * 250
        found = step == 3 and k == 2
        shown = step >= 2 or k < 2
        if not shown:
            continue
        d.rounded_rectangle((240, y, 2320, y + 190), radius=24, fill=(232, 245, 236) if found else LIGHT,
                            outline=GREEN if found else GREY, width=8 if found else 5)
        text(d, (300, y + 95), f'folder {k + 1}:  {f}', 70, INK, anchor='lm')
        text(d, (2260, y + 95), 'uvx is here' if found else 'not here', 70, GREEN if found else RED, anchor='rm')
    if step == 3:
        text(d, (W / 2, 1300), 'installing uv puts uvx into ~/.local/bin', 62, GREEN, R, anchor='mm')
    save(im, f'card-path-{step}.png')


def card_socket(step):
    im, d = canvas(bg=WHITE); header(d, 'Same words, three causes')
    d.rounded_rectangle((240, 230, 2320, 400), radius=24, fill=(253, 236, 236), outline=RED, width=6)
    text(d, (W / 2, 315), 'Error executing tool · Connection refused', 70, RED, anchor='mm')
    rows = [('Is FreeCAD open?', 'open it'), ('Is MCP Addon in the workbench list?', 'copy the add-on into Mod, restart'),
            ('Is the socket started?', 'click Start RPC Server')]
    for k, (q, fix) in enumerate(rows):
        if k >= step:
            break
        y = 480 + k * 290
        d.ellipse((260, y + 30, 400, y + 170), fill=INK)
        text(d, (330, y + 100), str(k + 1), 80, PAPER, anchor='mm')
        text(d, (460, y + 60), q, 72, INK, anchor='lm')
        text(d, (460, y + 150), 'no?  ' + fix, 60, GREEN, R, anchor='lm')
    save(im, f'card-socket-{step}.png')


def card_sofar(n):
    im, d = canvas(bg=WHITE); header(d, 'So far')
    cord(d, ticks=n, lit=n, numbers=4)
    msg = {2: 'on the list, and it starts · next: the socket', 3: 'list, start, socket · one stop left: the answer'}[n]
    text(d, (W / 2, 1210), msg, 64, INK, R, anchor='mm')
    save(im, f'card-sofar-{n}.png')


RECAP = [('1  On the list?', 'No MCP servers configured', 'add it with --scope user'),
         ('2  Does it start?', 'Executable not found: "uvx"', 'install uv'),
         ('3  Socket on?', 'Error executing tool · refused', 'FreeCAD open · add-on in Mod · Start RPC Server'),
         ('4  The answer?', "AttributeError · OSError", 'read the last words, fix that one thing')]


def card_recap(step):
    im, d = canvas(bg=WHITE); header(d, 'Follow the cord: the words at each stop')
    for k, (stop, words, fix) in enumerate(RECAP):
        y = 230 + k * 290
        on = k < step
        d.rounded_rectangle((120, y, 2440, y + 250), radius=26, fill=LIGHT if on else WHITE,
                            outline=INK if on else FAINT, width=6)
        text(d, (170, y + 70), stop, 64, INK if on else FAINT, anchor='lm')
        if on:
            text(d, (900, y + 70), words, 60, RED, anchor='lm')
            text(d, (170, y + 175), '→ ' + fix, 58, GREEN, R, anchor='lm')
    save(im, f'card-recap-{step}.png')


if __name__ == '__main__':
    for s in range(5):
        card_cord(s)
    for s in (1, 2, 3):
        card_path(s)
        card_socket(s)
    for n in (2, 3):
        card_sofar(n)
    for s in (1, 2, 3, 4):
        card_recap(s)
