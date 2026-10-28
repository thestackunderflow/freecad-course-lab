"""Record the whole virtual display: ffmpeg x11grab, 30 fps constant frame rate, H.264 CRF 14 (near-lossless), with
the cursor log polled beside it and T0 read from ffmpeg's own first-packet stamp.

    python3 -m screenlab.recorder DIR W H [--display :99] [--nomouse]
        records until DIR/.stop exists, then finalizes (the shell library's sl_record / sl_stop use this)."""
import argparse
import os
import signal
import subprocess
import sys
import threading
import time
from functools import partial

from . import cursorlog, logs, timing


def ffmpeg_cmd(out, size, display=':99', fps=30, crf=14, draw_mouse=True):
    return ['ffmpeg', '-hide_banner', '-nostdin', '-debug_ts', '-y',
            '-f', 'x11grab', '-draw_mouse', '1' if draw_mouse else '0', '-framerate', str(fps),
            '-video_size', f'{size[0]}x{size[1]}', '-i', display,
            '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', str(crf), '-pix_fmt', 'yuv420p',
            '-fps_mode', 'cfr', '-r', str(fps), out]


def _sample(env):
    r = subprocess.run(['xdotool', 'getmouselocation'], capture_output=True, text=True, env=env)
    return cursorlog.parse(r.stdout)


class Recorder:
    def __init__(self, out_dir, size, display=':99', fps=30, crf=14, draw_mouse=True, hz=30.0):
        self.dir, self.size, self.display = out_dir, tuple(size), display
        self.fps, self.crf, self.draw_mouse, self.hz = fps, crf, draw_mouse, hz
        self.env = dict(os.environ, DISPLAY=display)
        self.t0 = None
        self.tail = []

    def _drain(self, stream):
        for line in stream:
            if self.t0 is None:
                self.t0 = timing.parse_t0(line)
            elif 'debug_ts' not in line and '->' not in line and 'ist_index' not in line:
                self.tail = (self.tail + [line.rstrip()])[-40:]

    def start(self, timeout=10.0):
        os.makedirs(self.dir, exist_ok=True)
        self.raw_cursor = os.path.join(self.dir, 'cursor.raw.jsonl')
        open(self.raw_cursor, 'a').close()
        self.launched = time.time()
        self.proc = subprocess.Popen(ffmpeg_cmd(os.path.join(self.dir, 'screen.mp4'), self.size, self.display,
                                                self.fps, self.crf, self.draw_mouse),
                                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                                     text=True, errors='replace', env=self.env)
        self.reader = threading.Thread(target=self._drain, args=(self.proc.stderr,), daemon=True)
        self.reader.start()
        self._stop = threading.Event()
        self.poller = threading.Thread(target=cursorlog.poll, daemon=True, kwargs=dict(
            out=self.raw_cursor, sample=partial(_sample, self.env), stop=self._stop.is_set, hz=self.hz))
        self.poller.start()
        end = time.time() + timeout
        while self.t0 is None and time.time() < end and self.proc.poll() is None:
            time.sleep(0.02)
        if self.proc.poll() is not None:
            raise RuntimeError('ffmpeg stopped at once: ' + ' | '.join(self.tail[-5:]))
        return self

    def stop(self):
        time.sleep(0.2)                      # the last frame of the last action lands
        self._stop.set()
        self.poller.join(5)
        self.proc.send_signal(signal.SIGINT)
        try:
            self.proc.wait(60)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()
        self.reader.join(5)
        t0, src = (self.t0, 'debug_ts') if self.t0 is not None else (self.launched, 'launch')
        self.meta = logs.finalize(self.dir, t0, src, self.size, self.fps)
        return self.meta


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('dir')
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('--display', default=os.environ.get('DISPLAY', ':99'))
    ap.add_argument('--nomouse', action='store_true')
    a = ap.parse_args(argv)
    rec = Recorder(a.dir, (a.w, a.h), a.display, draw_mouse=not a.nomouse).start()
    with open(os.path.join(a.dir, '.recording'), 'w') as f:
        f.write(f'{rec.t0}\n')
    stop = os.path.join(a.dir, '.stop')
    while not os.path.exists(stop):
        time.sleep(0.05)
    rec.stop()
    for p in (stop, os.path.join(a.dir, '.recording')):
        if os.path.exists(p):
            os.remove(p)


if __name__ == '__main__':
    sys.exit(main())
