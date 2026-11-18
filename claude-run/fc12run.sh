#!/usr/bin/env bash
# fc12 Claude runs (PLAN 2.5/4.3): bash claude-run/fc12run.sh A1|B1. Cap $0.20 per run, $0.40 the stage (hard cap).
# lab/fc12_R.sh in fcc-app:1.1.4-0.1.28 with the network. API key: ONLY ANTHROPIC_API_KEY read from the owner's .env
# in-process, exported to this shell and handed to the container as an env var by name (-e NAME); never printed or written.
set -euo pipefail
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
RUN=$1; S=out/fc12/runs/$RUN
LEDGER="$LAB/../freecad-course-BUDGET.tsv"; CAP=${CAP:-0.20}; TOTAL=0.40
export BUDGET_MARK="# --- GO 17 Nov 2026 fc12"
case $RUN in *-2) CAP=0.25; TOTAL=0.50; BUDGET_MARK="# --- GO 18 Nov 2026 fc12 rerun";; esac   # run 2: own GO line, $0.25 each, $0.50 total
[ -e "$S/events.jsonl" ] && { echo "refusing to overwrite $S"; exit 3; }
grep -qF "$BUDGET_MARK" "$LEDGER" || echo "$BUDGET_MARK (lab stage: runs A1 + B1 (or A1-2 + B1-2), cap $CAP each, $TOTAL total, on the PC; guard CALIB 0.6)" >> "$LEDGER"
python claude-run/budget.py check "$LEDGER" "$CAP" "$TOTAL" || { echo "BUDGET STOP"; exit 2; }
ENVF="${FC12_ENV:-path/to/your/.env}"
ANTHROPIC_API_KEY="$(python -c "
import sys
for ln in open(sys.argv[1], encoding='utf-8'):
    if ln.startswith('ANTHROPIC_API_KEY='):
        sys.stdout.write(ln.split('=', 1)[1].strip().strip(chr(34)).strip(chr(39))); break" "$ENVF")"
[ -n "$ANTHROPIC_API_KEY" ] || { echo "no key"; exit 2; }
export ANTHROPIC_API_KEY
mkdir -p "$S"; T0=$(date +%s)
MSYS_NO_PATHCONV=1 docker run --rm --name fc12-claude --hostname pc --user maker --memory 6g --shm-size 1g \
  -e CAP=$CAP -e ANTHROPIC_API_KEY -v "$LAB:/lab" -w /lab fcc-app:1.1.4-0.1.28 bash /lab/lab/fc12_R.sh "$RUN" \
  > "$S.container.log" 2>&1 || echo "container exit $?"
mv "$S.container.log" "$S/container.log" 2>/dev/null || true
COST=$(python -c "
import re,os,sys; p=sys.argv[1]+'/pane-cost.txt'; t=open(p,encoding='utf-8',errors='replace').read() if os.path.exists(p) else ''
m=re.findall(r'[\$]([0-9]+[.][0-9]+)',t); print(m[0] if m else '')" "$S")
echo "{\"run\": \"$RUN\", \"wall_s\": $(( $(date +%s) - T0 )), \"cost_usd\": \"$COST\", \"launch\": \"claude --model claude-sonnet-5-5 --strict-mcp-config --mcp-config entry.json (freecad only) --max-budget-usd $CAP --max-turns 40\"}" > "$S/meta.json"
python claude-run/budget.py record "$LEDGER" "fc12-$RUN" "$COST" "$CAP" fc12-lesson12
python claude-run/scrub.py "$S"
echo "cost $COST" | tee "$S/cost.txt"
