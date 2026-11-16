# fc10 lab: deviations from PLAN rev 2 (16 Nov 2026)

1. **Volumes include the screw hole.** PLAN 2.2/2.3 say 8,500 / 10,500 / 12,500 mm3; with the 4.5 hole through the
   5 mm plate (79.52 mm3) the solids are 8,420.48 / 10,420.48 / 12,420.48. A plate that drifts so far that the hole
   misses it shows the hole-less number (12,500.00 at 100 in one headless try). Volume stays secondary (C12).
2. **The drop is not the same from try to try** (same file, same 60 -> 80): 1.32 (take A, 6 headless tries), 6.97 (GUI
   run 2, 2 headless tries), 10.39 (GUI run 1). Every try >= 1 mm, so T1 counts; the narration must say "this time"
   and never one number as "what FreeCAD does". At 100 headless: 19.23 (hole above the plate), 3.07, 3.07.
3. **Branch applied (PLAN 2.4): "T1 >= 1 mm but the stake not visible".** Take A, the only filmed trap take, dropped
   1.32 mm: the hole sits 13.68 below the top instead of 15 (about 24 px in the 9:16 crop, under 4 mm / 50 px). So the
   cold open (F0 / S0) uses take T (the T2 slip with the stake) and F7 keeps take A as "this time the size change
   moved it 1.32 mm"; F1 / S2 fallback uses take TB (the same drag on the pinned copy: nothing moves). Teacher +
   producer re-gate the changed frames (PLAN 6: F0, F1, F7/F8 per the branch, S0-S2, title 2, thumbnail). A was not
   re-filmed to get a bigger drop (that would pick the number).
4. **Pin route.** The corner sits exactly on the origin, so "click the corner, Ctrl-click the origin" deselects the
   corner (same spot), and tool-first clicks add nothing. Filmed route: drag a small box around the corner (selects
   the corner and the origin), then Coincident Constraint. F9 narration must change ("drag a small box around the
   corner: it picks the corner and the origin together").
5. **Measure is Position** (one click on the back corner): "X: 0.00 mm Y: -20.00 mm Z: -1.32 mm", signed. So the GUI
   itself shows "below the floor" (Z negative) on the bottom corner; the code inset still carries it on screen.
6. Take T first try (T-try1): the plate also slid 2.04 across, and both Measure clicks aimed at x = 0 missed the corner
   (Result "-"); fixed (the corner is read at XMin) and re-filmed as T. T-try1 kept as a record, not for the edit.
7. The panel truncates the link to "2 Degrees of Freedc" at the default panel width (full words read from the widget:
   "Under-constrained: " + "2 Degrees of Freedom"). The message zoom in F5 should show the full words: an overlay of
   the widget text or a wider panel at the script stage.
