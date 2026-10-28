"""The proof with no AI: replay the tools/call requests Claude sent (from the logging proxy's transcript.jsonl), in order,
over the same plug (`uvx freecad-mcp@0.1.28`) to a fresh FreeCAD, and keep every reply. Also: the call/reply pairs a
video's tool-call panels are read from.

    python3 -m client.replay TRANSCRIPT OUT.json -- COMMAND...
"""
import json
import sys
from datetime import datetime


def _rows(path):
    for line in open(path, encoding='utf-8'):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if isinstance(r, dict) and isinstance(r.get('msg'), dict):
            yield r


def logged_calls(path):
    calls = []
    for r in _rows(path):
        m = r['msg']
        if r.get('dir') == 'client->server' and m.get('method') == 'tools/call':
            p = m.get('params') or {}
            calls.append({'seq': r.get('seq'), 'name': p.get('name'), 'arguments': p.get('arguments') or {}})
    return calls


def call_pairs(path):
    """Each tools/call with its reply: name, arguments, isError, the reply's text, saved image names, seconds taken."""
    open_calls, out = {}, []
    for r in _rows(path):
        m = r['msg']
        if r.get('dir') == 'client->server' and m.get('method') == 'tools/call':
            p = m.get('params') or {}
            open_calls[json.dumps(m.get('id'))] = (r, p.get('name'), p.get('arguments') or {})
        elif r.get('dir') == 'server->client' and json.dumps(m.get('id')) in open_calls:
            c, name, args = open_calls.pop(json.dumps(m.get('id')))
            res = m.get('result') or {}
            content = res.get('content') or []
            texts = [x.get('text', '') for x in content if x.get('type') == 'text']
            imgs = [(x.get('data') or {}).get('saved_as') for x in content
                    if x.get('type') == 'image' and isinstance(x.get('data'), dict)]
            secs = round(datetime.fromisoformat(r['t']).timestamp() - datetime.fromisoformat(c['t']).timestamp(), 3)
            out.append({'call_seq': c.get('seq'), 'reply_seq': r.get('seq'), 'name': name, 'arguments': args,
                        'isError': bool(res.get('isError')) or 'error' in m, 'text': '\n'.join(texts),
                        'images': [i for i in imgs if i], 'seconds': secs})
    return out


def main(argv):
    from client.mcp import McpClient
    transcript, out = argv[0], argv[1]
    cmd = argv[argv.index('--') + 1:]
    calls = logged_calls(transcript)
    c = McpClient(cmd, timeout_s=180, log_path=out.replace('.json', '-transcript.jsonl'))
    c.start()
    rows = []
    for call in calls:
        r = c.call_tool(call['name'], call['arguments'])
        rows.append({'logged_seq': call['seq'], 'name': call['name'], 'isError': bool(r.get('isError')),
                     'text': McpClient.text(r)})
    c.close()
    res = {'calls': len(calls), 'names': [x['name'] for x in rows], 'errors': sum(x['isError'] for x in rows), 'rows': rows}
    json.dump(res, open(out, 'w', encoding='utf-8'), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != 'rows'}, indent=1))
    return res


if __name__ == '__main__':
    main(sys.argv[1:])
