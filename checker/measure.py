"""(From the screen-lab kit's apps/freecad/measure.py, plus the corner position min_mm.) The one measuring line for
every block in the lesson, by hand, by Claude or by the replay.
Measure a saved FreeCAD document headlessly (no GUI): every solid's volume, bounding box and validity.
    FC_DOC=/path/part.FCStd FC_OUT=/path/measure.json freecadcmd /lab/checker/measure.py
(freecadcmd passes no script arguments through, so the paths come from the environment.)"""
import json
import os

import FreeCAD

doc = FreeCAD.openDocument(os.environ['FC_DOC'])
doc.recompute()
rows = []
for o in doc.Objects:
    shp = getattr(o, 'Shape', None)
    if shp is None or shp.isNull() or not shp.Solids:
        continue
    b = shp.BoundBox
    rows.append({'name': o.Name, 'label': o.Label, 'type': o.TypeId, 'volume_mm3': round(shp.Volume, 4),
                 'valid': shp.isValid(), 'solids': len(shp.Solids),
                 'bbox_mm': [round(b.XLength, 4), round(b.YLength, 4), round(b.ZLength, 4)],
                 'z_range_mm': [round(b.ZMin, 4), round(b.ZMax, 4)],
                 'min_mm': [round(b.XMin, 4), round(b.YMin, 4), round(b.ZMin, 4)]})
res = {'document': os.path.basename(os.environ['FC_DOC']), 'freecad': '.'.join(FreeCAD.Version()[:3]),
       'objects': [o.Name for o in doc.Objects], 'solids': rows}
with open(os.environ['FC_OUT'], 'w') as f:
    json.dump(res, f, indent=1)
print(json.dumps(res))
