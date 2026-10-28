"""Replace host paths and the host user name in a session's text logs (they are committed; the lab may be published).
    python claude-run/scrub.py SESSION_DIR
The lab folder becomes $LAB; any other path under the user's home becomes ~ ; the user name itself becomes 'you';
Claude Code's dashed folder names become C--Users-you-project, and every word in LAB_PRIVATE_WORDS (comma-separated:
folder and account names, kept out of this public file) becomes 'project'. SCRUB_HOME overrides the home (tests)."""
import os
import re
import sys

BS = chr(92)   # a backslash, spelled out so no shell or editor can eat it

d = sys.argv[1]
lab = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
home = os.environ.get('SCRUB_HOME') or os.path.expanduser('~')
user = os.path.basename(home)
private = sorted((w for w in os.environ.get('LAB_PRIVATE_WORDS', '').split(',') if w), key=len, reverse=True)
forms = []
for p, rep in ((lab, '$LAB'), (home, '~')):
    for q in {p, p.replace(BS, '/'), p.replace('/', BS)}:
        forms += [(q.replace(BS, BS + BS), rep), (q, rep)]
forms.sort(key=lambda x: -len(x[0]))
n = 0
for root, _, files in os.walk(d):
    for f in files:
        if not f.endswith(('.json', '.jsonl', '.txt', '.log')):
            continue
        fp = os.path.join(root, f)
        s = open(fp, encoding='utf-8', errors='surrogateescape').read()
        t = s
        for a, b in forms:
            t = re.sub(re.escape(a), lambda _m: b, t, flags=re.IGNORECASE)
        t = re.sub(r'(?i)\b' + re.escape(user) + r'\b', 'you', t)
        # Claude Code's own folder names spell the project path with dashes (C--Users-NAME-...),
        # and a path may be split in other ways: drop the private words wherever they appear.
        t = re.sub(r'[A-Za-z]--Users-[A-Za-z0-9_.-]*', 'C--Users-you-project', t)
        for w in private:
            t = re.sub(r'(?i)' + re.escape(w), 'project', t)
        if t != s:
            open(fp, 'w', encoding='utf-8', errors='surrogateescape', newline='').write(t)
            n += 1
print(f'scrubbed {n} files in {d}')
