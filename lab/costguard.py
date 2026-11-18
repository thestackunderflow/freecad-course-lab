"""Lesson 5: the live cost guard for one paid Claude Code run. While the run is going, it reads Claude Code's own
session log (~/.claude/projects/*/*.jsonl: every assistant message's token usage), estimates the cost, and if the
estimate passes the cap it interrupts the turn (Escape in the run's tmux pane, twice) and writes costguard.json.
/cost at the end of the run stays the number that goes into the ledger; this is only the brake.

Rates per million tokens (fitted to lesson 4's three runs against their /cost lines, then raised ~20% so the guard
errs high): input 3.0, cache write 5.0, cache read 0.15, output 13.0 (any model).
fc12 (18 Nov 2026): with Claude Code 2.1.308 + claude-sonnet-5-5 that raw estimate read 1.82x / 1.81x Claude Code's
own /cost ($0.2089 vs $0.1094, $0.2090 vs $0.1152) and killed both runs ~30 s in. The estimate is now multiplied by
CALIB = 0.6 for that model only (measured /cost-to-raw ratio 0.52-0.55, raised ~10% so it still errs high); other
models keep 1.0 (lesson 4's fit still holds there); env GUARD_CALIB overrides for every model. Claude Code's own --max-budget-usd stays the hard brake on its real cost.
    python3 -m lab.costguard RUN_DIR PANE CAP_USD        (loops until RUN_DIR/.guard-stop exists)"""
import glob
import json
import os
import subprocess
import sys
import time

RATES = {'input_tokens': 3.0, 'cache_creation_input_tokens': 5.0, 'cache_read_input_tokens': 0.15, 'output_tokens': 13.0}
CALIB_BY_MODEL = {'claude-sonnet-5-5': 0.6}
CALIB = float(os.environ['GUARD_CALIB']) if os.environ.get('GUARD_CALIB') else None


def calib_for(model):
    return CALIB if CALIB is not None else CALIB_BY_MODEL.get(model or '', 1.0)


def usage(lines):
    """Sum each assistant message's usage once (Claude Code logs a message in several lines with the same id)."""
    seen, tot = set(), dict.fromkeys(RATES, 0)
    tot['model'] = None
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
        tot['model'] = m.get('model') or tot['model']
        for k in RATES:
            tot[k] += int(u.get(k) or 0)
    return tot


def estimate(tot, calib=None):
    c = calib_for(tot.get('model')) if calib is None else calib
    return round(c * sum(tot[k] * RATES[k] for k in RATES) / 1e6, 4)


def should_stop(tot, cap, calib=None):
    return estimate(tot, calib) > float(cap)


def session_lines(pattern=None):
    out = []
    for p in glob.glob(pattern or os.path.expanduser('~/.claude/projects/*/*.jsonl')):
        out += open(p, encoding='utf-8', errors='replace').read().splitlines()
    return out


def main(run_dir, pane, cap, every=3.0):
    cap = float(cap)
    log = os.path.join(run_dir, 'costguard.json')
    est, tot = 0.0, {}
    while not os.path.exists(os.path.join(run_dir, '.guard-stop')):
        tot = usage(session_lines())
        est = estimate(tot)
        if should_stop(tot, cap):
            for _ in range(2):
                subprocess.run(['tmux', 'send-keys', '-t', pane, 'Escape'])
                time.sleep(0.5)
            json.dump({'stopped': True, 'estimate_usd': est, 'cap_usd': cap, 'calib': calib_for(tot.get('model')), 'at': time.time()}, open(log, 'w'))
            open(os.path.join(run_dir, '.guard-tripped'), 'w').write(str(est))
            return 1
        time.sleep(every)
    json.dump({'stopped': False, 'estimate_usd': est, 'cap_usd': cap, 'calib': calib_for(tot.get('model'))}, open(log, 'w'))
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:4]))
