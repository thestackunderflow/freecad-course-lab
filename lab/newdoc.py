"""Lab instrument: a new, empty document in the running FreeCAD (the state a Claude run starts from).
    python3 -m lab.newdoc NAME"""
import sys

sys.path.insert(0, '/lab')
from lab import fcrpc  # noqa: E402

if __name__ == '__main__':
    print(fcrpc.run('import FreeCAD' + chr(10) + 'FreeCAD.newDocument(%r)' % sys.argv[1] + chr(10) + 'print(1)'))
