"""Task R (14 Nov 2026): does freecad-mcp 0.1.31 change what a beginner sees in fc1/fc7, and does uvx start it.
Reads out/r031/evidence.json (written by lab/r031_probe.sh) and writes out/r031/verdict.json.

    python3 -m lab.r031 out/r031
"""
import json
import os
import re
import sys

# What fc1/fc7 show on screen with 0.1.28 (the filmed words).
FILMED = {'workbench_menu': 'MCP Addon', 'Start_RPC_Server': 'Start RPC Server', 'Stop_RPC_Server': 'Stop RPC Server'}


def rpc_started(report):
    m = re.search(r'RPC Server started at (\S+):(\d+)', report or '')
    return (m.group(1), int(m.group(2))) if m else None


def mcp_connected(text, name):
    for line in (text or '').splitlines():
        if line.startswith(name + ':'):
            return 'Connected' in line and 'Failed' not in line
    return False


def tool_diff(a, b):
    return {'added': sorted(set(b) - set(a)), 'removed': sorted(set(a) - set(b))}


def verdict(ev):
    reasons = []
    if ev.get('workbench_menu') != FILMED['workbench_menu']:
        reasons.append(f"workbench name is {ev.get('workbench_menu')!r}, filmed 'MCP Addon'")
    cmds = ev.get('commands') or {}
    for cmd in ('Start_RPC_Server', 'Stop_RPC_Server'):
        if cmds.get(cmd) != FILMED[cmd]:
            reasons.append(f"{cmd} menu text is {cmds.get(cmd)!r}, filmed {FILMED[cmd]!r}")
    if rpc_started(ev.get('report')) is None:
        reasons.append("no 'RPC Server started at' line in the Report view")
    if not mcp_connected(ev.get('mcp_list'), 'freecad'):
        reasons.append("claude mcp list does not show freecad Connected")
    return {
        'q2_beginner_change': bool(reasons),
        'q5_starts': bool(ev.get('initialize_ok')) and bool(ev.get('tools31')),
        'reasons': reasons,
        'tools': tool_diff(ev.get('tools28') or [], ev.get('tools31') or []),
    }


def main(out):
    with open(os.path.join(out, 'evidence.json')) as f:
        v = verdict(json.load(f))
    with open(os.path.join(out, 'verdict.json'), 'w') as f:
        json.dump(v, f, indent=1)
    print(json.dumps({k: v[k] for k in ('q2_beginner_change', 'q5_starts', 'reasons')}))


if __name__ == '__main__':
    main(sys.argv[1])
