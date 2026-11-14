# Take P (LAB-fx20 3.P, not filmed): P/hook.FCStd = a copy of lesson 2's hand.FCStd; P/hook-red.FCStd came from G0a step 3.
# freecadcmd /lab/out/fx20/P/make.py  -> P/check.txt (stop rule P0: DoF 0 and 8500 within 0.1%)
import shutil, sys, FreeCAD
shutil.copy('/lab/out/l2/hand/hand.FCStd', '/lab/out/fx20/P/hook.FCStd')
out = []
for f in ('hook', 'hook-red'):
    shutil.copy('/lab/out/fx20/P/%s.FCStd' % f, '/tmp/%s.FCStd' % f)
    d = FreeCAD.openDocument('/tmp/%s.FCStd' % f)
    s = d.getObject('Sketch'); p = d.getObject('Pad')
    for o in d.Objects: o.touch()
    d.recompute()
    out.append('%s: constraints %d solve %s DoF %s conflicting %s pad valid %s volume %s' % (
        f, len(s.Constraints), s.solve(), s.DoF, list(s.ConflictingConstraints), p.isValid(),
        None if p.Shape.isNull() else round(p.Shape.Volume, 4)))
    FreeCAD.closeDocument(d.Name)
ok = 'hook: constraints 23 solve 0 DoF 0' in out[0] and 'volume 8500.0' in out[0]
out.append('P0 %s' % ('PASS' if ok else 'FAIL'))
open('/lab/out/fx20/P/check.txt', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
