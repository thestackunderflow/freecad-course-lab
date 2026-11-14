"""fx19 (Pad "Wire is not closed."): pure helpers that pick what G0a deletes and moves (LAB-fx19 section 1)."""
from lab import fx19geom as g

# lesson 2's hand.FCStd sketch, as dumped by freecadcmd (end points in sketch x, y)
GEO = [((0, 0), (25, 0)), ((25, 0), (25, 10)), ((25, 10), (20, 10)), ((20, 10), (20, 5)),
       ((20, 5), (5, 5)), ((5, 5), (5, 60)), ((5, 60), (0, 60)), ((0, 60), (0, 0))]
# (Type, First, FirstPos, Second, SecondPos)
CON = [('Coincident', -1, 1, 0, 1), ('PointOnObject', 0, 2, -1, 0), ('Coincident', 0, 2, 1, 1),
       ('Vertical', 1, 0, -2000, 0), ('Coincident', 6, 2, 7, 1), ('Coincident', 7, 2, 0, 1),
       ('Vertical', 7, 0, -2000, 0), ('DistanceY', 0, 1, 6, 2, ), ('DistanceY', 7, 1, 7, 2)]


def test_closing_line_found_by_end_points():
    assert g.closing_line(GEO) == 7


def test_constraints_on_line():
    assert g.on_line(CON, 7) == [4, 5, 6, 8]


def test_join_is_only_the_coincident_closing_end_to_first_start():
    assert g.join_index(CON, 7, 0) == 5


def test_length_sizes_on_closing_line():
    assert g.length_sizes(CON, 7) == [8]


def test_origin_tie_is_on_first_line_start():
    assert g.origin_tied_points(CON) == [(0, 1)]


def test_move_closing_end_when_it_is_free():
    assert g.move_plan(CON, 7, 0, 0.5) == (7, 2, (0, 0.5))


def test_move_first_start_when_closing_end_is_tied():
    con = [('Coincident', -1, 1, 7, 2)]
    assert g.move_plan(con, 7, 0, 0.5) == (0, 1, (0.5, 0))


def test_gap():
    assert abs(g.gap((0, 0.5), (0, 0)) - 0.5) < 1e-12


def test_the_text_button_query_names_the_text_and_compiles():
    from lab import button
    code = button.TEXT.format(text='OK')
    assert "'OK'" in code and 'QAbstractButton' in code
    compile(code, 'q', 'exec')


def test_redact_drops_context_lines_and_keeps_the_turn():
    import json
    from lab import fx19redact as r
    rows = [{'type': 'attachment', 'attachment': {'type': 'skill_listing', 'x': 'Goo' + 'gle Dr' + 'ive'}},
            {'type': 'attachment', 'attachment': {'type': 'session_context', 'x': 'a@b.com'}},
            {'type': 'api-request-shape', 'shape': 'claude' + '_ai_X'}, {'type': 'api-request-blob', 'b': 'Cla' + 'ude Do' + 'cs'},
            {'type': 'user', 'message': {'role': 'user', 'content': 'Pad the sketch in this document 20 mm.'}},
            {'type': 'assistant', 'message': {'model': 'claude-sonnet-5-5', 'content': []}}]
    kept, dropped = r.redact([json.dumps(x) for x in rows])
    assert dropped == 4 and len(kept) == 2
    assert not r.leaks(kept)
    assert r.leaks(['x drive' + 'mcp y'])
