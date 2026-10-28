"""The virtual screen: Xvfb at a given size (24-bit), and openbox as a light window manager (so windows can be
maximised, focused and raised the normal way)."""
import os
import subprocess
import time


class Display:
    def __init__(self, number, size, procs):
        self.number, self.size, self.procs = number, tuple(size), procs
        self.name = f':{number}'
        self.env = dict(os.environ, DISPLAY=self.name)

    def stop(self):
        for p in reversed(self.procs):
            if p.poll() is None:
                p.terminate()
                try:
                    p.wait(5)
                except subprocess.TimeoutExpired:
                    p.kill()


def start(size, number=99, wm=True, timeout=10.0):
    os.makedirs(os.environ.get('XDG_RUNTIME_DIR', '/tmp/xdg'), mode=0o700, exist_ok=True)
    sock = f'/tmp/.X11-unix/X{number}'
    xvfb = subprocess.Popen(['Xvfb', f':{number}', '-screen', '0', f'{size[0]}x{size[1]}x24', '-nolisten', 'tcp',
                             '-ac'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.time() + timeout
    while not os.path.exists(sock):
        if time.time() > end or xvfb.poll() is not None:
            raise RuntimeError(f'Xvfb :{number} did not start')
        time.sleep(0.05)
    procs = [xvfb]
    d = Display(number, size, procs)
    if wm:
        procs.append(subprocess.Popen(['openbox'], env=d.env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        time.sleep(0.5)
    return d
