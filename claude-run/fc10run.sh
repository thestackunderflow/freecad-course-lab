#!/usr/bin/env bash
# fc10 Claude runs (PLAN 4.2/4.3): bash claude-run/fc10run.sh A1|B1. Cap $0.45 per run, $0.90 the stage (hard cap).
# lab/fc10_R.sh in fcc-app:1.1.4-0.1.28 with the network; the sign-in file mounted read-only, copied in, deleted on exit.
set -euo pipefail
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
RUN=$1; S=out/fc10/runs/$RUN
LEDGER="$LAB/../freecad-course-BUDGET.tsv"; CAP=${CAP:-0.45}; TOTAL=0.90
export BUDGET_MARK="# --- GO 16 Nov 2026 fc10"
[ -e "$S/events.jsonl" ] && { echo "refusing to overwrite $S"; exit 3; }
grep -qF "$BUDGET_MARK" "$LEDGER" || echo "$BUDGET_MARK (lab stage: runs A1 + B1, cap $CAP each, $TOTAL total, on the PC)" >> "$LEDGER"
python claude-run/budget.py check "$LEDGER" "$CAP" "$TOTAL" || { echo "BUDGET STOP"; exit 2; }
creds="$(cd ~ && (pwd -W 2>/dev/null || pwd))/.claude/.credentials.json"
mkdir -p "$S"; T0=$(date +%s)
MSYS_NO_PATHCONV=1 docker run --rm --name fc10-claude --hostname pc --user maker --memory 6g --shm-size 1g \
  -e CAP=$CAP -v "$creds:/creds.json:ro" -v "$LAB:/lab" -w /lab fcc-app:1.1.4-0.1.28 bash /lab/lab/fc10_R.sh "$RUN" \
  > "$S.container.log" 2>&1 || echo "container exit $?"
mv "$S.container.log" "$S/container.log" 2>/dev/null || true
COST=$(python -c "
import re,os,sys; p=sys.argv[1]+'/pane-cost.txt'; t=open(p,encoding='utf-8',errors='replace').read() if os.path.exists(p) else ''
m=re.findall(r'[\$]([0-9]+[.][0-9]+)',t); print(m[0] if m else '')" "$S")
echo "{\"run\": \"$RUN\", \"wall_s\": $(( $(date +%s) - T0 )), \"cost_usd\": \"$COST\", \"launch\": \"claude --model claude-sonnet-5-5 --strict-mcp-config --mcp-config entry.json (freecad only) --max-budget-usd $CAP --max-turns 40\"}" > "$S/meta.json"
python claude-run/budget.py record "$LEDGER" "fc10-$RUN" "$COST" "$CAP" fc10-lesson10
python claude-run/scrub.py "$S"
echo "cost $COST" | tee "$S/cost.txt"
