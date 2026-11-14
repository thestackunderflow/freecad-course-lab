"""fx20 helpers (LAB-fx20 sections 0-1): find a hook line by its end points and the length sizes sitting on it.
Pure Python over plain tuples so it is tested without FreeCAD. Constraints are (Type, First, FirstPos, Second, SecondPos)."""
from lab.fx19geom import LENGTH_TYPES, _near


def line_by_ends(geo, a, b):
    """Index of the one line whose end points are a and b (either order); geometry indices are never assumed."""
    hits = [i for i, (p, q) in enumerate(geo) if (_near(p, a) and _near(q, b)) or (_near(p, b) and _near(q, a))]
    if len(hits) != 1:
        raise ValueError('line %r-%r not unique: %r' % (a, b, hits))
    return hits[0]


def length_sizes(con, line):
    """Length sizes measured along one line (both ends on it)."""
    return [i for i, c in enumerate(con) if c[0] in LENGTH_TYPES and c[1] == line and c[3] in (line, -2000)]


def arm_top(bottom, lip, back):
    """The arm's top has no size of its own: bottom minus lip minus back plate."""
    return bottom - lip - back
