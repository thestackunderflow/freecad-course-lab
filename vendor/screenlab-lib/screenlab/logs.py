"""Events while recording are written with the wall clock ("ts"); when the recording stops, finalize() rebases them
and the cursor log onto T0 (the first frame) and writes what footage tools read: cursor.jsonl, events.jsonl, record.json.

    python3 -m screenlab.logs finalize DIR T0 SOURCE W H FPS"""
import json
import os
import sys
import time

from . import timing


class EventLog:
    def __init__(self, path, clock=time.time):
        self.path, self.clock = path, clock

    def mark(self, label, **extra):
        row = {'ts': self.clock(), 'event': label}
        row.update(extra)
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(row) + '\n')
        return row['ts']


def _read(path):
    if not os.path.exists(path):
        return []
    rows = []
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except ValueError:
                pass                      # a line cut off by a killed writer
    return rows


def _write(path, rows):
    with open(path, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')


def finalize(d, t0, t0_source, size, fps):
    cur_raw, ev_raw = os.path.join(d, 'cursor.raw.jsonl'), os.path.join(d, 'events.raw.jsonl')
    _write(os.path.join(d, 'cursor.jsonl'), timing.rebase_cursor(_read(cur_raw), t0))
    _write(os.path.join(d, 'events.jsonl'), timing.rebase_events(_read(ev_raw), t0))
    meta = {'video': 'screen.mp4', 'size': [int(size[0]), int(size[1])], 'fps': int(fps), 't0_epoch': t0,
            't0_source': t0_source, 'time_base': 'seconds from the first frame of screen.mp4'}
    with open(os.path.join(d, 'record.json'), 'w') as f:
        json.dump(meta, f, indent=1)
    for p in (cur_raw, ev_raw):
        if os.path.exists(p):
            os.remove(p)
    return meta


if __name__ == '__main__':
    if len(sys.argv) == 8 and sys.argv[1] == 'finalize':
        _, _, d, t0, src, w, h, fps = sys.argv
        finalize(d, float(t0), src, (int(w), int(h)), int(fps))
    else:
        sys.exit(__doc__)
