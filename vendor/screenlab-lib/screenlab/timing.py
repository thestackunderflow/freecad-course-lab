"""T0 = the wall-clock time of the recording's first frame, and the logs rebased onto it.

x11grab stamps every packet with the wall clock (microseconds). With `-debug_ts` ffmpeg prints, for the first packet,
a line `... demuxer -> ist_index:0:0 type:video pkt_pts:<us> ...` before the timestamps are shifted to start at 0.

    python3 -m screenlab.timing t0 OUTFILE      (reads ffmpeg's stderr on stdin, writes the first stamp, drains the rest)"""
import re
import sys

T0_LINE = re.compile(r'demuxer -> ist_index:\d+:\d+ type:video pkt_pts:(\d+)')


def parse_t0(line):
    m = T0_LINE.search(line or '')
    return int(m.group(1)) / 1e6 if m else None


def read_t0(lines, out_path=None):
    """Consume all lines (ffmpeg blocks if its stderr is not drained); return and write the first stamp."""
    t0 = None
    for line in lines:
        if t0 is None:
            t0 = parse_t0(line)
            if t0 is not None and out_path:
                with open(out_path, 'w') as f:
                    f.write(f'{t0:.6f}\n')
    return t0


def rebase_cursor(rows, t0):
    """{"ts", "x", "y"} -> {"t", "x", "y"}; positions before the first frame collapse into one row at t = 0."""
    rows = sorted(rows, key=lambda r: r['ts'])
    before = [r for r in rows if r['ts'] < t0]
    out = []
    if before:
        out.append({'t': 0.0, 'x': before[-1]['x'], 'y': before[-1]['y']})
    for r in rows:
        if r['ts'] >= t0:
            out.append({'t': round(r['ts'] - t0, 3), 'x': r['x'], 'y': r['y']})
    return out


def rebase_events(rows, t0):
    out = []
    for r in sorted(rows, key=lambda r: r['ts']):
        e = {'t': round(r['ts'] - t0, 3)}
        e.update({k: v for k, v in r.items() if k != 'ts'})
        out.append(e)
    return out


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == 't0':
        read_t0(sys.stdin, sys.argv[2])
    else:
        sys.exit(__doc__)
