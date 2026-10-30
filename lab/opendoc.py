"""Lab instrument (lesson 4), not filmed: open a saved FreeCAD document in the running FreeCAD over the add-on's
socket (the replay starts from lesson 3's hook, as the Claude runs did).   python3 -m lab.opendoc PATH"""
import sys

sys.path.insert(0, '/lab')
from lab import fcrpc  # noqa: E402

if __name__ == '__main__':
    print(fcrpc.run('import FreeCAD\nd = FreeCAD.openDocument(%r)\nprint(d.Name)' % sys.argv[1]))
