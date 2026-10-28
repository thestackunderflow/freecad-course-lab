"""A take: a declarative list of steps (YAML or JSON) that films one app on the virtual screen.

    python3 -m screenlab.take TAKE.yaml OUT_DIR [--display :99]

Starts the display and the app, waits for its window (maximised, focused), records, runs the steps, stops cleanly,
then runs the `after` commands (for example measuring a file the take saved). See the README for the format."""
import argparse
import json
import os
import signal
import subprocess
import sys
import time

ACTIONS = ('glide', 'click', 'type', 'key', 'drag', 'scroll', 'wait', 'wait_window', 'wake', 'shot', 'mark')
MODIFIERS = ('mark', 'hold', 'steps', 'ms', 'pre', 'button', 'double', 'delay_ms', 'timeout')


class TakeError(ValueError):
    pass


def _xy(v):
    return isinstance(v, (list, tuple)) and len(v) == 2 and all(isinstance(a, (int, float)) for a in v)


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def action_of(step):
    acts = [k for k in step if k in ACTIONS and k != 'mark']
    if len(acts) > 1:
        raise TakeError(f'one action per step, got {acts}')
    if acts:
        return acts[0]
    if 'mark' in step:
        return 'mark'
    raise TakeError(f'unknown step {sorted(step)}; actions are {", ".join(ACTIONS)}')


def check_step(s):
    if not isinstance(s, dict):
        raise TakeError('a step is a mapping like {click: [x, y]}')
    a = action_of(s)
    extra = [k for k in s if k not in ACTIONS and k not in MODIFIERS]
    if extra:
        raise TakeError(f'unknown step key(s) {extra}')
    v = s[a]
    if a in ('glide', 'click') and not _xy(v):
        raise TakeError(f'{a} needs [x, y]')
    if a == 'type' and not isinstance(v, str):
        raise TakeError('type needs text')
    if a in ('key', 'wait_window', 'shot') and not isinstance(v, str):
        raise TakeError(f'{a} needs a string')
    if a == 'drag' and not (isinstance(v, dict) and _xy(v.get('from')) and _xy(v.get('to'))):
        raise TakeError('drag needs from and to, each [x, y]')
    if a == 'scroll' and not (isinstance(v, dict) and _xy(v.get('at')) and v.get('dir', 'down') in ('up', 'down')):
        raise TakeError('scroll needs at: [x, y] (clicks: N, dir: up|down)')
    if a == 'wait' and not (_num(v) and v >= 0):
        raise TakeError('wait needs seconds')
    if 'button' in s and s['button'] not in (1, 2, 3):
        raise TakeError('button must be 1, 2 or 3')
    if a == 'mark' and not isinstance(s['mark'], str):
        raise TakeError('mark needs a label')
    return a


def validate(t):
    if not isinstance(t, dict) or not isinstance(t.get('steps'), list):
        raise TakeError('a take needs a list of steps')
    out = dict(t)
    out['display'] = dict({'size': [1920, 1080]}, **(t.get('display') or {}))
    out.setdefault('units', None)
    out.setdefault('pace', 1.0)
    out.setdefault('wake', False)
    out.setdefault('after', [])
    out.setdefault('app', None)
    out['setup'] = list(t.get('setup') or [])
    out['finish'] = list(t.get('finish') or [])
    for kind, steps in (('setup step', out['setup']), ('step', t['steps']), ('finish step', out['finish'])):
        for i, s in enumerate(steps, 1):
            try:
                check_step(s)
            except TakeError as e:
                raise TakeError(f'{kind} {i}: {e}') from None
    return out


def load(path):
    text = open(path, encoding='utf-8').read()
    if path.lower().endswith('.json'):
        data = json.loads(text)
    else:
        import yaml
        data = yaml.safe_load(text)
    return validate(data)


def _opt(s, *keys):
    return {k: s[k] for k in keys if k in s}


def run_steps(t, actor, out, clock=time.time, wait_window=None, steps=None):
    timings = []
    for i, s in enumerate(t['steps'] if steps is None else steps, 1):
        a = action_of(s)
        start = clock()
        v = s[a]
        if a == 'glide':
            actor.glide(tuple(v), steps=s.get('steps'), ms=s.get('ms'), **_opt(s, 'mark', 'hold'))
        elif a == 'click':
            actor.click(tuple(v), button=s.get('button', 1), double=s.get('double', False), mark=s.get('mark'),
                        steps=s.get('steps'), ms=s.get('ms'), **_opt(s, 'pre', 'hold'))
        elif a == 'type':
            actor.type(v, delay_ms=s.get('delay_ms', 120), mark=s.get('mark'), **_opt(s, 'hold'))
        elif a == 'key':
            actor.key(v, mark=s.get('mark'), **_opt(s, 'hold'))
        elif a == 'drag':
            actor.drag(tuple(v['from']), tuple(v['to']), button=s.get('button', v.get('button', 1)),
                       mark=s.get('mark'), steps=s.get('steps'), ms=s.get('ms'), **_opt(s, 'hold'))
        elif a == 'scroll':
            actor.scroll(tuple(v['at']), clicks=v.get('clicks', 3), direction=v.get('dir', 'down'),
                         mark=s.get('mark'), hold=s.get('hold', 0.6))
        elif a == 'wait':
            if s.get('mark'):
                actor.mark(s['mark'])
            actor.wait(v)
        elif a == 'wait_window':
            if wait_window(v, s.get('timeout', 30)) is None:
                raise TakeError(f'step {i}: no window named {v!r} within {s.get("timeout", 30)} s')
            if s.get('mark'):
                actor.mark(s['mark'])
        elif a == 'wake':
            actor.wake()
        elif a == 'shot':
            actor.shot(os.path.join(out, v), wake=t.get('wake', False))
        elif a == 'mark':
            actor.mark(v)
        timings.append({'i': i, 'action': a, 'mark': s.get('mark') if a != 'mark' else v, 'start': start,
                        'end': clock()})
    return timings


