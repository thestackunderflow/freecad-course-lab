"""The cursor log a zoom follows: polls the pointer and writes one raw row {"ts": wall clock, "x", "y"} per change.
The recorder runs it in a thread; finalize() rebases the rows onto the first frame.

    python3 -m screenlab.cursorlog OUT.raw.jsonl [HZ]        (stops when OUT.raw.jsonl.stop exists)"""
import json
import os
import re
import subprocess
import sys
import time

LOC = re.compile(r'x:(-?\d+)\s+y:(-?\d+)')


def parse(line):
    m = LOC.search(line or '')
    return (int(m.group(1)), int(m.group(2))) if m else None


def xdotool_sample():
    r = subprocess.run(['xdotool', 'getmouselocation'], capture_output=True, text=True)
    return parse(r.stdout)


def poll(out, sample=xdotool_sample, stop=None, clock=time.time, hz=30.0, sleep=time.sleep):
    stop = stop or (lambda: os.path.exists(out + '.stop'))
    last = None
    with open(out, 'a', encoding='utf-8') as f:
        while not stop():
            t = clock()
            xy = sample()
            if xy and xy != last:
                f.write(json.dumps({'ts': round(t, 6), 'x': xy[0], 'y': xy[1]}) + '\n')
                f.flush()
                last = xy
            sleep(max(0.0, 1.0 / hz - (time.time() - t)))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    poll(sys.argv[1], hz=float(sys.argv[2]) if len(sys.argv) > 2 else 30.0)
