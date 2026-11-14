"""Take D (LAB-fx19 3.D), no AI: the same plug Claude uses (uvx freecad-mcp@0.1.28, stdio), one execute_code call that
opens hook-gap.FCStd and pads its sketch 20 mm with NO prints, then the same on a second copy WITH the two prints.
Prints exactly what each reply carries.      python3 noai.py   (in ~/fx19, FreeCAD running with its socket on)"""
import json
import sys

sys.path.insert(0, '/lab')
from client.mcp import McpClient  # noqa: E402

CODE = """import FreeCAD
d = FreeCAD.openDocument('/home/maker/fx19/{name}.FCStd')
s = d.getObject('Sketch')
pad = d.getObject('Body').newObject('PartDesign::Pad', 'Pad')
pad.Profile = s
pad.Length = 20
d.recompute()
"""
PRINTS = """print(pad.isValid())
print(pad.getStatusString())
"""

c = McpClient(['uvx', 'freecad-mcp@0.1.28'], timeout_s=180, log_path='/lab/out/fx19/D/transcript.jsonl')
c.start()
for n, (name, extra) in enumerate((('gap-1', ''), ('gap-2', PRINTS)), 1):
    print('=== call %d: execute_code, %s' % (n, 'with the two prints' if extra else 'no prints'))
    r = c.call_tool('execute_code', {'code': CODE.format(name=name) + extra})
    print('reply text:', McpClient.text(r))
    print('isError:', r.get('isError', False), '| content types:', [x.get('type') for x in r.get('content', [])])
    print()
c.close()
