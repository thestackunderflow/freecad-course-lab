"""fx19 G0a helpers (LAB-fx19 section 1): which line closes the hook, which rule joins it, which end to move.
Pure Python over plain tuples so it is tested without FreeCAD. Constraints are (Type, First, FirstPos, Second, SecondPos).
PosId: 1 = start, 2 = end; GeoId -1 = the sketch's root point (origin), -1/-2 as Second of PointOnObject = H/V axis."""
import math

LENGTH_TYPES = ('Distance', 'DistanceX', 'DistanceY')


def _near(a, b, tol=1e-6):
    return abs(a[0] - b[0]) < tol and abs(a[1] - b[1]) < tol


def closing_line(geo, start=(0, 60), end=(0, 0)):
    """Index of the line whose end points are start -> end (in either order)."""
    hits = [i for i, (p, q) in enumerate(geo)
            if (_near(p, start) and _near(q, end)) or (_near(p, end) and _near(q, start))]
    if len(hits) != 1:
        raise ValueError('closing line not unique: %r' % hits)
    return hits[0]


def on_line(con, line):
    return [i for i, c in enumerate(con) if c[1] == line or (len(c) > 3 and c[3] == line)]


def join_index(con, closing, first):
    """The Coincident joining the closing line's end (2) to the first line's start (1)."""
    hits = [i for i, c in enumerate(con) if c[0] == 'Coincident' and
            ({(c[1], c[2]), (c[3], c[4])} == {(closing, 2), (first, 1)})]
    if len(hits) != 1:
        raise ValueError('join not unique: %r' % hits)
    return hits[0]


def length_sizes(con, line):
    """Length sizes that sit on the closing line alone (both ends on it)."""
    return [i for i, c in enumerate(con) if c[0] in LENGTH_TYPES and c[1] == line and c[3] in (line, -2000)]


def origin_tied_points(con):
    """(GeoId, PosId) points tied to the origin by a root Coincident."""
    out = []
    for c in con:
        if c[0] == 'Coincident' and (c[1], c[2]) == (-1, 1):
            out.append((c[3], c[4]))
        elif c[0] == 'Coincident' and (c[3], c[4]) == (-1, 1):
            out.append((c[1], c[2]))
    return out


def move_plan(con, closing, first, gap):
    """(GeoId, PosId, new point): the closing line's end to (0, gap), or, if that end carries the origin tie,
    the first line's start to (gap, 0). No other branch."""
    tied = origin_tied_points(con)
    if (closing, 2) not in tied:
        return (closing, 2, (0, gap))
    return (first, 1, (gap, 0))


def gap(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])
