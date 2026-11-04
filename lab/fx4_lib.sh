# fx4 helpers on top of common.sh: a filmed terminal (46 columns) where each command is typed, its output is read back
# from the terminal itself (tmux, lines joined) into a file, and the event names are exactly the SCRIPT-fx4 section 1 names.
#   . /lab/lab/common.sh; . /lab/lab/fx4_lib.sh
X=/lab/out/fx4

home_init() {   # not filmed: a short prompt, the test script where a person would find it, onboarding already passed
  mkdir -p ~/tools ~/work
  ln -sf /lab/tools/test_mcp.py ~/tools/test_mcp.py
  cat >> ~/.bashrc <<'EOF'
export PATH="$HOME/.local/bin:$PATH"
PS1='$ '
EOF
  claude_home /home/maker
}

last_line() { tmux capture-pane -p -t cc | sed -e 's/[[:space:]]*$//' | grep -v '^$' | tail -n 1; }

wait_prompt() {   # wait_prompt [TIMEOUT]: until the shell prompt is the last thing on the screen
  local end=$(( $(date +%s) + ${1:-60} )); sleep 0.8
  until [ "$(last_line)" = '$' ]; do [ "$(date +%s)" -ge "$end" ] && return 1; sleep 0.25; done
}

fresh() { term_focus cc; tmux send-keys -t cc C-l; sleep 0.4; tmux clear-history -t cc; sleep 0.2; }

save_out() {      # save_out FILE: the output of the last command only (first line = prompt + command, last = prompt)
  tmux capture-pane -J -p -S - -t cc | sed -e 's/[[:space:]]*$//' > "$1.screen"
  python3 - "$1.screen" "$1" <<'PY'
import sys
L = open(sys.argv[1], encoding='utf-8').read().split('\n')
L = L[1:]
while L and (L[-1].strip() in ('', '$')):
    L.pop()
open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(L) + '\n')
PY
}

# type CMD at a person's pace; the typed event is stamped at the Enter key. Sets ENTER_T (epoch) for timed marks.
typ() {           # typ "command" "event name"
  fresh; sl_nap 0.6
  sl_type "$1" "" 70
  ENTER_T=$(date +%s.%N)
  sl_key Return "$2"
}

run_wait() {      # run_wait "command" TYPED_EVENT DONE_EVENT OUTFILE [TIMEOUT]: type, wait for the prompt, mark, save
  typ "$1" "$2"
  wait_prompt "${5:-90}" && sl_mark "$3" || sl_mark "TIMEOUT: $3"
  save_out "$4"
}

run_timed() {     # run_timed "command" TYPED_EVENT WAITS_EVENT OUTFILE SECONDS_AFTER_ENTER_FOR_WAITS: a command run under timeout
  typ "$1" "$2"
  local now e=$(( $(date +%s) + 200 )); now=$(date +%s.%N)
  while [ "$(awk -v e="$ENTER_T" -v n="$(date +%s.%N)" -v s="$5" 'BEGIN{print (n-e < s) ? 1 : 0}')" = 1 ]; do
    [ "$(last_line)" = '$' ] && break; sleep 0.2
  done
  [ "$(last_line)" = '$' ] || sl_mark "$3"
  wait_prompt 60 || sl_mark "TIMEOUT: $3"
  save_out "$4"
}

tsv() {           # tsv TAKE_DIR [OUT_NAME]: events.jsonl (t = seconds from the first frame) to events.tsv
  python3 - "$1" "${2:-events.tsv}" <<'PY'
import json, os, sys
d, name = sys.argv[1], sys.argv[2]
rows = [json.loads(l) for l in open(os.path.join(d, 'events.jsonl')) if l.strip()]
with open(os.path.join(d, name), 'w') as f:
    for r in rows:
        f.write('%s\t%.2f\n' % (r.get('event') or r.get('label'), r['t']))
PY
}

term_start() {    # the filmed terminal, left; a login shell so uv's installer line in the profile applies
  term_open cc 0 0 46 36 30 bash -l
  xdotool mousemove 2000 900
}

stamp() { sl_stop; tsv "$1" "${2:-events.tsv}"; }
