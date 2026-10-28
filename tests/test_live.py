"""Live checks on a real virtual screen inside the lab image: the filmed-terminal prompt helper (typing a request into a
tmux pane in an xterm, read back from the pane, UTF-8 intact) and a two-window take (FreeCAD-style app window + a
terminal on one display, each focused in turn, both filmed)."""
import json
import os
import shutil
import subprocess
import sys
import time

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, LAB)
from lab import drive  # noqa: E402

pytestmark = pytest.mark.skipif(shutil.which('Xvfb') is None, reason='needs the lab image (Xvfb, xterm, tmux)')


def sh(script, timeout=90):
    r = subprocess.run(['bash', '-c', script], capture_output=True, text=True, timeout=timeout,
                       env=dict(os.environ, SL_DISPLAY=':77'))
    assert r.returncode == 0, r.stdout + r.stderr
    return r.stdout


def test_a_request_typed_into_the_terminal_reads_back_from_the_pane(tmp_path):
    msg = 'make a block 5 by 20 by 60 millimetres in FreeCAD, then tell me its volume (mm³)'
    out = sh(f'''
      export SL_DISPLAY=:77; . /lab/lab/common.sh; sl_display 1600 1000
      term_open tt 0 0 60 20 20 cat
      python3 -c "import sys; sys.path.insert(0, '/lab'); from lab import drive; drive.type_text('tt', {msg!r}, delay=0.005)"
      sleep 0.5; pane tt; tmux kill-server; sl_display_stop
    ''')
    assert msg in ' '.join(out.split()), out


def test_two_windows_are_filmed_and_focused_in_turn(tmp_path):
    d = tmp_path / 'take'
    out = sh(f'''
      export SL_DISPLAY=:77; . /lab/lab/common.sh; sl_display 1600 1000
      term_open left 0 0 40 20 18 bash
      term_open right 800 0 40 20 18 bash
      sl_record {d}
      term_focus left; sl_mark "focus left"; echo "L $(xdotool getwindowfocus getwindowname)"
      term_focus right; sl_mark "focus right"; echo "R $(xdotool getwindowfocus getwindowname)"
      sleep 1; sl_stop; tmux kill-server; sl_display_stop
    ''')
    assert 'L left' in out and 'R right' in out, out
    ev = [json.loads(x)['event'] for x in open(d / 'events.jsonl')]
    assert ev == ['focus left', 'focus right']
    assert (d / 'screen.mp4').stat().st_size > 1000


def test_drive_marks_each_tool_call_once_even_with_a_half_written_line(tmp_path):
    # lab run claude-1: every tool call was marked twice
    t = tmp_path / 'transcript.jsonl'
    call = {'t': '2026-10-28T21:00:00.000+00:00', 'seq': 1, 'dir': 'client->server',
            'msg': {'id': 1, 'method': 'tools/call', 'params': {'name': 'create_object'}}}
    reply = {'t': '2026-10-28T21:00:01.000+00:00', 'seq': 2, 'dir': 'server->client', 'msg': {'id': 1, 'result': {}}}
    r = drive.Run(str(tmp_path), pane_name='nope')
    t.write_text(json.dumps(call) + '\n' + json.dumps(reply)[:20], encoding='utf-8')
    r.tail(); r.tail()
    with open(t, 'a', encoding='utf-8') as f:
        f.write(json.dumps(reply)[20:] + '\n')
    r.tail(); r.tail()
    ev = [json.loads(x)['event'] for x in open(tmp_path / 'events.raw.jsonl')]
    assert ev == ['tool call: create_object', 'tool reply: create_object']


def test_a_second_drive_process_marks_only_calls_after_it_started(tmp_path):
    # lab runs claude-1, fail-1: message 2's drive re-marked message 1's calls
    t = tmp_path / 'transcript.jsonl'
    old = {'t': '2026-10-28T21:00:00.000+00:00', 'seq': 1, 'dir': 'client->server',
           'msg': {'id': 1, 'method': 'tools/call', 'params': {'name': 'list_documents'}}}
    t.write_text(json.dumps(old) + '\n', encoding='utf-8')
    r = drive.Run(str(tmp_path), pane_name='nope')
    new = dict(old, seq=2, msg={'id': 2, 'method': 'tools/call', 'params': {'name': 'create_object'}})
    with open(t, 'a', encoding='utf-8') as f:
        f.write(json.dumps(new) + '\n')
    r.tail()
    ev = [json.loads(x)['event'] for x in open(tmp_path / 'events.raw.jsonl')]
    assert ev == ['tool call: create_object']


def test_drive_events_go_to_the_kits_raw_log_and_survive_finalize(tmp_path):
    # the recorder's finalize rewrites events.jsonl from events.raw.jsonl, so drive writes raw rows (epoch "ts")
    r = drive.Run(str(tmp_path), pane_name='nope')
    now = time.time()
    r.mark('hello', k=1)
    row = json.loads(open(tmp_path / 'events.raw.jsonl').read())
    assert row['event'] == 'hello' and row['k'] == 1 and abs(row['ts'] - now) < 1.0
    from screenlab import logs
    logs.finalize(str(tmp_path), now - 2.0, 'test', (100, 100), 30)
    ev = json.loads(open(tmp_path / 'events.jsonl').read())
    assert ev['event'] == 'hello' and 1.9 < ev['t'] < 3.0
