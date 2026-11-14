#!/usr/bin/env bash
# fx20 R1 (pre-registered in out/fx20/LAB-fx20.md section 4, one run, no retry): lab/fx20_R1.sh in fcc-app:1.1.4-0.1.28
# with the network (Claude's servers, PyPI for uvx). The sign-in file is mounted read-only, copied in, deleted on exit.
#   bash claude-run/fx20run.sh
set -euo pipefail
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
S=out/fx20/runs/R1
LEDGER="$LAB/../freecad-course-BUDGET.tsv"; CAP=0.25
export BUDGET_MARK="# --- GO 14 Nov 2026 fx20"
[ -e "$S/events.jsonl" ] && { echo "refusing to overwrite $S"; exit 3; }
grep -qF "$BUDGET_MARK" "$LEDGER" || echo "$BUDGET_MARK (lab stage: one pre-registered R1 run, cap $CAP, on the PC)" >> "$LEDGER"
python claude-run/budget.py check "$LEDGER" "$CAP" || { echo "BUDGET STOP"; exit 2; }
creds="$(cd ~ && (pwd -W 2>/dev/null || pwd))/.claude/.credentials.json"
mkdir -p "$S"; T0=$(date +%s)
MSYS_NO_PATHCONV=1 docker run --rm --name fx20-claude --hostname pc --user maker --memory 6g --shm-size 1g \
  -v "$creds:/creds.json:ro" -v "$LAB:/lab" -w /lab fcc-app:1.1.4-0.1.28 bash /lab/lab/fx20_R1.sh > "$S.container.log" 2>&1 \
  || echo "container exit $?"
mv "$S.container.log" "$S/container.log" 2>/dev/null || true
COST=$(python -c "
import re,os,sys; p=sys.argv[1]+'/pane-cost.txt'; t=open(p,encoding='utf-8',errors='replace').read() if os.path.exists(p) else ''
m=re.findall(r'[\$]([0-9]+[.][0-9]+)',t); print(m[0] if m else '')" "$S")
echo "{\"run\": \"R1\", \"wall_s\": $(( $(date +%s) - T0 )), \"cost_usd\": \"$COST\", \"launch\": \"claude --model claude-sonnet-5-5 --strict-mcp-config --mcp-config entry.json (freecad only)\"}" > "$S/meta.json"
python claude-run/budget.py record "$LEDGER" "fx20-R1" "$COST" "$CAP" fixit-fx20
python claude-run/scrub.py "$S"
echo "cost $COST" | tee "$S/cost.txt"
