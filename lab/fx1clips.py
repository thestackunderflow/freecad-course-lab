"""Zoomed, silent clips of the fx1 takes, cut by event time (footage.py hand-off). Run inside screen-lab-base style image:
    FOOTAGE_PY=/footage/footage.py python3 /lab/lab/fx1clips.py [name ...]
Output: out/fx1/clips/<name>.mp4 (1920x1080, 30 fps, click rings, no chip: the build stage adds chips/labels)."""
import importlib.util
import json
import os
import sys

spec = importlib.util.spec_from_file_location('footage', os.environ['FOOTAGE_PY'])
footage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(footage)

OUT = '/lab/out/fx1'
SIZE = (1920, 1080)
SRC = (2880, 1800)
os.makedirs(f'{OUT}/clips', exist_ok=True)


def ev(take):
    return [json.loads(l) for l in open(f'{OUT}/{take}/events.jsonl')]


def at(take, label, nth=0):
    return [e for e in ev(take) if e['event'] == label][nth]['t']


# (clip name, take, start, end, zoom, mode) ; mode 'cursor' follows the cursor, a box [x,y,w,h] holds a fixed crop
def segs():
    S = []
    # terminal crop box: left 1150 px of the display, top part where the 3-line crop sits
    TERM = [{'t': 0, 'box': [0, 0, 1150, 650]}]
    # FreeCAD window (right side), the top with the menus / workbench list / toolbar
    FCTOP = [{'t': 0, 'box': [1150, 0, 1730, 970]}]
    FCBOT = [{'t': 0, 'box': [1150, 830, 1730, 970]}]
    a = 'A'
    S.append(('F0-A-filemanager', a, at(a, 'file manager: old Mod/FreeCADMCP') - 0.3, at(a, 'file manager: old Mod/FreeCADMCP') + 4.0, 1.6, [{'t': 0, 'box': [1150, 0, 1730, 973]}]))
    S.append(('F0-A-workbench-list', a, at(a, 'workbench list: opened (no MCP Addon)') - 1.0, at(a, 'workbench list: opened (no MCP Addon)') + 5.5, 1.6, FCTOP))
    S.append(('A-report-view', a, at(a, 'report view: shown') - 1.0, at(a, 'report view: shown') + 5.0, 1.6, FCBOT))
    b = 'B'
    S.append(('F2-B-console', b, at(b, 'console: opened') - 1.0, at(b, 'console: path printed') + 4.5, 1.6, FCBOT))
    c = 'C-drag'
    S.append(('F1-C-drag', c, at(c, 'file manager: new folder Mod') - 1.0, at(c, 'file manager: drag FreeCADMCP to v1-1/Mod: released') + 3.0, 1.2, None))
    S.append(('F1-C-drag-list', c, at(c, 'workbench list: opened') - 1.0, at(c, 'workbench list: MCP Addon chosen') + 3.0, 1.6, FCTOP))
    S.append(('F5-C-drag-start', c, at(c, 'FreeCAD: Start RPC Server') - 1.0, at(c, 'status bar: started') + 5.0, 1.5, None))
    t = 'C-terminal'
    for name, lab in (('F4-1-ls', 'terminal: ls FreeCAD typed'), ('F4-2-mkdir', 'terminal: mkdir -p typed'),
                      ('F4-3-mv', 'terminal: mv typed'), ('F4-4-ls-InitGui', 'terminal: ls InitGui shown')):
        S.append((name, t, at(t, lab) - 0.5, at(t, lab + ': Enter') + 3.0, 2.4, TERM))
    S.append(('F5-C-terminal-list', t, at(t, 'workbench list: opened') - 1.0, at(t, 'workbench list: MCP Addon chosen') + 3.0, 1.6, FCTOP))
    d = 'D'
    for name, lab in (('F7-1-cp-star', 'terminal: cp star typed'), ('F7-2-ls-loose', 'terminal: ls Mod loose')):
        S.append((name, d, at(d, lab) - 0.5, at(d, lab + ': Enter') + 3.5, 2.4, TERM))
    S.append(('F7-D-list', d, at(d, 'workbench list: opened (no MCP Addon)') - 1.0, at(d, 'workbench list: opened (no MCP Addon)') + 5.0, 1.6, FCTOP))
    S.append(('D-report-view', d, at(d, 'report view: shown') - 1.0, at(d, 'report view: shown') + 5.0, 1.6, FCBOT))
    e = 'E'
    for name, lab in (('F8-1-mkdir', 'terminal: mkdir FreeCADMCP typed'), ('F8-2-mv', 'terminal: mv loose typed'),
                      ('F8-3-ls-Mod', 'terminal: ls Mod after mv')):
        S.append((name, e, at(e, lab) - 0.5, at(e, lab + ': Enter') + 3.0, 2.4, TERM))
    S.append(('F8-E-list', e, at(e, 'workbench list: MCP Addon') - 1.0, at(e, 'workbench list: closed') + 0.5, 1.6, FCTOP))
    S.append(('F8-4-ls-R', e, at(e, 'terminal: ls -R typed') - 0.5, at(e, 'terminal: ls -R typed: Enter') + 5.0, 2.4, TERM))
    return S


def main():
    want = set(sys.argv[1:])
    out = []
    for name, take, t0, t1, zoom, focus in segs():
        if want and name not in want:
            continue
        p = f'{OUT}/clips/{name}.mp4'
        d = f'{OUT}/{take}'
        clicks = [(e['t'], e['x'], e['y']) for e in ev(take) if 'button' in e and t0 <= e['t'] <= t1]
        kw = {'focus': focus} if focus else {'cursor': f'{d}/cursor.jsonl'}
        footage.clip(f'{d}/screen.mp4', p, src=SRC, t0=max(0, t0), t1=t1, zoom=zoom, size=SIZE, clicks=clicks, **kw)
        out.append({'clip': name, 'take': take, 't0': round(t0, 2), 't1': round(t1, 2)})
    print(json.dumps(out, indent=0))


main()
