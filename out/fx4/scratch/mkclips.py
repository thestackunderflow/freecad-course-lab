import json, os, subprocess, sys
FP = '/ev/Refream-Canvas/mcp-canvas/tools/video-qa/footage.py'
def ev(tsv, name):
    for l in open(tsv, encoding='utf-8'):
        n, t = l.rstrip('\n').rsplit('\t', 1)
        if n == name: return float(t)
    raise KeyError(name)
TOP = [0, 0, 1156, 650]; MID = [0, 640, 1156, 650]; LOW = [0, 780, 1156, 650]
# name, video, tsv, start event, end event, hold after end, box
C = [
 ('A-0.1.19-traceback', 'A/screen.mp4', 'A/events.tsv', '0.1.19: typed', '0.1.19: traceback last line', 15, LOW),
 ('A-0.1.20-waits', 'A/screen.mp4', 'A/events.tsv', '0.1.20: typed', '0.1.20: waits', 4, TOP),
 ('B-metadata-2x', 'B/screen.mp4', 'B/events.tsv', 'metadata 0.1.19: typed', 'metadata: 2.x printed', 6, TOP),
 ('B-metadata-pinned', 'B/screen.mp4', 'B/events.tsv', 'metadata pinned: typed', 'metadata pinned: 1.x printed', 6, TOP),
 ('B-metadata-0.1.28', 'B/screen.mp4', 'B/events.tsv', 'metadata 0.1.28: typed', 'metadata 0.1.28: printed', 6, TOP),
 ('C-pinned-waits', 'C/screen.mp4', 'C/events.tsv', 'pinned 0.1.19: typed', 'pinned 0.1.19: waits', 4, TOP),
 ('C-add-connected', 'C/screen.mp4', 'C/events.tsv', 'add 0.1.28: typed', 'list: Connected', 8, TOP),
 ('C-get-freecad', 'C/screen.mp4', 'C/events.tsv', 'your turn get: typed', 'get freecad: printed', 8, TOP),
 ('D-release', 'D/screen.mp4', 'D/events.tsv', 'firefox: release v2.0.0 opened', 'typed: pypi json', -3, [0, 150, 2000, 1125]),
 ('D-json-requires', 'D/screen.mp4', 'D/events.tsv', 'JSON filter box', 'json: requires_dist shown', 6, [0, 150, 2000, 1125]),
 ('D-json-upload', 'D/screen.mp4', 'D/events.tsv', 'json: requires_dist shown', 'json: upload_time shown', 6, [0, 150, 2000, 1125]),
 ('D-pypi-0.1.28', 'D/screen.mp4', 'D/events.tsv', 'firefox: pypi 0.1.28 Requires Python', 'recording stopped', -1, [1200, 300, 1600, 900]),
 ('E1-pip', 'E/E1rec/screen.mp4', 'E/events-E1.tsv', 'pip 3.11: typed', 'pip 3.11: error block', 17, TOP),
 ('E1-uvx-download', 'E/E1rec/screen.mp4', 'E/events-E1.tsv', 'uvx 0.1.28: typed', '0.1.28: waits', 6, TOP),
 ('E2-sys-version', 'E/E2rec/screen.mp4', 'E/events-E2.tsv', 'console: typed sys.version', 'console: sys.version', 8, [0, 900, 1760, 990]),
 ('E2-status-bar', 'E/E2rec/screen.mp4', 'E/events-E2.tsv', 'workbench list: MCP Addon chosen', 'status: rpc started', 5, [0, 0, 2880, 1620]),
 ('R1-reply', 'runs/R1/screen.mp4', 'runs/R1/events.tsv', 'turn 1: Enter', 'turn 1: reply done', 5, MID),
]
os.makedirs('clips', exist_ok=True)
for n, v, tsv, a, b, hold, box in C:
    t0 = max(0, ev(tsv, a) - 1.0); t1 = ev(tsv, b) + hold
    fj = f'clips/focus_{n}.json'; json.dump([{'t': 0, 'box': box}], open(fj, 'w'))
    r = subprocess.run([sys.executable, FP, 'clip', v, f'clips/{n}.mp4', '--src', '2880x1800', '--t0', f'{t0:.2f}', '--t1', f'{t1:.2f}',
                        '--zoom', '1.5', '--size', '1920x1080', '--focus', fj], capture_output=True, text=True)
    print(n, 'ok' if r.returncode == 0 else r.stderr[-300:])
