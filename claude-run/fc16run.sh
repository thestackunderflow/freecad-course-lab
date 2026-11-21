#!/usr/bin/env bash
# fc16 Claude runs (PLAN 2.5/4.3): FC16_ENV=<path to a .env> bash claude-run/fc16run.sh A1|B1. Cap $0.25 per run, $0.50 the
# stage (hard cap). lab/fc16_R.sh in fcc-app:1.1.4-0.1.28 with the network. API key: ONLY ANTHROPIC_API_KEY read from the
# .env named by FC16_ENV (no default: set it at run time) in-process, exported to this shell and handed to the container
# as an env var by name (-e NAME); never printed or written.
set -euo pipefail
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
RUN=$1; S=out/fc16/runs/$RUN
LEDGER="$LAB/../freecad-course-BUDGET.tsv"; CAP=${CAP:-0.25}; TOTAL=0.50
export BUDGET_MARK="# --- GO 21 Nov 2026 fc16"
[ -e "$S/events.jsonl" ] && { echo "refusing to overwrite $S"; exit 3; }
ENVF="${FC16_ENV:?set FC16_ENV to the .env path at run time}"
grep -qF "$BUDGET_MARK" "$LEDGER" || echo "$BUDGET_MARK (lab stage: runs A1 + B1, cap $CAP each, $TOTAL total, on the PC; guard CALIB 0.6)" >> "$LEDGER"
python claude-run/budget.py check "$LEDGER" "$CAP" "$TOTAL" || { echo "BUDGET STOP"; exit 2; }
ANTHROPIC_API_KEY="$(python -c "
import sys
for ln in open(sys.argv[1], encoding='utf-8'):
    if ln.startswith('ANTHROPIC_API_KEY='):
        sys.stdout.write(ln.split('=', 1)[1].strip().strip(chr(34)).strip(chr(39))); break" "$ENVF")"
[ -n "$ANTHROPIC_API_KEY" ] || { echo "no key"; exit 2; }
export ANTHROPIC_API_KEY
mkdir -p "$S"; T0=$(date +%s)
MSYS_NO_PATHCONV=1 docker run --rm --name fc16-claude --hostname pc --user maker --memory 6g --shm-size 1g \
  -e CAP=$CAP -e ANTHROPIC_API_KEY -v "$LAB:/lab" -w /lab fcc-app:1.1.4-0.1.28 bash /lab/lab/fc16_R.sh "$RUN" \
  > "$S.container.log" 2>&1 || echo "container exit $?"
mv "$S.container.log" "$S/container.log" 2>/dev/null || true
COST=$(python -c "
import re,os,sys; p=sys.argv[1]+'/pane-cost.txt'; t=open(p,encoding='utf-8',errors='replace').read() if os.path.exists(p) else ''
m=re.findall(r'[\$]([0-9]+[.][0-9]+)',t); print(m[0] if m else '')" "$S")
echo "{\"run\": \"$RUN\", \"wall_s\": $(( $(date +%s) - T0 )), \"cost_usd\": \"$COST\", \"launch\": \"claude --model claude-sonnet-5-5 --strict-mcp-config --mcp-config entry.json (freecad only) --max-budget-usd $CAP --max-turns 40\"}" > "$S/meta.json"
python claude-run/budget.py record "$LEDGER" "fc16-$RUN" "$COST" "$CAP" fc16-lesson16
python claude-run/scrub.py "$S"
echo "cost $COST" | tee "$S/cost.txt"
