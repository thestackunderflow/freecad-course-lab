# fc18 lab queries (exec'd inside FreeCAD by FQ18 after fc8q.py + fc9q.py), never filmed: numbers a person cannot see.
import json
import FreeCAD
import FreeCADGui
from PySide import QtCore, QtWidgets


def _viewer():
    vw = [w for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QWidget)
          if w.metaObject().className() == 'Gui::View3DInventorViewer' and w.isVisible()]
    return max(vw, key=lambda w: w.width() * w.height())


def skp(doc, sk, u, v):
    """screen "x y" of the sketch-local point (u, v) (works before any line exists)"""
    s = FreeCAD.getDocument(doc).getObject(sk)
    q = s.getGlobalPlacement().multVec(FreeCAD.Vector(u, v, 0))
    w = _viewer(); k = w.devicePixelRatioF(); gp = w.mapToGlobal(QtCore.QPoint(0, 0))
    av = FreeCADGui.getDocument(doc).activeView()
    x, y = av.getPointOnViewport(q)
    print('%d %d' % (round(gp.x() * k + x), round(gp.y() * k + av.getSize()[1] - y)))


def skview(doc, sk, u, v, height):
    """the camera (orientation kept) centred on sketch-local (u, v), `height` mm high"""
    s = FreeCAD.getDocument(doc).getObject(sk)
    c = s.getGlobalPlacement().multVec(FreeCAD.Vector(u, v, 0))
    av = FreeCADGui.getDocument(doc).activeView(); av.setAnimationEnabled(False)
    cam = av.getCameraNode()
    d = cam.orientation.getValue().multVec(__import__('pivy').coin.SbVec3f(0, 0, -1))
    p = c - FreeCAD.Vector(d[0], d[1], d[2]) * 200
    cam.position.setValue(p.x, p.y, p.z)
    if hasattr(cam, 'height'):
        cam.height.setValue(height)
    print('skview', u, v, height)


def skinfo(doc, sk='Sketch'):
    """the sketch: lines, constraints (type, value, driving, expression), DoF, solver lists"""
    d = FreeCAD.getDocument(doc); s = d.getObject(sk)
    if s is None:
        print(json.dumps({'sketch': None})); return
    s.solve()
    ex = dict(s.ExpressionEngine)
    cs = []
    for i, c in enumerate(s.Constraints):
        e = ex.get('.Constraints.%s' % c.Name) if c.Name else None
        e = e or ex.get('Constraints[%d]' % i) or ex.get('.Constraints[%d]' % i)
        cs.append([i, c.Type, c.First, round(c.Value, 3) if c.Type.startswith(('Dist', 'Radius', 'Diameter')) else None,
                   c.Driving, e])
    out = {'geo': [[round(g.StartPoint.x, 3), round(g.StartPoint.y, 3), round(g.EndPoint.x, 3), round(g.EndPoint.y, 3)]
                   for g in s.Geometry if hasattr(g, 'StartPoint')],
           'n_constraints': len(s.Constraints), 'constraints': cs,
           'dof': getattr(s, 'DoF', None),
           'support': [o.Name for o, _ in s.AttachmentSupport] if s.AttachmentSupport else None,
           'conflicts': list(getattr(s, 'ConflictingConstraints', []) or []),
           'redundant': list(getattr(s, 'RedundantConstraints', []) or []),
           'malformed': list(getattr(s, 'MalformedConstraints', []) or [])}
    print(json.dumps(out))


def cstate(doc):
    """the Body as FreeCAD holds it now: params, tip, outer / inner cylinder diameters (from the faces), volume, z"""
    d = FreeCAD.getDocument(doc); P = d.getObject('Params')
    b = [o for o in d.Objects if o.TypeId == 'PartDesign::Body'][0]
    pr = {n: float(P.get(n)) for n in ('cup_diameter', 'cup_height', 'wall')}
    st = {o.Name: list(o.State) for o in b.Group if o.TypeId.startswith(('PartDesign::', 'Sketcher::')) and
          list(o.State) != ['Up-to-date'] and list(o.State) != []}
    s = b.Shape
    out = {'params': pr, 'tip': b.Tip.Name if b.Tip else None, 'state': st, 'body': b.Label}
    if not s.isNull() and s.Solids:
        rs = sorted({round(f.Surface.Radius, 4) for f in s.Faces if 'Cylinder' in type(f.Surface).__name__})
        bb = s.BoundBox
        out.update({'solids': len(s.Solids), 'volume': round(s.Volume, 3), 'outside': round(2 * rs[-1], 3) if rs else None,
                    'inside': round(2 * rs[0], 3) if len(rs) > 1 else None, 'z': [round(bb.ZMin, 3), round(bb.ZMax, 3)]})
    print(json.dumps(out))


def wincheck():
    """visible top-level windows / dialogs: title + labels + field texts (no lab query while a modal box is up)"""
    out = []
    for w in QtWidgets.QApplication.topLevelWidgets():
        if w.isVisible() and w is not FreeCADGui.getMainWindow():
            t = [x.text()[:60] for x in w.findChildren(QtWidgets.QLabel) if x.isVisible() and x.text()]
            f = [x.text()[:60] for x in w.findChildren(QtWidgets.QLineEdit) if x.isVisible()]
            out.append([w.windowTitle(), w.metaObject().className(), t[:12], f[:6]])
    print(json.dumps(out))


def cmdinfo(name):
    c = FreeCADGui.Command.get(name)
    print(json.dumps(c.getInfo() if c else None))
