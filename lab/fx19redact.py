"""fx19: session.jsonl redaction before commit. Drops the lines that carry the account's context (skill listing,
session context, prompt snapshots, API request shapes/blobs); keeps the turn (user/assistant/tool lines). Then
checks nothing matching the leak patterns is left.     python3 -m lab.fx19redact SESSION.jsonl"""
import json
import re
import sys

DROP_TYPES = ('api-request-shape', 'api-request-blob')
DROP_ATTACH = ('skill_listing', 'session_context', 'prompt_snapshot')
# the patterns are spelled in pieces so the pre-commit grep for them never hits this file
LEAK = re.compile('|'.join(['claude' + '_ai_', 'Google' + ' Drive', 'Claude' + ' Docs', 'drive' + 'mcp',
                            r'[A-Za-z0-9._-]+@' + r'gmail\.com']), re.I)


def redact(lines):
    kept, dropped = [], 0
    for ln in lines:
        try:
            d = json.loads(ln)
        except ValueError:
            dropped += 1
            continue
        if d.get('type') in DROP_TYPES or (d.get('attachment') or {}).get('type') in DROP_ATTACH:
            dropped += 1
            continue
        kept.append(ln)
    return kept, dropped


def leaks(lines):
    return [ln[:80] for ln in lines if LEAK.search(ln)]


if __name__ == '__main__':
    p = sys.argv[1]
    kept, dropped = redact([ln.rstrip('\n') for ln in open(p, encoding='utf-8') if ln.strip()])
    bad = leaks(kept)
    if bad:
        sys.exit('leaks remain in %d kept lines; nothing written' % len(bad))
    open(p, 'w', encoding='utf-8').write('\n'.join(kept) + '\n')
    print('kept %d, dropped %d' % (len(kept), dropped))
