"""The X backend: xdotool for the fake mouse and keyboard, window search/focus/size, and ffmpeg for a still."""
import re
import subprocess
import time

LOC = re.compile(r'x:(-?\d+)\s+y:(-?\d+)')


class XDo:
    def __init__(self, run=None, env=None):
        self._run = run or (lambda argv, **kw: subprocess.run(argv, **kw))
        self.env = env

    def _x(self, *args):
        kw = {'capture_output': True, 'text': True}
        if self.env is not None:
            kw['env'] = self.env
        return self._run(['xdotool'] + [str(a) for a in args], **kw)

    # mouse and keyboard
    def location(self):
        m = LOC.search(self._x('getmouselocation').stdout or '')
        return (int(m.group(1)), int(m.group(2))) if m else (0, 0)

    def move(self, x, y):
        self._x('mousemove', x, y)

    def click(self, button, repeat=1):
        if repeat > 1:
            self._x('click', '--repeat', repeat, '--delay', 120, button)
        else:
            self._x('click', button)

    def down(self, button):
        self._x('mousedown', button)

    def up(self, button):
        self._x('mouseup', button)

    def type(self, text, delay_ms):
        self._x('type', '--delay', delay_ms, '--', text)

    def key(self, keys):
        self._x('key', '--clearmodifiers', keys)

    # windows
    def search(self, regex, visible=True):
        args = ['search'] + (['--onlyvisible'] if visible else []) + ['--name', regex]
        return [w for w in (self._x(*args).stdout or '').split() if w.strip()]

    def wait_window(self, regex, timeout=30.0, clock=time.time, sleep=time.sleep):
        end = clock() + timeout
        while True:
            ids = self.search(regex)
            if ids:
                return ids[0]
            if clock() >= end:
                return None
            sleep(0.25)

    def focus(self, wid):
        self._x('windowactivate', '--sync', wid)
        self._x('windowfocus', '--sync', wid)

    def place(self, wid, x, y, w, h):
        self._x('windowsize', '--sync', wid, w, h)
        self._x('windowmove', '--sync', wid, x, y)

    def windows(self):
        """id, name and geometry of every visible window (for a probe's windows.txt)."""
        rows = []
        for wid in self.search('.*'):
            name = (self._x('getwindowname', wid).stdout or '').strip()
            geo = ' '.join((self._x('getwindowgeometry', wid).stdout or '').split())
            rows.append(f'{wid}\t{name}\t{geo}')
        return rows


def maximise(xd, wid, size, wmctrl_env=None):
    """Fill the display: wmctrl's maximise when a window manager runs, then an explicit size as a fallback."""
    subprocess.run(['wmctrl', '-i', '-r', wid, '-b', 'add,maximized_vert,maximized_horz'], capture_output=True,
                   env=wmctrl_env)
    time.sleep(0.5)
    geo = xd._x('getwindowgeometry', wid).stdout or ''
    m = re.search(r'Geometry:\s*(\d+)x(\d+)', geo)
    if not m or int(m.group(1)) < size[0] * 0.9:
        xd.place(wid, 0, 0, size[0], size[1])


def screenshot(path, display=':99', size=None, env=None):
    """One frame of the whole display as PNG (ffmpeg x11grab; no ImageMagick needed)."""
    args = ['ffmpeg', '-v', 'error', '-y', '-f', 'x11grab', '-draw_mouse', '1']
    if size:
        args += ['-video_size', f'{size[0]}x{size[1]}']
    args += ['-i', display, '-frames:v', '1', '-update', '1', path]
    subprocess.run(args, check=True, capture_output=True, env=env)
