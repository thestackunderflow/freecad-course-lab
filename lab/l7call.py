"""Lesson 7: our test script, with no AI. It starts FreeCAD's plug with the same line Claude Code uses
(`uvx freecad-mcp@0.1.28`), sends ONE tool call, the same JSON-RPC request a Claude app sends, and prints the plug's
reply word for word: wrapped at spaces to fit the filmed terminal, never shortened, and marked OK or ERROR the way the
reply itself marks it (MCP's isError). A picture in a reply is named, not printed. Every call is also logged.

    test-call TOOL                        e.g. test-call list_documents
    test-call TOOL '{"json": "args"}'     e.g. test-call get_objects '{"doc_name": "Hook"}'
    test-call execute_code FILE.py        the file's text is the code (show it first with cat)
(test-call is a two-line wrapper: exec python3 -m lab.l7call "$@"; env L7_LOG = the transcript, default ~/test-call.jsonl)"""
import json
import os
import sys
import textwrap
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

PLUG = ['uvx', 'freecad-mcp@0.1.28']
COLS = int(os.environ.get('L7_COLS', '44'))


def parse(argv):
    name = argv[0]
    if len(argv) < 2:
        return name, {}
    a = argv[1]
    if name.startswith('execute_code') and not a.lstrip().startswith('{'):
        return name, {'code': open(a, encoding='utf-8').read()}
    return name, json.loads(a)


def _wrap(text):
    out = []
    for para in str(text).split('\n'):
        out += textwrap.wrap(para, COLS - 2, break_long_words=False, break_on_hyphens=False) or ['']
    return ['  ' + x if x else '' for x in out]


def reason(stderr_lines):
    """The plug's own reason for a failed call: the last 'Exception: ...' line of its log (stderr), or None."""
    found = None
    for ln in stderr_lines:
        ln = ln.rstrip()
        if ln.startswith('Exception: '):
            found = ln[len('Exception: '):]
    return found


def render(name, args, result, log_reason=None):
    lines = ['call: ' + name, 'reply: ' + ('ERROR' if result.get('isError') else 'OK')]
    pics = 0
    for c in result.get('content', []):
        if c.get('type') == 'text':
            lines += _wrap(c['text'])
        elif c.get('type') == 'image':
            pics += 1
    while len(lines) > 2 and lines[-1] == '':
        lines.pop()
    if pics:
        lines.append('(+ a picture of the 3D view)')
    if log_reason and result.get('isError'):
        lines += ["plug's log:"] + _wrap(log_reason)
    return lines


def log_call(path, name, args, result):
    text = '\n'.join(c['text'] for c in result.get('content', []) if c.get('type') == 'text')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({'tool': name, 'arguments': args, 'isError': bool(result.get('isError')), 'text': text,
                            'images': sum(1 for c in result.get('content', []) if c.get('type') == 'image')}) + '\n')


def call(name, args, client, settle_s=0.0):
    """One tool call. The plug flushes its log (stderr) only when it exits, so the reason is read after close()."""
    try:
        client.start()
        r = client.call_tool(name, args)
    finally:
        client.close()
    why = None
    for _ in range(20):
        why = reason(client.stderr_text())
        if why or not r.get('isError'):
            break
        time.sleep(settle_s)
    return r, why


def main(argv):
    from client.mcp import McpClient
    name, args = parse(argv)
    log = os.environ.get('L7_LOG', os.path.expanduser('~/test-call.jsonl'))
    r, why = call(name, args, McpClient(PLUG, timeout_s=90, log_path=log + '.rpc'), settle_s=0.1)
    log_call(log, name, args, r)
    print('\n'.join(render(name, args, r, why)), flush=True)
    return 1 if r.get('isError') else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
