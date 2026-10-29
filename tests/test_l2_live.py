"""Lesson 2 live check in the lab image (freecadcmd, no display): a J built the Part Design way in a script (a body, a
sketch attached to XZ_Plane, eight lines with level/upright pins, six sizes, a pad of 20) and measured with the
course's one measuring script. This proves the checker on a known part; it is not the by-hand take or Claude's run."""
import json
import os
import shutil
import subprocess

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, '..'))
pytestmark = pytest.mark.skipif(shutil.which('freecadcmd') is None, reason='needs the lab image (freecadcmd)')

BUILD = r'''
import FreeCAD as App, Part, Sketcher
d = App.newDocument('J')
body = d.addObject('PartDesign::Body', 'Body')
sk = body.newObject('Sketcher::SketchObject', 'Sketch')
xz = [f for f in body.Origin.OriginFeatures if f.Role == 'XZ_Plane'][0]
sk.AttachmentSupport = [(xz, '')]
sk.MapMode = 'FlatFace'
pts = [(0, 0), (25, 0), (25, 10), (20, 10), (20, 5), (5, 5), (5, 60), (0, 60)]
for i in range(8):
    a, b = pts[i], pts[(i + 1) % 8]
    sk.addGeometry(Part.LineSegment(App.Vector(a[0], a[1], 0), App.Vector(b[0], b[1], 0)))
for i in range(8):
    sk.addConstraint(Sketcher.Constraint('Coincident', i, 2, (i + 1) % 8, 1))
    a, b = pts[i], pts[(i + 1) % 8]
    sk.addConstraint(Sketcher.Constraint('Horizontal' if a[1] == b[1] else 'Vertical', i))
sk.addConstraint(Sketcher.Constraint('Coincident', 0, 1, -1, 1))
for geo, val in ((0, 25), (1, 10), (2, 5), (3, 5), (5, 55), (6, 5)):
    sk.addConstraint(Sketcher.Constraint('Distance', geo, val))
pad = body.newObject('PartDesign::Pad', 'Pad')
pad.Profile = sk
pad.Length = 20
d.recompute()
d.saveAs(OUT)
'''


def test_a_part_design_j_measures_8500_and_its_sketch_is_fully_constrained(tmp_path):
    fc = tmp_path / 'j.FCStd'
    script = tmp_path / 'build.py'
    script.write_text('OUT = %r\n' % str(fc) + BUILD, encoding='utf-8')
    r = subprocess.run(['freecadcmd', str(script)], capture_output=True, text=True, timeout=180)
    assert fc.exists(), r.stdout[-2000:] + r.stderr[-2000:]
    out = tmp_path / 'm.json'
    subprocess.run(['freecadcmd', os.path.join(LAB, 'checker', 'measure.py')], capture_output=True, text=True,
                   timeout=180, env=dict(os.environ, FC_DOC=str(fc), FC_OUT=str(out)))
    m = json.loads(out.read_text())
    import sys
    sys.path.insert(0, LAB)
    from checker import compare
    part = compare.final_solids(m)
    assert [p['type'] for p in part] == ['PartDesign::Body']
    assert part[0]['volume_mm3'] == 8500.0 and part[0]['bbox_mm'] == [25.0, 20.0, 60.0]
    sk = m['sketches'][0]
    assert sk['support'][0][0].startswith('XZ_Plane') and sk['geometry'] == 8
    assert sk['dependent_parameters'] == 0 or sk['fully_constrained'] is True
    assert [f['type'] for f in m['bodies'][0]['features']] == ['Sketcher::SketchObject', 'PartDesign::Pad']
    (tmp_path / 'report.json').write_text(json.dumps({'z': part[0]['z_range_mm'], 'min': part[0]['min_mm'],
                                                      'sketch': sk}), encoding='utf-8')
    print(json.dumps({'z': part[0]['z_range_mm'], 'min': part[0]['min_mm'], 'up': sk['up_vector'],
                      'normal': sk['normal'], 'fc': sk['fully_constrained'], 'dep': sk['dependent_parameters']}))
