"""Mouse paths a viewer can follow: a straight line, eased in and out (cosine), about 30 ms a step."""
import math

STEP_S = 0.03


def eased_path(x0, y0, x1, y1, steps):
    """`steps` integer points from just after (x0, y0) to exactly (x1, y1)."""
    steps = max(1, int(steps))
    out = []
    for i in range(1, steps + 1):
        e = (1 - math.cos(math.pi * i / steps)) / 2
        out.append((int(round(x0 + (x1 - x0) * e)), int(round(y0 + (y1 - y0) * e))))
    out[-1] = (int(x1), int(y1))
    return out


def steps_for(ms, step_s=STEP_S):
    return max(1, int(round(ms / 1000 / step_s)))


def default_steps(x0, y0, x1, y1):
    """A glide's length from its distance: 12 steps for a short hop up to 36 across the screen."""
    d = math.hypot(x1 - x0, y1 - y0)
    return int(min(36, max(12, 12 + d / 60)))


def scale_point(pt, units, display):
    if not units:
        return int(pt[0]), int(pt[1])
    return (int(round(pt[0] * display[0] / units[0])), int(round(pt[1] * display[1] / units[1])))
