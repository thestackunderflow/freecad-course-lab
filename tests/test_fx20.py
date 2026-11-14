"""fx20 ("Negative datum values ..."): pure helpers that find the arm-top line and the bottom size (LAB-fx20 0, 1)."""
import pytest

from lab import fx20geom as g

# lesson 2's hand.FCStd sketch end points (as fx19's G0a dumped them)
GEO = [((0, 0), (25, 0)), ((25, 0), (25, 10)), ((25, 10), (20, 10)), ((20, 10), (20, 5)),
       ((20, 5), (5, 5)), ((5, 5), (5, 60)), ((5, 60), (0, 60)), ((0, 60), (0, 0))]
CON = [('Coincident', -1, 1, 0, 1), ('DistanceX', 0, 1, 0, 2), ('Coincident', 3, 2, 4, 1),
       ('Horizontal', 4, 0, -2000, 0), ('DistanceY', 7, 1, 7, 2), ('Distance', 2, 1, 2, 2)]


def test_arm_top_found_by_end_points_either_order():
    assert g.line_by_ends(GEO, (20, 5), (5, 5)) == 4
    assert g.line_by_ends(GEO, (5, 5), (20, 5)) == 4


def test_line_by_ends_refuses_missing():
    with pytest.raises(ValueError):
        g.line_by_ends(GEO, (1, 1), (2, 2))


def test_bottom_line():
    assert g.line_by_ends(GEO, (0, 0), (25, 0)) == 0


def test_length_sizes_on_line():
    assert g.length_sizes(CON, 0) == [1]
    assert g.length_sizes(CON, 4) == []
    assert g.length_sizes(CON, 2) == [5]


def test_arm_top_length_is_bottom_minus_lip_minus_back():
    assert g.arm_top(25, 5, 5) == 15
    assert g.arm_top(27, 5, 5) == 17
