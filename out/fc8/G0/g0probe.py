import FreeCAD, sys
print('VER', FreeCAD.Version()[:4])
for m in ('Assembly', 'JointObject', 'UtilsAssembly', 'Spreadsheet', 'Part', 'Measure'):
    try:
        __import__(m); print('IMPORT', m, 'ok')
    except Exception as e:
        print('IMPORT', m, 'fail', e)
import os
d = '/opt/freecad/usr/Mod/Assembly'
print('ASM FILES', sorted(os.listdir(d)) if os.path.isdir(d) else 'nodir')
