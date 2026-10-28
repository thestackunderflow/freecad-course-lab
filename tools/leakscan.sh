#!/bin/bash
# Leak scan before publishing: every file git would publish (text and binary), the commit metadata, and optionally
# the untracked out/ folder, checked against a patterns file kept OUTSIDE the kit (one fixed string per line,
# case-insensitive), so the private strings themselves are never committed.
#   tools/leakscan.sh PATTERNS.txt [--out]
# Exit 0 = clean, 1 = a hit (printed as file: matches), 2 = the scan itself failed.
# Case folding is done with tr, not grep -i: Git for Windows' grep aborts on -i -F -f (exit 134), which would
# otherwise read as "no match". Any grep exit above 1 stops the scan.
set -u
P=${1:?patterns file}
cd "$(dirname "$0")/.."
LP=$(mktemp); tr 'A-Z' 'a-z' < "$P" | grep -v '^$' > "$LP"
hits=0
scan() {          # scan LABEL < data
  local m rc
  m=$(tr 'A-Z' 'a-z' | grep -a -o -F -f "$LP"); rc=$?
  [ $rc -gt 1 ] && { echo "SCAN FAILED on $1 (grep exit $rc)"; rm -f "$LP"; exit 2; }
  [ -n "$m" ] && { echo "HIT $1: $(echo "$m" | sort -u | tr '\n' ' ')"; hits=1; }
  return 0
}
n=0
while IFS= read -r -d '' f; do
  scan "$f" < "$f"; n=$((n + 1))
done < <(git ls-files -z --cached --others --exclude-standard; [ "${2:-}" = --out ] && find out -type f -print0 2>/dev/null)
git log --format='%an %ae %cn %ce %B' | scan "git log"
printf 'canary %s\n' "$(head -1 "$LP")" | (m=$(tr 'A-Z' 'a-z' | grep -a -c -F -f "$LP"); [ "$m" = 1 ]) \
  || { echo "SCAN FAILED: the canary line was not found"; rm -f "$LP"; exit 2; }
rm -f "$LP"
[ $hits = 0 ] && echo "leak scan: clean ($n files${2:+, out/ included}, git log; canary found)"
exit $hits
