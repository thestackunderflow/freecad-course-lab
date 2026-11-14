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
