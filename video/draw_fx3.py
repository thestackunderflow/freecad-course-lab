"""Fix-it fx3 cards (spawn uvx ENOENT: the two PATH lists), white, one layout per sequence:
  card-path-1    the real `echo $PATH` of take A one folder per line, .local/bin lit (twice), the lab image's own folder named
  card-lists-1..4 the terminal's list beside the app's shorter list; the measured default list; the installer's line; the app that does not read it
  card-paths     the MCP docs' config and log folders (connect-local-servers), from the page, labelled as such
  card-sofar-1..3, card-recap-1..3, card-ans-1..3, card-outro-1..2
Every value comes from out/fx3 (ANSWERS.md): PATH, short list from /etc/environment, the line `. "$HOME/.local/bin/env"`.
Run in the QA image:  docker run --rm --network none -v "<lab>:/work" -w /work video-qa:2 python3 video/draw_fx3.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw_l2 import B, BLUE, GREEN, GREY, INK, R, RED, canvas, header, text  # noqa: E402

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-fx3')
os.makedirs(OUT, exist_ok=True)
WHITE = (255, 255, 255)
LIGHT = (241, 245, 249)
FAINT = (205, 211, 220)
AMBER = (180, 110, 0)
AMBER_BG = (253, 236, 214)
GREEN_BG = (221, 240, 227)
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
MONOB = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'

LONG = ['/home/maker/.local/bin', '/home/maker/.local/bin', '/opt/freecad/usr/bin', '/usr/local/sbin', '/usr/local/bin',
        '/usr/sbin', '/usr/bin', '/sbin', '/bin']
SHORT = ['/usr/local/sbin', '/usr/local/bin', '/usr/sbin', '/usr/bin', '/sbin', '/bin', '/usr/games', '/usr/local/games',
         '/snap/bin']


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(name)


def box(d, x0, y0, x1, y1, fill=LIGHT, outline=INK):
    d.rounded_rectangle((x0, y0, x1, y1), radius=26, fill=fill, outline=outline, width=6)


def cross(d, cx, cy, s=70, col=RED):
    d.line((cx - s, cy - s, cx + s, cy + s), fill=col, width=18)
    d.line((cx - s, cy + s, cx + s, cy - s), fill=col, width=18)


def card_path1():
    im, d = canvas(bg=WHITE)
    header(d, 'Your terminal\'s list: echo $PATH')
    box(d, 120, 250, 1700, 1300)
    for k, p in enumerate(LONG):
        y = 330 + k * 108
        hot = '.local/bin' in p
        if hot:
            d.rounded_rectangle((150, y - 44, 1670, y + 44), radius=14, fill=AMBER_BG, outline=AMBER, width=4)
        text(d, (190, y), p, 62, INK, path=MONOB if hot else MONO, anchor='lm')
    text(d, (1780, 440), 'uvx lives here', 66, AMBER, anchor='la')
    text(d, (1780, 530), '(the folder is listed twice)', 52, GREY, R, anchor='la')
    text(d, (1780, 800), 'this lab image\'s own folder:', 52, GREY, R, anchor='la')
    text(d, (1780, 870), '/opt/freecad/usr/bin', 52, GREY, MONO, anchor='la')
    text(d, (1780, 1100), 'a list = folders', 54, INK, anchor='la')
    text(d, (1780, 1170), 'searched in order', 54, INK, anchor='la')
    save(im, 'card-path-1.png')


def card_lists(step):
    im, d = canvas(bg=WHITE)
    if step == 1:
        header(d, 'Two lists on one computer')
        box(d, 120, 330, 1230, 1100, fill=GREEN_BG, outline=GREEN)
        text(d, (675, 410), 'your terminal', 70, INK, anchor='mm')
        for k, p in enumerate(LONG[1:]):
            hot = '.local/bin' in p
            text(d, (180, 500 + k * 70), p, 46, AMBER if hot else INK, path=MONOB if hot else MONO, anchor='lm')
        box(d, 1330, 330, 2440, 1100, fill=LIGHT, outline=INK)
        text(d, (1885, 410), 'a desktop app', 70, INK, anchor='mm')
        for k, p in enumerate(SHORT[:6]):
            text(d, (1390, 500 + k * 70), p, 46, INK, path=MONO, anchor='lm')
        text(d, (1885, 960), 'shorter: no .local/bin', 58, RED, anchor='mm')
        text(d, (1280, 1250), 'same computer, two different lists', 70, INK, anchor='mm')
    elif step == 2:
        header(d, 'The system\'s default list')
        box(d, 160, 300, 2400, 1080)
        for k, p in enumerate(SHORT):
            col, row = divmod(k, 5)
            text(d, (260 + col * 1080, 400 + row * 120), p, 58, INK, path=MONO, anchor='lm')
        text(d, (1280, 1000), 'nine folders, no .local/bin on it', 64, RED, anchor='mm')
        text(d, (1280, 1140), 'measured in Docker, from /etc/environment', 52, GREY, R, anchor='mm')
        text(d, (1280, 1230), 'a real app\'s list may be longer:', 52, GREY, R, anchor='mm')
        text(d, (1280, 1310), 'what matters is that .local/bin is missing', 52, GREY, R, anchor='mm')
    elif step == 3:
        header(d, 'uv\'s installer added one line')
        box(d, 160, 300, 2400, 540, fill=AMBER_BG, outline=AMBER)
        text(d, (230, 420), '. "$HOME/.local/bin/env"', 84, INK, path=MONOB, anchor='lm')
        text(d, (1280, 640), 'it puts .local/bin on the terminal\'s list', 66, GREEN, anchor='mm')
        box(d, 160, 760, 1230, 1040)
        text(d, (695, 860), '~/.bashrc', 72, INK, path=MONOB, anchor='mm')
        text(d, (695, 960), 'line 120', 56, GREY, R, anchor='mm')
        box(d, 1330, 760, 2400, 1040)
        text(d, (1865, 860), '~/.profile', 72, INK, path=MONOB, anchor='mm')
        text(d, (1865, 960), 'line 29', 56, GREY, R, anchor='mm')
        text(d, (1280, 1200), 'start-up files: the terminal reads them when it opens', 60, INK, anchor='mm')
    else:
        header(d, 'Who reads the start-up file?')
        box(d, 160, 330, 1230, 960, fill=GREEN_BG, outline=GREEN)
        text(d, (695, 440), 'your terminal', 76, INK, anchor='mm')
        text(d, (695, 600), 'reads it', 90, GREEN, anchor='mm')
        text(d, (695, 780), 'at every open', 56, GREY, R, anchor='mm')
        box(d, 1330, 330, 2400, 960, fill=LIGHT, outline=INK)
        text(d, (1865, 440), 'a desktop app', 76, INK, anchor='mm')
        text(d, (1865, 600), 'on most systems:', 62, GREY, R, anchor='mm')
        text(d, (1865, 720), 'does not', 90, RED, anchor='mm')
        cross(d, 1280, 650, 70)
        text(d, (1280, 1140), 'which files a system reads differs', 66, INK, anchor='mm')
        text(d, (1280, 1250), 'a full path works everywhere', 66, GREEN, anchor='mm')
    save(im, f'card-lists-{step}.png')


def card_name():
    im, d = canvas(bg=WHITE)
    header(d, 'Think of an address book')
    box(d, 160, 330, 1230, 960, fill=AMBER_BG, outline=AMBER)
    text(d, (695, 450), 'a short name', 76, INK, anchor='mm')
    text(d, (695, 620), '= a nickname', 80, AMBER, anchor='mm')
    text(d, (695, 790), 'uvx', 90, INK, path=MONOB, anchor='mm')
    box(d, 1330, 330, 2400, 960, fill=GREEN_BG, outline=GREEN)
    text(d, (1865, 450), 'a full path', 76, INK, anchor='mm')
    text(d, (1865, 620), '= the whole address', 80, GREEN, anchor='mm')
    text(d, (1865, 790), '/home/maker/.local/bin/uvx', 44, INK, path=MONOB, anchor='mm')
    text(d, (1280, 1150), 'the computer searches the list for the nickname', 62, INK, anchor='mm')
    save(im, 'card-name-1.png')


def card_claude():
    im, d = canvas(bg=WHITE)
    header(d, 'What Claude wrote, and what we use')
    box(d, 120, 300, 2440, 620, fill=AMBER_BG, outline=AMBER)
    text(d, (180, 380), "Claude's config block (from its reply)", 54, GREY, R, anchor='lm')
    text(d, (180, 500), '"args": ["freecad-mcp"]', 78, INK, path=MONOB, anchor='lm')
    text(d, (2380, 560), 'no version number', 54, RED, anchor='rm')
    box(d, 120, 720, 2440, 1040, fill=GREEN_BG, outline=GREEN)
    text(d, (180, 800), 'what our lab used', 54, GREY, R, anchor='lm')
    text(d, (180, 920), '"args": ["freecad-mcp@0.1.28"]', 78, INK, path=MONOB, anchor='lm')
    text(d, (2380, 980), '@0.1.28 = pinned', 54, GREEN, anchor='rm')
    text(d, (1280, 1200), 'it also added Windows steps we did not ask for', 60, INK, anchor='mm')
    text(d, (1280, 1300), 'the check is which uvx on your machine', 56, GREY, R, anchor='mm')
    save(im, 'card-claude-1.png')


def card_paths():
    im, d = canvas(bg=WHITE)
    header(d, 'Where the config and the logs live')
    rows = [('macOS', '~/Library/Application Support/Claude/', '~/Library/Logs/Claude'),
            ('Windows', '%APPDATA%\\Claude\\', '%APPDATA%\\Claude\\logs'),
            ('Linux', '~/.config/Claude/', '~/.config/Claude/logs')]
    text(d, (560, 270), 'config file folder', 54, GREY, R, anchor='mm')
    text(d, (1850, 270), 'log folder', 54, GREY, R, anchor='mm')
    for k, (osn, cfg, log) in enumerate(rows):
        y = 330 + k * 270
        box(d, 100, y, 2460, y + 230)
        text(d, (150, y + 50), osn, 62, BLUE, anchor='lm')
        text(d, (150, y + 150), cfg, 48, INK, path=MONO, anchor='lm')
        text(d, (1330, y + 150), log, 48, INK, path=MONO, anchor='lm')
    text(d, (1280, 1180), 'file: claude_desktop_config.json', 58, INK, path=MONO, anchor='mm')
    text(d, (1280, 1280), 'from the MCP docs (connect-local-servers)', 52, GREY, R, anchor='mm')
    text(d, (1280, 1360), 'Windows: write every backslash twice', 52, AMBER, anchor='mm')
    save(im, 'card-paths.png')


def card_sofar(step):
    im, d = canvas(bg=WHITE)
    if step == 1:
        header(d, 'So far')
        box(d, 160, 380, 2400, 960, fill=AMBER_BG, outline=AMBER)
        text(d, (1280, 560), 'a short name', 100, INK, anchor='mm')
        text(d, (1280, 780), 'needs the list', 100, AMBER, anchor='mm')
    elif step == 2:
        header(d, 'So far')
        box(d, 160, 380, 2400, 960, fill=GREEN_BG, outline=GREEN)
        text(d, (1280, 560), 'a full path', 100, INK, anchor='mm')
        text(d, (1280, 780), 'needs no list at all', 100, GREEN, anchor='mm')
    else:
        header(d, 'The Fix-it series')
        box(d, 160, 380, 2400, 960, fill=LIGHT)
        text(d, (1280, 560), 'every fix tested on screen', 88, INK, anchor='mm')
        text(d, (1280, 760), 'not guessed', 88, GREEN, anchor='mm')
        text(d, (1280, 1120), 'Subscribe for the next fix', 80, BLUE, anchor='mm')
    save(im, f'card-sofar-{step}.png')


RECAP = [('1  which uvx', 'Windows: Get-Command uvx (not tested here)'),
         ('2  the full path', 'in command, instead of uvx'),
         ('3  quit completely', 'then reopen: it reads at start')]


def card_recap(step):
    im, d = canvas(bg=WHITE)
    header(d, 'Recap: the full path')
    for k, (head, line) in enumerate(RECAP):
        y = 260 + k * 360
        on = k < step
        d.rounded_rectangle((120, y, 2440, y + 310), radius=26, fill=LIGHT if on else WHITE,
                            outline=INK if on else FAINT, width=6)
        text(d, (170, y + 90), head, 78, INK if on else FAINT, anchor='lm')
        if on:
            text(d, (170, y + 220), '→ ' + line, 66, GREEN, anchor='lm')
    save(im, f'card-recap-{step}.png')


ANS = [('you add .local/bin', 'to your terminal\'s start-up file', INK),
       ('the desktop app, on most systems,', 'does not read that file', RED),
       ('the full path', 'needs no list', GREEN)]


def card_ans(step):
    im, d = canvas(bg=WHITE)
    header(d, 'The answer: not reliably')
    a, b, col = ANS[step - 1]
    box(d, 160, 360, 2400, 960)
    text(d, (1280, 560), a, 88, col, anchor='mm')
    text(d, (1280, 760), b, 88, col, anchor='mm')
    for k in range(3):
        x = 1280 + (k - 1) * 90
        d.ellipse((x - 18, 1120 - 18, x + 18, 1120 + 18), fill=INK if k < step else FAINT)
    save(im, f'card-ans-{step}.png')


OUTRO = [('The Fix-it playlist', 'more exact errors, with exact fixes', INK),
         ('FreeCAD lesson 7', 'the PATH in full', BLUE)]


def card_outro(step):
    im, d = canvas(bg=WHITE)
    header(d, 'Before you go')
    a, b, col = OUTRO[step - 1]
    box(d, 160, 360, 2400, 960)
    text(d, (1280, 560), a, 96, col, anchor='mm')
    text(d, (1280, 770), b, 66, col, R, anchor='mm')
    save(im, f'card-outro-{step}.png')


if __name__ == '__main__':
    card_path1()
    card_name()
    card_claude()
    for s in (1, 2, 3, 4):
        card_lists(s)
    card_paths()
    for s in (1, 2, 3):
        card_sofar(s)
        card_recap(s)
        card_ans(s)
    for s in (1, 2):
        card_outro(s)
