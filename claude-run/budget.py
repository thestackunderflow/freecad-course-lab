"""The spending ledger (freecad-course-BUDGET.tsv, next to the lab folder; a TSV: run, cost_usd, kind, lab).

The 28 Oct 2026 GO ("GO FreeCAD course lesson 1") set a $1.00 cap for everything logged below the line that
starts with "# --- GO 27 Oct 2026". Paid runs stop at $0.90.
Each later lesson has its own GO line and cap: BUDGET_MARK="# --- GO 27 Oct 2026 L2" counts only lesson 2's rows.

    python budget.py check  LEDGER RUN_CAP [STOP_AT]      exit 0 = may start, 2 = stop
    python budget.py record LEDGER RUN COST_OR_EMPTY RUN_CAP LAB   (empty cost = a killed run, counted at RUN_CAP)
    python budget.py total  LEDGER
"""
import os
import sys

MARK = '# --- GO 28 Oct 2026 FreeCAD L1'
STOP_AT = 0.90


def total(path, mark=None):
    mark = mark or os.environ.get('BUDGET_MARK') or MARK
    if not os.path.exists(path):
        return 0.0
    s, on = 0.0, False
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.startswith(mark):
                on = True
                continue
            if not on or line.startswith('#') or not line.strip():
                continue
            s += float(line.split('\t')[1])
    return round(s, 4)


def allowed(spent, run_cap, stop_at=STOP_AT):
    return spent + run_cap <= stop_at + 1e-9


def record(path, run, cost, run_cap, lab):
    kind = 'logged' if cost is not None else 'killed-floor'
    value = float(cost) if cost is not None else float(run_cap)
    with open(path, 'a', encoding='utf-8', newline='\n') as f:
        f.write(f'{run}\t{value:.4f}\t{kind}\t{lab}\n')
    return total(path)


if __name__ == '__main__':
    cmd, ledger = sys.argv[1], sys.argv[2]
    if cmd == 'check':
        stop = float(sys.argv[4]) if len(sys.argv) > 4 else STOP_AT
        t = total(ledger)
        ok = allowed(t, float(sys.argv[3]), stop)
        print(f'GO-28-Oct spend ${t:.4f}; this run may cost up to ${float(sys.argv[3]):.2f}; stop at ${stop:.2f}: '
              f'{"GO" if ok else "STOP"}')
        sys.exit(0 if ok else 2)
    if cmd == 'record':
        c = sys.argv[4]
        print(f'GO-28-Oct total now ${record(ledger, sys.argv[3], float(c) if c else None, float(sys.argv[5]), sys.argv[6]):.4f}')
    if cmd == 'total':
        print(f'{total(ledger):.4f}')
