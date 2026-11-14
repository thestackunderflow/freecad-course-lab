"""Take D (LAB-fx20 3.D), no AI: the plug Claude uses (uvx freecad-mcp@0.1.28, stdio). Four execute_code calls, each
on its own copy: (1) a new arm-top size, then setDatum 17, no prints; (2) the same, the exception printed;
(3) hook-red.FCStd opened and recomputed, no prints; (4) the same, solve code + conflicts printed.
Prints what each reply carries.      python3 noai.py   (in ~/fx20, FreeCAD running with its socket on)"""
import sys

sys.path.insert(0, '/lab')
from client.mcp import McpClient  # noqa: E402

SIZE = """import FreeCAD, Sketcher
d = FreeCAD.openDocument('/home/maker/fx20/{name}.FCStd')
s = d.getObject('Sketch')
i = s.addConstraint(Sketcher.Constraint('DistanceX', 4, 2, 4, 1, 15))
"""
SET = "s.setDatum(i, FreeCAD.Units.Quantity('17 mm'))\nd.recompute()\n"
SET_P = """try:
    s.setDatum(i, FreeCAD.Units.Quantity('17 mm'))
except Exception as e:
    print(type(e).__name__ + ':', e)
d.recompute()
print('arm top', s.Geometry[4].length())
"""
RED = """import FreeCAD
d = FreeCAD.openDocument('/home/maker/fx20/{name}.FCStd')
s = d.getObject('Sketch')
d.recompute()
"""
RED_P = "print('solve', s.solve(), 'conflicting', list(s.ConflictingConstraints))\n"

CALLS = [('size-1', SIZE + SET, 'arm-top size 17, no prints'),
         ('size-2', SIZE + SET_P, 'arm-top size 17, the error printed'),
         ('red-1', RED, 'hook-red opened, no prints'),
         ('red-2', RED + RED_P, 'hook-red opened, solve + conflicts printed')]

c = McpClient(['uvx', 'freecad-mcp@0.1.28'], timeout_s=180, log_path='/lab/out/fx20/D/transcript.jsonl')
c.start()
for n, (name, code, what) in enumerate(CALLS, 1):
    print('=== call %d: %s' % (n, what))
    r = c.call_tool('execute_code', {'code': code.format(name=name)})
    print('reply text:', McpClient.text(r))
    print('isError:', r.get('isError', False), '| types:', [x.get('type') for x in r.get('content', [])])
    print()
c.close()
