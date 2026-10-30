"""The filmed-terminal prompt helper (ported from the SolidCraft course lab's l2drive.py): drive one Claude Code session
in its real terminal (tmux inside an xterm on the filmed display). It types each message as a person would (one
character at a time into the pane, UTF-8), presses Enter, then only waits: it reads the screen (tmux capture-pane) to
see when Claude is working or shows a permission prompt (answered with the prompt's own plain "Yes" after 1.5 s), and
tails the logging proxy's transcript to mark each tool call. Events go to events.jsonl in seconds from T0 (the
recording's first frame), so the footage can be cut by event: rows are written to the screen-lab kit's raw log
(events.raw.jsonl, wall-clock "ts"), which the recorder rebases into events.jsonl when it stops.

    python3 -m lab.drive RUN_DIR PANE "message 1" ["message 2" ...]
    (env DRIVE_BETWEEN="cmd" runs a shell command between messages, e.g. a click in FreeCAD)"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client import tui  # noqa: E402

TURN_LIMIT_S = 420
QUIET_S = 4.0


def pane(name, full=False):
    a = ['tmux', 'capture-pane', '-p', '-t', name] + (['-S', '-3000'] if full else [])
    return subprocess.run(a, capture_output=True, text=True).stdout


def keys(name, *k, literal=False):
    subprocess.run(['tmux', 'send-keys', '-t', name] + (['-l'] if literal else []) + list(k), check=True)


def type_text(name, text, delay=0.045):
    """Type text into a tmux pane one character at a time (what a person typing would send)."""
    for ch in text:
        keys(name, ch, literal=True)
        time.sleep(delay)


class Run:
    def __init__(self, out, pane_name='cc'):
        self.out, self.pane = out, pane_name
        os.makedirs(out, exist_ok=True)
        self.ev = open(os.path.join(out, 'events.raw.jsonl'), 'a')
        self.tpath = os.path.join(out, 'transcript.jsonl')
        self.tpos = os.path.getsize(self.tpath) if os.path.exists(self.tpath) else 0   # only rows after we started
        self.calls = {}

    def mark(self, what, **kw):
        row = {'ts': time.time(), 'event': what}
        row.update(kw)
        self.ev.write(json.dumps(row) + '\n')
        self.ev.flush()

    def tail(self):
        """New proxy rows: mark tools/call requests and their replies (at the proxy's own UTC time). Reads by byte
        offset and only whole lines, so a line the proxy is still writing is read once, on a later call."""
        if not os.path.exists(self.tpath):
            return
        with open(self.tpath, 'rb') as f:
            f.seek(self.tpos)
            data = f.read()
        end = data.rfind(b'\n') + 1
        self.tpos += end
        for raw in data[:end].splitlines():
            try:
                r = json.loads(raw.decode('utf-8', errors='replace'))
            except ValueError:
                continue
            m = r.get('msg') if isinstance(r, dict) else None
            if not isinstance(m, dict):
                continue
            t = datetime.fromisoformat(r['t']).timestamp()
            if r.get('dir') == 'client->server' and m.get('method') == 'tools/call':
                name = (m.get('params') or {}).get('name')
                self.calls[m.get('id')] = name
                self.ev.write(json.dumps({'ts': t, 'event': f'tool call: {name}', 'seq': r.get('seq')}) + '\n')
            elif r.get('dir') == 'server->client' and m.get('id') in self.calls:
                name = self.calls.pop(m.get('id'))
                err = bool((m.get('result') or {}).get('isError')) or 'error' in m
                self.ev.write(json.dumps({'ts': t, 'event': f'tool reply: {name}', 'seq': r.get('seq'),
                                          'isError': err}) + '\n')
        self.ev.flush()

    def say(self, n, msg):
        self.mark(f'turn {n}: typing', text=msg)
        type_text(self.pane, msg)
        time.sleep(0.8)
        done_before = pane(self.pane, full=True)
        self.mark(f'turn {n}: Enter')
        keys(self.pane, 'Enter')
        start, seen_busy, quiet_since, approvals = time.time(), False, None, 0
        while time.time() - start < TURN_LIMIT_S:
            time.sleep(0.4)
            self.tail()
            text = pane(self.pane)
            if tui.approval(text):
                k = tui.approval_key(text)
                self.mark(f'turn {n}: approval asked', key=k, tool=tui.approval_tool(text))
                open(os.path.join(self.out, f'approval-{n}-{approvals + 1}.txt'), 'w').write(text)
                time.sleep(1.5)
                keys(self.pane, k)
                self.mark(f'turn {n}: approval answered', key=k)
                approvals += 1
                quiet_since = None
                continue
            if tui.new_turn_end(done_before, pane(self.pane, full=True)) and not self.calls:
                self.mark(f'turn {n}: end-of-turn line seen')
                time.sleep(2.0)
                break
            if tui.busy(text):
                if not seen_busy:
                    self.mark(f'turn {n}: Claude working')
                seen_busy, quiet_since = True, None
            elif seen_busy and not self.calls:
                quiet_since = quiet_since or time.time()
                if time.time() - quiet_since >= QUIET_S:
                    break
        self.tail()
        self.mark(f'turn {n}: reply done', approvals=approvals, timed_out=time.time() - start >= TURN_LIMIT_S)
        open(os.path.join(self.out, f'pane-turn{n}.txt'), 'w').write(pane(self.pane))


def main(out, pane_name, messages):
    r = Run(out, pane_name)
    between = os.environ.get('DRIVE_BETWEEN')
    for i, m in enumerate(messages, 1):
        if i > 1 and between:
            r.mark(f'between {i - 1} and {i}: start')
            subprocess.run(['bash', '-c', between])
            r.mark(f'between {i - 1} and {i}: done')
        r.say(i, m)
        time.sleep(3.0)
    open(os.path.join(out, 'pane-full.txt'), 'w').write(pane(pane_name, full=True))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
