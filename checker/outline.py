"""Lesson 2: the J outline as the walk a viewer types (one line at a time: a direction and a length), and the numbers
SolidCraft should report for it, worked out here without SolidCraft: the profile area (shoelace rule), the bounding
box and the volume of the outline extruded by a width.

The J (side view, millimetres): back plate 60 tall and 5 thick, hook arm 25 deep (wall to the lip's front) and 5
thick, lip 10 high (from the bottom). Start at the origin, the bottom-left corner on the wall side."""

J_MOVES = [('right', 25), ('up', 10), ('left', 5), ('down', 5), ('left', 15), ('up', 55), ('left', 5), ('down', 60)]
STEP = {'right': (1, 0), 'left': (-1, 0), 'up': (0, 1), 'down': (0, -1)}


def walk(moves, start=(0.0, 0.0)):
    pts = [(float(start[0]), float(start[1]))]
    for d, n in moves:
        dx, dy = STEP[d]
        x, y = pts[-1]
        pts.append((x + dx * n, y + dy * n))
    return pts


def bbox(pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return (min(xs), min(ys)), (max(xs), max(ys))


def area(pts):
    s = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        s += x0 * y1 - x1 * y0
    return abs(s) / 2.0


def expected(moves, width):
    pts = walk(moves)
    if pts[-1] != pts[0]:
        raise ValueError(f'the outline does not close: it ends at {pts[-1]}, not {pts[0]}')
    (x0, y0), (x1, y1) = bbox(pts)
    a = area(pts)
    return {'area_mm2': a, 'width_mm': float(width), 'volume_mm3': a * width,
            'bbox_mm': [x1 - x0, float(width), y1 - y0], 'vertices': pts}


def free_sizes(moves):
    """How many sizes stay free once every line is level or upright and the start sits on the origin: each distinct x
    position and each distinct y position is one unknown, minus the origin's own x and y (FreeCAD reports the same as
    the degrees of freedom left before any length is typed)."""
    pts = walk(moves)[:-1]
    return (len({p[0] for p in pts}) - 1) + (len({p[1] for p in pts}) - 1)


# ---- lesson 3: the same walk written from five named sizes (a FreeCAD spreadsheet's aliases) -------------------
NAMED_WALK = [('right', 'hook_depth'), ('up', 'lip_height'), ('left', 'thickness'), ('down', 'lip_height - thickness'),
              ('left', 'hook_depth - 2 * thickness'), ('up', 'plate_height - thickness'), ('left', 'thickness'),
              ('down', 'plate_height')]
# the six sizes lesson 2 pinned by hand (in its order) and the name or formula each one takes in lesson 3
PINNED_SIZES = [('bottom', 'hook_depth'), ('lip height', 'lip_height'), ('lip width', 'thickness'),
                ('lip inside (lip_height - thickness)', 'lip_height - thickness'), ('back plate height', 'plate_height'),
                ('back plate thickness', 'thickness')]


def _eval(expr, names):
    return float(eval(expr, {'__builtins__': {}}, dict(names)))   # only names and + - * from the table above


def named_moves(names):
    """The walk with each length worked out from the named sizes (lengths as numbers, like J_MOVES)."""
    out = []
    for d, expr in NAMED_WALK:
        v = _eval(expr, names)
        out.append((d, int(v) if v == int(v) else v))
    return out


def uses_of(name):
    """Which of lesson 2's six pinned sizes a name drives."""
    return [label for label, expr in PINNED_SIZES if name in expr.replace('-', ' ').split()]
