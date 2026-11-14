# fx20 deviations (LAB-fx20 v1.1)

1. G0b attempt 1 (G0/b, kept): the Dimension shortcut was read before the Sketcher had loaded (empty), so no tool
   started; the script's Ctrl+A then selected every constraint. Fix 1: the shortcut read inside the sketch ("D"),
   no Ctrl+A. Attempt 2 (G0/b2): rung a 17 and 15 clean; "17 mm" typed after the selected number left "17 mm mm" in
   the field (FreeCAD read it as 17 mm). Takes type the number only. The notification button found by objectName
   "notificationArea" (status bar), not by class.
2. G0b attempt 3 (G0/b3) = the clean run with the Reference rung (box at its place in attempt 2's dialog still).
3. Labels as found (adapted, no design change): the popup has no "Value Error" caption (columns Type / Notifier /
   Message; Notifier "hook#Sketch"); the Python class shows only in the Report view ("<class 'ValueError'>").
   The Dimension tool on the horizontal arm top makes a DistanceX, not a Distance. The constraint index is 23.
   The reference size shows grey in brackets, "(15 mm)", not blue "15.00"; take C reads it in that form.
4. The G0 checkpoint with the planner was taken by the session brief (adapt labels, stop only for a design change);
   the takes went ahead after G0 without a separate PLAN rev 3 fill.
5. Take A ran once in full (A/). Its Esc after the list may not have turned the Dimension tool off (the status bar
   still reads "pick second point or edge, or click to finish" in A/unchanged.png); the sketch is unchanged (23).
6. Take B first run (B/attempt1, kept) and C after it (C/attempt1, kept): the bottom size's label sat below the
   visible 3D view (behind the Report dock), the double-click hit nothing, bottom stayed 25 (READ 8500.0). Fix 1
   (lab/fx20_BC.sh, pickup B + C in one container): starts at take A's end state (hook open, sketch in edit, not
   filmed), the Report view hidden, "Fit all" clicked on film first, places read live, a guard stops the take if no
   dialog opens. B: bottom 27, Fully constrained, Close, Pad 8700.0 on the console (B/volume.png). C: Reference ticked,
   no value typed: "(17 mm)" grey; bottom 30: "(20 mm)"; Ctrl+Z: back to 27 / "(17 mm)". xdotool printed "unknown
   opt" 3 times during the run (a mousemove argument); no step was missed (take logs).
7. Take D (D/): the four calls and replies filmed (terminal left); the planned FreeCAD full-window view of red-2 failed
   (the terminal stayed on top; D/red.png shows only the panel). Pickup D2 (D2/): FreeCAD alone, hook-red's sketch in
   edit by a lab query, Fit all, 10 s hold: "Over-constrained (3, 4, 5, and 13 more)", sketch small (Fit all on the
   whole document): zoom in the render. D note: through Python the added 15 size stays in the file after the failed
   setDatum (size-1/size-2: 24 constraints, solve -2, redundant), unlike the GUI, which undoes it.
8. Take E attempt 1 (E/attempt1, kept): the rectangle's far corner (42 mm right of the origin) fell on the task panel;
   no rectangle. Fix 1: the pan drag 250 px further left. E (final) ran once: DoF 0 after 40 and 20; top 41 refused
   "Negative datum values are not valid for the constraint with index 11" (not kept); Reference "(40 mm)"; Pad 10;
   the console prints 7999.999999999998, not 8000.0 (floating point; the script says "8000" or shows the line as is).
9. R1 ran once (claude-run/fx20run.sh -> lab/fx20_R1.sh, copied from fx19's with the strict MCP config; tools.txt
   parser now skips non-dict proxy lines). Claude Code was started before the recording, so its start banner (version,
   model, plan name, folder; no e-mail) is on screen from 0 s of runs/R1/screen.mp4: cut or crop it. pane-start.txt:
   the plan name replaced by "[plan]" before commit. session.jsonl: 14 context lines dropped by lab/fx19redact.py
   (kept 61). model.txt counts one "claude-opus-5-5" string: it sits in an api-request-shape line (dropped by the
   redaction), not in the turn; every assistant line is claude-sonnet-5-5.
10. Cost guard: lab/costguard.py (the live session-log guard, the FreeCAD lab's equivalent of SolidCraft's
   costguard6.py), cap $0.25; estimate $0.1853, not fired; /cost $0.1490 into ../freecad-course-BUDGET.tsv.
