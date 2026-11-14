#!/usr/bin/env bash
# fc8 Claude runs (LAB-fc8; PLAN 4.B2.3/4.B2.4): bash claude-run/fc8run.sh A1|B1. Cap $0.30 per run, $0.60 the stage.
# lab/fc8_R.sh in fcc-app:1.1.4-0.1.28 with the network; the sign-in file mounted read-only, copied in, deleted on exit.
set -euo pipefail
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
RUN=$1; S=out/fc8/runs/$RUN
LEDGER="$LAB/../freecad-course-BUDGET.tsv"; CAP=${CAP:-0.30}; TOTAL=0.60
export BUDGET_MARK="# --- GO 14 Nov 2026 fc8"
[ -e "$S/events.jsonl" ] && { echo "refusing to overwrite $S"; exit 3; }
grep -qF "$BUDGET_MARK" "$LEDGER" || echo "$BUDGET_MARK (lab stage: runs A1 + B1, cap $CAP each, $TOTAL total, on the PC)" >> "$LEDGER"
python claude-run/budget.py check "$LEDGER" "$CAP" "$TOTAL" || { echo "BUDGET STOP"; exit 2; }
creds="$(cd ~ && (pwd -W 2>/dev/null || pwd))/.claude/.credentials.json"
mkdir -p "$S"; T0=$(date +%s)
MSYS_NO_PATHCONV=1 docker run --rm --name fc8-claude --hostname pc --user maker --memory 6g --shm-size 1g \
  -e CAP=$CAP -v "$creds:/creds.json:ro" -v "$LAB:/lab" -w /lab fcc-app:1.1.4-0.1.28 bash /lab/lab/fc8_R.sh "$RUN" \
  > "$S.container.log" 2>&1 || echo "container exit $?"
mv "$S.container.log" "$S/container.log" 2>/dev/null || true
COST=$(python -c "
import re,os,sys; p=sys.argv[1]+'/pane-cost.txt'; t=open(p,encoding='utf-8',errors='replace').read() if os.path.exists(p) else ''
m=re.findall(r'[\$]([0-9]+[.][0-9]+)',t); print(m[0] if m else '')" "$S")
echo "{\"run\": \"$RUN\", \"wall_s\": $(( $(date +%s) - T0 )), \"cost_usd\": \"$COST\", \"launch\": \"claude --model claude-sonnet-5-5 --strict-mcp-config --mcp-config entry.json (freecad only) --max-budget-usd $CAP --max-turns 30\"}" > "$S/meta.json"
python claude-run/budget.py record "$LEDGER" "fc8-$RUN" "$COST" "$CAP" fc8-lesson8
python claude-run/scrub.py "$S"
echo "cost $COST" | tee "$S/cost.txt"
