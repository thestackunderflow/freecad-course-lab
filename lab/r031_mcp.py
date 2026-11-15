"""Task R: start `uvx freecad-mcp@VER` as Claude Code would (stdio), initialize, list its tools and, when FreeCAD's
RPC server is on, run one line through it. Prints one JSON line.
    python3 -m lab.r031_mcp 0.1.31 LOG [call]"""
import json
import sys

from client.mcp import McpClient


def main(ver, log, call=False):
    r = {'version': ver, 'initialize_ok': False, 'tools': [], 'server_info': None, 'call': None}
    c = McpClient(['uvx', f'freecad-mcp@{ver}'], timeout_s=240, log_path=log)
    try:
        init = c.start()
        r['initialize_ok'] = bool(init)
        r['server_info'] = (init or {}).get('serverInfo')
        r['tools'] = sorted(t['name'] for t in c.list_tools())
        if call:
            res = c.call_tool('execute_code', {'code': "import FreeCAD, sys; print(FreeCAD.Version()[:3], sys.version.split()[0])"})
            r['call'] = McpClient.text(res)
    except Exception as e:  # recorded, not raised: the verdict says what failed
        r['error'] = f'{type(e).__name__}: {e}'
        r['stderr'] = c.stderr_text()[-800:]
    finally:
        c.kill()
    print(json.dumps(r))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], len(sys.argv) > 3)
