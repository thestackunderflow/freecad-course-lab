"""Lesson 4 live check in the lab image (freecadcmd, no display): lesson 3's named hook at hook_depth 40 gets two names
(hole_d, hole_spacing), a sketch on the back plate's back face with two circles whose centres are written from names
(across: width / 2; up: (plate_height -+ hole_spacing) / 2), a Hole feature through all with Diameter = hole_d, and a
2 mm fillet on the lip's top outer edge. Measured with the course's measuring script at width 20 and width 30, and the
same part with the centres typed as plain numbers (10 across). This proves the checker on known parts; it is not the
by-hand take or Claude's run."""
import json
import os
import shutil
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, LAB)
sys.path.insert(0, HERE)
pytestmark = pytest.mark.skipif(shutil.which('freecadcmd') is None, reason='needs the lab image (freecadcmd)')

from test_l3_live import BUILD as BUILD3  # noqa: E402

HOLES = r'''
# BUILD3's sheet is unitless (a value with mm beside one without is a unit-mismatch error), so these are too
ss.set('hook_depth', '40'); ss.set('thickness', '5')
ss.set('A6', 'hole_d'); ss.set('B6', '4'); ss.setAlias('B6', 'hole_d')
ss.set('A7', 'hole_spacing'); ss.set('B7', '30'); ss.setAlias('B7', 'hole_spacing')
d.recompute()
back = [i for i, f in enumerate(pad.Shape.Faces) if abs(f.normalAt(0, 0).x + 1) < 1e-6 and abs(f.CenterOfMass.x) < 1e-6]
hs = body.newObject('Sketcher::SketchObject', 'HoleSketch')
hs.AttachmentSupport = [(pad, 'Face%d' % (back[0] + 1))]
hs.MapMode = 'FlatFace'
d.recompute()
# a face's own orientation depends on how its outline was drawn; the GUI take's sketch on this face came out with its
# normal -X (out of the back) and its x axis -Y; this script's outline gives another, so the same placement is set
hs.MapMode = 'Deactivated'
hs.Placement = App.Placement(App.Vector(0, 0, 0), App.Rotation(-90, 0, 90))
d.recompute()
for k, y in enumerate((15, 45)):
    g = hs.addGeometry(Part.Circle(App.Vector(10, y, 0), App.Vector(0, 0, 1), 2), False)
    cx = hs.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, g, 3, 10))
    cy = hs.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, g, 3, y))
    hs.addConstraint(Sketcher.Constraint('Diameter', g, 4))
    if not PLAIN:
        hs.setExpression('Constraints[%d]' % cx, 'Spreadsheet.width / 2')
        hs.setExpression('Constraints[%d]' % cy, '(Spreadsheet.plate_height %s Spreadsheet.hole_spacing) / 2' % '-+'[k])
hole = body.newObject('PartDesign::Hole', 'Hole')
hole.Profile = hs
hole.DepthType = 'ThroughAll'
hole.setExpression('Diameter', 'Spreadsheet.hole_d')
d.recompute()
lip = [i for i, e in enumerate(hole.Shape.Edges)
       if {round(v.X, 3) for v in e.Vertexes} == {40.0} and {round(v.Z, 3) for v in e.Vertexes} == {10.0}]
fil = body.newObject('PartDesign::Fillet', 'Fillet')
fil.Base = (hole, ['Edge%d' % (lip[0] + 1)])
fil.Radius = 2
d.recompute()
d.saveAs(OUTH)
ss.set('width', '30')
d.recompute()
d.saveAs(OUTW)
'''


def _measure(fc, out):
    subprocess.run(['freecadcmd', os.path.join(LAB, 'checker', 'measure.py')], capture_output=True, text=True,
                   timeout=180, env=dict(os.environ, FC_DOC=str(fc), FC_OUT=str(out)))
    return json.loads(out.read_text())


def _build(tmp_path, plain):
    t = tmp_path / ('plain' if plain else 'named')
    t.mkdir()
    fh, fw = t / 'h.FCStd', t / 'w30.FCStd'
    script = t / 'build.py'
    script.write_text('OUT = %r\nOUT40 = %r\nOUT8 = %r\nOUTH = %r\nOUTW = %r\nPLAIN = %r\n'
                      % (str(t / 'j.FCStd'), str(t / 'j40.FCStd'), str(t / 'j8.FCStd'), str(fh), str(fw), plain)
                      + BUILD3 + HOLES, encoding='utf-8')
    r = subprocess.run(['freecadcmd', str(script)], capture_output=True, text=True, timeout=240)
    assert fw.exists(), r.stdout[-2000:] + r.stderr[-2000:]
    return _measure(fh, t / 'mh.json'), _measure(fw, t / 'mw.json')


def test_holes_from_names_stay_centred_at_width_30_and_the_fillet_follows(tmp_path):
    from checker import holes, score_l4
    mh, mw = _build(tmp_path, plain=False)
    top = score_l4._part(mh)
    c = holes.check(top, holes.NAMES)
    assert c['ok'], c
    assert c['hole_sides_mm'] == [[10.0, 10.0], [10.0, 10.0]]
    c30 = holes.check(score_l4._part(mw), dict(holes.NAMES, width=30))
    assert c30['ok'], c30
    assert c30['hole_sides_mm'] == [[15.0, 15.0], [15.0, 15.0]] and c30['fillet_on_lip_edge']
    s = score_l4.score(mh, mw, [('execute_code', json.dumps({'code': "ss.set('width', '30')"}))])
    assert s['names']['hole_names'] == ['hole_d', 'hole_spacing'] and s['names']['positions_from_width'], s
    assert s['first_build_right'] and s['edit_by_one_cell'], s


def test_holes_typed_as_plain_numbers_end_10_and_20_from_the_sides(tmp_path):
    from checker import holes, score_l4
    mh, mw = _build(tmp_path, plain=True)
    assert holes.check(score_l4._part(mh), holes.NAMES)['ok']
    c30 = holes.check(score_l4._part(mw), dict(holes.NAMES, width=30))
    assert not c30['centred'] and c30['hole_sides_mm'] == [[10.0, 20.0], [10.0, 20.0]]
    assert c30['fillet_on_lip_edge']
