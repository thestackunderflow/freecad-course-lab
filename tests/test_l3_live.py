"""Lesson 3 live check in the lab image (freecadcmd, no display): lesson 2's Part Design J with a spreadsheet of five
named sizes, the six sizes and the pad written from them (expressions), measured with the course's measuring script
before and after one cell changes (hook_depth 25 to 40), and scored with the pre-registered rules. This proves the
checker on a known part; it is not the by-hand take or Claude's run."""
import json
import os
import shutil
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, LAB)
pytestmark = pytest.mark.skipif(shutil.which('freecadcmd') is None, reason='needs the lab image (freecadcmd)')

BUILD = r'''
import FreeCAD as App, Part, Sketcher
d = App.newDocument('J')
ss = d.addObject('Spreadsheet::Sheet', 'Spreadsheet')
for r, (n, v) in enumerate([('plate_height', 60), ('width', 20), ('thickness', 5), ('hook_depth', 25), ('lip_height', 10)], 1):
    ss.set('A%d' % r, n); ss.set('B%d' % r, str(v)); ss.setAlias('B%d' % r, n)
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
dims = []
for geo, val, expr in ((0, 25, 'hook_depth'), (1, 10, 'lip_height'), (2, 5, 'thickness'),
                       (3, 5, 'lip_height - thickness'), (5, 55, 'plate_height - thickness'), (6, 5, 'thickness')):
    i = sk.addConstraint(Sketcher.Constraint('Distance', geo, val))
    sk.renameConstraint(i, 'c%d' % i)          # a named size: 1.1.4 keys its expression '.Constraints.c<i>'
    sk.setExpression('.Constraints.c%d' % i, ' '.join('Spreadsheet.' + w if w[0].isalpha() else w for w in expr.split()))
k = sk.addGeometry(Part.LineSegment(App.Vector(12.5, 0, 0), App.Vector(12.5, 60, 0)), True)   # a construction line
pad = body.newObject('PartDesign::Pad', 'Pad')
pad.Profile = sk
pad.setExpression('Length', 'Spreadsheet.width')
d.recompute()
d.saveAs(OUT)
ss.set('hook_depth', '40')
d.recompute()
d.saveAs(OUT40)
ss.set('thickness', '8')
d.recompute()
d.saveAs(OUT8)
'''


def _measure(fc, out):
    subprocess.run(['freecadcmd', os.path.join(LAB, 'checker', 'measure.py')], capture_output=True, text=True,
                   timeout=180, env=dict(os.environ, FC_DOC=str(fc), FC_OUT=str(out)))
    return json.loads(out.read_text())


def test_one_cell_moves_the_part_and_the_checker_reads_names_expressions_and_corners(tmp_path):
    fc, fc40, fc8 = tmp_path / 'j.FCStd', tmp_path / 'j40.FCStd', tmp_path / 'j8.FCStd'
    script = tmp_path / 'build.py'
    script.write_text('OUT = %r\nOUT40 = %r\nOUT8 = %r\n' % (str(fc), str(fc40), str(fc8)) + BUILD, encoding='utf-8')
    r = subprocess.run(['freecadcmd', str(script)], capture_output=True, text=True, timeout=180)
    assert fc8.exists(), r.stdout[-2000:] + r.stderr[-2000:]
    m25, m40, m8 = (_measure(f, tmp_path / ('m%d.json' % i)) for i, f in enumerate((fc, fc40, fc8)))
    assert m25['sheets'][0]['aliases'] == {'plate_height': '60', 'width': '20', 'thickness': '5', 'hook_depth': '25',
                                           'lip_height': '10'}
    sk = m25['sketches'][0]
    assert [d['expression'] for d in sk['dimensions']][0] == 'Spreadsheet.hook_depth'
    assert sorted(map(tuple, sk['corners_xy'])) == sorted([(0, 0), (25, 0), (25, 10), (20, 10), (20, 5), (5, 5), (5, 60), (0, 60)])
    assert m25['pads'][0]['expression'] == 'Spreadsheet.width' and m25['pads'][0]['length'] == 20.0
    assert m40['sheets'][0]['aliases']['hook_depth'] == '40'
    from checker import compare, score_l3
    p = compare.final_solids(m40)[0]
    assert p['volume_mm3'] == 10000.0 and p['bbox_mm'] == [40.0, 20.0, 60.0]
    assert compare.final_solids(m8)[0]['volume_mm3'] == 15040.0
    s = score_l3.score(m25, m40, m8, ["ss.set('hook_depth', '40')"], ["ss.set('thickness', '8')"])
    assert s['names']['exprs_from_names'] == 7 and s['names']['sketch_sizes_from_names'] == 6, s
    assert s['first_build_right'] and s['edit2_by_one_cell'] and s['edit3_by_one_cell'], s
    assert s['corners'] == {'first': True, 'after2': True, 'after3': True}      # the construction line is skipped
