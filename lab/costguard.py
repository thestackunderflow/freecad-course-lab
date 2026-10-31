"""Lesson 5: the live cost guard for one paid Claude Code run. While the run is going, it reads Claude Code's own
session log (~/.claude/projects/*/*.jsonl: every assistant message's token usage), estimates the cost, and if the
estimate passes the cap it interrupts the turn (Escape in the run's tmux pane, twice) and writes costguard.json.
/cost at the end of the run stays the number that goes into the ledger; this is only the brake.

Rates per million tokens (fitted to lesson 4's three runs against their /cost lines, then raised ~20% so the guard
errs high): input 3.0, cache write 5.0, cache read 0.15, output 13.0 (any model).
    python3 -m lab.costguard RUN_DIR PANE CAP_USD        (loops until RUN_DIR/.guard-stop exists)"""
import glob
import json
import os
import subprocess
import sys
import time

RATES = {'input_tokens': 3.0, 'cache_creation_input_tokens': 5.0, 'cache_read_input_tokens': 0.15, 'output_tokens': 13.0}


def usage(lines):
    """Sum each assistant message's usage once (Claude Code logs a message in several lines with the same id)."""
    seen, tot = set(), dict.fromkeys(RATES, 0)
    for ln in lines:
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        m = d.get('message') or {}
        u = m.get('usage')
        if d.get('type') != 'assistant' or not u:
            continue
        key = m.get('id') or d.get('uuid')
        if key in seen:
            continue
        seen.add(key)
        for k in RATES:
            tot[k] += int(u.get(k) or 0)
    return tot


def estimate(tot):
    return round(sum(tot[k] * RATES[k] for k in RATES) / 1e6, 4)


def session_lines(pattern=None):
    out = []
    for p in glob.glob(pattern or os.path.expanduser('~/.claude/projects/*/*.jsonl')):
        out += open(p, encoding='utf-8', errors='replace').read().splitlines()
    return out


def main(run_dir, pane, cap, every=3.0):
    cap = float(cap)
    log = os.path.join(run_dir, 'costguard.json')
    est = 0.0
    while not os.path.exists(os.path.join(run_dir, '.guard-stop')):
        est = estimate(usage(session_lines()))
        if est > cap:
            for _ in range(2):
                subprocess.run(['tmux', 'send-keys', '-t', pane, 'Escape'])
                time.sleep(0.5)
            json.dump({'stopped': True, 'estimate_usd': est, 'cap_usd': cap, 'at': time.time()}, open(log, 'w'))
            open(os.path.join(run_dir, '.guard-tripped'), 'w').write(str(est))
            return 1
        time.sleep(every)
    json.dump({'stopped': False, 'estimate_usd': est, 'cap_usd': cap}, open(log, 'w'))
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:4]))
