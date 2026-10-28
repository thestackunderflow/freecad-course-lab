"""Contact sheet: one captioned frame per event (just after it), or every N seconds, tiled into one PNG.

    python3 -m screenlab.sheet VIDEO.mp4 OUT.png [--events events.jsonl] [--every S] [--width 480] [--cols C]"""
import argparse
import glob
import json
import math
import os
import subprocess
import tempfile

FONTS = ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')


def pick(events, after=0.5, min_gap=1.0):
    """(time, caption) for each event, skipping events closer than min_gap to the previous pick."""
    out, last = [], None
    for e in sorted(events, key=lambda e: e['t']):
        if last is None or e['t'] - last >= min_gap:
            out.append((round(e['t'] + after, 3), e['event']))
            last = e['t']
    return out


def grid(n, cols=None):
    c = cols or max(1, math.ceil(math.sqrt(n)))
    return c, max(1, math.ceil(n / c))


def _font():
    for f in FONTS + tuple(sorted(glob.glob('/usr/share/fonts/**/*.ttf', recursive=True))):
        if os.path.exists(f):
            return f
    return None


def duration(mp4):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp4],
                                check=True, capture_output=True, text=True).stdout.strip())


def make(mp4, out, events=None, every=None, width=480, cols=None, after=0.5):
    if events:
        rows = [json.loads(line) for line in open(events, encoding='utf-8') if line.strip()]
        picks = pick(rows, after=after)
    else:
        step = every or 5.0
        picks = [(round(i * step, 3), '') for i in range(int(duration(mp4) // step) + 1)]
    end = duration(mp4) - 0.05
    tmp = tempfile.mkdtemp(prefix='sheet-')
    font = _font()
    cap_h = max(24, width // 14)
    for i, (t, text) in enumerate(picks):
        tf = os.path.join(tmp, f'c{i:03d}.txt')
        with open(tf, 'w', encoding='utf-8') as f:
            f.write(f'{min(t, end):.1f} s  {text}'.strip()[:70])
        vf = f'scale={width}:-2,pad=iw:ih+{cap_h}:0:0:color=black'
        if font:
            vf += (f",drawtext=fontfile='{font}':textfile='{tf}':fontsize={int(cap_h * 0.55)}:fontcolor=white:"
                   f"x=8:y=h-{cap_h}+({cap_h}-text_h)/2")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{min(t, end):.3f}', '-i', mp4, '-frames:v', '1',
                        '-vf', vf, os.path.join(tmp, f'f{i:03d}.png')], check=True)
    c, r = grid(len(picks), cols)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '1', '-i', os.path.join(tmp, 'f%03d.png'),
                    '-vf', f'tile={c}x{r}:padding=4:color=white', '-frames:v', '1', '-update', '1', out], check=True)
    return len(picks)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('mp4')
    ap.add_argument('out')
    ap.add_argument('--events')
    ap.add_argument('--every', type=float)
    ap.add_argument('--width', type=int, default=480)
    ap.add_argument('--cols', type=int)
    a = ap.parse_args(argv)
    print(json.dumps({'out': a.out, 'frames': make(a.mp4, a.out, a.events, a.every, a.width, a.cols)}))


if __name__ == '__main__':
    main()
