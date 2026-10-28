"""Logs are committed and the lab may be published: no host path, user name or project folder name may remain.
Private words (folder and account names) come from the LAB_PRIVATE_WORDS environment variable, never from this file,
so the public repo does not spell out the host's folder layout."""
import os

import pytest
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, '..'))
FOLDER_WORDS = ['Alpha-Folder', 'ProjectZulu', 'lab-parent']   # stand-ins: the real ones come from LAB_PRIVATE_WORDS


def test_scrub_removes_dashed_project_folder_names(tmp_path):
    d = tmp_path / 's'
    d.mkdir()
    home = '/home/someuserx'
    user = 'someuserx'
    dashed = 'C--Users-' + user + '-Alpha-Folder-ProjectZulu-lab-parent'
    (d / 'session.jsonl').write_text('{"p": "' + home.replace(chr(92), '/') + '/.claude/projects/' + dashed + '/x.txt", '
                                     '"q": "C:/Users/' + user + '/Alpha-Folder/ProjectZulu/lab-parent/x"}\n',
                                     encoding='utf-8')
    env = dict(os.environ, SCRUB_HOME=home, LAB_PRIVATE_WORDS=','.join(FOLDER_WORDS))
    subprocess.run([sys.executable, os.path.join(LAB, 'claude-run', 'scrub.py'), str(d)], check=True, capture_output=True, env=env)
    t = (d / 'session.jsonl').read_text(encoding='utf-8')
    for w in FOLDER_WORDS + [user]:
        assert w.lower() not in t.lower(), (w, t)


def test_no_committed_text_file_leaks_host_words():
    words = [w for w in os.environ.get('LAB_PRIVATE_WORDS', '').split(',') if w]
    if not words:
        pytest.skip('set LAB_PRIVATE_WORDS (folder and account names) to run this check')
    pat = re.compile('|'.join(re.escape(w) for w in words), re.IGNORECASE)
    bad = []
    for root, dirs, files in os.walk(os.path.join(LAB, 'out')):
        for f in files:
            if f.endswith(('.json', '.jsonl', '.txt', '.log', '.md', '.tsv')):
                fp = os.path.join(root, f)
                if pat.search(open(fp, encoding='utf-8', errors='replace').read()):
                    bad.append(os.path.relpath(fp, LAB))
    assert bad == []
