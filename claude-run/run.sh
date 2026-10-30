#!/usr/bin/env bash
# One paid Claude Code take: the budget check, then the take script in the lab image with network on (Claude's servers,
# PyPI for uvx). The container gets this PC's Claude sign-in as one environment variable, read here from the Claude
# Code credentials file into a temporary env file that is deleted when the run ends; nothing about it reaches the run
# folder. Afterwards: the cost from Claude Code's own /cost line goes into the ledger, and the run folder is scrubbed.
#   bash claude-run/run.sh RUN_NAME CAP_USD lab/take_X.sh      (the take writes out/$LESSON/runs/RUN_NAME/)
#   LESSON=l2 (default l1) also picks the ledger prefix (fc2-) and, with BUDGET_MARK, the lesson's own GO line.
set -euo pipefail
RUN=$1; CAP=$2; TAKE=$3
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
LESSON=${LESSON:-l1}; N=${LESSON#l}
S=out/$LESSON/runs/$RUN
LEDGER="${LEDGER:-$LAB/../freecad-course-BUDGET.tsv}"
[ -e "$S/meta.json" ] && { echo "refusing to overwrite $S"; exit 3; }
python claude-run/budget.py check "$LEDGER" "$CAP" || { echo "BUDGET STOP"; exit 2; }
mkdir -p out/scratch "$S"; ENVF=out/scratch/run-$$.env
trap 'rm -f "$ENVF"' EXIT
python - "$ENVF" <<'PY'
import json, os, sys
d = json.load(open(os.path.expanduser('~/.claude/.credentials.json')))
open(sys.argv[1], 'w').write('CLAUDE_CODE_OAUTH_TOKEN=' + d['claudeAiOauth']['accessToken'] + '\n')
PY
T0=$(date +%s)
MSYS_NO_PATHCONV=1 docker run --rm --name "${FCC_PREFIX:-fcc}-claude-$RUN" --hostname pc --shm-size 1g --memory 6g --user maker \
  --env-file "$ENVF" -e LESSON="$LESSON" -v "$LAB:/lab" -w /lab fcc-app:1.1.4-0.1.28 bash "/lab/$TAKE" "$RUN" > "$S/container.log" 2>&1 \
  || echo "container exit $?"
rm -f "$ENVF"
COST=$(python - "$S" <<'PY'
import os, re, sys
p = os.path.join(sys.argv[1], 'pane-cost.txt')
t = open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else ''
m = re.findall(r'\$(\d+\.\d+)', t)
print(m[0] if m else '')
PY
)
echo "{\"run\": \"$RUN\", \"take\": \"$TAKE\", \"wall_s\": $(( $(date +%s) - T0 )), \"cost_usd\": \"$COST\", \"launch\": \"claude (no flags: Claude Code's own default mode and model)\"}" > "$S/meta.json"
python claude-run/budget.py record "$LEDGER" "fc$N-$RUN" "$COST" "$CAP" "fc$N-lesson$N"
python claude-run/scrub.py "$S"
cat "$S/meta.json"
