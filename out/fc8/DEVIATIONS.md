# fc8 deviations (14 Nov 2026)

1. freecad-mcp **0.1.28** (image `fcc-app:1.1.4-0.1.28`, as fc1-fc7 filmed), not 0.1.31 as PLAN 4.B2.3 says. No new
   image was built for this stage. Task R covers the 0.1.31 facts.
2. Parts are Part Design **boxes** driven by the spreadsheet `Params` (lib `lab/fc8parts.py`), not lesson 3's sketch
   hook. Same outline and sizes as sc8: hook 17,260 / rail 12,000 mm3 at gap 0, the same as SolidCraft.
3. PLAN F7 "click a face on each part": not filmed. The slider picks are the **two components in the tree** (Ctrl for the
   second). Faces were not tried in the GUI. Assembly's own code puts a flat face's joint axis on its normal.
4. "Common" is labelled **Intersection** in FreeCAD 1.1 (command Part_Common; the result object is still called "Common").
   The volume comes from **Check Geometry > Expand shape content > Run check**, then fold "Check Geometry Results" and
   open "Shape Content". The takes run Intersection on the two bodies outside the assembly: in G0, Intersection on the
   two components moved them under Common.
5. Take A: try 1 folded the wrong place, so Shape Content was empty on screen (out/fc8/A-try1, video deleted). Fix 1:
   click the panel labels found by query. Take B: try 1's down-drag grabbed a point off screen and the hook did not move
   (B-try1). Fix 1: fit the view before each drag. Take D: try 1's right side was measured off screen because the view
   stayed zoomed (D-try1). Fix 1: bottom view + fit before each side. Take E: try 1 broke because I edited the take
   script while it ran, so no logs were finalised (E-try1). Re-filmed; that redo was not a fix attempt.
6. In the filmed takes the workbench switch to Assembly is done by a lab query (an open workbench list blocks the
   add-on's socket). The cut shows the switch as a jump. The hook's start colours (orange / blue-grey) and the red of
   the Intersection result are also set by query.
7. Measure: one side per click pair (bottom view, 14 wheel steps of zoom, the slot's wall edge then Ctrl + the rib's
   wall edge). Both sides were filmed (D: left 0.40 mm, right 0.40 mm).
8. Claude runs: **B1's run cap was raised to $0.36** (the $0.361 left of the $0.60 total after A1). Both runs were still
   stopped by the live guard, whose estimate runs ~25-30% above /cost (A1 estimate 0.3094 vs /cost 0.2390; B1 0.3694 vs
   0.2846). No reruns. Stage total $0.5236 of $0.60.
9. The plan name stays in Claude Code's **welcome header** (pane line 3), not a ~24 s banner: it was still there after the
   30 s wait in both runs, so it is in the first part of both runs' screen.mp4. Render: crop or cover the terminal's
   top rows (the fx20 `ov-r1-top` overlay pattern) until the header scrolls off. In the stored pane files it is
   replaced with "[plan redacted]". The session logs were redacted with lab/fx19redact.py (15 and 16 lines dropped).
   After that, a grep of out/fc8 for the connector strings and the plan name finds nothing.
10. B1's launcher shell was stopped by Claude Code for host memory pressure while the run was going. The container was
    not affected and finished on its own; the ledger row, scrub and meta.json were all written. No rerun.
11. Q4 (STL export + PrusaSlicer, F20) was not run in this stage.
