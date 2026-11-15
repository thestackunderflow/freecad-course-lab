"""Task R (14 Nov 2026): freecad-mcp 0.1.31 vs 0.1.28 on the fc1/fc7 steps. lab/r031.py reads the probe's evidence
(lab/r031_probe.sh, out/r031/) and says whether a beginner sees a change (Q2) and whether uvx starts it (Q5).
Run: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_r031.py"""
import json
import os

import pytest

from lab import r031

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'r031')

GOOD = {
    'workbench_menu': 'MCP Addon',
    'commands': {'Start_RPC_Server': 'Start RPC Server', 'Stop_RPC_Server': 'Stop RPC Server'},
    'report': 'Workbench loaded\nRPC Server started at 127.0.0.1:9875 (PID 42).\n',
    'initialize_ok': True,
    'tools28': ['create_document', 'execute_code', 'get_objects'],
    'tools31': ['create_document', 'execute_code', 'get_objects'],
    'mcp_list': 'Checking MCP server health...\n\nfreecad: uvx freecad-mcp@0.1.31 - ✓ Connected\n',
}


def test_rpc_started_reads_the_report_line():
    assert r031.rpc_started(GOOD['report']) == ('127.0.0.1', 9875)
    assert r031.rpc_started('nothing here') is None


def test_mcp_connected():
    assert r031.mcp_connected(GOOD['mcp_list'], 'freecad') is True
    assert r031.mcp_connected('freecad: uvx freecad-mcp@0.1.31 - ✗ Failed to connect', 'freecad') is False
    assert r031.mcp_connected('', 'freecad') is False


def test_tool_diff():
    assert r031.tool_diff(['a', 'b'], ['b', 'c']) == {'added': ['c'], 'removed': ['a']}


def test_verdict_no_change_and_starts():
    v = r031.verdict(GOOD)
    assert v['q2_beginner_change'] is False and v['q5_starts'] is True and v['reasons'] == []


@pytest.mark.parametrize('key,value,reason', [
    ('workbench_menu', 'FreeCAD MCP', 'workbench'),
    ('commands', {'Start_RPC_Server': 'Start MCP Server'}, 'Start RPC Server'),
    ('report', 'no line', 'RPC'),
    ('mcp_list', 'freecad: x - ✗ Failed to connect', 'Connected'),
])
def test_verdict_flags_each_visible_change(key, value, reason):
    v = r031.verdict(dict(GOOD, **{key: value}))
    assert v['q2_beginner_change'] is True
    assert any(reason in r for r in v['reasons'])


def test_verdict_uvx_not_starting():
    v = r031.verdict(dict(GOOD, initialize_ok=False, tools31=[]))
    assert v['q5_starts'] is False


def test_probe_evidence_once_written():
    p = os.path.join(OUT, 'evidence.json')
    if not os.path.exists(p):
        pytest.skip('probe not run yet')
    with open(p) as f:
        ev = json.load(f)
    v = r031.verdict(ev)
    with open(os.path.join(OUT, 'verdict.json')) as f:
        assert json.load(f) == v
