import FreeCAD
d = FreeCAD.openDocument('/lab/out/fc16/P/hole-typed.FCStd'); d.recompute()
d.getObject('Params').set('wall', '3'); d.recompute()
for o in d.Objects:
    if o.TypeId.startswith('PartDesign::') and o.TypeId != 'PartDesign::Body': o.touch()
d.recompute(); d.saveAs('/lab/out/fc16/P/hole-typed-w3.FCStd'); print('PX saved')