def run(t, out, display=':99'):
    """The whole take on a fresh display. Returns the take.json content."""
    from . import actions, logs, recorder, x as xmod
    from . import display as dmod
    if isinstance(t, str):
        t = load(t)
    else:
        t = validate(t)
    os.makedirs(out, exist_ok=True)
    size = tuple(t['display']['size'])
    d = dmod.start(size, number=int(display.lstrip(':')), wm=t['display'].get('wm', True))
    xd = xmod.XDo(env=d.env)
    app_proc = None
    result = {'take': t}
    try:
        app = t['app']
        if app:
            env = dict(d.env, **{k: str(v) for k, v in (app.get('env') or {}).items()})
            app_proc = subprocess.Popen(app['cmd'], env=env, stdout=open(os.path.join(out, 'app.log'), 'w'),
                                        stderr=subprocess.STDOUT, start_new_session=True, cwd=app.get('cwd'))
            wid = xd.wait_window(app['window'], timeout=app.get('timeout', 60))
            if wid is None:
                raise TakeError(f'app window {app["window"]!r} did not appear (see app.log)')
            time.sleep(app.get('settle', 2))
            wid = xd.search(app['window'])[0]
            if app.get('maximise', True):
                xmod.maximise(xd, wid, size, wmctrl_env=d.env)
            xd.focus(wid)
            time.sleep(0.5)
        start_at = t.get('start_at') or [size[0] // 2, size[1] // 2]
        xd.move(*start_at)
        ev = logs.EventLog(os.path.join(out, 'events.raw.jsonl'))
        actor = actions.Actor(xd, ev, units=t['units'], display=size, pace=t['pace'])
        actor.shot = lambda path, wake=False: (actor.wake() if wake else None,
                                               xmod.screenshot(path, d.name, size, d.env))
        if t['setup']:                   # not filmed: first-run dialogs, preferences, window layout
            run_steps(t, actor, out, wait_window=lambda rx, timeout: xd.wait_window(rx, timeout), steps=t['setup'])
            if os.path.exists(ev.path):
                os.remove(ev.path)       # setup marks are not part of the recording
        rec = recorder.Recorder(out, size, display=d.name, draw_mouse=t.get('draw_mouse', True)).start()
        try:
            timings = run_steps(t, actor, out, wait_window=lambda rx, timeout: xd.wait_window(rx, timeout))
        finally:
            meta = rec.stop()
        t0 = meta['t0_epoch']
        result['record'] = meta
        result['timings'] = [dict(r, start=round(r['start'] - t0, 3), end=round(r['end'] - t0, 3)) for r in timings]
        if t.get('wake'):
            actor.wake()
        xmod.screenshot(os.path.join(out, 'end.png'), d.name, size, d.env)
        if t['finish']:                  # not filmed: save the file the `after` commands measure, and so on
            actor.ev = logs.EventLog(os.devnull)
            run_steps(t, actor, out, wait_window=lambda rx, timeout: xd.wait_window(rx, timeout), steps=t['finish'])
        result['after'] = []
        for cmd in t['after']:
            r = subprocess.run(['bash', '-c', cmd], env=dict(d.env, OUT=out), capture_output=True, text=True)
            with open(os.path.join(out, 'after.log'), 'a') as f:
                f.write(f'$ {cmd}\n{r.stdout}{r.stderr}[exit {r.returncode}]\n')
            result['after'].append({'cmd': cmd, 'exit': r.returncode})
        with open(os.path.join(out, 'take.json'), 'w') as f:
            json.dump(result, f, indent=1)
    finally:
        if app_proc and app_proc.poll() is None:
            quit_keys = (t.get('app') or {}).get('quit')
            if quit_keys:
                xd.key(quit_keys)
                try:
                    app_proc.wait(10)
                except subprocess.TimeoutExpired:
                    pass
            if app_proc.poll() is None:
                try:
                    os.killpg(app_proc.pid, signal.SIGTERM)
                    app_proc.wait(10)
                except (ProcessLookupError, subprocess.TimeoutExpired):
                    os.killpg(app_proc.pid, signal.SIGKILL)
        d.stop()
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('take')
    ap.add_argument('out')
    ap.add_argument('--display', default=':99')
    a = ap.parse_args(argv)
    r = run(a.take, a.out, a.display)
    print(json.dumps({'out': a.out, 'events': len(open(os.path.join(a.out, 'events.jsonl')).readlines()),
                      'after': r.get('after')}))


if __name__ == '__main__':
    sys.exit(main())
