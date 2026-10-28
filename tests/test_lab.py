"""Lesson 1 lab checks (unit tests; no display, no network, no Claude)."""
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, LAB)
sys.path.insert(0, os.path.join(LAB, 'claude-run'))

from checker import compare  # noqa: E402
from client import replay, tui  # noqa: E402
import budget  # noqa: E402

# Claude Code 2.1.308 screens (tmux capture-pane text, from the lab's dev probe, 28 Oct 2026)
IDLE_308 = """  tmux detected · scroll with PgUp/PgDn · o…
──────────────────────────────────────────────
❯ Try "how do I log an error?"
──────────────────────────────────────────────
  ⏵⏵ auto mode on (shift+tab to cycle)"""
BUSY = """✻ Thinking… (esc to interrupt)
──────────────────────────────────────────────
❯
──────────────────────────────────────────────"""
ASK = """ Tool use
   freecad - execute_code (MCP)
 Do you want to proceed?
 ❯ 1. Yes
   2. Yes, and don't ask again for freecad - execute_code commands in /home/maker/hook
   3. No, and tell Claude what to do differently (esc)"""
DONE = """  The block is 6000 mm³.

✻ Worked for 9s · done 9:10 PM

──────────────────────────────────────────────
❯"""


def test_busy_and_idle():
    assert tui.busy(BUSY) and not tui.busy(IDLE_308)


def test_an_approval_is_answered_with_its_plain_yes_never_dont_ask_again():
    assert tui.approval(ASK) and not tui.approval(IDLE_308)
    assert tui.approval_key(ASK) == '1'
    assert tui.approval_tool(ASK) == 'freecad - execute_code'


def test_end_of_turn_lines_are_counted():
    assert tui.turns_done(DONE) == 1 and tui.turns_done(IDLE_308) == 0
    assert tui.turns_done(DONE + '\n✻ Baked for 1m 3s · done 9:12 PM') == 2
    # lab run claude-1 (2.1.308): the verb had a non-ASCII letter and the turn was never seen to end
    assert tui.turns_done('✻ Sautéed for 12s · done 9:39 PM') == 1


def _measure(vol, bbox, z, doc='Unnamed', name='Box', label='Cube'):
    return {'document': doc, 'freecad': '1.1.4', 'objects': [name],
            'solids': [{'name': name, 'label': label, 'volume_mm3': vol, 'valid': True, 'solids': 1,
                        'bbox_mm': bbox, 'z_range_mm': z}]}


def test_compare_same_block_is_a_match_whatever_its_name():
    a = _measure(6000.0, [5.0, 20.0, 60.0], [0.0, 60.0])
    b = _measure(6000.0000000001, [5.0, 20.0, 60.0], [0.0, 60.0], doc='Unnamed1', name='Block', label='Block')
    r = compare.compare(a, b, expected=6000.0)
    assert r['same'] is True
    assert r['rows']['volume'] == {'hand': 6000.0, 'claude': 6000.0, 'expected': 6000.0, 'ok': True}
    assert r['rows']['up'] == {'hand': [0.0, 60.0], 'claude': [0.0, 60.0], 'ok': True}


def test_compare_reports_the_one_difference_plainly():
    a = _measure(6000.0, [5.0, 20.0, 60.0], [0.0, 60.0])
    b = _measure(6000.0, [60.0, 20.0, 5.0], [0.0, 5.0])
    r = compare.compare(a, b, expected=6000.0)
    assert r['same'] is False
    assert r['rows']['size']['ok'] is False and r['rows']['volume']['ok'] is True
    assert 'size' in r['differences']


def test_compare_size_ignores_axis_order_only_when_asked():
    a = _measure(6000.0, [5.0, 20.0, 60.0], [0.0, 60.0])
    b = _measure(6000.0, [20.0, 5.0, 60.0], [0.0, 60.0])
    assert compare.compare(a, b, 6000.0)['rows']['size']['ok'] is False
    assert compare.compare(a, b, 6000.0, any_axis_order=True)['rows']['size']['ok'] is True


def test_compare_needs_exactly_one_solid_each():
    a = _measure(6000.0, [5.0, 20.0, 60.0], [0.0, 60.0])
    two = dict(a, solids=a['solids'] * 2)
    with pytest.raises(ValueError):
        compare.compare(a, two, 6000.0)


def test_replay_takes_only_tools_call_requests_in_order(tmp_path):
    p = tmp_path / 't.jsonl'
    rows = [
        {'seq': 1, 'dir': 'proxy', 'msg': {'start': ['uvx']}},
        {'seq': 2, 'dir': 'client->server', 'msg': {'jsonrpc': '2.0', 'id': 0, 'method': 'initialize', 'params': {}}},
        {'seq': 3, 'dir': 'client->server', 'msg': {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'}},
        {'seq': 4, 'dir': 'client->server', 'msg': {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
                                                    'params': {'name': 'create_document', 'arguments': {'name': 'Hook'}}}},
        {'seq': 5, 'dir': 'server->client', 'msg': {'jsonrpc': '2.0', 'id': 2, 'result': {}}},
        {'seq': 6, 'dir': 'client->server', 'msg': {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call',
                                                    'params': {'name': 'create_object', 'arguments': {'doc_name': 'Hook'}}}},
    ]
    p.write_text('\n'.join(json.dumps(r) for r in rows) + '\nnot json\n', encoding='utf-8')
    calls = replay.logged_calls(str(p))
    assert [(c['seq'], c['name']) for c in calls] == [(4, 'create_document'), (6, 'create_object')]
    assert calls[0]['arguments'] == {'name': 'Hook'}


def test_tool_panel_rows_pair_each_call_with_its_reply(tmp_path):
    p = tmp_path / 't.jsonl'
    rows = [
        {'t': '2026-10-28T21:00:00.000+00:00', 'seq': 7, 'dir': 'client->server',
         'msg': {'id': 5, 'method': 'tools/call', 'params': {'name': 'list_documents', 'arguments': {}}}},
        {'t': '2026-10-28T21:00:00.400+00:00', 'seq': 8, 'dir': 'server->client',
         'msg': {'id': 5, 'result': {'content': [{'type': 'text', 'text': '["Unnamed"]'},
                                                  {'type': 'image', 'data': {'bytes': 10, 'saved_as': 'claude-shot-01.png'}}],
                                     'isError': False}}},
    ]
    p.write_text('\n'.join(json.dumps(r) for r in rows) + '\n', encoding='utf-8')
    pairs = replay.call_pairs(str(p))
    assert pairs == [{'call_seq': 7, 'reply_seq': 8, 'name': 'list_documents', 'arguments': {}, 'isError': False,
                      'text': '["Unnamed"]', 'images': ['claude-shot-01.png'], 'seconds': 0.4}]


def test_budget_counts_only_this_lessons_rows_and_stops_at_090(tmp_path):
    p = tmp_path / 'b.tsv'
    p.write_text('# run\tcost_usd\tkind\tlab\n' + budget.MARK + ' cap $1.00\nfc1-a\t0.20\tlogged\tfc1\n', encoding='utf-8')
    assert budget.MARK.startswith('# --- GO 28 Oct 2026 FreeCAD L1')
    assert budget.total(str(p)) == 0.2
    assert budget.allowed(0.20, 0.30) and not budget.allowed(0.70, 0.30)
    assert budget.record(str(p), 'fc1-b', None, 0.30, 'fc1') == 0.5   # a killed run counts at its cap
