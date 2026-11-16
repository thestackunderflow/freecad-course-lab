"""Video D probe P2 (plan inputs/video-plans/2026-11-16-video-d PLAN.md 3): the pure verdicts of lab/p2verdict.py.
Run: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_p2verdict.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lab'))
import p2verdict as v  # noqa: E402


def test_field_mm_reads_the_measure_panel():
    assert v.field_mm('combo:Distance field:0.40 mm ') == 0.4
    assert v.field_mm('combo:Volume field:16204.00 mm^3') is None
    assert v.field_mm('') is None


def test_s2_not_hit_when_whole_bodies_give_no_distance():
    assert v.s2('combo:Volume field:28204.00 mm^3') == 'S2 not hit'
    assert v.s2('') == 'S2 not hit'
    assert v.s2('combo:Distance Free field:0.00 mm ') == 'S2 not hit'   # P2F: two picked points, not the nearest


def test_s2_hit_when_whole_bodies_give_a_distance():
    assert v.s2('combo:Distance field:0.20 mm').startswith('S2 HIT')


def test_sign_issue_when_typo_reads_like_a_positive_gap():
    assert v.sign_issue(0.2, 0.2) is True
    assert v.sign_issue(0.0, 0.2) is False
    assert v.sign_issue(None, 0.2) is None


def test_side_agrees_within_001():
    assert v.agrees(0.4, 0.40000001) is True and v.agrees(0.39, 0.4) is False
