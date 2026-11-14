# fx19 deviations (LAB-fx19 v1.1)

1. G0a step 1: FreeCAD 1.1.4's Python has no `SketchObject.movePoint`; the same call is `moveGeometry(GeoId, PointPos,
   Vector, relative)` (its own docstring: "Move a given point (or curve) to another location."). Used with the same
   arguments; the first g0a run stopped at that line before saving anything. The solver's DoF read from the
   sketch's `DoF` property after `solve()`.
2. G0b first container: the env line called the FreeCAD GUI binary with --version, which never returned; the
   container was killed with no stills. Fix 1: env from `freecadcmd --version` (env.txt).
3. G0b run 2 (G0/run2): the reader sent socket queries while the modal "Input error" box was up; they waited, then
   ran and printed their code in red into the Report view, and the box closed out of order. Fix 2 (the clean
   run, G0/g0b-*): the box closed by its own OK at the place run 1's still shows it, no query while it is up. Rule for
   the takes: no socket query while a modal box is open; every socket query adds "Python code executed
   successfully." to the Report view.
4. G0b: Validate Sketch started by its command (Sketcher_ValidateSketch) after the still of the open Sketch menu, not
   by clicking the menu item (an open menu blocks the socket). The takes click the item (offset from g0b-7).
5. G0b: the tree tooltip was not recorded (hover gave no popup on Xvfb; ToolTipRole empty). The tree icon's error mark is.
