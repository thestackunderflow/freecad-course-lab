"""Video D probe P2 (plan inputs/video-plans/2026-11-16-video-d PLAN.md 3): pure verdicts on what the FreeCAD 1.1.4 Measure
panel shows (the `task_texts()` line the take logs, e.g. "combo:Distance field:0.40 mm") and on the ladder numbers."""
import re

TOL = 0.01


def field_mm(text):
    """The distance a Measure panel line shows, in mm; None when it shows no distance (a volume, an area, nothing)."""
    m = re.search(r'combo:Distance[^ ]*\s+field:\s*(-?[0-9.]+)\s*mm(?!\^)', text or '')
    return float(m.group(1)) if m else None


def s2(whole_body_text):
    """S2 fires only if Measure on the two whole bodies gives a distance (the nearest in one step)."""
    d = field_mm(whole_body_text)
    return 'S2 not hit' if d is None else f'S2 HIT: whole bodies give {d:.2f} mm in one step'


def sign_issue(typo_mm, positive_mm):
    """True when the typo rung (head 0.2 too narrow) reads the same as a +0.2 gap: Measure carries no sign."""
    if typo_mm is None or positive_mm is None:
        return None
    return abs(typo_mm - positive_mm) <= TOL


def agrees(a, b):
    return a is not None and b is not None and abs(a - b) <= TOL
