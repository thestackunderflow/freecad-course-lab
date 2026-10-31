"""Lesson 5: measure an STL file with no CAD and no AI (plain Python + numpy), the same way for the by-hand files,
Claude's file and the replay's file.

    python3 -m checker.mesh5 FILE.stl [OUT.json]

Reads binary or ASCII STL. Reports: triangles, volume (signed tetrahedra, mm³), bounding box, closed (every edge
shared by exactly two triangles, in opposite directions), parts (triangles joined through shared edges), and the
course hook's two screw holes: for each hole axis (along X through the back plate, at the lesson 4 positions, or given),
the number of flat sides, the corner diameter (vertices) and the flat-to-flat diameter (the facet planes' distance)."""
import json
import math
import struct
import sys

import numpy as np

# the hook at 30 wide (lesson 4's width30): holes through the plate (x 0..5) along X, at y = -15, z = 15 and 45
HOLE_AXES = ((-15.0, 15.0), (-15.0, 45.0))
PLATE_X = (0.0, 5.0)
HOLE_R = 2.0
Q = 1e-4   # vertex weld tolerance (mm) for edge matching


def read(path):
    data = open(path, 'rb').read()
    if len(data) >= 84:
        n = struct.unpack('<I', data[80:84])[0]
        if 84 + 50 * n == len(data):
            arr = np.frombuffer(data, dtype=np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]),
                                count=n, offset=84)
            return arr['v'].astype(np.float64)
    tris, cur = [], []
    for ln in data.decode('utf-8', 'replace').splitlines():
        p = ln.split()
        if p and p[0] == 'vertex':
            cur.append([float(x) for x in p[1:4]])
            if len(cur) == 3:
                tris.append(cur)
                cur = []
    return np.array(tris, dtype=np.float64).reshape(-1, 3, 3)


def volume(t):
    return float(np.einsum('ij,ij->i', t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6.0)


def _keys(t):
    return np.round(t / Q).astype(np.int64)


def edges_report(t):
    """closed: every undirected edge used exactly twice, once in each direction; parts by shared edges."""
    k = _keys(t)
    idx = {}
    vid = np.empty(k.shape[:2], dtype=np.int64)
    for i in range(k.shape[0]):
        for j in range(3):
            vid[i, j] = idx.setdefault(tuple(k[i, j]), len(idx))
    directed = {}
    for i in range(len(vid)):
        for a, b in ((0, 1), (1, 2), (2, 0)):
            e = (vid[i, a], vid[i, b])
            directed.setdefault(e, []).append(i)
    und = {}
    for (a, b), fs in directed.items():
        und.setdefault((min(a, b), max(a, b)), []).append(((a, b), fs))
    open_edges = nonmanifold = flipped = 0
    parent = list(range(len(vid)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for (a, b), uses in und.items():
        count = sum(len(fs) for _, fs in uses)
        if count == 1:
            open_edges += 1
        elif count > 2:
            nonmanifold += 1
        elif len(uses) == 1:          # both triangles use the edge in the same direction
            flipped += 1
        faces = [f for _, fs in uses for f in fs]
        for f in faces[1:]:
            parent[find(f)] = find(faces[0])
    degenerate = int((np.linalg.norm(np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]), axis=1) < 1e-12).sum())
    parts = len({find(i) for i in range(len(vid))})
    return {'open_edges': open_edges, 'nonmanifold_edges': nonmanifold, 'flipped_edges': flipped,
            'degenerate': degenerate, 'parts': parts, 'points': len(idx),
            'closed': open_edges == 0 and nonmanifold == 0 and flipped == 0}


def hole(t, cy, cz, r=HOLE_R, x=PLATE_X):
    """The hole wall: triangles inside the plate, near radius r, facing sideways."""
    c = t.mean(axis=1)
    rr = np.hypot(c[:, 1] - cy, c[:, 2] - cz)
    n = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0])
    ln = np.linalg.norm(n, axis=1)
    ok = ln > 1e-12
    n[ok] /= ln[ok, None]
    wall = ok & (c[:, 0] > x[0]) & (c[:, 0] < x[1]) & (rr < r * 1.15) & (np.abs(n[:, 0]) < 0.01)
    if not wall.any():
        return {'found': False, 'sides': 0, 'corner_d': None, 'flat_d': None}
    w = t[wall]
    pts = w.reshape(-1, 3)
    ang = np.round(np.degrees(np.arctan2(pts[:, 2] - cz, pts[:, 1] - cy)), 3) % 360.0
    sides = len(set(ang.tolist()))
    corner = float(np.hypot(pts[:, 1] - cy, pts[:, 2] - cz).max())
    nn = n[wall]
    d = np.abs(nn[:, 1] * (w[:, 0, 1] - cy) + nn[:, 2] * (w[:, 0, 2] - cz))
    return {'found': True, 'sides': sides, 'corner_d': round(2 * corner, 4), 'flat_d': round(2 * float(d.min()), 4)}


def measure(path, axes=HOLE_AXES):
    t = read(path)
    lo, hi = t.reshape(-1, 3).min(axis=0), t.reshape(-1, 3).max(axis=0)
    out = {'file': path.replace('\\', '/').split('/')[-1], 'triangles': int(len(t)), 'volume_mm3': round(volume(t), 3),
           'bbox_mm': [round(float(v), 4) for v in hi - lo], 'min_mm': [round(float(v), 4) + 0.0 for v in lo]}
    out.update(edges_report(t))
    out['holes'] = [dict(hole(t, cy, cz), axis_yz=[cy, cz]) for cy, cz in axes]
    return out


def _turns():
    """The 24 proper axis-aligned rotations (identity first)."""
    import itertools
    out = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            m = np.zeros((3, 3))
            for r, (c, sg) in enumerate(zip(perm, signs)):
                m[r, c] = sg
            if round(np.linalg.det(m)) == 1:
                out.append(m)
    out.sort(key=lambda m: 0 if np.allclose(m, np.eye(3)) else 1)
    return out


BOX = (40.0, 30.0, 60.0)
BOX_MIN = (0.0, -30.0, 0.0)


def measure_any(path, axes=HOLE_AXES):
    """measure(), but if the part was turned or moved (a run may lay it down "for printing"), try the 24 axis-aligned
    turns, shift each to the lesson's box corner, and read the holes there. moved = not the identity at the corner."""
    t0 = read(path)
    base = measure(path, axes)
    for k, m in enumerate(_turns()):
        t = t0 @ m.T
        lo, hi = t.reshape(-1, 3).min(axis=0), t.reshape(-1, 3).max(axis=0)
        if not all(abs((hi - lo)[i] - BOX[i]) <= 0.02 for i in range(3)):
            continue
        t = t + (np.array(BOX_MIN) - lo)
        hs = [dict(hole(t, cy, cz), axis_yz=[cy, cz]) for cy, cz in axes]
        if all(h['found'] for h in hs):
            moved = not (k == 0 and np.allclose(lo, BOX_MIN, atol=0.02))
            return dict(base, holes=hs, moved=moved, turn=m.astype(int).tolist())
    return dict(base, moved=None, turn=None)


def flat_d(d, sides):
    """Flat-to-flat size of a regular polygon whose corners sit on a circle of diameter d."""
    return d * math.cos(math.pi / sides)


if __name__ == '__main__':
    r = measure(sys.argv[1])
    s = json.dumps(r, indent=1)
    if len(sys.argv) > 2:
        open(sys.argv[2], 'w').write(s)
    print(s)
