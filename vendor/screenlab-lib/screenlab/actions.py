"""Human-paced input over an X backend (screenlab.x.XDo, or a fake in tests).

Timing rule: an event is logged when its action happens. A click's event is written after the glide and the short
pre-click pause, immediately before the button goes down; typing is logged at the first key; a drag logs the press
and the release. Positions are given in `units` (or display pixels) and every event carries display pixels, the same
space as the cursor log."""
import time

from . import ease


class Actor:
    def __init__(self, x, events, units=None, display=None, pace=1.0, sleep=time.sleep, clock=time.time,
                 step_s=ease.STEP_S):
        self.x, self.ev = x, events
        self.units, self.display = units, display
        self.pace, self._sleep, self.clock, self.step_s = pace, sleep, clock, step_s

    # helpers
    def nap(self, s):
        if s and s > 0:
            self._sleep(s * self.pace)

    def px(self, pt):
        return ease.scale_point(pt, self.units, self.display) if self.units and self.display else (int(pt[0]), int(pt[1]))

    def _mark(self, mark, default=None, **extra):
        label = mark or default
        if label:
            self.ev.mark(label, **extra)

    def _path(self, tx, ty, steps=None, ms=None):
        x0, y0 = self.x.location()
        n = steps or (ease.steps_for(ms, self.step_s) if ms else ease.default_steps(x0, y0, tx, ty))
        for px, py in ease.eased_path(x0, y0, tx, ty, n):
            self.x.move(px, py)
            self._sleep(self.step_s)

    # actions
    def glide(self, pt, steps=None, ms=None, mark=None, hold=0.0):
        tx, ty = self.px(pt)
        if mark:
            self.ev.mark(mark, x=tx, y=ty, kind='glide')
        self._path(tx, ty, steps, ms)
        self.nap(hold)

    def click(self, pt, button=1, double=False, mark=None, steps=None, ms=None, pre=0.25, hold=0.6):
        tx, ty = self.px(pt)
        self._path(tx, ty, steps, ms)
        self.nap(pre)
        extra = {'x': tx, 'y': ty, 'button': int(button)}
        if double:
            extra['double'] = True
        self.ev.mark(mark or 'click', **extra)
        self.x.click(int(button), 2 if double else 1)
        self.nap(hold)

    def type(self, text, delay_ms=120, mark=None, hold=0.6):
        self._mark(mark, None, text=text)
        self.x.type(text, int(delay_ms))
        self.nap(hold)

    def key(self, keys, mark=None, hold=0.6):
        self._mark(mark, None, keys=keys)
        self.x.key(keys)
        self.nap(hold)

    def drag(self, a, b, button=1, mark=None, steps=None, ms=None, hold=0.6):
        ax, ay = self.px(a)
        bx, by = self.px(b)
        self._path(ax, ay)
        self.nap(0.25)
        label = mark or 'drag'
        self.ev.mark(label, x=ax, y=ay, button=int(button))
        self.x.down(int(button))
        self._sleep(0.1)
        self._path(bx, by, steps or 24, ms)
        self._sleep(0.1)
        self.ev.mark(f'{label}: released', x=bx, y=by, button=int(button))
        self.x.up(int(button))
        self.nap(hold)

    def scroll(self, at, clicks=3, direction='down', mark=None, hold=0.6):
        tx, ty = self.px(at)
        self._path(tx, ty)
        self._mark(mark, None, x=tx, y=ty, clicks=clicks, dir=direction)
        b = 5 if direction == 'down' else 4
        for _ in range(int(clicks)):
            self.x.click(b, 1)
            self._sleep(0.15)
        self.nap(hold)

    def wait(self, s):
        self.nap(s)

    def wake(self, settle=0.3):
        """Repaint nudge for apps that draw only on input: 2 px over and back, then let a frame land."""
        x0, y0 = self.x.location()
        self.x.move(x0 + 2, y0)
        self._sleep(0.08)
        self.x.move(x0, y0)
        self._sleep(settle)

    def mark(self, label, **extra):
        self.ev.mark(label, **extra)
